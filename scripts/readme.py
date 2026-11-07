"""Generate README.md (GitHub front page) from data/. Run after build.py data is ready."""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(__file__))
from i18n import CATS
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
cfg = json.load(open(os.path.join(ROOT, "config.json")))
repos = json.load(open(os.path.join(ROOT, "data/repos.json")))
sys.argv = [sys.argv[0]]
import build
comps = build.comps
B, N = cfg["base_url"].rstrip("/"), cfg["site_name"]
k = {x: sum(1 for c in comps if c["kind"] == x) for x in ("skill", "agent", "command")}
def fmt(n): return f"{n/1000:.1f}k" if n >= 1000 else str(n)
def anchor(s): return "".join(ch for ch in s.lower().replace(" ", "-") if ch.isalnum() or ch == "-")
cats = {}
for r in repos: cats.setdefault(r["category"], []).append(r)
order = sorted(cats, key=lambda c: -len(cats[c]))
L = [f"# {N}", "",
     f"**The {len(repos):,} open-source projects that matter by 2030, plus {k['skill']:,} Claude Code skills, {k['agent']:,} agents and {k['command']:,} commands found inside them.**", "",
     f"🌐 **Website:** {B} · English · العربية · Français · Español · Deutsch", "",
     "Repos are ranked by stars gained per year, community size, update activity and trend momentum, giving each a **future score (0–100)** and a tier (S/A/B/C). "
     "Skills, agents and commands are copied unchanged from permissively licensed repos, with credit and a link to the source.", "",
     "⭐ Star this repo to follow the list. It is rebuilt every day.", "",
     "## Contents", ""]
L += [f"- [{CATS[c]['en']}](#{anchor(CATS[c]['en'])}) ({len(cats[c])})" for c in order]
L += ["- [Install a skill](#install-a-skill)", "- [API](#api)", "- [Contributing](#contributing)", ""]
for c in order:
    L += [f"## {CATS[c]['en']}", "", "| # | Repo | What it does | ★ | Score |", "|---|---|---|---|---|"]
    for r in cats[c][:25]:
        d = (r["desc"] or "").replace("|", "/").replace("\n", " ")[:110]
        L.append(f"| {r['rank']} | [{r['repo']}]({B}/r/{r['repo'].lower()}/) | {d} | {fmt(r['stars'])} | {r['tier']} · {r['score']} |")
    if len(cats[c]) > 25: L.append(f"\n[See all {len(cats[c])} →]({B}/c/{re.sub(r'[^a-z0-9]+','-',CATS[c]['en'].lower()).strip('-')}/)")
    L.append("")
L += ["## Install a skill", "", "```bash", "# into this project", "npx degit <owner>/<repo>/<path-to-skill> .claude/skills/<name>",
      "# for every project", "npx degit <owner>/<repo>/<path-to-skill> ~/.claude/skills/<name>", "```",
      "Every component page on the site gives you the exact command. **Read a skill before you install it.**", "",
      "## API", "", f"- `{B}/api/v1/repos.json`: all repos", f"- `{B}/api/v1/components.json`: all skills, agents and commands", f"- `{B}/llms.txt`: guide for AI agents", "",
      "## Contributing", "", "See [CONTRIBUTING.md](CONTRIBUTING.md). Authors can ask for any file to be removed or fixed.", "",
      "## License", "", "Site code and ranking data: MIT. Each listed component keeps its original license (shown on its page).", "",
      "_Not affiliated with GitHub or Anthropic._", ""]
open(os.path.join(ROOT, "README.md"), "w").write("\n".join(L))
print("README.md", len(L), "lines")
