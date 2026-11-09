# 0002 · Marketplace com plugins em subpasta e nomes permanentes

- **Estado:** aceita
- **Data:** 2026-11-09

## Contexto

Queremos publicar a skill `landing-page` agora e outras ferramentas depois. No Claude Code, o **nome do plugin e o do marketplace são identificadores**: quem instala guarda `plugin@marketplace`, e renomear depois quebra a instalação de todo mundo. Os comandos de um plugin ganham o nome do plugin na frente (`/<plugin>:<skill>`). Quem recebe uma atualização só a recebe quando a `version` do plugin muda.

## Decisão

- Um marketplace chamado **`vortexsystems`** (`.claude-plugin/marketplace.json` na raiz) e um plugin chamado **`vtx`** em `plugins/vtx/` (com o próprio `.claude-plugin/plugin.json`, README e CHANGELOG). O comando fica `/vtx:landing-page`.
- Plugins novos entram como **novas pastas em `plugins/`**; skills novas do mesmo assunto entram em `plugins/vtx/skills/`.
- Nomes em **kebab-case** e **permanentes**. Se um dia for inevitável mudar, usa-se o mapa `renames` do marketplace; para mudar só o rótulo, `displayName`.
- **Versão explícita** em `plugin.json` (SemVer), subida a cada lançamento e anotada no CHANGELOG. A versão não é repetida no `marketplace.json`.
- Nome do marketplace escolhido para ter pouca chance de colidir com o de outra pessoa (um usuário não pode ter dois marketplaces com o mesmo nome).

## Consequências

- (+) O repositório cresce sem reorganizar; cada plugin tem versão e histórico próprios.
- (+) `claude plugin update vtx@vortexsystems` é previsível; quem não atualizar fica numa versão conhecida.
- (−) O comando é um pouco mais longo (`/vtx:landing-page`). Quem quiser o curto (`/landing-page`) copia a pasta da skill para `.claude/skills/`.
- (−) Esquecer de subir o `version` faz a atualização não chegar. O guia de [manutenção](../manutencao.md) e o checklist do pull request lembram disso.

## Alternativas descartadas

- **Plugin na raiz do repositório.** Funciona, mas impede abrigar um segundo plugin sem reorganizar.
- **Só copiar a pasta da skill.** Simples, mas sem atualização e sem padrão de instalação para quem está de fora.
- **Chamar o plugin de `landing-page`.** O comando viraria `/landing-page:landing-page`, repetido e confuso.
- **Sem `version` (acompanhar o commit).** Cada commit viraria "versão nova" para todos, inclusive correções pela metade.
