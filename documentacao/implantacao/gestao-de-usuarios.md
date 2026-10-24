# Gestão de Usuários e Controle de Acesso

Seção 3 (primeira parte) da Entrega Final: quem tem acesso ao PortfolioHUB, com qual permissão, e como isso aparece no site.

## Sumário

1. [Política de acesso](#1-política-de-acesso)
2. [Limitação conhecida (conta pessoal)](#2-limitação-conhecida-conta-pessoal)
3. [Papéis](#3-papéis)
4. [Mecanismos que garantem os papéis](#4-mecanismos-que-garantem-os-papéis)
5. [Inventário de acessos](#5-inventário-de-acessos)
6. [Concessão e revogação](#6-concessão-e-revogação)
7. [Integração com o site](#7-integração-com-o-site)
8. [Como verificar](#8-como-verificar)

## 1. Política de acesso

- **Menor privilégio:** acesso de escrita só com necessidade contínua e prazo definido.
- **Contribuições pontuais** entram por fork + Pull Request, sem convite.
- **Nenhuma alteração na `main` sem Pull Request**, inclusive do mantenedor.
- **Tags de versão (`v*`) e Releases** são exclusivas do mantenedor.
- **Revisão deste inventário** a cada Release e ao fim de cada acesso temporário.

Alinhado a: CIS Control 6 (gestão de acesso), ISO/IEC 27001 A.5.15 e A.5.18 (controle e direitos de acesso), NIST CSF 2.0 PR.AA (identidade e controle de acesso). O projeto se alinha a essas referências; não há certificação.

## 2. Limitação conhecida (conta pessoal)

O repositório está na conta pessoal `MarcellinhoHM` (decisão D2 do [plano](plano-de-implantacao.md#4-premissas-restrições-e-decisões), para não quebrar as URLs já divulgadas). Nesse tipo de conta:

| Recurso | Conta pessoal | Organization |
|---|---|---|
| Papéis Read / Triage / Write / Maintain / Admin | ❌ Todo colaborador recebe escrita | ✅ |
| Teams | ❌ | ✅ |
| Exigir 2FA de quem tem acesso | ❌ | ✅ |
| Rulesets, CODEOWNERS, bypass por papel | ✅ | ✅ |
| Contribuição por fork sem acesso concedido | ✅ | ✅ |

**Consequência:** quem limita o que cada pessoa consegue fazer são as **rulesets** e o **CODEOWNERS**, não o convite. Se o projeto passar a ter mais de um mantenedor, o plano é migrar para uma Organization.

## 3. Papéis

| Papel | Quem | Como obtém | Pode | Não pode |
|---|---|---|---|---|
| **Visitante / contribuidor externo** | Qualquer pessoa | Repositório público | Ler, abrir issues, fazer fork e abrir PR | Push no repositório. Workflows do PR dele só rodam após aprovação |
| **Colaborador** | Pessoa convidada | Convite em *Settings → Collaborators* | Criar branches, abrir e comentar PRs, gerenciar issues e labels | Mesclar na `main` sem aprovação do code owner; criar, alterar ou apagar tags `v*`; mudar configurações |
| **Mantenedor (admin)** | @MarcellinhoHM | Dono do repositório | Tudo, inclusive mesclar com bypass **somente dentro de um PR** | Push direto na `main` |
| **Automação** | Dependabot e GitHub Actions | Configuração | Dependabot abre PRs; Actions testa e publica | Escrever no repositório: o token padrão é somente leitura |

> **Sobre o bypass do mantenedor:** o GitHub não permite aprovar o próprio PR. Enquanto houver um único mantenedor, os PRs dele são mesclados marcando *bypass rules*, o que só é possível dentro de um PR e fica registrado nele. O push direto continua bloqueado.

### Regra de uso do bypass

A revisão final com o guia apontou que o bypass dispensa **também** os checks obrigatórios. Por isso vale a regra:

1. **Bypass só com os checks "Testes do site" e "Varredura de segredos" verdes** no PR.
2. **Justificativa no PR** (por exemplo: "mantenedor único; checks verdes").
3. Nunca usar bypass para contornar um check vermelho: corrigir o problema no próprio PR.

### Evolução da regra de revisão

| Opção | Configuração | Quando |
|---|---|---|
| **Atual** | 1 aprovação + code owner, com bypass do admin só via PR e a regra acima | Mantenedor único |
| **A** | Convidar um colaborador (Write) e incluí-lo no CODEOWNERS para as áreas comuns; áreas sensíveis continuam só com o mantenedor | Quando houver um colaborador que possa revisar |
| **B** | 0 aprovações, sem exigir code owner e **sem bypass**: os checks passam a valer sempre, inclusive para o mantenedor | Alternativa recomendada pelo guia enquanto não houver um segundo revisor |

## 4. Mecanismos que garantem os papéis

### Ruleset "Proteção da main" (branch padrão)

| Regra | Efeito |
|---|---|
| Pull Request obrigatório, com 1 aprovação | Nada entra na `main` sem PR aprovado |
| Revisão obrigatória do code owner | O responsável definido no CODEOWNERS precisa aprovar |
| Aprovação descartada após novo push | Um commit novo depois da aprovação exige nova revisão |
| Aprovação do último push por outra pessoa | Quem fez o último push não pode ser quem aprova |
| Conversas resolvidas | Comentários de revisão precisam ser resolvidos antes do merge |
| Checks obrigatórios: "Testes do site" e "Varredura de segredos" | O CI precisa passar |
| Bloqueio de force push e de exclusão | Ninguém reescreve o histórico nem apaga a `main` |
| Bypass: papel Admin, **somente via PR** | O mantenedor mescla os próprios PRs, mas nunca faz push direto |

### Ruleset "Tags de versão" (`refs/tags/v*`)

Bloqueia criação, alteração e exclusão de tags de versão, com bypass só para o Admin. Isso importa porque o ambiente `github-pages` aceita publicar a partir de tags `v*` (rollback).

### CODEOWNERS

Arquivo [`.github/CODEOWNERS`](../../.github/CODEOWNERS): o mantenedor revisa tudo, e as áreas sensíveis (`/.github/`, `/scripts/`, `/ferramentas/`, `SECURITY.md`, `documentacao/implantacao/`) continuam exclusivas dele mesmo quando houver outros revisores.

### Actions

- Token padrão somente leitura; cada job pede só a permissão de que precisa.
- Workflows de PRs vindos de forks exigem aprovação para qualquer contribuidor externo.
- Nenhum workflow usa `pull_request_target`.
- Automações não podem aprovar Pull Requests.

## 5. Inventário de acessos

Levantado em 24/10/2026 com a GitHub CLI:

```bash
R=MarcellinhoHM/PortfolioHUB
gh api repos/$R/collaborators --jq '.[] | "\(.login) (\(.role_name))"'   # MarcellinhoHM (admin)
gh api repos/$R/invitations --jq length                                   # 0
gh api repos/$R/keys --jq length                                          # 0 deploy keys
gh api repos/$R/hooks --jq length                                         # 0 webhooks
```

| Usuário | Papel | Motivo | Concedido em | Válido até | 2FA confirmado | Status |
|---|---|---|---|---|---|---|
| @MarcellinhoHM | Mantenedor (admin) | Dono do repositório | — | — | Conferir | Ativo |

Inventário da **conta** (feito pelo mantenedor, nas configurações da conta do GitHub):

- [ ] *Password and authentication*: 2FA ativo (app TOTP ou passkey) e códigos de recuperação guardados fora do computador
- [ ] *SSH and GPG keys*: só chaves em uso
- [ ] *Applications* (OAuth Apps e GitHub Apps): revogar o que não é usado
- [ ] *Developer settings → Personal access tokens*: apagar tokens sem uso; os restantes com validade
- [ ] *Sessions*: encerrar sessões desconhecidas

## 6. Concessão e revogação

### Concessão (onboarding)

- [ ] Necessidade e prazo definidos
- [ ] 2FA confirmado pela pessoa (em conta pessoal não dá para exigir; registrar a confirmação)
- [ ] [CONTRIBUTING.md](../../CONTRIBUTING.md) e [CODE_OF_CONDUCT.md](../../CODE_OF_CONDUCT.md) lidos
- [ ] Convite enviado: `gh api -X PUT repos/MarcellinhoHM/PortfolioHUB/collaborators/<usuario>` (expira em 7 dias)
- [ ] Linha adicionada ao inventário acima

### Revogação (offboarding)

- [ ] Acesso removido: `gh api -X DELETE repos/MarcellinhoHM/PortfolioHUB/collaborators/<usuario>`
- [ ] Branches abertas revisadas ou removidas
- [ ] Inventário atualizado (status "Revogado" e data)

## 7. Integração com o site

O site **não tem login**, e não deve ter: qualquer verificação feita no navegador pode ser burlada. A integração mostra publicamente como o acesso funciona:

- Seção **Implantação → Equipe e permissões** do site: contribuidores vindos da API do GitHub (avatar, perfil, número de commits) e um resumo fiel da situação atual (um mantenedor; contribuições externas por fork e PR; ninguém faz push direto).
- Usa a lista de **contribuidores** (pública), não a de colaboradores (quem tem acesso), que não deve ser exposta (LGPD).
- Links para CONTRIBUTING, CODE_OF_CONDUCT e esta política na documentação.

## 8. Como verificar

| Teste | Como | Resultado esperado |
|---|---|---|
| Push direto na `main` | `git push origin <commit>:refs/heads/main` | ❌ Recusado (GH013), ver [testes-e-lancamento.md](testes-e-lancamento.md#push-direto-na-main) |
| PR próprio | Abrir um PR | "Review required"; merge só marcando *bypass rules* |
| CODEOWNERS válido | `gh api repos/MarcellinhoHM/PortfolioHUB/codeowners/errors` | `{"errors":[]}` |
| Inventário consistente | Comparar `gh api .../collaborators` com a seção 5 | Listas iguais |
| Rulesets | *Settings → Rules → Rulesets* | "Proteção da main" e "Tags de versão" ativas |

---

[← Voltar para a documentação da implantação](README.md)
