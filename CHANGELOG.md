# Changelog

Todas as mudanças relevantes deste repositório são registradas aqui.

O formato segue o [Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/) e o projeto usa [Versionamento Semântico](https://semver.org/lang/pt-BR/).

## [2.0.0] — 2026-10-25

Versão de produção (Entrega Final: implantação). Marcada como *major* porque muda a forma de publicar o site e passa a exigir Pull Request com checks para qualquer mudança na `main`.

### Adicionado

- **Guia de implantação com o Claude** (`ferramentas/guia-implantacao-claude/`): system prompt de guia, trilha de prompts com os enunciados anexados e transcrições versionadas.
- **Documentação da implantação** (`documentacao/implantacao/`): plano, IA como guia, ambiente GitHub, gestão de usuários, política de segurança, compartilhamento e colaboração, testes e lançamento, roteiro e resumo.
- **CI** (`.github/workflows/ci.yml`): testes do site e varredura de segredos (gitleaks) em todo PR.
- **Publicação via GitHub Actions** (`.github/workflows/deploy-pages.yml`) no ambiente `github-pages`, só depois dos testes, com republicação diária.
- **Integração com o GitHub no site**: seções Repositórios (lista ao vivo com filtro) e Implantação (versão em produção, último commit, status dos workflows, equipe). Dados gerados no build por `scripts/gerar_dados_github.py`, com a API pública como reserva.
- **Testes automatizados** (`tests/test_site.py`): CSP, scripts e estilos inline, `noopener`, uso de `innerHTML`/`eval`, padrões de chaves, `.env`, links internos, âncoras, estrutura, JSON e versão.
- `SECURITY.md`, `CODE_OF_CONDUCT.md`, `.github/CODEOWNERS`, `.github/dependabot.yml`.
- Página 404, favicon, sitemap, imagem de prévia (`og:image`) e aviso de privacidade.
- Slides da apresentação da implantação (`documentacao/slides/implantacao/`).
- Card do próprio PortfolioHUB como projeto em destaque e competências por área.
- Notas de Release por categoria (`.github/release.yml`).
- Republicação automática do site ao publicar uma Release.

### Alterado

- Content Security Policy restritiva em todas as páginas; CSS e JS dos slides movidos para arquivos (`slides.css`, `slides.js`) para dispensar `unsafe-inline`.
- Fontes Inter e JetBrains Mono hospedadas no próprio site (licença OFL), sem requisições ao Google Fonts.
- Lista de repositórios sem forks; texto da equipe fiel à situação atual.

### Corrigido

- Com o JavaScript desligado, as seções animadas ficavam invisíveis; agora só são ocultadas quando o JavaScript está ativo.
- Botão do menu mobile com `aria-controls` e `aria-expanded`.
- `CONTRIBUTING.md` com o fluxo protegido e como obter acesso.

### Segurança (configurações do repositório)

- Rulesets "Proteção da main" (PR com aprovação do code owner, checks obrigatórios, sem force push e sem exclusão) e "Tags de versão".
- Secret scanning com push protection, Dependabot (alertas e atualizações), CodeQL e relato privado de vulnerabilidades.
- Token dos workflows somente leitura por padrão, Actions fixadas por SHA, só Actions permitidas e aprovação para workflows de forks.

## [1.1.0] — 2026-10-16

### Adicionado

- Projeto acadêmico **Bootcamp — Integração com a API do Claude** (`projetos-academicos/bootcamp-claude-api/`), com 5 notebooks, README, `requirements.txt` e `.env.example`.
- Índices de projetos acadêmicos e pessoais com links para os demais repositórios.
- Guias em `documentacao/`: Git e versionamento, colaboração, GitHub Pages, integração com o LinkedIn e roteiro da apresentação.
- Slides do repositório em HTML (`documentacao/slides/`).
- Seções **Documentação**, **Slides** e **Versões** no site.
- `CONTRIBUTING.md` e modelos de Issue e Pull Request em `.github/`.
- README principal completo, com badges, estrutura, versionamento e contato.

## [1.0.0] — 2026-10-16

### Adicionado

- Estrutura de diretórios: `projetos-academicos/`, `projetos-pessoais/`, `documentacao/` e `assets/`.
- Site estático no GitHub Pages com as seções Sobre, Projetos e Contato.
- Tema claro/escuro, layout responsivo e menu mobile.
- `.gitignore` (inclui `.env`) e licença MIT.

[2.0.0]: https://github.com/MarcellinhoHM/PortfolioHUB/compare/v1.1.0...v2.0.0
[1.1.0]: https://github.com/MarcellinhoHM/PortfolioHUB/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/MarcellinhoHM/PortfolioHUB/releases/tag/v1.0.0
