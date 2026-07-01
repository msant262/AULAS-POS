  var cweModalEl = document.getElementById('cwe-modal');
  var cweModalTitle = document.getElementById('cwe-modal-title');
  var cweCurrent = null;
  var cweModalOpen = false;
  var CWE_ORDER = Array.from(document.querySelectorAll('.cwe-card[data-cwe]')).map(function (c) {
    return c.getAttribute('data-cwe');
  });

  function cwePanel(cid) {
    return document.getElementById('cwe-panel-' + cid);
  }

  function resetCwePanelTabs(panel) {
    if (!panel) return;
    panel.querySelectorAll('.ok-tab').forEach(function (t, i) {
      t.classList.toggle('active', i === 0);
    });
    panel.querySelectorAll('.tab-panel').forEach(function (p, i) {
      p.classList.toggle('active', i === 0);
    });
    if (window.resetModalTabScroll) window.resetModalTabScroll(panel);
  }

  function openCweModal(cid, tab) {
    if (!cweModalEl || CWE_ORDER.indexOf(cid) === -1) return;
    var panel = cwePanel(cid);
    if (!panel) return;

    applyFilter(null, cid, { hubOnly: true });

    CWE_ORDER.forEach(function (id) {
      var p = cwePanel(id);
      if (p) p.hidden = id !== cid;
    });

    var card = document.querySelector('.cwe-card[data-cwe="' + cid + '"]');
    var title = card ? card.querySelector('.cwe-card-title') : null;
    if (cweModalTitle) {
      cweModalTitle.textContent = cid + ' — ' + (title ? title.textContent : 'CWE TOP 25');
    }

    cweCurrent = cid;
    cweModalEl.classList.add('open');
    cweModalEl.setAttribute('aria-hidden', 'false');
    document.documentElement.classList.add('cwe-modal-open');
    document.body.classList.add('cwe-modal-open');

    if (tab) {
      var tabBtn = panel.querySelector('.ok-tab[data-tab="' + tab + '"]');
      if (tabBtn) tabBtn.click();
    } else {
      resetCwePanelTabs(panel);
    }

    cweModalOpen = true;
    if (history.replaceState) {
      history.replaceState(null, '', '#cwe-' + cid.replace('CWE-', ''));
    }
  }

  function closeCweModal() {
    if (!cweModalEl) return;
    cweModalEl.classList.remove('open');
    cweModalEl.setAttribute('aria-hidden', 'true');
    document.documentElement.classList.remove('cwe-modal-open');
    document.body.classList.remove('cwe-modal-open');
    cweCurrent = null;
    cweModalOpen = false;
    if (history.replaceState && location.hash.match(/^#cwe-\d+$/)) {
      history.replaceState(null, '', location.pathname + location.search);
    }
    requestAnimationFrame(function () {
      applyFilter(null, null, { hubOnly: true });
    });
  }

  function stepCweModal(delta) {
    if (!cweCurrent) return;
    var idx = CWE_ORDER.indexOf(cweCurrent);
    var next = CWE_ORDER[(idx + delta + CWE_ORDER.length) % CWE_ORDER.length];
    openCweModal(next);
  }

  function scrollCweSim(boxId) {
    scrollToId('simuladores-cwe');
    setTimeout(function () {
      var box = document.getElementById(boxId);
      if (box) {
        box.scrollIntoView({ behavior: 'smooth', block: 'center' });
        box.classList.add('sim-flash');
      }
    }, 320);
  }

  window.openCweModal = openCweModal;
  window.closeCweModal = closeCweModal;

  document.addEventListener('click', function (e) {
    var infoBtn = e.target.closest('[data-cwe-info]');
    if (infoBtn) {
      e.preventDefault();
      openCweModal(infoBtn.getAttribute('data-cwe-info'), 'guia');
      return;
    }

    var simCardBtn = e.target.closest('[data-cwe-sim]');
    if (simCardBtn) {
      e.preventDefault();
      e.stopPropagation();
      scrollCweSim(simCardBtn.getAttribute('data-sim-box'));
      return;
    }

    if (e.target.closest('[data-cwe-close]')) {
      e.preventDefault();
      closeCweModal();
      return;
    }

    var prev = e.target.closest('.cwe-modal-prev');
    if (prev) {
      e.preventDefault();
      stepCweModal(-1);
      return;
    }

    var next = e.target.closest('.cwe-modal-next');
    if (next) {
      e.preventDefault();
      stepCweModal(1);
      return;
    }

    var simBtn = e.target.closest('.cwe-open-sim');
    if (simBtn) {
      e.preventDefault();
      var boxId = simBtn.getAttribute('data-sim-box');
      closeCweModal();
      scrollCweSim(boxId);
      return;
    }

    var owaspBtn = e.target.closest('.cwe-open-owasp');
    if (owaspBtn) {
      e.preventDefault();
      var oid = owaspBtn.getAttribute('data-owasp-jump');
      closeCweModal();
      if (oid && window.openOwaspModal) {
        setTimeout(function () { openOwaspModal(oid, 'guia'); }, 120);
      }
      return;
    }

    var corrBtn = e.target.closest('.cwe-open-corr');
    if (corrBtn) {
      e.preventDefault();
      var cid = corrBtn.getAttribute('data-cwe-corr');
      closeCweModal();
      scrollToId('correlacao');
      if (cid && typeof applyFilter === 'function') {
        setTimeout(function () { applyFilter(null, cid); }, 200);
      }
    }
  });

  document.addEventListener('keydown', function (e) {
    if (!cweModalOpen) return;
    if (e.key === 'Escape') {
      e.preventDefault();
      closeCweModal();
    }
    if (e.key === 'ArrowLeft') {
      e.preventDefault();
      stepCweModal(-1);
    }
    if (e.key === 'ArrowRight') {
      e.preventDefault();
      stepCweModal(1);
    }
  });

  function handleCweHash() {
    var m = (location.hash || '').match(/^#cwe-(\d+)$/);
    if (m) {
      scrollToSectionIfNeeded(document.getElementById('cwe-hub'));
      openCweModal('CWE-' + m[1], 'guia');
    }
  }

  window.addEventListener('hashchange', function () {
    if (location.hash.match(/^#cwe-\d+$/)) handleCweHash();
  });
  if (location.hash.match(/^#cwe-\d+$/)) {
    setTimeout(handleCweHash, 80);
  }