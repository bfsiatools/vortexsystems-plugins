# 0004 · Só afirmar o que está confirmado e perguntar em vez de supor

- **Estado:** aceita
- **Data:** 2026-11-09

## Contexto

A página vai ao cliente **em nome da empresa**, logo depois da venda. Uma promessa errada (preço, resultado, prazo, função) vira problema comercial. Português mal concordado ("o Casa Exemplo", "Bem-vindo, Maria e Joana") faz a página parecer amadora e é um erro que se repete em metade dos clientes se o modelo supõe um gênero e um número.

## Decisão

- O que a página pode dizer está em [`referencia/regras-de-conteudo.md`](../../plugins/vtx/skills/landing-page/referencia/regras-de-conteudo.md): **sem preço, sem promessa de resultado, sem depoimento**, datas como **previsão**, e nada sobre a página do restaurante já estar entregue.
- A skill **pergunta** o que não dá para adivinhar e **não gera com lacuna**: logo, foto e WhatsApp de quem fechou são obrigatórios; o artigo da casa (o/a/os/as) e o gênero dos donos viram campos.
- A skill **mostra "nome · número"** do vendedor antes de gerar e pede confirmação.
- `verificar.py` **avisa** quando o texto tiver valor em reais, percentual, garantia ou promessa de resultado, e **falha** em erro estrutural (placeholder sobrando, asset ausente, número de WhatsApp inválido ou diferente entre os botões, falta de `noindex`).
- Mudar o que a página afirma é decisão do responsável pela marca: muda-se o modelo e o documento de regras **juntos**.

## Consequências

- (+) Menos retrabalho e menos risco de promessa indevida.
- (+) Concordância certa para qualquer casa e qualquer dupla de donos.
- (−) Mais perguntas no começo (cinco, curtas).
- (−) As regras envelhecem: cada mudança de produto exige atualizar o documento (parte do checklist do pull request).

## Alternativas descartadas

- **Texto livre por vendedor.** Flexível, mas cada página viraria uma promessa diferente.
- **Gerar com padrões quando faltar dado** (foto genérica, número da empresa). Esconde o erro em vez de pedir o dado.
- **Supor gênero e artigo pelo nome.** Erra com frequência; perguntar custa três segundos.
