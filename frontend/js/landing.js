/* ============================================================
   GREEN TIME MARINE TIME — Landing Page Scripts
   Vanilla JS • No libraries
   ============================================================ */

(function () {
  'use strict';

  /* ---------- PRELOADER ---------- */
  window.addEventListener('load', function () {
    var preloader = document.getElementById('preloader');
    if (preloader) {
      setTimeout(function () {
        preloader.classList.add('loaded');
      }, 600);
    }
  });

  /* ---------- SCROLL PROGRESS BAR ---------- */
  var scrollProgressBar = document.getElementById('scrollProgress');

  function updateScrollProgress() {
    var scrollTop = window.pageYOffset || document.documentElement.scrollTop;
    var docHeight = document.documentElement.scrollHeight - window.innerHeight;
    var scrollPercent = (scrollTop / docHeight) * 100;
    if (scrollProgressBar) {
      scrollProgressBar.style.width = scrollPercent + '%';
    }
  }

  /* ---------- HEADER SCROLL STATE ---------- */
  var header = document.getElementById('siteHeader');

  function updateHeader() {
    if (!header) return;
    if (window.pageYOffset > 60) {
      header.classList.add('scrolled');
    } else {
      header.classList.remove('scrolled');
    }
  }

  /* ---------- BACK TO TOP BUTTON ---------- */
  var backToTop = document.getElementById('backToTop');

  function updateBackToTop() {
    if (!backToTop) return;
    if (window.pageYOffset > 600) {
      backToTop.classList.add('visible');
    } else {
      backToTop.classList.remove('visible');
    }
  }

  if (backToTop) {
    backToTop.addEventListener('click', function () {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
  }

  /* ---------- COMBINED SCROLL HANDLER ---------- */
  var ticking = false;

  window.addEventListener('scroll', function () {
    if (!ticking) {
      requestAnimationFrame(function () {
        updateScrollProgress();
        updateHeader();
        updateBackToTop();
        ticking = false;
      });
      ticking = true;
    }
  });

  // Initial calls
  updateHeader();
  updateScrollProgress();

  /* ---------- MOBILE NAVIGATION ---------- */
  var hamburger = document.getElementById('hamburger');
  var mobileMenu = document.getElementById('mobileMenu');
  var mobileLinks = document.querySelectorAll('.mobile-link');

  function toggleMenu() {
    if (!hamburger || !mobileMenu) return;
    hamburger.classList.toggle('active');
    mobileMenu.classList.toggle('open');
    document.body.style.overflow = mobileMenu.classList.contains('open') ? 'hidden' : '';
  }

  if (hamburger) {
    hamburger.addEventListener('click', toggleMenu);
  }

  mobileLinks.forEach(function (link) {
    link.addEventListener('click', function () {
      if (hamburger) hamburger.classList.remove('active');
      if (mobileMenu) mobileMenu.classList.remove('open');
      document.body.style.overflow = '';
    });
  });

  /* ---------- ACTIVE NAV LINK ON SCROLL ---------- */
  var sections = document.querySelectorAll('section[id]');
  var navLinks = document.querySelectorAll('.nav-link');

  function updateActiveLink() {
    var scrollPos = window.pageYOffset + 120;

    sections.forEach(function (section) {
      var top = section.offsetTop;
      var height = section.offsetHeight;
      var id = section.getAttribute('id');

      if (scrollPos >= top && scrollPos < top + height) {
        navLinks.forEach(function (link) {
          link.classList.remove('active');
          if (link.getAttribute('href') === '#' + id) {
            link.classList.add('active');
          }
        });
      }
    });
  }

  window.addEventListener('scroll', updateActiveLink);

  /* ---------- SMOOTH SCROLL FOR ANCHOR LINKS ---------- */
  document.querySelectorAll('a[href^="#"]').forEach(function (anchor) {
    anchor.addEventListener('click', function (e) {
      var targetId = this.getAttribute('href');
      if (targetId === '#') return;

      var target = document.querySelector(targetId);
      if (target) {
        e.preventDefault();
        var offsetTop = target.offsetTop - 80;
        window.scrollTo({ top: offsetTop, behavior: 'smooth' });
      }
    });
  });

  /* ---------- SCROLL REVEAL ANIMATIONS ---------- */
  function revealElements() {
    var reveals = document.querySelectorAll('[data-reveal]:not(.revealed)');

    reveals.forEach(function (el) {
      var rect = el.getBoundingClientRect();
      var windowHeight = window.innerHeight;

      if (rect.top < windowHeight - 80) {
        el.classList.add('revealed');
      }
    });
  }

  window.addEventListener('scroll', revealElements);
  window.addEventListener('load', function () {
    setTimeout(revealElements, 100);
  });

  /* ---------- COUNTER ANIMATION ---------- */
  var countersAnimated = false;

  function animateCounters() {
    if (countersAnimated) return;

    var counters = document.querySelectorAll('[data-count]');
    if (counters.length === 0) return;

    var firstCounter = counters[0];
    var rect = firstCounter.getBoundingClientRect();

    if (rect.top < window.innerHeight - 50) {
      countersAnimated = true;

      counters.forEach(function (counter) {
        var target = parseInt(counter.getAttribute('data-count'), 10);
        var duration = 2000;
        var startTime = null;

        function easeOut(t) {
          return 1 - Math.pow(1 - t, 3);
        }

        function step(timestamp) {
          if (!startTime) startTime = timestamp;
          var progress = Math.min((timestamp - startTime) / duration, 1);
          var easedProgress = easeOut(progress);
          var current = Math.floor(easedProgress * target);

          counter.textContent = current.toLocaleString();

          if (progress < 1) {
            requestAnimationFrame(step);
          } else {
            counter.textContent = target.toLocaleString();
          }
        }

        requestAnimationFrame(step);
      });
    }
  }

  window.addEventListener('scroll', animateCounters);

  /* ---------- PARALLAX EFFECT ON QUOTE SECTION ---------- */
  var parallaxBg = document.querySelector('.parallax-bg');

  function updateParallax() {
    if (!parallaxBg) return;
    var section = parallaxBg.closest('.parallax-quote');
    if (!section) return;

    var rect = section.getBoundingClientRect();
    var windowHeight = window.innerHeight;

    if (rect.bottom > 0 && rect.top < windowHeight) {
      var scrolled = (windowHeight - rect.top) / (windowHeight + rect.height);
      var offset = (scrolled - 0.5) * 60;
      parallaxBg.style.transform = 'translateY(' + offset + 'px)';
    }
  }

  window.addEventListener('scroll', function () {
    requestAnimationFrame(updateParallax);
  });

  /* ---------- CONTACT FORM HANDLING ---------- */
  var contactForm = document.getElementById('contactForm');

  if (contactForm) {
    contactForm.addEventListener('submit', function (e) {
      e.preventDefault();

      var btn = contactForm.querySelector('button[type="submit"]');
      var originalText = btn.innerHTML;

      btn.innerHTML = '<span style="display:inline-flex;align-items:center;gap:8px;">Sending... <span class="preloader-ring" style="width:18px;height:18px;border-width:2px;"></span></span>';
      btn.disabled = true;

      // Simulate send (can be replaced with actual API)
      setTimeout(function () {
        btn.innerHTML = '<span style="display:inline-flex;align-items:center;gap:8px;">Request Sent &#10003;</span>';
        btn.style.background = '#14553F';

        setTimeout(function () {
          btn.innerHTML = originalText;
          btn.disabled = false;
          btn.style.background = '';
          contactForm.reset();
        }, 2500);
      }, 1500);
    });
  }

  /* ---------- FLOATING LABEL FIX FOR SELECT ---------- */
  var selects = document.querySelectorAll('.form-group select');
  selects.forEach(function (select) {
    select.addEventListener('change', function () {
      if (this.value) {
        this.classList.add('has-value');
      } else {
        this.classList.remove('has-value');
      }
    });
  });

  /* ---------- KEYBOARD ACCESSIBILITY ---------- */
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && mobileMenu && mobileMenu.classList.contains('open')) {
      toggleMenu();
    }
  });

})();
