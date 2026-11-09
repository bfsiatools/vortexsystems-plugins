# 0001 · Modelo público, dados privados fora do plugin

- **Estado:** aceita
- **Data:** 2026-11-09

## Contexto

A skill `landing-page` gera páginas com a logo de um cliente, o nome do dono e a **foto, o nome e o WhatsApp de uma pessoa real do time**. O repositório é público para que qualquer pessoa instale. Dado de cliente ou de pessoa que entra num repositório público fica no histórico do git, em forks e em caches: remover depois é trabalhoso e nunca é completo.

## Decisão

- **Dentro do plugin** só entra o que qualquer pessoa pode ver: modelo, scripts, fontes, marca e um **exemplo fictício** (casa e vendedora inventadas).
- **Fora do plugin**, na pasta `landing-pages/` do **projeto de quem usa**, ficam: o cadastro da equipe (`equipe/equipe.json` e `fotos/`), cada cliente (`clientes/<casa>/`) e as páginas geradas (`saida/`). Os scripts leem e gravam ali (`--equipe`, `--saida`) e nunca dentro do plugin.
- **Trava automática:** `checar_publicacao.py` barra foto, vídeo, pacote, telefone, e-mail que não seja o institucional, caminho de usuário do computador, token e **qualquer nome da lista privada** `.nomes-privados.txt` (que fica fora do repositório, para a lista não virar vazamento). O CI roda essa checagem em todo push e pull request.
- `.gitignore` ignora `landing-pages/`, `saida/`, `.nomes-privados.txt` e vídeos.

## Consequências

- (+) O repositório pode ser público sem risco de expor cliente ou pessoa.
- (+) Cada vendedor mantém o próprio cadastro; ninguém precisa pedir permissão para usar.
- (−) Há um passo de preparação: criar `landing-pages/equipe/` na primeira vez (a skill faz isso pedindo os dados).
- (−) A checagem é heurística: não pega tudo (por exemplo, um nome que não esteja na lista privada). **Revisão humana no pull request continua obrigatória.**
- (−) Cada pessoa precisa manter a própria lista `.nomes-privados.txt`.

## Alternativas descartadas

- **Dados dentro do plugin, protegidos por `.gitignore`.** Um erro de `git add` vaza. A separação física elimina essa classe de erro.
- **Repositório privado.** Não atende "qualquer pessoa pode usar", e quem está de fora não conseguiria instalar.
- **Serviço central de cadastro da equipe.** Resolveria o preenchimento repetido, mas exige infraestrutura, conta e manutenção para um problema que um arquivo JSON resolve.
