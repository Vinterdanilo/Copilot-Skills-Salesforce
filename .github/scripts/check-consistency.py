#!/usr/bin/env python3
"""
check-consistency.py — keeps the AI instructions and the Salesforce code honest.

Checks (exit 1 on any error):
  1. Version drift: every API version written in .github docs/instructions equals
     salesforce-platform.json apiVersion (allow-listed files may cite other versions).
  2. Forbidden patterns (from salesforce-platform.json) inside code blocks of the docs
     and inside project source (force-app/**), except lines tagged "LEGACY".
  3. Justification comments: every WITH SYSTEM_MODE / AccessLevel.SYSTEM_MODE /
     `without sharing` in project Apex has a "// SYSTEM_MODE:" or "// WITHOUT_SHARING:"
     comment on the same or previous line.
  4. sfdx-project.json sourceApiVersion (if present) is not lower than apiVersion.

Usage: python .github/scripts/check-consistency.py [--root .] [--src force-app]
"""
import argparse, json, pathlib, re, sys

ALLOW_OTHER_VERSIONS = {
    "platform-release-delta.md", "salesforce-platform.json", "CHANGELOG.md", "MIGRATION.md",
    "agentforce-mcp-architecture.md", "devops-alm.md", "org-strategy.md", "evals.json",
    "apex.instructions.md", "lwc.instructions.md", "metadata-xml.instructions.md",
    "SKILL.md", "copilot-instructions.md",
}
VERSION_RE = re.compile(r"(?:<apiVersion>|/v|sourceApiVersion\"\s*:\s*\")(\d{2}\.0)")
CODE_FENCE_RE = re.compile(r"```[\w-]*\n(.*?)```", re.S)


def load_cfg(root):
    return json.loads((root / ".github" / "salesforce-platform.json").read_text(encoding="utf-8"))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".")
    ap.add_argument("--src", default="force-app")
    a = ap.parse_args()
    root = pathlib.Path(a.root).resolve()
    cfg = load_cfg(root)
    api = cfg["apiVersion"]
    errors = []

    gh = root / ".github"
    docs = [p for p in gh.rglob("*") if p.suffix in {".md", ".json"} and p.is_file()]

    # 1. version drift in docs
    for p in docs:
        if p.name in ALLOW_OTHER_VERSIONS:
            continue
        for n, line in enumerate(p.read_text(encoding="utf-8").splitlines(), 1):
            for v in VERSION_RE.findall(line):
                if v != api:
                    errors.append(f"{p.relative_to(root)}:{n}: API version {v} != {api}")

    # 2. forbidden patterns in doc code blocks
    forb = [(re.compile(f["pattern"]), f["reason"]) for f in cfg.get("forbiddenPatterns", [])]
    for p in docs:
        if p.suffix != ".md":
            continue
        for block in CODE_FENCE_RE.findall(p.read_text(encoding="utf-8")):
            for line in block.splitlines():
                if any(m in line.upper() for m in ("LEGACY", "BAD", "❌", "VIOLATION", "NO LONGER", "DEPRECATED", "DO NOT USE")):
                    continue
                for rx, reason in forb:
                    if rx.search(line):
                        errors.append(f"{p.relative_to(root)}: forbidden in example → {line.strip()[:80]} ({reason})")

    # 2b/3. project source
    src = root / a.src
    if src.is_dir():
        for p in src.rglob("*"):
            if not p.is_file() or p.suffix not in {".cls", ".trigger", ".js", ".html", ".xml"}:
                continue
            lines = p.read_text(encoding="utf-8", errors="ignore").splitlines()
            for n, line in enumerate(lines, 1):
                for rx, reason in forb:
                    if rx.search(line):
                        errors.append(f"{p.relative_to(root)}:{n}: {reason}")
                if p.suffix == ".cls":
                    prev = lines[n - 2] if n > 1 else ""
                    if re.search(r"SYSTEM_MODE", line) and "// SYSTEM_MODE:" not in line + prev:
                        errors.append(f"{p.relative_to(root)}:{n}: SYSTEM_MODE without '// SYSTEM_MODE: <reason>'")
                    if re.search(r"\bwithout sharing\b", line) and "// WITHOUT_SHARING:" not in line + prev:
                        errors.append(f"{p.relative_to(root)}:{n}: without sharing without '// WITHOUT_SHARING: <reason>'")
            if p.name.endswith("-meta.xml"):
                m = re.search(r"<apiVersion>([\d.]+)</apiVersion>", "\n".join(lines))
                if m and float(m.group(1)) < float(api):
                    errors.append(f"{p.relative_to(root)}: apiVersion {m.group(1)} < baseline {api} (warning-level: bump in a dedicated PR)")

    # 4. sfdx-project.json
    sp = root / "sfdx-project.json"
    if sp.is_file():
        v = json.loads(sp.read_text()).get("sourceApiVersion")
        if v and float(v) < float(api):
            errors.append(f"sfdx-project.json sourceApiVersion {v} < baseline {api}")

    if errors:
        print(f"✗ {len(errors)} consistency issue(s):")
        for e in errors:
            print("  -", e)
        sys.exit(1)
    print(f"✓ consistency OK (baseline API {api}, validated {cfg.get('validatedOn')})")


if __name__ == "__main__":
    main()
