/* Mejora progresiva: sin JavaScript permanece visible la primera fotografía. */
(() => {
  const root = document.querySelector('[data-hero-carousel]');
  if (!root) return;
  const slides = [...root.querySelectorAll('[data-slide]')];
  const dots = [...root.querySelectorAll('[data-dot]')];
  const controls = root.querySelector('[data-carousel-controls]');
  const toggle = root.querySelector('[data-carousel-toggle]');
  if (slides.length < 2 || dots.length !== slides.length || !controls || !toggle) return;

  const motion = window.matchMedia('(prefers-reduced-motion: reduce)');
  let index = 0;
  let timer = null;
  let paused = false;
  let hovered = false;
  let focused = false;

  function stop() {
    if (timer !== null) window.clearInterval(timer);
    timer = null;
  }

  function go(next) {
    index = (next + slides.length) % slides.length;
    slides.forEach((slide, i) => { slide.hidden = i !== index; });
    dots.forEach((dot, i) => {
      if (i === index) dot.setAttribute('aria-current', 'true');
      else dot.removeAttribute('aria-current');
    });
  }

  function sync() {
    stop();
    toggle.disabled = motion.matches;
    toggle.textContent = motion.matches ? root.dataset.motionLabel :
      paused ? root.dataset.playLabel : root.dataset.pauseLabel;
    if (motion.matches || paused || hovered || focused || document.hidden) return;
    timer = window.setInterval(() => go(index + 1), 6500);
  }

  // Los botones nativos ya ofrecen Enter y Espacio: no duplicar sus eventos.
  dots.forEach((dot, i) => dot.addEventListener('click', () => { go(i); sync(); }));
  toggle.addEventListener('click', () => { paused = !paused; sync(); });
  root.addEventListener('mouseenter', () => { hovered = true; sync(); });
  root.addEventListener('mouseleave', () => { hovered = false; sync(); });
  root.addEventListener('focusin', () => { focused = true; sync(); });
  root.addEventListener('focusout', () => {
    queueMicrotask(() => { focused = root.contains(document.activeElement); sync(); });
  });
  document.addEventListener('visibilitychange', sync);
  motion.addEventListener('change', sync);
  controls.hidden = false;
  go(0);
  sync();
})();
