#!/usr/bin/env python3
"""
bump-api-version.py — moves the whole instruction set to a new API version in one PR.

  python .github/scripts/bump-api-version.py 68.0 "Winter '27" [--project]

Updates salesforce-platform.json (apiVersion, apiRelease, validatedOn) and rewrites
<apiVersion>, /vNN.0/ and sourceApiVersion occurrences in .github docs. With --project it
also rewrites sfdx-project.json and force-app/**/*-meta.xml. Review platform-release-delta.md
manually afterwards: breaking changes are never automated.
"""
import datetime, json, pathlib, re, sys

if len(sys.argv) < 3 or not re.fullmatch(r"\d{2}\.0", sys.argv[1]):
    sys.exit(__doc__)
new, release = sys.argv[1], sys.argv[2]
root = pathlib.Path(".")
cfg_p = root / ".github" / "salesforce-platform.json"
cfg = json.loads(cfg_p.read_text(encoding="utf-8"))
old = cfg["apiVersion"]
cfg.update(apiVersion=new, apiRelease=release, validatedOn=str(datetime.date.today()))
cfg_p.write_text(json.dumps(cfg, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

pats = [(rf"<apiVersion>{re.escape(old)}</apiVersion>", f"<apiVersion>{new}</apiVersion>"),
        (rf"/v{re.escape(old)}/", f"/v{new}/"),
        (rf'"sourceApiVersion":\s*"{re.escape(old)}"', f'"sourceApiVersion": "{new}"')]
targets = list((root / ".github").rglob("*.md"))
if "--project" in sys.argv:
    targets += list(root.glob("force-app/**/*-meta.xml")) + [root / "sfdx-project.json"]
changed = 0
for p in targets:
    if not p.is_file():
        continue
    t = p.read_text(encoding="utf-8")
    n = t
    for a, b in pats:
        n = re.sub(a, b, n)
    if n != t:
        p.write_text(n, encoding="utf-8"); changed += 1
print(f"{old} → {new}: {changed} file(s) updated. Now update platform-release-delta.md and run check-consistency.py.")
