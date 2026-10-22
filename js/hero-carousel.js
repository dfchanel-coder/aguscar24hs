(function(){
  const root = document.querySelector('[data-hero-carousel]');
  if(!root) return;
  const slides = Array.from(root.querySelectorAll('[data-slide]'));
  const dots = Array.from(root.querySelectorAll('[data-dot]'));
  if(slides.length < 2) return;
  let idx = 0;
  let timer;

  function go(n){
    slides[idx].classList.remove('is-active');
    dots[idx].classList.remove('is-active');
    idx = (n + slides.length) % slides.length;
    slides[idx].classList.add('is-active');
    dots[idx].classList.add('is-active');
  }

  dots.forEach((d,i)=>d.addEventListener('click', ()=>{ go(i); restart(); }));

  function restart(){
    clearInterval(timer);
    timer = setInterval(()=>go(idx+1), 5500);
  }
  restart();

  // respect reduced motion
  if(window.matchMedia('(prefers-reduced-motion: reduce)').matches){
    clearInterval(timer);
  }
})();
