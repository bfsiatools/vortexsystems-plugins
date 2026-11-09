# Histórico de mudanças

Formato: [Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/). Versionamento: [SemVer](https://semver.org/lang/pt-BR/). **Toda versão nova precisa subir o `version` em `.claude-plugin/plugin.json`**: sem isso os usuários não recebem a atualização.

## [Não lançado]

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
