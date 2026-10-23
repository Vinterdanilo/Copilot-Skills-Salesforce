# Salesforce — Repository Instructions (always loaded)

You are working in a Salesforce DX project. Keep this file short: detailed rules load on demand.

## Platform baseline
- **API version:** use `sourceApiVersion` from the project's `sfdx-project.json`. If absent, use `apiVersion` from `.github/salesforce-platform.json` (currently **67.0**, orgs on **Winter '27**).
- Never write a version number from memory. Features gated to **68.0** (listed in `salesforce-platform.json → gatedFeatures`) are allowed only if the project is on 68.0+.
- If this file and the project's own conventions disagree, **the project wins** — ask before changing an existing pattern (trigger framework, logging, naming).

## Non-negotiable rules (apply to every answer)
1. **Bulkify:** no SOQL, DML or callouts inside loops. Design for 200+ records per transaction.
2. **Explicit access mode on every database operation:** `WITH USER_MODE` / `AccessLevel.USER_MODE` / `insert as user`. `SYSTEM_MODE` only with a `// SYSTEM_MODE: <reason>` comment on the line above. `WITH SECURITY_ENFORCED` **does not compile** at 67.0 — never generate it.
3. **Explicit sharing keyword on every class** (`with sharing` default; `inherited sharing` for utilities; `without sharing` only with a `// WITHOUT_SHARING: <reason>` comment). Triggers run in system mode and cannot declare sharing — the handler decides.
4. **No hardcoded IDs, URLs or credentials** — Custom Metadata, Custom Labels, Named Credentials / External Credentials.
5. **Every test asserts behavior** (positive, negative, bulk, `System.runAs` for user-facing code). Coverage is a by-product.
6. **Always ship `-meta.xml`** with classes, triggers and LWC bundles.
7. Use `sf` CLI (Node.js 22+). Never print or log secrets.

## Where the details live (load only what the task needs)
| Task | Load |
|---|---|
| Write/review Apex, LWC, SOQL, Flow, tests, deploy | skill `salesforce-developer` |
| Design, data model, integration, org strategy, ADR, review | skill `salesforce-architect-skill` |
| Editing `*.cls` / `*.trigger` / `*Test.cls` / `lwc/**` / `*-meta.xml` / flows | matching file in `.github/instructions/` (auto-applied by path) |
| Full coding standard (long, consult sections, don't read end to end) | `.github/standards/apex-coding-rules.md`, `.github/standards/lwc-coding-rules.md` |
| What changed in API 67.0 / Winter '27 | `skills/salesforce-developer/references/platform-release-delta.md` |

## Real enforcement
These instructions are guidance. The source of truth for quality is CI: Code Analyzer (PMD + ESLint), Apex tests and `.github/scripts/check-consistency.py`. Never suggest disabling a rule to make CI pass without stating the trade-off.
