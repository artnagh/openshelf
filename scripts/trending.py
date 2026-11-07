"""OpenShelf trending bot.

Finds new, fast-growing open-source repos on GitHub every day, scores them and writes
data/trending.json. With --components it also pulls Claude skills / agents / commands from
permissively licensed trending repos (text files only, via the GitHub API: nothing is executed)
into data/components/.

Token: GITHUB_TOKEN env var (GitHub Actions provides it) or `gh auth token`.
Usage: python3 scripts/trending.py [--components]
"""
import json, os, re, sys, math, time, datetime, subprocess, urllib.request, urllib.parse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
TODAY = datetime.date.today()
TOKEN = os.environ.get("GITHUB_TOKEN") or subprocess.run(["gh", "auth", "token"], capture_output=True, text=True).stdout.strip()
import ssl
try:
    import certifi; _CTX = ssl.create_default_context(cafile=certifi.where())
except ImportError:
    _CTX = ssl.create_default_context(cafile="/etc/ssl/cert.pem") if os.path.exists("/etc/ssl/cert.pem") else ssl.create_default_context()
_open = lambda req, timeout=30: urllib.request.urlopen(req, timeout=timeout, context=_CTX)
PERMISSIVE = ("MIT", "Apache", "BSD", "ISC", "CC0", "Unlicense", "0BSD", "MPL", "Zlib")

def api(path):
    req = urllib.request.Request("https://api.github.com/" + path, headers={
        "Accept": "application/vnd.github+json", "User-Agent": "openshelf-trending-bot",
        **({"Authorization": f"Bearer {TOKEN}"} if TOKEN else {})})
    for attempt in range(3):
        try:
            with _open(req) as r:
                return json.load(r)
        except urllib.error.HTTPError as ex:
            if ex.code in (403, 429) and attempt < 2:
                time.sleep(30); continue
            if ex.code in (404, 409, 422): return None
            raise
    return None

def search(q, pages=3):
    out = []
    for p in range(1, pages + 1):
        j = api("search/repositories?" + urllib.parse.urlencode({"q": q, "sort": "stars", "order": "desc", "per_page": 100, "page": p}))
        if not j or not j.get("items"): break
        out += j["items"]
        time.sleep(2)  # search API: 30 requests/min
    return out

d = lambda n: (TODAY - datetime.timedelta(days=n)).isoformat()
QUERIES = [
    (f"created:>{d(30)} stars:>150", 3),
    (f"created:>{d(7)} stars:>40", 2),
    (f"created:>{d(120)} stars:>800 topic:claude-code", 1),
    (f"created:>{d(120)} stars:>800 topic:mcp", 1),
    (f"created:>{d(120)} stars:>1500 topic:ai-agents", 1),
    (f"created:>{d(120)} stars:>1500 topic:llm", 1),
    (f"created:>{d(120)} stars:>1500 topic:self-hosted", 1),
]

# keyword -> site category (same keys as i18n.CATS)
CAT_RULES = [
    ("Skills & MCP", ["claude-code", "claude-skills", "mcp", "skill", "model-context-protocol"]),
    ("AI Agents", ["agent", "agents", "agentic", "autonomous"]),
    ("Image/Video/Audio AI", ["image", "video", "audio", "tts", "speech", "diffusion", "voice"]),
    ("Security", ["security", "pentest", "vulnerability", "osint"]),
    ("Trading & Finance", ["trading", "finance", "crypto", "stock", "quant"]),
    ("Self-Hosted Apps", ["self-hosted", "selfhosted", "homelab"]),
    ("Automation", ["automation", "workflow", "scraper", "crawler", "rpa"]),
    ("Data & Databases", ["database", "sql", "vector-database", "etl", "analytics"]),
    ("Game Dev", ["game", "gamedev", "game-engine"]),
    ("Developer Tools", ["cli", "developer-tools", "devtools", "ide", "terminal", "vscode"]),
    ("Machine Learning", ["machine-learning", "deep-learning", "pytorch", "training", "dataset"]),
    ("LLM & GenAI", ["llm", "gpt", "rag", "chatbot", "genai", "inference", "deepseek", "openai"]),
    ("Web & Frameworks", ["react", "nextjs", "framework", "web", "frontend"]),
    ("Productivity Apps", ["notes", "productivity", "calendar", "todo"]),
]
def guess_cat(it):
    hay = " ".join(it.get("topics") or []) + " " + (it.get("description") or "").lower() + " " + it["name"].lower()
    for cat, kws in CAT_RULES:
        if any(k in hay for k in kws): return cat
    return "General / Other"

def guess_type(cat):
    return {"Skills & MCP": "Skill / MCP", "AI Agents": "Agent", "Machine Learning": "Model / ML", "Web & Frameworks": "Library / Framework"}.get(cat, "App / Tool")

def main():
    hist_p = os.path.join(DATA, "trending_history.json")
    hist = json.load(open(hist_p)) if os.path.exists(hist_p) else {}
    top1000 = {r["repo"].lower() for r in json.load(open(os.path.join(DATA, "repos.json")))}
    seen = {}
    for q, pages in QUERIES:
        for it in search(q, pages):
            if it.get("fork") or it.get("archived"): continue
            seen[it["full_name"].lower()] = it
    rows = []
    for key, it in seen.items():
        created = it["created_at"][:10]
        age = max(1, (TODAY - datetime.date.fromisoformat(created)).days)
        stars = it["stargazers_count"]
        h = hist.get(key, [])
        prev = next((s for dt, s in reversed(h) if dt < TODAY.isoformat()), None)
        gained = stars - prev if prev is not None else None
        spd = stars / age
        days_upd = (TODAY - datetime.date.fromisoformat(it["pushed_at"][:10])).days
        # power score 0-100: speed (stars/day), size, freshness
        score = min(100, round(16 * math.log10(1 + spd) + 5 * math.log10(1 + stars) + (10 if days_upd <= 2 else 4 if days_upd <= 7 else 0), 1))
        cat = guess_cat(it)
        lic = (it.get("license") or {}).get("spdx_id") or ""
        why = ["actively updated"] if days_upd <= 7 else []
        if spd > 500: why.append("very fast growth")
        elif spd > 50: why.append("fast growth")
        if stars > 10000: why.append("huge community")
        if cat in ("AI Agents", "Skills & MCP", "LLM & GenAI"): why.append("hot AI trend")
        rows.append(dict(repo=it["full_name"], link=it["html_url"], desc=it.get("description") or "", stars=stars, forks=it["forks_count"],
                         spy=round(spd * 365), lang=it.get("language") or "", license=lic, created=created, updated=it["pushed_at"][:10],
                         days=days_upd, size_mb=round(it["size"] / 1024, 1), score=score, category=cat, type=guess_type(cat),
                         why=", ".join(why), spd=round(spd, 1), gained_24h=gained, first_seen=(h[0][0] if h else TODAY.isoformat()),
                         in_top1000=key in top1000, topics=it.get("topics") or []))
        h = [x for x in h if x[0] != TODAY.isoformat()] + [[TODAY.isoformat(), stars]]
        hist[key] = h[-30:]
    rows.sort(key=lambda r: -r["score"])
    rows = rows[:200]
    for i, r in enumerate(rows, 1):
        r["trend_rank"] = i
        r["tier"] = "S" if r["score"] >= 80 else "A" if r["score"] >= 65 else "B" if r["score"] >= 50 else "C"
        r["rank"] = f"T{i}"
    json.dump({"generatedAt": TODAY.isoformat(), "count": len(rows), "repos": rows}, open(os.path.join(DATA, "trending.json"), "w"), ensure_ascii=False, indent=0)
    json.dump(hist, open(hist_p, "w"), separators=(",", ":"))
    new_today = sum(1 for r in rows if r["first_seen"] == TODAY.isoformat())
    print(f"trending: {len(rows)} repos ({new_today} first seen today) from {len(seen)} candidates")
    if "--components" in sys.argv: pull_components(rows)

def fm(text):
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, re.S)
    if not m: return {}, text
    meta = {}
    for line in m.group(1).splitlines():
        mm = re.match(r"^([A-Za-z_-]+):\s*(.*)$", line)
        if mm: meta[mm.group(1).lower()] = mm.group(2).strip().strip("\"'")
    return meta, text[m.end():]

LOC = re.compile(r"^[a-z]{2}[-_][A-Za-z]{2,4}$")
SKIP = {"node_modules", "dist", "build", "vendor", "test", "tests", "fixtures", "i18n", "locales", "translations"}

def pull_components(rows):
    outdir = os.path.join(DATA, "components")
    os.makedirs(outdir, exist_ok=True)
    added = 0
    for r in rows:
        if not r["license"].startswith(PERMISSIVE) or r["size_mb"] > 800: continue
        shard = os.path.join(outdir, r["repo"].replace("/", "__") + ".json")
        if os.path.exists(shard) and os.path.getmtime(shard) > time.time() - 6 * 86400: continue  # refresh weekly
        tree = api(f"repos/{r['repo']}/git/trees/HEAD?recursive=1")
        if not tree or "tree" not in tree: continue
        items, seen = [], set()
        for node in tree["tree"]:
            p = node["path"]
            if node["type"] != "blob" or not p.endswith(".md") or node.get("size", 0) > 200_000: continue
            parts = p.split("/")
            if any(x in SKIP or LOC.match(x) for x in parts[:-1]): continue
            fn = parts[-1]
            kind = "skill" if fn == "SKILL.md" else "agent" if len(parts) > 1 and parts[-2] == "agents" and fn.lower() != "readme.md" \
                else "command" if len(parts) > 1 and parts[-2] == "commands" and fn.lower() != "readme.md" else None
            if not kind: continue
            if len(items) >= 300: break
            try:
                raw = _open(urllib.request.Request(f"https://raw.githubusercontent.com/{r['repo']}/HEAD/{urllib.parse.quote(p)}",
                                             headers={"User-Agent": "openshelf-trending-bot"})).read().decode("utf-8", "replace")
            except Exception:
                continue
            meta, body = fm(raw)
            name = meta.get("name") or (parts[-2] if kind == "skill" and len(parts) > 1 else fn[:-3])
            desc = meta.get("description", "")
            if (kind != "skill" and not desc) or len(body.strip()) < 80: continue
            slug = re.sub(r"[^a-z0-9-]+", "-", name.lower()).strip("-")[:60] or "item"
            if (kind, slug) in seen: continue
            seen.add((kind, slug))
            path = "/".join(parts[:-1]) if kind == "skill" else p
            items.append(dict(kind=kind, name=name, slug=slug, description=desc[:400], repo=r["repo"], license=r["license"],
                              path=path, category=r["category"], content=raw[:60_000]))
        if items:
            json.dump(items, open(shard, "w"), ensure_ascii=False)
            added += len(items)
            print(f"  + {len(items):4d} components from {r['repo']}")
    print(f"components pulled from trending repos: {added}")

if __name__ == "__main__":
    main()
