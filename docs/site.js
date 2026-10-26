'use strict';
const assetBase = new URL('assets/', document.currentScript.src);
const comparison = document.querySelector('[data-player-comparison]');
if (comparison) {
  const image = comparison.querySelector('#comparison-image');
  const switcher = comparison.querySelector('.state-switch');
  const state = comparison.querySelector('.capture-state');
  const captureLink = comparison.querySelector('.capture-link');
  const enlargeLink = comparison.querySelector('.enlarge-link');
  const buttons = [...switcher.querySelectorAll('button[data-state]')];
  let request = 0;

  // Load and decode before swapping: a failed request never removes the honest fallback.
  switcher.addEventListener('click', async event => {
    const button = event.target.closest('button[data-state]');
    if (!button || !switcher.contains(button)) return;
    const currentRequest = ++request;
    const controls = button.dataset.state === 'controls';
    const name = controls ? 'controls' : 'clean';
    const src = new URL(`desktop-${name}-1152.webp`, assetBase).href;
    const srcset = `${new URL(`desktop-${name}-384.webp`, assetBase).href} 384w, ${new URL(`desktop-${name}-768.webp`, assetBase).href} 768w, ${src} 1152w`;
    const next = new Image();
    next.sizes = image.sizes;
    next.srcset = srcset;
    next.src = src;
    try {
      await next.decode();
    } catch {
      if (currentRequest === request) state.textContent = 'Capture unavailable. Please try again.';
      return;
    }
    if (currentRequest !== request) return;
    image.srcset = srcset;
    image.src = src;
    image.alt = `The same Caminandes frame in kurtz on a staged Mac desktop, with playback controls ${controls ? 'visible' : 'hidden'}. Finder, Notes and the pug wallpaper remain unchanged.`;
    state.textContent = controls ? 'Controls visible' : 'Controls hidden';
    captureLink.href = enlargeLink.href = src;
    captureLink.setAttribute('aria-label', `Open the full-size Mac capture: controls ${controls ? 'visible' : 'hidden'}`);
    buttons.forEach(item => item.setAttribute('aria-pressed', String(item === button)));
  });
  switcher.hidden = false;
  comparison.querySelector('.comparison-fallback').hidden = true;
}
