# Testes e Lançamento em Produção

Seção 5 da Entrega Final: finalização da integração, testes e preparação do PortfolioHUB para produção. O plano segue a estratégia proposta pelo guia (prompt 11 da [trilha](../../ferramentas/guia-implantacao-claude/transcricoes/trilha.md)), ajustada ao que faz sentido para um site estático.

## Sumário

1. [Estratégia](#1-estratégia)
2. [Testes automatizados](#2-testes-automatizados)
3. [Testes de controle de acesso](#3-testes-de-controle-de-acesso)
4. [Testes manuais](#4-testes-manuais)
5. [Checklist de lançamento da v2.0.0](#5-checklist-de-lançamento-da-v200)
6. [Registro de execução](#6-registro-de-execução)

## 1. Estratégia

| Camada | Quando roda | Bloqueia? | Objetivo |
|---|---|---|---|
| CI no PR ([`ci.yml`](../../.github/workflows/ci.yml)) | Todo PR e todo push na `main` | ✅ Checks obrigatórios na ruleset | Impedir que defeitos cheguem à `main` |
| Testes antes de publicar ([`deploy-pages.yml`](../../.github/workflows/deploy-pages.yml)) | Toda publicação | ✅ Interrompe a publicação | Não publicar um site quebrado |
| Busca de segredos no pacote publicado | Toda publicação | ✅ Interrompe a publicação | Nada sensível chega ao Pages |
| Teste de fumaça em produção | Depois de cada publicação | ⚠️ Marca a execução como falha | Confirmar que o site no ar responde |
| CodeQL e Dependabot | Em PRs e periodicamente | ⚠️ Alertas na aba Security | Vulnerabilidades no código e nas dependências |
| Testes manuais | Antes da Release | ✅ Critério de Go/No-Go | O que a automação não vê |

**Fora do escopo, por não fazer sentido aqui:** testes de carga e testes de API própria (não há backend).

## 2. Testes automatizados

| ID | Teste | Ferramenta | Controle |
|---|---|---|---|
| T-01 | Toda página tem CSP restritiva (sem `unsafe-inline`/`unsafe-eval`) | `unittest` | SITE-02 |
| T-02 | Nenhum script, `<style>` ou atributo `style=` inline; nenhum CSS ou fonte de terceiros | `unittest` | SITE-02, SITE-05 |
| T-03 | Links externos com `noopener` | `unittest` | SITE-06 |
| T-04 | JavaScript sem `innerHTML`, `outerHTML`, `insertAdjacentHTML`, `eval`, `new Function` | `unittest` | SITE-04 |
| T-05 | Nenhum padrão de chave (Anthropic, GitHub, AWS, chave privada) em arquivo versionado | `unittest` | REP-03, SITE-07 |
| T-06 | `.env` fora do Git e presente no `.gitignore` | `unittest` | REP-08 |
| T-07 | SECURITY.md, CODEOWNERS e dependabot.yml existem | `unittest` | REP-02, REP-04, REP-06 |
| T-08 | Links internos (`href`/`src`) apontam para arquivos existentes | `unittest` | Integridade |
| T-09 | Âncoras do menu existem na página | `unittest` | Integridade |
| T-10 | Pastas principais têm README; arquivos de produção (404, sitemap, favicon) existem | `unittest` | Documentação, produção |
| T-11 | Todo `.json` do repositório é válido | `unittest` | Integridade |
| T-12 | Versão do rodapé igual à última versão do CHANGELOG | `unittest` | Versionamento |
| T-13 | HTML válido (regras recomendadas) | `html-validate` 11.17.0 | Qualidade, acessibilidade |
| T-14 | Sintaxe do JavaScript | `node --check` | Qualidade |
| T-15 | Segredos no histórico completo do Git | gitleaks | REP-03 |
| T-16 | Segredos no pacote que vai ser publicado (`_site`) | `grep` no workflow | ACT-06 |
| T-17 | Teste de fumaça: páginas 200, 404 personalizado, CSP presente, `github.json` com repositórios | `curl` no workflow | Disponibilidade |
| T-18 | Análise estática do código | CodeQL (configuração padrão) | REP-05 |

Rodar localmente:

```bash
python -m unittest discover -s tests -v   # T-01 a T-12 (14 testes)
npm ci && npm run test:html                # T-13
for f in assets/js/*.js documentacao/slides/*.js; do node --check "$f"; done   # T-14
```

### Os testes pegam problemas de verdade

Prova negativa feita em 24/10/2026: uma página temporária com script inline, sem CSP, com link quebrado e link externo sem `noopener`, mais um arquivo com uma chave falsa no formato da Anthropic.

```text
FAIL: test_links_internos_existem ... link='nao-existe.html'
FAIL: test_links_externos_com_noopener ... ['https://example.com'] != []
FAIL: test_nenhum_segredo_versionado ... possível chave da Anthropic encontrado
FAIL: test_sem_script_ou_estilo_inline ... 1 != 0 : script inline
FAIL: test_toda_pagina_tem_csp_restritiva ... página sem Content-Security-Policy
Ran 13 tests — FAILED (failures=5)
```

Depois de remover os arquivos temporários: `Ran 13 tests — OK`.

## 3. Testes de controle de acesso

### Push direto na main

Teste feito em 24/10/2026, logo depois de ativar a ruleset:

```text
$ git push origin <commit-de-teste>:refs/heads/main
remote: error: GH013: Repository rule violations found for refs/heads/main.
remote: - Changes must be made through a pull request.
remote: - 2 of 2 required status checks are expected.
 ! [remote rejected] ... -> main (push declined due to repository rule violations)
```

A `main` continuou no commit `f741d68`: nada foi alterado.

### Demais verificações

| Verificação | Como | Resultado esperado |
|---|---|---|
| PR sem checks verdes | Abrir PR | Merge bloqueado até "Testes do site" e "Varredura de segredos" passarem |
| PR sem aprovação | Abrir PR | "Review required"; o mantenedor só mescla marcando *bypass rules* |
| Tag `v*` por quem não é admin | `git push origin v9.9.9` | Recusado pela ruleset "Tags de versão" |
| CODEOWNERS válido | `gh api repos/MarcellinhoHM/PortfolioHUB/codeowners/errors` | `{"errors":[]}` |

## 4. Testes manuais

| ID | Teste | Como | Aprovado se |
|---|---|---|---|
| M-01 | Navegadores | Chrome e Edge | Layout e funções iguais |
| M-02 | Responsividade | Larguras de 390 e 1280 px | Sem rolagem horizontal; menu mobile funcionando |
| M-03 | Tema claro e escuro | Alternar e recarregar | Preferência mantida; contraste legível |
| M-04 | Teclado | Tab, Shift+Tab e Enter | Foco visível; tudo acessível |
| M-05 | Slides | Todas as telas, no iframe e em tela cheia | Navegação e centralização corretas |
| M-06 | Reserva da API | Bloquear `github.json` no DevTools | Dados vêm da API ao vivo |
| M-07 | API indisponível | Bloquear também `api.github.com` | Mensagem amigável com link para o GitHub |
| M-08 | JavaScript desligado | DevTools → *Disable JavaScript* | Conteúdo estático visível e aviso no lugar da lista |
| M-09 | Console limpo | Console em todas as páginas | Nenhum erro e nenhuma violação de CSP |
| M-10 | Links do LinkedIn | Clicar | Abrem o perfil correto |
| M-11 | Página 404 | URL inexistente | Página personalizada com link de volta |
| M-12 | Conteúdo e LGPD | Ler todas as seções | Sem erros; sem telefone, endereço ou e-mail pessoal |
| M-13 | HTTPS | Abrir com `http://` | Redireciona para `https://` |

## 5. Checklist de lançamento da v2.0.0

### Critérios de Go/No-Go

| Critério | Go |
|---|---|
| CI (T-01 a T-15) | Verde no PR e na `main` |
| Publicação (T-16, T-17) | Verde, incluindo o teste de fumaça |
| CodeQL e Dependabot | Nenhum alerta crítico ou alto aberto |
| Testes manuais | M-01 a M-13 aprovados |
| Documentação | Plano, políticas, guias, CHANGELOG e README atualizados |

Qualquer item vermelho é No-Go: corrigir ou registrar a exceção com justificativa.

### Passos

- [x] PR da implantação aberto, fechando as issues das fases concluídas
- [x] CI verde no PR
- [x] Revisão final com o guia ([transcrição](../../ferramentas/guia-implantacao-claude/transcricoes/revisao.md))
- [x] Merge do PR #9 (mantenedor, com bypass registrado e checks verdes)
- [x] Publicação verde, com o teste de fumaça
- [x] `git tag -a v2.0.0 -m "v2.0.0 — Implantação em produção" && git push origin v2.0.0`
- [x] `gh release create v2.0.0 --verify-tag --title "v2.0.0 — Implantação em produção"`
- [x] Rodapé mostrando `v2.0.0`
- [ ] Painel "Versão em produção" mostrando `v2.0.0` → **falhou**; corrigido na v2.0.1 (ver abaixo)

### Depois do lançamento

| Momento | Verificação |
|---|---|
| Logo após a publicação | Teste de fumaça verde; M-09 e M-11 repetidos em produção |
| +1 hora | Painel mostra a `v2.0.0`; nenhum alerta novo na aba Security |
| Divulgação | Atualizar o projeto no LinkedIn com o link da Release |

### Gatilhos de rollback

| Situação | Ação |
|---|---|
| Teste de fumaça falhou ou site fora do ar | RB1: `git revert` por PR, ou publicar a partir da tag `v1.1.0` |
| Segredo detectado depois da publicação | RB3: revogar a chave imediatamente |
| Defeito visual grave | Correção por PR e Release `v2.0.1` (não reescrever a `v2.0.0` divulgada) |

## 6. Registro de execução

> **Problema encontrado no lançamento:** depois da Release v2.0.0, o painel "Versão em produção" continuou mostrando a v1.1.0. O site lia primeiro o JSON gerado no build, e a publicação disparada pela Release rodou com o mesmo commit do merge; o GitHub Pages manteve o conteúdo já publicado para aquele commit (o arquivo seguiu com a data da publicação anterior por mais de 10 minutos). Correção na v2.0.1: dados ao vivo da API do GitHub, com o JSON como reserva, e remoção do gatilho de Release.


| ID | Data | Ambiente | Resultado | Evidência |
|---|---|---|---|---|
| T-01 a T-12 | 24/10/2026 | Local (Python 3.12) | ✅ 14 testes OK (13 na primeira execução; +1 após a revisão) | — |
| Prova negativa | 24/10/2026 | Local | ✅ 5 falhas detectadas | Saída acima |
| T-13 | 24/10/2026 | Local (html-validate 11.17.0) | ✅ após corrigir 8 botões sem `type` | — |
| T-14 | 24/10/2026 | Local (Node) | ✅ | — |
| Push direto na `main` | 24/10/2026 | GitHub | ✅ Recusado (GH013) | Saída acima |
| T-01 a T-15 | 24/10/2026 | CI no PR da implantação | Ver execução | [Actions → CI](https://github.com/MarcellinhoHM/PortfolioHUB/actions/workflows/ci.yml) |
| T-16, T-17 | 24/10/2026 | Publicação após o merge do PR #9 | ✅ Testes, publicação e teste de fumaça (páginas 200, 404 personalizado, `github.json` 200) | [Execução 40118746308](https://github.com/MarcellinhoHM/PortfolioHUB/actions/runs/40118746308) |
| T-15 (histórico completo) | 24/10/2026 | CI manual na `main` | ✅ gitleaks: 24 commits varridos, nenhum vazamento | [Execução 40118913581](https://github.com/MarcellinhoHM/PortfolioHUB/actions/runs/40118913581) |
| Tag `v2.0.0` | 24/10/2026 | GitHub | ✅ Ruleset de tags ativa: "Bypassed rule violations… creations being restricted" (só o admin passa) | Saída do `git push` |
| Painel mostra a versão nova | 24/10/2026 | Produção | ❌ Continuou em v1.1.0: a publicação da Release usou o mesmo commit e o Pages manteve o conteúdo anterior | Corrigido na v2.0.1 |
| M-01 a M-05, M-11 | 24/10/2026 | Chrome (headless) em 390 e 1280 px | ✅ | Capturas no PDF da entrega |

---

[← Voltar para a documentação da implantação](README.md)
