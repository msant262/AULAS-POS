(function () {
  'use strict';

  if ('scrollRestoration' in history) {
    history.scrollRestoration = 'manual';
  }

  var pageBootActive = true;

  function releasePageBoot() {
    pageBootActive = false;
  }

  function $(s, ctx) { return (ctx || document).querySelector(s); }
  function $$(s, ctx) { return [...(ctx || document).querySelectorAll(s)]; }

  function parseJSON(id, fallback) {
    var el = document.getElementById(id);
    if (!el) return fallback;
    try { return JSON.parse(el.textContent); } catch (e) { console.error(id, e); return fallback; }
  }

  var QUIZ = parseJSON('data-quiz', []);
  var CORR = parseJSON('data-corr', []);
  var CWE_CHART = parseJSON('data-cwe-chart', []);
  var OWASP_CHART = parseJSON('data-owasp-chart', []);
  var KEV_CHART = parseJSON('data-kev-chart', []);
  var PREV_CHART = parseJSON('data-prev-chart', []);
  var BREACH_CHART = parseJSON('data-breach-chart', []);
  var DELTA_CHART = parseJSON('data-delta-chart', []);
  var TERMINALS = parseJSON('data-terminals', {});

  // Seções de navegação — nunca esconder/dim (senão a matriz fica inacessível)
  var FILTER_EXEMPT = {
    intro: 1, mercado: 1, pesquisa: 1, noticias: 1, correlacao: 1,
    'terminal-lab': 1, 'code-vault': 1, simuladores: 1, 'simuladores-cwe': 1, 'owasp-hub': 1, 'ponte-owasp-cwe': 1, 'cwe-hub': 1, 'juice-setup': 1, 'juice-ide': 1, quiz: 1
  };

  var sections = $$('.lesson-sec');
  var hero = $('.hero');
  var hmCells = $$('.hm-cell');
  var hmOwasp = $$('.hm-owasp');
  var hmCwe = $$('.hm-cwe');
  var filterOwasp = null;
  var filterCwe = null;

  function getScrollOffset() {
    var toolbar = document.querySelector('.toolbar');
    return (toolbar ? toolbar.offsetHeight : 56) + 12;
  }

  function resolveScrollTarget(id) {
    if (!id) return null;
    if (/^owasp-A\d{2}$/.test(id)) return document.getElementById('owasp-hub');
    if (/^cwe-\d+$/.test(id)) return document.getElementById('cwe-hub');
    var el = document.getElementById(id);
    if (!el) return null;
    if (el.classList.contains('lesson-sec')) return el;
    var sec = el.closest('.lesson-sec');
    return sec || el;
  }

  function preserveSidebarScroll() {
    var sidebar = document.querySelector('.sidebar');
    if (!sidebar) return function () {};
    var top = sidebar.scrollTop;
    return function () {
      requestAnimationFrame(function () {
        sidebar.scrollTop = top;
        requestAnimationFrame(function () { sidebar.scrollTop = top; });
      });
    };
  }

  function scrollToSection(el, opts) {
    opts = opts || {};
    if (!el) return;
    var offset = getScrollOffset();
    var targetTop = el.getBoundingClientRect().top + window.pageYOffset - offset;
    targetTop = Math.max(0, Math.round(targetTop));
    if (!opts.force && Math.abs(targetTop - window.pageYOffset) < 10) return;
    window.scrollTo({ top: targetTop, behavior: opts.behavior || 'smooth' });
  }

  function scrollToSectionIfNeeded(el) {
    scrollToSection(el, { force: true });
  }

  function setHashQuiet(hash) {
    var next = hash ? hash : (location.pathname + location.search);
    if (history.replaceState) history.replaceState(null, '', next);
    else if (hash) location.hash = hash;
  }

  function scrollToId(id, opts) {
    if (!id) return;
    opts = opts || {};
    releasePageBoot();
    var restoreSidebar = preserveSidebarScroll();

    if (/^owasp-A\d{2}$/.test(id) && window.openOwaspModal) {
      scrollToSection(document.getElementById('owasp-hub'), { force: true });
      window.openOwaspModal(id.replace('owasp-', ''));
      restoreSidebar();
      updateNavActive();
      return;
    }
    if (/^cwe-\d+$/.test(id) && window.openCweModal) {
      scrollToSection(document.getElementById('cwe-hub'), { force: true });
      window.openCweModal('CWE-' + id.replace('cwe-', ''));
      restoreSidebar();
      updateNavActive();
      return;
    }
    var el = resolveScrollTarget(id);
    if (opts.updateHash !== false) setHashQuiet('#' + id);
    scrollToSection(el, { force: opts.force !== false });
    restoreSidebar();
    updateNavActive();
  }

  // Links internos: scroll sem navegar (evita erro file:// em iframe/preview)
  document.addEventListener('click', function (e) {
    var a = e.target.closest('a[href^="#"]');
    if (!a) return;
    var hash = a.getAttribute('href');
    if (!hash || hash.length < 2) return;
    e.preventDefault();
    scrollToId(hash.slice(1), { force: true });
  }, true);

  document.addEventListener('wheel', releasePageBoot, { passive: true });
  document.addEventListener('touchstart', releasePageBoot, { passive: true });

  function resetTabScroll(sec) {
    if (!sec) return;
    var scrollEl = sec.querySelector('.owasp-modal-scroll, .cwe-modal-scroll');
    if (scrollEl) scrollEl.scrollTop = 0;
  }
  window.resetModalTabScroll = resetTabScroll;

  // ── Tabs ──
  document.addEventListener('click', function (e) {
    var tab = e.target.closest('.ok-tab[data-tab]');
    if (!tab) return;
    var tabs = tab.closest('.section-tabs');
    var sec = tabs && (tabs.closest('.lesson-sec') || tabs.closest('.owasp-modal-panel') || tabs.closest('.cwe-modal-panel'));
    if (!sec) return;
    e.preventDefault();
    tabs.querySelectorAll('.ok-tab').forEach(function (t) { t.classList.remove('active'); });
    tab.classList.add('active');
    sec.querySelectorAll('.tab-panel').forEach(function (p) { p.classList.remove('active'); });
    var panel = sec.querySelector('[data-panel="' + tab.dataset.tab + '"]');
    if (panel) panel.classList.add('active');
    resetTabScroll(sec);
  });

  // ── Código vulnerável ↔ correção ──
  document.addEventListener('click', function (e) {
    var btn = e.target.closest('.code-toggle');
    if (!btn) return;
    var wrap = btn.closest('.code-wrap');
    if (!wrap) return;
    var show = btn.dataset.show;
    wrap.querySelectorAll('.code-toggle').forEach(function (b) {
      b.classList.toggle('solid', b === btn);
      b.classList.toggle('ghost', b !== btn);
      b.classList.toggle('cyan', b === btn && show === 'fix');
    });
    var vuln = wrap.querySelector('.code-panel.vuln');
    var fix = wrap.querySelector('.code-panel.fix');
    if (vuln) vuln.classList.toggle('active', show === 'vuln');
    if (fix) fix.classList.toggle('active', show === 'fix');
    var slider = wrap.querySelector('.diff-slider');
    if (slider) slider.value = show === 'fix' ? 100 : 0;
    updateDiffSlider(wrap);
  });

  function updateDiffSlider(wrap) {
    var slider = wrap.querySelector('.diff-slider');
    var vuln = wrap.querySelector('.code-panel.vuln');
    var fix = wrap.querySelector('.code-panel.fix');
    if (!slider || !vuln || !fix) return;
    var pct = parseInt(slider.value, 10);
    vuln.style.clipPath = 'inset(0 ' + (100 - pct) + '% 0 0)';
    fix.style.clipPath = 'inset(0 0 0 ' + pct + '%)';
    var lbl = wrap.querySelector('.diff-label');
    if (lbl) lbl.textContent = pct < 50 ? 'Vulnerável' : pct > 50 ? 'Corrigido' : 'Comparar';
  }

  document.addEventListener('input', function (e) {
    if (!e.target.classList.contains('diff-slider')) return;
    updateDiffSlider(e.target.closest('.code-wrap'));
  });

  // ── Correlação OWASP ↔ CWE ──
  var corrDetail = $('#corr-detail');
  var filterLabel = $('#filter-label');

  function scrollCorrListToItem(item) {
    var list = $('#corr-list');
    if (!list || !item) return;
    var listRect = list.getBoundingClientRect();
    if (listRect.bottom < 0 || listRect.top > window.innerHeight) return;
    var target = item.offsetTop - list.clientHeight / 2 + item.offsetHeight / 2;
    list.scrollTo({ top: Math.max(0, target), behavior: 'smooth' });
  }

  function applyFilter(o, c, opts) {
    opts = opts || {};
    var hubOnly = !!opts.hubOnly;
    filterOwasp = o || null;
    filterCwe = c || null;
    var active = !!(o || c);
    document.body.classList.toggle('corr-filtering', active && !hubOnly);

    sections.forEach(function (s) {
      s.classList.remove('highlight', 'dimmed', 'filter-match');
      if (hubOnly || FILTER_EXEMPT[s.id]) return;
      if (!active) return;
      var match = (o && s.dataset.owasp === o) || (c && s.dataset.cwe === c);
      if (match) s.classList.add('filter-match');
    });
    $$('.owasp-card').forEach(function (card) {
      card.classList.remove('filter-match', 'dimmed');
      if (!active) return;
      var cardMatch = o && card.dataset.owasp === o;
      card.classList.toggle('filter-match', cardMatch);
      card.classList.toggle('dimmed', !cardMatch);
    });
    $$('.cwe-card').forEach(function (card) {
      card.classList.remove('filter-match', 'dimmed');
      if (!active) return;
      var cweMatch = c && card.dataset.cwe === c;
      card.classList.toggle('filter-match', cweMatch);
      card.classList.toggle('dimmed', !cweMatch);
    });

    hmCells.forEach(function (cell) {
      var empty = cell.classList.contains('empty');
      var match = false;
      if (o && c) match = cell.dataset.owasp === o && cell.dataset.cwe === c;
      else if (o) match = cell.dataset.owasp === o && !empty;
      else if (c) match = cell.dataset.cwe === c && !empty;
      cell.classList.toggle('sel', !!(o && c) && match);
      cell.classList.toggle('hl', active && match);
      cell.classList.toggle('dim', active && !match && !empty);
    });
    hmOwasp.forEach(function (th) {
      th.classList.toggle('sel', !!o && th.dataset.owasp === o);
    });
    hmCwe.forEach(function (th) {
      th.classList.toggle('sel', !!c && th.dataset.cwe === c);
    });
    var listCount = $('#corr-list-count');
    var visible = 0;
    $$('.corr-item').forEach(function (el) {
      el.style.display = '';
      var exact = !!(o && c && el.dataset.owasp === o && el.dataset.cwe === c);
      var row = !!(o && el.dataset.owasp === o);
      var col = !!(c && el.dataset.cwe === c);
      var relevant = !active || exact || (o && !c && row) || (c && !o && col) || (o && c && (row || col));
      if (relevant) visible++;
      el.classList.toggle('sel', exact);
      el.classList.toggle('hl', active && relevant && !exact);
      el.classList.toggle('dim', active && !relevant);
    });
    if (listCount) {
      listCount.textContent = active ? visible + ' em destaque · lista completa mantida' : 'todas visíveis';
    }

    if (filterLabel && !hubOnly) {
      filterLabel.textContent = active
        ? (o || '—') + (o && c ? ' ↔ ' : (o && !c ? ' (linha)' : c ? ' (coluna)' : '')) + (c || '')
        : 'nenhum';
    }

    if (!hubOnly) {
      var scrollTarget = $('.corr-item.sel') || $('.corr-item.hl');
      if (scrollTarget) scrollCorrListToItem(scrollTarget);
    }
  }

  function renderCorrDetail(o, c) {
    if (!corrDetail) return;
    if (o && c) {
      var item = CORR.find(function (x) { return x.o === o && x.c === c; });
      if (item) {
        corrDetail.innerHTML =
          '<span class="ok-badge accent">' + item.o + '</span> ↔ <span class="ok-badge cyan">' + item.c + '</span>' +
          '<p>' + item.n + '</p><p>Força ' + item.s + '/3</p>' +
          '<button type="button" class="ok-btn sm scroll-to" data-target="owasp-' + item.o + '">Ver ' + item.o + '</button> ' +
          '<button type="button" class="ok-btn sm cyan scroll-to" data-target="cwe-' + item.c.split('-')[1] + '">Ver ' + item.c + '</button>';
        return;
      }
    }
    var matches = CORR.filter(function (x) {
      if (o && c) return x.o === o && x.c === c;
      if (o) return x.o === o;
      if (c) return x.c === c;
      return false;
    });
    if (!matches.length) {
      corrDetail.textContent = 'Nenhuma correlação mapeada para este filtro.';
      return;
    }
    corrDetail.innerHTML = '<p><strong>' + matches.length + '</strong> correlação(ões) — clique para detalhar:</p>' +
      matches.map(function (m) {
        return '<button type="button" class="corr-mini" data-owasp="' + m.o + '" data-cwe="' + m.c + '">' +
          m.o + ' ↔ ' + m.c + ' · ' + m.n + ' (força ' + m.s + '/3)</button>';
      }).join('');
  }

  function showCorr(o, c) {
    applyFilter(o, c);
    renderCorrDetail(o, c);
  }

  function showResearch(id) {
    $$('.research-nav-item').forEach(function (btn) {
      btn.classList.toggle('active', btn.dataset.research === id);
    });
    $$('.research-panel').forEach(function (panel) {
      panel.classList.toggle('active', panel.dataset.researchPanel === id);
    });
  }

  function showBreach(node, withFilter) {
    if (!node) return;
    $$('.timeline-node').forEach(function (n) { n.classList.remove('sel'); });
    node.classList.add('sel');
    var detail = $('#breach-detail');
    if (!detail) return;
    detail.innerHTML =
      '<span class="section-label">' + node.dataset.year + ' · ' + node.dataset.cat + '</span>' +
      '<h4>' + node.dataset.name + '</h4>' +
      '<p>' + node.dataset.desc + '</p>' +
      '<div class="breach-meta">' +
      '<span class="ok-badge accent">' + node.dataset.owasp + '</span>' +
      '<span class="ok-badge cyan">' + node.dataset.cwe + '</span>' +
      '<span class="ok-badge pill">Impacto: ' + node.dataset.impact + '</span>' +
      '<span class="ok-badge pill">' + node.dataset.ref + '</span></div>' +
      '<button type="button" class="ok-btn sm scroll-to" data-target="owasp-' + node.dataset.owasp + '">Ver ' + node.dataset.owasp + '</button> ' +
      '<button type="button" class="ok-btn sm cyan scroll-to" data-target="cwe-' + node.dataset.cwe.split('-')[1] + '">Ver ' + node.dataset.cwe + '</button>' +
      (node.dataset.url ? ' <a class="ok-btn sm ghost" href="' + node.dataset.url + '" target="_blank" rel="noopener">Fonte →</a>' : '');
    if (withFilter !== false) showCorr(node.dataset.owasp, node.dataset.cwe);
  }

  function showPattern(id) {
    $$('.vault-item').forEach(function (btn) {
      btn.classList.toggle('active', btn.dataset.pattern === id);
    });
    $$('.pattern-detail').forEach(function (panel) {
      panel.classList.toggle('active', panel.dataset.patternId === id);
    });
  }

  function filterVault(ow) {
    var items = $$('.vault-item');
    var firstVisible = null;
    items.forEach(function (btn) {
      var match = !ow || btn.dataset.owasp === ow;
      btn.style.display = match ? '' : 'none';
      if (match && !firstVisible) firstVisible = btn;
    });
    $$('.pattern-detail').forEach(function (panel) {
      var item = $('.vault-item[data-pattern="' + panel.dataset.patternId + '"]');
      panel.style.display = item && item.style.display !== 'none' ? '' : 'none';
    });
    if (firstVisible) showPattern(firstVisible.dataset.pattern);
  }

  document.addEventListener('click', function (e) {
    var clearBtn = e.target.closest('#filter-clear');
    if (clearBtn) {
      applyFilter(null, null);
      $$('.corr-item').forEach(function (el) {
        el.style.display = '';
        el.classList.remove('sel', 'hl', 'dim');
      });
      if (corrDetail) {
        corrDetail.textContent = 'Selecione uma correlação na matriz 10×25 para filtrar as seções e ver a explicação.';
      }
      return;
    }

    var scrollBtn = e.target.closest('.scroll-to,[data-scroll]');
    if (scrollBtn) {
      scrollToId(scrollBtn.dataset.target || scrollBtn.dataset.scroll);
      return;
    }

    var corrMini = e.target.closest('.corr-mini');
    if (corrMini) {
      e.preventDefault();
      showCorr(corrMini.dataset.owasp, corrMini.dataset.cwe);
      return;
    }

    var cell = e.target.closest('.hm-cell');
    if (cell && !cell.classList.contains('empty')) {
      e.preventDefault();
      showCorr(cell.dataset.owasp, cell.dataset.cwe);
      return;
    }
    var owaspTh = e.target.closest('.hm-owasp');
    if (owaspTh) {
      e.preventDefault();
      showCorr(owaspTh.dataset.owasp, null);
      return;
    }
    var cweTh = e.target.closest('.hm-cwe');
    if (cweTh) {
      e.preventDefault();
      showCorr(null, cweTh.dataset.cwe);
      return;
    }
    var item = e.target.closest('.corr-item');
    if (item) {
      e.preventDefault();
      showCorr(item.dataset.owasp, item.dataset.cwe);
      return;
    }
    var chip = e.target.closest('.corr-chip');
    if (chip) {
      e.preventDefault();
      showCorr(chip.dataset.owasp, chip.dataset.cwe);
      return;
    }

    var researchBtn = e.target.closest('.research-nav-item');
    if (researchBtn) {
      e.preventDefault();
      showResearch(researchBtn.dataset.research);
      return;
    }

    var timelineNode = e.target.closest('.timeline-node');
    if (timelineNode) {
      e.preventDefault();
      showBreach(timelineNode);
      return;
    }

    var vaultItem = e.target.closest('.vault-item');
    if (vaultItem && vaultItem.style.display !== 'none') {
      e.preventDefault();
      showPattern(vaultItem.dataset.pattern);
      return;
    }

    var vFilter = e.target.closest('.vault-filter');
    if (vFilter) {
      var ow = vFilter.dataset.vault || '';
      $$('.vault-filter').forEach(function (b) {
        b.classList.toggle('solid', b === vFilter);
        b.classList.toggle('ghost', b !== vFilter);
      });
      filterVault(ow);
      return;
    }

    var termTab = e.target.closest('.term-tab');
    if (termTab) {
      var tid = termTab.dataset.termTab;
      $$('.term-tab').forEach(function (t) { t.classList.remove('active'); });
      termTab.classList.add('active');
      $$('.term-panel').forEach(function (p) {
        p.classList.toggle('active', p.dataset.termPanel === tid);
      });
      return;
    }

    var termClear = e.target.closest('.term-clear');
    if (termClear) {
      clearTerminal(termClear.dataset.term);
      return;
    }

    var termCmd = e.target.closest('.term-cmd,.term-embed-cmd');
    if (termCmd) {
      var tid = termCmd.dataset.term;
      var cmd = termCmd.dataset.cmd;
      var embedOut = $('#term-embed-' + tid);
      if (termCmd.classList.contains('term-embed-cmd') && embedOut) {
        runTerminalTo(embedOut, tid, cmd);
      } else {
        runTerminal(tid, cmd);
      }
      return;
    }

    var termDemo = e.target.closest('.term-demo');
    if (termDemo) {
      runTerminalDemo(termDemo.dataset.term);
      return;
    }
  });

  // ── Terminal interativo ──
  function classifyLine(text) {
    if (/^HTTP\/|^\{.*authentication|^\[200\]/.test(text)) return 'http';
    if (/^#|→|BYPASS|OK|SQLite|correção/i.test(text)) return 'ok';
    if (/^!|WARN|vulnerável|bypass|exfiltr/i.test(text)) return 'warn';
    if (/erro|invalid|não reconhecido|403|401/i.test(text)) return 'err';
    if (/^\$/.test(text)) return 'cmd';
    return 'out';
  }

  function termLine(out, text, cls) {
    var line = document.createElement('div');
    line.className = 'line ' + (cls || classifyLine(text));
    line.textContent = text;
    out.appendChild(line);
    out.scrollTop = out.scrollHeight;
  }

  function runTerminalTo(out, tid, cmd) {
    var lab = TERMINALS[tid];
    if (!out || !cmd) return;
    if (!lab || !lab.cmds) {
      termLine(out, '$ ' + cmd, 'cmd');
      termLine(out, 'Lab não carregado — recarregue a página (Cmd+Shift+R).', 'err');
      return;
    }
    termLine(out, '$ ' + cmd, 'cmd');
    var resp = findTermResponse(lab, cmd.trim());
    if (!resp) {
      termLine(out, 'Comando não reconhecido. Digite help ou use os atalhos.', 'warn');
      return;
    }
    resp.split('\n').forEach(function (ln) { termLine(out, ln); });
  }

  function findTermResponse(lab, cmd) {
    if (!lab || !lab.cmds) return null;
    if (lab.cmds[cmd]) return lab.cmds[cmd];
    var keys = Object.keys(lab.cmds);
    var lower = cmd.toLowerCase();
    for (var i = 0; i < keys.length; i++) {
      if (keys[i].toLowerCase().indexOf(lower) === 0 || lower.indexOf(keys[i].toLowerCase().slice(0, 12)) === 0) {
        return lab.cmds[keys[i]];
      }
    }
    if (lower.indexOf('help') !== -1) return lab.cmds.help || 'Comandos disponíveis: ' + keys.join(', ');
    return 'Comando não reconhecido. Digite help ou clique nos atalhos.';
  }

  function runTerminal(tid, cmd) {
    var out = $('#term-out-' + tid);
    if (!out || !cmd) return;
    runTerminalTo(out, tid, cmd);
  }

  function clearTerminal(tid) {
    var out = $('#term-out-' + tid);
    var lab = TERMINALS[tid];
    if (!out || !lab) return;
    out.innerHTML = '';
    lab.welcome.split('\n').forEach(function (ln) { termLine(out, ln, 'dim'); });
  }

  function runTerminalDemo(tid) {
    var panel = document.querySelector('[data-term-panel="' + tid + '"]');
    var demo = panel && panel.dataset.termDemo;
    var lab = TERMINALS[tid];
    if (!lab) return;
    clearTerminal(tid);
    var cmds = Object.keys(lab.cmds).filter(function (k) { return k !== 'help'; }).slice(0, 3);
    if (demo && cmds.indexOf(demo) === -1) cmds.unshift(demo);
    cmds.forEach(function (cmd, i) {
      setTimeout(function () { runTerminal(tid, cmd); }, 400 * (i + 1));
    });
  }

  $$('.term-input').forEach(function (inp) {
    inp.addEventListener('keydown', function (e) {
      if (e.key !== 'Enter') return;
      e.preventDefault();
      var cmd = inp.value.trim();
      if (!cmd) return;
      runTerminal(inp.dataset.term, cmd);
      inp.value = '';
    });
  });

  // ── Simuladores OWASP ──
  /*simulators_INJECT*/

  // ── Simuladores CWE TOP 25 ──
  /*cwe-simulators_INJECT*/

  // ── OWASP Hub + Modal ──
  /*owasp-hub_INJECT*/

  // ── CWE Hub + Modal ──
  /*cwe-hub_INJECT*/

  // ── Busca (só dataset — evita ler textContent gigante) ──
  var search = $('#search');
  var searchTimer;
  if (search) {
    search.addEventListener('input', function () {
      clearTimeout(searchTimer);
      searchTimer = setTimeout(function () {
        var q = search.value.toLowerCase().trim();
        document.body.classList.toggle('search-active', !!q);
        if (q) applyFilter(null, null);
        sections.forEach(function (s) {
          if (FILTER_EXEMPT[s.id]) return;
          if (!q) {
            s.classList.remove('search-hide');
            return;
          }
          var text = (s.dataset.search || '').toLowerCase();
          s.classList.toggle('search-hide', text.indexOf(q) === -1);
        });
        $$('.owasp-card').forEach(function (card) {
          var ct = (card.dataset.search || '').toLowerCase();
          card.classList.toggle('search-hide', !!q && ct.indexOf(q) === -1);
        });
        $$('.cwe-card').forEach(function (card) {
          var ct = (card.dataset.search || '').toLowerCase();
          card.classList.toggle('search-hide', !!q && ct.indexOf(q) === -1);
        });
        $$('.news-card').forEach(function (card) {
          var ct = (card.dataset.search || '').toLowerCase();
          card.classList.toggle('search-hide', !!q && ct.indexOf(q) === -1);
        });
      }, 120);
    });
  }

  // ── Quiz ──
  var qi = 0;
  function showQuiz() {
    if (!QUIZ.length) return;
    var q = QUIZ[qi];
    var qEl = $('#quiz-q');
    var opts = $('#quiz-opts');
    var fb = $('#quiz-fb');
    if (qEl) qEl.textContent = q.q;
    if (opts) {
      opts.innerHTML = q.opts.map(function (t, i) {
        return '<button class="ok-btn ghost sm q-opt" data-i="' + i + '" type="button">' + t + '</button>';
      }).join('');
    }
    if (fb) fb.textContent = '';
  }

  document.addEventListener('click', function (e) {
    var b = e.target.closest('.q-opt');
    if (!b || !QUIZ.length) return;
    var q = QUIZ[qi];
    var fb = $('#quiz-fb');
    if (fb) fb.textContent = +b.dataset.i === q.a ? 'Correto.' : 'Resposta: ' + q.opts[q.a];
  });

  var quizNext = $('#quiz-next');
  if (quizNext) quizNext.addEventListener('click', function () {
    qi = (qi + 1) % QUIZ.length;
    showQuiz();
  });
  showQuiz();

  // ── Toolbar ──
  var btnSidebar = $('#btn-sidebar');
  if (btnSidebar) btnSidebar.addEventListener('click', function () {
    document.body.classList.toggle('sidebar-collapsed');
  });

  var btnTheme = $('#btn-theme');
  if (btnTheme) btnTheme.addEventListener('click', function () {
    document.body.classList.toggle('theme-light');
  });
  var printSnapshot = null;

  function preparePrint() {
    if (printSnapshot) return;
    printSnapshot = {
      owasp: filterOwasp,
      cwe: filterCwe,
      searchActive: document.body.classList.contains('search-active'),
      searchVal: ($('#search') && $('#search').value) || '',
      sidebarCollapsed: document.body.classList.contains('sidebar-collapsed'),
      presentMode: document.body.classList.contains('present-mode')
    };
    document.body.classList.remove('corr-filtering', 'search-active', 'sidebar-collapsed', 'present-mode');
    document.documentElement.classList.add('print-mode');
    document.body.classList.add('print-mode');
    var layout = document.querySelector('.layout');
    if (layout) {
      layout.style.setProperty('padding', '16mm 14mm 18mm', 'important');
      layout.style.setProperty('box-decoration-break', 'clone', 'important');
      layout.style.setProperty('-webkit-box-decoration-break', 'clone', 'important');
      layout.style.setProperty('box-sizing', 'border-box', 'important');
    }
    $$('.lesson-sec').forEach(function (s) { s.classList.remove('search-hide', 'filter-match', 'highlight', 'dimmed'); });
    $$('.owasp-card, .cwe-card, .news-card').forEach(function (card) {
      card.classList.remove('search-hide', 'dimmed', 'filter-match');
      card.style.display = '';
    });
    var search = $('#search');
    if (search) search.value = '';
    if (typeof window.closeOwaspModal === 'function') window.closeOwaspModal();
    if (typeof window.closeCweModal === 'function') window.closeCweModal();
    applyFilter(null, null);
    $$('.chart-embed canvas').forEach(function (c) { if (c.id) initChart(c.id); });
    Object.keys(chartRegistry).forEach(function (id) {
      var s = chartRegistry[id];
      if (!s) return;
      s.progress = 1;
      s.ready = true;
      if (s.redraw) s.redraw();
      if (typeof renderChartLegend === 'function') renderChartLegend(s);
    });
    hideChartTooltip();
  }

  function restoreAfterPrint() {
    if (!printSnapshot) return;
    document.documentElement.classList.remove('print-mode');
    document.body.classList.remove('print-mode');
    var layout = document.querySelector('.layout');
    if (layout) {
      layout.style.removeProperty('padding');
      layout.style.removeProperty('box-decoration-break');
      layout.style.removeProperty('-webkit-box-decoration-break');
      layout.style.removeProperty('box-sizing');
    }
    if (printSnapshot.sidebarCollapsed) document.body.classList.add('sidebar-collapsed');
    if (printSnapshot.presentMode) document.body.classList.add('present-mode');
    if (printSnapshot.owasp || printSnapshot.cwe) applyFilter(printSnapshot.owasp, printSnapshot.cwe);
    if (printSnapshot.searchActive) {
      var search = $('#search');
      if (search) {
        search.value = printSnapshot.searchVal;
        search.dispatchEvent(new Event('input', { bubbles: true }));
      }
    }
    printSnapshot = null;
  }

  window.addEventListener('beforeprint', preparePrint);
  window.addEventListener('afterprint', restoreAfterPrint);

  var btnPdf = $('#btn-pdf');
  if (btnPdf) {
    btnPdf.addEventListener('click', function () {
      preparePrint();
      setTimeout(function () { window.print(); }, 200);
    });
  }
  var btnPresent = $('#btn-present');
  if (btnPresent) btnPresent.addEventListener('click', function () {
    document.body.classList.toggle('present-mode');
  });

  // ── Progresso ──
  var seen = new Set();
  var progTimer;
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      var changed = false;
      entries.forEach(function (en) {
        if (en.isIntersecting && en.target.id && !seen.has(en.target.id)) {
          seen.add(en.target.id);
          changed = true;
        }
      });
      if (!changed) return;
      clearTimeout(progTimer);
      progTimer = setTimeout(function () {
        var prog = $('#progress');
        if (prog) prog.style.width = Math.round(seen.size / 55 * 100) + '%';
        seen.forEach(function (id) {
          $$('.nav-link[href="#' + id + '"]').forEach(function (l) {
            l.classList.add('done');
          });
        });
      }, 80);
    }, { threshold: 0.25, rootMargin: '0px 0px -10% 0px' });
    sections.forEach(function (s) { io.observe(s); });
    if (hero) io.observe(hero);
  }

  var navScrollTimer;
  function updateNavActive() {
    var links = $$('.sidebar .nav-link');
    var hash = location.hash;
    if (hash && hash.length > 1) {
      links.forEach(function (l) { l.classList.remove('active'); });
      var hashLink = $('.sidebar .nav-link[href="' + hash + '"]');
      if (hashLink) {
        hashLink.classList.add('active');
        return;
      }
    }
    var best = null;
    var bestTop = -Infinity;
    links.forEach(function (link) {
      var id = (link.getAttribute('href') || '').slice(1);
      if (!id) return;
      var el = resolveScrollTarget(id);
      if (!el) return;
      var top = el.getBoundingClientRect().top;
      if (top <= getScrollOffset() + 24 && top > bestTop) {
        bestTop = top;
        best = link;
      }
    });
    links.forEach(function (l) { l.classList.remove('active'); });
    if (best) best.classList.add('active');
  }
  window.addEventListener('scroll', function () {
    clearTimeout(navScrollTimer);
    navScrollTimer = setTimeout(updateNavActive, 40);
  }, { passive: true });
  window.addEventListener('hashchange', updateNavActive);
  updateNavActive();

  document.addEventListener('keydown', function (e) {
    if (!document.body.classList.contains('present-mode')) return;
    var secs = sections.filter(function (s) {
      return !s.classList.contains('search-hide') && !FILTER_EXEMPT[s.id];
    });
    var idx = secs.findIndex(function (s) {
      var r = s.getBoundingClientRect();
      return r.top >= -100 && r.top < window.innerHeight / 2;
    });
    if (e.key === 'ArrowDown' && idx < secs.length - 1) secs[idx + 1].scrollIntoView({ behavior: 'smooth' });
    if (e.key === 'ArrowUp' && idx > 0) secs[idx - 1].scrollIntoView({ behavior: 'smooth' });
  });

  // ── Gráficos interativos (Canvas + tooltip + hover + clique) ──
  var chartRegistry = {};
  var chartInited = {};
  var chartTooltipEl = null;
  function chartTheme() {
    var cs = getComputedStyle(document.body);
    return {
      fg: cs.getPropertyValue('--ok-fg').trim() || '#f4f4f8',
      fgSoft: cs.getPropertyValue('--ok-fg-soft').trim() || '#b9bac8',
      fgMute: cs.getPropertyValue('--ok-fg-mute').trim() || '#6c6d80',
      bg1: cs.getPropertyValue('--ok-bg-1').trim() || '#0b0b12',
      light: document.body.classList.contains('theme-light')
    };
  }

  function chartPalette() {
    if (chartTheme().light) {
      return {
        accent: '#b8420a',
        magenta: '#8f1f5c',
        cyan: '#0a6570',
        mute: '#3a3e50',
        dim: '#5c6074',
        success: '#1a6b42',
        warning: '#7a5a08',
        upBar: '#c44a10',
        upLabel: '#8f3208',
        downBar: '#0a6570',
        downLabel: '#084f58',
        ink: '30,33,48'
      };
    }
    return {
      accent: '#ff6b35',
      magenta: '#e040a0',
      cyan: '#5ce1e6',
      mute: '#6c6d80',
      dim: '#3d3e50',
      success: '#7ee787',
      warning: '#d2a8ff',
      upBar: '#ff6b35',
      upLabel: '#ff8f5c',
      downBar: '#5ce1e6',
      downLabel: '#5ce1e6',
      ink: '185,186,200'
    };
  }

  function chartHotInk() {
    var t = chartTheme();
    return t.light ? t.fg : '#fff';
  }

  function chartInk(alpha) {
    var a = alpha != null ? alpha : 1;
    return 'rgba(' + chartPalette().ink + ',' + a + ')';
  }

  function chartColors() {
    var p = chartPalette();
    return [p.accent, p.magenta, p.cyan, p.mute, p.dim, p.success, p.warning];
  }

  function chartHexAlpha(hex, alpha) {
    var h = String(hex || '').replace('#', '');
    if (h.length === 3) h = h.split('').map(function (c) { return c + c; }).join('');
    if (h.length !== 6) return 'rgba(255,107,53,' + alpha + ')';
    return 'rgba(' + parseInt(h.slice(0, 2), 16) + ',' + parseInt(h.slice(2, 4), 16) + ',' + parseInt(h.slice(4, 6), 16) + ',' + alpha + ')';
  }

  function chartEsc(s) {
    return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
  }

  function chartBg() {
    return getComputedStyle(document.body).getPropertyValue('--ok-bg-1').trim() || '#0b0b12';
  }

  function getChartTooltip() {
    if (!chartTooltipEl) {
      chartTooltipEl = document.createElement('div');
      chartTooltipEl.className = 'chart-tooltip';
      chartTooltipEl.setAttribute('role', 'tooltip');
      document.body.appendChild(chartTooltipEl);
    }
    return chartTooltipEl;
  }

  function showChartTooltip(cx, cy, html) {
    var tip = getChartTooltip();
    tip.innerHTML = html;
    tip.classList.add('visible');
    var pad = 16;
    var rect = tip.getBoundingClientRect();
    var left = cx + pad;
    var top = cy - rect.height - pad;
    if (left + rect.width > window.innerWidth - 10) left = cx - rect.width - pad;
    if (top < 10) top = cy + pad;
    if (left < 10) left = 10;
    tip.style.left = left + 'px';
    tip.style.top = top + 'px';
  }

  function hideChartTooltip() {
    if (chartTooltipEl) chartTooltipEl.classList.remove('visible');
  }

  function chartPointer(canvas, e) {
    var rect = canvas.getBoundingClientRect();
    var dpr = Math.min(window.devicePixelRatio || 1, 2);
    var logicalW = canvas.width / dpr;
    var logicalH = canvas.height / dpr;
    if (!rect.width || !rect.height) {
      return { x: 0, y: 0, cx: e.clientX, cy: e.clientY };
    }
    return {
      x: (e.clientX - rect.left) * (logicalW / rect.width),
      y: (e.clientY - rect.top) * (logicalH / rect.height),
      cx: e.clientX,
      cy: e.clientY
    };
  }

  function chartInnerWidth(node) {
    if (!node) return 0;
    var style = window.getComputedStyle(node);
    var padL = parseFloat(style.paddingLeft) || 0;
    var padR = parseFloat(style.paddingRight) || 0;
    var inner = node.clientWidth - padL - padR;
    if (inner >= 8) return Math.round(inner);
    var rect = node.getBoundingClientRect();
    return rect.width >= 8 ? Math.round(rect.width - padL - padR) : 0;
  }

  function chartBoxWidth(canvas) {
    var node = canvas.parentElement;
    while (node) {
      var w = chartInnerWidth(node);
      if (w >= 8) return w;
      node = node.parentElement;
    }
    var rect = canvas.getBoundingClientRect();
    return rect.width >= 8 ? Math.round(rect.width) : 320;
  }

  function applyCanvasSize(canvas, w, h) {
    var dpr = Math.min(window.devicePixelRatio || 1, 2);
    w = Math.max(1, Math.round(w));
    h = Math.max(1, Math.round(h));
    canvas.width = Math.floor(w * dpr);
    canvas.height = Math.floor(h * dpr);
    canvas.style.width = w + 'px';
    canvas.style.height = h + 'px';
    canvas.style.maxWidth = '100%';
    canvas.style.display = 'block';
    var ctx = canvas.getContext('2d');
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    return { ctx: ctx, w: w, h: h };
  }

  function setupCanvas(canvas, height) {
    var w = chartBoxWidth(canvas);
    var h = height || parseInt(canvas.getAttribute('height'), 10) || 240;
    return applyCanvasSize(canvas, w, h);
  }

  function chartCanvasHeight(count, rowH, pad) {
    return Math.max(240, count * rowH + (pad || 32));
  }

  function setupCanvasSquare(canvas) {
    var wrap = canvas.parentElement;
    var raw = wrap ? (wrap.clientWidth || chartBoxWidth(canvas)) : chartBoxWidth(canvas);
    var size = Math.max(220, Math.min(Math.round(raw) || 280, 360));
    return applyCanvasSize(canvas, size, size);
  }

  function sortChartDesc(data) {
    return data.slice().sort(function (a, b) { return b.v - a.v; });
  }

  function drawChartGrid(ctx, w, h, pad) {
    ctx.strokeStyle = chartInk(0.12);
    ctx.lineWidth = 1;
    for (var g = 0; g <= 4; g++) {
      var gy = pad.t + g * (h - pad.t - pad.b) / 4;
      ctx.beginPath();
      ctx.moveTo(pad.l, gy);
      ctx.lineTo(w - pad.r, gy);
      ctx.stroke();
    }
    ctx.strokeStyle = chartInk(0.22);
    ctx.beginPath();
    ctx.moveTo(pad.l, pad.t);
    ctx.lineTo(pad.l, h - pad.b);
    ctx.stroke();
  }

  function roundBar(ctx, x, y, w, h, r) {
    if (h <= 0) return;
    r = Math.min(r, w / 2, h);
    ctx.beginPath();
    ctx.moveTo(x, y + h);
    ctx.lineTo(x, y + r);
    ctx.quadraticCurveTo(x, y, x + r, y);
    ctx.lineTo(x + w - r, y);
    ctx.quadraticCurveTo(x + w, y, x + w, y + r);
    ctx.lineTo(x + w, y + h);
    ctx.closePath();
    ctx.fill();
  }

  function legendColor(state, i) {
    var palette = chartColors();
    var p = chartPalette();
    if (state.type === 'donut' || state.type === 'hbar') return palette[i % palette.length];
    if (state.type === 'bar' && state.opts.color) return state.opts.color;
    if (state.type === 'delta') return state.data[i].dir === 'up' ? p.upBar : p.downBar;
    return palette[i % palette.length];
  }

  function legendValue(state, d) {
    if (state.type === 'donut') return Math.round((d.v / state.total) * 100) + '%';
    if (state.type === 'hbar' && d.survey) return 'survey';
    if (state.type === 'hbar') return d.v + (state.opts.suffix || '');
    if (state.type === 'delta') return (d.dir === 'up' ? '↑' : '↓') + d.v;
    if (state.type === 'trend') return '#' + d.rank;
    return String(d.v) + (state.opts.unit || state.opts.suffix || '');
  }

  function chartLegendLabel(state, d) {
    if (state.type === 'delta') return d.short || d.name_pt || d.id || d.l;
    if (state.opts.cweClick) return d.name_pt || d.l;
    return d.l;
  }

  function chartLegendSub(state, d) {
    if (state.type === 'delta') return '#' + d.prev + ' → #' + d.rank + ' · ' + (d.id || '');
    if (state.type === 'donut') return d.v + ' correlação' + (d.v === 1 ? '' : 'ões');
    if (state.opts.owaspPrev && d.name) return d.name + (d.cwes && d.cwes != '—' ? ' · ' + d.cwes : '');
    if (state.opts.cweClick && d.id) return d.id + (d.rank ? ' · MITRE #' + d.rank : '');
    return '';
  }

  function syncChartHover(canvasId, idx, tipX, tipY) {
    var state = chartRegistry[canvasId];
    if (!state) return;
    if (state.hover !== idx) {
      state.hover = idx;
      state.redraw();
    }
    var host = document.getElementById(canvasId + '-legend');
    if (host) {
      host.querySelectorAll('.chart-legend-item').forEach(function (el) {
        el.classList.toggle('active', parseInt(el.getAttribute('data-idx'), 10) === idx);
      });
    }
    if (idx >= 0) {
      if (tipX != null && tipY != null) showChartTooltip(tipX, tipY, state.tooltip(idx));
      else if (host) {
        var item = host.querySelector('.chart-legend-item[data-idx="' + idx + '"]');
        if (item) {
          var r = item.getBoundingClientRect();
          showChartTooltip(r.left + r.width / 2, r.top, state.tooltip(idx));
        }
      }
    } else hideChartTooltip();
  }

  function renderChartLegend(state) {
    var host = document.getElementById(state.canvasId + '-legend');
    if (!host || !state.data.length) return;
    var maxV = Math.max.apply(null, state.data.map(function (d) { return d.v; })) || 1;
    host.innerHTML = state.data.map(function (d, i) {
      var color = legendColor(state, i);
      var pct = state.type === 'donut' ? Math.round((d.v / state.total) * 100) : Math.round((d.v / maxV) * 100);
      var meter = (state.type === 'donut' || state.type === 'hbar') ?
        '<span class="chart-legend-meter"><i style="width:' + pct + '%;background:' + color + '"></i></span>' : '';
      var rankNum = d.rank != null ? String(d.rank).padStart(2, '0') : String(i + 1).padStart(2, '0');
      var rank = state.opts.ranked ? '<span class="chart-legend-rank">' + rankNum + '</span>' :
        (state.type === 'delta' ? '<span class="chart-legend-rank">' + (d.dir === 'up' ? '↑' : '↓') + '</span>' : '');
      var sub = chartLegendSub(state, d);
      var subHtml = sub ? '<span class="chart-legend-sub">' + chartEsc(sub) + '</span>' : '';
      var itemCls = 'chart-legend-item' + (state.type === 'donut' ? ' chart-legend-item--donut' : '');
      return '<button type="button" class="' + itemCls + '" data-chart="' + state.canvasId + '" data-idx="' + i + '">' +
        rank +
        '<span class="chart-legend-swatch" style="background:' + color + '"></span>' +
        '<span class="chart-legend-label">' + chartEsc(chartLegendLabel(state, d)) + '</span>' +
        '<span class="chart-legend-val">' + chartEsc(legendValue(state, d)) + '</span>' +
        subHtml + meter + '</button>';
    }).join('');
    host.querySelectorAll('.chart-legend-item').forEach(function (btn) {
      btn.addEventListener('mouseenter', function () {
        syncChartHover(state.canvasId, parseInt(btn.getAttribute('data-idx'), 10));
      });
      btn.addEventListener('mouseleave', function () {
        syncChartHover(state.canvasId, -1);
      });
      btn.addEventListener('focus', function () {
        syncChartHover(state.canvasId, parseInt(btn.getAttribute('data-idx'), 10));
      });
      btn.addEventListener('blur', function () {
        syncChartHover(state.canvasId, -1);
      });
      btn.addEventListener('click', function () {
        var idx = parseInt(btn.getAttribute('data-idx'), 10);
        if (state.onClick && state.data[idx]) state.onClick(state.data[idx], idx);
      });
    });
  }

  function bindChart(canvasId, state) {
    var canvas = document.getElementById(canvasId);
    if (!canvas || canvas._chartBound) return;
    canvas._chartBound = true;
    canvas.addEventListener('mousemove', function (e) {
      if (!state.ready) return;
      var pt = chartPointer(canvas, e);
      var idx = state.hitTest(pt.x, pt.y);
      syncChartHover(canvasId, idx, pt.cx, pt.cy);
    });
    canvas.addEventListener('mouseleave', function () {
      syncChartHover(canvasId, -1);
    });
    canvas.addEventListener('click', function (e) {
      if (!state.ready || !state.onClick) return;
      var pt = chartPointer(canvas, e);
      var idx = state.hitTest(pt.x, pt.y);
      if (idx >= 0) state.onClick(state.data[idx], idx);
    });
  }

  function animateChart(state, step) {
    if (state.progress >= 1) {
      state.ready = true;
      state.redraw();
      if (!state.legendBuilt) {
        state.legendBuilt = true;
        renderChartLegend(state);
      }
      return;
    }
    state.progress = Math.min(1, state.progress + step);
    state.redraw();
    requestAnimationFrame(function () { animateChart(state, step); });
  }

  function filterOwaspFromChart(id) {
    if (window.openOwaspModal) window.openOwaspModal(id);
  }

  function filterCweFromChart(id) {
    if (window.openCweModal) window.openCweModal(id);
  }

  function mountBarChart(canvasId, data, opts) {
    var canvas = document.getElementById(canvasId);
    if (!canvas || !data.length) return;
    var state = {
      canvasId: canvasId, type: 'bar', data: data, opts: opts || {},
      progress: 0, ready: false, hover: -1, regions: [],
      redraw: function () { drawBarChart(state); },
      hitTest: function (x, y) {
        for (var i = 0; i < state.regions.length; i++) {
          var r = state.regions[i];
          if (x >= r.x && x <= r.x + r.w && y >= r.y && y <= r.y + r.h) return r.i;
        }
        return -1;
      },
      tooltip: function (i) {
        var d = data[i];
        var lines = '<strong>' + chartEsc(d.l) + '</strong>';
        lines += '<span>Valor: <em>' + d.v + (opts.unit || '') + '</em></span>';
        if (d.id) lines += '<span>' + chartEsc(d.id) + '</span>';
        if (d.rank) lines += '<span>Ranking MITRE: #' + d.rank + '</span>';
        if (d.kev) lines += '<span>Entradas CISA KEV: ' + d.kev + '</span>';
        return lines;
      },
      onClick: opts.onClick || (opts.cweClick ? function (d) { filterCweFromChart(d.id); } : null)
    };
    chartRegistry[canvasId] = state;
    bindChart(canvasId, state);
    observeChartCanvas(canvasId);
    animateChart(state, 0.04);
  }

  function drawBarChart(state) {
    var canvas = document.getElementById(state.canvasId);
    if (!canvas) return;
    var dims = setupCanvas(canvas, state.opts.height || 320);
    var ctx = dims.ctx, w = dims.w, h = dims.h;
    var data = state.data, max = Math.max.apply(null, data.map(function (d) { return d.v; })) || 1;
    var pad = { l: 44, r: 12, t: 16, b: state.opts.compactLabels ? 28 : 40 };
    var plotW = w - pad.l - pad.r;
    var plotH = h - pad.t - pad.b;
    var gap = data.length > 16 ? 2 : 4;
    var barW = Math.max(6, plotW / data.length - gap);
    var color = state.opts.color || '#ff6b35';
    state.regions = [];
    ctx.clearRect(0, 0, w, h);
    drawChartGrid(ctx, w, h, pad);
    data.forEach(function (d, i) {
      var bh = (d.v / max) * plotH * state.progress;
      var x = pad.l + i * (barW + gap);
      var y = pad.t + plotH - bh;
      var hot = state.hover === i;
      var dim = state.hover >= 0 && !hot;
      var grad = ctx.createLinearGradient(x, y, x, pad.t + plotH);
      grad.addColorStop(0, hot ? chartHotInk() : color);
      grad.addColorStop(1, hot ? color : 'rgba(255,107,53,0.15)');
      ctx.globalAlpha = dim ? 0.35 : 1;
      ctx.fillStyle = grad;
      roundBar(ctx, x, y, barW, bh, Math.min(4, barW / 3));
      ctx.globalAlpha = 1;
      if (hot && bh > 2) {
        ctx.strokeStyle = chartInk(0.75);
        ctx.lineWidth = 1.5;
        ctx.strokeRect(x + 0.5, y + 0.5, barW - 1, bh - 1);
        ctx.fillStyle = chartHotInk();
        ctx.font = 'bold 10px JetBrains Mono';
        ctx.textAlign = 'center';
        ctx.fillText(d.v + (state.opts.unit || ''), x + barW / 2, y - 6);
        ctx.textAlign = 'left';
      }
      if (state.progress >= 1) state.regions.push({ x: x, y: pad.t, w: barW, h: plotH, i: i });
      if (!state.opts.compactLabels || hot) {
        ctx.fillStyle = hot ? chartHotInk() : chartInk(0.85);
        ctx.font = (data.length > 16 ? '9px' : '10px') + ' JetBrains Mono';
        ctx.save();
        ctx.translate(x + barW / 2, h - 6);
        ctx.rotate(-Math.PI / 4);
        ctx.fillText(d.l, 0, 0);
        ctx.restore();
      }
    });
  }

  function mountHBarChart(canvasId, data, opts) {
    var canvas = document.getElementById(canvasId);
    if (!canvas || !data.length) return;
    opts = opts || {};
    var sorted = opts.preserveOrder ? data.slice() : sortChartDesc(data);
    var rowH = opts.cweRanked ? 42 : 32;
    opts.height = chartCanvasHeight(sorted.length, rowH, 28);
    var state = {
      canvasId: canvasId, type: 'hbar', data: sorted, opts: opts,
      progress: 0, ready: false, hover: -1, regions: [],
      redraw: function () { drawHBarChart(state); },
      hitTest: function (x, y) {
        for (var i = 0; i < state.regions.length; i++) {
          var r = state.regions[i];
          if (x >= r.x && x <= r.x + r.w && y >= r.y && y <= r.y + r.h) return r.i;
        }
        return -1;
      },
      tooltip: function (i) {
        var d = sorted[i];
        if (opts.cweClick) {
          return '<strong>' + chartEsc(d.name_pt || d.l) + '</strong>' +
            '<span>' + chartEsc(d.id) + ' · posição #' + d.rank + '</span>' +
            '<span>Score MITRE: <em>' + d.v + (opts.suffix || '') + '</em></span>' +
            (d.kev ? '<span>' + d.kev + ' CVEs no CISA KEV</span>' : '') +
            '<span>Clique para abrir o painel da fraqueza</span>';
        }
        if (opts.owaspPrev && d.survey) {
          return '<strong>' + chartEsc(d.l) + ' — ' + chartEsc(d.name || '') + '</strong><span>Sem % publicado em testes automatizados</span><span>Ranking via community survey OWASP</span>';
        }
        if (opts.owaspPrev) {
          return '<strong>' + chartEsc(d.l) + ' — ' + chartEsc(d.name || '') + '</strong><span>Prevalência: <em>' + d.v + (opts.suffix || '') + '</em></span><span>OWASP Top 10:2025 · 2,8M+ apps testadas</span>';
        }
        return '<strong>' + chartEsc(d.l) + '</strong><span>Prevalência: <em>' + d.v + (opts.suffix || '') + '</em></span><span>OWASP Top 10:2025 · 2,8M+ apps</span>';
      },
      onClick: opts.cweClick ? function (d) { filterCweFromChart(d.id); } : function (d) { filterOwaspFromChart(d.l); }
    };
    chartRegistry[canvasId] = state;
    bindChart(canvasId, state);
    observeChartCanvas(canvasId);
    animateChart(state, 0.05);
  }

  function drawHBarChart(state) {
    var canvas = document.getElementById(state.canvasId);
    if (!canvas) return;
    var data = state.data;
    var rowH = state.opts.cweRanked ? 42 : 32;
    var targetH = chartCanvasHeight(data.length, rowH, 28);
    if (state.opts.height !== targetH) state.opts.height = targetH;
    var dims = setupCanvas(canvas, targetH);
    var ctx = dims.ctx, w = dims.w, h = dims.h;
    var published = data.filter(function (d) { return !d.survey && d.v > 0; });
    var max = Math.max.apply(null, (published.length ? published : data).map(function (d) { return d.v; })) || 1;
    var pad = { l: 10, r: 10, t: 12, b: 12 };
    var ranked = !!state.opts.ranked;
    var cweMinimal = !!state.opts.cweRanked;
    var rankW = ranked ? 30 : 0;
    var valW = state.opts.owaspPrev ? 72 : 64;
    var barX = pad.l + rankW + (cweMinimal ? 6 : 40);
    var barMax = Math.max(80, w - barX - pad.r - valW);
    state.regions = [];
    ctx.clearRect(0, 0, w, h);
    if (ranked) {
      ctx.strokeStyle = chartInk(0.12);
      ctx.lineWidth = 1;
      ctx.beginPath();
      ctx.moveTo(barX - 4, pad.t);
      ctx.lineTo(barX - 4, h - pad.b);
      ctx.stroke();
    }
    data.forEach(function (d, i) {
      var isSurvey = !!d.survey;
      var bw = isSurvey ? 0 : (d.v / max) * barMax * state.progress;
      var y = pad.t + i * rowH;
      var hot = state.hover === i;
      var dim = state.hover >= 0 && !hot;
      var palette = chartColors();
      var barCol = palette[i % palette.length];
      var barTop = y + 11;
      var barHt = rowH - 22;
      ctx.globalAlpha = dim ? 0.38 : 1;
      if (ranked) {
        ctx.fillStyle = hot ? chartHotInk() : chartInk(0.5);
        ctx.font = '11px JetBrains Mono';
        ctx.textAlign = 'right';
        var rk = d.rank != null ? d.rank : (i + 1);
        ctx.fillText(String(rk).padStart(2, '0'), pad.l + rankW - 4, y + rowH * 0.58);
        ctx.textAlign = 'left';
      }
      if (!cweMinimal) {
        ctx.fillStyle = hot ? chartHotInk() : chartInk(0.9);
        ctx.font = 'bold 11px JetBrains Mono';
        ctx.fillText(d.l, pad.l + rankW, y + rowH * 0.58);
      }
      ctx.fillStyle = chartInk(0.07);
      ctx.fillRect(barX, barTop, barMax, barHt);
      if (!isSurvey) {
        var grad = ctx.createLinearGradient(barX, y, barX + Math.max(bw, 1), y);
        grad.addColorStop(0, hot ? chartHotInk() : barCol);
        grad.addColorStop(1, hot ? chartHexAlpha(barCol, 0.38) : chartHexAlpha(barCol, 0.14));
        ctx.fillStyle = grad;
        roundBar(ctx, barX, barTop, Math.max(bw, hot ? 4 : 0), barHt, 5);
        if (hot) {
          ctx.strokeStyle = barCol;
          ctx.lineWidth = 1.5;
          ctx.strokeRect(barX + 0.5, barTop + 0.5, Math.max(bw, 3) - 1, barHt - 1);
        }
      } else {
        ctx.strokeStyle = chartInk(hot ? 0.35 : 0.18);
        ctx.lineWidth = 1;
        ctx.setLineDash([4, 4]);
        ctx.strokeRect(barX + 0.5, barTop + 0.5, barMax - 1, barHt - 1);
        ctx.setLineDash([]);
      }
      ctx.fillStyle = hot ? chartHotInk() : (isSurvey ? chartInk(0.55) : barCol);
      ctx.font = 'bold 11px JetBrains Mono';
      ctx.textAlign = 'left';
      var valX = isSurvey ? barX + 8 : barX + Math.max(bw, 0) + 8;
      if (valX + 56 > w - pad.r) valX = w - pad.r - 56;
      ctx.fillText(isSurvey ? 'survey' : (d.v + (state.opts.suffix || '')), valX, y + rowH * 0.58);
      ctx.textAlign = 'left';
      ctx.globalAlpha = 1;
      if (state.progress >= 1) state.regions.push({ x: 0, y: y, w: w, h: rowH, i: i });
    });
  }

  function mountDonutChart(canvasId, data, opts) {
    var canvas = document.getElementById(canvasId);
    if (!canvas || !data.length) return;
    opts = opts || {};
    var sorted = sortChartDesc(data);
    var state = {
      canvasId: canvasId, type: 'donut', data: sorted, opts: opts,
      progress: 0, ready: false, hover: -1, slices: [],
      redraw: function () { drawDonutChart(state); },
      hitTest: function (x, y) {
        var s = state.layout;
        if (!s || !state.slices.length) return -1;
        var dx = x - s.cx, dy = y - s.cy;
        var dist = Math.sqrt(dx * dx + dy * dy);
        if (dist < s.ir - 2 || dist > s.r + 10) return -1;
        var rel = Math.atan2(dy, dx) + Math.PI / 2;
        if (rel < 0) rel += Math.PI * 2;
        for (var i = 0; i < state.slices.length; i++) {
          var sl = state.slices[i];
          if (sl.start <= sl.end) {
            if (rel >= sl.start && rel < sl.end) return i;
          } else if (rel >= sl.start || rel < sl.end) return i;
        }
        return -1;
      },
      tooltip: function (i) {
        var d = sorted[i], pct = Math.round((d.v / state.total) * 100);
        var extra = opts.owaspClick ? '<span>Clique para filtrar ' + chartEsc(d.l) + ' na matriz</span>' : '<span>Representa ' + pct + '% do total</span>';
        return '<strong>' + chartEsc(d.l) + '</strong><span>Valor: <em>' + d.v + '</em> · ' + pct + '%</span>' + extra;
      },
      onClick: opts.onClick || (opts.owaspClick ? function (d) { filterOwaspFromChart(d.l); } : null),
      total: sorted.reduce(function (a, d) { return a + d.v; }, 0)
    };
    chartRegistry[canvasId] = state;
    bindChart(canvasId, state);
    observeChartCanvas(canvasId);
    requestAnimationFrame(function () { animateChart(state, 0.035); });
  }

  function observeChartCanvas(canvasId) {
    var canvas = document.getElementById(canvasId);
    if (!canvas || canvas._sizeObserved || !('ResizeObserver' in window)) return;
    var parent = canvas.parentElement;
    if (!parent) return;
    canvas._sizeObserved = true;
    var resizeTimer;
    var ro = new ResizeObserver(function () {
      clearTimeout(resizeTimer);
      resizeTimer = setTimeout(function () {
        var s = chartRegistry[canvasId];
        if (s && s.ready && s.redraw) s.redraw();
      }, 80);
    });
    ro.observe(parent);
  }

  function redrawAllCharts() {
    Object.keys(chartRegistry).forEach(function (id) {
      var s = chartRegistry[id];
      if (s && s.ready && s.redraw) s.redraw();
    });
  }

  function drawDonutChart(state) {
    var canvas = document.getElementById(state.canvasId);
    if (!canvas) return;
    var dims = setupCanvasSquare(canvas);
    var ctx = dims.ctx, w = dims.w, h = dims.h;
    var cx = w / 2, cy = h / 2;
    var r = Math.min(w, h) * 0.4;
    var ir = r * 0.56;
    var GAP = 0.028;
    var totalGap = GAP * state.data.length;
    var avail = Math.PI * 2 - totalGap;
    state.layout = { cx: cx, cy: cy, r: r, ir: ir };
    state.slices = [];
    ctx.clearRect(0, 0, w, h);
    ctx.beginPath();
    ctx.arc(cx, cy, r + 3, 0, Math.PI * 2);
    ctx.strokeStyle = 'rgba(92,225,230,0.14)';
    ctx.lineWidth = 1;
    ctx.stroke();
    ctx.beginPath();
    ctx.arc(cx, cy, ir - 4, 0, Math.PI * 2);
    ctx.strokeStyle = chartInk(0.08);
    ctx.stroke();
    var start = -Math.PI / 2;
    var hasHover = state.hover >= 0 && state.progress >= 1;
    var palette = chartColors();
    state.data.forEach(function (d, i) {
      var slice = (d.v / state.total) * avail * state.progress;
      var hot = state.hover === i;
      var end = start + slice;
      var col = palette[i % palette.length];
      if (slice > 0.005) {
        ctx.beginPath();
        ctx.arc(cx, cy, hot ? r + 8 : r, start, end);
        ctx.arc(cx, cy, ir, end, start, true);
        ctx.closePath();
        ctx.fillStyle = col;
        ctx.globalAlpha = hot ? 1 : (hasHover ? 0.22 : 0.95);
        ctx.fill();
        ctx.globalAlpha = 1;
        if (hot) {
          ctx.strokeStyle = 'rgba(255,255,255,0.95)';
          ctx.lineWidth = 2;
          ctx.stroke();
        }
      }
      if (state.progress >= 1 && slice > 0.005) {
        var a0 = start + Math.PI / 2;
        var a1 = end + Math.PI / 2;
        if (a0 < 0) a0 += Math.PI * 2;
        if (a1 < 0) a1 += Math.PI * 2;
        state.slices.push({ start: a0, end: a1, i: i });
      }
      start = end + GAP;
    });
    ctx.textAlign = 'center';
    if (hasHover) {
      var hd = state.data[state.hover];
      var pct = Math.round((hd.v / state.total) * 100);
      ctx.fillStyle = palette[state.hover % palette.length];
      ctx.font = 'bold 18px JetBrains Mono';
      ctx.fillText(hd.l, cx, cy - 8);
      ctx.fillStyle = chartTheme().fg;
      ctx.font = 'bold 13px JetBrains Mono';
      ctx.fillText(pct + '%', cx, cy + 10);
      ctx.font = '10px JetBrains Mono';
      ctx.fillStyle = chartInk(0.9);
      ctx.fillText(hd.v + ' no total', cx, cy + 26);
    } else if (state.progress >= 1) {
      var idle = state.opts.centerIdle || { main: String(state.data.length), sub: 'itens' };
      ctx.fillStyle = chartTheme().fg;
      ctx.font = 'bold 28px JetBrains Mono';
      ctx.fillText(idle.main, cx, cy - 12);
      if (idle.sub) {
        ctx.font = '10px JetBrains Mono';
        ctx.fillStyle = chartInk(0.82);
        String(idle.sub).split(' · ').forEach(function (line, li) {
          ctx.fillText(line, cx, cy + 6 + li * 13);
        });
      }
    }
    ctx.textAlign = 'left';
  }

  function mountDeltaChart(canvasId, data) {
    var canvas = document.getElementById(canvasId);
    if (!canvas || !data.length) return;
    var rowH = 40;
    var state = {
      canvasId: canvasId, type: 'delta', data: data, opts: { height: chartCanvasHeight(data.length, rowH, 36) },
      progress: 0, ready: false, hover: -1, regions: [],
      redraw: function () { drawDeltaChart(state); },
      hitTest: function (x, y) {
        for (var i = 0; i < state.regions.length; i++) {
          var r = state.regions[i];
          if (x >= r.x && x <= r.x + r.w && y >= r.y && y <= r.y + r.h) return r.i;
        }
        return -1;
      },
      tooltip: function (i) {
        var d = data[i];
        var dir = d.dir === 'up' ? 'Subiu' : 'Desceu';
        return '<strong>' + chartEsc(d.name_pt || d.id || d.l) + '</strong>' +
          '<span>' + chartEsc(d.id || '') + '</span>' +
          '<span>' + dir + ' <em>' + d.v + '</em> posições · #' + d.prev + ' → #' + d.rank + '</span>' +
          '<span>Clique para ver detalhes da fraqueza</span>';
      },
      onClick: function (d) { if (d.id) filterCweFromChart(d.id); }
    };
    chartRegistry[canvasId] = state;
    bindChart(canvasId, state);
    observeChartCanvas(canvasId);
    animateChart(state, 0.05);
  }

  function drawDeltaChart(state) {
    var canvas = document.getElementById(state.canvasId);
    if (!canvas) return;
    var data = state.data;
    var rowH = 40;
    var targetH = chartCanvasHeight(data.length, rowH, 36);
    if (state.opts.height !== targetH) state.opts.height = targetH;
    var dims = setupCanvas(canvas, targetH);
    var ctx = dims.ctx, w = dims.w, h = dims.h;
    var p = chartPalette();
    var absVals = data.map(function (d) { return Math.abs(d.v); });
    var max = Math.max.apply(null, absVals) || 1;
    var pad = { t: 28, b: 10, l: 12, r: 12 };
    var mid = Math.floor(w / 2);
    var barMax = Math.max(48, (w - pad.l - pad.r) / 2 - 40);
    state.regions = [];
    ctx.clearRect(0, 0, w, h);
    ctx.strokeStyle = chartInk(0.28);
    ctx.setLineDash([5, 5]);
    ctx.beginPath();
    ctx.moveTo(mid, pad.t - 6);
    ctx.lineTo(mid, h - pad.b);
    ctx.stroke();
    ctx.setLineDash([]);
    ctx.fillStyle = chartInk(0.72);
    ctx.font = 'bold 9px JetBrains Mono';
    ctx.textAlign = 'center';
    ctx.fillText('2024', mid, 14);
    ctx.font = 'bold 8px JetBrains Mono';
    ctx.fillStyle = chartInk(0.58);
    ctx.fillText('desceu', mid - barMax * 0.55, pad.t - 2);
    ctx.fillText('subiu', mid + barMax * 0.55, pad.t - 2);
    data.forEach(function (d, i) {
      var y = pad.t + i * rowH;
      var mag = Math.abs(d.v);
      var bw = (mag / max) * barMax * state.progress;
      var hot = state.hover === i;
      var barH = 18;
      var barY = y + (rowH - barH) / 2;
      var dim = state.hover >= 0 && !hot;
      var dir = d.dir || (d.v >= 0 ? 'up' : 'down');
      ctx.globalAlpha = dim ? 0.35 : 1;
      if (dir === 'up') {
        ctx.fillStyle = hot ? chartHotInk() : p.upBar;
        roundBar(ctx, mid + 3, barY, Math.max(bw, hot ? 4 : 0), barH, 4);
        ctx.fillStyle = hot ? chartHotInk() : p.upLabel;
        ctx.font = 'bold 11px JetBrains Mono';
        ctx.textAlign = 'left';
        ctx.fillText('+' + mag, mid + bw + 10, barY + barH * 0.72);
      } else {
        ctx.fillStyle = hot ? chartHotInk() : p.downBar;
        roundBar(ctx, mid - Math.max(bw, hot ? 4 : 0) - 3, barY, Math.max(bw, hot ? 4 : 0), barH, 4);
        ctx.fillStyle = hot ? chartHotInk() : p.downLabel;
        ctx.font = 'bold 11px JetBrains Mono';
        ctx.textAlign = 'right';
        ctx.fillText('-' + mag, mid - bw - 10, barY + barH * 0.72);
      }
      ctx.textAlign = 'left';
      ctx.globalAlpha = 1;
      if (state.progress >= 1) state.regions.push({ x: 0, y: y, w: w, h: rowH, i: i });
    });
  }

  function mountTrendChart(canvasId, data) {
    var canvas = document.getElementById(canvasId);
    if (!canvas || !data.length) return;
    var state = {
      canvasId: canvasId, type: 'trend', data: data,
      progress: 0, ready: false, hover: -1, points: [],
      redraw: function () { drawTrendChart(state); },
      hitTest: function (x, y) {
        for (var i = 0; i < state.points.length; i++) {
          var p = state.points[i];
          var dx = x - p.x, dy = y - p.y;
          if (dx * dx + dy * dy <= 100) return i;
        }
        return -1;
      },
      tooltip: function (i) {
        var d = data[i];
        return '<strong>' + chartEsc(d.id) + '</strong><span>Ranking atual: <em>#' + d.rank + '</em></span><span>Score MITRE: ' + d.v + '</span>';
      },
      onClick: function (d) { filterCweFromChart(d.id); }
    };
    chartRegistry[canvasId] = state;
    bindChart(canvasId, state);
    animateChart(state, 0.025);
  }

  function drawTrendChart(state) {
    var canvas = document.getElementById(state.canvasId);
    if (!canvas) return;
    var dims = setupCanvas(canvas, 240);
    var ctx = dims.ctx, w = dims.w, h = dims.h;
    var data = state.data, n = data.length;
    var step = (w - 80) / Math.max(1, n - 1);
    state.points = [];
    ctx.clearRect(0, 0, w, h);
    ctx.strokeStyle = 'rgba(255,107,53,0.25)';
    ctx.lineWidth = 1;
    for (var g = 0; g < 5; g++) {
      var gy = 20 + g * (h - 40) / 4;
      ctx.beginPath();
      ctx.moveTo(40, gy);
      ctx.lineTo(w - 20, gy);
      ctx.stroke();
    }
    var pts = data.map(function (d, i) {
      return { x: 40 + i * step, y: 20 + (25 - d.rank) / 24 * (h - 40), i: i };
    });
    var len = Math.floor(pts.length * state.progress);
    if (len >= 2) {
      ctx.strokeStyle = '#5ce1e6';
      ctx.lineWidth = 2;
      ctx.beginPath();
      ctx.moveTo(pts[0].x, pts[0].y);
      for (var j = 1; j < len; j++) ctx.lineTo(pts[j].x, pts[j].y);
      ctx.stroke();
    }
    pts.slice(0, len).forEach(function (p, i) {
      var hot = state.hover === i;
      ctx.fillStyle = hot ? chartHotInk() : chartColors()[0];
      ctx.beginPath();
      ctx.arc(p.x, p.y, hot ? 7 : 4, 0, Math.PI * 2);
      ctx.fill();
      if (hot) { ctx.strokeStyle = chartColors()[2]; ctx.lineWidth = 2; ctx.stroke(); }
      ctx.fillStyle = hot ? chartHotInk() : chartInk(0.85);
      ctx.font = '10px JetBrains Mono';
      ctx.fillText(data[i].id.replace('CWE-', ''), p.x - 8, h - 5);
      if (state.progress >= 1) state.points.push(p);
    });
  }

  function chartLayoutReady(canvas) {
    var parent = canvas.parentElement;
    if (!parent) return true;
    if (parent.classList.contains('chart-wrap') || parent.classList.contains('chart-plot-ranked') || parent.classList.contains('chart-body-bar') || parent.classList.contains('chart-plot')) {
      return parent.getBoundingClientRect().width >= 8;
    }
    return true;
  }

  function initChart(canvasId) {
    if (chartInited[canvasId]) return;
    var canvas = document.getElementById(canvasId);
    if (!canvas) return;
    if (!chartLayoutReady(canvas)) {
      requestAnimationFrame(function () { initChart(canvasId); });
      return;
    }
    chartInited[canvasId] = true;
    if (canvasId === 'chart-cwe-scores' && CWE_CHART.length) mountHBarChart(canvasId, CWE_CHART.slice(0, 10), { color: '#e040a0', suffix: ' pts', ranked: true, cweClick: true, cweRanked: true });
    else if (canvasId === 'chart-owasp-donut' && OWASP_CHART.length) {
      var owTotal = OWASP_CHART.reduce(function (a, d) { return a + d.v; }, 0);
      mountDonutChart(canvasId, OWASP_CHART, { owaspClick: true, centerIdle: { main: String(owTotal), sub: 'correlações OWASP↔CWE' } });
    } else if (canvasId === 'chart-cwe-kev' && KEV_CHART.length) mountBarChart(canvasId, KEV_CHART, { color: '#ff6b35', height: 260, unit: ' KEV', cweClick: true, compactLabels: true });
    else if (canvasId === 'chart-owasp-prev' && PREV_CHART.length) mountHBarChart(canvasId, PREV_CHART, { color: '#5ce1e6', suffix: '%', ranked: true, owaspPrev: true });
    else if (canvasId === 'chart-breach-vectors' && BREACH_CHART.length) mountDonutChart(canvasId, BREACH_CHART, { centerIdle: { main: 'DBIR', sub: 'Vetores · 2025' } });
    else if (canvasId === 'chart-cwe-delta' && DELTA_CHART.length) mountDeltaChart(canvasId, DELTA_CHART);
  }

  function initCharts() {
    $$('.chart-embed canvas').forEach(function (c) {
      if (c.id) initChart(c.id);
    });
  }

  if ('IntersectionObserver' in window) {
    var chartObs = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        var id = entry.target.id;
        if (id) initChart(id);
        chartObs.unobserve(entry.target);
      });
    }, { rootMargin: '120px', threshold: 0.05 });
    $$('.chart-embed canvas').forEach(function (c) { chartObs.observe(c); });
  } else {
    initCharts();
  }

  var chartResizeTimer;
  window.addEventListener('resize', function () {
    clearTimeout(chartResizeTimer);
    chartResizeTimer = setTimeout(redrawAllCharts, 150);
  });
  window.addEventListener('load', function () {
    setTimeout(redrawAllCharts, 120);
  });

  // Inicializar componentes split-panel
  var firstPattern = $('.vault-item');
  if (firstPattern) showPattern(firstPattern.dataset.pattern);
  var firstTimeline = $('.timeline-node');
  if (firstTimeline) showBreach(firstTimeline, false);

  // Auto-demo terminal ativo + embeds com primeiro comando
  var activePanel = $('.term-panel.active');
  if (activePanel) {
    var demoTid = activePanel.dataset.termPanel;
    setTimeout(function () { runTerminalDemo(demoTid); }, 600);
  }
  $$('.term-embed').forEach(function (embed) {
    var tid = embed.dataset.termId;
    var lab = TERMINALS[tid];
    var out = $('#term-embed-' + tid);
    if (!lab || !out) return;
    var first = Object.keys(lab.cmds).filter(function (k) { return k !== 'help'; })[0];
    if (first) setTimeout(function () { runTerminalTo(out, tid, first); }, 300);
  });
  document.addEventListener('click', function (e) {
    var tab = e.target.closest('.term-tab');
    if (!tab) return;
    setTimeout(function () { runTerminalDemo(tab.dataset.termTab); }, 200);
  });

  if (btnTheme) {
    btnTheme.addEventListener('click', function () {
      setTimeout(function () {
        Object.keys(chartRegistry).forEach(function (id) {
          var s = chartRegistry[id];
          if (s && s.ready) {
            s.redraw();
            renderChartLegend(s);
          }
        });
      }, 100);
    });
  }

  function pinPageTop() {
    window.scrollTo(0, 0);
    if (document.documentElement) document.documentElement.scrollTop = 0;
    if (document.body) document.body.scrollTop = 0;
  }

  function initPageScroll() {
    pinPageTop();
    requestAnimationFrame(function () {
      if (pageBootActive) pinPageTop();
    });
  }
  initPageScroll();

  /*juice-ide_INJECT*/
})();