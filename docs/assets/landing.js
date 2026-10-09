/* The annotation follows real page elements. Material remounts it on navigation. */
(() => {
  'use strict';
  let dispose = () => {};
  function mount() {
    dispose();
    const hero = document.querySelector('[data-mk-hero]');
    const search = document.querySelector('.mk-search-trigger');
    function searchKey(event) {
      if (event.key === 'Enter' || event.key === ' ') {event.preventDefault(); search.click();}
    }
    function syncHeader() {
      if (hero) return;
      const animation = selector => document.querySelector(selector)?.getAnimations()
        .find(item => item.animationName === 'mk-header-flow');
      const header = animation('.md-header'), tabs = animation('.md-tabs');
      if (header && tabs && header.currentTime !== null) tabs.currentTime = header.currentTime;
    }
    search?.addEventListener('keydown', searchKey);
    window.addEventListener('resize', syncHeader);
    syncHeader();
    const cleanupHeader = () => {
      search?.removeEventListener('keydown', searchKey);
      window.removeEventListener('resize', syncHeader);
    };
    dispose = cleanupHeader;
    if (!hero) return;
    const marker = hero.querySelector('.mk-marker');
    const targets = [...hero.querySelectorAll('[data-mk-target]')];
    const pause = hero.querySelector('[data-mk-pause]');
    const number = hero.querySelector('[data-mk-number]');
    const label = hero.querySelector('[data-mk-label]');
    const es = hero.dataset.lang === 'es';
    const labels = es ? ['El detalle', 'El mensaje', 'La acción'] : ['The detail', 'The message', 'The action'];
    const media = matchMedia('(prefers-reduced-motion: reduce)');
    const hold = 1.5, travel = 2, leg = hold + travel;
    let elapsed = 0, last = 0, frame = 0, paused = false, visible = true;
    let boxes = [], active = true;
    const stopped = () => paused || media.matches;

    function measure() {
      const h = hero.getBoundingClientRect();
      boxes = targets.map(target => {
        const r = target.getBoundingClientRect(), button = target.classList.contains('mk-primary');
        const pad = innerWidth < 680 ? (button ? 8 : 10) : (button ? 14 : 16);
        let left = r.left, width = r.width;
        if (!button) {
          const range = document.createRange();
          range.selectNodeContents(target);
          const text = range.getBoundingClientRect();
          const spacing = parseFloat(getComputedStyle(target).letterSpacing) || 0;
          if (text.width > 0) { left = text.left; width = Math.max(0, text.width - spacing); }
        }
        return {x: left - h.left - pad, y: r.top - h.top - pad, w: width + pad * 2, h: r.height + pad * 2};
      });
      render();
    }
    function render() {
      if (!boxes.length) return;
      const position = (elapsed / leg) % targets.length;
      const from = media.matches ? 0 : Math.floor(position), to = (from + 1) % targets.length;
      const local = (position - Math.floor(position)) * leg;
      const mix = media.matches ? 0 : Math.max(0, (local - hold) / travel);
      const a = boxes[from], b = boxes[to], lerp = (x, y) => x + (y - x) * mix;
      const ramp = Math.min(1, Math.max(0, Math.min(mix, 1 - mix) / .15));
      marker.style.transform = `translate3d(${lerp(a.x, b.x)}px,${lerp(a.y, b.y)}px,0)`;
      marker.style.width = lerp(a.w, b.w) + 'px';
      marker.style.height = lerp(a.h, b.h) + 'px';
      marker.style.opacity = String(1 - .65 * ramp * ramp * (3 - 2 * ramp));
      hero.dataset.mkStage = String(from);
      hero.dataset.mkPhase = mix > 0 ? 'travel' : 'hold';
      number.textContent = String(from + 1).padStart(2, '0');
      label.textContent = mix > 0 ? (es ? 'En tránsito' : 'In transit') : labels[from];
    }
    function tick(now) {
      frame = 0;
      if (!active || stopped() || !visible || document.hidden) { last = 0; return; }
      if (last) elapsed += Math.min((now - last) / 1000, .1);
      last = now;
      render();
      frame = requestAnimationFrame(tick);
    }
    function schedule() {
      if (active && !frame && !stopped() && visible && !document.hidden) frame = requestAnimationFrame(tick);
    }
    function controls() {
      hero.dataset.mkPaused = String(stopped());
      pause.textContent = stopped() ? (es ? 'Reanudar' : 'Resume') : (es ? 'Pausar' : 'Pause');
      pause.setAttribute('aria-pressed', String(stopped()));
      pause.disabled = media.matches;
      pause.title = media.matches ? (es ? 'Movimiento reducido: vista estática' : 'Reduced motion: static view') : '';
    }
    function toggle() { paused = !paused; controls(); last = 0; schedule(); }
    function preference() { last = 0; controls(); render(); schedule(); }
    function visibility() { last = 0; schedule(); }
    function focusContent(event) {
      const content = document.getElementById('mk-content');
      if (!content) return;
      event.preventDefault();
      content.focus({preventScroll: true});
      content.scrollIntoView({behavior: media.matches ? 'auto' : 'smooth'});
      history.replaceState(null, '', '#overview');
    }
    const resize = new ResizeObserver(measure);
    const intersection = new IntersectionObserver(entries => {
      visible = entries[0].isIntersecting; last = 0; schedule();
    }, {threshold: .05});
    const scrollLinks = [...hero.querySelectorAll('[data-mk-scroll]')];
    marker.hidden = false;
    hero.querySelector('.mk-marker-status').hidden = false;
    pause.hidden = false;
    resize.observe(hero);
    targets.forEach(target => resize.observe(target));
    intersection.observe(hero);
    pause.addEventListener('click', toggle);
    media.addEventListener('change', preference);
    document.addEventListener('visibilitychange', visibility);
    window.addEventListener('resize', measure);
    scrollLinks.forEach(link => link.addEventListener('click', focusContent));
    measure(); controls(); schedule();
    document.fonts.ready.then(() => {if (active) measure();});
    dispose = () => {
      cleanupHeader();
      active = false;
      cancelAnimationFrame(frame);
      resize.disconnect(); intersection.disconnect();
      pause.removeEventListener('click', toggle);
      media.removeEventListener('change', preference);
      document.removeEventListener('visibilitychange', visibility);
      window.removeEventListener('resize', measure);
      scrollLinks.forEach(link => link.removeEventListener('click', focusContent));
    };
  }
  if (typeof document$ !== 'undefined') document$.subscribe(mount);
  else if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', mount, {once: true});
  else mount();
})();
