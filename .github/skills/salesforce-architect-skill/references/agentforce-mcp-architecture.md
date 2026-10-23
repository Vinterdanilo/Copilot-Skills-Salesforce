# Agentforce & MCP Architecture

## Contents
1. Building blocks · 2. Security model · 3. Patterns · 4. Testing and observability · 5. ALM for agents

## 1. Building blocks (as of Winter '27)
- **Agent Script + new Agentforce Builder** (GA Summer '26; legacy builder no longer used for new agents). Deterministic logic (`before_reasoning`, `else if`, `escalate`) mixed with reasoning.
- **Subagents** and **Multi-Agent Orchestration** (GA Winter '27): an orchestrator delegates to connected specialist agents.
- **Actions:** invocable Apex, Flows, Prompt Templates, MCP server tools from AgentExchange.
- **Grounding:** Agentforce Data Libraries (ADL Connect API Beta), Data 360 retrievers (context precision metrics).
- **Hosted MCP Servers:** standard servers (SObject, Data 360, Tableau) and custom servers exposing invocable Apex, flows, Apex REST, `@AuraEnabled`, Named Queries, prompts and **agents as MCP tools** (agents must be built with the new Agent Script Builder).
- **Headless Experience Layer (Beta):** widgets rendered in Agentforce, Claude and Slackbot from Custom Lightning Types.

## 2. Security model
- MCP calls and agent invocations run as the **authenticated user**; sharing, FLS and Trust Layer apply. Design tools with least privilege.
- Agent users: dedicated, minimal permission sets; `sf org create agent-user` for setup automation.
- Any action that elevates access (system-mode Apex) must be an ADR-level decision with auditing.
- External tool selection relies only on **name and description** — make tools task-specific ("Schedule customer meeting"), never a generic "Sales agent" tool.

## 3. Patterns
| Need | Pattern |
|---|---|
| External AI client needs Salesforce data/actions | Custom Hosted MCP server with narrow tools |
| Agent needs an external capability | MCP server tool from AgentExchange or invocable Apex with Named Credential |
| Cross-domain conversations | Orchestrator + connected subagents |
| Rich UI in agent responses | Custom Lightning Types (+ HXL widgets where Beta is acceptable) |
| Knowledge grounding | Data Library or Data 360 retriever; measure context precision before/after changes |

## 4. Testing and observability
- `sf agent preview` (GA) for scripted sessions, `sf agent trace read` for routing analysis, `sf agent test run-eval` (Beta) for YAML/JSON evaluation specs in CI.
- Custom Scorers (Beta) for KPI-based grading; retriever quality via `ssot__AiRetrieverQualityMetric__dlm`.
- Rehearse model changes: platform-level model reroutes happen (e.g., Gemini 2.5 family rerouted on 2026-10-20) — keep regression evals.

## 5. ALM for agents
- At API 68.0: `AiAgentDefinition` + `AiAgentDefinitionVersion`, retrieved with dependencies in one command; both orgs must be on 68.0.
- At 67.0: previous agent metadata types; list dependencies explicitly.
- Version agents, prompts and eval specs together in source control.
