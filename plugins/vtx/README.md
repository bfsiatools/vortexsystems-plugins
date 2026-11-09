# Plugin `vtx`

Ferramentas da VTX Tap para quem vende e implanta. Faz parte do marketplace [`vortexsystems`](../../README.md).

## Skills

| Comando | Para quê |
|---|---|
| `/vtx:landing-page` | Gera a landing page de boas-vindas e próximos passos de um cliente fechado, pronta para enviar. |

## Instalar

```bash
claude plugin marketplace add bfsiatools/vortexsystems-plugins
claude plugin install vtx@vortexsystems
```

Ou, dentro de uma sessão do Claude Code: `/plugin install vtx --marketplace bfsiatools/vortexsystems-plugins`. Mais opções e solução de problemas no [README do repositório](../../README.md#instalar).

## Primeira vez

1. Com o plugin instalado, abra um projeto seu.
2. Digite `/vtx:landing-page`.
3. Responda: a casa, a logo, o(s) dono(s), quem fechou o contrato e **se quer o vídeo dos próximos passos** (com "sim", mande também o print da página da casa no VTX Tap; com "não", a página sai igual, sem vídeo). Na primeira vez a skill cadastra a pessoa (nome, **foto**, **WhatsApp**) em `landing-pages/equipe/`.
4. A skill gera o vídeo (2 a 3 minutos, só se você quis), gera e confere a página. Você recebe o caminho de `landing-pages/saida/<casa>-unico.html`: um arquivo só, que abre com dois cliques e serve para mandar por WhatsApp ou e-mail.

## O que a skill nunca faz

Publicar a página, enviar mensagem ou subir servidor. Entregar é com você.

## Onde ficam os dados

Tudo o que é de cliente ou de pessoa fica em `landing-pages/`, na pasta do **seu** projeto, e nunca dentro do plugin: equipe e fotos (`equipe/`), cada cliente (`clientes/<casa>/`) e as páginas geradas (`saida/`). Não faça commit dessa pasta.

## Requisitos

- Python 3 (`py` no Windows).
- Chrome ou Edge, opcional: fotos de conferência da página.
- Para o vídeo: Node.js (`npx`), ffmpeg e internet na primeira vez.
- Playwright, opcional: `verificar-navegador.cjs` (rolagem, cliques e vídeo).

## Testar o plugin

O plugin traz uma casa e uma vendedora **fictícias** em `skills/landing-page/exemplo/`. Para conferir que tudo funciona:

```bash
cd skills/landing-page
python scripts/gerar.py exemplo/clientes/casa-exemplo/cliente.json --equipe exemplo/equipe/equipe.json --saida saida-teste
python scripts/verificar.py saida-teste/casa-exemplo
```

Resultado esperado: `Bem-vindas, Maria e Joana.` e `RESULTADO: OK`.

## Mais

- Fluxo completo da skill: [`skills/landing-page/SKILL.md`](skills/landing-page/SKILL.md)
- Design (tipografia, cores, componentes, movimento): [`referencia/design.md`](skills/landing-page/referencia/design.md)
- Regras do que a página pode afirmar: [`referencia/regras-de-conteudo.md`](skills/landing-page/referencia/regras-de-conteudo.md)
- Histórico: [CHANGELOG](CHANGELOG.md)



