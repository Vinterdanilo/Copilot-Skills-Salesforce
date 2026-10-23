---
applyTo: "**/*.flow-meta.xml"
description: "Flow rules"
---
# Flow — path-scoped rules

- One automation strategy per object and event: decide Flow vs Apex trigger per object, document it, and do not mix both for the same timing without an explicit order.
- Before-save flows for same-record field updates; after-save for related records; async paths for callouts.
- No DML or Get Records inside loops; use collection variables and a single update.
- Fault paths on every DML/action element, routed to a logging subflow.
- Process Builder and Workflow Rules are retired — never generate them; offer migration to Flow.
- Invocable Apex called from Flow: `List<Input>` → `List<Output>`, `label` + `description`, public no-arg constructor on parameter classes.
