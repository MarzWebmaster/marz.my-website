// Mobile menu toggle
document.addEventListener('DOMContentLoaded', function() {
  const toggle = document.querySelector('.menu-toggle');
  const header = document.querySelector('.header');
  if (toggle) {
    toggle.addEventListener('click', function() {
      header.classList.toggle('nav-open');
    });
  }

  // Scroll animations
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
      }
    });
  }, { threshold: 0.1 });
  document.querySelectorAll('.animate-on-scroll').forEach(el => observer.observe(el));

  // Header scroll effect
  let lastScroll = 0;
  window.addEventListener('scroll', () => {
    const current = window.scrollY;
    if (current > 100) {
      header.style.background = 'rgba(10,22,40,.98)';
    } else {
      header.style.background = 'rgba(10,22,40,.95)';
    }
    lastScroll = current;
  });

  // Active nav link
  const path = window.location.pathname.split('/').pop() || 'index.html';
  document.querySelectorAll('.nav-link').forEach(link => {
    if (link.getAttribute('href') === path) {
      link.classList.add('active');
    }
  });

  // Contact form handler
  const form = document.getElementById('contactForm');
  if (form) {
    form.addEventListener('submit', function(e) {
      e.preventDefault();
      const btn = this.querySelector('button[type="submit"]');
      const original = btn.innerHTML;
      btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Sending...';
      btn.disabled = true;
      // Submit with fetch to Formspree or similar
      fetch(this.action, {
        method: 'POST',
        body: new FormData(this),
        headers: { 'Accept': 'application/json' }
      }).then(r => {
        if (r.ok) {
          btn.innerHTML = '<i class="fas fa-check"></i> Sent!';
          this.reset();
          setTimeout(() => { btn.innerHTML = original; btn.disabled = false; }, 3000);
        } else {
          btn.innerHTML = '<i class="fas fa-exclamation"></i> Error';
          setTimeout(() => { btn.innerHTML = original; btn.disabled = false; }, 3000);
        }
      }).catch(() => {
        btn.innerHTML = '<i class="fas fa-exclamation"></i> Error';
        setTimeout(() => { btn.innerHTML = original; btn.disabled = false; }, 3000);
      });
    });
  }
});
