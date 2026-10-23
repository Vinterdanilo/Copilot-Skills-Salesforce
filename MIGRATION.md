# Migração da v1 (repositório original) para a v2

1. **Faça backup** da sua `.github/` atual e copie a nova por cima. Remova a pasta antiga `.github/Blogs/` e `.github/skills/scripts/`.
2. **Ajuste o baseline** em `.github/salesforce-platform.json` (`apiVersion`, `owner`, `reviewBy`, `quality.coverageTarget`). Se o seu `sfdx-project.json` tiver `sourceApiVersion`, ele prevalece.
3. **Rode** `python .github/scripts/check-consistency.py --src force-app`. Os erros apontam:
   - `WITH SECURITY_ENFORCED` no seu código (não compila na 67.0);
   - `SYSTEM_MODE` / `without sharing` sem justificativa;
   - `-meta.xml` abaixo do baseline.
4. **Migre classes para 67.0 em lotes pequenos** seguindo a receita em `skills/salesforce-developer/references/platform-release-delta.md` (seção 1). Teste com `System.runAs` usuário restrito — é onde a mudança de default para user mode aparece.
5. **Personalize** as regras com as decisões do seu time (framework de trigger, logging, nomenclatura). Elas são o diferencial em relação às skills oficiais genéricas (`forcedotcom/sf-skills`).
6. **Ative os workflows** em `.github/workflows/` e rode as evals depois de cada customização.

## Por que a API 67.0 com orgs em Winter '27?
Winter '27 corresponde à API 68.0, mas fixar os componentes em 67.0 é uma escolha conservadora válida: você ganha os recursos de org do Winter '27 (heap maior, template expressions em LWC ≥ 66.0, `lwc:external`) sem depender de recursos Beta da 68.0. Os recursos exclusivos da 68.0 ficam listados em `gatedFeatures` e só são usados se o projeto subir para 68.0 — com `python .github/scripts/bump-api-version.py 68.0 "Winter '27" --project`.
