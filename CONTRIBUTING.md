# Como contribuir

Obrigado por querer melhorar o plugin. Este repositório é **público**, então algumas regras existem para proteger quem usa.

## Regras que não mudam

1. **Nada de dado real.** Nenhum cliente, pessoa, foto, vídeo, telefone ou e-mail pessoal, nem em commit, issue, comentário ou captura de tela. Use sempre o exemplo fictício (`Casa Exemplo`, `Ana Souza`).
2. **Marca:** não altere nem recolora os logos da VTX Tap e da Vortex. Use apenas os arquivos em `modelo/assets/marca/`.
3. **A página só afirma o que está em [`regras-de-conteudo.md`](plugins/vtx/skills/landing-page/referencia/regras-de-conteudo.md)**: sem preço, sem promessa de resultado, sem depoimento.
4. **O modelo é a fonte.** Mudou algo visual ou de texto fixo? Atualize `referencia/design.md` (ou `regras-de-conteudo.md`) no mesmo commit.

## Fluxo

1. Abra uma **issue** para conversar (use o modelo; leia o aviso de privacidade antes de colar qualquer coisa).
2. Crie um ramo: `tipo/descricao-curta`, por exemplo `feat/campo-de-video` ou `fix/artigo-plural`.
3. Faça a mudança e **teste** (veja abaixo).
4. Abra um **pull request** pelo modelo. Ele traz o checklist; marque o que fez.
5. Alguém do time revisa. **Revisão humana é obrigatória**: a checagem automática não pega tudo.

## Testar antes de enviar

```bash
cd plugins/vtx/skills/landing-page
python scripts/gerar.py exemplo/clientes/casa-exemplo/cliente.json --equipe exemplo/equipe/equipe.json --saida saida-teste
python scripts/verificar.py saida-teste/casa-exemplo
python scripts/checar_publicacao.py
```

Na raiz: `claude plugin validate --strict .` e `claude plugin validate --strict plugins/vtx`. O CI repete isso.

## Commits

Mensagens curtas em português, no formato [Conventional Commits](https://www.conventionalcommits.org/pt-br/):

| Tipo | Quando |
|---|---|
| `feat` | recurso novo (pergunta nova, campo novo, componente novo) |
| `fix` | correção |
| `docs` | só documentação |
| `ci` | automação |
| `chore` | manutenção, versão, limpeza |

Exemplo: `fix(landing-page): concordar o artigo no plural`.

## Mudou o comportamento? Suba a versão

Os usuários só recebem a atualização quando o `version` de [`plugin.json`](plugins/vtx/.claude-plugin/plugin.json) muda. Suba-o (SemVer) e anote no [CHANGELOG](plugins/vtx/CHANGELOG.md). Detalhes em [docs/manutencao.md](docs/manutencao.md).

## Decisões de fundo

Se a mudança altera uma escolha registrada em [docs/decisoes](docs/decisoes), escreva uma decisão nova explicando por quê (não edite as antigas).
