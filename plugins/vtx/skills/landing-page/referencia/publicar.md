# Tornar a skill pública

"Pública" aqui significa: qualquer pessoa pode baixar e usar a skill (por exemplo, o outro sócio ou outra equipe), sem ver dado de cliente nem de pessoa da empresa. Nada disto é feito automaticamente: publicar é decisão do responsável.

## 1. O que pode e o que não pode ir

| Pode | Não pode |
|---|---|
| `SKILL.md`, `modelo/`, `scripts/`, `referencia/` | Qualquer pasta `landing-pages/` do projeto (equipe, clientes, saída) |
| Fontes com licença OFL (já acompanham as licenças) | Foto de pessoa, vídeo, logo de cliente, número de telefone, e-mail pessoal |
| `exemplo/` com dados fictícios | `equipe.json` ou `cliente.json` reais |
| `contato@vortexsystems.tech` (e-mail institucional) | Tokens, chaves, caminhos de usuário do computador |

Decisão pendente do responsável antes de publicar: **os logos e o endosso VTX/Vortex em `modelo/assets/marca/` são marca registrada ou em registro da empresa**. Publicá-los permite que qualquer um gere páginas com a marca. Se não quiser isso, a skill pode ser publicada sem eles e pedir ao usuário que ponha os SVGs oficiais na pasta.

## 2. Checagem automática

Na raiz do projeto, **antes de qualquer cópia ou publicação**:

```bash
py -I -X utf8 <SKILL>/scripts/checar_publicacao.py
```

Ela barra fotos, vídeos, telefones, e-mails que não sejam o institucional, caminhos de usuário, tokens e qualquer nome da lista `.nomes-privados.txt` (arquivo **fora** da skill, na raiz do projeto, um nome por linha: clientes, pessoas, números). Só publique com `RESULTADO: limpo`.

## 3. Caminhos para publicar (escolha com o responsável)

1. **Pasta compartilhada ou ZIP.** Copiar a pasta da skill para dentro de `.claude/skills/` do projeto de quem vai usar (ou para `~/.claude/skills/`, para valer em todos os projetos). Simples; sem atualização automática.
2. **Repositório público no GitHub.** Criar um repositório só com a pasta da skill (mais um `README` e uma `LICENSE`). Quem quiser usa clonando e copiando a pasta.
3. **Plugin em marketplace.** Empacotar como plugin do Claude Code (um repositório com o manifesto do plugin e `skills/landing-page/`) para que outras pessoas instalem com os comandos de plugin e recebam atualizações. O formato exato do manifesto muda; confira a documentação atual do Claude Code antes.

Em qualquer caso: publicar um repositório é **fora do computador e difícil de desfazer** (cópias e caches). Faça a checagem, releia o diff e só então publique.

## 4. Depois de publicar

- Dados privados continuam só em `landing-pages/` de cada projeto; nunca mande essa pasta junto.
- Mudanças no modelo viram uma nova versão da skill: registre no `README` o que mudou.
- Quem usar precisa de Python 3 (`py` no Windows) e, para as fotos de conferência, de um Chrome ou Edge. O teste de navegador é opcional (Playwright).

