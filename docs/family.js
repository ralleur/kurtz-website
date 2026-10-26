'use strict';
// Preserve the previous public player anchors when the root becomes the portal.
if (['#experience', '#platforms', '#foundation', '#get-kurtz'].includes(location.hash) && /\/(?:index\.html)?$/.test(location.pathname)) {
  location.replace(new URL(`player/${location.hash}`, location.href));
}

// The artwork stays untouched. One short, local scene is enough company.
(() => {
  const images = [...document.querySelectorAll('.kurt-scene')];
  const control = document.querySelector('[data-motion-toggle]');
  if (!images.length || !control) return;
  const preference = matchMedia('(prefers-reduced-motion: reduce)');
  let enabled = true;
  const scenes = images.map((image, index) => ({ image, index, poster: image.getAttribute('src'), card: image.closest('.destination'), visible: false, seen: false, active: false, pending: false, timer: null, delay: null, token: 0 }));
  function updateControl() {
    control.hidden = preference.matches;
    const playing = scenes.some(scene => scene.active || scene.pending || scene.delay != null);
    control.querySelector('[data-motion-label]').textContent = playing ? 'Pause animations' : 'Play Kurt';
    control.firstElementChild.textContent = playing ? 'Ⅱ' : '▷';
  }
  function stop(scene) {
    scene.token++;
    clearTimeout(scene.timer);
    clearTimeout(scene.delay);
    scene.timer = scene.delay = null;
    scene.active = scene.pending = false;
    scene.image.src = scene.poster;
    updateControl();
  }
  async function play(scene) {
    if (!enabled || preference.matches || document.hidden || !scene.visible || scene.active || scene.pending) return;
    scene.pending = true;
    const token = ++scene.token;
    updateControl();
    const animation = new Image();
    animation.src = scene.image.dataset.animatedSrc;
    try { await animation.decode(); } catch { if (token === scene.token) stop(scene); return; }
    if (token !== scene.token || !enabled || preference.matches || document.hidden || !scene.visible) return;
    scene.pending = false;
    scene.active = scene.seen = true;
    scene.image.src = scene.image.dataset.animatedSrc;
    scene.timer = setTimeout(() => stop(scene), Number(scene.image.dataset.duration));
    updateControl();
  }
  function firstVisit(scene) {
    if (scene.seen || !enabled || preference.matches || document.hidden) return;
    clearTimeout(scene.delay);
    scene.delay = setTimeout(() => { scene.delay = null; play(scene); }, scene.index * 260);
    updateControl();
  }
  const observer = new IntersectionObserver(entries => {
    for (const entry of entries) {
      const scene = scenes.find(item => item.card === entry.target);
      scene.visible = entry.isIntersecting && entry.intersectionRatio >= .45;
      if (scene.visible) firstVisit(scene); else stop(scene);
    }
  }, { threshold: [0, .45] });
  scenes.forEach(scene => {
    observer.observe(scene.card);
    scene.card.addEventListener('pointerenter', event => { if (event.pointerType !== 'touch') play(scene); });
    scene.card.addEventListener('focusin', () => play(scene));
    scene.card.addEventListener('pointerleave', () => stop(scene));
    scene.card.addEventListener('focusout', () => stop(scene));
  });
  control.addEventListener('click', () => {
    const playing = scenes.some(scene => scene.active || scene.pending || scene.delay != null);
    if (playing) { enabled = false; scenes.forEach(stop); }
    else { enabled = true; scenes.filter(scene => scene.visible).forEach(scene => play(scene)); }
    updateControl();
  });
  preference.addEventListener('change', () => { scenes.forEach(stop); updateControl(); });
  document.addEventListener('visibilitychange', () => {
    if (document.hidden) scenes.forEach(stop); else scenes.filter(scene => scene.visible).forEach(firstVisit);
  });
  updateControl();
})();
