# 0003 · Página estática, de um arquivo só, sem servidor

- **Estado:** aceita
- **Data:** 2026-11-09

## Contexto

O vendedor precisa **mandar a página minutos depois de fechar**, normalmente por WhatsApp. O cliente abre no celular, às vezes com internet fraca. A hospedagem dos clientes não é nossa, e a equipe não quer depender de servidor, painel ou conta para entregar uma página de boas-vindas.

## Decisão

- A página é **HTML + CSS + um JavaScript pequeno**, sem framework, sem CDN e sem build. Fontes e marca ficam em arquivos locais.
- `gerar.py --unico` embute tudo em base64 e produz **um arquivo `.html` único** (logo, foto, fontes, prévia e vídeo incluídos), que abre com dois cliques e se manda como anexo.
- A mesma página sai também em **pasta** (`index.html` + `assets/`), para quem for subir num site.
- A página **funciona sem JavaScript** e com "movimento reduzido": o conteúdo aparece direto, e só a animação de entrada some. Há **um** momento animado (as ondas de NFC); não se acrescenta outro.
- A página nasce com `noindex` e sem dado sensível, porque quem tem o link a abre.

## Consequências

- (+) Abre offline, em qualquer celular, sem conta, sem servidor e sem risco de o serviço sair do ar.
- (+) Nada para instalar ou atualizar do lado do cliente.
- (−) Com vídeo, o arquivo único passa de ~15 MB (um vídeo menor resolve).
- (−) Sem framework, mudar o visual significa editar o HTML do modelo com cuidado (por isso a [referência de design](../../plugins/vtx/skills/landing-page/referencia/design.md) é parte do repositório).
- (−) Se quem hospedar tiver uma política de segurança que bloqueie scripts embutidos, a animação de entrada não roda (o conteúdo continua visível).

## Alternativas descartadas

- **Site com framework (React, Next) hospedado.** Exige build, hospedagem e manutenção para uma página que muda por cliente em 5 campos.
- **Documento no Notion ou Google Docs.** Não carrega a identidade visual nem a animação, e depende da conta de quem compartilha.
- **PDF.** Não tem botão de WhatsApp com mensagem pronta nem vídeo.
