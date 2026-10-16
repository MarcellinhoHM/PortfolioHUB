# Bootcamp — Integração com a API do Claude (Anthropic)

![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)
![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-F37626?logo=jupyter&logoColor=white)
![Anthropic SDK](https://img.shields.io/badge/Anthropic_SDK-Python-191919)
![Categoria](https://img.shields.io/badge/categoria-acad%C3%AAmico-7b2d8e)

Série de notebooks desenvolvidos durante o bootcamp para aprender, na prática, a integrar um modelo de linguagem (LLM) em aplicações Python usando o SDK oficial da Anthropic.

## Sumário

- [Objetivo](#objetivo)
- [Conteúdo](#conteúdo)
- [Tecnologias](#tecnologias)
- [Como executar](#como-executar)
- [Estrutura](#estrutura)
- [O que aprendi](#o-que-aprendi)

## Objetivo

Entender como uma aplicação conversa com um LLM por meio de uma API: montar requisições, manter o histórico da conversa, controlar o comportamento do modelo e receber as respostas de forma eficiente.

## Conteúdo

| Notebook | Tema | O que é feito |
|---|---|---|
| [`001_requests.ipynb`](notebooks/001_requests.ipynb) | Requisições e chat | Cria o cliente, funções auxiliares (`add_user_message`, `add_assistant_message`, `chat`) e um chatbot em loop que mantém o histórico de mensagens. |
| [`002_system_prompt.ipynb`](notebooks/002_system_prompt.ipynb) | System prompt | Usa o parâmetro `system` para definir o papel do modelo (ex.: "dev preciso e conciso") e compara o efeito na resposta. |
| [`003_temperature.ipynb`](notebooks/003_temperature.ipynb) | Temperatura | Ajusta a `temperature` para controlar a criatividade/aleatoriedade das respostas (ex.: geração de ideias de filmes). |
| [`004_streaming.ipynb`](notebooks/004_streaming.ipynb) | Streaming e stop sequences | Recebe a resposta em tempo real (eventos e `text_stream`), usa *prefill* da mensagem do assistente e `stop_sequences` para obter saídas estruturadas. |
| [`001_tools.ipynb`](notebooks/001_tools.ipynb) | Tool use (ferramentas) | Define funções Python (data/hora atual, somar duração a uma data, criar lembrete) e seus *schemas* JSON para que o modelo decida quando chamá-las. |

## Tecnologias

- **Python 3.12**
- **Jupyter Notebook** (VS Code)
- **anthropic** — SDK oficial da API
- **python-dotenv** — leitura da chave de API a partir do arquivo `.env`

## Como executar

1. Clone o repositório e entre na pasta do projeto:

   ```bash
   git clone https://github.com/MarcellinhoHM/PortfolioHUB.git
   cd PortfolioHUB/projetos-academicos/bootcamp-claude-api
   ```

2. (Opcional) Crie um ambiente virtual:

   ```bash
   python -m venv .venv
   # Windows
   .venv\Scripts\activate
   # Linux/macOS
   source .venv/bin/activate
   ```

3. Instale as dependências:

   ```bash
   pip install -r requirements.txt
   ```

4. Copie o arquivo de exemplo e coloque sua chave de API:

   ```bash
   cp .env.example .env
   # edite o .env e preencha ANTHROPIC_API_KEY
   ```

5. Abra os notebooks no VS Code ou no Jupyter e execute as células em ordem.

> **Segurança:** o arquivo `.env` está no `.gitignore` e **nunca** deve ser enviado ao GitHub. Apenas o `.env.example` (sem a chave) é versionado.

## Estrutura

```
bootcamp-claude-api/
├── notebooks/
│   ├── 001_requests.ipynb
│   ├── 001_tools.ipynb
│   ├── 002_system_prompt.ipynb
│   ├── 003_temperature.ipynb
│   └── 004_streaming.ipynb
├── .env.example
├── requirements.txt
└── README.md
```

## O que aprendi

- A API é *stateless*: o histórico da conversa precisa ser reenviado a cada requisição.
- O *system prompt* muda o comportamento do modelo sem alterar a pergunta do usuário.
- Temperaturas baixas geram respostas mais previsíveis; temperaturas altas, mais variadas.
- *Streaming* melhora a experiência do usuário, mostrando o texto enquanto ele é gerado.
- Com *tool use*, o modelo pode pedir para executar funções do meu código e usar o resultado na resposta.

---

[← Voltar para Projetos Acadêmicos](../README.md) · [Página inicial do repositório](../../README.md)
