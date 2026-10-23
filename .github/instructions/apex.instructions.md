---
applyTo: "**/*.cls,**/*.trigger"
description: "Apex rules applied automatically when editing Apex classes and triggers"
---
# Apex — path-scoped rules

**Architecture:** Trigger (logic-free, one per object) → Handler (`switch on Trigger.operationType`, recursion guard with `static Set<Id>`) → Service (stateless business logic, DML) → Selector (all SOQL for one SObject).

**Access mode (API 67.0):**
- Database operations default to user mode at 67.0, but **always declare it explicitly** — classes saved at older versions behave differently and reviewers must see intent.
- SOQL: `WITH USER_MODE`. DML: `insert as user`, `Database.update(records, false, AccessLevel.USER_MODE)`.
- System mode is opt-in: `// SYSTEM_MODE: <business reason>` on the line above `WITH SYSTEM_MODE` / `AccessLevel.SYSTEM_MODE`.
- `WITH SECURITY_ENFORCED` does not compile at 67.0. Migrate on sight.
- Triggers always run in system mode and cannot declare sharing; put security-relevant logic in the handler/service with an explicit keyword and access level.
- Handlers processing records the running user cannot see (cross-object roll-ups, integration users) must decide consciously between USER_MODE and documented SYSTEM_MODE — call this out in the PR description.

**Sharing:** every class declares `with sharing`, `inherited sharing` or `without sharing` (`// WITHOUT_SHARING: <reason>`). At 67.0 "no keyword" means `with sharing`, but implicit is not allowed here.

**Language features available at 67.0** (prefer them):
- Multiline strings `'''...'''` and `String.template(Map<String,Object>)` instead of `+ '\n' +` chains or `String.format` index juggling. Note: `String.template()` renders `Datetime` in GMT.
- `Assert` class, safe navigation `?.`, `switch on`, Queueable + `System.attachFinalizer()` over `@future`.
- Invocable parameter classes need a visible no-arg constructor.
- `sf template generate apex class --template Queueable|Batchable` produces a compliant skeleton.

**Limits:** heap is 10 MB sync / 25 MB async since Winter '27 — unless the sandbox enforces the Summer '26 limit (6/12 MB) while production is behind. Do not design for the bigger heap if any target org is still on Summer '26.

**Never:** SOQL/DML/callouts in loops; `Boolean` recursion guards; empty `catch`; hardcoded IDs; `global` outside managed packages or web services; callout after uncommitted DML.
