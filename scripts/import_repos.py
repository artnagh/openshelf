"""Turn the Top-1000 Excel sheet into data/repos.json.
Usage: python3 scripts/import_repos.py <Top-1000-Open-Source-Repos.xlsx>"""
import sys, os, json, openpyxl
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ws = openpyxl.load_workbook(sys.argv[1], read_only=True)["Top 1000"]
out = []
for r in list(ws.iter_rows(values_only=True))[1:]:
    if not r[1]: continue
    out.append(dict(rank=r[0], repo=r[1], link=r[2], category=r[3], type=r[4], desc=r[5] or "", stars=r[6] or 0, forks=r[7] or 0,
                    spy=r[8] or 0, lang=r[9] or "", license=r[10] or "", created=str(r[11])[:10], updated=str(r[12])[:10],
                    days=r[13] or 0, size_mb=r[14] or 0, score=r[15], tier=r[16], why=(r[17] or "").replace("your pick", "").strip(", ")))
out.sort(key=lambda x: x["rank"])
json.dump(out, open(os.path.join(ROOT, "data", "repos.json"), "w"), ensure_ascii=False, indent=0)
print(len(out), "repos")
