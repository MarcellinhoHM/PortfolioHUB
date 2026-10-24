# IA como Guia da Implantação (Claude)

O enunciado da Entrega Final pede para "configurar o Google Gemini para guiar a trilha de implantação" e usá-lo como referência de boas práticas. Neste projeto, esse papel foi feito pelo **Claude**, da Anthropic.

## Sumário

1. [Por que o Claude](#1-por-que-o-claude)
2. [Como o guia foi configurado](#2-como-o-guia-foi-configurado)
3. [A trilha de prompts](#3-a-trilha-de-prompts)
4. [Registro de uso: recomendação, decisão e validação](#4-registro-de-uso-recomendação-decisão-e-validação)
5. [Equivalência com o enunciado (Gemini → Claude)](#5-equivalência-com-o-enunciado-gemini--claude)
6. [Regras e limites](#6-regras-e-limites)

## 1. Por que o Claude

- O projeto acadêmico do PortfolioHUB já é sobre a API do Claude ([bootcamp-claude-api](../../projetos-academicos/bootcamp-claude-api/)): usar a mesma IA como guia aproveita o SDK e a chave que já estavam configurados.
- O guia roda **pela API**, com um script versionado. Assim a configuração (instruções, prompts e anexos) e as respostas ficam no repositório, revisáveis por qualquer pessoa.

## 2. Como o guia foi configurado

Ferramenta: [`ferramentas/guia-implantacao-claude/`](../../ferramentas/guia-implantacao-claude/)

| Elemento | Configuração |
|---|---|
| Papel | [`system_prompt.md`](../../ferramentas/guia-implantacao-claude/system_prompt.md): "Guia de Implantação do PortfolioHUB", com o contexto do projeto, as 6 seções da entrega e as restrições (site estático, nada de segredos no front-end) |
| Formato das respostas | Português, passos concretos (`git`, `gh`, caminhos de menu), normas ligadas a ações práticas, riscos e validação; toda resposta termina com **Próximos passos** e **Como comprovar** |
| Contexto fornecido | PDFs do enunciado da Entrega Final e da entrega intermediária, enviados como anexos |
| Modelo | `claude-opus-5-5`, esforço `medium`, com cache de prompt e *fallback* do servidor |
| Execução | `python guia.py trilha --etapa trilha` (12 prompts) e `--etapa revisao` (2 prompts) |
| Registro | Transcrições em Markdown e JSON (com modelo e tokens de cada turno) em [`transcricoes/`](../../ferramentas/guia-implantacao-claude/transcricoes/) |

## 3. A trilha de prompts

| # | Prompt | Uso na implantação |
|---|---|---|
| 1 | Apresentação inicial | Contexto |
| 2 | Comando para atuar como guia | Configuração do papel |
| 3 | Enunciado da Entrega Intermediária | O PDF não estava mais na pasta e o prompt foi sem anexo; o guia pediu o conteúdo em vez de supor. O contexto veio no prompt 4 |
| 4 | Resultado da Entrega Intermediária (PDF) | Estado inicial do plano |
| 5 | Enunciado da Entrega Final (PDF) | O que cada seção pede, na prática, para um site estático |
| 6 | Plano de implantação | Base do [plano](plano-de-implantacao.md) |
| 7 | Ambiente GitHub e integração | Actions como backend no build, ambiente `github-pages`, regra de tag (resposta cortada no limite de tokens) |
| 8 | Gestão de usuários | Papéis, ruleset com code owner, ruleset de tags, inventário, aprovação de workflows de forks |
| 9 | Política de segurança | Controles com ID e mapeamento para normas (resposta cortada no limite de tokens) |
| 10 | Compartilhamento e colaboração | Fluxo protegido e documentação |
| 11 | Testes e lançamento | Plano de testes, teste de fumaça, checklist de Go/No-Go |
| 12 | Roteiro da apresentação | Base do [roteiro](roteiro-apresentacao-final.md) |
| R1 | Revisão da implantação concluída | Ajustes finais antes da `v2.0.0` |
| R2 | Análise do portfólio | Sugestões de melhoria do conteúdo |

Transcrições completas: [trilha](../../ferramentas/guia-implantacao-claude/transcricoes/trilha.md) · [revisão](../../ferramentas/guia-implantacao-claude/transcricoes/revisao.md).

> As respostas 7 e 9 passaram do limite de 16 mil tokens por resposta e foram cortadas. Para a revisão, o limite subiu para 32 mil tokens, com streaming.

## 4. Registro de uso: recomendação, decisão e validação

| Prompt | Recomendação do guia | Decisão | Como foi validado |
|---|---|---|---|
| 5 | Pages via Actions para ter um ambiente de produção verificável | Adotado | *Settings → Pages* = GitHub Actions; ambiente `github-pages` com histórico |
| 5 | Manter o repositório na conta pessoal (opção A) | Adotado (D2) | URLs do site e do LinkedIn inalteradas |
| 6 | Plano com fases, critérios de pronto, riscos e rollback | Adotado, com as datas reais | [plano-de-implantacao.md](plano-de-implantacao.md) |
| 6 | Uma issue por fase num milestone | Adotado | Issues #3 a #8 no milestone v2.0.0 |
| 6 | Segurança antes de abrir acesso e de automatizar | Adotado | Ruleset e scanning ativos antes do PR da implantação |
| 7 | GitHub Actions como "backend" no build (JSON gerado com o token do workflow) | Adotado | `scripts/gerar_dados_github.py` testado localmente: 7 repositórios, versão, commit, equipe |
| 7 | Regra de tag `v*` no ambiente, com ruleset de tags | Adotado | Ruleset "Tags de versão" e política `v*` no ambiente |
| 7 | Manifesto `projeto.json` por projeto | Adiado | Os projetos pessoais estão em outros repositórios; a lista de repositórios já vem da API |
| 8 | Ruleset: 1 aprovação, code owner, aprovação do último push, bypass do admin só via PR | Adotado | Push direto recusado (GH013) |
| 8 | Aprovação para workflows de forks; token somente leitura | Adotado | `approval_policy: all_external_contributors`; *Workflow permissions* = read |
| 8 | Inventário de acessos | Executado | 1 colaborador (admin), 0 convites, 0 deploy keys, 0 webhooks |
| 8 | Mostrar contribuidores (públicos), não colaboradores (LGPD) | Adotado | Seção Equipe usa `/contributors` |
| 9 | Controles com ID (CON, REP, ACT, SITE, DAD) e "alinhado a" em vez de "conforme" | Adotado | [politica-de-seguranca.md](politica-de-seguranca.md) |
| 9 | Aviso de privacidade no site | Adotado | Seção Contato |
| 9 | Commits assinados e OpenSSF Scorecard | Adiado (próximos passos) | Registrado na política |
| 10 | CODE_OF_CONDUCT e "como obter acesso" no CONTRIBUTING | Adotado | Arquivos na raiz |
| 10 | Colaborador real para demonstrar o fluxo | Pendente | Convite a um colega como próximo passo (R2 do plano) |
| 11 | `html-validate`, `node --check`, teste de fumaça, busca de segredos no pacote publicado | Adotado | T-13, T-14, T-16, T-17 em [testes-e-lancamento.md](testes-e-lancamento.md) |
| 11 | Lighthouse CI e `lychee` semanal | Adiado | Os links internos já são testados (T-08); links externos conferidos à mão |
| 12 | Roteiro de 5 minutos por blocos ligados aos critérios | Adotado e adaptado aos desafios reais | [roteiro-apresentacao-final.md](roteiro-apresentacao-final.md) |

## 5. Equivalência com o enunciado (Gemini → Claude)

| Uso previsto para o Gemini | Como foi cumprido com o Claude |
|---|---|
| "Configurar o Google Gemini para guiar a trilha de implantação" (Seção 1) | System prompt de guia + trilha de prompts com os enunciados anexados, versionados no repositório |
| "Utilizando o Google Gemini para garantir conformidade com as melhores práticas" (Seção 3) | Prompts 8 e 9: papéis, rulesets e política com controles mapeados para OWASP, OpenSSF, NIST CSF, ISO 27001, CIS e LGPD |
| "Utilizando o Google Gemini como referência" para completar a integração (Seção 5) | Prompt 11 (plano de testes) e revisão final da implantação concluída (R1) |
| "Google Gemini como ferramenta de apoio e guia durante todo o processo" | Registro de uso acima, prompt a prompt |

## 6. Regras e limites

1. A IA **nunca** recebeu tokens, chaves, senhas ou dados de terceiros. A chave da API fica só no `.env` local.
2. Toda recomendação foi **validada** antes de entrar no repositório: teste automatizado, execução no GitHub ou conferência na documentação oficial.
3. Recomendações não aplicadas estão registradas como "adiado" ou "pendente", com o motivo.
4. A IA orientou; as decisões, as configurações e a responsabilidade técnica são do estudante.

---

[← Voltar para a documentação da implantação](README.md)
