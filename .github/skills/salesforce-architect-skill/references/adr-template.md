# Architecture Decision Record (ADR) — Template

Use for decisions that are expensive to reverse: org strategy, integration pattern, data model of a core object, automation strategy per object, security model, packaging strategy, build vs buy.

```markdown
# ADR-NNN: <short decision title>

- **Status:** Proposed | Accepted | Superseded by ADR-XXX | Deprecated
- **Date:** YYYY-MM-DD
- **Deciders:** <names/roles>
- **Platform baseline:** API <version from salesforce-platform.json>, org release <release>

## Context
What problem are we solving? Business drivers, constraints (compliance, licenses, limits, team skills),
volumes (records, growth, API calls, peak TPS). Link requirements.

## Options considered
| Option | Pros | Cons | Risk | Cost (build + run) | Wins when |
|---|---|---|---|---|---|
| A | | | | | |
| B | | | | | |
| C (do nothing / standard) | | | | | |

## Decision
We choose **<option>** because <reasons tied to the context>.

## Consequences
- Positive:
- Negative / accepted trade-offs:
- Follow-up work (tickets):

## Well-Architected lens
- Trusted (security, compliance, reliability):
- Easy (UX, maintainability, time to value):
- Adaptable (scale, extensibility, release-upgrade resilience):

## Revisit triggers
Conditions that reopen this decision (volume threshold, new license, platform feature GA, API retirement).
```

Rules for the assistant:
- Always include at least one option you do **not** recommend, including "standard feature / do nothing".
- Write "Revisit triggers" with measurable conditions.
- Never mark an ADR as Accepted — only humans accept.
