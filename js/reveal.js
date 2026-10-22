/* El contenido nunca se oculta: las animaciones son exclusivamente decorativas. */
(() => {
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches ||
      !('IntersectionObserver' in window)) return;
  const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (!entry.isIntersecting) return;
      entry.target.classList.add('reveal-animate');
      observer.unobserve(entry.target);
    });
  }, { threshold: 0.12 });
  document.querySelectorAll('.service-card, .plan, .coverage-photo')
    .forEach(element => observer.observe(element));
})();
