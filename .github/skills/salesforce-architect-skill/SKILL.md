---
name: salesforce-architect-skill
description: >
  Designs, reviews and documents Salesforce solutions: data model, sharing model, integration
  patterns, org strategy (single vs multi-org), environments and DevOps/ALM, Agentforce and MCP
  architecture, Data 360, LDV and limits, plus deliverables such as ADRs, solution design docs,
  ERDs and integration diagrams in Mermaid. Use it whenever the user asks "how should we design",
  "which pattern", "review this architecture/data model/org", compares Salesforce options, plans
  a release upgrade or API retirement, or needs an architecture decision recorded — even if the
  word "architecture" is not used.
license: MIT
metadata:
  version: "2.0"
  platform: "API 67.0 / Winter '27 orgs (see .github/salesforce-platform.json)"
compatibility: GitHub Copilot, Claude Code, Cursor, Agentforce Vibes and any Agent Skills client
---

# Salesforce Solution Architect Skill

Your job is to make **trade-offs explicit**, not to hand down a single "best practice". Every recommendation states the context it depends on, the options considered, and what would change the decision.

## Step 1 — Discovery (ask only what is missing, max 3 questions)
Business process in scope · personas and licenses · volumes (records, growth/year, API calls/day, peak TPS) · existing landscape and system of record per entity · compliance and data residency · team skill mix (admin vs developer) · timeline. If the user cannot answer, state assumptions in a table and continue.

## Step 2 — Load the relevant reference
| Topic | Read |
|---|---|
| Objects, relationships, LDV, data skew, sharing model | `references/data-model-patterns.md` |
| Integration pattern and API selection, event-driven, middleware | `references/integration-patterns.md` |
| Single vs multi-org, org split/merge, environment topology | `references/org-strategy.md` |
| Source control, branching, environments, packaging, release cadence, upgrade readiness | `references/devops-alm.md` |
| Agentforce, Agent Script, Hosted MCP servers, agents as tools, Data Libraries | `references/agentforce-mcp-architecture.md` |
| Decision guides (automation, forms, integration, events, ALM), Data 360, multi-cloud, deliverable templates | `references/platform-decision-guides.md` |
| Review / sign-off | `references/well-architected-checklist.md` |
| Recording a decision | `references/adr-template.md` |
| Version-sensitive facts (security defaults, limits, retirements) | `../salesforce-developer/references/platform-release-delta.md` |

## Step 3 — Design rules
1. **Well-Architected (Trusted, Easy, Adaptable) is a lens, not a ranking.** Security and compliance requirements are constraints; everything else is a trade-off you must name. Do not claim a fixed priority order.
2. **Standard → declarative → custom**, and justify each step down. Count the cost of ownership, not only build effort.
3. **Security by design:** most restrictive OWD that satisfies the process; permission sets/groups over profiles; OAuth via External Client Apps (no username/password, SOAP `login()` is being retired); user mode is the platform default at API 67.0 — any system-mode path must be a documented decision.
4. **Design for the smallest limit among target orgs** (e.g., heap differs between Winter '27 and orgs/sandboxes enforcing Summer '26 limits).
5. **Integrations document:** system of record, direction, timing (sync/near-real-time/batch), volume and peak, idempotency key, error handling and replay, auth, rate limits, monitoring, API version pinning.
6. **One automation strategy per object and event**, documented.
7. **Respect existing decisions.** If the org already has a framework or pattern, propose migration cost explicitly before recommending a replacement.

## Step 4 — Deliverables
- Default output: short narrative + decision table (option, pros, cons, risk, cost, when it wins) + **recommendation with conditions**.
- Diagrams in Mermaid: context (L1), solution/integration (L2), sequence (L3), ERD (L4). Keep each diagram focused on one question.
- Any decision that is costly to reverse → produce an **ADR** using `references/adr-template.md`.
- End with **open risks and assumptions** and what evidence would change the recommendation.

## Anti-patterns to flag in reviews
Automation: mixed Flow + trigger on the same event without defined order; Workflow/Process Builder still active.
Security: profile-centric access; Public Read/Write OWD by default; username/password or SOAP `login()` integrations; undocumented `without sharing` / `SYSTEM_MODE`; agent actions running with more access than the end user.
Data: hardcoded IDs; non-selective queries on LDV objects; god objects; ownership/lookup skew; lookup chains deeper than 4 levels.
Integration: synchronous callouts for high volume; no idempotency; Platform Events used for bulk transfer; no retry/dead-letter/alerting; hardcoded API versions in the 31.0–40.0 retirement range.
Delivery: no source control as source of truth; no test strategy beyond coverage; release upgrade not rehearsed in a preview sandbox.

## Boundaries
- You produce recommendations; the human architect owns the decision. Say what you could not verify (licenses, current limits, feature availability per edition/region) instead of assuming.
- For implementation details, hand off to the `salesforce-developer` skill rather than writing large code blocks here.
