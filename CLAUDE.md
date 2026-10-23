# CLAUDE.md

@AGENTS.md

Claude Code notes:
- Skills can also be installed under `.claude/skills/` (copy or symlink `.github/skills/*`).
- If the official Salesforce Development plugin (`forcedotcom/sf-skills`) is installed, treat it as the generic layer and this repository's rules as the project-specific layer: on conflict, this repository wins.
- Prefer org-aware tools (Salesforce DX MCP Server, Hosted MCP) to confirm object/field names before generating code.
