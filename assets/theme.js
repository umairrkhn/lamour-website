'use strict';

class LamourThemeToggle extends HTMLElement {
  connectedCallback() {
    this.button = this.querySelector('button');
    this.apply(this.current());
    this.button?.addEventListener('click', () => this.toggle());
  }

  current() {
    return localStorage.getItem('lm-theme')
      || (matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
  }

  apply(theme) {
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('lm-theme', theme);
    if (this.button) {
      this.button.setAttribute('aria-label', theme === 'dark' ? 'Zum hellen Modus wechseln' : 'Zum dunklen Modus wechseln');
      this.button.setAttribute('aria-pressed', theme === 'dark' ? 'true' : 'false');
    }
  }

  toggle() {
    this.apply(document.documentElement.getAttribute('data-theme') === 'dark' ? 'light' : 'dark');
  }
}
customElements.define('lamour-theme-toggle', LamourThemeToggle);

class LamourCursor extends HTMLElement {
  connectedCallback() {
    if (!matchMedia('(hover: hover) and (pointer: fine)').matches) return;
    const dot  = document.querySelector('.cursor-dot');
    const ring = document.querySelector('.cursor-ring');
    if (!dot || !ring) return;
    let rx = -100, ry = -100, mx = -100, my = -100;
    const lerp = (a, b, t) => a + (b - a) * t;

    document.addEventListener('mousemove', e => { mx = e.clientX; my = e.clientY; });
    document.addEventListener('mousedown', () => document.documentElement.classList.add('cursor-press'));
    document.addEventListener('mouseup',   () => document.documentElement.classList.remove('cursor-press'));

    document.querySelectorAll('a, button, [data-hover]').forEach(el => {
      el.addEventListener('mouseenter', () => document.documentElement.classList.add('cursor-hover'));
      el.addEventListener('mouseleave', () => document.documentElement.classList.remove('cursor-hover'));
    });

    const tick = () => {
      rx = lerp(rx, mx, 0.12); ry = lerp(ry, my, 0.12);
      dot.style.transform  = `translate3d(${mx}px,${my}px,0)`;
      ring.style.transform = `translate3d(${rx}px,${ry}px,0)`;
      ring.style.setProperty('--cx', `${rx}px`);
      ring.style.setProperty('--cy', `${ry}px`);
      requestAnimationFrame(tick);
    };
    requestAnimationFrame(tick);
  }
}
customElements.define('lamour-cursor', LamourCursor);

class LamourReveal extends HTMLElement {
  connectedCallback() {
    if (matchMedia('(prefers-reduced-motion: reduce)').matches) return;
    const io = new IntersectionObserver(entries => {
      entries.forEach(e => {
        if (e.isIntersecting) {
          e.target.classList.add('in');
          io.unobserve(e.target);
        }
      });
    }, { threshold: 0.12 });
    document.querySelectorAll('.reveal').forEach(el => io.observe(el));
  }
}
customElements.define('lamour-reveal', LamourReveal);

class LamourHeader extends HTMLElement {
  connectedCallback() {
    const header = this.closest('header') || document.querySelector('.lm-header');
    if (!header) return;
    let ticking = false;
    window.addEventListener('scroll', () => {
      if (!ticking) {
        requestAnimationFrame(() => {
          header.classList.toggle('scrolled', window.scrollY > 40);
          ticking = false;
        });
        ticking = true;
      }
    }, { passive: true });
  }
}
customElements.define('lamour-header', LamourHeader);

class LamourMobileMenu extends HTMLElement {
  connectedCallback() {
    this.toggle = this.querySelector('[data-menu-toggle]');
    this.overlay = document.querySelector('.lm-nav-overlay');
    this.toggle?.addEventListener('click', () => this.open());
    this.overlay?.querySelector('[data-menu-close]')?.addEventListener('click', () => this.close());
    document.addEventListener('keydown', e => { if (e.key === 'Escape') this.close(); });
  }

  open() {
    this.overlay?.classList.add('open');
    document.body.style.overflow = 'hidden';
  }

  close() {
    this.overlay?.classList.remove('open');
    document.body.style.overflow = '';
  }
}
customElements.define('lamour-mobile-menu', LamourMobileMenu);
