# Org Strategy — Single vs Multi-Org and Environment Topology

## Contents
1. Decision drivers · 2. Patterns · 3. Signals to split or merge · 4. Environment topology · 5. Release upgrades

## 1. Decision drivers
| Driver | Favors single org | Favors multi-org |
|---|---|---|
| Shared customer view across BUs | Strong | Requires integration / Data 360 |
| Divergent processes and governance | Weak | Strong |
| Data residency / regulatory isolation | Weak | Strong |
| Limits (storage, API, LDV, sharing recalculation) | Risky at very large scale | Isolates load |
| Release independence between BUs | Coupled releases | Independent cadence |
| Total cost of ownership | Lower | Higher (integration, licenses, admin) |

## 2. Patterns
- **Single org, multiple BUs:** record types, permission set groups, BU-scoped sharing, Custom Metadata per BU. Governance board for shared objects.
- **Hub and spoke:** a hub org (customer master) with spoke orgs; Salesforce Connect / platform events / middleware between them.
- **Multi-org with Data 360:** orgs remain systems of record; Data 360 harmonizes for unified profile and activation (system of reference, not of record).
- **Industry/regional isolation:** separate orgs per residency zone, consolidated analytics.

## 3. Signals to reconsider
Split: sharing recalculations measured in hours; conflicting automation per BU on the same objects; release freezes blocking BUs; residency mandates.
Merge: duplicated master data with constant reconciliation; integration cost greater than governance cost; license overlap.

## 4. Environment topology (baseline)
Developer (scratch orgs or Developer sandboxes) → Integration/QA (Developer Pro or Partial) → UAT (Partial or Full) → Staging/Pre-prod (Full) → Production.
- Source control is the source of truth; no direct production changes except emergency procedures with retro-commit.
- One **preview sandbox** kept on the next release during the preview window to rehearse upgrades.
- Scratch org definitions under version control; use `roleDeveloperName` in user definitions for realistic sharing tests (Winter '27).

## 5. Release upgrades (three times a year)
- Track preview dates; refresh the preview sandbox; run the full test suite and key UI journeys.
- When a sandbox is ahead of production, check settings such as *Enforce the Summer '26 Apex heap limit* to avoid deploying code that only works with the newer limits.
- Review the release-delta reference and update `.github/salesforce-platform.json` via `scripts/bump-api-version.py` in a dedicated PR.
