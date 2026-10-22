const { test } = require('node:test');
const assert = require('node:assert/strict');
const vm = require('node:vm');
const fs = require('node:fs');
const path = require('node:path');
const code = fs.readFileSync(path.join(__dirname, '../js/hero-carousel.js'), 'utf8');

function element() {
  const handlers = {};
  const attrs = {};
  return {
    hidden: false, disabled: false, textContent: '',
    addEventListener(type, fn) { handlers[type] = fn; },
    setAttribute(name, value) { attrs[name] = value; },
    removeAttribute(name) { delete attrs[name]; },
    emit(type) { handlers[type]?.(); },
    attrs,
  };
}

function fixture(reduced = false) {
  const slides = [element(), element(), element()];
  const dots = [element(), element(), element()];
  const controls = element();
  const toggle = element();
  const root = element();
  const media = element();
  media.matches = reduced;
  root.dataset = { pauseLabel: 'Pausar', playLabel: 'Reanudar', motionLabel: 'Modo manual' };
  root.querySelectorAll = selector => selector === '[data-slide]' ? slides : dots;
  root.querySelector = selector => selector === '[data-carousel-controls]' ? controls : toggle;
  root.contains = el => el === toggle || dots.includes(el);
  const document = element();
  document.hidden = false;
  document.activeElement = null;
  document.querySelector = () => root;
  const timers = new Map();
  let id = 0;
  const window = {
    matchMedia: () => media,
    setInterval(fn) { timers.set(++id, fn); return id; },
    clearInterval(timer) { timers.delete(timer); },
  };
  vm.runInNewContext(code, { document, window, queueMicrotask });
  return { slides, dots, controls, toggle, root, media, document, timers };
}

test('con movimiento reducido, la selección manual nunca inicia el temporizador', () => {
  const f = fixture(true);
  assert.equal(f.timers.size, 0);
  assert.equal(f.toggle.disabled, true);
  f.dots[1].emit('click');
  assert.equal(f.slides[1].hidden, false);
  assert.equal(f.slides[0].hidden, true);
  assert.equal(f.timers.size, 0);
});

test('pausar conserva la selección manual hasta reanudar', () => {
  const f = fixture();
  assert.equal(f.timers.size, 1);
  f.toggle.emit('click');
  assert.equal(f.timers.size, 0);
  assert.equal(f.toggle.textContent, 'Reanudar');
  f.dots[2].emit('click');
  assert.equal(f.slides[2].hidden, false);
  assert.equal(f.timers.size, 0);
  f.toggle.emit('click');
  assert.equal(f.timers.size, 1);
});

test('la pestaña oculta, el puntero y el foco suspenden la rotación', async () => {
  const f = fixture();
  f.document.hidden = true;
  f.document.emit('visibilitychange');
  assert.equal(f.timers.size, 0);
  f.document.hidden = false;
  f.document.emit('visibilitychange');
  assert.equal(f.timers.size, 1);
  f.root.emit('mouseenter');
  assert.equal(f.timers.size, 0);
  f.root.emit('mouseleave');
  assert.equal(f.timers.size, 1);
  f.document.activeElement = f.dots[0];
  f.root.emit('focusin');
  assert.equal(f.timers.size, 0);
  f.root.emit('focusout');
  await Promise.resolve();
  assert.equal(f.timers.size, 0, 'el foco sigue en los controles');
  f.document.activeElement = null;
  f.root.emit('focusout');
  await Promise.resolve();
  assert.equal(f.timers.size, 1);
});

test('un cambio de preferencia de movimiento detiene la rotación activa', () => {
  const f = fixture();
  [...f.timers.values()][0]();
  assert.equal(f.slides[1].hidden, false);
  f.media.matches = true;
  f.media.emit('change');
  assert.equal(f.timers.size, 0);
  assert.equal(f.toggle.disabled, true);
  f.dots[0].emit('click');
  assert.equal(f.timers.size, 0);
});
