# Guia de Implantação com o Claude

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)
![Anthropic SDK](https://img.shields.io/badge/Anthropic_SDK-Python-191919)
![Modelo](https://img.shields.io/badge/modelo-claude--opus--5--5-d97757)

Ferramenta que configura o **Claude** (Anthropic) como guia da trilha de implantação do PortfolioHUB. Ela substitui o Google Gemini citado no enunciado da Entrega Final: o Claude recebe o contexto do projeto, os enunciados e as entregas anteriores, e orienta cada etapa da implantação.

## Sumário

- [Como o guia é configurado](#como-o-guia-é-configurado)
- [Arquivos](#arquivos)
- [Como executar](#como-executar)
- [Transcrições](#transcrições)
- [Segurança](#segurança)

## Como o guia é configurado

| Peça | Onde | Função |
|---|---|---|
| Papel e regras do guia | [`system_prompt.md`](system_prompt.md) | Define o contexto do PortfolioHUB, as restrições (site estático, nada de segredos no front-end) e o formato das respostas, sempre terminando com **Próximos passos** e **Como comprovar**. |
| Trilha de prompts | [`trilha.json`](trilha.json) | Sequência de prompts por etapa, com anexos (PDFs dos enunciados, entrega anterior, arquivos do repositório). |
| Conversa | [`guia.py`](guia.py) | Mantém o histórico entre os turnos, envia os anexos e grava a transcrição. |

Parâmetros da chamada à API:

- Modelo `claude-opus-5-5`, com esforço `medium`.
- Cache de prompt automático, para não pagar de novo pelos PDFs a cada turno.
- Fallback do servidor (`fallbacks="default"`): se um classificador de segurança recusar a resposta, a API refaz o pedido no modelo recomendado.

## Arquivos

```
guia-implantacao-claude/
├── guia.py             # script principal (modos "trilha" e "chat")
├── system_prompt.md    # configuração do guia
├── trilha.json         # prompts das etapas "trilha" e "revisao"
├── requirements.txt
├── .env.example        # modelo do arquivo de chave
└── transcricoes/       # prompts e respostas gravados (Markdown e JSON)
```

## Como executar

```bash
cd ferramentas/guia-implantacao-claude
pip install -r requirements.txt
cp .env.example .env        # preencha ANTHROPIC_API_KEY

# trilha completa (12 prompts); --pasta-anexos é a pasta onde estão os PDFs citados
python guia.py trilha --etapa trilha --pasta-anexos /caminho/dos/anexos

# revisão depois da implantação
python guia.py trilha --etapa revisao --pasta-anexos /caminho/dos/anexos

# conversa livre com o guia
python guia.py chat
```

Os enunciados da disciplina não ficam no repositório (são material do curso). Por isso o caminho deles é informado em `--pasta-anexos`.

## Transcrições

| Etapa | Arquivo | Conteúdo |
|---|---|---|
| Trilha | [`transcricoes/trilha.md`](transcricoes/trilha.md) | Apresentação do projeto, plano de implantação, ambiente GitHub, usuários, segurança, colaboração, testes e roteiro. |
| Revisão | [`transcricoes/revisao.md`](transcricoes/revisao.md) | Revisão da implantação concluída e análise do portfólio. |

O arquivo `.json` ao lado de cada transcrição guarda também o modelo que respondeu e o uso de tokens de cada turno.

## Segurança

- A chave fica no `.env`, que está no `.gitignore`. Só o `.env.example` vai para o repositório.
- O guia roda localmente. O site no GitHub Pages é estático e **não** chama a API, porque qualquer chave colocada no navegador ficaria pública.

---

[← Voltar para a documentação da implantação](../../documentacao/implantacao/README.md)
