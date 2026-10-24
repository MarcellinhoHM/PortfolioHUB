// PortfolioHUB — navegação compartilhada das apresentações
(function () {
  const stage = document.getElementById("stage");
  const slides = Array.from(document.querySelectorAll(".slide"));
  const counter = document.getElementById("counter");
  const progress = document.getElementById("progress");
  let i = 0;

  const fromHash = parseInt(location.hash.replace("#", ""), 10);
  if (fromHash >= 1 && fromHash <= slides.length) i = fromHash - 1;

  function fit() {
    const s = Math.min(window.innerWidth / 1280, (window.innerHeight - 56) / 720);
    stage.style.transform = "translate(-50%, -50%) scale(" + Math.max(s, 0.1) + ")";
  }

  function show(n) {
    i = Math.max(0, Math.min(slides.length - 1, n));
    slides.forEach((el, k) => el.classList.toggle("active", k === i));
    counter.textContent = (i + 1) + " / " + slides.length;
    progress.style.width = ((i + 1) / slides.length * 100) + "%";
    history.replaceState(null, "", "#" + (i + 1));
  }

  document.getElementById("prev").onclick = () => show(i - 1);
  document.getElementById("next").onclick = () => show(i + 1);
  document.getElementById("fs").onclick = () => {
    if (!document.fullscreenElement) document.documentElement.requestFullscreen?.();
    else document.exitFullscreen?.();
  };

  document.addEventListener("keydown", (e) => {
    if (["ArrowRight", "PageDown", " "].includes(e.key)) { e.preventDefault(); show(i + 1); }
    if (["ArrowLeft", "PageUp"].includes(e.key)) { e.preventDefault(); show(i - 1); }
    if (e.key === "Home") show(0);
    if (e.key === "End") show(slides.length - 1);
    if (e.key === "f" || e.key === "F") document.getElementById("fs").click();
  });

  let x0 = null;
  document.addEventListener("touchstart", (e) => { x0 = e.touches[0].clientX; }, { passive: true });
  document.addEventListener("touchend", (e) => {
    if (x0 === null) return;
    const dx = e.changedTouches[0].clientX - x0;
    if (Math.abs(dx) > 40) show(i + (dx < 0 ? 1 : -1));
    x0 = null;
  });

  window.addEventListener("resize", fit);
  fit();
  show(i);
})();
