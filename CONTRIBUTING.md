# Contributing to OpenShelf

## Suggest a repo
Open an issue titled `Add: owner/repo` with one line on why it will matter by 2030.
We only list open-source repos that are public on GitHub and still updated.

## Suggest a skill, agent or command
It must live in a public repo with a permissive license (MIT, Apache-2.0, BSD, ISC, MPL-2.0, CC0, Unlicense).
Open an issue with the link to the folder (skill) or `.md` file (agent / command).

## Authors: remove or fix your file
Open an issue titled `Remove: owner/repo/path` (or `Fix:`). We act on these first.

## Build locally
```bash
python3 scripts/build.py
python3 -m http.server 8932 -d site
```
