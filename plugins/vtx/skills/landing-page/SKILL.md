---
name: landing-page
description: Gera a landing page de boas-vindas e próximos passos de um cliente que acabou de fechar contrato com a VTX Tap, pronta para enviar (um arquivo HTML só). Pergunta a logo da casa, o nome do(s) dono(s), quem fechou o contrato (com a foto e o WhatsApp dessa pessoa) e monta a página com a tipografia, as cores e a estrutura aprovadas. Use quando o usuário digitar /landing-page ou pedir a página do cliente, welcome page, boas-vindas de cliente fechado, próximos passos para mandar ao cliente, ou "fechei com a casa X, gera a página".
---

# Landing page do cliente fechado

Gera, a partir de um modelo fixo e aprovado, a página que o vendedor manda ao cliente logo depois de fechar. A página é **a mesma para todos**; só mudam: a casa, o(s) dono(s), a logo e a pessoa que fechou (foto, nome e WhatsApp). O visual nunca é reinventado por cliente.

**Caminhos:** `<SKILL>` é a pasta onde está este `SKILL.md` (o "Base directory for this skill" que aparece quando a skill carrega). Ela muda conforme a instalação (projeto, global ou plugin); use sempre esse diretório, nunca um caminho fixo. Os dados do projeto ficam sempre em `landing-pages/`, na pasta onde o usuário está trabalhando.

Antes de qualquer coisa leia `referencia/estrutura.md` (campos e arquivos). Para mexer em visual, texto fixo ou fluxo, leia também `referencia/design.md` e `referencia/regras-de-conteudo.md`.

## Onde ficam as coisas

| O quê | Onde | Público? |
|---|---|---|
| Modelo, gerador, verificadores, fontes, marca | esta pasta (`modelo/`, `scripts/`) | sim, sem dado pessoal |
| Quem fecha contratos (nome, foto, WhatsApp) | `landing-pages/equipe/equipe.json` e `landing-pages/equipe/fotos/` **no projeto** | **não** |
| Cada cliente (logo, vídeo, `cliente.json`) | `landing-pages/clientes/<slug>/` no projeto | **não** |
| Páginas geradas | `landing-pages/saida/<slug>/` e `<slug>-unico.html` | **não** |

Nunca grave pessoa, número, foto ou cliente dentro desta pasta. Ela precisa poder ser publicada.

## Roteiro de perguntas

Pergunte em poucas mensagens, sem despejar tudo de uma vez. Use `AskUserQuestion` para escolhas fechadas (quem fechou, artigo da casa); para arquivos, peça que o usuário arraste a imagem na conversa ou cole o caminho. Se o usuário já disse algo (ex.: "fechei a Padaria do Zé em Lavras"), não pergunte de novo.

1. **A casa:** nome completo, nome curto (como o dono fala, ex.: "Casa Exemplo"), cidade e o artigo (**o / a / os / as**). Sugira pelo nome (Casa, Pizzaria, Padaria, Cantina, Adega, Choperia → "a"; Bar, Restaurante, Empório → "o") e confirme.
2. **A logo da casa:** arquivo png, webp, jpg ou svg. Confira: pelo menos ~400 px; fundo branco ou transparente; **logo branca sobre transparente some** no círculo branco da página, então peça a versão escura. Nunca recolorir nem esticar.
3. **O(s) dono(s):** o nome como o vendedor chama cada um (só o primeiro nome, ou nome e sobrenome se for assim que tratam). Pergunte o gênero para a saudação: um homem "Bem-vindo", uma mulher "Bem-vinda", vários "Bem-vindos" (só mulheres: "Bem-vindas").
4. **Quem fechou o contrato.** Leia `landing-pages/equipe/equipe.json`. Ofereça as pessoas cadastradas e "outra pessoa". Se for nova, peça **nome, foto, WhatsApp com DDD** e, se quiser, uma linha de função; cadastre em `equipe.json` (foto em `equipe/fotos/`). Depois **mostre o que vai aparecer** ("Ana Souza · (DDD) número") e peça confirmação. Nunca invente foto ou número e nunca use os de outra pessoa.
5. **Só se o usuário pedir:** data do fechamento (padrão: hoje), prazo das plaquinhas (padrão: 15 dias), vídeo + pôster, prévia da tela da casa, uma frase de elogio personalizada para a carta.

Se faltar a logo, a foto ou o WhatsApp, **pare e peça**; não gere com lacuna.

## Gerar

1. Crie `landing-pages/clientes/<slug>/` (slug: minúsculas, sem acento, hifens) e ponha lá a logo (e vídeo/prévia, se houver). Escreva `cliente.json` com a ferramenta Write em UTF-8 (campos em `referencia/estrutura.md`).
2. Na raiz do projeto:

```bash
py -I -X utf8 <SKILL>/scripts/gerar.py landing-pages/clientes/<slug>/cliente.json --unico
py -I -X utf8 <SKILL>/scripts/verificar.py landing-pages/saida/<slug>
```

3. Leia a saída do gerador (avisos de imagem pequena, por exemplo) e a do verificador. **Erros param a entrega.** Avisos precisam ser lidos.
4. Olhe as fotos de conferência (`landing-pages/saida/verificacao/<slug>/desktop-1440.png` e `celular-390.png`) com a ferramenta Read: o título com os nomes certos, a logo no círculo, a foto e o número do vendedor no cartão "Quem cuida de vocês", o artigo certo ("Vamos colocar **a** Casa Exemplo na mesa").
5. Se o usuário tiver Playwright, `node scripts/verificar-navegador.cjs <index.html>` confere rolagem horizontal, cliques e vídeo.

## Entregar

- Diga o caminho de `landing-pages/saida/<slug>-unico.html` (um arquivo só, abre com dois cliques e serve para mandar por WhatsApp ou e-mail) e, no app, envie o arquivo com `SendUserFile`.
- Resuma em 4 linhas o que foi usado: casa, saudação, vendedor (nome e número como aparecem), previsão das plaquinhas.
- **Não publique, não envie mensagem e não suba servidor.** Publicar é decisão do usuário (ver `referencia/publicar.md`).

## Regras que não mudam

- Só se afirma o que está em `referencia/regras-de-conteudo.md`: **sem preço, sem promessa de resultado, sem depoimento**. Datas são previsões.
- Marca: logos da VTX só os SVGs de `modelo/assets/marca/`. A logo do cliente nunca é recolorida.
- Tipografia, cores, espaçamento e movimento ficam como estão em `modelo/index.html`. Para mudar o **modelo** (texto fixo, ordem dos passos, visual), é uma mudança do produto, não de um cliente: confirme com o usuário, edite `modelo/index.html`, rode os dois testes do exemplo (abaixo) e registre a mudança.
- A página é pública por endereço: `noindex` e nada sensível nela.

## Testar depois de mexer no modelo ou no gerador

```bash
py -I -X utf8 <SKILL>/scripts/gerar.py <SKILL>/exemplo/clientes/casa-exemplo/cliente.json --equipe <SKILL>/exemplo/equipe/equipe.json --saida <pasta-temporaria>
py -I -X utf8 <SKILL>/scripts/verificar.py <pasta-temporaria>/casa-exemplo
```

O exemplo usa dono no plural feminino, artigo "a" e outro vendedor: pega os erros de concordância e de cartão do vendedor.

## Manutenção

O usuário às vezes edita a landing por fora (texto, ordem dos passos, vídeo, e-mail). Antes de gerar, leia o `modelo/index.html` atual: ele manda. Se houver cópia do modelo em outro lugar do projeto, não deixe as duas divergirem; avise.

Para tornar esta skill pública: `referencia/publicar.md` e `scripts/checar_publicacao.py`.


