# AGENTS.md — Salesforce project

Universal entry point for coding agents (Codex, Cursor, Cline, Windsurf, Agentforce Vibes…).

Read `.github/copilot-instructions.md` first: it holds the always-on rules and the routing table.
Path-specific rules live in `.github/instructions/*.instructions.md` (match the file you are editing by its `applyTo` glob).
Skills: `.github/skills/salesforce-developer/` and `.github/skills/salesforce-architect-skill/`.
Platform baseline (API version, gated features, quality targets): `.github/salesforce-platform.json`.
