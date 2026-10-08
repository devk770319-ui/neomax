/* NeoMax — site interactions */
(() => {
  const d = document;
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;

  // header state
  const header = d.querySelector('.site-header');
  const onScroll = () => header && header.classList.toggle('scrolled', window.scrollY > 8);
  onScroll();
  window.addEventListener('scroll', onScroll, { passive: true });

  // mobile menu
  const mbtn = d.querySelector('.menu-btn');
  const mmenu = d.querySelector('.mobile-menu');
  if (mbtn && mmenu) {
    const set = (open) => { d.body.classList.toggle('menu-open', open); mbtn.setAttribute('aria-expanded', String(open)); };
    mbtn.addEventListener('click', () => set(!d.body.classList.contains('menu-open')));
    mmenu.querySelectorAll('a').forEach((a) => a.addEventListener('click', () => set(false)));
    window.addEventListener('resize', () => { if (window.innerWidth > 920) set(false); });
  }

  // reveal on scroll
  const els = d.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window && !reduce) {
    const io = new IntersectionObserver((entries) => {
      entries.forEach((e) => {
        if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); }
      });
    }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });
    els.forEach((el) => io.observe(el));
  } else {
    els.forEach((el) => el.classList.add('in'));
  }

  // hero parallax
  const hv = d.querySelector('[data-parallax]');
  if (hv && !reduce && matchMedia('(pointer: fine)').matches) {
    const area = hv.closest('section') || hv;
    area.addEventListener('pointermove', (e) => {
      const r = hv.getBoundingClientRect();
      hv.style.setProperty('--px', ((e.clientX - r.left) / r.width - 0.5).toFixed(3));
      hv.style.setProperty('--py', ((e.clientY - r.top) / r.height - 0.5).toFixed(3));
    });
    area.addEventListener('pointerleave', () => { hv.style.setProperty('--px', 0); hv.style.setProperty('--py', 0); });
  }

  // screenshot gallery arrows
  d.querySelectorAll('[data-gallery]').forEach((wrap) => {
    const g = wrap.querySelector('.gallery');
    d.querySelectorAll(`[data-gallery-target="${wrap.id}"] [data-dir]`).forEach((b) => {
      b.addEventListener('click', () => {
        g.scrollBy({ left: (b.dataset.dir === 'next' ? 1 : -1) * g.clientWidth * 0.8, behavior: 'smooth' });
      });
    });
  });

  // lightbox
  const lb = d.querySelector('.lightbox');
  if (lb) {
    const img = lb.querySelector('img');
    const count = lb.querySelector('.lb-count');
    let list = [];
    let idx = 0;
    const show = (i) => {
      idx = (i + list.length) % list.length;
      img.src = list[idx].dataset.full || list[idx].src;
      img.alt = list[idx].alt;
      count.textContent = `${idx + 1} / ${list.length}`;
    };
    const shots = [...d.querySelectorAll('.gallery .shot')];
    shots.forEach((s, i) => {
      s.addEventListener('click', () => {
        list = shots.map((x) => x.querySelector('img'));
        show(i);
        lb.classList.add('open');
        d.body.style.overflow = 'hidden';
      });
    });
    const close = () => { lb.classList.remove('open'); d.body.style.overflow = ''; };
    lb.querySelector('.lb-close').addEventListener('click', close);
    lb.querySelector('.lb-prev').addEventListener('click', (e) => { e.stopPropagation(); show(idx - 1); });
    lb.querySelector('.lb-next').addEventListener('click', (e) => { e.stopPropagation(); show(idx + 1); });
    lb.addEventListener('click', (e) => { if (e.target === lb) close(); });
    d.addEventListener('keydown', (e) => {
      if (!lb.classList.contains('open')) return;
      if (e.key === 'Escape') close();
      if (e.key === 'ArrowLeft') show(idx - 1);
      if (e.key === 'ArrowRight') show(idx + 1);
    });
    // swipe
    let sx = null;
    lb.addEventListener('touchstart', (e) => { sx = e.touches[0].clientX; }, { passive: true });
    lb.addEventListener('touchend', (e) => {
      if (sx === null) return;
      const dx = e.changedTouches[0].clientX - sx;
      if (Math.abs(dx) > 50) show(idx + (dx < 0 ? 1 : -1));
      sx = null;
    });
  }

  // copy e-mail
  d.querySelectorAll('[data-copy]').forEach((b) => {
    b.addEventListener('click', async () => {
      const label = b.querySelector('.copy-label');
      try {
        await navigator.clipboard.writeText(b.dataset.copy);
        const old = label.textContent;
        label.textContent = '복사했어요';
        b.classList.add('copied');
        setTimeout(() => { label.textContent = old; b.classList.remove('copied'); }, 1800);
      } catch (_) { /* clipboard blocked */ }
    });
  });

  const y = d.querySelector('[data-year]');
  if (y) y.textContent = new Date().getFullYear();
})();
