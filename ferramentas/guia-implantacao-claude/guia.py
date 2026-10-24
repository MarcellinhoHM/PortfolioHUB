"""Guia de Implantação do PortfolioHUB com o Claude.

Configura o Claude como guia da trilha de implantação (system prompt em
system_prompt.md) e conduz a conversa de duas formas:

  python guia.py trilha  --etapa trilha   # roda os prompts de trilha.json
  python guia.py chat                     # conversa livre no terminal

Cada execução grava a transcrição (prompts e respostas) em transcricoes/.
A chave da API vem do arquivo .env (ANTHROPIC_API_KEY), nunca do código.
"""

import argparse
import base64
import json
import sys
from datetime import datetime
from pathlib import Path

import anthropic
from dotenv import find_dotenv, load_dotenv

PASTA = Path(__file__).resolve().parent
MODELO = "claude-opus-5-5"
ESFORCO = "medium"
MAX_TOKENS = 32000  # respostas longas (planos, políticas); exige streaming
# Se um classificador de segurança recusar a resposta, a API refaz o pedido
# no modelo de fallback recomendado para aquela categoria.
BETAS = ["server-side-fallback-2026-07-01"]


def carregar_system_prompt() -> str:
    return (PASTA / "system_prompt.md").read_text(encoding="utf-8")


def bloco_de_anexo(caminho: Path) -> dict:
    """Transforma um arquivo em bloco de conteúdo: PDF vira documento, texto vira texto."""
    if caminho.suffix.lower() == ".pdf":
        dados = base64.standard_b64encode(caminho.read_bytes()).decode("ascii")
        return {
            "type": "document",
            "source": {"type": "base64", "media_type": "application/pdf", "data": dados},
            "title": caminho.name,
        }
    texto = caminho.read_text(encoding="utf-8")
    return {"type": "text", "text": f"<anexo nome=\"{caminho.name}\">\n{texto}\n</anexo>"}


def montar_mensagem(prompt: str, anexos: list[str], pasta_anexos: Path) -> tuple[dict, list[str]]:
    conteudo, usados = [], []
    for nome in anexos:
        caminho = (pasta_anexos / nome).resolve()
        if not caminho.exists():
            print(f"  aviso: anexo não encontrado, seguindo sem ele: {caminho}", file=sys.stderr)
            continue
        conteudo.append(bloco_de_anexo(caminho))
        usados.append(caminho.name)
    conteudo.append({"type": "text", "text": prompt})
    return {"role": "user", "content": conteudo}, usados


def perguntar(client: anthropic.Anthropic, system: str, historico: list) -> tuple[str, object]:
    # Streaming evita o timeout de requisições longas; só a mensagem final é usada
    with client.beta.messages.stream(
        model=MODELO,
        max_tokens=MAX_TOKENS,
        system=system,
        messages=historico,
        output_config={"effort": ESFORCO},
        cache_control={"type": "ephemeral"},
        betas=BETAS,
        fallbacks="default",
    ) as stream:
        resposta = stream.get_final_message()
    if resposta.stop_reason == "refusal":
        raise RuntimeError("O modelo recusou a resposta (stop_reason=refusal).")
    texto = "\n".join(b.text for b in resposta.content if b.type == "text").strip()
    if resposta.stop_reason == "max_tokens":
        texto += "\n\n> (resposta cortada pelo limite de tokens)"
    # O conteúdo completo volta para o histórico para manter o contexto entre turnos.
    historico.append({"role": "assistant", "content": resposta.content})
    return texto, resposta


class Transcricao:
    def __init__(self, titulo: str, nome_arquivo: str):
        pasta = PASTA / "transcricoes"
        pasta.mkdir(exist_ok=True)
        self.md = pasta / f"{nome_arquivo}.md"
        self.json = pasta / f"{nome_arquivo}.json"
        self.registros = []
        self.md.write_text(
            f"# {titulo}\n\n"
            f"- Data: {datetime.now():%d/%m/%Y %H:%M}\n"
            f"- Modelo: `{MODELO}` (esforço `{ESFORCO}`)\n"
            f"- Configuração do guia: [`system_prompt.md`](../system_prompt.md)\n\n",
            encoding="utf-8",
        )

    def adicionar(self, numero: int, titulo: str, prompt: str, anexos: list[str], resposta: str, meta: dict):
        partes = [f"## Prompt {numero}: {titulo}\n\n{prompt}\n"]
        if anexos:
            partes.append("\n" + "\n".join(f"- Anexo: `{a}`" for a in anexos) + "\n")
        partes.append(f"\n### Resposta ao Prompt {numero}\n\n{resposta}\n\n---\n\n")
        with self.md.open("a", encoding="utf-8") as f:
            f.write("".join(partes))
        self.registros.append({"numero": numero, "titulo": titulo, "prompt": prompt,
                               "anexos": anexos, "resposta": resposta, **meta})
        self.json.write_text(json.dumps(self.registros, ensure_ascii=False, indent=2), encoding="utf-8")


def metadados(resposta) -> dict:
    uso = resposta.usage
    return {
        "modelo": resposta.model,
        "stop_reason": resposta.stop_reason,
        "tokens_entrada": uso.input_tokens,
        "tokens_cache_lidos": getattr(uso, "cache_read_input_tokens", 0) or 0,
        "tokens_saida": uso.output_tokens,
    }


def rodar_trilha(args, client):
    trilha = json.loads(Path(args.arquivo).read_text(encoding="utf-8"))
    passos = trilha["etapas"][args.etapa]
    system = carregar_system_prompt()
    transcricao = Transcricao(f"{trilha['titulo']} — etapa \"{args.etapa}\"", args.etapa)
    historico = []
    for numero, passo in enumerate(passos, start=1):
        print(f"[{numero}/{len(passos)}] {passo['titulo']}...")
        mensagem, usados = montar_mensagem(passo["prompt"], passo.get("anexos", []), Path(args.pasta_anexos))
        historico.append(mensagem)
        texto, resposta = perguntar(client, system, historico)
        transcricao.adicionar(numero, passo["titulo"], passo["prompt"], usados, texto, metadados(resposta))
    print(f"\nTranscrição salva em {transcricao.md}")


def rodar_chat(args, client):
    system = carregar_system_prompt()
    transcricao = Transcricao("Conversa com o Guia de Implantação", f"chat-{datetime.now():%Y%m%d-%H%M}")
    historico, numero = [], 0
    print("Guia de Implantação do PortfolioHUB. Digite 'sair' para encerrar.\n")
    while True:
        try:
            pergunta = input("> ").strip()
        except EOFError:
            break
        if pergunta.lower() in {"sair", "exit", "quit"}:
            break
        if not pergunta:
            continue
        numero += 1
        historico.append({"role": "user", "content": pergunta})
        texto, resposta = perguntar(client, system, historico)
        print(f"\nGuia: {texto}\n")
        transcricao.adicionar(numero, "pergunta livre", pergunta, [], texto, metadados(resposta))
    print(f"Transcrição salva em {transcricao.md}")


def main():
    parser = argparse.ArgumentParser(description="Guia de Implantação do PortfolioHUB com o Claude")
    sub = parser.add_subparsers(dest="modo", required=True)
    p_trilha = sub.add_parser("trilha", help="roda os prompts de um arquivo de trilha")
    p_trilha.add_argument("--arquivo", default=str(PASTA / "trilha.json"))
    p_trilha.add_argument("--etapa", default="trilha", help="nome da etapa dentro do arquivo")
    p_trilha.add_argument("--pasta-anexos", default=".", help="pasta base dos anexos citados na trilha")
    sub.add_parser("chat", help="conversa livre com o guia")
    args = parser.parse_args()

    load_dotenv(find_dotenv(usecwd=True))
    client = anthropic.Anthropic()

    try:
        if args.modo == "trilha":
            rodar_trilha(args, client)
        else:
            rodar_chat(args, client)
    except anthropic.AuthenticationError:
        sys.exit("Chave de API inválida. Confira ANTHROPIC_API_KEY no arquivo .env.")
    except anthropic.RateLimitError as e:
        sys.exit(f"Limite de requisições atingido. Tente de novo em {e.response.headers.get('retry-after', '60')}s.")
    except anthropic.BadRequestError as e:
        sys.exit(f"Requisição inválida: {e.message}")
    except anthropic.APIStatusError as e:
        sys.exit(f"Erro da API ({e.status_code}): {e.message}")
    except anthropic.APIConnectionError:
        sys.exit("Falha de conexão com a API. Verifique a internet.")


if __name__ == "__main__":
    main()
