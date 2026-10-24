# Política de Segurança — PortfolioHUB

| Campo | Valor |
|---|---|
| Responsável | Marcello Augusto Hesketh Montella (@MarcellinhoHM) |
| Versão | 1.0 (24/10/2026) |
| Revisão | A cada Release maior e, no mínimo, a cada 6 meses |
| Política pública de relato | [SECURITY.md](../../SECURITY.md) |

Seção 3 (segunda parte) da Entrega Final. A estrutura (controles com ID, rastreáveis até o teste) foi proposta pelo guia (Claude) no prompt 9 da [trilha](../../ferramentas/guia-implantacao-claude/transcricoes/trilha.md) e aplicada ao que de fato foi implementado.

> O projeto se **alinha** às práticas de OWASP, OpenSSF, NIST CSF, ISO/IEC 27001, CIS e LGPD. Não há certificação em nenhuma delas.

## Sumário

1. [Objetivo e escopo](#1-objetivo-e-escopo)
2. [Ativos e ameaças](#2-ativos-e-ameaças)
3. [Princípios](#3-princípios)
4. [Controles](#4-controles)
5. [Gestão de vulnerabilidades](#5-gestão-de-vulnerabilidades)
6. [Resposta a incidentes](#6-resposta-a-incidentes)
7. [Riscos aceitos](#7-riscos-aceitos)
8. [Mapeamento para as referências](#8-mapeamento-para-as-referências)

## 1. Objetivo e escopo

Proteger a integridade do código e do site, as credenciais do mantenedor e a privacidade de quem visita ou contribui.

**Escopo:** conta GitHub do mantenedor, repositório `PortfolioHUB`, workflows do GitHub Actions, site no GitHub Pages, o projeto Python com a API do Claude e a ferramenta do guia de implantação.

## 2. Ativos e ameaças

| Ativo | Ameaça principal | Controles |
|---|---|---|
| Conta GitHub do mantenedor | Tomada de conta (phishing, senha vazada) | CON-01 a CON-04 |
| Branch `main` e tags `v*` | Alteração não autorizada, PR malicioso | REP-01, REP-02, REP-07, ACT-05 |
| Chave da API do Claude | Vazamento em commit, notebook ou site | REP-03, REP-08, ACT-06, SITE-07, DAD-03 |
| Pipeline (Actions) | Action comprometida, injeção em workflow | ACT-01 a ACT-04 |
| Dependências | Componente vulnerável | REP-04, REP-05 |
| Site publicado | XSS por dados externos, desfiguração | SITE-01 a SITE-07 |
| Dados pessoais | Exposição excessiva (LGPD) | DAD-01, DAD-02 |

## 3. Princípios

1. **Menor privilégio:** cada pessoa e cada automação recebem só o acesso necessário.
2. **Nenhum segredo no repositório ou no site:** segredos só no `.env` local.
3. **Toda mudança passa por Pull Request**, com verificações automáticas.
4. **Defesa em camadas:** prevenir (push protection, CSP), detectar (scanning, testes), conter (rulesets).
5. **Tudo verificável:** cada controle tem um teste ou uma evidência.

## 4. Controles

Legenda: ✅ implementado · 🔶 depende de ação do mantenedor na conta · ⏭️ próximo passo

### 4.1 Conta GitHub

| ID | Controle | Status | Verificação |
|---|---|---|---|
| CON-01 | 2FA com passkey ou app autenticador; códigos de recuperação guardados offline | 🔶 | *Settings → Password and authentication* mostra 2FA ativo |
| CON-02 | Commits com e-mail privado (`noreply` do GitHub) | ✅ | `git log --format=%ae` mostra `@users.noreply.github.com` |
| CON-03 | Tokens só *fine-grained* com validade; apps OAuth revisados | 🔶 | *Developer settings* e *Applications* sem itens sem uso |
| CON-04 | Commits assinados (SSH) e *vigilant mode* | ⏭️ | Commits com selo "Verified" |

### 4.2 Repositório

| ID | Controle | Status | Verificação |
|---|---|---|---|
| REP-01 | Ruleset "Proteção da main": PR com aprovação, code owner, checks obrigatórios, conversas resolvidas, sem force push e sem exclusão | ✅ | Push direto recusado (GH013) |
| REP-02 | CODEOWNERS com áreas sensíveis exclusivas do mantenedor | ✅ | `gh api .../codeowners/errors` vazio |
| REP-03 | Secret scanning e push protection | ✅ | *Settings → Advanced Security* |
| REP-04 | Dependabot: alertas, atualizações de segurança e de versão (`dependabot.yml` para Actions e pip) | ✅ | Aba *Dependabot* e PRs automáticos |
| REP-05 | CodeQL, configuração padrão | ✅ | *Security → Code scanning* |
| REP-06 | Relato privado de vulnerabilidades e `SECURITY.md` | ✅ | Botão *Report a vulnerability* |
| REP-07 | Ruleset "Tags de versão" (`v*`): só o Admin cria, altera ou apaga | ✅ | *Settings → Rules → Rulesets* |
| REP-08 | `.env` ignorado, `.env.example` versionado, saídas de notebook revisadas | ✅ | Teste `test_arquivo_env_nao_versionado` |

### 4.3 GitHub Actions

| ID | Controle | Status | Verificação |
|---|---|---|---|
| ACT-01 | `GITHUB_TOKEN` somente leitura por padrão; `pages: write` e `id-token: write` só no job de publicação | ✅ | `permissions:` nos workflows e *Settings → Actions* |
| ACT-02 | Actions fixadas por SHA do commit; Dependabot atualiza | ✅ | Nenhum `uses:` com tag solta |
| ACT-03 | Só Actions do GitHub, de criadores verificados e o gitleaks | ✅ | *Settings → Actions → General* |
| ACT-04 | Aprovação para workflows de forks; sem `pull_request_target`; nenhuma entrada não confiável interpolada em `run:`; `persist-credentials: false` | ✅ | Revisão dos workflows |
| ACT-05 | Ambiente `github-pages` restrito à `main` e às tags `v*` | ✅ | *Settings → Environments* |
| ACT-06 | Testes (inclui busca por padrões de chaves) antes de publicar; gitleaks no histórico completo em todo PR | ✅ | Jobs "Testes antes de publicar" e "Varredura de segredos" |
| ACT-07 | OpenSSF Scorecard semanal | ⏭️ | Resultado em *Code scanning* |

### 4.4 Site (GitHub Pages)

| ID | Controle | Status | Verificação |
|---|---|---|---|
| SITE-01 | HTTPS obrigatório | ✅ | *Settings → Pages → Enforce HTTPS* |
| SITE-02 | Content Security Policy por `<meta>` em todas as páginas, sem `unsafe-inline` e sem `unsafe-eval` | ✅ | Teste `test_toda_pagina_tem_csp_restritiva` e console sem violações |
| SITE-03 | `Referrer-Policy: strict-origin-when-cross-origin` | ✅ | Meta tag em todas as páginas |
| SITE-04 | DOM seguro: dados externos só via `textContent`, links validados (`https:`), sem `innerHTML` nem `eval` | ✅ | Teste `test_javascript_nao_usa_innerhtml_nem_eval` |
| SITE-05 | Nenhum script de terceiros (só CSS de fontes do Google) | ✅ | CSP `script-src 'self'` |
| SITE-06 | Links externos com `rel="noopener"` | ✅ | Teste `test_links_externos_com_noopener` |
| SITE-07 | Nenhum segredo no front-end; a API do Claude não é chamada pelo site | ✅ | Teste `test_nenhum_segredo_versionado` |

A CSP do `index.html`:

```text
default-src 'self'; script-src 'self'; style-src 'self' https://fonts.googleapis.com;
font-src https://fonts.gstatic.com; img-src 'self' data: https://avatars.githubusercontent.com https://github.com;
connect-src 'self' https://api.github.com; frame-src 'self'; object-src 'none'; base-uri 'self'; form-action 'none'
```

### 4.5 Dados e privacidade

| ID | Controle | Status | Verificação |
|---|---|---|---|
| DAD-01 | Minimização: só LinkedIn e GitHub como contato (sem telefone, endereço ou e-mail pessoal) | ✅ | Revisão do site |
| DAD-02 | Aviso de privacidade no site: sem cookies e sem coleta de dados; o que fica no navegador (tema e cache) | ✅ | Seção Contato do site |
| DAD-03 | Chave da API só no `.env` local, dedicada ao projeto e com limite de gastos | 🔶 | Console da Anthropic com limite configurado |

## 5. Gestão de vulnerabilidades

| Severidade (Dependabot, CodeQL, relato) | Prazo para corrigir ou mitigar |
|---|---|
| Segredo exposto | **Revogar imediatamente** (até 1 hora após a detecção) |
| Crítica / alta | Até 7 dias |
| Média | Até 30 dias |
| Baixa | Próxima versão |

Alerta descartado exige justificativa registrada no próprio alerta.

## 6. Resposta a incidentes

| Incidente | Conter | Erradicar | Recuperar |
|---|---|---|---|
| Segredo vazado | Revogar a chave no provedor | Remover do código e, se preciso, do histórico | Nova chave só no `.env` (rollback RB3 do [plano](plano-de-implantacao.md#9-plano-de-reversão-rollback)) |
| Conta comprometida | Trocar a senha, encerrar sessões, revogar tokens e chaves SSH | Revisar o *security log* e os commits recentes | Reconfigurar o 2FA e gerar novos códigos de recuperação |
| Site desfigurado ou quebrado | Identificar o commit | `git revert` por PR | Nova publicação ou publicação a partir da última tag (RB1) |
| Dependência vulnerável | Avaliar a exposição real | Atualizar (PR do Dependabot) | CI verde e nova publicação |

Depois de cada incidente: registro com data, causa, ações e lição aprendida no histórico desta política.

## 7. Riscos aceitos

| Risco | Motivo | Mitigação parcial |
|---|---|---|
| Sem cabeçalhos HTTP próprios (`frame-ancestors`, `X-Frame-Options`) | O GitHub Pages não permite configurá-los | CSP por `<meta>`; o site não tem formulários nem ações que mudem estado, então *clickjacking* tem impacto baixo |
| Fontes carregadas do Google Fonts | Simplicidade | Só CSS e fontes; nenhum script de terceiros. Alternativa: hospedar as fontes no próprio site |
| Mantenedor mescla os próprios PRs com bypass | O GitHub não permite autoaprovação | Bypass só dentro de PR, registrado; checks rodam em todo PR |
| Sem papéis granulares para colaboradores | Repositório em conta pessoal | Rulesets e CODEOWNERS limitam o que um colaborador consegue fazer |

## 8. Mapeamento para as referências

| Referência | Onde aparece neste projeto |
|---|---|
| OWASP Top 10 — A01 (controle de acesso) | REP-01, REP-02, REP-07, ACT-05 |
| OWASP Top 10 — A03 (injeção/XSS) | SITE-02, SITE-04 |
| OWASP Top 10 — A06 (componentes vulneráveis) | REP-04, REP-05, ACT-02 |
| OWASP Top 10 CI/CD Security Risks | ACT-01 a ACT-04 |
| OpenSSF Scorecard (Branch-Protection, Code-Review, Pinned-Dependencies, Token-Permissions, Security-Policy, SAST, Dependency-Update-Tool) | REP-01, REP-02, ACT-02, ACT-01, REP-06, REP-05, REP-04 |
| NIST CSF 2.0 (Identificar, Proteger, Detectar, Responder, Recuperar) | Seções 2, 4, 4.2/4.3, 6 e plano de rollback |
| ISO/IEC 27001 A.5.15 / A.5.18 / A.8.28 | Gestão de acesso ([gestao-de-usuarios.md](gestao-de-usuarios.md)) e codificação segura (SITE-04) |
| CIS Controls 6 e 16 | Gestão de acesso; segurança de software (CI, CodeQL) |
| LGPD (minimização, transparência) | DAD-01, DAD-02 |

---

[← Voltar para a documentação da implantação](README.md)
