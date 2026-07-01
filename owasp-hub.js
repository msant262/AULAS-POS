  var OWASP_ORDER = ['A01', 'A02', 'A03', 'A04', 'A05', 'A06', 'A07', 'A08', 'A09', 'A10'];
  var owaspModalEl = document.getElementById('owasp-modal');
  var owaspModalTitle = document.getElementById('owasp-modal-title');
  var owaspCurrent = null;
  var owaspModalOpen = false;
  function owaspPanel(oid) {
    return document.getElementById('owasp-panel-' + oid);
  }

  function resetOwaspPanelTabs(panel) {
    if (!panel) return;
    panel.querySelectorAll('.ok-tab').forEach(function (t, i) {
      t.classList.toggle('active', i === 0);
    });
    panel.querySelectorAll('.tab-panel').forEach(function (p, i) {
      p.classList.toggle('active', i === 0);
    });
    if (window.resetModalTabScroll) window.resetModalTabScroll(panel);
  }

  function openOwaspModal(oid, tab) {
    if (!owaspModalEl || OWASP_ORDER.indexOf(oid) === -1) return;
    var panel = owaspPanel(oid);
    if (!panel) return;

    applyFilter(oid, null, { hubOnly: true });

    OWASP_ORDER.forEach(function (id) {
      var p = owaspPanel(id);
      if (p) p.hidden = id !== oid;
    });

    var card = document.querySelector('.owasp-card[data-owasp="' + oid + '"]');
    var title = card ? card.querySelector('.owasp-card-title') : null;
    if (owaspModalTitle) {
      owaspModalTitle.textContent = oid + ' — ' + (title ? title.textContent : 'OWASP Top 10');
    }

    owaspCurrent = oid;
    owaspModalEl.classList.add('open');
    owaspModalEl.setAttribute('aria-hidden', 'false');
    document.documentElement.classList.add('owasp-modal-open');
    document.body.classList.add('owasp-modal-open');

    if (tab) {
      var tabBtn = panel.querySelector('.ok-tab[data-tab="' + tab + '"]');
      if (tabBtn) tabBtn.click();
    } else {
      resetOwaspPanelTabs(panel);
    }

    owaspModalOpen = true;
    if (history.replaceState) {
      history.replaceState(null, '', '#owasp-' + oid);
    }
  }

  function closeOwaspModal() {
    if (!owaspModalEl) return;
    owaspModalEl.classList.remove('open');
    owaspModalEl.setAttribute('aria-hidden', 'true');
    document.documentElement.classList.remove('owasp-modal-open');
    document.body.classList.remove('owasp-modal-open');
    owaspCurrent = null;
    owaspModalOpen = false;
    if (history.replaceState && location.hash.match(/^#owasp-A\d{2}$/)) {
      history.replaceState(null, '', location.pathname + location.search);
    }
    requestAnimationFrame(function () {
      applyFilter(null, null, { hubOnly: true });
    });
  }

  function stepOwaspModal(delta) {
    if (!owaspCurrent) return;
    var idx = OWASP_ORDER.indexOf(owaspCurrent);
    var next = OWASP_ORDER[(idx + delta + OWASP_ORDER.length) % OWASP_ORDER.length];
    openOwaspModal(next);
  }

  function scrollOwaspSim(boxId) {
    scrollToId('simuladores');
    setTimeout(function () {
      var box = document.getElementById(boxId);
      if (box) {
        box.scrollIntoView({ behavior: 'smooth', block: 'center' });
        box.classList.add('sim-flash');
      }
    }, 320);
  }

  window.openOwaspModal = openOwaspModal;
  window.closeOwaspModal = closeOwaspModal;

  document.addEventListener('click', function (e) {
    var infoBtn = e.target.closest('[data-owasp-info]');
    if (infoBtn) {
      e.preventDefault();
      openOwaspModal(infoBtn.getAttribute('data-owasp-info'), 'guia');
      return;
    }

    var simCardBtn = e.target.closest('[data-owasp-sim]');
    if (simCardBtn) {
      e.preventDefault();
      e.stopPropagation();
      scrollOwaspSim(simCardBtn.getAttribute('data-sim-box'));
      return;
    }

    if (e.target.closest('[data-owasp-close]')) {
      e.preventDefault();
      closeOwaspModal();
      return;
    }

    var prev = e.target.closest('.owasp-modal-prev');
    if (prev) {
      e.preventDefault();
      stepOwaspModal(-1);
      return;
    }

    var next = e.target.closest('.owasp-modal-next');
    if (next) {
      e.preventDefault();
      stepOwaspModal(1);
      return;
    }

    var simBtn = e.target.closest('.owasp-open-sim');
    if (simBtn) {
      e.preventDefault();
      var boxId = simBtn.getAttribute('data-sim-box');
      closeOwaspModal();
      scrollOwaspSim(boxId);
      return;
    }

    var corrBtn = e.target.closest('.owasp-open-corr');
    if (corrBtn) {
      e.preventDefault();
      var oid = corrBtn.getAttribute('data-owasp-corr');
      closeOwaspModal();
      scrollToId('correlacao');
      if (oid && typeof applyFilter === 'function') {
        setTimeout(function () { applyFilter(oid, null); }, 200);
      }
    }
  });

  document.addEventListener('keydown', function (e) {
    if (!owaspModalOpen) return;
    if (e.key === 'Escape') {
      e.preventDefault();
      closeOwaspModal();
    }
    if (e.key === 'ArrowLeft') {
      e.preventDefault();
      stepOwaspModal(-1);
    }
    if (e.key === 'ArrowRight') {
      e.preventDefault();
      stepOwaspModal(1);
    }
  });

  function handleOwaspHash() {
    var m = (location.hash || '').match(/^#owasp-(A\d{2})$/);
    if (m) {
      scrollToSectionIfNeeded(document.getElementById('owasp-hub'));
      openOwaspModal(m[1], 'guia');
    }
  }

  window.addEventListener('hashchange', handleOwaspHash);
  if (location.hash.match(/^#owasp-A\d{2}$/)) {
    setTimeout(handleOwaspHash, 80);
  }