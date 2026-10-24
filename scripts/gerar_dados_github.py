"""Gera o JSON com os dados do GitHub que o site estático do PortfolioHUB exibe.

Roda no GitHub Actions, durante a publicação: o Actions faz o papel de backend
no momento do build. Usa o GITHUB_TOKEN do próprio workflow (somente leitura)
para não depender do limite da API anônima, e grava apenas dados públicos.

Uso: python scripts/gerar_dados_github.py [arquivo_de_saida]
"""

import json
import os
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

USUARIO = "MarcellinhoHM"
REPO = os.environ.get("GITHUB_REPOSITORY", "MarcellinhoHM/PortfolioHUB")
TOKEN = os.environ.get("GITHUB_TOKEN")
SAIDA = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("assets/data/github.json")

# Só estes campos de cada repositório vão para o arquivo público
CAMPOS_REPO = ("name", "description", "html_url", "homepage", "language", "topics",
               "stargazers_count", "pushed_at", "has_pages", "fork", "archived")

avisos = []


def api(caminho: str):
    req = urllib.request.Request(
        "https://api.github.com" + caminho,
        headers={"Accept": "application/vnd.github+json", "User-Agent": "portfoliohub-build",
                 "X-GitHub-Api-Version": "2022-11-28"},
    )
    if TOKEN:
        req.add_header("Authorization", "Bearer " + TOKEN)
    with urllib.request.urlopen(req, timeout=20) as resp:
        return json.load(resp)


def tentar(descricao: str, caminho: str):
    """Falha na API vira aviso: o site é publicado mesmo assim e o navegador usa a API ao vivo."""
    try:
        return api(caminho)
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as erro:
        avisos.append(f"{descricao}: {erro}")
        return None


def main():
    repos = tentar("repositórios", f"/users/{USUARIO}/repos?per_page=100&sort=pushed")
    release = tentar("versão atual", f"/repos/{REPO}/releases/latest")
    commits = tentar("último commit", f"/repos/{REPO}/commits?per_page=1")
    pessoas = tentar("contribuidores", f"/repos/{REPO}/contributors?per_page=20")

    dados = {
        "gerado_em": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "repos": [{c: r.get(c) for c in CAMPOS_REPO} for r in repos] if repos else None,
        "release": {"tag_name": release["tag_name"], "published_at": release["published_at"],
                    "html_url": release["html_url"]} if release else None,
        "commit": {"sha": commits[0]["sha"], "message": commits[0]["commit"]["message"],
                   "date": commits[0]["commit"]["committer"]["date"]} if commits else None,
        "contribuidores": [{"login": p["login"], "html_url": p["html_url"], "avatar_url": p["avatar_url"],
                            "contributions": p["contributions"], "type": p["type"]} for p in pessoas] if pessoas else None,
    }

    SAIDA.parent.mkdir(parents=True, exist_ok=True)
    SAIDA.write_text(json.dumps(dados, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Gerado {SAIDA}: {len(dados['repos'] or [])} repositórios")
    for aviso in avisos:
        print(f"::warning::{aviso}")


if __name__ == "__main__":
    main()
