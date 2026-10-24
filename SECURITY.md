# Política de Segurança

## Versões com suporte

| Versão | Suporte |
|---|---|
| 2.x (atual, em produção) | ✅ Recebe correções de segurança |
| 1.x | ❌ Sem suporte. Atualize para a 2.x |

## Como relatar uma vulnerabilidade

**Não abra uma Issue pública** para relatar falhas de segurança.

1. Use o relato privado do GitHub: aba **Security → Report a vulnerability** ([link direto](https://github.com/MarcellinhoHM/PortfolioHUB/security/advisories/new)).
2. Descreva o problema, como reproduzir e o impacto esperado.
3. Se encontrou uma chave ou token exposto, diga onde (arquivo, commit ou página), mas **não** use a credencial.

## Prazos de resposta

| Etapa | Prazo |
|---|---|
| Confirmação de recebimento | até 3 dias |
| Avaliação inicial e classificação | até 7 dias |
| Correção de falha crítica ou alta | até 14 dias |
| Divulgação | depois da correção, por GitHub Security Advisory |

## Escopo

- Site publicado em https://marcellinhohm.github.io/PortfolioHUB/ (HTML, CSS e JavaScript).
- Código, workflows do GitHub Actions e configurações deste repositório.
- Ferramenta `ferramentas/guia-implantacao-claude/`.

Fora do escopo: os repositórios externos listados no portfólio (cada um tem seu próprio dono) e a infraestrutura do GitHub.

## Medidas em vigor

A política completa, com as medidas aplicadas e as referências (OWASP, NIST CSF, CIS, LGPD), está em [`documentacao/implantacao/politica-de-seguranca.md`](documentacao/implantacao/politica-de-seguranca.md).
