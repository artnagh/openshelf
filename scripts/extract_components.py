"""Extract Claude Code skills / agents / commands from the Repo 2030 archive.
Only repos with a permissive license are used. Reads files as text only (never runs them).
Usage: python3 -I extract_components.py <archive_root> <xlsx> <out_dir: data/components>"""
import sys, os, re, json, subprocess, openpyxl
root, xlsx, out = sys.argv[1:4]
OK = ("MIT", "Apache", "BSD", "ISC", "CC0", "Unlicense", "0BSD", "MPL")
lic = {}
ws = openpyxl.load_workbook(xlsx, read_only=True)["Top 1000"]
for r in list(ws.iter_rows(values_only=True))[1:]:
    if r[1]: lic[r[1].replace("/", "__").lower()] = (r[1], r[10] or "")
SKIP = {"node_modules", ".git", "dist", "build", "vendor", "__pycache__", "test", "tests", "fixtures", "examples-broken"}
def fm(text):
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, re.S)
    if not m: return {}, text
    meta = {}
    for line in m.group(1).splitlines():
        mm = re.match(r"^([A-Za-z_-]+):\s*(.*)$", line)
        if mm: meta[mm.group(1).lower()] = mm.group(2).strip().strip('"\'')
    return meta, text[m.end():]
items, seen = [], set()
for cat in sorted(os.listdir(root)):
    cp = os.path.join(root, cat)
    if not os.path.isdir(cp) or not cat[:2].isdigit(): continue
    for repo in sorted(os.listdir(cp)):
        full, L = lic.get(repo.lower(), (repo.replace("__", "/"), ""))
        if not any(L.startswith(o) for o in OK): continue
        rp = os.path.join(cp, repo)
        try:
            files = subprocess.run(["git", "-c", "core.fsmonitor=false", "-c", "core.hooksPath=/dev/null", "-C", rp, "ls-files", "-z"], capture_output=True, timeout=60).stdout.decode("utf-8", "replace").split("\0")
        except Exception:
            continue
        for f in files:
            if not f.endswith(".md"): continue
            parts = f.split("/")
            if any(x in SKIP for x in parts[:-1]): continue
            fn, rel = parts[-1], "/".join(parts[:-1]) or "."
            dp = os.path.join(rp, rel)
            if True:
                kind = None
                if fn == "SKILL.md": kind = "skill"
                elif fn.lower() != "readme.md" and len(parts) > 1:
                    if parts[-2] == "agents": kind = "agent"
                    elif parts[-2] == "commands": kind = "command"
                if not kind: continue
                p = os.path.join(dp, fn)
                try:
                    if os.path.getsize(p) > 200_000: continue
                    text = open(p, encoding="utf-8", errors="replace").read()
                except OSError: continue
                meta, body = fm(text)
                name = meta.get("name") or (os.path.basename(dp) if kind == "skill" else fn[:-3])
                desc = meta.get("description", "")
                if kind != "skill" and not desc: continue  # agents/commands need frontmatter
                if len(body.strip()) < 80: continue
                slug = re.sub(r"[^a-z0-9-]+", "-", name.lower()).strip("-")[:60] or "item"
                key = (kind, full.lower(), slug)
                if key in seen: continue
                seen.add(key)
                relpath = os.path.relpath(dp if kind == "skill" else p, rp).replace("\\", "/")
                items.append(dict(kind=kind, name=name, slug=slug, description=desc[:400], repo=full,
                                  license=L, path=relpath, category=cat[5:], content=text[:60_000]))
os.makedirs(out, exist_ok=True)
for f in os.listdir(out):
    if f.endswith(".json"): os.remove(os.path.join(out, f))
by = {}
for i in items: by.setdefault(i["repo"], []).append(i)
for r, its in by.items():
    json.dump(its, open(os.path.join(out, r.replace("/", "__") + ".json"), "w"), ensure_ascii=False)
from collections import Counter
print(len(items), Counter(i["kind"] for i in items), len({i["repo"] for i in items}), "repos")
