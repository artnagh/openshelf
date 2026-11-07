#!/usr/bin/env bash
# Keep a zip copy of every permissively licensed trending repo in Cloudflare R2.
# Zips come from GitHub's own codeload service (source snapshot of the default branch); nothing is executed.
set -euo pipefail
mkdir -p /tmp/arch
python3 - <<'PY' > /tmp/arch/list.txt
import json
ok = ("MIT", "Apache", "BSD", "ISC", "CC0", "Unlicense", "0BSD", "MPL", "Zlib")
for r in json.load(open("data/trending.json"))["repos"]:
    if r["license"].startswith(ok) and r["size_mb"] < 500: print(r["repo"])
PY
while read -r repo; do
  key="repos/${repo//\//__}/$(date -u +%F).zip"
  if aws s3 ls "s3://$R2_BUCKET/repos/${repo//\//__}/" --endpoint-url "$R2_ENDPOINT" >/dev/null 2>&1; then continue; fi  # already archived
  curl -fsSL "https://codeload.github.com/$repo/zip/HEAD" -o /tmp/arch/r.zip || continue
  aws s3 cp /tmp/arch/r.zip "s3://$R2_BUCKET/$key" --endpoint-url "$R2_ENDPOINT" --only-show-errors && echo "archived $repo"
done < /tmp/arch/list.txt
