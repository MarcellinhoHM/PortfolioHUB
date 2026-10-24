# Como contribuir

Obrigado pelo interesse no PortfolioHUB! Sugestões e correções são bem-vindas. Ao participar, você concorda com o [Código de Conduta](CODE_OF_CONDUCT.md).

## Resumo

1. Abra uma [Issue](https://github.com/MarcellinhoHM/PortfolioHUB/issues/new/choose) descrevendo o problema ou a ideia.
2. Faça um *fork* do repositório e crie uma branch a partir da `main`:
   - `feature/<nome>` para novidades;
   - `fix/<nome>` para correções;
   - `docs/<nome>` para documentação.
3. Faça commits seguindo o [Conventional Commits](https://www.conventionalcommits.org/pt-br/), por exemplo `fix(site): corrige link do LinkedIn`.
4. Rode os testes antes de enviar: `python -m unittest discover -s tests -v`.
5. Abra um Pull Request para a `main` preenchendo o modelo e citando a issue (`Closes #n`).

## O que acontece com o seu Pull Request

A `main` é protegida por uma ruleset. Seu PR só entra quando:

- os checks **Testes do site** e **Varredura de segredos** passarem (em PRs de fork, o mantenedor aprova a execução primeiro);
- o responsável definido no [CODEOWNERS](.github/CODEOWNERS) aprovar;
- todas as conversas de revisão estiverem resolvidas.

Um commit novo depois da aprovação exige nova revisão.

## Regras

- Não envie arquivos `.env`, chaves de API ou senhas. Um segredo enviado por engano é bloqueado pelo push protection e precisa ser revogado.
- Não use scripts inline nem atributos `style=""` no HTML: a Content Security Policy do site bloqueia. Coloque o código em `assets/`.
- Mantenha atualizado o README do projeto que você alterar.
- Teste o site localmente antes de abrir o PR (`python -m http.server 8000`).

## Como obter acesso de colaborador

Contribuições começam por fork + Pull Request. O convite como colaborador é considerado depois de contribuições recorrentes aceitas, seguindo a [política de acesso](documentacao/implantacao/gestao-de-usuarios.md).

## Segurança

Encontrou uma vulnerabilidade? **Não abra uma issue pública.** Siga o [SECURITY.md](SECURITY.md).

O passo a passo completo está no [Guia de Colaboração](documentacao/guia-colaboracao.md), no [Guia de Git e Versionamento](documentacao/guia-git-e-versionamento.md) e em [Compartilhamento e Colaboração](documentacao/implantacao/compartilhamento-e-colaboracao.md).
