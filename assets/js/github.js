// PortfolioHUB — integração com o GitHub
// Lista os repositórios, a versão em produção, o último commit e a equipe.
// Fonte principal: assets/data/github.json, gerado pelo GitHub Actions a cada publicação
// (scripts/gerar_dados_github.py). Se faltar algum dado, usa a API pública ao vivo.
// Segurança: os dados são inseridos só com textContent (nunca innerHTML)
// e todo link é validado antes de ir para o atributo href.

(function () {
  const USUARIO = "MarcellinhoHM";
  const REPO = "MarcellinhoHM/PortfolioHUB";
  const API = "https://api.github.com";
  const DADOS_BUILD = "assets/data/github.json";
  const CACHE_MIN = 10;

  // Carrega uma vez o JSON gerado no build; null se não existir (ex.: rodando localmente)
  const dadosBuild = fetch(DADOS_BUILD, { cache: "no-cache" })
    .then((r) => (r.ok ? r.json() : null))
    .catch(() => null);

  async function doBuildOuApi(campo, caminho) {
    const build = await dadosBuild;
    if (build && build[campo]) return build[campo];
    return buscar(caminho);
  }

  const CORES = {
    JavaScript: "#f1e05a", HTML: "#e34c26", CSS: "#563d7c", Python: "#3572A5",
    Java: "#b07219", C: "#555555", "Jupyter Notebook": "#DA5B0B", TypeScript: "#3178c6",
  };

  // Cache em sessionStorage para não estourar o limite de 60 requisições/hora da API anônima
  function lerCache(chave) {
    try {
      const item = JSON.parse(sessionStorage.getItem(chave));
      if (item && Date.now() - item.t < CACHE_MIN * 60 * 1000) return item.d;
    } catch (e) { /* sem storage */ }
    return null;
  }

  function gravarCache(chave, dados) {
    try { sessionStorage.setItem(chave, JSON.stringify({ t: Date.now(), d: dados })); } catch (e) { /* sem storage */ }
  }

  async function buscar(caminho) {
    const chave = "gh:" + caminho;
    const emCache = lerCache(chave);
    if (emCache) return emCache;
    const resp = await fetch(API + caminho, { headers: { Accept: "application/vnd.github+json" } });
    if (!resp.ok) throw new Error(resp.status === 403 || resp.status === 429 ? "limite" : "http " + resp.status);
    const dados = await resp.json();
    gravarCache(chave, dados);
    return dados;
  }

  function linkSeguro(url) {
    try {
      const u = new URL(url);
      return u.protocol === "https:" ? u.href : null;
    } catch (e) {
      return null;
    }
  }

  function el(tag, classe, texto) {
    const n = document.createElement(tag);
    if (classe) n.className = classe;
    if (texto !== undefined && texto !== null) n.textContent = texto;
    return n;
  }

  function linkExterno(texto, url) {
    const href = linkSeguro(url);
    if (!href) return null;
    const a = el("a", null, texto);
    a.href = href;
    a.target = "_blank";
    a.rel = "noopener noreferrer";
    return a;
  }

  function dataCurta(iso) {
    return new Date(iso).toLocaleDateString("pt-BR", { day: "2-digit", month: "short", year: "numeric" });
  }

  // ---------- Repositórios ----------
  const lista = document.getElementById("repo-lista");
  const status = document.getElementById("repo-status");
  const filtro = document.getElementById("repo-filtro");
  let repos = [];

  function cardRepo(r) {
    const card = el("article", "card");
    const tags = el("div", "tag-row");
    tags.append(el("span", "tag cat", "Repositório"));
    if (r.topics) r.topics.slice(0, 3).forEach((t) => tags.append(el("span", "tag", t)));
    card.append(tags, el("h3", null, r.name), el("p", null, r.description || "Sem descrição."));

    const meta = el("div", "repo-meta");
    if (r.language) {
      const lang = el("span");
      const dot = el("span", "lang-dot");
      dot.style.background = CORES[r.language] || "";
      lang.append(dot, document.createTextNode(r.language));
      meta.append(lang);
    }
    meta.append(el("span", null, "★ " + r.stargazers_count));
    meta.append(el("span", null, "Atualizado em " + dataCurta(r.pushed_at)));
    card.append(meta);

    const links = el("div", "links");
    const codigo = linkExterno("Código →", r.html_url);
    if (codigo) links.append(codigo);
    const site = r.homepage ? linkExterno("Site →", r.homepage)
      : r.has_pages ? linkExterno("Site →", "https://" + USUARIO.toLowerCase() + ".github.io/" + r.name + "/") : null;
    if (site) links.append(site);
    card.append(links);
    return card;
  }

  function renderizar() {
    const termo = (filtro.value || "").trim().toLowerCase();
    const visiveis = repos.filter((r) =>
      [r.name, r.language, r.description].join(" ").toLowerCase().includes(termo)
    );
    lista.replaceChildren(...visiveis.map(cardRepo));
    status.textContent = visiveis.length + " de " + repos.length + " repositórios públicos";
  }

  async function carregarRepos() {
    if (!lista) return;
    try {
      const dados = await doBuildOuApi("repos", "/users/" + USUARIO + "/repos?per_page=100&sort=pushed");
      // Só repositórios próprios e ativos: forks e arquivados diluiriam a seleção
      repos = dados.filter((r) => !r.fork && !r.archived);
      renderizar();
      filtro.addEventListener("input", renderizar);
    } catch (e) {
      status.textContent = e.message === "limite"
        ? "Limite da API do GitHub atingido. Tente de novo em alguns minutos."
        : "Não foi possível carregar os repositórios agora.";
      const a = linkExterno("Ver no GitHub →", "https://github.com/" + USUARIO + "?tab=repositories");
      if (a) lista.replaceChildren(a);
    }
  }

  // ---------- Painel de implantação ----------
  async function carregarStatus() {
    const rel = document.getElementById("st-release");
    if (!rel) return;
    try {
      const r = await doBuildOuApi("release", "/repos/" + REPO + "/releases/latest");
      rel.textContent = r.tag_name;
      document.getElementById("st-release-data").textContent = "publicada em " + dataCurta(r.published_at);
    } catch (e) {
      rel.textContent = "indisponível";
    }
    try {
      const build = await dadosBuild;
      let c = build && build.commit;
      if (!c) {
        const commits = await buscar("/repos/" + REPO + "/commits?per_page=1");
        c = { sha: commits[0].sha, message: commits[0].commit.message, date: commits[0].commit.committer.date };
      }
      document.getElementById("st-commit").textContent = c.sha.slice(0, 7);
      document.getElementById("st-commit-data").textContent =
        c.message.split("\n")[0] + " · " + dataCurta(c.date);
    } catch (e) {
      document.getElementById("st-commit").textContent = "indisponível";
    }
  }

  async function carregarEquipe() {
    const ul = document.getElementById("equipe");
    if (!ul) return;
    try {
      const pessoas = await doBuildOuApi("contribuidores", "/repos/" + REPO + "/contributors?per_page=20");
      ul.replaceChildren(...pessoas.filter((p) => p.type === "User").map((p) => {
        const li = el("li");
        const img = el("img");
        const avatar = linkSeguro(p.avatar_url);
        if (avatar) img.src = avatar;
        img.alt = "";
        img.loading = "lazy";
        const info = el("div");
        const nome = linkExterno("@" + p.login, p.html_url) || el("span", null, "@" + p.login);
        const papel = el("span", null, (p.login === USUARIO ? "Mantenedor · " : "Colaborador · ") + p.contributions + " commits");
        info.append(nome, papel);
        li.append(img, info);
        return li;
      }));
    } catch (e) {
      ul.replaceChildren(el("li", "muted", "Equipe indisponível no momento."));
    }
  }

  carregarRepos();
  carregarStatus();
  carregarEquipe();
})();
