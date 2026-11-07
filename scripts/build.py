"""Build the OpenShelf static site into ./site.

python3 scripts/build.py            # full build (needs data/repos.json + data/components.json)
Data files are created by scripts/import_repos.py and scripts/extract_components.py.
"""
import json, os, re, shutil, html, random, datetime, sys
sys.path.insert(0, os.path.dirname(__file__))
from i18n import LANGS, LANG_NAMES, RTL, T, CATS

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "site")
CFG = json.load(open(os.path.join(ROOT, "config.json")))
BASE = CFG["base_url"].rstrip("/")
NAME = CFG["site_name"]
GH = CFG["github_repo"]
TODAY = datetime.date.today()
e = html.escape
BP = CFG.get("path_prefix", "").rstrip("/")
def fix(txt):
    """Prefix root-relative URLs when the site is served from a subfolder (GitHub Pages project site)."""
    if not BP: return txt
    for a in ('href="/', 'src="/', "url(/", "fetch('/", 'action="/'):  # also covers data-href / data-src
        txt = txt.replace(a, a[:-1] + BP + "/")
    return txt.replace(f'{BP}//', '//')

repos = json.load(open(os.path.join(ROOT, "data", "repos.json")))
import hashlib
_cd = os.path.join(ROOT, "data", "components")
_raw = [x for f in sorted(os.listdir(_cd)) if f.endswith(".json") for x in json.load(open(os.path.join(_cd, f)))] if os.path.isdir(_cd) else []
_rank = {r["repo"].lower(): r["rank"] for r in repos}
_excl = {x.lower() for x in CFG.get("exclude_repos", [])}
_raw.sort(key=lambda x: (_rank.get(x["repo"].lower(), 9999), x["kind"], x["slug"]))
_LOC = re.compile(r"^[a-z]{2}[-_][A-Za-z]{2,4}$")
_LOCW = {"i18n", "l10n", "locales", "locale", "translations", "translated", "zh", "ja", "ko", "ru", "pt", "it", "tr", "vi", "th", "pl", "nl", "uk", "fa", "he", "hi", "es", "fr", "de", "ar", "id", "cn", "jp", "kr"}
comps, _seen = [], set()
for x in _raw:
    if x["repo"].lower() in _excl: continue
    if any(_LOC.match(seg) or seg.lower() in _LOCW for seg in x["path"].split("/")): continue
    h = hashlib.md5(x["content"].strip().encode()).hexdigest()
    if h in _seen: continue
    _seen.add(h); comps.append(x)

def slug(s): return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")
CAT_SLUG = {c: slug(CATS[c]["en"]) for c in CATS}
KIND_DIR = {"skill": "skills", "agent": "agents", "command": "commands"}

# ---------- data prep ----------
_tp = os.path.join(ROOT, "data", "trending.json")
TREND = json.load(open(_tp)) if os.path.exists(_tp) else {"generatedAt": "", "repos": []}
trending = TREND["repos"]
_SHOW_NEW = any(r.get("first_seen") != TREND.get("generatedAt") for r in trending)  # not on the bot's first day
_known = {r["repo"].lower() for r in repos}
extra_repos = [r for r in trending if r["repo"].lower() not in _known and r["category"] in CATS]
by_name = {r["repo"].lower(): r for r in repos + extra_repos}
for c in comps:
    c["id"] = f'{KIND_DIR[c["kind"]]}/{c["repo"].replace("/", "__").lower()}/{c["slug"]}'
    owner_repo = c["repo"]
    if c["kind"] == "skill":
        c["install"] = f'npx degit {owner_repo}/{c["path"]} .claude/skills/{c["slug"]}'
        c["install_user"] = f'npx degit {owner_repo}/{c["path"]} ~/.claude/skills/{c["slug"]}'
    else:
        d = KIND_DIR[c["kind"]]
        raw = f'https://raw.githubusercontent.com/{owner_repo}/HEAD/{c["path"]}'
        c["install"] = f'curl -fsSL --create-dirs -o .claude/{d}/{c["slug"]}.md {raw}'
        c["install_user"] = f'curl -fsSL --create-dirs -o ~/.claude/{d}/{c["slug"]}.md {raw}'
    c["src_url"] = f'https://github.com/{owner_repo}/tree/HEAD/{c["path"]}'
_trank = {r["repo"].lower(): i for i, r in enumerate(trending)}
_rank.update({k: 5000 + v for k, v in _trank.items() if k not in _rank})
comps_by_repo = {}
for c in sorted(comps, key=lambda c: ("skill", "agent", "command").index(c["kind"])): comps_by_repo.setdefault(c["repo"].lower(), []).append(c)
cats_count = {}
for r in repos: cats_count[r["category"]] = cats_count.get(r["category"], 0) + 1
CAT_ORDER = sorted(cats_count, key=lambda c: -cats_count[c])

def fmt(n):
    n = int(n or 0)
    if n >= 1_000_000: return f"{n/1_000_000:.1f}M"
    if n >= 1000: return f"{n/1000:.1f}k".replace(".0k", "k")
    return str(n)

def lic_kind(l):
    l = (l or "").upper()
    if any(l.startswith(x) for x in ("MIT", "APACHE", "BSD", "ISC", "CC0", "UNLICENSE", "0BSD", "MPL", "ZLIB")): return "lic_permissive"
    if "GPL" in l: return "lic_copyleft"
    return "lic_other"

def pre(lang): return "" if lang == "en" else f"/{lang}"
def url(lang, path): return f"{pre(lang)}{path}"

# ---------- background: colourful contribution-grid mosaic ----------
def make_bg():
    """Rows of colourful book spines on shelves (fits the OpenShelf name)."""
    rnd = random.Random(2030)
    pal = ["#3a5bff", "#ff6b4a", "#12b886", "#f7b32b", "#7950f2", "#15aabf", "#e64980", "#0b1b33", "#94d82d"]
    W, shelf_h, rows = 1700, 150, 4
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{shelf_h*rows}">']
    for row in range(rows):
        base = (row + 1) * shelf_h - 12
        x = rnd.randint(0, 30)
        while x < W:
            w = rnd.choice([14, 18, 22, 26, 30, 34])
            h = rnd.randint(70, 128)
            col = rnd.choice(pal)
            if rnd.random() < 0.12:  # leaning book
                parts.append(f'<rect x="{x}" y="{base-h}" width="{w}" height="{h}" rx="3" fill="{col}" transform="rotate(-12 {x+w} {base})"/>')
                x += w + 14; continue
            parts.append(f'<rect x="{x}" y="{base-h}" width="{w}" height="{h}" rx="3" fill="{col}"/>')
            if w >= 22:
                parts.append(f'<rect x="{x+4}" y="{base-h+14}" width="{w-8}" height="3" rx="1.5" fill="#fff" opacity=".55"/>')
                parts.append(f'<rect x="{x+4}" y="{base-22}" width="{w-8}" height="3" rx="1.5" fill="#fff" opacity=".35"/>')
            x += w + rnd.choice([2, 3, 4])
            if rnd.random() < 0.06: x += rnd.randint(30, 80)  # gap on the shelf
        parts.append(f'<rect x="0" y="{base}" width="{W}" height="8" rx="2" fill="#0b1b33" opacity=".25"/>')
    parts.append("</svg>")
    return "".join(parts)

CSS = """
:root{--bg:#f7f8fc;--fg:#0b1b33;--mut:#566179;--line:#e3e7f0;--card:#ffffff;--acc:#3a5bff;--acc2:#ff6b4a;--code:#eef1f8}
[data-theme=dark]{--bg:#0a0f1c;--fg:#e8ecf6;--mut:#94a0ba;--line:#1d2638;--card:#111829;--acc:#7b93ff;--acc2:#ff8a6e;--code:#161f33}
*{box-sizing:border-box}html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--bg);color:var(--fg);font:16px/1.6 Geist,system-ui,-apple-system,Segoe UI,Roboto,sans-serif;position:relative;min-height:100vh}
[dir=rtl] body{font-family:Geist,"Noto Sans Arabic",Tahoma,system-ui,sans-serif}
.bg{position:absolute;inset:0 0 auto 0;height:600px;background:url(/assets/bg.svg) top right/1700px auto no-repeat;
 -webkit-mask-image:radial-gradient(ellipse 70% 95% at 100% 0,#000 0,rgba(0,0,0,.5) 35%,transparent 72%);mask-image:radial-gradient(ellipse 70% 95% at 100% 0,#000 0,rgba(0,0,0,.5) 35%,transparent 72%);pointer-events:none;z-index:0;opacity:.8}
[dir=rtl] .bg{background-position:top left;-webkit-mask-image:radial-gradient(ellipse 70% 95% at 0 0,#000 0,rgba(0,0,0,.5) 35%,transparent 72%);mask-image:radial-gradient(ellipse 70% 95% at 0 0,#000 0,rgba(0,0,0,.5) 35%,transparent 72%)}
[data-theme=dark] .bg{opacity:.5}
.wrap{max-width:1160px;margin:0 auto;padding:0 20px;position:relative;z-index:1}
a{color:inherit;text-decoration:none}a:hover{color:var(--acc)}
header.top{display:flex;align-items:center;gap:18px;padding:16px 0}
.logo{font-weight:700;font-size:20px;letter-spacing:-.02em;display:flex;align-items:center;gap:9px}
.logo i{display:inline-flex;align-items:flex-end;gap:2px;height:20px}.logo i b{width:5px;border-radius:2px;background:var(--acc);height:20px}.logo i b:nth-child(2){background:var(--acc2);height:15px}.logo i b:nth-child(3){background:#12b886;height:18px}.logo i b:nth-child(4){background:#f7b32b;height:13px;transform:rotate(-14deg);transform-origin:bottom right}
nav.main{display:flex;gap:18px;flex-wrap:wrap;font-size:15px;color:var(--mut)}
.sp{flex:1}
.ctl{display:flex;gap:8px;align-items:center}
select,button.tg{background:var(--card);color:var(--fg);border:1px solid var(--line);border-radius:10px;padding:6px 10px;font:inherit;font-size:14px;cursor:pointer}
.hero{padding:58px 0 30px;max-width:760px}
.hero h1{font-size:clamp(32px,4.8vw,52px);line-height:1.08;letter-spacing:-.035em;margin:0 0 14px}
.hero p{color:var(--mut);font-size:18px;margin:0 0 24px}
.search{position:relative;max-width:640px}
.search input{width:100%;padding:14px 18px;font:inherit;border:1px solid var(--line);border-radius:14px;background:var(--card);color:var(--fg);box-shadow:0 8px 24px -12px rgba(11,27,51,.18)}
.search input:focus{outline:2px solid var(--acc);outline-offset:1px}
#results{position:absolute;inset-inline:0;top:100%;margin-top:6px;background:var(--card);border:1px solid var(--line);border-radius:14px;max-height:420px;overflow:auto;display:none;z-index:5;box-shadow:0 16px 40px -16px rgba(11,27,51,.3)}
#results a{display:block;padding:10px 14px;border-bottom:1px solid var(--line)}#results a small{color:var(--mut);display:block}
.stats{display:flex;gap:30px;margin:28px 0 8px;flex-wrap:wrap}.stats b{font-size:28px;display:block;letter-spacing:-.03em}.stats span{color:var(--mut);font-size:14px}
h2{font-size:22px;letter-spacing:-.02em;margin:46px 0 14px}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:12px}
.card{background:var(--card);border:1px solid var(--line);border-radius:16px;padding:16px 16px 14px;display:block;transition:border-color .15s,transform .15s,box-shadow .15s;position:relative;overflow:hidden}
.card::before{content:"";position:absolute;inset-block:0;inset-inline-start:0;width:4px;background:var(--acc);opacity:0;transition:opacity .15s}
.card:hover{border-color:var(--acc);color:inherit;transform:translateY(-2px);box-shadow:0 12px 28px -18px rgba(58,91,255,.55)}.card:hover::before{opacity:1}
.card h3{margin:0 0 4px;font-size:16px;word-break:break-word}.card p{margin:0;color:var(--mut);font-size:14px;display:-webkit-box;-webkit-line-clamp:3;-webkit-box-orient:vertical;overflow:hidden}
.meta{display:flex;gap:12px;flex-wrap:wrap;color:var(--mut);font-size:13px;margin-top:10px}
.tier{display:inline-block;font-weight:700;font-size:12px;border-radius:7px;padding:1px 8px;color:#fff;background:#64748b}
.tier.S{background:#ff6b4a}.tier.A{background:#3a5bff}.tier.B{background:#12b886}
.pill{display:inline-block;font-size:12px;border:1px solid var(--line);border-radius:99px;padding:1px 9px;color:var(--mut);background:var(--bg)}
.crumbs{color:var(--mut);font-size:14px;margin:26px 0 6px}
.page h1{font-size:clamp(26px,3.6vw,40px);letter-spacing:-.03em;margin:0 0 8px;word-break:break-word}
.lead{color:var(--mut);font-size:18px;margin:0 0 20px;max-width:800px}
.kv{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:10px;margin:20px 0}
.kv div{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:12px}.kv span{display:block;color:var(--mut);font-size:13px}.kv b{font-size:17px}
.prose{max-width:800px}.prose p{margin:0 0 14px}
.cmd{display:flex;gap:8px;align-items:stretch;margin:8px 0 14px;max-width:900px}
.cmd code{flex:1;background:var(--code);border:1px solid var(--line);border-radius:12px;padding:11px 13px;font:13.5px/1.5 "Geist Mono",ui-monospace,Menlo,monospace;overflow-x:auto;white-space:nowrap;direction:ltr;text-align:left}
.cmd button{border:0;background:var(--acc);color:#fff;border-radius:12px;padding:0 16px;cursor:pointer;font:inherit;font-size:14px;font-weight:500}
.btn{display:inline-block;background:var(--acc);color:#fff;border-radius:12px;padding:10px 18px;font-size:15px;font-weight:600}.btn:hover{color:#fff;opacity:.9}
pre.file{background:var(--code);border:1px solid var(--line);border-radius:14px;padding:16px;overflow:auto;max-height:640px;font:13px/1.55 "Geist Mono",ui-monospace,Menlo,monospace;white-space:pre-wrap;word-break:break-word;direction:ltr;text-align:left}
table.list{width:100%;border-collapse:collapse;font-size:15px}table.list td,table.list th{padding:11px 8px;border-bottom:1px solid var(--line);text-align:start;vertical-align:top}
table.list tr:hover td{background:var(--card)}
table.list th{color:var(--mut);font-weight:500;font-size:13px}table.list td small{color:var(--mut);display:block}
.filter{padding:10px 14px;border:1px solid var(--line);border-radius:12px;background:var(--card);color:var(--fg);font:inherit;width:100%;max-width:420px;margin:0 0 14px}
.tabs{display:flex;gap:8px;flex-wrap:wrap;margin:6px 0 18px}.tabs a{border:1px solid var(--line);border-radius:99px;padding:5px 14px;font-size:14px;background:var(--card)}.tabs a.on{background:var(--acc);border-color:var(--acc);color:#fff}.tabs span{padding:5px 2px;color:var(--mut)}
.ad{margin:26px 0;min-height:0}
footer{border-top:1px solid var(--line);margin-top:70px;padding:28px 0 40px;color:var(--mut);font-size:14px}
footer .wrap{display:flex;gap:18px;flex-wrap:wrap}
.card .new{position:absolute;top:10px;inset-inline-end:10px;background:var(--acc2);color:#fff;font-size:11px;font-weight:700;border-radius:6px;padding:1px 7px}
.up{color:#12b886;font-weight:600}
/* centered layout */
.hero{margin:0 auto;text-align:center}.hero .search{margin:0 auto}.stats{justify-content:center}
h2{text-align:center}.page h1,.lead,.crumbs{text-align:center;margin-inline:auto}
.page>p,.page>div.meta{text-align:center;justify-content:center}.meta{justify-content:center}
.card{text-align:center}.card::before{inset-inline-start:0;inset-inline-end:0;inset-block:auto 0;width:auto;height:3px}
.kv{text-align:center}.prose{margin-inline:auto;text-align:center}.tabs{justify-content:center}
.filter{display:block;margin:0 auto 14px}.cmd{margin-inline:auto}footer .wrap{justify-content:center}
.page>h2+p{text-align:center}
@media(max-width:720px){nav.main{display:none}.hero{padding-top:30px}}
"""

JS = r"""
(function(){var d=document.documentElement,k='os-theme';
document.getElementById('tg').onclick=function(){var t=d.dataset.theme==='dark'?'light':'dark';d.dataset.theme=t;localStorage.setItem(k,t)};
document.getElementById('lg').onchange=function(){localStorage.setItem('os-lang',this.value);location.href=this.selectedOptions[0].dataset.href};
document.querySelectorAll('.cmd button').forEach(function(b){b.onclick=function(){navigator.clipboard.writeText(b.previousElementSibling.textContent);var o=b.textContent;b.textContent='✓';setTimeout(function(){b.textContent=o},1200)}});
var q=document.getElementById('q'),box=document.getElementById('results'),idx=null,P=d.dataset.pre||'';
if(q){q.addEventListener('input',function(){var v=q.value.trim().toLowerCase();if(!v){box.style.display='none';return}
 var go=function(){var out=[];for(var i=0;i<idx.length&&out.length<30;i++){var it=idx[i];if((it.t+' '+it.d).toLowerCase().indexOf(v)>-1)out.push(it)}
 box.innerHTML=out.map(function(it){return '<a href="'+P+it.u+'"><b>'+esc(it.t)+'</b> <span class="pill">'+it.k+'</span><small>'+esc(it.d.slice(0,120))+'</small></a>'}).join('')||'<a>—</a>';box.style.display='block'};
 if(idx)go();else fetch('/search-index.json').then(function(r){return r.json()}).then(function(j){idx=j;go()})});
 document.addEventListener('click',function(ev){if(!box.contains(ev.target)&&ev.target!==q)box.style.display='none'})}
var f=document.getElementById('flt');if(f)f.addEventListener('input',function(){var v=f.value.toLowerCase();document.querySelectorAll('[data-s]').forEach(function(r){r.style.display=r.dataset.s.indexOf(v)>-1?'':'none'})});
document.querySelectorAll('pre[data-src]').forEach(function(p){fetch(p.dataset.src).then(function(r){return r.text()}).then(function(x){p.textContent=x})});
function esc(s){return String(s).replace(/[&<>"]/g,function(c){return{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]})}
})();
"""

HEAD_JS = "<script>(function(){var t=localStorage.getItem('os-theme')||(matchMedia('(prefers-color-scheme: dark)').matches?'dark':'light');document.documentElement.dataset.theme=t})()</script>"

def layout(lang, path, title, desc, body, alt_paths=None, jsonld=None):
    t = T[lang]
    alt_paths = alt_paths if alt_paths is not None else {l: path for l in LANGS}
    hreflang = "".join(f'<link rel="alternate" hreflang="{l}" href="{BASE}{url(l, alt_paths[l])}">' for l in LANGS if l in alt_paths)
    hreflang += f'<link rel="alternate" hreflang="x-default" href="{BASE}{alt_paths.get("en", path)}">'
    opts = "".join(f'<option value="{l}" data-href="{url(l, alt_paths.get(l, "/"))}"{" selected" if l == lang else ""}>{LANG_NAMES[l]}</option>' for l in LANGS)
    nav = (f'<a href="{url(lang, "/trending/")}">🔥 {t["trending"]}</a><a href="{url(lang, "/")}">{t["repos"]}</a><a href="{url(lang, "/skills/")}">{t["skills"]}</a>'
           f'<a href="{url(lang, "/agents/")}">{t["agents"]}</a><a href="{url(lang, "/commands/")}">{t["commands"]}</a>'
           f'<a href="{url(lang, "/about/")}">{t["about"]}</a>')
    ads = f'<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client={CFG["adsense_client"]}" crossorigin="anonymous"></script>' if CFG.get("adsense_client") else ""
    ld = f'<script type="application/ld+json">{json.dumps(jsonld, ensure_ascii=False)}</script>' if jsonld else ""
    return f"""<!doctype html><html lang="{lang}" dir="{'rtl' if lang in RTL else 'ltr'}" data-pre="{BP}{pre(lang)}"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>{e(title)}</title><meta name="description" content="{e(desc[:300])}">
<link rel="canonical" href="{BASE}{url(lang, path)}">{hreflang}
<meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc[:300])}"><meta property="og:type" content="website"><meta property="og:url" content="{BASE}{url(lang, path)}">
<link rel="icon" href="/assets/favicon.svg"><link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Geist:wght@400;500;600;700&family=Geist+Mono:wght@400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/site.css">{HEAD_JS}{ads}{ld}</head><body><div class="bg"></div>
<div class="wrap"><header class="top"><a class="logo" href="{url(lang, '/')}"><i><b></b><b></b><b></b><b></b></i>{NAME}</a><nav class="main">{nav}</nav><span class="sp"></span>
<div class="ctl"><select id="lg" aria-label="Language">{opts}</select><button class="tg" id="tg" aria-label="{t['theme']}">◐</button></div></header>
<main>{body}</main></div>
<footer><div class="wrap"><span>© {TODAY.year} {NAME}</span><a href="{url(lang, '/about/')}">{t['about']}</a><a href="{url(lang, '/privacy/')}">{t['privacy']}</a>
<a href="{url(lang, '/terms/')}">{t['terms']}</a><a href="https://github.com/{GH}">{t['open_source']}</a><a href="/llms.txt">llms.txt</a><a href="/api/v1/repos.json">API</a></div></footer>
<script src="/assets/site.js" defer></script></body></html>"""

def write(path, content):
    full = os.path.join(OUT, path.lstrip("/"))
    if full.endswith("/"): full += "index.html"
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f: f.write(fix(content) if full.endswith(".html") else content)

def cmd(text, t): return f'<div class="cmd"><code>{e(text)}</code><button type="button">Copy</button></div>'

def repo_path(r): return f'/r/{r["repo"].lower()}/'
def comp_path(c): return f'/{c["id"]}/'

def repo_card(lang, r):
    t = T[lang]
    return (f'<a class="card" href="{url(lang, repo_path(r))}"><h3>{e(r["repo"])}</h3><p>{e(r["desc"] or "")}</p>'
            f'<div class="meta"><span class="tier {r["tier"]}">{r["tier"]}</span><span>{r["rank"] if str(r["rank"]).startswith("T") else "#" + str(r["rank"])}</span><span>★ {fmt(r["stars"])}</span><span>{e(r["lang"] or "")}</span></div></a>')

def comp_card(lang, c):
    return (f'<a class="card" href="{url(lang, comp_path(c))}"><h3>{e(c["name"])}</h3><p>{e(c["description"] or "")}</p>'
            f'<div class="meta"><span class="pill">{c["kind"]}</span><span>{e(c["repo"])}</span></div></a>')

def trend_card(lang, r):
    t = T[lang]
    badge = f'<span class="new">{t["new_badge"]}</span>' if _SHOW_NEW and r.get("first_seen") == TREND.get("generatedAt") else ""
    g = f'<span class="up">{t["gained"].format(n=fmt(r["gained_24h"]))}</span>' if r.get("gained_24h") else ""
    return (f'<a class="card" href="{url(lang, repo_path(r))}">{badge}<h3>{e(r["repo"])}</h3><p>{e(r["desc"] or "")}</p>'
            f'<div class="meta"><span class="tier {r["tier"]}">{r["tier"]}</span><span>★ {fmt(r["stars"])}</span><span>{fmt(r["spd"])} {t["stars_day"]}</span>{g}</div></a>')

def build_trending(lang):
    t = T[lang]
    cards = "".join(trend_card(lang, r) for r in trending)
    body = f"""<div class="page"><div class="crumbs"><a href="{url(lang, '/')}">{t['home']}</a></div><h1>🔥 {t['trending']}</h1>
<p class="lead">{e(t['trending_sub'])}</p><p class="meta">{t['updated_on']}: {TREND.get('generatedAt', '')} · {len(trending)} {t['repos']}</p>
<div class="grid">{cards}</div></div>"""
    write(url(lang, "/trending/"), layout(lang, "/trending/", f"{t['trending']} — {NAME}", t["trending_sub"], body))

def ago(lang, days):
    return T[lang]["today"] if not days else T[lang]["days_ago"].format(n=days)

# ---------- pages ----------
def build_home(lang):
    t = T[lang]
    ks = {k: sum(1 for c in comps if c["kind"] == k) for k in KIND_DIR}
    cats = "".join(f'<a class="card" href="{url(lang, "/c/" + CAT_SLUG[c] + "/")}"><h3>{e(CATS[c][lang])}</h3><div class="meta"><span>{cats_count[c]} {t["projects"]}</span></div></a>' for c in CAT_ORDER)
    top = "".join(repo_card(lang, r) for r in repos[:24])
    skills = [c for c in comps if c["kind"] == "skill"][:12]
    body = f"""<section class="hero"><h1>{e(t['tagline'])}</h1><p>{e(t['hero_sub'])}</p>
<div class="search"><input id="q" type="search" placeholder="{e(t['search'])}" autocomplete="off"><div id="results"></div></div>
<div class="stats"><div><b>{len(repos):,}</b><span>{t['repos']}</span></div><div><b>{ks['skill']:,}</b><span>{t['skills']}</span></div>
<div><b>{ks['agent']:,}</b><span>{t['agents']}</span></div><div><b>{ks['command']:,}</b><span>{t['commands']}</span></div></div></section>
{f'<h2>🔥 {t["trending"]}</h2><p class="lead">{e(t["trending_sub"])}</p><div class="grid">{"".join(trend_card(lang, r) for r in trending[:12])}</div><p style="text-align:center"><a class="btn" href="{url(lang, "/trending/")}">{t["see_trending"]} →</a></p>' if trending else ''}
<h2>{t['categories']}</h2><div class="grid">{cats}</div>
<div class="ad" data-slot="home-1"></div>
<h2>{t['top']}</h2><div class="grid">{top}</div>
{f'<h2>{t["skills"]}</h2><div class="grid">{"".join(comp_card(lang, c) for c in skills)}</div><p><a class="btn" href="{url(lang, "/skills/")}">{t["browse_all"]} →</a></p>' if skills else ''}"""
    ld = {"@context": "https://schema.org", "@type": "WebSite", "name": NAME, "url": BASE + url(lang, "/"),
          "potentialAction": {"@type": "SearchAction", "target": BASE + "/?q={q}", "query-input": "required name=q"}}
    write(url(lang, "/"), layout(lang, "/", f"{NAME} — {t['tagline']}", t["hero_sub"], body, jsonld=ld))

def build_cat(lang, cat):
    t = T[lang]; rs = [r for r in repos if r["category"] == cat]
    rows = "".join(f'<tr data-s="{e((r["repo"] + " " + (r["desc"] or "")).lower())}"><td>#{r["rank"]}</td><td><a href="{url(lang, repo_path(r))}"><b>{e(r["repo"])}</b></a><small>{e(r["desc"] or "")}</small></td>'
                   f'<td><span class="tier {r["tier"]}">{r["tier"]}</span> {r["score"]}</td><td>★ {fmt(r["stars"])}</td><td>{e(r["lang"] or "")}</td></tr>' for r in rs)
    body = f"""<div class="page"><div class="crumbs"><a href="{url(lang, '/')}">{t['home']}</a> / {t['categories']}</div>
<h1>{e(CATS[cat][lang])}</h1><p class="lead">{len(rs)} {t['projects']}</p><input class="filter" id="flt" placeholder="{e(t['filter'])}">
<table class="list"><tr><th>{t['rank']}</th><th>{t['repos']}</th><th>{t['score']}</th><th>{t['stars']}</th><th>{t['lang']}</th></tr>{rows}</table></div>"""
    p = f"/c/{CAT_SLUG[cat]}/"
    write(url(lang, p), layout(lang, p, f"{CATS[cat][lang]} — {t['all_in']} {NAME}", f"{t['all_in']} {CATS[cat][lang]}: " + ", ".join(r["repo"] for r in rs[:12]), body))

def build_repo(lang, r):
    t = T[lang]
    reasons = ", ".join(t["reasons"].get(x.strip(), x.strip()) for x in (r["why"] or "").split(",") if x.strip())
    s1 = t["summary"].format(name=r["repo"], a_type=t["types"].get(r["type"], r["type"]), lang=r["lang"] or "—", created=r["created"],
                             stars=f'{r["stars"]:,}', forks=f'{r["forks"]:,}', spy=f'{int(r["spy"] or 0):,}', upd=ago(lang, r["days"]),
                             lic=r["license"] or "—", lic_note=t[lic_kind(r["license"])])
    s2 = t["summary2"].format(score=r["score"], tier=r["tier"], reasons=reasons)
    rel = [x for x in repos if x["category"] == r["category"] and x["repo"] != r["repo"]][:6]
    rank_txt = r["rank"] if str(r["rank"]).startswith("T") else f'#{r["rank"]}' 
    mine = comps_by_repo.get(r["repo"].lower(), [])
    kv = "".join(f'<div><span>{k}</span><b>{v}</b></div>' for k, v in [
        (t["rank"], rank_txt), (t["score"], f'{r["score"]}/100'), (t["stars"], fmt(r["stars"])), (t["forks"], fmt(r["forks"])),
        (t["star_year"], fmt(r["spy"])), (t["lang"], e(r["lang"] or "—")), (t["license"], e(r["license"] or "—")), (t["size"], f'{r["size_mb"]} MB'),
        (t["created"], r["created"]), (t["updated"], r["updated"])])
    body = f"""<div class="page"><div class="crumbs"><a href="{url(lang, '/')}">{t['home']}</a> / <a href="{url(lang, '/c/' + CAT_SLUG[r['category']] + '/')}">{e(CATS[r['category']][lang])}</a></div>
<h1>{e(r['repo'])} <span class="tier {r['tier']}">{r['tier']}</span></h1><p class="lead" dir="auto">{e(r['desc'] or '')}</p>
<p><a class="btn" href="{e(r['link'])}" rel="noopener">{t['view_github']} ↗</a></p>
<div class="kv">{kv}</div>
<div class="prose"><p>{e(s1)}</p><p>{e(s2)}</p></div>
<div class="ad" data-slot="repo-1"></div>
<h2>{t['get']}</h2><p>{t['clone_hint']}</p>{cmd('git clone --depth 1 ' + r['link'] + '.git', t)}
{f'<h2>{t["from_repo"]}</h2><div class="grid">{"".join(comp_card(lang, c) for c in mine[:30])}</div>' if mine else ''}
<h2>{t['related']}</h2><div class="grid">{''.join(repo_card(lang, x) for x in rel)}</div></div>"""
    ld = {"@context": "https://schema.org", "@type": "SoftwareSourceCode", "name": r["repo"], "description": r["desc"], "codeRepository": r["link"],
          "programmingLanguage": r["lang"], "license": r["license"], "dateCreated": r["created"], "dateModified": r["updated"]}
    write(url(lang, repo_path(r)), layout(lang, repo_path(r), f"{r['repo']} — {t['score']} {r['score']}/100 | {NAME}", (r["desc"] or "") + " " + s1, body, jsonld=ld))

PER = 100
def build_kind_index(lang, kind):
    t = T[lang]; d = KIND_DIR[kind]; items = [c for c in comps if c["kind"] == kind]
    pages = max(1, -(-len(items) // PER))
    tabs = "".join(f'<a class="{"on" if k == kind else ""}" href="{url(lang, "/" + KIND_DIR[k] + "/")}">{t[KIND_DIR[k]]}</a>' for k in KIND_DIR)
    for n in range(1, pages + 1):
        chunk = items[(n - 1) * PER:n * PER]
        p = f"/{d}/" if n == 1 else f"/{d}/page/{n}/"
        rows = "".join(f'<tr data-s="{e((c["name"] + " " + c["description"] + " " + c["repo"]).lower())}"><td><a href="{url(lang, comp_path(c))}"><b>{e(c["name"])}</b></a><small>{e(c["description"][:200])}</small></td><td><small>{e(c["repo"])}</small></td></tr>' for c in chunk)
        pg = lambda k: f"/{d}/" if k == 1 else f"/{d}/page/{k}/"
        nums = [k for k in range(1, pages + 1) if k <= 2 or k > pages - 2 or abs(k - n) <= 2]
        pager, last = [], 0
        for k in nums:
            if k - last > 1: pager.append("<span>…</span>")
            pager.append(f'<a class="{"on" if k == n else ""}" href="{url(lang, pg(k))}">{k}</a>'); last = k
        body = f"""<div class="page"><div class="crumbs"><a href="{url(lang, '/')}">{t['home']}</a></div><h1>{t[d]}</h1><p class="lead">{len(items):,} {t['items']}</p>
<div class="tabs">{tabs}</div><p><small>{t['search']} ↑ <a href="{url(lang, '/')}">{t['home']}</a></small></p><input class="filter" id="flt" placeholder="{e(t['filter'])}"><table class="list">{rows}</table>
<div class="tabs" style="margin-top:20px">{''.join(pager)}</div></div>"""
        title = f"{t[d]} — {NAME}" + (f" ({n}/{pages})" if n > 1 else "")
        write(url(lang, p), layout(lang, p, title, f"{len(items)} Claude Code {d}: " + ", ".join(c["name"] for c in chunk[:15]), body))
    KIND_PAGES[d] = pages

KIND_PAGES = {}
def build_comp(lang, c):
    t = T[lang]; d = KIND_DIR[c["kind"]]
    r = by_name.get(c["repo"].lower())
    body = f"""<div class="page"><div class="crumbs"><a href="{url(lang, '/')}">{t['home']}</a> / <a href="{url(lang, '/' + d + '/')}">{t[d]}</a> / {e(c['repo'])}</div>
<h1>{e(c['name'])}</h1><p class="lead" dir="auto">{e(c['description'])}</p>
<div class="meta"><span class="pill">{c['kind']}</span><span>{t['license']}: {e(c['license'])}</span>
<span>{t['source']}: {f'<a href="{url(lang, repo_path(r))}">{e(c["repo"])}</a>' if r else e(c['repo'])}</span></div>
<h2>{t['install']}</h2><p>{t['install_hint']}</p>{cmd(c['install'], t)}<p>{t['install_user']}</p>{cmd(c['install_user'], t)}
<div class="ad" data-slot="comp-1"></div>
<h2>{t['content']}</h2><p><small>{t['attribution']} {e(c['license'])}. {t['attribution2']} <a href="{e(c['src_url'])}" rel="noopener">{t['source']} ↗</a></small></p>
{f'<pre class="file">{e(c["content"])}</pre>' if lang == "en" else f'<pre class="file" data-src="/content/{c["id"]}.txt">…</pre><noscript><a href="/content/{c["id"]}.txt">{t["content"]}</a></noscript>'}</div>"""
    write(url(lang, comp_path(c)), layout(lang, comp_path(c), f"{c['name']} — Claude Code {c['kind']} from {c['repo']} | {NAME}",
                                          c["description"] or f"{c['name']} {c['kind']} for Claude Code", body))

def build_static(lang, key, title_key):
    t = T[lang]; p = f"/{key}/"
    write(url(lang, p), layout(lang, p, f"{t[title_key]} — {NAME}", re.sub("<[^>]+>", "", t[key + "_body"])[:200],
                               f'<div class="page prose"><div class="crumbs"><a href="{url(lang, "/")}">{t["home"]}</a></div><h1>{t[title_key]}</h1>{t[key + "_body"]}</div>'))

def build_extras():
    # search index (shared by all languages; links are prefixed client-side)
    idx = [{"t": r["repo"], "d": r["desc"] or "", "u": repo_path(r), "k": "repo"} for r in repos + extra_repos]
    idx += [{"t": c["name"], "d": c["description"] + " — " + c["repo"], "u": comp_path(c), "k": c["kind"]} for c in comps]
    json.dump(idx, open(os.path.join(OUT, "search-index.json"), "w"), ensure_ascii=False, separators=(",", ":"))
    os.makedirs(os.path.join(OUT, "api/v1"), exist_ok=True)
    json.dump({"generatedAt": TODAY.isoformat(), "count": len(repos), "repos": [{k: r[k] for k in ("rank", "repo", "link", "category", "type", "desc", "stars", "forks", "lang", "license", "score", "tier")} | {"page": BASE + repo_path(r)} for r in repos]},
              open(os.path.join(OUT, "api/v1/repos.json"), "w"), ensure_ascii=False)
    json.dump(TREND, open(os.path.join(OUT, "api/v1/trending.json"), "w"), ensure_ascii=False)
    json.dump({"generatedAt": TODAY.isoformat(), "count": len(comps), "components": [{k: c[k] for k in ("id", "kind", "name", "description", "repo", "license", "path", "install")} | {"page": BASE + comp_path(c), "source": c["src_url"]} for c in comps]},
              open(os.path.join(OUT, "api/v1/components.json"), "w"), ensure_ascii=False)
    # sitemap with hreflang
    paths = [f"/{d}/page/{n}/" for d, m in KIND_PAGES.items() for n in range(2, m + 1)] + ["/", "/skills/", "/agents/", "/commands/", "/about/", "/privacy/", "/terms/"] + [f"/c/{CAT_SLUG[c]}/" for c in CAT_ORDER] + [repo_path(r) for r in repos + extra_repos] + ["/trending/"] + [comp_path(c) for c in comps]
    chunks = [paths[i:i + 9000] for i in range(0, len(paths), 9000)]
    for n, ch in enumerate(chunks):
        xs = ['<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">']
        for p in ch:
            alts = "".join(f'<xhtml:link rel="alternate" hreflang="{l}" href="{BASE}{url(l, p)}"/>' for l in LANGS)
            for l in LANGS: xs.append(f"<url><loc>{BASE}{url(l, p)}</loc>{alts}</url>")
        xs.append("</urlset>")
        open(os.path.join(OUT, f"sitemap-{n+1}.xml"), "w").write("".join(xs))
    open(os.path.join(OUT, "sitemap.xml"), "w").write('<?xml version="1.0" encoding="UTF-8"?><sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' +
        "".join(f"<sitemap><loc>{BASE}/sitemap-{n+1}.xml</loc></sitemap>" for n in range(len(chunks))) + "</sitemapindex>")
    open(os.path.join(OUT, "robots.txt"), "w").write(f"User-agent: *\nAllow: /\nSitemap: {BASE}/sitemap.xml\n")
    if CFG.get("adsense_client"):
        open(os.path.join(OUT, "ads.txt"), "w").write(f"google.com, {CFG['adsense_client'].replace('ca-', '')}, DIRECT, f08c47fec0942fa0\n")
    ks = {k: sum(1 for c in comps if c["kind"] == k) for k in KIND_DIR}
    open(os.path.join(OUT, "llms.txt"), "w").write(f"""# {NAME}

> Directory of the top {len(repos)} open-source repositories ranked by growth and future potential, plus {ks['skill']} Claude Code skills, {ks['agent']} agents and {ks['command']} slash commands extracted from permissively licensed repos. Every component links to its original source.

## Data (JSON, no auth)
- [All repos]({BASE}/api/v1/repos.json): rank, category, stars, license, future score, tier, page URL
- [All components]({BASE}/api/v1/components.json): skills, agents, commands with install command and source URL

## Install a component
- Skill: `npx degit <owner>/<repo>/<path> .claude/skills/<name>`
- Agent / command: `curl -fsSL --create-dirs -o .claude/agents/<name>.md https://raw.githubusercontent.com/<owner>/<repo>/HEAD/<path>`
- Read a component's content before installing it: hooks, skills and agents can run code locally.

## Pages
- [Skills]({BASE}/skills/) · [Agents]({BASE}/agents/) · [Commands]({BASE}/commands/) · [About]({BASE}/about/)
- Languages: English (/), Arabic (/ar/), French (/fr/), Spanish (/es/), German (/de/)
- [Source code](https://github.com/{GH})
""")
    for lang in LANGS:
        t = T[lang]
        write(url(lang, "/404.html") if lang != "en" else "/404.html", layout(lang, "/", f"{t['not_found']} — {NAME}", t["not_found"],
              f'<div class="page"><h1 style="margin-top:60px">{t["not_found"]}</h1><p><a class="btn" href="{url(lang, "/")}">{t["back_home"]}</a></p></div>'))

def main():
    if os.path.exists(OUT): shutil.rmtree(OUT)
    os.makedirs(os.path.join(OUT, "assets"))
    open(os.path.join(OUT, "assets/bg.svg"), "w").write(make_bg())
    open(os.path.join(OUT, "assets/site.css"), "w").write(fix(CSS))
    open(os.path.join(OUT, "assets/site.js"), "w").write(fix(JS))
    open(os.path.join(OUT, "assets/favicon.svg"), "w").write('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32"><rect width="32" height="32" rx="8" fill="#0b1b33"/><rect x="7" y="8" width="4" height="16" rx="1.5" fill="#3a5bff"/><rect x="12.5" y="11" width="4" height="13" rx="1.5" fill="#ff6b4a"/><rect x="18" y="9" width="4" height="15" rx="1.5" fill="#12b886"/><rect x="22" y="12" width="4" height="12" rx="1.5" fill="#f7b32b" transform="rotate(-14 26 24)"/></svg>')
    if CFG.get("cname"): open(os.path.join(OUT, "CNAME"), "w").write(CFG["cname"] + "\n")
    open(os.path.join(OUT, ".nojekyll"), "w").write("")
    for lang in LANGS:
        build_home(lang)
        for c in CAT_ORDER: build_cat(lang, c)
        for r in repos + extra_repos: build_repo(lang, r)
        build_trending(lang)
        for k in KIND_DIR: build_kind_index(lang, k)
        for c in comps: build_comp(lang, c)
        build_static(lang, "about", "about"); build_static(lang, "privacy", "privacy"); build_static(lang, "terms", "terms")
    for c in comps:
        fp = os.path.join(OUT, "content", c["id"] + ".txt"); os.makedirs(os.path.dirname(fp), exist_ok=True)
        open(fp, "w", encoding="utf-8").write(c["content"])
    build_extras()
    n = sum(len(f) for _, _, f in os.walk(OUT))
    print(f"built {n} files: {len(repos)} repos, {len(comps)} components x {len(LANGS)} languages -> {OUT}")

if __name__ == "__main__":
    main()
