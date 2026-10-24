# Resumo da Implantação — PortfolioHUB v2.0.0

Visão de uma página de tudo o que foi configurado e implementado na Entrega Final.

## Configurações do GitHub

| Área | Configuração | Estado |
|---|---|---|
| Planejamento | Milestone "v2.0.0 — Implantação (Entrega Final)"; issues #3 a #8 (uma por fase); labels `implantação`, `segurança`, `colaboração`, `ci-cd`, `dependências` | ✅ |
| Repositório | Público; wiki desativada; apagar branch após merge; merge commit e squash (rebase desativado) | ✅ |
| Pages | Fonte: GitHub Actions; HTTPS obrigatório | ✅ |
| Ambiente | `github-pages` aceita só a branch `main` e as tags `v*` | ✅ |
| Ruleset "Proteção da main" | PR obrigatório; 1 aprovação; revisão do code owner; aprovação descartada após novo push; aprovação do último push; conversas resolvidas; checks "Testes do site" e "Varredura de segredos"; sem force push; sem exclusão; bypass do admin só via PR | ✅ |
| Ruleset "Tags de versão" | `refs/tags/v*`: criação, alteração e exclusão bloqueadas; bypass só do admin | ✅ |
| Segurança | Secret scanning + push protection; Dependabot alerts + security updates; CodeQL (configuração padrão); relato privado de vulnerabilidades | ✅ |
| Actions | Token padrão somente leitura; Actions não podem aprovar PRs; só Actions do GitHub, verificadas ou o gitleaks; aprovação para workflows de forks de qualquer contribuidor externo | ✅ |
| Acesso | Inventário: 1 colaborador (admin), 0 convites, 0 deploy keys, 0 webhooks | ✅ |
| Conta | 2FA | 🔶 conferir na conta |

## Arquivos do repositório

| Arquivo | Função |
|---|---|
| `.github/workflows/ci.yml` | Testes do site (unittest, html-validate, node --check) e varredura de segredos (gitleaks), em todo PR e push na main |
| `.github/workflows/deploy-pages.yml` | Testes → montagem do `_site` → geração do `github.json` → busca de segredos → publicação no ambiente `github-pages` → teste de fumaça; a cada push na main, a cada Release publicada e diariamente |
| `.github/dependabot.yml` | Atualizações semanais de Actions, npm e pip |
| `.github/release.yml` | Categorias das notas de Release geradas automaticamente |
| `.github/CODEOWNERS` | Mantenedor revisa tudo; áreas sensíveis exclusivas |
| `SECURITY.md`, `CODE_OF_CONDUCT.md`, `CONTRIBUTING.md` | Políticas públicas |
| `scripts/gerar_dados_github.py` | Gera, no build, os dados públicos do GitHub para o site |
| `assets/js/github.js` | Seções Repositórios e Implantação: lê o JSON do build, com a API ao vivo como reserva; só `textContent` e links validados |
| `tests/test_site.py` | 14 testes: CSP, inline, estilos e fontes externos, noopener, innerHTML/eval, segredos, .env, links, âncoras, estrutura, JSON, versão |
| `package.json` + `package-lock.json` | html-validate com versão travada |
| `404.html`, `sitemap.xml`, `assets/img/favicon.svg` | Produção |
| `ferramentas/guia-implantacao-claude/` | Claude configurado como guia da implantação; transcrições |
| `documentacao/implantacao/` | Plano, IA como guia, ambiente, usuários, segurança, colaboração, testes, roteiro |
| `documentacao/slides/implantacao/` | Slides da apresentação final |

## Site

- CSP restritiva por `<meta>` em todas as páginas, sem `unsafe-inline` e sem `unsafe-eval`; `Referrer-Policy`.
- Novas seções: **Repositórios no GitHub** (lista ao vivo com filtro) e **Implantação** (versão em produção, último commit, status do CI e da publicação, equipe, links para as 6 etapas).
- Aviso de privacidade (sem cookies, sem coleta de dados).
- Botões dos slides e do site com `type="button"`; HTML validado.
- Fontes servidas pelo próprio site; imagem de prévia (`og:image`); conteúdo visível sem JavaScript; menu com `aria-expanded`.
- O próprio PortfolioHUB como projeto em destaque; lista de repositórios sem forks.

## Verificações feitas

| Verificação | Resultado |
|---|---|
| Testes locais | 14/14 OK |
| Prova negativa | 5 violações detectadas |
| html-validate | Sem erros (após corrigir 8 botões) |
| Push direto na main | Recusado (GH013) |
| Script de dados do GitHub | 7 repositórios, versão, commit e equipe gerados |

## Pendências conhecidas

- Confirmar o 2FA na conta do GitHub.
- Convidar um colega para um ciclo de PR com revisão real.
- Commits assinados e OpenSSF Scorecard (próximos passos da política).
- Gravar o vídeo de 5 minutos.

---

[← Voltar para a documentação da implantação](README.md)
