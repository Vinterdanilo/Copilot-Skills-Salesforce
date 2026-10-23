# Platform Release Delta — API 67.0 (Summer '26) and Winter '27 (API 68.0)

> Validated on 2026-10-23 against the Salesforce Developers Blog release guides for Summer '26 and Winter '27.
> Review owner and next review date: `.github/salesforce-platform.json`.
> This file overrides any conflicting statement in older references or standards.

## Contents
1. Breaking changes at API 67.0 (code that stops compiling or changes behavior)
2. New capabilities at API 67.0
3. Winter '27 org-level changes (apply regardless of component API version)
4. Gated to API 68.0
5. Integration and CLI deadlines
6. Tooling for coding agents

---

## 1. Breaking changes at API 67.0

| Change | Impact | What to generate |
|---|---|---|
| SOQL, SOSL, DML and `Database` methods default to **user mode** | Code that silently relied on system mode now hits FLS/sharing errors | Declare mode explicitly on every operation; `SYSTEM_MODE` only with a justification comment |
| Class with **no sharing keyword** defaults to `with sharing` (was `without sharing`) | Utility classes may suddenly filter records | Always declare a keyword |
| `WITH SECURITY_ENFORCED` **no longer compiles** | Deploy failure | `WITH USER_MODE` (also checks WHERE, polymorphic fields, reports all inaccessible fields via `QueryException.getInaccessibleFields()`) |
| **Triggers always run in system mode** and cannot declare sharing/access mode | Security logic in trigger body is not enforced | Move logic to handler/service with explicit keyword and access level |
| Invocable action parameter classes need a **visible no-arg constructor** | Runtime failure of Flow/Agent actions | Add `public MyInput() {}` |
| LWS blocks `data:` URIs on `HTMLAnchorElement.href` (plus new distortions: `getAttribute`, `innerHTML` getters, `MutationObserver.observe`, IndexedDB, Promise methods) | Client-side downloads break | `Blob` + `URL.createObjectURL()`; run the LWS ESLint rules |

### Migration recipe for an existing class moving to 67.0
1. Replace every `WITH SECURITY_ENFORCED` with `WITH USER_MODE`.
2. Add an explicit sharing keyword where missing.
3. For each query/DML, decide USER_MODE vs SYSTEM_MODE; justify SYSTEM_MODE.
4. Run tests with `System.runAs` a restricted user — this is where regressions appear.
5. Bump `apiVersion` in the `-meta.xml` last, in the same PR.

## 2. New capabilities at API 67.0
- **Apex multiline strings** (`'''`) and **`String.template()`** with `${name}` placeholders. The newline right after the opening `'''` is trimmed; `Datetime` renders in GMT `yyyy-MM-dd HH:mm:ss`.
- **LWC State Managers (GA):** `defineState` from `@lwc/state` (`atom`, `computed`, `setAtom`) plus built-in `lightning/stateManager*` modules over LDS.
- **LWC `<details name>` grouping** for exclusive accordions without JS; faster hot module reload.
- **`lightning/accApi`:** `open`, `close`, `execute(utterance, botId)` to drive the Agentforce panel from LWC (execute does not return the reply).
- **Dynamic lists (Developer Preview):** `lightning-dynamic-list-container` / `-item` virtualization.
- **Elastic async limits (Beta):** Queueable/@future beyond the daily limit, throttled not rejected; Batch added in Winter '27.

## 3. Winter '27 org-level changes
- **Heap:** 10 MB sync / 25 MB async (from 6/12). Sandboxes ahead of production can enable *Enforce the Summer '26 Apex heap limit*; design to the smallest limit among target orgs.
- **LWC complex template expressions (GA)** for components at API 66.0+. Restrictions: quote attribute expressions, no `this`, `new` or function declarations. Team rule: trivial display logic only; business logic stays in getters.
- **`lwc:external` (GA):** native third-party web components, IIFE/UMD via `loadScript`, requires LWS.
- **`refresh()` on state managers** without a single record id (e.g., related lists); call only when status is `loaded`.
- **Apex integration tests (`@IntegrationTest`, Developer Preview):** scratch orgs only, real callouts, no coverage credit, no rollback (`@TearDown` required), one class per org at a time, async only.
- **Recompile only invalid Apex** classes/triggers from Setup or Tooling `apexCompileResults`.
- Compiler warns on classes saved at API 9.0–19.0.
- **Web Console GA**; Developer Console hidden by default.

## 4. Gated to API 68.0 (use only if the project is on 68.0+)
- `FORMULA()` in SOQL `WHERE` (Beta, not available in production).
- `Database.QueryOptions.builder().withExplicitNamespace(true)` + `SET OPTIONS :options` for managed packages (`SET OPTIONS` must come after WHERE/ORDER BY/LIMIT/OFFSET; only `FOR UPDATE` may follow).
- Agent metadata: `AiAgentDefinition` + `AiAgentDefinitionVersion`, retrieved with `--root-type-with-dependencies`; both orgs must be on 68.0.
- Test Discovery API `testLevel` (replaces `showAllMethods`).
- Apex cursors over Data 360 DMOs (Beta) — consumes Data Services credits; cursors expire after 24h.

## 5. Integration and CLI deadlines
| Date | Change | Action |
|---|---|---|
| 2026-10-28 | `SF_TEMP_SHOW_SECRETS` workaround removed | Use `sf org auth show-access-token` / `show-sfdx-auth-url`; fix CI scripts that read `accessToken` from `org display --json` |
| 2026-12-01 | SOAP `login()` requires the **Use Any API Auth** permission | Assign or migrate |
| Summer '27 | SOAP `login()` retired for API 31.0–64.0; API 31.0–40.0 deprecated | Move to OAuth (External Client Apps, JWT) |
| Summer '28 | SOAP/REST/Bulk API 31.0–40.0 retired | Remove hardcoded old versions |

- REST supports `/services/data/latest/` — fine for scripts and internal tools; **pin a version for production integrations**.
- Salesforce CLI requires **Node.js 22+**. `sf api request rest|graphql` is GA.
- `sf template generate apex class --template Queueable|Batchable` scaffolds best-practice async classes.

## 6. Tooling for coding agents
- **Official skills:** `forcedotcom/sf-skills` (Agent Skills format) and the *Salesforce Development* plugin for Claude Code. This repository is meant to sit **on top of** them as the team/org standards layer — do not duplicate their generic content; encode your project's decisions here.
- **Salesforce DX MCP Server:** ApexGuru (`scan_apex_class_for_antipatterns`, `scale-products` toolset), SLDS guidance, metadata context.
- **Apex Symbol API (Beta, Tooling):** real type information to ground code generation — prefer it over memory for method signatures.
