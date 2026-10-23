# Changelog

## 2.0.0 — 2026-10-23 (baseline API 67.0, orgs on Winter '27)

### Breaking
- `WITH SECURITY_ENFORCED` removed from every rule and example (does not compile at API 67.0); replaced by `WITH USER_MODE`.
- `Blogs/` renamed to `standards/` (`apex-coding-rules.md`, `lwc-coding-rules.md`).
- `copilot-instructions.md` no longer forces reading every skill, ruleset and reference before each answer.
- `skills/scripts/` moved to `.github/scripts/`.

### Fixed
- `inherited sharing` documented as `without sharing` when there is no caller context — it runs `with sharing`.
- Trigger handler guidance updated: triggers run in system mode at 67.0 and cannot declare sharing.
- Heap limits (10/25 MB in Winter '27), Workflow/Process Builder references, LWC inline-expression rule (template expressions GA in Winter '27).

### Added
- `salesforce-platform.json` as the single source of truth for version, gated 68.0 features and quality targets.
- Path-scoped `.github/instructions/` (Apex, Apex tests, LWC, metadata XML, Flow).
- `platform-release-delta.md` (Summer '26 + Winter '27), architect references: ADR template, org strategy, DevOps/ALM, Agentforce & MCP architecture.
- Machine-checkable evals + `grade-evals.py`, `check-consistency.py`, `bump-api-version.py`, CI workflows.
- `AGENTS.md` and `CLAUDE.md` entry points.

### Changed
- Coverage policy: behavior-driven assertions with configurable target instead of a fixed 95%.
- Developer SKILL.md from 289 to ~90 lines; architect SKILL.md from 402 to ~80 lines (deep-dive moved to references).
