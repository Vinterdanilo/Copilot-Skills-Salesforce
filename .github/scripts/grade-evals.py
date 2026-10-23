#!/usr/bin/env python3
"""
grade-evals.py — grades saved model answers against machine-checkable assertions.

  python .github/scripts/grade-evals.py <evals.json> <output-dir>

<output-dir> contains one file per case named <case id>.md (the full answer, code included).
Assertion types: contains, not_contains, regex, not_regex (optional "flags": "i").
Qualitative "expected_behavior" items still need human review.
"""
import json, pathlib, re, sys

if len(sys.argv) != 3:
    sys.exit(__doc__)
spec = json.loads(pathlib.Path(sys.argv[1]).read_text(encoding="utf-8"))
out = pathlib.Path(sys.argv[2])
total = passed = 0
for case in spec["cases"]:
    f = out / f"{case['id']}.md"
    if not f.is_file():
        print(f"- {case['id']}: SKIPPED (no output file)")
        continue
    text = f.read_text(encoding="utf-8")
    fails = []
    for a in case.get("assertions", []):
        flags = re.I if "i" in a.get("flags", "") else 0
        t, v = a["type"], a["value"]
        ok = {"contains": lambda: v in text, "not_contains": lambda: v not in text,
              "regex": lambda: re.search(v, text, flags) is not None,
              "not_regex": lambda: re.search(v, text, flags) is None}[t]()
        total += 1; passed += ok
        if not ok:
            fails.append(f"{t}: {v}")
    print(f"{'✓' if not fails else '✗'} {case['id']}" + ("".join(f"\n    ✗ {x}" for x in fails)))
print(f"\n{passed}/{total} assertions passed")
sys.exit(0 if passed == total else 1)
