---
applyTo: "**/*-meta.xml"
description: "Metadata XML rules"
---
# Metadata XML — path-scoped rules

- `apiVersion`: read `sourceApiVersion` from `sfdx-project.json`; fall back to `.github/salesforce-platform.json`. Never bump a single file in isolation — version changes go through a dedicated PR.
- Permission sets over profiles. Grant `classAccesses` for every Apex class exposed to LWC via `@AuraEnabled`; FLS only for fields that actually exist on that object.
- LWC `js-meta.xml`: declare only the `targets` the component really supports; expose design properties via `targetConfigs` (e.g., `botId` for `lightning/accApi` launchers).
- Agentforce agents at 68.0+: `AiAgentDefinition` + `AiAgentDefinitionVersion` (retrieve with `--root-type-with-dependencies`). At 67.0 keep using the previous agent metadata types.
