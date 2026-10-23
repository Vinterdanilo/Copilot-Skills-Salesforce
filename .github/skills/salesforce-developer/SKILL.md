---
name: salesforce-developer
description: >
  Generates, reviews and debugs Salesforce platform code: Apex classes, triggers, tests,
  SOQL/SOSL, Lightning Web Components, Flows and invocable actions, metadata XML, REST/Bulk
  integrations, Agentforce actions and sf CLI deployments. Use it for ANY Salesforce coding
  task, even small ones, and whenever .cls, .trigger, .js-meta.xml, lwc/, flow-meta.xml or
  sfdx-project.json files are involved, or the user mentions Apex, LWC, SOQL, governor limits,
  user mode, sharing, Agentforce actions or Salesforce deployment.
license: MIT
metadata:
  version: "3.0"
  platform: "API 67.0 / Winter '27 orgs (see .github/salesforce-platform.json)"
compatibility: GitHub Copilot, Claude Code, Cursor, Agentforce Vibes and any Agent Skills client
---

# Salesforce Developer Skill

## Step 0 — Establish context before writing code
1. Read `sourceApiVersion` from the project's `sfdx-project.json`; fall back to `.github/salesforce-platform.json`. Use that version everywhere. Never use a version from memory.
2. Look for existing conventions in the project (trigger framework such as fflib/TDTM/O'Hara, logging library, selector base class, naming). **Follow them** over the defaults below.
3. If an org-aware MCP server is available (Salesforce DX MCP, Hosted MCP), use it to confirm object/field API names before referencing them. Never invent fields.

## Step 1 — Load only the reference you need
| Task | Read |
|---|---|
| Apex classes, triggers, async, JSON, error handling | `references/apex-patterns.md` |
| SOQL/SOSL, selectivity, LDV, cursors | `references/soql-optimization.md` |
| LWC, wire, LDS, dynamic components | `references/lwc-guide.md` |
| REST/Bulk/SOAP, OAuth, Named Credentials | `references/api-integration.md` |
| Flows, invocable Apex | `references/flows-automation.md` |
| Sharing, CRUD/FLS, user/system mode | `references/security-sharing.md` |
| sf CLI, CI/CD, packaging | `references/deployment-devops.md` |
| Agentforce actions, Prompt Builder, Platform Events, CDC | `references/agentforce-ai.md` |
| Formulas, validation rules | `references/formulas-validation.md` |
| **Anything version-sensitive** (security defaults, heap, LWC template syntax, retired APIs) | `references/platform-release-delta.md` |

The long standards in `../../standards/` are a lookup source: search the section you need, do not read them end to end.

## Step 2 — Generate following the non-negotiables
1. **Bulkified:** no SOQL/DML/callouts in loops; Maps for lookups; 200+ records per trigger batch.
2. **Explicit access mode** on every query and DML (`WITH USER_MODE`, `AccessLevel.USER_MODE`, `insert as user`). `SYSTEM_MODE` needs `// SYSTEM_MODE: <reason>`. **Never `WITH SECURITY_ENFORCED`** (compile error at 67.0).
3. **Explicit sharing keyword** on every class; `without sharing` needs `// WITHOUT_SHARING: <reason>`. Triggers cannot declare sharing (always system mode) — the handler decides.
4. **Layering:** Trigger → Handler → Service → Selector, unless the project uses another framework.
5. **Errors:** no empty `catch`; `addError()` in trigger context; `AuraHandledException` to LWC; partial-success DML with `SaveResult` inspection when appropriate.
6. **Config, not constants:** Custom Metadata / Labels / Named Credentials; no hardcoded IDs or URLs.
7. **Files:** every class/trigger/LWC ships with its `-meta.xml` at the project API version.

## Step 3 — Self-check before answering (LLM anti-patterns)
Run this list against your own output and fix before replying:
- **A1** every field used in Apex is in the SELECT. **A2** parent via dot notation, children via subquery.
- **A3/A4** no Java-isms: `StringBuilder`, `HashMap`, `ArrayList`, `int`, `char`, `List.sort(comparator)` on non-Comparator types.
- **A5** static vs instance calls (`String.isBlank(s)`, `s.toLowerCase()`).
- **S1** no `WITH SECURITY_ENFORCED`; access mode declared on every operation.
- **S2** sharing keyword present; no sharing keyword on triggers.
- **R1** query into a `List` and check `isEmpty()` before `[0]`. **R2** `containsKey` before `get` when null matters. **R3** recursion guard is `Set<Id>`, not `Boolean`.
- **I1** no callout after uncommitted DML. **I2** no `api.salesforce.com` for same-org calls.
- **L1** LWC template expressions only if trivial and API ≥ 66.0; otherwise a getter. **L2** decorators imported from `lwc`. **L3** event names lowercase, no hyphens. **L4** no `data:` URI downloads (LWS).
- **AF1** invocable parameter classes have a public no-arg constructor; `@InvocableVariable` types exclude Maps.
- **V1** every 68.0-only feature is gated (project on 68.0+) and flagged as Beta where applicable.

## Step 4 — Tests and verification
- Generate tests together with the code: positive, negative, bulk (200), `System.runAs` for user-facing code. Every method asserts.
- Tell the user how to verify: `sf apex run test --code-coverage --result-format human`, `sf code-analyzer run --rule-selector Recommended`, and Jest for LWC.
- If you could not verify field names, limits or a feature's availability, **say so** instead of guessing.

## Governor limits (sync / async)
SOQL 100/200 · rows 50,000 · DML 150 · DML rows 10,000 · CPU 10s/60s · **heap 10 MB / 25 MB (Winter '27; 6/12 MB if the sandbox enforces Summer '26 limits)** · callouts 100.

## Order of execution (summary)
System validation → before-save flows → before triggers → custom validation → duplicate rules → save (no commit) → after triggers → assignment/auto-response rules → after-save flows → roll-ups → sharing recalculation → commit → post-commit (email, async Apex, async flow paths). Workflow Rules and Process Builder are retired; do not generate them.
