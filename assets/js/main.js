// PortfolioHUB — interações do site

(function () {
  const root = document.documentElement;
  // Marca que o JavaScript está ativo: só então as seções começam ocultas para a animação.
  // Sem JavaScript, todo o conteúdo fica visível.
  root.classList.add("js");

  // Tema claro/escuro (lembra a escolha do visitante)
  const themeBtn = document.getElementById("theme-toggle");
  const saved = (() => {
    try { return localStorage.getItem("theme"); } catch (e) { return null; }
  })();
  if (saved) root.setAttribute("data-theme", saved);

  function currentTheme() {
    const attr = root.getAttribute("data-theme");
    if (attr) return attr;
    return window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";
  }

  function updateIcon() {
    if (themeBtn) themeBtn.textContent = currentTheme() === "dark" ? "☀" : "☾";
  }

  if (themeBtn) {
    themeBtn.addEventListener("click", () => {
      const next = currentTheme() === "dark" ? "light" : "dark";
      root.setAttribute("data-theme", next);
      try { localStorage.setItem("theme", next); } catch (e) { /* sem storage */ }
      updateIcon();
    });
  }
  updateIcon();

  // Menu mobile
  const menuBtn = document.getElementById("menu-toggle");
  const nav = document.getElementById("nav");
  if (menuBtn && nav) {
    const definirMenu = (aberto) => {
      nav.classList.toggle("open", aberto);
      menuBtn.setAttribute("aria-expanded", String(aberto));
      menuBtn.setAttribute("aria-label", aberto ? "Fechar menu" : "Abrir menu");
    };
    menuBtn.addEventListener("click", () => definirMenu(!nav.classList.contains("open")));
    nav.querySelectorAll("a").forEach((a) => a.addEventListener("click", () => definirMenu(false)));
  }

  // Animação de entrada das seções
  const items = document.querySelectorAll(".reveal");
  if ("IntersectionObserver" in window) {
    const io = new IntersectionObserver((entries) => {
      entries.forEach((e) => {
        if (e.isIntersecting) {
          e.target.classList.add("visible");
          io.unobserve(e.target);
        }
      });
    }, { threshold: 0.1 });
    items.forEach((el) => io.observe(el));
  } else {
    items.forEach((el) => el.classList.add("visible"));
  }

  // Ano no rodapé
  const year = document.getElementById("year");
  if (year) year.textContent = new Date().getFullYear();
})();
