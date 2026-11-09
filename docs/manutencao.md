# Manutenção: alterar, versionar e lançar

Para quem mantém o plugin. Regra de ouro: **o modelo é a fonte**. Qualquer mudança de texto, ordem dos passos ou visual é mudança do produto, não de um cliente.

## Mudar o modelo da página

1. Edite `plugins/vtx/skills/landing-page/modelo/index.html`.
2. Se mudou tipografia, cor, espaço, componente ou movimento, atualize `referencia/design.md` **no mesmo commit**.
3. Se mudou o que a página afirma, o fluxo dos passos ou um prazo, atualize `referencia/regras-de-conteudo.md` e `referencia/estrutura.md`, e confirme com o responsável pela marca antes.
4. Se mudou uma decisão de fundo, escreva um novo registro em [`docs/decisoes/`](decisoes/) (não edite os antigos: marque-os como substituídos).

## Testar (sempre, antes do commit)

```bash
cd plugins/vtx/skills/landing-page
python scripts/gerar.py exemplo/clientes/casa-exemplo/cliente.json --equipe exemplo/equipe/equipe.json --saida saida-teste
python scripts/verificar.py saida-teste/casa-exemplo
python scripts/checar_publicacao.py
```

O exemplo é de propósito difícil: dono no **plural feminino**, artigo **"a"** e uma vendedora diferente. Esperado: `Bem-vindas, Maria e Joana.` e `RESULTADO: OK`, e a checagem de publicação `limpo`.

Na raiz do repositório, valide também o plugin e o catálogo:

```bash
claude plugin validate --strict .
claude plugin validate --strict plugins/vtx
```

O CI repete tudo isso em cada push e pull request.

## Versionar e lançar

O plugin usa **versão explícita** (`plugins/vtx/.claude-plugin/plugin.json`). Os usuários só recebem uma atualização quando a versão **muda**: se você subir commits sem subir o `version`, ninguém recebe nada.

1. Escolha a versão ([SemVer](https://semver.org/lang/pt-BR/)): `0.x.y` enquanto estiver se firmando; **patch** para correção, **minor** para recurso novo, **major** para mudança que quebra (ex.: campo obrigatório novo em `cliente.json`).
2. Suba o `version` em `plugin.json` **e só lá** (não repita no `marketplace.json`: o Claude Code usa o do `plugin.json` sem avisar).
3. Mova o que estava em "Não lançado" do [CHANGELOG](../plugins/vtx/CHANGELOG.md) para a nova versão, com a data.
4. Commit: `chore(release): vtx 0.2.0`.
5. Opcional: crie a etiqueta de versão com `claude plugin tag` (a partir de `plugins/vtx`; cria `vtx--v0.2.0`). Só é necessário se outro plugin declarar dependência de versão do `vtx`.

## Como o usuário recebe

`claude plugin update vtx@vortexsystems` (ou a atualização automática, que cada pessoa liga em `/plugin` > **Marketplaces**). Ela vem **desligada** por padrão.

## Nomes são permanentes

- O marketplace (`vortexsystems`) e o plugin (`vtx`) são identificadores: quem instalou guarda esses nomes. **Não renomeie.**
- Se for inevitável, use o mapa `renames` no `marketplace.json` para migrar quem já instalou (`claude plugin validate` confere a cadeia).
- Para mudar só o rótulo que aparece, use `displayName` no `plugin.json`.

## Novos plugins ou skills

- Skill nova que combina com o `vtx` (vendas e implantação da VTX Tap): `plugins/vtx/skills/<nome>/SKILL.md`; o comando vira `/vtx:<nome>`.
- Assunto diferente: novo plugin em `plugins/<nome>/`, com a própria entrada em `marketplace.json`.
- Em ambos: README do plugin, CHANGELOG, exemplo fictício, nenhum dado real.

## Privacidade, o tempo todo

- **Nunca** coloque cliente, pessoa, foto, vídeo, telefone ou e-mail pessoal no repositório. O `.gitignore` e a checagem ajudam, mas a revisão é humana.
- Mantenha, **fora do repositório**, um arquivo `.nomes-privados.txt` (na raiz do seu projeto de trabalho, um nome por linha: clientes, pessoas, números). A checagem o usa para barrar nomes reais.
- Se algo vazou, siga o [SECURITY](../SECURITY.md): remover do histórico, não só do último commit.
