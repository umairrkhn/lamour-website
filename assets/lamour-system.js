/* Lamour Design System v2.0 — Web Components */

/* ── Custom Cursor ──────────────────────────────────── */
class LamourCursor extends HTMLElement {
  connectedCallback() {
    if (!window.matchMedia('(hover: hover) and (pointer: fine)').matches) return;
    const dot = document.querySelector('.lm-cursor-dot');
    const ring = document.querySelector('.lm-cursor-ring');
    if (!dot || !ring) return;
    const mouse = { x: -100, y: -100 };
    const ringPos = { x: -100, y: -100 };
    let raf = 0;

    const onMove = (e) => {
      mouse.x = e.clientX;
      mouse.y = e.clientY;
      dot.style.transform = `translate3d(${e.clientX}px,${e.clientY}px,0)`;
      const t = e.target.closest('[data-hover], a, button, input[type="submit"], [role="button"], label');
      document.documentElement.classList.toggle('cursor-hover', !!t);
    };
    const onDown = () => document.documentElement.classList.add('cursor-press');
    const onUp = () => document.documentElement.classList.remove('cursor-press');
    const tick = () => {
      ringPos.x += (mouse.x - ringPos.x) * 0.18;
      ringPos.y += (mouse.y - ringPos.y) * 0.18;
      ring.style.transform = `translate3d(${ringPos.x}px,${ringPos.y}px,0)`;
      raf = requestAnimationFrame(tick);
    };

    window.addEventListener('mousemove', onMove, { passive: true });
    window.addEventListener('mousedown', onDown);
    window.addEventListener('mouseup', onUp);
    raf = requestAnimationFrame(tick);

    this._cleanup = () => {
      window.removeEventListener('mousemove', onMove);
      window.removeEventListener('mousedown', onDown);
      window.removeEventListener('mouseup', onUp);
      cancelAnimationFrame(raf);
      document.documentElement.classList.remove('cursor-hover', 'cursor-press');
    };
  }
  disconnectedCallback() { this._cleanup?.(); }
}

/* ── Scroll Reveal ──────────────────────────────────── */
class LamourReveal extends HTMLElement {
  connectedCallback() {
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
      document.querySelectorAll('[data-reveal]').forEach(el => el.classList.add('is-visible'));
      return;
    }
    const io = new IntersectionObserver((entries) => {
      entries.forEach(e => {
        if (e.isIntersecting) {
          e.target.classList.add('is-visible');
          io.unobserve(e.target);
        }
      });
    }, { threshold: 0.12, rootMargin: '0px 0px -8% 0px' });

    document.querySelectorAll('[data-reveal]').forEach(el => io.observe(el));
    this._io = io;
  }
  disconnectedCallback() { this._io?.disconnect(); }
}

/* ── Magnetic Button ────────────────────────────────── */
class LamourMagnetic extends HTMLElement {
  connectedCallback() {
    if (!window.matchMedia('(hover: hover) and (pointer: fine)').matches) return;
    const strength = parseFloat(this.dataset.strength || '0.35');
    const onMove = (e) => {
      const r = this.getBoundingClientRect();
      const x = e.clientX - (r.left + r.width / 2);
      const y = e.clientY - (r.top + r.height / 2);
      this.style.transform = `translate(${x * strength}px, ${y * strength}px)`;
    };
    const onLeave = () => { this.style.transform = ''; };
    this.addEventListener('mousemove', onMove);
    this.addEventListener('mouseleave', onLeave);
    this._cleanup = () => {
      this.removeEventListener('mousemove', onMove);
      this.removeEventListener('mouseleave', onLeave);
    };
  }
  disconnectedCallback() { this._cleanup?.(); }
}

/* ── Marquee Pause-on-hover ─────────────────────────── */
class LamourMarquee extends HTMLElement {
  connectedCallback() {
    const track = this.querySelector('.lm-marquee-track');
    if (!track) return;
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
      track.style.animationPlayState = 'paused';
      return;
    }
    this.addEventListener('mouseenter', () => { track.style.animationPlayState = 'paused'; });
    this.addEventListener('mouseleave', () => { track.style.animationPlayState = 'running'; });
  }
}

customElements.define('lamour-cursor', LamourCursor);
customElements.define('lamour-reveal', LamourReveal);
customElements.define('lamour-magnetic', LamourMagnetic);
customElements.define('lamour-marquee', LamourMarquee);
