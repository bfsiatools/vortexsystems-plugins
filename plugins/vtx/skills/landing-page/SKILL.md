---
name: landing-page
description: Gera a landing page de boas-vindas e próximos passos de um cliente que acabou de fechar contrato com a VTX Tap, pronta para enviar (um arquivo HTML só). Pergunta a logo da casa, o nome do(s) dono(s), quem fechou o contrato (com a foto e o WhatsApp dessa pessoa) e pergunta se quer o vídeo dos próximos passos (se quiser, gera o vídeo da casa; se não, gera a página igual, sem vídeo) e monta a página com a tipografia, as cores e a estrutura aprovadas. Use quando o usuário digitar /landing-page ou pedir a página do cliente, welcome page, boas-vindas de cliente fechado, próximos passos para mandar ao cliente, ou "fechei com a casa X, gera a página".
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
5. **O vídeo dos próximos passos.** **Sempre pergunte** (`AskUserQuestion`: "Quer o vídeo dos próximos passos na página?", Sim / Não). É vertical, ~41 s, com voz e legendas, e explica os 4 passos.
   - **Sim:** peça o **print da página da casa no VTX Tap** (vertical, ~734×1280; o vídeo marca nele cardápio, banner e logo). Ponha em `tela_previa`. Se o print **não** for o padrão (outro tamanho, ou outra tela, como "Chamar o garçom" em vez do card Cardápio), o gerador recusa. Ou peça um print no formato certo, ou, se o usuário insistir em usar o que mandou, olhe o print com Read e descreva as 3 marcações em `video_realces` do `cliente.json` (campos em `referencia/estrutura.md`; `null` esconde a marcação de algo que não aparece no print) e avise que o cardápio pode ficar pouco visível. A logo precisa ser png, webp ou jpg (SVG não carrega no 3D). O vídeo é gerado por você (veja "Gerar") e entra na página sozinho.
   - **Não:** deixe `video` e `poster` vazios e **não gere nada de vídeo**. A página sai com a mesma estrutura, só sem o vídeo. Se o usuário ainda assim mandou o print, ele aparece sozinho em "Como vai ficar"; se não mandou, essa seção some. Não insista.
6. **Só se o usuário pedir:** data do fechamento (padrão: hoje), prazo das plaquinhas (padrão: 15 dias), prévia da tela da casa (quando não houver vídeo), uma frase de elogio personalizada para a carta.

Se faltar a logo, a foto ou o WhatsApp (ou o print, quando o usuário quis o vídeo), **pare e peça**; não gere com lacuna.

## Gerar

1. Crie `landing-pages/clientes/<slug>/` (slug: minúsculas, sem acento, hifens) e ponha lá a logo (e vídeo/prévia, se houver). Escreva `cliente.json` com a ferramenta Write em UTF-8 (campos em `referencia/estrutura.md`).
2. **Só se o usuário quis o vídeo**, gere-o antes da página (não é opcional "depois": a página só leva o vídeo se ele já existir). Avise que leva de 2 a 3 minutos e que precisa de Node.js, ffmpeg e internet na primeira vez. Rode **em segundo plano** e espere o aviso de término:

```bash
py -I -X utf8 <SKILL>/scripts/gerar_video.py landing-pages/clientes/<slug>/cliente.json
```

   Ele troca no modelo (`modelo-video/`) a logo da casa, o print da página e o WhatsApp de quem fechou (o mesmo número do cartão da página), renderiza com o HyperFrames, cria `proximos-passos.mp4` e `poster.jpg` na pasta do cliente e preenche `video` e `poster` no `cliente.json`. **A voz não fala o nome da casa** (é a mesma para todas); o nome aparece escrito, junto com a logo. Se faltar Node ou ffmpeg, ou o render falhar, diga o que faltou e ofereça gerar a página **sem** vídeo; nunca entregue com vídeo quebrado. Confira o resultado com `ffmpeg -ss 1.5 -i proximos-passos.mp4 -frames:v 1 f.png` em 3 ou 4 instantes (1,5 s, 12 s, 22 s, 38 s) e olhe com a ferramenta Read: a logo da casa certa, o print, o número certo no fecho. Não mexa na voz: gerar outra custa crédito e muda o produto aprovado.

3. Na raiz do projeto, a página:

```bash
py -I -X utf8 <SKILL>/scripts/gerar.py landing-pages/clientes/<slug>/cliente.json --unico
py -I -X utf8 <SKILL>/scripts/verificar.py landing-pages/saida/<slug>
```

4. Leia a saída do gerador (avisos de imagem pequena, por exemplo) e a do verificador. **Erros param a entrega.** Avisos precisam ser lidos.
5. Olhe as fotos de conferência (`landing-pages/saida/verificacao/<slug>/desktop-1440.png` e `celular-390.png`) com a ferramenta Read: o título com os nomes certos, a logo no círculo, a foto e o número do vendedor no cartão "Quem cuida de vocês", o artigo certo ("Vamos colocar **a** Casa Exemplo na mesa").
6. Se o usuário tiver Playwright, `node scripts/verificar-navegador.cjs <index.html>` confere rolagem horizontal, cliques e vídeo.

## Entregar

- Diga o caminho de `landing-pages/saida/<slug>-unico.html` (um arquivo só, abre com dois cliques e serve para mandar por WhatsApp ou e-mail) e, no app, envie o arquivo com `SendUserFile`.
- Resuma em 5 linhas o que foi usado: casa, saudação, vendedor (nome e número como aparecem), previsão das plaquinhas e **se tem vídeo** (com o caminho do mp4) ou não.
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


