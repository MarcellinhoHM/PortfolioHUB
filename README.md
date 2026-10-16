<div align="center">

# PortfolioHUB

**Portfólio de projetos acadêmicos e pessoais, versionado com Git e publicado no GitHub Pages.**

[![GitHub Pages](https://img.shields.io/badge/site-GitHub_Pages-7b2d8e?logo=github&logoColor=white)](https://marcellinhohm.github.io/PortfolioHUB/)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Marcello_Montella-0A66C2?logo=linkedin&logoColor=white)](https://www.linkedin.com/in/marcello-augusto-hesketh-montella-042a66370)
[![Release](https://img.shields.io/github/v/release/MarcellinhoHM/PortfolioHUB?label=vers%C3%A3o&color=d63384)](https://github.com/MarcellinhoHM/PortfolioHUB/releases)
[![Licença MIT](https://img.shields.io/badge/licen%C3%A7a-MIT-green)](LICENSE)

[**Site**](https://marcellinhohm.github.io/PortfolioHUB/) ·
[**Slides**](https://marcellinhohm.github.io/PortfolioHUB/documentacao/slides/) ·
[**Documentação**](documentacao/) ·
[**LinkedIn**](https://www.linkedin.com/in/marcello-augusto-hesketh-montella-042a66370)

</div>

---

## Sumário

- [Sobre](#sobre)
- [Estrutura do repositório](#estrutura-do-repositório)
- [Projetos](#projetos)
- [GitHub Pages](#github-pages)
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

## Estrutura do repositório

```
PortfolioHUB/
├── index.html                    # página do portfólio (GitHub Pages)
├── assets/
│   ├── css/style.css             # estilos do site
│   ├── js/main.js                # interações (tema, menu, animações)
│   └── img/                      # imagens
├── projetos-academicos/          # trabalhos de faculdade e bootcamp
│   ├── README.md                 # índice dos projetos acadêmicos
│   └── bootcamp-claude-api/      # notebooks Python + README
├── projetos-pessoais/            # projetos próprios
│   └── README.md                 # índice dos projetos pessoais
├── documentacao/                 # guias, roteiro e slides
│   ├── guia-git-e-versionamento.md
│   ├── guia-colaboracao.md
│   ├── guia-github-pages.md
│   ├── integracao-linkedin.md
│   ├── roteiro-apresentacao.md
│   └── slides/index.html
├── .github/                      # modelos de Issue e Pull Request
├── CHANGELOG.md                  # histórico de versões
├── CONTRIBUTING.md               # como contribuir
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

O site é publicado a partir da branch `main` (pasta raiz) e reúne:

- **Sobre** e **Contato** (com LinkedIn e GitHub);
- **Projetos** em cards, com links para código e demonstração;
- **Documentação** com atalhos para os guias;
- **Slides** da apresentação embutidos na página;
- **Versões** em linha do tempo.

🔗 **https://marcellinhohm.github.io/PortfolioHUB/**

Detalhes em [Guia do GitHub Pages](documentacao/guia-github-pages.md).

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
| [Roteiro da Apresentação](documentacao/roteiro-apresentacao.md) | Roteiro do vídeo de 5 minutos. |

## Contribuindo

Sugestões são bem-vindas! Leia o [CONTRIBUTING.md](CONTRIBUTING.md) e use os modelos de [Issue](https://github.com/MarcellinhoHM/PortfolioHUB/issues/new/choose) e de Pull Request.

## Contato

**Marcello Augusto Hesketh Montella**

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Conectar-0A66C2?logo=linkedin&logoColor=white&style=for-the-badge)](https://www.linkedin.com/in/marcello-augusto-hesketh-montella-042a66370)
[![GitHub](https://img.shields.io/badge/GitHub-MarcellinhoHM-181717?logo=github&logoColor=white&style=for-the-badge)](https://github.com/MarcellinhoHM)

---

<sub>Distribuído sob a licença MIT. Veja [LICENSE](LICENSE).</sub>
