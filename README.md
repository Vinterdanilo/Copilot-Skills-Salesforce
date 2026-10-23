# Copilot Skills — Salesforce (v2, API 67.0 · orgs Winter '27)

Fork evoluído de [SalesforceDiariesBySanket/Copilot-Skills-Salesforce](https://github.com/SalesforceDiariesBySanket/Copilot-Skills-Salesforce) (MIT). Conteúdo original preservado e corrigido; estrutura, enforcement e baseline de plataforma reescritos.

## O que mudou em relação à v1
| Problema na v1 | Solução na v2 |
|---|---|
| `WITH SECURITY_ENFORCED` recomendado — **não compila na API 67.0** | `WITH USER_MODE` explícito em toda operação; `SYSTEM_MODE` só com justificativa verificada no CI |
| Leitura obrigatória de ~10 mil linhas antes de cada resposta | Entrada enxuta + regras por caminho (`applyTo`) + referências sob demanda |
| Versão da API fixa em vários arquivos | `salesforce-platform.json` como fonte única + `bump-api-version.py` |
| Regras só como sugestão | `check-consistency.py`, Code Analyzer e evals com asserções no GitHub Actions |
| Cobertura de 95% como meta | Asserts obrigatórios (positivo, negativo, bulk, `runAs`) + meta configurável |
| Lado de arquiteto raso | ADR, estratégia de org, DevOps/ALM, Agentforce & MCP |
| Pasta `Blogs/` | `standards/` |

## Estrutura
```
.
├── AGENTS.md                         # entrada universal (Codex, Cursor, Cline, Windsurf, Vibes)
├── CLAUDE.md                         # entrada Claude Code (importa AGENTS.md)
├── README.md · MIGRATION.md · CHANGELOG.md
└── .github/
    ├── copilot-instructions.md       # SEMPRE carregado — curto (regras inegociáveis + roteamento)
    ├── salesforce-platform.json      # fonte única: API, recursos 68.0 bloqueados, metas de qualidade
    ├── instructions/                 # aplicados automaticamente por caminho (applyTo)
    │   ├── apex.instructions.md          **/*.cls, **/*.trigger
    │   ├── apex-tests.instructions.md    **/*Test.cls
    │   ├── lwc.instructions.md           **/lwc/**
    │   ├── metadata-xml.instructions.md  **/*-meta.xml
    │   └── flows.instructions.md         **/*.flow-meta.xml
    ├── standards/                    # rulesets longos (consulta por seção)
    │   ├── apex-coding-rules.md
    │   └── lwc-coding-rules.md
    ├── skills/
    │   ├── salesforce-developer/
    │   │   ├── SKILL.md              # ~90 linhas: contexto → referência → regras → autochecagem
    │   │   ├── references/           # 9 originais corrigidas + platform-release-delta.md
    │   │   └── evals/evals.json      # casos com asserções verificáveis
    │   └── salesforce-architect-skill/
    │       ├── SKILL.md              # ~80 linhas: trade-offs explícitos
    │       ├── references/           # +adr-template, org-strategy, devops-alm,
    │       │                         #  agentforce-mcp-architecture, platform-decision-guides
    │       └── evals/evals.json
    ├── scripts/
    │   ├── validate-skill.py         # frontmatter, tamanho, links quebrados, evals
    │   ├── check-consistency.py      # drift de versão, padrões proibidos, justificativas
    │   ├── bump-api-version.py       # sobe a baseline inteira em um PR
    │   └── grade-evals.py            # corrige respostas salvas contra as asserções
    └── workflows/
        ├── ai-instructions-quality.yml   # PR em .github/** + mensal (reviewBy)
        └── salesforce-code-quality.yml   # PR em force-app/**: Code Analyzer + consistência + Jest
```

## Como usar
1. Copie `.github/`, `AGENTS.md` e `CLAUDE.md` para a raiz do projeto SFDX.
2. Edite `.github/salesforce-platform.json` (`owner`, `reviewBy`, metas). O `sourceApiVersion` do `sfdx-project.json` prevalece.
3. Rode localmente:
   ```bash
   pip install pyyaml
   python .github/scripts/validate-skill.py .github/skills/salesforce-developer .github/skills/salesforce-architect-skill
   python .github/scripts/check-consistency.py --src force-app
   ```
4. Personalize com as decisões do seu time (framework de trigger, logging, nomenclatura).

## Relação com as skills oficiais da Salesforce
Desde o Summer '26 a Salesforce publica a biblioteca oficial `forcedotcom/sf-skills` e, no Winter '27, o plugin *Salesforce Development* para Claude Code com MCP hospedado. Use-os como **camada genérica**; este repositório é a **camada do seu time/org** (padrões, decisões, enforcement). Em conflito, este repositório vence.

## Ciclo de manutenção (3 releases/ano)
Preview sandbox → revisar `platform-release-delta.md` → `bump-api-version.py` em PR dedicado → evals → merge. O workflow mensal falha quando `reviewBy` vence.
