# vortexsystems-plugins

Marketplace de plugins da **Vortex Systems** para o [Claude Code](https://code.claude.com). Hoje reúne um plugin, o **`vtx`**, para quem vende e implanta a **VTX Tap**.

> Versão atual: **0.1.0** · [Histórico de mudanças](plugins/vtx/CHANGELOG.md)

## O que tem

| Plugin | Comando | O que faz |
|---|---|---|
| [`vtx`](plugins/vtx) | `/vtx:landing-page` | Gera a **landing page de boas-vindas e próximos passos** de um cliente que acabou de fechar contrato. Pergunta a logo da casa, o(s) dono(s), quem fechou o contrato (com foto e WhatsApp dessa pessoa) e entrega um HTML pronto para enviar, em um arquivo só. |

## Instalar

Você precisa do Claude Code, de `git` e de Python 3 (no Windows, o comando `py`).

```bash
claude plugin marketplace add bfsiatools/vortexsystems-plugins
claude plugin install vtx@vortexsystems
```

Ou, de uma vez só: `claude plugin install vtx --marketplace bfsiatools/vortexsystems-plugins`.

Dentro de uma sessão do Claude Code também funciona: `/plugin marketplace add bfsiatools/vortexsystems-plugins` e depois `/plugin` (aba **Discover**) para instalar `vtx`.

**Atualizar:** `claude plugin update vtx@vortexsystems`. A atualização automática vem desligada; quem quiser liga em `/plugin` > **Marketplaces** > **Enable auto-update**.

**Sem plugin:** copie `plugins/vtx/skills/landing-page/` para `.claude/skills/` do seu projeto (ou para `~/.claude/skills/`, para valer em todos). Aí o comando é `/landing-page`.

<details>
<summary>Deu erro ao instalar?</summary>

- Se você não tem chave SSH do GitHub, rode `set CLAUDE_CODE_PLUGIN_PREFER_HTTPS=1` (Windows) ou `export CLAUDE_CODE_PLUGIN_PREFER_HTTPS=1` e tente de novo.
- Confira `git --version` e `py --version` (ou `python3 --version`).
- `claude plugin list` mostra se o `vtx` está habilitado.
</details>

## Usar

Em qualquer projeto, digite `/vtx:landing-page`. A skill pergunta, nesta ordem:

1. a casa (nome, nome curto, cidade, o/a);
2. a **logo** da casa;
3. o(s) **dono(s)**;
4. **quem fechou o contrato** (usa o cadastro da equipe; se for alguém novo, pede nome, **foto** e **WhatsApp**).

Depois gera a página, confere, tira fotos de conferência (desktop e celular) e entrega um `.html` único. Passo a passo em [docs/guia-de-uso.md](docs/guia-de-uso.md).

**Seus dados ficam no seu projeto**, em `landing-pages/`. Nada de cliente ou de pessoa vai para este repositório (ver [por quê](docs/decisoes/0001-modelo-publico-dados-privados-fora.md)).

## Estrutura do repositório

```
.
├── .claude-plugin/marketplace.json     catálogo (nome: vortexsystems)
├── plugins/
│   └── vtx/                            o plugin
│       ├── .claude-plugin/plugin.json  nome, versão, autoria
│       ├── README.md  CHANGELOG.md
│       └── skills/landing-page/
│           ├── SKILL.md                fluxo da skill
│           ├── modelo/                 a página (HTML), fontes e marca
│           ├── scripts/                gerar, verificar, checar_publicacao
│           ├── referencia/             design, estrutura, regras de conteúdo, publicar
│           └── exemplo/                cliente e vendedor FICTÍCIOS para testar
├── docs/
│   ├── guia-de-uso.md                  como usar, passo a passo
│   ├── manutencao.md                   como alterar, versionar e lançar
│   └── decisoes/                       por que as coisas são assim (ADRs)
├── .github/                            CI, modelos de issue e de pull request
├── CONTRIBUTING.md  SECURITY.md
└── README.md
```

## Por que é assim

As escolhas que valem como padrão para quem mexer aqui estão registradas em [docs/decisoes](docs/decisoes):

- [0001](docs/decisoes/0001-modelo-publico-dados-privados-fora.md) · Modelo público, dados privados fora do plugin
- [0002](docs/decisoes/0002-marketplace-com-plugins-em-subpasta.md) · Marketplace com plugins em subpasta e nomes permanentes
- [0003](docs/decisoes/0003-pagina-estatica-de-um-arquivo-so.md) · Página estática, de um arquivo só, sem servidor
- [0004](docs/decisoes/0004-so-afirmar-o-que-esta-confirmado.md) · Só afirmar o que está confirmado e perguntar em vez de supor

## Contribuir e segurança

- Quer mudar algo? Leia o [CONTRIBUTING](CONTRIBUTING.md): cada mudança passa pela checagem de privacidade e pelo exemplo fictício.
- Achou dado de cliente ou de pessoa no repositório? **Não abra issue pública.** Veja o [SECURITY](SECURITY.md).

## Marca, fontes e licença

- Fontes (Big Shoulders Display, Schibsted Grotesk, IBM Plex Mono): licença OFL, que acompanha os arquivos.
- Os logos **VTX Tap**, **Vortex** e "uma solução VORTEX" são marcas da empresa; use-os apenas em páginas de clientes da VTX Tap.
- **Licença do código: ainda não definida.** Enquanto não houver um arquivo `LICENSE`, valem os direitos reservados do autor: dá para instalar e usar o plugin, mas não para copiar e redistribuir o código.
