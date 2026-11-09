# Guia de uso: `/vtx:landing-page`

Para quem vende. Em uns 5 minutos você sai com a página do cliente pronta para mandar.

## Antes de começar

Tenha à mão:

| Item | O que é | Dica |
|---|---|---|
| Logo da casa | arquivo png, webp, jpg ou svg, de pelo menos ~400 px | Fundo branco ou transparente. Logo **branca** sobre transparente some no círculo branco da página: peça a versão escura. |
| Nome do(s) dono(s) | como você os chama | Só o primeiro nome costuma ficar melhor. |
| Quem fechou o contrato | você ou outra pessoa do time | A pessoa precisa de **foto** e **WhatsApp**. |

## O fluxo

1. **Digite `/vtx:landing-page`.** A skill lê o cadastro da equipe (`landing-pages/equipe/equipe.json`, no seu projeto).
2. **A casa:** nome completo, nome curto (como o dono fala), cidade e o artigo: **o / a / os / as**. É o artigo que faz a página dizer "Vamos colocar *a* Casa Exemplo na mesa".
3. **A logo.** Arraste a imagem na conversa ou cole o caminho. A skill avisa se estiver pequena ou se for clara demais.
4. **O(s) dono(s) e o gênero**, para a saudação certa: *Bem-vindo*, *Bem-vinda*, *Bem-vindos* ou *Bem-vindas*.
5. **Quem fechou o contrato.** Escolha na lista ou "outra pessoa". Se for nova, a skill pede nome, **foto** e **WhatsApp com DDD** e cadastra. Depois mostra "nome · número" e pede confirmação: é exatamente o que o cliente verá.
6. **Opcionais** (só se você pedir): data do fechamento (padrão: hoje), prazo das plaquinhas (padrão: 15 dias), vídeo, prévia da tela da casa e uma frase de elogio para a carta.

A skill **não gera com lacuna**: se faltar logo, foto ou número, ela para e pede.

## O que ela entrega

- `landing-pages/saida/<casa>-unico.html`: **um arquivo só**, com fontes, logos, fotos e vídeo embutidos. Abre com dois cliques; manda por WhatsApp ou e-mail.
- `landing-pages/saida/<casa>/`: a mesma página em pasta (para subir em um site).
- Fotos de conferência (desktop e celular) em `landing-pages/saida/verificacao/<casa>/`.
- Um resumo: título da abertura, vendedor (nome e número como aparecem) e a previsão de chegada das plaquinhas.

## O que a página tem

Abertura com a saudação e o lockup VTX Tap × logo da casa → carta → "O que chega na sua mesa" → **4 passos** (três coisas do cliente; página do restaurante em até 24 horas depois; plaquinhas em 15 dias; treinamento) → prévia e vídeo → **Quem cuida de vocês** (foto, nome e WhatsApp de quem fechou) → fecho com botão de WhatsApp.

## Boas práticas

- Abra o `-unico.html` no celular antes de mandar.
- A página é **pública para quem tem o link**. Ela já vem com `noindex` e sem dado sensível; não acrescente preço, valor de contrato nem dado pessoal.
- Datas são **previsões**. Se algo mudar, avise o cliente pelo WhatsApp.

## Problemas comuns

| Sintoma | Causa provável | O que fazer |
|---|---|---|
| "WhatsApp invalido" | número sem DDD ou com letras | Digite DDD + número (ex.: `11 90000-0000`). |
| Aviso de imagem pequena | logo ou foto abaixo do mínimo | Peça uma versão maior ao cliente. |
| Sem fotos de conferência | Chrome/Edge não encontrado | Use `--chrome CAMINHO` no `verificar.py` ou ignore (as checagens continuam). |
| Acento virou `?` no JSON | arquivo salvo em ASCII | Salve o `cliente.json` em UTF-8. |
| `/vtx:landing-page` não aparece | plugin não carregou | `claude plugin list`; reinicie a sessão ou use `/reload-plugins`. |
