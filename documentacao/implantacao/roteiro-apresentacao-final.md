# Roteiro da Apresentação Final (5 minutos)

Seção 6 da Entrega Final. Roteiro do vídeo no YouTube sobre as etapas da implantação. Partiu da proposta do guia (prompt 12 da [trilha](../../ferramentas/guia-implantacao-claude/transcricoes/trilha.md)) e foi ajustado ao que foi realmente feito e aos desafios que de fato apareceram.

**Slides:** https://marcellinhohm.github.io/PortfolioHUB/documentacao/slides/implantacao/

**Meta:** 4min40s (cerca de 650 palavras a 140 palavras por minuto), com 20 segundos de folga.

| Tempo | Bloco | Seção do enunciado | Critério de avaliação | Slide |
|---|---|---|---|---|
| 0:00–0:20 | Abertura | — | Apresentação | 1 |
| 0:20–0:55 | Planejamento e IA | 1 | Documentação | 2 |
| 0:55–1:45 | Ambiente e integração | 2 | Implementação | 3 |
| 1:45–2:45 | Usuários e segurança | 3 | Segurança | 4, 5 |
| 2:45–3:25 | Colaboração | 4 | Colaboração | 6 |
| 3:25–4:05 | Testes e produção | 5 | Implementação | 7 |
| 4:05–4:45 | Desafios | 6 | Apresentação | 8 |
| 4:45–5:00 | Encerramento | — | — | 9 |

## Bloco 1 · Abertura (0:00–0:20)

**Na tela:** slide 1 e depois a página inicial do site.

> "Olá, eu sou o Marcello Montella. Este é o PortfolioHUB, meu portfólio profissional publicado no GitHub Pages. Nesta Entrega Final eu levei o projeto da versão 1.1 para a 2.0: um site em produção, com segurança, controle de acesso, colaboração e testes automatizados. Vou mostrar as seis etapas."

## Bloco 2 · Planejamento e IA (0:20–0:55)

**Na tela:** `plano-de-implantacao.md` no GitHub, o milestone v2.0.0 com as issues, a pasta `ferramentas/guia-implantacao-claude` e um trecho da transcrição.

> "Comecei com um plano de implantação: seis fases, critérios de pronto, riscos e plano de reversão. Cada fase virou uma issue neste milestone. O enunciado sugere o Gemini como guia; eu usei o Claude, da Anthropic, no mesmo papel. Escrevi um script em Python que configura o Claude como guia de implantação, envia os enunciados e salva as respostas aqui no repositório. No ia-guia.md registrei cada recomendação, o que adotei, o que adiei e como validei. A IA orientou; as decisões e os testes foram meus."

## Bloco 3 · Ambiente e integração (0:55–1:45)

**Na tela:** *Settings → Pages* (GitHub Actions), *Settings → Environments → github-pages*, o workflow de publicação verde, e no site as seções Repositórios (com o filtro) e Implantação.

> "Para ter um ambiente dedicado, a publicação passou a ser feita pelo GitHub Actions, no ambiente github-pages, que só aceita a branch main. O desafio era integrar o GitHub a um site sem backend. A solução foi usar o Actions como backend na hora da publicação: o workflow consulta a API do GitHub com o token dele e gera um arquivo de dados que vai junto com o site. O token nunca chega ao navegador. Por isso esta lista de repositórios se atualiza sozinha, e o painel mostra a versão em produção, o último commit, o status dos testes e a equipe. Se o arquivo falhar, o site usa a API pública ao vivo, com cache."

## Bloco 4 · Usuários e segurança (1:45–2:45)

**Na tela:** *Settings → Rules → Rulesets*, o terminal com o push recusado (gravado antes), a aba *Security* e a meta tag da CSP no código.

> "Na gestão de usuários, segui o menor privilégio. A main é protegida por uma ruleset: Pull Request obrigatório, aprovação do responsável no CODEOWNERS, testes obrigatórios, sem force push. Ninguém faz push direto, nem eu: olhem o push recusado. As tags de versão só eu crio. Na segurança, ativei secret scanning com push protection, Dependabot, CodeQL e o relato privado de vulnerabilidades. Nos workflows, o token é somente leitura e as Actions ficam fixadas pelo SHA. No site, uma Content Security Policy sem inline, e os dados externos nunca entram como HTML. Cada controle tem um ID na política de segurança, ligado a OWASP, NIST e LGPD."

## Bloco 5 · Colaboração (2:45–3:25)

**Na tela:** o PR da implantação com os checks verdes, "Review required" e o merge com bypass registrado; as issues fechadas pelo PR; o CONTRIBUTING e o CODE_OF_CONDUCT.

> "A própria implantação passou pelo fluxo que ela criou: issues, uma branch, um Pull Request que fecha as issues, os dois checks obrigatórios verdes e o merge. Como o GitHub não deixa ninguém aprovar o próprio PR, eu uso um bypass que só funciona dentro de um Pull Request e fica registrado nele. Quem quiser contribuir faz fork e abre PR; os workflows de forks só rodam depois que eu aprovo. Está tudo documentado: como contribuir, código de conduta e como conceder e revogar acesso."

> Se houver tempo antes da gravação, convide um colega, peça um PR pequeno e mostre o merge bloqueado até a sua revisão: é a evidência mais forte deste bloco.

## Bloco 6 · Testes e produção (3:25–4:05)

**Na tela:** execução do CI, execução da publicação com o teste de fumaça, a Release `v2.0.0` e o rodapé do site.

> "Todo Pull Request passa por testes automáticos: CSP em todas as páginas, nenhum script inline, links internos, links externos seguros, nenhuma chave no código, HTML válido e varredura de segredos no histórico inteiro. Para provar que os testes funcionam, eu quebrei o site de propósito e eles pegaram as cinco falhas. Antes de publicar, os testes rodam de novo e o pacote é checado contra segredos; depois, um teste de fumaça confere o site no ar. Com tudo verde, publiquei a versão 2.0.0."

## Bloco 7 · Desafios (4:05–4:45)

**Na tela:** slide 8.

> "Três desafios marcaram o projeto. Primeiro: a CSP rígida bloqueava os slides, porque tinham CSS e JavaScript inline; tirei tudo para arquivos separados. Segundo: como único mantenedor, eu não podia aprovar meus próprios PRs; resolvi com o bypass que só vale dentro de um PR. Terceiro: algumas respostas da IA passaram do limite de tokens e foram cortadas, e um anexo não foi enviado. Aprendi a não confiar cegamente: aumentei o limite, ativei streaming e validei cada recomendação antes de aplicar."

## Bloco 8 · Encerramento (4:45–5:00)

**Na tela:** slide 9.

> "Os links do site, do repositório e do LinkedIn estão na descrição. Obrigado!"

## Abas para deixar abertas (na ordem)

| # | Aba | Bloco |
|---|---|---|
| 1 | Slides da implantação | 1, 7, 8 |
| 2 | Site em produção | 1, 3, 6 |
| 3 | `plano-de-implantacao.md` e `ia-guia.md` | 2 |
| 4 | Milestone v2.0.0 | 2, 5 |
| 5 | `ferramentas/guia-implantacao-claude/transcricoes/trilha.md` | 2 |
| 6 | *Settings → Pages* e *Environments* | 3 |
| 7 | *Settings → Rules → Rulesets* | 4 |
| 8 | Terminal com o push recusado | 4 |
| 9 | Aba *Security* | 4 |
| 10 | PR da implantação | 5 |
| 11 | *Actions*: CI e publicação | 6 |
| 12 | Release `v2.0.0` | 6 |

## Antes de gravar

- [ ] Fechar o `.env`, terminais com histórico e o console da Anthropic
- [ ] Desativar notificações
- [ ] Não mostrar *Settings → Emails*, o *security log* nem códigos de recuperação
- [ ] Zoom do navegador entre 125% e 150%; resolução 1080p
- [ ] Ensaiar duas vezes com cronômetro; gravar bloco a bloco

## Publicação no YouTube

**Visibilidade:** não listado. **Título:** `PortfolioHUB v2.0: Implantação com GitHub, Segurança e IA | Bootcamp I`

```text
Entrega Final do Bootcamp I: implantação do PortfolioHUB, com o Claude (Anthropic) como IA guia.

Site: https://marcellinhohm.github.io/PortfolioHUB/
Repositório: https://github.com/MarcellinhoHM/PortfolioHUB
Release v2.0.0: https://github.com/MarcellinhoHM/PortfolioHUB/releases/tag/v2.0.0
Plano de implantação: https://github.com/MarcellinhoHM/PortfolioHUB/blob/main/documentacao/implantacao/plano-de-implantacao.md
LinkedIn: https://www.linkedin.com/in/marcello-augusto-hesketh-montella-042a66370

00:00 Abertura
00:20 Planejamento e IA como guia
00:55 Ambiente GitHub e integração
01:45 Usuários e segurança
02:45 Colaboração
03:25 Testes e produção
04:05 Desafios
04:45 Encerramento
```

---

[← Voltar para a documentação da implantação](README.md)
