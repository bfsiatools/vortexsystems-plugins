# Segurança e privacidade

## O que conta como problema

- **Dado de cliente ou de pessoa** no repositório: nome, foto, telefone, e-mail pessoal, logo de cliente, vídeo.
- Chave, token ou caminho de usuário do computador.
- Qualquer coisa nos scripts ou nas páginas geradas que possa executar código ou enviar dado para fora sem o usuário saber.

## Como avisar

**Não abra uma issue pública** (ela ficaria visível e indexada). Use um destes:

1. Aba **Security** do repositório > **Report a vulnerability** (aviso privado), se estiver habilitada.
2. E-mail: **contato@vortexsystems.tech**, com o assunto "Segurança: vortexsystems-plugins". Descreva **onde** está o problema (arquivo e commit); **não cole o dado** no e-mail.

## O que fazemos

- Confirmamos o recebimento e removemos o dado.
- **Remover do último commit não basta**: o dado continua no histórico. Reescrevemos o histórico e pedimos que o GitHub limpe caches e forks quando aplicável.
- Se o dado era de uma pessoa, avisamos a pessoa.

## Versões com suporte

Só a versão mais recente do plugin recebe correções. Atualize com `claude plugin update vtx@vortexsystems`.

## O que este repositório faz e não faz

O plugin **não envia mensagens, não publica páginas e não sobe servidor**. Ele gera arquivos no computador de quem usa. A decisão de publicar ou enviar é sempre da pessoa.
