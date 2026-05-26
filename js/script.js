// Marz Technology & Trading — Main Interactive Script
// Mobile menu, scroll effects, animations, email decode, form, back-to-top

document.addEventListener('DOMContentLoaded', function() {
  'use strict';

  // === 1. DECODE OBFUSCATED EMAILS ===
  document.querySelectorAll('.contact-email').forEach(function(el) {
    try {
      var user = atob(el.dataset.user);
      var domain = atob(el.dataset.domain);
      var email = user + '@' + domain;
      el.innerHTML = '<a href="mailto:' + email + '">' + email + '</a>';
    } catch(e) {
      // fallback if data attributes missing
    }
  });

  // === 2. MOBILE HAMBURGER MENU ===
  var toggle = document.querySelector('.menu-toggle');
  var header = document.querySelector('.header');
  if (toggle && header) {
    toggle.addEventListener('click', function() {
      header.classList.toggle('nav-open');
    });

    // Close menu on link click
    document.querySelectorAll('.nav-link').forEach(function(link) {
      link.addEventListener('click', function() {
        header.classList.remove('nav-open');
      });
    });
  }

  // === 3. HEADER SCROLL EFFECT ===
  function handleScroll() {
    if (window.scrollY > 50) {
      header.classList.add('scrolled');
    } else {
      header.classList.remove('scrolled');
    }
  }
  window.addEventListener('scroll', handleScroll, { passive: true });
  handleScroll(); // Check initial state

  // === 4. ACTIVE NAV LINK ===
  var path = window.location.pathname.split('/').pop() || 'index.html';
  document.querySelectorAll('.nav-link').forEach(function(link) {
    if (link.getAttribute('href') === path) {
      link.classList.add('active');
    }
  });

  // === 5. SCROLL ANIMATIONS (IntersectionObserver) ===
  if ('IntersectionObserver' in window) {
    var animObserver = new IntersectionObserver(function(entries) {
      entries.forEach(function(entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('visible');
          animObserver.unobserve(entry.target);
        }
      });
    }, { threshold: 0.1, rootMargin: '0px 0px -50px 0px' });

    document.querySelectorAll('.animate-on-scroll').forEach(function(el) {
      animObserver.observe(el);
    });
  } else {
    // Fallback for older browsers
    document.querySelectorAll('.animate-on-scroll').forEach(function(el) {
      el.classList.add('visible');
    });
  }

  // === 6. CONTACT FORM AJAX SUBMIT ===
  var form = document.getElementById('contactForm');
  if (form) {
    var toastEl = document.getElementById('formToast');

    function showToast(message, type) {
      if (toastEl) {
        toastEl.textContent = message;
        toastEl.style.display = 'block';
        toastEl.style.background = type === 'success' ? '#d1fae5' : '#fee2e2';
        toastEl.style.color = type === 'success' ? '#065f46' : '#991b1b';
        toastEl.style.border = '1px solid ' + (type === 'success' ? '#a7f3d0' : '#fecaca');
        setTimeout(function() {
          toastEl.style.display = 'none';
        }, 5000);
      }
    }

    form.addEventListener('submit', function(e) {
      e.preventDefault();

      // Validate
      var name = document.getElementById('name').value.trim();
      var email = document.getElementById('email').value.trim();
      var subject = document.getElementById('subject').value;
      var message = document.getElementById('message').value.trim();

      if (!name || !email || !subject || !message) {
        showToast('Please fill in all required fields.', 'error');
        return;
      }

      var btn = form.querySelector('button[type="submit"]');
      var btnText = btn.querySelector('.btn-text');
      var btnLoading = btn.querySelector('.btn-loading');
      var originalHTML = btn.innerHTML;

      // Show loading state
      btnText.style.display = 'none';
      btnLoading.style.display = 'inline-flex';
      btn.disabled = true;

      var xhr = new XMLHttpRequest();
      xhr.open('POST', form.action, true);
      xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

      xhr.onload = function() {
        btnText.style.display = 'inline-flex';
        btnLoading.style.display = 'none';
        btn.disabled = false;

        try {
          var resp = JSON.parse(xhr.responseText);
          if (resp.success) {
            showToast(resp.message || 'Thank you! Your message has been sent successfully.', 'success');
            form.reset();
          } else {
            showToast(resp.message || 'Something went wrong. Please try again.', 'error');
          }
        } catch(e) {
          showToast('Server error. Please try again later.', 'error');
        }
      };

      xhr.onerror = function() {
        btnText.style.display = 'inline-flex';
        btnLoading.style.display = 'none';
        btn.disabled = false;
        showToast('Network error. Please check your connection.', 'error');
      };

      xhr.send(new FormData(form));
    });
  }

  // === 7. BACK-TO-TOP BUTTON ===
  var backToTop = document.createElement('button');
  backToTop.className = 'back-to-top';
  backToTop.innerHTML = '<i class="fas fa-arrow-up"></i>';
  backToTop.setAttribute('aria-label', 'Scroll to top');
  document.body.appendChild(backToTop);

  window.addEventListener('scroll', function() {
    if (window.scrollY > 300) {
      backToTop.classList.add('visible');
    } else {
      backToTop.classList.remove('visible');
    }
  }, { passive: true });

  backToTop.addEventListener('click', function() {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  });

  // === 8. YEAR AUTO-UPDATE IN FOOTER ===
  var yearSpan = document.getElementById('year');
  if (yearSpan) {
    yearSpan.textContent = new Date().getFullYear();
  }

  // === 9. GLOBAL TOAST SYSTEM ===
  window.showToast = function(message, type) {
    var toast = document.createElement('div');
    toast.className = 'toast toast-' + (type || 'success');
    var icon = type === 'success' ? 'fa-check-circle' : 'fa-exclamation-circle';
    toast.innerHTML = '<i class="fas ' + icon + '"></i>' + message;
    document.body.appendChild(toast);

    // Trigger animation
    requestAnimationFrame(function() {
      toast.classList.add('show');
    });

    // Auto-remove
    setTimeout(function() {
      toast.classList.remove('show');
      setTimeout(function() {
        toast.remove();
      }, 400);
    }, 4000);
  };
});
