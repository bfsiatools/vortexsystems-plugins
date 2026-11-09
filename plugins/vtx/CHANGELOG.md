# Histórico de mudanças

Formato: [Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/). Versionamento: [SemVer](https://semver.org/lang/pt-BR/). **Toda versão nova precisa subir o `version` em `.claude-plugin/plugin.json`**: sem isso os usuários não recebem a atualização.

## [Não lançado]

## [0.2.0] - 2026-11-09

### Adicionado
- **Vídeo opcional dos próximos passos.** A skill agora pergunta sempre se a pessoa quer o vídeo. Com "sim", gera o vídeo da casa (`scripts/gerar_video.py`, modelo em `modelo-video/`): vertical, ~41 s, 3D, voz e legendas, com a logo da casa, o print da página da casa e o WhatsApp de quem fechou. Com "não", a página sai com a mesma estrutura, só sem o vídeo.
- `video_realces` no `cliente.json`: descreve onde ficam as marcações de banner, logo e cardápio quando o print da página não é o padrão (734×1280).
- Decisão registrada: [0005](../../docs/decisoes/0005-video-opcional-com-voz-sem-o-nome-da-casa.md).

### Alterado
- A voz do vídeo **não fala o nome da casa** (abre com "Fechou com a VTX Tap."); o nome aparece escrito, junto da logo. Assim a mesma voz serve para todas as casas.
- `checar_publicacao.py` ignora constantes numéricas em `.js` e `.css` e trechos `pacote@1.2.3`, sem afrouxar a checagem de telefone, e-mail e nomes privados.

### Requisitos novos (só para o vídeo)
- Node.js (`npx`), ffmpeg e internet na primeira vez (baixa o HyperFrames 0.8.209). Sem eles a skill oferece gerar a página sem vídeo.

### Em aberto
- Licença de uso comercial e redistribuição do áudio sintético (`modelo-video/assets/voz.m4a`) ainda não conferida.

## [0.1.0] - 2026-11-09

Primeira versão.

### Adicionado
- Skill `landing-page` (`/vtx:landing-page`): pergunta a logo da casa, o(s) dono(s), quem fechou o contrato, a foto e o WhatsApp dessa pessoa e gera a landing page de boas-vindas e próximos passos.
- Modelo da página: três vozes tipográficas (Big Shoulders Display, Schibsted Grotesk, IBM Plex Mono), cores da marca, linha do tempo de 4 passos, lockup VTX Tap × logo da casa com ondas de NFC, prévia de tela e vídeo opcionais, cartão do vendedor com foto, nome e WhatsApp.
- Saudação e artigo concordados (Bem-vindo, Bem-vinda, Bem-vindos, Bem-vindas; o, a, os, as).
- Cadastro da equipe (`landing-pages/equipe/`) fora do plugin, com foto e WhatsApp por pessoa.
- `gerar.py` (com `--unico`: arquivo único com tudo embutido), `verificar.py` (checagens e fotos de conferência) e `verificar-navegador.cjs` (teste de navegador, opcional).
- `checar_publicacao.py`: barra foto, vídeo, telefone, e-mail que não seja o institucional, caminho de usuário, token e nomes da lista privada antes de qualquer publicação.
- Exemplo fictício (casa e vendedora) para testar.
- Referências: design, estrutura, regras de conteúdo e publicação.
