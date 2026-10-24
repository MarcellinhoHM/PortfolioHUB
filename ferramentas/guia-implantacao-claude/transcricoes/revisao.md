# Trilha de Implantação do PortfolioHUB — etapa "revisao"

- Data: 24/10/2026 14:19
- Modelo: `claude-opus-5-5` (esforço `medium`)
- Configuração do guia: [`system_prompt.md`](../system_prompt.md)

## Prompt 1: revisão da implantação concluída

Implementei a implantação seguindo a trilha. Em anexo estão o resumo do que foi feito (configurações do GitHub e arquivos do repositório) e o README atualizado. Revise como guia: o que está adequado, o que falta ou tem risco, e o que você ajustaria antes de declarar a versão de produção v2.0.0.

- Anexo: `resumo-da-implantacao.md`
- Anexo: `README.md`

### Resposta ao Prompt 1

# Revisão da implantação do PortfolioHUB v2.0.0

## Veredito

A base está sólida e acima do esperado para um site estático: rulesets, CI obrigatório, publicação por ambiente, Actions restritas e CSP sem `unsafe-inline`. Antes de criar a tag v2.0.0, porém, há **quatro bloqueios**:

1. Confirmar o 2FA na conta.
2. Resolver a contradição entre a regra de revisão e a equipe de uma pessoa só.
3. Ajustar o aviso de privacidade.
4. Ordenar o lançamento para que o site mostre a v2.0.0 de fato.

Há também algumas inconsistências na documentação que a banca pode notar.

---

## 1. O que está adequado

| Área | Por que está bom |
|---|---|
| Ruleset da `main` + checks obrigatórios | O push direto recusado (GH013) prova a regra na prática. |
| Ruleset de tags `v*` | Protege a integridade das versões publicadas. |
| Ambiente `github-pages` restrito | Uma branch qualquer não consegue publicar em produção. |
| Actions: token somente leitura, sem aprovar PRs, lista de permitidas, aprovação para forks | Cobre os principais vetores de ataque à cadeia de CI. |
| Busca de segredos no `_site` antes de publicar | É uma segunda barreira além do gitleaks no repositório. |
| `github.js` só com `textContent` e links validados | Neutraliza XSS a partir de dados da API, como descrições de repositórios. |
| Prova negativa (5 violações detectadas) | Mostra que os testes realmente falham quando devem. |
| `package-lock.json` com versão travada | Garante builds reproduzíveis. |

---

## 2. Bloqueios antes da v2.0.0

### B1. 2FA da conta (crítico)

Você é o único admin de um repositório em produção. Sem 2FA, todas as outras proteções caem junto com a senha.

- Confirme em *Settings (da conta) → Password and authentication → Two-factor authentication*. Prefira app TOTP ou passkey e guarde os recovery codes fora do computador.
- Faça também o inventário da **conta**, não só do repositório. O inventário atual (0 deploy keys, 0 webhooks) cobre apenas o repo:
  - *Settings → SSH and GPG keys*: remova chaves antigas.
  - *Settings → Applications* (abas Authorized OAuth Apps e Installed GitHub Apps): revogue o que não usa.
  - *Settings → Developer settings → Personal access tokens*: apague tokens sem uso e dê validade aos restantes.
  - *Settings → Sessions*: encerre sessões desconhecidas.

### B2. Regra de revisão incompatível com uma equipe de uma pessoa

O ruleset exige 1 aprovação e revisão do code owner. O CODEOWNERS diz que "o mantenedor revisa tudo". Como ninguém aprova o próprio PR, **todo PR seu só entra por bypass**.

O risco mais sério: no ruleset, o bypass dispensa **também os checks obrigatórios**. Na prática, hoje você conseguiria fazer merge com o CI vermelho.

Escolha uma das opções e documente em `gestao-de-usuarios.md`:

| Opção | Configuração | Quando usar |
|---|---|---|
| **A (recomendada)** | Convidar um colega com papel **Write** (*Settings → Collaborators → Add people*). No CODEOWNERS: `* @MarcellinhoHM @colega` para o geral; áreas sensíveis (`.github/`, `scripts/`, `SECURITY.md`) só `@MarcellinhoHM`. | Se o colega aceitar antes da entrega. Mudanças suas em áreas sensíveis continuam por bypass, como exceção documentada. |
| **B** | Aprovações = 0 e sem exigência de code owner até haver um segundo membro. Manter checks, conversas resolvidas, sem force push e sem exclusão. Remover o bypass. | Se não houver colega a tempo. É mais honesto e mais seguro que o bypass rotineiro, porque os checks passam a valer sempre. |

Seja qual for a opção, registre a regra: **"bypass só com checks verdes, e justificado no PR"**.

Para validar:

```bash
gh api repos/MarcellinhoHM/PortfolioHUB/rulesets --jq '.[] | {id, name}'
gh api repos/MarcellinhoHM/PortfolioHUB/rulesets/<ID> --jq '.bypass_actors, .rules[].type'
gh api repos/MarcellinhoHM/PortfolioHUB/collaborators --jq '.[] | {login, role_name}'
```

### B3. Aviso de privacidade impreciso (LGPD, transparência)

"Sem coleta de dados" vale para você, mas não para terceiros:

- O **GitHub Pages** registra o IP de quem acessa (política de privacidade do GitHub).
- O `github.js` chama **`api.github.com`** a partir do navegador do visitante quando cai na reserva ao vivo.

Sugestão de texto:

> "Este site não usa cookies nem coleta dados pessoais. Ele é hospedado no GitHub Pages e pode consultar a API pública do GitHub; o GitHub pode registrar dados técnicos de acesso (como o endereço IP) conforme a [Declaração de Privacidade do GitHub](https://docs.github.com/pt/site-policy/privacy-policies/github-general-privacy-statement)."

Para validar, abra o DevTools → *Network*, carregue o site e confira que os únicos domínios externos são os citados no aviso e permitidos no `connect-src` da CSP.

### B4. Ordem do lançamento: o site precisa mostrar a v2.0.0

A seção Implantação mostra a "versão em produção" a partir dos dados gerados no build. Se a tag for criada depois do último deploy, o site continua exibindo **v1.1.0** até a execução diária. Faça nesta ordem:

```bash
# 1. PR final mergeado, CI verde, main atualizada
git switch main && git pull --ff-only

# 2. Tag anotada (cai no bypass de admin do ruleset de tags)
git tag -a v2.0.0 -m "v2.0.0 — Implantação em produção (Entrega Final)"
git push origin v2.0.0

# 3. Release a partir da tag existente
gh release create v2.0.0 --verify-tag --title "v2.0.0 — Implantação" --notes-file notas-v2.0.0.md

# 4. Republicar para o site refletir a versão
gh workflow run deploy-pages.yml --ref main
gh run watch
```

Para tornar isso automático, adicione `release: types: [published]` ou `push: tags: ['v*']` ao `deploy-pages.yml`. O ambiente já aceita tags `v*`. Se não for usar tags para publicar, retire `v*` da política do ambiente, porque é superfície de ataque sem uso.

---

## 3. Recomendados (não bloqueiam, mas fortalecem)

| # | Ajuste | Por quê / referência | Como validar |
|---|---|---|---|
| R1 | Fixar Actions por **SHA de commit** (`uses: actions/checkout@<sha40> # v4.x.x`) | Uma tag de Action pode ser movida por terceiros (OWASP Top 10 A08, Scorecard *Pinned-Dependencies*). O Dependabot atualiza os SHAs. | `grep -rn "uses:" .github/workflows \| grep -vE "@[0-9a-f]{40}"` deve retornar vazio |
| R2 | `permissions:` mínimas **por job**. Só o job de deploy deve ter `pages: write` e `id-token: write`. | Menor privilégio (CIS Software Supply Chain). | Ler os YAMLs; `gh api repos/MarcellinhoHM/PortfolioHUB/actions/permissions/workflow` |
| R3 | Varredura do **histórico completo** uma vez (o CI normalmente só vê o diff) | Segredos antigos continuam públicos no histórico. | `gitleaks git -v` (v8.19+) ou `gitleaks detect -v`; no CI, `fetch-depth: 0` |
| R4 | Revisar **notebooks e transcrições do Claude** | Saídas de células e transcrições podem conter chave, caminhos locais ou dados pessoais. | `grep -rn "sk-ant-" .`; `jupyter nbconvert --clear-output --inplace projetos-academicos/bootcamp-claude-api/*.ipynb` |
| R5 | Montar o `_site` por **lista de permissões** (só `index.html`, `404.html`, `sitemap.xml`, `assets/`, `documentacao/slides/`...) em vez de copiar o repo | Publica só o necessário. `tests/`, `scripts/` e `ferramentas/` não precisam estar no site. | Baixar o artefato do run e listar o conteúdo |
| R6 | Testar o **404 em profundidade** | Em sites de projeto, o 404 é servido em qualquer caminho. Caminhos relativos quebram o CSS. Use `/PortfolioHUB/assets/...`. | Abrir `https://marcellinhohm.github.io/PortfolioHUB/a/b/c` e conferir se o estilo carrega; `curl -sI` deve retornar 404 |
| R7 | Documentar os **limites da CSP por `<meta>`** | `frame-ancestors`, `report-uri` e `sandbox` são **ignorados** em meta, e o Pages não permite cabeçalhos. A proteção contra clickjacking não existe; registre como risco aceito (baixo impacto: site sem login nem formulários). | Seção "Riscos aceitos" em `politica-de-seguranca.md` |
| R8 | Conferir o `dependabot.yml` | `directory` do pip precisa apontar para `/projetos-academicos/bootcamp-claude-api`. Se apontar para `/`, nada é monitorado. | *Insights → Dependency graph → Dependabot*: os três ecossistemas devem aparecer sem erro |
| R9 | Rodar o **OpenSSF Scorecard** uma vez e registrar a nota | Dá uma métrica externa para a apresentação, mesmo sem corrigir tudo. | Workflow `ossf/scorecard-action` ou CLI local com token em variável de ambiente, nunca no repo |
| R10 | Ensaiar o **rollback** do plano | Um plano sem ensaio não comprova nada (NIST CSF, função *Recover*). | `git revert` de um PR trivial → deploy → site volta; registrar o run |

Observações menores:

- Workflows agendados em repositório público são **desativados após 60 dias sem atividade**. Anote isso no plano de manutenção.
- O `sitemap.xml` de um site de projeto não é descoberto automaticamente, porque o `robots.txt` precisaria estar na raiz `marcellinhohm.github.io`. Envie pelo Google Search Console, se quiser indexação.

---

## 4. Inconsistências na documentação

| Onde | Problema | Ajuste |
|---|---|---|
| README, etapa 5 | "CI com **18** verificações" contra "**13** testes" no resumo | Detalhe a conta (13 unittest + html-validate + node --check + gitleaks + ...) ou use um único número nos dois arquivos. |
| README, Segurança | "Só recebe mudanças por PR com revisão do responsável" | Ajuste conforme a opção escolhida em B2. Hoje a revisão é dispensada por bypass. |
| Resumo, Verificações | Não há linha sobre o deploy e o teste de fumaça em produção | Adicione o link do run do `deploy-pages.yml` com o teste de fumaça verde. |
| `ia-guia.md` | Precisa explicar a troca Gemini → Claude | Uma frase: o enunciado cita o Gemini; este projeto usou o Claude, com a configuração e as transcrições em `ferramentas/guia-implantacao-claude/`. |
| Pendências | O 2FA aparece como pendência | Precisa virar ✅ antes da tag. |

---

## 5. Normas, ligadas ao que você já fez

| Referência | Ação concreta no PortfolioHUB |
|---|---|
| OWASP Top 10 (A05 / A06 / A08) | CSP restritiva; Dependabot; Actions fixadas por SHA |
| LGPD (transparência) | Aviso de privacidade corrigido (B3) |
| NIST CSF 2.0 | *Govern*: SECURITY.md · *Protect*: rulesets e 2FA · *Detect*: secret scanning e CodeQL · *Recover*: rollback ensaiado |
| CIS Software Supply Chain | 2FA, `main` protegida, menor privilégio no token |
| OpenSSF Scorecard | Nota registrada como linha de base para evolução |

A ISO/IEC 27001 só cabe como inspiração (inventário de acessos, política escrita). Não afirme conformidade.

---

## Próximos passos

1. Ativar ou confirmar o 2FA e limpar chaves, tokens e apps da conta (B1).
2. Decidir entre a opção A e a B do ruleset, ajustar o CODEOWNERS e documentar a regra do bypass (B2).
3. Corrigir o aviso de privacidade e conferir a aba Network (B3).
4. Aplicar R1, R2 e R4 num PR `chore/endurecimento-pre-v2`.
5. Corrigir as inconsistências do README e do resumo.
6. Executar a sequência de lançamento (B4) e só então gravar o vídeo.

## Como comprovar

- Captura de *Password and authentication* mostrando 2FA ativo, sem expor recovery codes.
- Saída de `gh api .../rulesets/<ID>` e de `gh api .../collaborators` no documento de usuários.
- Um PR com revisão real do colega (opção A) ou o ruleset sem bypass com um PR barrado por check vermelho (opção B).
- Saída vazia do `grep` de Actions sem SHA e relatório do `gitleaks` no histórico completo sem achados.
- Link da Release v2.0.0, link do run de deploy com teste de fumaça verde e captura do site exibindo **v2.0.0** na seção Implantação.
- Nota do Scorecard e link do run do rollback ensaiado, se feitos.

---

## Prompt 2: análise e sugestões de melhoria do portfólio

Agora avalie o meu portfólio como um recrutador da área de tecnologia avaliaria. Em anexo estão a página principal do site (HTML) e o índice de projetos. Aponte pontos fortes e sugestões de melhoria para o conteúdo, a apresentação dos projetos e o README.

- Anexo: `index.html`
- Anexo: `README.md`
- Anexo: `README.md`

### Resposta ao Prompt 2

# Avaliação do PortfolioHUB pelo olhar de um recrutador de tecnologia

## Primeira impressão em 30 segundos

Um recrutador costuma passar de 30 a 60 segundos na primeira leitura. Ele procura três respostas: **quem é você e o que busca**, **o que você sabe fazer de verdade** e **qual é o seu melhor trabalho**. Hoje o site responde bem à segunda e mal à primeira e à terceira:

- **Quem é / o que busca:** o hero diz "Estudante de Ciência da Computação" e "gosto de transformar ideias em código". Isso é genérico, e não há objetivo (estágio? área?), instituição, semestre nem forma direta de contato.
- **Melhor trabalho:** seu projeto mais forte é **o próprio PortfolioHUB** (CI/CD, rulesets, CSP, testes, publicação por ambiente). Mas ele não aparece como projeto. Está diluído na seção "Implantação", com cara de entrega de disciplina ("etapas 1 a 6").

---

## 1. Pontos fortes

| O que o recrutador nota | Por que conta a favor |
|---|---|
| Site próprio, rápido, sem framework, com HTML validado | Mostra fundamentos sólidos de front-end. |
| Badges de CI e publicação funcionando | Prova de que você entende integração contínua, coisa rara em júnior. |
| CSP, `rel="noopener"`, `textContent`, nenhum segredo no front | Cuidado com segurança que um avaliador técnico percebe ao abrir o código. |
| Acessibilidade básica: `label` com `sr-only`, `role="status"`, `aria-live`, `<noscript>` | Detalhe de qualidade que poucos portfólios têm. |
| Projeto com API do Claude em destaque | IA aplicada é um tema valorizado, e ele está no lugar certo. |
| Aviso de privacidade já cita GitHub e Google Fonts | O ajuste B3 da revisão anterior foi bem aplicado. |
| Histórico com SemVer, CHANGELOG e Conventional Commits | Indica disciplina de trabalho em equipe. |

---

## 2. Melhorias prioritárias (maior impacto primeiro)

### P1. Transformar o PortfolioHUB no projeto principal

Crie um card como **primeiro** item de "Projetos", escrito como estudo de caso e não como entrega:

```html
<article class="card featured">
  <div class="tag-row"><span class="tag cat">Destaque · DevSecOps</span><span class="tag">GitHub Actions</span><span class="tag">JavaScript</span><span class="tag">Python</span></div>
  <h3>PortfolioHUB — site estático com CI/CD e segurança de produção</h3>
  <p>
    Este site. Publicação automatizada no GitHub Pages só após testes (13 testes Python, validação de HTML,
    varredura de segredos), main protegida por rulesets, Content Security Policy sem <code>unsafe-inline</code>,
    Dependabot e CodeQL. Dados do GitHub gerados no build, com a API ao vivo como reserva.
  </p>
  <div class="links">
    <a href="https://github.com/MarcellinhoHM/PortfolioHUB" target="_blank" rel="noopener">Código →</a>
    <a href="https://github.com/MarcellinhoHM/PortfolioHUB/actions" target="_blank" rel="noopener">Pipelines →</a>
    <a href="#implantacao">Como foi implantado →</a>
  </div>
</article>
```

### P2. Reescrever o hero com objetivo claro

Sugestão (troque os colchetes pelos seus dados reais):

> **Marcello Montella**
> Estudante de Ciência da Computação ([Instituição], [Xº] semestre) · Desenvolvimento Web e IA aplicada
> Busco **[estágio / primeira oportunidade] em [desenvolvimento / DevOps / dados]**. Construo projetos com HTML/CSS/JS, Python e Java, e levo boas práticas de produção (testes, CI/CD, segurança) até para projetos pessoais.

Botões: **LinkedIn** · **GitHub** · **Currículo (PDF)**, com `assets/docs/curriculo-marcello.pdf` sem telefone nem endereço. Se quiser e-mail, use um profissional dedicado, ciente de que endereços públicos recebem spam.

### P3. Reescrever os cards no formato problema → o que fiz → resultado

Hoje os cards dizem **o que o projeto é**. O recrutador quer saber **o que você fez e aprendeu**. Use um modelo fixo:

| Elemento | Exemplo para o RPG de Terminal |
|---|---|
| Problema / objetivo | Praticar orientação a objetos em um jogo com regras de combate. |
| O que eu fiz | Hierarquia com classe abstrata `Character`, inventário, sistema de nível e HP/MP. |
| Destaque técnico | Polimorfismo para tipos de personagem; [testes JUnit, se adicionar]. |
| Link | Código · [GIF do terminal] |

Observações por projeto:

| Projeto | Ajuste sugerido |
|---|---|
| Bootcamp Claude | Troque "API de IA" por "Claude (Anthropic)". Mostre um resultado concreto, como um exemplo de tool use com entrada e saída. Mantenha as saídas dos notebooks sem chaves nem dados pessoais (item R4). |
| Ponto Eletrônico | Bom, porque tem demo. Adicione um print ou GIF no card. |
| Caixa Eletrônico (ATM) | Destaque a modularização (headers e arquivos separados) e adicione `Makefile`. |
| **Prova — Site Temático** | O nome "Prova" passa a ideia de exercício avaliativo. Renomeie pelo tema do site ou tire da seleção. |
| Programação Web | "Exercícios da disciplina" é o card mais fraco. Mova para a lista automática de repositórios ou destaque um único exercício interessante. |

### P4. Reduzir o peso das seções acadêmicas

A ordem atual (Implantação → Documentação → Slides → Versões) faz o recrutador rolar muito conteúdo de disciplina. Sugestão de ordem:

1. Hero
2. Sobre + Competências
3. **Projetos** (PortfolioHUB primeiro)
4. Repositórios
5. Contato
6. **"Como este site foi construído"**: reúne Implantação, Documentação, Slides e Versões dentro de `<details>`. Funciona sem JavaScript e não exige mudar a CSP.

A banca continua encontrando tudo, e o recrutador vê primeiro o que importa para ele.

### P5. Mostrar as competências reais

A lista "Ferramentas: Git · GitHub · VS Code" subestima o que você já entregou. Agrupe por área:

| Área | Itens |
|---|---|
| Linguagens | Python, JavaScript, Java, C, HTML/CSS |
| Práticas | Testes automatizados (unittest), CI/CD (GitHub Actions), Git Flow com PRs, SemVer |
| Segurança | CSP, secret scanning, Dependabot, CodeQL, rulesets |
| IA | API do Claude: system prompt, streaming, tool use |

### P6. Filtrar a lista de repositórios

A lista ao vivo mostra **todo** repositório público, inclusive forks e exercícios pequenos, o que dilui a seleção. No `github.js` (e no `scripts/gerar_dados_github.py`), filtre antes de renderizar:

```js
const visiveis = repos
  .filter(r => !r.fork && !r.archived && r.name !== 'MarcellinhoHM')
  .sort((a, b) => new Date(b.pushed_at) - new Date(a.pushed_at));
```

Ajuste também o texto da seção ("todo repositório público que eu criar aparece aqui") e inclua um teste que confirme a exclusão de forks.

---

## 3. Detalhes técnicos que um recrutador técnico notaria

| Item | Problema | Ajuste |
|---|---|---|
| **Sem `og:image`** | Ao compartilhar o link no LinkedIn, a prévia sai sem imagem. É justamente o canal do recrutador. | Crie `assets/img/og-image.png` (1200×630) e adicione `<meta property="og:image" content="https://marcellinhohm.github.io/PortfolioHUB/assets/img/og-image.png">` e `<meta property="og:image:alt" content="...">`. Valide no LinkedIn Post Inspector. |
| **Google Fonts externo** | Envia o IP do visitante ao Google (LGPD), adiciona dois domínios à CSP e atrasa o carregamento. | Hospede a fonte Inter (`.woff2`) em `assets/fonts/` com `@font-face` e `font-display: swap`, e inclua a licença OFL. Remova os `preconnect`, troque para `font-src 'self'` e `style-src 'self'` e atualize o aviso de privacidade. |
| **Classe `.reveal`** | Se o CSS deixar `.reveal` com `opacity: 0` desde o início, quem tem JavaScript desativado ou bloqueado vê uma página quase vazia. | Esconda apenas quando o JS marcar o `<html>` (ex.: `.js .reveal { opacity: 0 }`) e respeite `prefers-reduced-motion`. |
| **Botão de menu** | Não tem `aria-expanded` nem `aria-controls`. | Adicione `aria-controls="nav" aria-expanded="false"` e alterne o valor no `main.js`. |
| **Versão fixa no HTML** | Rodapé e linha do tempo dizem "v2.0.0" antes de a tag existir. | Publique isso junto com a release (sequência B4) ou leia a versão do `github.json` gerado no build. |
| **Texto da equipe** | Promete revisão por CODEOWNERS e colaboradores com Triage ou Write, mas hoje a equipe é só você. | Ajuste conforme a opção A ou B da revisão anterior. Recrutador técnico percebe quando o texto promete mais do que o repositório mostra. |
| **Inconsistência de tecnologias** | "Prova" aparece como "HTML, Bootstrap" no site e como "HTML, Bootstrap, JS" no índice acadêmico. | Unifique. A lista de projetos existe em três lugares (README principal, `index.html` e índices), então vale um teste simples que compare os nomes. |

---

## 4. README (repositório e perfil)

**README principal:** a primeira tela fala de "Implantação (v2.0.0)… Entrega Final", que é linguagem de disciplina. Sugestão:

1. Logo abaixo dos badges, uma frase de valor: *"Portfólio pessoal publicado com CI/CD, testes e segurança de produção — HTML/CSS/JS puros."*
2. Um **print ou GIF do site**, que é o que mais prende atenção no GitHub.
3. Uma seção **"Destaques técnicos"** com 4 ou 5 marcadores (pipeline, CSP, rulesets, dados gerados no build, testes).
4. A tabela da Entrega Final vai para `documentacao/implantacao/README.md`, com um link no README principal.

**Índices de projetos:** estão claros e o passo a passo para adicionar projetos mostra método. Ganham com uma coluna "Destaque" (o que você aprendeu ou resolveu) e com prints.

**Perfil do GitHub (onde o recrutador costuma chegar primeiro):**

- Crie o README de perfil (repositório `MarcellinhoHM/MarcellinhoHM`) com duas ou três linhas, a stack e o link do site.
- Fixe 4 a 6 repositórios (*Customize your pins*), com o PortfolioHUB primeiro.
- Preencha descrição, *topics* e o campo *Website* de cada repositório fixado.
- Leve as práticas do PortfolioHUB para os outros repositórios: README com "como executar", e um CI simples (`javac`/JUnit no RPG, `gcc -Wall -Werror` no ATM). Isso mostra que o padrão é seu, não apenas da disciplina.

---

## Próximos passos

1. Reescrever o hero com objetivo e instituição e adicionar o botão de currículo em PDF (P2).
2. Criar o card de estudo de caso do PortfolioHUB e reescrever os cards no formato problema → o que fiz → resultado (P1, P3).
3. Reorganizar as seções e agrupar o conteúdo acadêmico em `<details>` (P4).
4. Abrir um PR `feat/site-recrutador` com `og:image`, fonte local, correção do `.reveal`, `aria-expanded` e filtro de forks, mantendo os testes verdes.
5. Atualizar o README principal com print e destaques, e montar o perfil do GitHub com repositórios fixados.

## Como comprovar

- Capturas de tela **antes e depois** do hero e da seção Projetos, anexadas ao PR.
- Print do LinkedIn Post Inspector mostrando a prévia com imagem.
- Aba *Network* do DevTools sem requisições a `fonts.googleapis.com` e `fonts.gstatic.com`, e CSP atualizada no diff.
- Site aberto com JavaScript desativado e todo o conteúdo visível.
- Relatório do Lighthouse (Desempenho, Acessibilidade, SEO) antes e depois.
- Print do perfil do GitHub com o README de perfil e os repositórios fixados.

---

