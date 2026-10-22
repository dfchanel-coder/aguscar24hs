(function(){
  const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if(reduce) return;
  const els = document.querySelectorAll('.section, .service-card, .split, .faq-item, .footer-card');
  els.forEach(el=>el.classList.add('reveal'));
  const io = new IntersectionObserver((entries)=>{
    entries.forEach(e=>{
      if(e.isIntersecting){
        e.target.classList.add('in-view');
        io.unobserve(e.target);
      }
    });
  }, {threshold: 0.12});
  els.forEach(el=>io.observe(el));
})();
