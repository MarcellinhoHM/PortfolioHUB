"""Testes do PortfolioHUB (só biblioteca padrão do Python).

Rodar localmente:  python -m unittest discover -s tests -v
"""

import json
import re
import subprocess
import unittest
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlparse

RAIZ = Path(__file__).resolve().parent.parent
# Pastas geradas ou de terceiros, que não fazem parte do site
IGNORADAS = {".git", "node_modules", "_site"}


def do_projeto(caminho: Path) -> bool:
    return not IGNORADAS.intersection(caminho.relative_to(RAIZ).parts)


PAGINAS = sorted(p for p in RAIZ.rglob("*.html") if do_projeto(p))
JS = sorted((RAIZ / "assets" / "js").glob("*.js")) + sorted((RAIZ / "documentacao" / "slides").glob("*.js"))

# Padrões de chaves e tokens que nunca podem aparecer no repositório
PADROES_SEGREDO = {
    "chave da Anthropic": re.compile(r"sk-ant-[A-Za-z0-9_\-]{20,}"),
    "token do GitHub": re.compile(r"\b(ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9]{30,}\b"),
    "token fino do GitHub": re.compile(r"github_pat_[A-Za-z0-9_]{40,}"),
    "chave da AWS": re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    "chave privada": re.compile(r"-----BEGIN (RSA |EC |OPENSSH )?PRIVATE KEY-----"),
}


class Pagina(HTMLParser):
    """Coleta o que os testes precisam de cada página HTML."""

    def __init__(self):
        super().__init__()
        self.csp = None
        self.links = []          # (tag, atributo, valor)
        self.blank_sem_noopener = []
        self.scripts_inline = 0
        self.estilos_inline = 0
        self.atributos_style = 0
        self.ids = set()
        self._em_script_inline = False

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if "id" in a:
            self.ids.add(a["id"])
        if tag == "meta" and (a.get("http-equiv") or "").lower() == "content-security-policy":
            self.csp = a.get("content", "")
        if "style" in a:
            self.atributos_style += 1
        if tag == "style":
            self.estilos_inline += 1
        if tag == "script":
            if a.get("src"):
                self.links.append((tag, "src", a["src"]))
            else:
                self._em_script_inline = True
        for attr in ("href", "src"):
            if attr in a and a[attr] and not (tag == "script" and attr == "src"):
                self.links.append((tag, attr, a[attr]))
        if tag == "a" and a.get("target") == "_blank":
            if "noopener" not in (a.get("rel") or ""):
                self.blank_sem_noopener.append(a.get("href"))

    def handle_data(self, data):
        if self._em_script_inline and data.strip():
            self.scripts_inline += 1

    def handle_endtag(self, tag):
        if tag == "script":
            self._em_script_inline = False


def analisar(caminho: Path) -> Pagina:
    p = Pagina()
    p.feed(caminho.read_text(encoding="utf-8"))
    return p


def arquivos_versionados() -> list[Path]:
    try:
        saida = subprocess.run(["git", "ls-files"], cwd=RAIZ, capture_output=True, text=True, check=True).stdout
        return [RAIZ / linha for linha in saida.splitlines() if linha]
    except (OSError, subprocess.CalledProcessError):
        return [p for p in RAIZ.rglob("*") if p.is_file() and do_projeto(p)]


class TestSeguranca(unittest.TestCase):
    def test_toda_pagina_tem_csp_restritiva(self):
        for pagina in PAGINAS:
            with self.subTest(pagina=pagina.relative_to(RAIZ)):
                csp = analisar(pagina).csp
                self.assertIsNotNone(csp, "página sem Content-Security-Policy")
                self.assertIn("default-src 'self'", csp)
                self.assertIn("object-src 'none'", csp)
                self.assertNotIn("unsafe-inline", csp)
                self.assertNotIn("unsafe-eval", csp)

    def test_sem_script_ou_estilo_inline(self):
        # Necessário para a CSP funcionar sem 'unsafe-inline'
        for pagina in PAGINAS:
            with self.subTest(pagina=pagina.relative_to(RAIZ)):
                p = analisar(pagina)
                self.assertEqual(p.scripts_inline, 0, "script inline")
                self.assertEqual(p.estilos_inline, 0, "bloco <style> inline")
                self.assertEqual(p.atributos_style, 0, "atributo style=")

    def test_sem_estilos_externos(self):
        # Estilos e fontes servidos pelo próprio site (privacidade e CSP 'self')
        for pagina in PAGINAS:
            with self.subTest(pagina=pagina.relative_to(RAIZ)):
                externos = [v for tag, attr, v in analisar(pagina).links
                            if tag == "link" and attr == "href" and v.startswith(("http://", "https://", "//"))
                            and not v.endswith((".png", ".svg"))]
                self.assertEqual(externos, [])

    def test_links_externos_com_noopener(self):
        for pagina in PAGINAS:
            with self.subTest(pagina=pagina.relative_to(RAIZ)):
                self.assertEqual(analisar(pagina).blank_sem_noopener, [])

    def test_javascript_nao_usa_innerhtml_nem_eval(self):
        for arquivo in JS:
            with self.subTest(arquivo=arquivo.name):
                codigo = arquivo.read_text(encoding="utf-8")
                self.assertNotRegex(codigo, r"\.innerHTML\s*=|\.outerHTML\s*=|insertAdjacentHTML|\beval\(|new Function\(")

    def test_nenhum_segredo_versionado(self):
        for arquivo in arquivos_versionados():
            if arquivo.suffix.lower() in {".png", ".jpg", ".jpeg", ".gif", ".ico", ".pdf"} or not arquivo.exists():
                continue
            texto = arquivo.read_text(encoding="utf-8", errors="ignore")
            for nome, padrao in PADROES_SEGREDO.items():
                with self.subTest(arquivo=arquivo.relative_to(RAIZ), tipo=nome):
                    self.assertIsNone(padrao.search(texto), f"possível {nome} encontrado")

    def test_arquivo_env_nao_versionado(self):
        nomes = [p.name for p in arquivos_versionados()]
        self.assertNotIn(".env", nomes)
        self.assertIn(".env", (RAIZ / ".gitignore").read_text(encoding="utf-8").split())

    def test_politica_de_seguranca_existe(self):
        self.assertTrue((RAIZ / "SECURITY.md").exists())
        self.assertTrue((RAIZ / ".github" / "CODEOWNERS").exists())
        self.assertTrue((RAIZ / ".github" / "dependabot.yml").exists())


class TestLinks(unittest.TestCase):
    def test_links_internos_existem(self):
        for pagina in PAGINAS:
            p = analisar(pagina)
            for tag, attr, valor in p.links:
                url = urlparse(valor)
                if url.scheme or valor.startswith(("//", "mailto:", "#")):
                    continue
                caminho = unquote(url.path)
                if not caminho:
                    continue
                if caminho.startswith("/PortfolioHUB/"):
                    alvo = RAIZ / caminho[len("/PortfolioHUB/"):]
                else:
                    alvo = (pagina.parent / caminho).resolve()
                if alvo.is_dir():
                    alvo = alvo / "index.html"
                with self.subTest(pagina=pagina.relative_to(RAIZ), link=valor):
                    self.assertTrue(alvo.exists(), f"{tag}[{attr}] aponta para arquivo inexistente")

    def test_ancoras_do_menu_existem(self):
        p = analisar(RAIZ / "index.html")
        for tag, attr, valor in p.links:
            if valor.startswith("#") and len(valor) > 1:
                with self.subTest(ancora=valor):
                    self.assertIn(valor[1:], p.ids)


class TestEstrutura(unittest.TestCase):
    def test_pastas_principais_tem_readme(self):
        for pasta in ["", "projetos-academicos", "projetos-pessoais", "documentacao",
                      "documentacao/implantacao", "projetos-academicos/bootcamp-claude-api",
                      "ferramentas/guia-implantacao-claude"]:
            with self.subTest(pasta=pasta or "raiz"):
                self.assertTrue((RAIZ / pasta / "README.md").exists())

    def test_arquivos_de_producao(self):
        for nome in ["index.html", "404.html", "sitemap.xml", ".nojekyll", "assets/img/favicon.svg", "LICENSE"]:
            with self.subTest(arquivo=nome):
                self.assertTrue((RAIZ / nome).exists())

    def test_json_validos(self):
        for arquivo in RAIZ.rglob("*.json"):
            if not do_projeto(arquivo):
                continue
            with self.subTest(arquivo=arquivo.relative_to(RAIZ)):
                json.loads(arquivo.read_text(encoding="utf-8"))

    def test_versao_do_rodape_bate_com_o_changelog(self):
        rodape = re.search(r"PortfolioHUB v(\d+\.\d+\.\d+)", (RAIZ / "index.html").read_text(encoding="utf-8"))
        changelog = re.search(r"## \[(\d+\.\d+\.\d+)\]", (RAIZ / "CHANGELOG.md").read_text(encoding="utf-8"))
        self.assertIsNotNone(rodape)
        self.assertIsNotNone(changelog)
        self.assertEqual(rodape.group(1), changelog.group(1))


if __name__ == "__main__":
    unittest.main()
