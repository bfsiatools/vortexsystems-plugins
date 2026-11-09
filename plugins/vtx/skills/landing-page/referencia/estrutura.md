# Estrutura da landing page, campos e arquivos

## Mapa da página (de cima para baixo)

| # | Bloco | Classe | O que mostra | Vem de |
|---|---|---|---|---|
| 1 | Abertura | `.hero` | Logo VTX Tap, "casa · cidade" em mono, **"Bem-vindo(a)(s), {nomes}."**, frase com a previsão de chegada, botão "Ver os próximos passos" (âncora `#proximos-passos`), e o **lockup** VTX Tap × logo da casa com ondas de NFC | `saudacao`, `donos`, `casa`, `cidade`, `prazo_dias`, `logo_cliente` |
| 2 | Carta | `.carta` | "{nomes}, meus parabéns." + frase de elogio (opcional) + 3 parágrafos fixos | `donos`, `elogio` |
| 3 | O que chega na mesa | `.secao` + `.tres` | 3 cartões fixos: Encostou, abriu · Com a cara do cliente · Do nosso lado, o trabalho | `artigo`, `casa_curta` |
| 4 | Próximos passos | `.passos` | Linha do tempo de 4 passos com chip de estado | `estado_passos`, `prazo_dias`, `data_inicio` |
| 5 | Como vai ficar | `.secao` + `.duas` | Prévia da tela da casa e/ou vídeo (só aparece se houver) | `tela_previa`, `video`, `poster` |
| 6 | Quem cuida de vocês | `.contatos` | Cartão do vendedor (foto, nome, função, botão com o número) + cartão Time VTX Tap (e-mail) | `vendedor` |
| 7 | Fecho | `.fecho` | "Vamos colocar {o/a} {casa} na mesa." + botão do WhatsApp | `artigo`, `casa_curta` |
| 8 | Rodapé | `footer` | Endosso "uma solução VORTEX", site e Instagram | `site_rodape`, `insta` |

### Os 4 passos (ordem aprovada)

1. **Três coisas suas** (imagens do cardápio, uma imagem para o banner, a logo da casa) + botão "Enviar pelo WhatsApp". Estado padrão: **agora**.
2. **Sua página**: em até 24 horas após recebermos os três materiais, o cliente recebe acesso à página do restaurante. Estado: depois.
3. **{prazo} dias: as plaquinhas chegam**, com "Previsão: {data} · contada a partir de {início}". Estado: depois.
4. **Treinamento com a equipe** + botão "Combinar o dia". Estado: depois.

Estados do chip: `feito` (verde), `agora` (amarelo), `depois` (lilás). Mude `estado_passos` conforme o andamento.

## cliente.json

Arquivo UTF-8 em `landing-pages/clientes/<slug>/cliente.json`. Os arquivos citados ficam na mesma pasta.

| Campo | Obrig. | Exemplo / regra |
|---|---|---|
| `slug` | sim | `casa-exemplo` (minúsculas, sem acento, hifens). Vira a pasta de saída e o futuro subdomínio |
| `casa` | sim | nome completo (rodapé do hero, alt da logo, meta description) |
| `casa_curta` | sim | como o dono fala; entra nas frases |
| `cidade` | sim | |
| `artigo` | não (`o`) | `o`, `a`, `os` ou `as`: concorda "o/a Casa", "do/da Casa", "O/A Casa agora é casa VTX Tap" |
| `donos` | não | `["Maria", "Joana"]` → "Maria e Joana". Vazio usa o nome curto da casa |
| `genero_donos` | não (`m`) | `m` ou `f`; define Bem-vindo/Bem-vinda (e plural) |
| `saudacao` | não | força o texto (ex.: "Bem-vindos") |
| `elogio` | não | 1 frase pessoal no início da carta, sobre a casa. Nada de resultado, número ou preço |
| `logo_cliente` | sim | png, webp, jpg ou svg, ≥ 400 px |
| `vendedor` | sim | id em `equipe.json` (`"ana"`) **ou** objeto `{nome, foto, whatsapp, funcao?, whatsapp_exibicao?}` |
| `data_inicio` | não (hoje) | `AAAA-MM-DD`; de onde conta o prazo |
| `prazo_dias` | não (15) | previsão de chegada das plaquinhas |
| `estado_passos` | não | 4 itens entre `feito`, `agora`, `depois` |
| `tela_previa`, `tela_legenda` | não | print da página da casa; a página **corta o trecho de baixo** (aspect 734:1100) para não mostrar valores |
| `video`, `poster`, `video_legenda` | não | mp4 e imagem de capa; só aparecem se houver |
| `site_rodape`, `insta`, `email_time` | não | dados da empresa (padrões da VTX) |

## equipe.json

Em `landing-pages/equipe/equipe.json` (privado):

```json
{ "pessoas": { "ana": { "nome": "Ana Souza", "funcao": "Comercial. Seu contato direto, do início ao fim.",
  "whatsapp": "11900000000", "whatsapp_exibicao": "(11) 90000-0000", "foto": "fotos/ana.png" } } }
```

- `whatsapp`: DDD + número (o gerador põe o 55). Aceita com máscara. `whatsapp_exibicao` é opcional (o gerador formata).
- `foto`: relativa à pasta do `equipe.json`. Quadrada com o rosto no centro funciona melhor (a página recorta em círculo de 72 px).
- `funcao`: opcional; padrão "Seu contato direto, do início ao fim."

## O que o gerador faz e valida

- Lê com tolerância a BOM; escapa todo texto de cliente.
- Para (erro) se faltar campo, slug inválido, arquivo ausente, WhatsApp fora do padrão, vendedor sem foto/número, extensão de imagem não aceita ou artigo inválido.
- Avisa (não para) se logo/foto/prévia forem pequenas ou pesadas.
- Normaliza o WhatsApp para `55` + DDD + número e monta 3 links `wa.me` com mensagem pronta ("Oi, {primeiro nome do vendedor}! Aqui é {do/da} {casa}...").
- Copia fontes e marca do `modelo/assets`, a logo, a foto (como `vendedor-<arquivo>`) e os extras para `assets/`.
- `--unico` embute tudo em base64 num arquivo só (com vídeo pode passar de 15 MB).

## Arquivos da skill

```
SKILL.md                      fluxo e regras
modelo/index.html             a página (template com {{placeholders}})
modelo/assets/fonts           Big Shoulders Display, Schibsted Grotesk, IBM Plex Mono + licenças OFL
modelo/assets/marca           logo VTX Tap (negativo), ícone, endosso "uma solução VORTEX"
scripts/gerar.py              gera a página
scripts/verificar.py          confere + fotos de conferência (sem servidor)
scripts/verificar-navegador.cjs  teste de navegador (opcional, Playwright)
scripts/checar_publicacao.py  barra dado pessoal antes de publicar a skill
exemplo/                      cliente e vendedor FICTÍCIOS para testar
referencia/                   design, estrutura, regras de conteúdo, publicar
```
