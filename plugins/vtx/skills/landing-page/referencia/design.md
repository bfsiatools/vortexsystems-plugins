# Design da landing page (como está em `modelo/index.html`)

Lido do CSS aprovado. Se mudar o modelo, atualize este arquivo no mesmo passo.

## Ideia visual

Uma página escura na abertura (a "noite" da marca VTX, com brilho roxo no canto) que vira fundo claro e neutro (névoa) no resto. Cartões planos (borda fina, sem sombra), botões em pílula, um único acento quente (**ouro**) por trecho, e um único momento animado: **as ondas de NFC** saindo do lockup VTX Tap × logo da casa. Nada de ícones decorativos, kicker acima de título ou sombra em tudo.

## Tipografia (três vozes, uma por função)

| Voz | Família | Uso | Tamanhos |
|---|---|---|---|
| Display | **Big Shoulders Display** 900, caixa alta, `line-height .95`, tracking `.005em` | h2 e h3 (títulos de seção, cartões, passos), número dos passos | carta h2 `clamp(40px, 7vw, 72px)` · seção h2 `clamp(36px, 6vw, 60px)` · "Próximos passos" `clamp(44px, 8vw, 88px)` · passo h3 `clamp(28px, 4.4vw, 40px)` · cartão h3 `30px` · fecho h2 `clamp(40px, 7.2vw, 84px)`, `max-width: 12em` · número do passo `26px` |
| Corpo | **Schibsted Grotesk** 400–900 | tudo que se lê: corpo, botões, chips, **o h1** | corpo `18px/1.55` (`17px` até 820 px) · sub da abertura `21px` · parágrafos de cartão `17px` · botões `700 18px` (`16px` nos do contato) · chips `700 13px`, caixa alta, tracking `.06em` |
| Mono | **IBM Plex Mono** 500 | metadado curto, nunca frase | "casa · cidade" `14px` caixa alta tracking `.08em` · legenda do lockup `13px` tracking `.1em` · previsão do prazo `15px` |

**O h1** ("Bem-vindo, {nomes}.") é exceção ao display: Schibsted Grotesk **700**, `clamp(34px, 4.6vw, 60px)`, `line-height 1.1`, tracking `-.035em`, **sem caixa alta**, em duas linhas (a segunda, os nomes, em ouro, `overflow-wrap: anywhere`). O "Seja bem-vindo" gigante em Big Shoulders foi **rejeitado** pelo responsável pela marca; não voltar a ele.

Fontes são arquivos TTF em `assets/fonts/` (`font-display: swap`); nunca depender de fonte instalada. Licença OFL junto.

## Cores (tokens em `:root`)

| Token | Hex | Papel |
|---|---|---|
| `--noite` | `#140b33` | fundo da abertura e do fecho |
| `--noite-ink` | `#f1ecff` | texto sobre noite |
| `--noite-2` | `#cfc6f2` | texto de apoio sobre noite |
| `--roxo` | `#7d27fc` | marca: ponto das etiquetas, número das listas |
| `--lilas` | `#a874ff` | ondas de NFC, linha do tempo, foco |
| `--ouro` | `#ffc61a` | **único acento quente**: nomes no h1, botões principais, passo "agora" |
| `--on-ouro` | `#1d1400` | texto sobre ouro |
| `--nevoa` | `#f4f2f9` | fundo claro da página |
| `--ink` / `--ink-2` / `--muted` | `#160e33` / `#2f2752` / `#5b5378` | texto principal, forte, de apoio |
| `--line` | `#e1dcee` | bordas |
| `--ok` / `--ok-soft` | `#1b7f52` / `#daf0e4` | passo "feito" |
| `--roxo-ink` / `--roxo-soft` | `#6a1be0` / `#eee5ff` | texto e fundo do chip "depois", previsão |

Regras: ouro nunca em texto pequeno sobre fundo claro; roxo `#7d27fc` nunca como cor de texto sobre noite; sem laranja, azul ou outra cor de marca da casa (a logo do cliente já traz a dela).

## Espaço e forma

- Coluna: `.wrap { width: min(1080px, 100% - 48px) }` (24 px de respiro em cada lado no celular).
- Seções: `56px` de padding vertical; carta `84px 56px`; próximos passos `88px` (`64px` no celular).
- Abertura: grade `1.15fr / .85fr`, `gap 40px`; vira uma coluna abaixo de **820 px**.
- Cartões: fundo branco, borda `1px var(--line)`, raio **22 px**, padding `28px`, **sem sombra**. Fecho: raio 28. Botões e chips: raio 999 (pílula).
- Botão: `padding 16px 30px`, `gap 10px`. Variantes: `.btn-ouro` (principal), `.btn-claro` (branco com borda; borda vira roxa no hover).

## Componentes

- **Lockup:** dois discos de `clamp(110px, 17vw, 168px)`: VTX Tap (fundo `#1a1042`, borda `#4a3a96`, logo a 64 %) e a casa (fundo **branco**, logo a 80 % e círculo), separados por um "×" ouro. Legenda mono embaixo.
- **Ondas de NFC:** 3 círculos de 150 px, borda `2px` lilás, `animation: onda 4.8s` com atrasos de 1,2 s, escala `.7 → 3.3`, opacidade até `.55`. É **o** momento animado; não adicionar outro.
- **Linha do tempo:** lista ordenada com trilho vertical (gradiente lilás → linha) que se desenha em 1,4 s; nó circular de 44 px (branco; verde em "feito"; ouro em "agora"); chip de estado ao lado do título; lista "três coisas" em cartinhas com número roxo; previsão em mono roxo.
- **Prévia de tela:** moldura `noite` com raio 28 e padding 12; a tela é recortada em `aspect-ratio 734/1100` com `object-fit: cover; object-position: top` — **de propósito**, para cortar o trecho de baixo (valores em reais). Largura máxima 360 px.
- **Vídeo:** 9:16, raio 22, máx. 340 px, `controls`, `playsinline`, `preload="metadata"`, pôster.
- **Contato:** cartões brancos com foto de 72 px em círculo (`object-fit: cover`), nome em negrito 20 px, função, botão com o número (quebra em qualquer ponto se o e-mail for longo).
- **Fecho:** cartão `noite` com título display e botão ouro; círculo decorativo ouro (`pointer-events: none`, para não bloquear o clique).
- **Rodapé:** endosso "uma solução VORTEX" (SVG para fundo claro) + linha de texto.

## Movimento

- Curva única: `cubic-bezier(0.22, 1, 0.36, 1)`. Sem bounce, glow ou neon.
- Entrada de blocos (`.reveal`): sobe 26 px e aparece em 0,8 s, ao entrar na tela (IntersectionObserver). Só liga **depois** que o JavaScript acrescenta a classe `js` ao `<html>`: sem JavaScript, ou sem IntersectionObserver, ou com `prefers-reduced-motion`, o conteúdo aparece direto.
- Hover de botão: sobe 2 px em 0,25 s.
- `prefers-reduced-motion: reduce`: sem rolagem suave, ondas paradas, sem transições.

## Acessibilidade

- Foco visível: contorno de 3 px lilás com offset 3 px.
- Todo `<img>` com `alt` (decorativos com `alt=""`); lockup com `role="img"` e `aria-label`; ondas e setas `aria-hidden`.
- Links externos `target="_blank" rel="noopener"`; âncora `#proximos-passos` com `scroll-margin-top`.
- Contraste: texto sobre noite ≥ 8:1 (medido), corpo sobre branco/névoa ≥ 6:1; chips e botões ≥ 4,5:1.
- Conteúdo inteiro legível sem JavaScript.

## Metadados e privacidade

`noindex, nofollow`; `color-scheme: dark light`; título "{Saudação}, {casa curta} · VTX Tap". O endereço é público por quem tem o link: nada de preço, contrato, CPF, e-mail pessoal ou dado de funcionário.

## O que NÃO fazer

- Trocar fonte, cor, raio, espaçamento ou o h1 por cliente.
- Recolorir, esticar ou redesenhar a logo do cliente ou a da VTX (só os SVGs oficiais de `modelo/assets/marca`).
- Acrescentar sombra, gradiente extra, ícone decorativo, emoji, rótulo pequeno acima de título, segundo acento de cor ou segunda animação.
- Mostrar valor em reais, percentual de resultado, "garantia" ou depoimento.
- Hospedar fonte ou script em CDN: a página tem de abrir offline, de um arquivo só.

