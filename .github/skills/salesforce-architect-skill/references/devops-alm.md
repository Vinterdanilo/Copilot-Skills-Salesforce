# DevOps & ALM

## Contents
1. Delivery models · 2. Branching · 3. Pipeline quality gates · 4. Packaging · 5. Secrets and auth · 6. API version policy

## 1. Delivery models
| Model | Use when | Watch out |
|---|---|---|
| Org-based (source tracking + CI deploy) | Single team, monolithic org | Dependency sprawl |
| Unlocked packages | Modular domains, multiple teams | Dependency graph discipline, package versioning |
| DevOps Center | Admin-heavy teams needing Git without CLI | Fewer customization options for complex pipelines |
| Managed 2GP | ISV / distributing locked internal apps | Namespace, upgrade compatibility, `withExplicitNamespace` (68.0) |

## 2. Branching
Trunk-based with short-lived feature branches is the default. Use release branches only if the business requires parallel release trains. Every org change goes through a PR.

## 3. Pipeline quality gates (minimum)
1. `sf code-analyzer run --rule-selector Recommended` (PMD, ESLint, ApexGuru where available) — fail on severity threshold agreed by the team.
2. `python .github/scripts/check-consistency.py` — no forbidden patterns, version drift or undocumented SYSTEM_MODE/without sharing.
3. Validation deploy with `RunLocalTests` against an integration org.
4. Jest for LWC.
5. Manual approval for UAT and production; quick deploy of the validated ID.

## 4. Packaging
Keep domain boundaries aligned with packages; shared kernel package for selectors/utilities; avoid circular dependencies; version Custom Metadata contracts.

## 5. Secrets and auth
- CI authenticates with JWT (External Client App + certificate), never username/password.
- Since Summer '26 the CLI redacts secrets; the `SF_TEMP_SHOW_SECRETS` escape hatch ended on 2026-10-28. Use `sf org auth show-access-token` explicitly and mask it in CI logs.
- CLI requires Node.js 22+ — pin it in the pipeline image.

## 6. API version policy
- One `sourceApiVersion` per project; bump in a dedicated PR after the preview-sandbox rehearsal.
- Production integrations pin a REST version; scripts may use `/services/data/latest/`.
- Inventory and remove integrations on API 31.0–40.0 (deprecated Summer '27, retired Summer '28) and SOAP `login()` (Use Any API Auth from 2026-12-01; retirement for 31.0–64.0 in Summer '27).
