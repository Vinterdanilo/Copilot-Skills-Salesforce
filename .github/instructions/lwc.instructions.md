---
applyTo: "**/lwc/**"
description: "Lightning Web Components rules"
---
# LWC — path-scoped rules

**Templates**
- `lwc:if` / `lwc:elseif` / `lwc:else` only. Every `for:each` item needs a stable `key`.
- **Template expressions are GA in Winter '27** (component API 66.0+): `{a ? b : c}`, template literals, `?.`, `??`, simple `.filter().length`. Rules: quote attribute expressions (`class="{...}"`), no `this`, no `new`, no function declarations. Keep them trivial — anything with business meaning, reuse or >1 operator chain goes to a getter (testable in Jest).
- Group native `<details name="...">` for zero-JS exclusive accordions (API 67.0).

**State and data**
- Prefer Lightning Data Service, built-in state managers (`lightning/stateManagerRecord`, `lightning/stateManagerRelatedListRecords`…) and `@lwc/state` (`defineState`) before custom Apex.
- Wire for reads, imperative Apex for side effects; `async/await` + `try/catch/finally`, reset loading state in `finally`.
- `@AuraEnabled(cacheable=true)` only for pure reads.

**Security (Lightning Web Security)**
- No `data:` URIs on anchors for downloads — LWS blocks them since Summer '26. Use `Blob` + `URL.createObjectURL()` and revoke after click.
- Third-party web components: load as IIFE/UMD static resource via `loadScript`, render with `lwc:external` (GA Winter '27, requires LWS).
- Never `innerHTML` with dynamic content, `eval`, or secrets in component state/storage.

**Communication:** `@api` down, `CustomEvent` up (lowercase names, no hyphens), LMS across the DOM. `NavigationMixin` for navigation. `lightning/toast` / `lightning/alert` instead of `window.*`.

**Tests:** Jest in `__tests__/`, clean the DOM in `afterEach`, mock wire adapters and Apex. ESLint with `@salesforce/eslint-config-lwc/recommended` + LWS rules must pass.
