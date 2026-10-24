<div align="center">

# PortfolioHUB

**Portfólio de projetos acadêmicos e pessoais, versionado com Git e publicado no GitHub Pages.**

[![GitHub Pages](https://img.shields.io/badge/site-GitHub_Pages-7b2d8e?logo=github&logoColor=white)](https://marcellinhohm.github.io/PortfolioHUB/)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Marcello_Montella-0A66C2?logo=linkedin&logoColor=white)](https://www.linkedin.com/in/marcello-augusto-hesketh-montella-042a66370)
[![Release](https://img.shields.io/github/v/release/MarcellinhoHM/PortfolioHUB?label=vers%C3%A3o&color=d63384)](https://github.com/MarcellinhoHM/PortfolioHUB/releases)
[![Licença MIT](https://img.shields.io/badge/licen%C3%A7a-MIT-green)](LICENSE)
[![CI](https://github.com/MarcellinhoHM/PortfolioHUB/actions/workflows/ci.yml/badge.svg)](https://github.com/MarcellinhoHM/PortfolioHUB/actions/workflows/ci.yml)
[![Publicação](https://github.com/MarcellinhoHM/PortfolioHUB/actions/workflows/deploy-pages.yml/badge.svg)](https://github.com/MarcellinhoHM/PortfolioHUB/actions/workflows/deploy-pages.yml)

[**Site**](https://marcellinhohm.github.io/PortfolioHUB/) ·
[**Implantação**](documentacao/implantacao/) ·
[**Slides**](https://marcellinhohm.github.io/PortfolioHUB/documentacao/slides/implantacao/) ·
[**Documentação**](documentacao/) ·
[**LinkedIn**](https://www.linkedin.com/in/marcello-augusto-hesketh-montella-042a66370)

</div>

---

## Sumário

- [Sobre](#sobre)
- [Implantação (v2.0.0)](#implantação-v200)
- [Estrutura do repositório](#estrutura-do-repositório)
- [Projetos](#projetos)
- [GitHub Pages](#github-pages)
- [Segurança](#segurança)
- [Versionamento](#versionamento)
- [Como usar este repositório](#como-usar-este-repositório)
- [Documentação](#documentação)
- [Contribuindo](#contribuindo)
- [Contato](#contato)

## Sobre

O **PortfolioHUB** é o repositório central do meu portfólio profissional. Ele reúne meus projetos acadêmicos e pessoais em um só lugar, organizados por categoria, documentados e com histórico de versões. O site gerado a partir deste repositório está no ar em **[marcellinhohm.github.io/PortfolioHUB](https://marcellinhohm.github.io/PortfolioHUB/)**.

Objetivos:

- Organizar meus projetos de forma clara, com um README para cada um.
- Aplicar boas práticas de versionamento com Git (commits padronizados, branches, Pull Requests, tags).
- Publicar uma página de portfólio no GitHub Pages.
- Conectar o repositório ao meu perfil no LinkedIn.
- Manter o portfólio em produção com segurança, controle de acesso e testes automatizados.

## Implantação (v2.0.0)

Na Entrega Final, o PortfolioHUB foi implantado em produção com o **Claude** (Anthropic) como IA guia da trilha. Toda a documentação está em [`documentacao/implantacao/`](documentacao/implantacao/).

| Etapa | O que foi feito | Documento |
|---|---|---|
| 1. Planejamento | Plano com fases, riscos e rollback; Claude configurado como guia por API, com as transcrições versionadas | [Plano](documentacao/implantacao/plano-de-implantacao.md) · [IA como guia](documentacao/implantacao/ia-guia.md) |
| 2. Ambiente GitHub | Publicação via Actions no ambiente `github-pages`; site integrado à API do GitHub | [Ambiente](documentacao/implantacao/ambiente-github.md) |
| 3. Usuários e segurança | Rulesets, CODEOWNERS, secret scanning, Dependabot, CodeQL, CSP, SECURITY.md | [Usuários](documentacao/implantacao/gestao-de-usuarios.md) · [Segurança](documentacao/implantacao/politica-de-seguranca.md) |
| 4. Colaboração | Fluxo Issue → branch → PR → CI → revisão → merge, documentado | [Colaboração](documentacao/implantacao/compartilhamento-e-colaboracao.md) |
| 5. Testes e produção | CI com 18 verificações, teste de fumaça, checklist de lançamento | [Testes](documentacao/implantacao/testes-e-lancamento.md) |
| 6. Apresentação | Roteiro de 5 minutos e slides | [Roteiro](documentacao/implantacao/roteiro-apresentacao-final.md) |

## Estrutura do repositório

```
PortfolioHUB/
├── index.html                    # página do portfólio (GitHub Pages)
├── 404.html · sitemap.xml        # produção
├── assets/
│   ├── css/style.css             # estilos do site
│   ├── js/main.js                # interações (tema, menu, animações)
│   ├── js/github.js              # integração com o GitHub (repositórios, versão, equipe)
│   └── img/                      # imagens e favicon
├── projetos-academicos/          # trabalhos de faculdade e bootcamp
│   ├── README.md                 # índice dos projetos acadêmicos
│   └── bootcamp-claude-api/      # notebooks Python + README
├── projetos-pessoais/            # projetos próprios
│   └── README.md                 # índice dos projetos pessoais
├── documentacao/                 # guias, roteiro e slides
│   ├── implantacao/              # documentação da Entrega Final
│   ├── guia-git-e-versionamento.md
│   ├── guia-colaboracao.md
│   ├── guia-github-pages.md
│   ├── integracao-linkedin.md
│   ├── roteiro-apresentacao.md
│   └── slides/                   # apresentações (intermediária e implantação)
├── ferramentas/
│   └── guia-implantacao-claude/  # Claude como guia da implantação + transcrições
├── scripts/                      # geração dos dados do GitHub no build
├── tests/                        # testes automatizados do site
├── .github/                      # workflows, CODEOWNERS, Dependabot, modelos
├── CHANGELOG.md                  # histórico de versões
├── CONTRIBUTING.md · CODE_OF_CONDUCT.md · SECURITY.md
└── LICENSE                       # licença MIT
```

| Seção | Conteúdo |
|---|---|
| [`projetos-academicos/`](projetos-academicos/) | Trabalhos de disciplinas e do bootcamp. |
| [`projetos-pessoais/`](projetos-pessoais/) | Projetos próprios de estudo e prática. |
| [`documentacao/`](documentacao/) | Guias de Git, colaboração, GitHub Pages, LinkedIn, roteiro e slides. |
| [`assets/`](assets/) | Arquivos do site publicado no GitHub Pages. |

## Projetos

### Acadêmicos

| Projeto | Descrição | Tecnologias |
|---|---|---|
| ⭐ [Bootcamp — API do Claude](projetos-academicos/bootcamp-claude-api/) | Notebooks sobre requisições, system prompt, temperatura, streaming e tool use com o SDK da Anthropic. | Python, Jupyter |
| [Caixa Eletrônico (ATM)](https://github.com/MarcellinhoHM/Atm) | Simulador de caixa eletrônico modularizado. | C |
| [Prova — Site Temático](https://github.com/MarcellinhoHM/Prova) | Site com login e página principal. | HTML, Bootstrap |
| [Programação Web](https://github.com/MarcellinhoHM/programacao_web_cc_a) | Exercícios da disciplina de Programação para Web. | HTML, CSS, JS |

### Pessoais

| Projeto | Descrição | Tecnologias |
|---|---|---|
| [RPG de Terminal](https://github.com/MarcellinhoHM/RPG) | RPG por turnos com personagens, inventário e níveis. | Java |
| [Ponto Eletrônico](https://github.com/MarcellinhoHM/ponto-eletronico) | Registro de ponto com data e hora em tempo real ([demo](https://marcellinhohm.github.io/ponto-eletronico/)). | HTML, CSS, JS |

## GitHub Pages

O site é publicado pelo GitHub Actions (workflow `deploy-pages.yml`) no ambiente `github-pages`, só depois que os testes passam, e reúne:

- **Sobre** e **Contato** (com LinkedIn, GitHub e aviso de privacidade);
- **Projetos** em cards, com links para código e demonstração;
- **Repositórios no GitHub**, lista atualizada automaticamente, com filtro;
- **Implantação**, com a versão em produção, o último commit, o status do CI e a equipe;
- **Documentação** com atalhos para os guias;
- **Slides** da apresentação embutidos na página;
- **Versões** em linha do tempo.

🔗 **https://marcellinhohm.github.io/PortfolioHUB/**

Detalhes em [Guia do GitHub Pages](documentacao/guia-github-pages.md) e [Ambiente GitHub](documentacao/implantacao/ambiente-github.md).

## Segurança

- A `main` só recebe mudanças por Pull Request, com testes obrigatórios e revisão do responsável ([CODEOWNERS](.github/CODEOWNERS)).
- Secret scanning com push protection, Dependabot e CodeQL ativos.
- Site com Content Security Policy restritiva e nenhum segredo no front-end.
- Encontrou uma vulnerabilidade? Siga o [SECURITY.md](SECURITY.md).

Política completa: [politica-de-seguranca.md](documentacao/implantacao/politica-de-seguranca.md).

## Versionamento

| Prática | Como é aplicada |
|---|---|
| Commits | [Conventional Commits](https://www.conventionalcommits.org/pt-br/) — `feat`, `docs`, `fix`, `chore`... |
| Branches | `main` estável; `feature/*`, `docs/*` e `fix/*` para mudanças. |
| Integração | Toda mudança entra na `main` por [Pull Request](https://github.com/MarcellinhoHM/PortfolioHUB/pulls?q=is%3Apr). |
| Versões | [SemVer](https://semver.org/lang/pt-BR/) com tags anotadas e [Releases](https://github.com/MarcellinhoHM/PortfolioHUB/releases). |
| Histórico | [CHANGELOG.md](CHANGELOG.md). |

Versões publicadas:

- **v1.0.0** — estrutura de diretórios e primeira versão do site.
- **v1.1.0** — projeto do bootcamp, documentação, slides, integração com LinkedIn e este README.
- **v2.0.0** — implantação em produção: ambiente GitHub, segurança, colaboração protegida, testes e guia de implantação com o Claude.

Veja o histórico completo com:

```bash
git log --oneline --graph --decorate --all
```

## Como usar este repositório

```bash
# 1. clonar
git clone https://github.com/MarcellinhoHM/PortfolioHUB.git
cd PortfolioHUB

# 2. ver o site localmente
python -m http.server 8000
# abrir http://localhost:8000

# 2b. rodar os testes
python -m unittest discover -s tests -v
npm ci && npm run test:html

# 3. executar o projeto do bootcamp
cd projetos-academicos/bootcamp-claude-api
pip install -r requirements.txt
cp .env.example .env   # e preencher a ANTHROPIC_API_KEY
```

## Documentação

| Guia | Conteúdo |
|---|---|
| [Git e Versionamento](documentacao/guia-git-e-versionamento.md) | Fluxo local → remoto, comandos, commits, branches, SemVer e tags. |
| [Colaboração](documentacao/guia-colaboracao.md) | Issues, Pull Requests, revisão e conflitos. |
| [GitHub Pages](documentacao/guia-github-pages.md) | Publicação e atualização do site. |
| [Integração com o LinkedIn](documentacao/integracao-linkedin.md) | Links de compartilhamento e passo a passo no LinkedIn. |
| [Roteiro da Apresentação](documentacao/roteiro-apresentacao.md) | Roteiro do vídeo de 5 minutos (etapa intermediária). |
| [Implantação](documentacao/implantacao/) | Documentação completa da Entrega Final. |

## Contribuindo

Sugestões são bem-vindas! Leia o [CONTRIBUTING.md](CONTRIBUTING.md) e o [Código de Conduta](CODE_OF_CONDUCT.md), e use os modelos de [Issue](https://github.com/MarcellinhoHM/PortfolioHUB/issues/new/choose) e de Pull Request.

## Contato

**Marcello Augusto Hesketh Montella**

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Conectar-0A66C2?logo=linkedin&logoColor=white&style=for-the-badge)](https://www.linkedin.com/in/marcello-augusto-hesketh-montella-042a66370)
[![GitHub](https://img.shields.io/badge/GitHub-MarcellinhoHM-181717?logo=github&logoColor=white&style=for-the-badge)](https://github.com/MarcellinhoHM)

---

<sub>Distribuído sob a licença MIT. Veja [LICENSE](LICENSE).</sub>
