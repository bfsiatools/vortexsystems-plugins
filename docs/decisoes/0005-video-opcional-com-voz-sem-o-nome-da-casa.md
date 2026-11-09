# 0005 · Vídeo opcional por casa, com voz que não fala o nome da casa

- **Estado:** aceita
- **Data:** 2026-11-09

## Contexto

O vídeo dos próximos passos (vertical, ~41 s, 3D, voz e legendas) ajuda o cliente a entender o que vem depois do contrato. A primeira versão tinha a voz dizendo o nome da casa na abertura. Isso impedia reaproveitar o vídeo: cada casa exigiria uma voz nova, com custo por geração e dependência de um serviço de voz que nem todo usuário do plugin tem.

## Decisão

- A skill **sempre pergunta** se a pessoa quer o vídeo. Com **sim**, gera o vídeo da casa; com **não**, gera a página **com a mesma estrutura, só sem o vídeo**, e não renderiza nada.
- A voz é **uma só, para todas as casas**, e a abertura é "Fechou com a VTX Tap." O nome da casa aparece **escrito**, junto da logo.
- Por casa mudam só três coisas: a **logo**, o **print da página da casa** e o **WhatsApp** de quem fechou (o mesmo do cartão da página). O restante do vídeo vem pronto em `modelo-video/`.
- `scripts/gerar_video.py` troca esses três itens, renderiza com o HyperFrames (versão fixa) e preenche `video` e `poster` no `cliente.json`.
- O gerador **recusa** um print fora do padrão (vertical, ~734×1280, com banner, logo e card Cardápio). Quando a pessoa insiste em usar outro print, as marcações de banner, logo e cardápio são descritas em `video_realces`, no `cliente.json`.

## Consequências

- (+) Qualquer pessoa gera o vídeo de uma casa em 2 a 3 minutos, sem gastar crédito de voz e sem conta em serviço de voz.
- (+) A página continua inteira sem o vídeo: quem não quer vídeo não perde nada da estrutura.
- (−) Exige Node.js, ffmpeg e internet na primeira vez (baixa o HyperFrames).
- (−) A voz perde o toque pessoal de ouvir o nome da casa.
- (−) Com print fora do padrão, uma marcação pode ficar pouco visível (por exemplo, o cardápio como uma faixa fina).
- (−) **Em aberto:** o áudio (`modelo-video/assets/voz.m4a`) foi gerado com voz sintética. A licença do serviço de voz para uso comercial e redistribuição não foi conferida. Quem mantém o plugin deve verificar antes de divulgar o repositório.

## Alternativas descartadas

- **Voz nova por casa.** Mais pessoal, mas gasta crédito a cada cliente e não funciona para quem não tem acesso ao serviço de voz.
- **Vídeo obrigatório.** Atrasa a entrega de quem só precisa da página.
- **Aceitar qualquer print.** Gera marcações no lugar errado sem avisar.
