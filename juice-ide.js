(function () {
  'use strict';

  function parseJSONJuice(id, fallback) {
    var el = document.getElementById(id);
    if (!el) return fallback;
    try { return JSON.parse(el.textContent); } catch (e) {
      console.error('[juice-ide] JSON inválido em #' + id + ':', e);
      return fallback;
    }
  }

  var JUICE_IDE = parseJSONJuice('data-juice-ide', []);
  var shell = document.getElementById('juice-ide');
  if (!shell || !JUICE_IDE.length) return;

  var treeEl = document.getElementById('juice-ide-tree');
  var tabEl = document.getElementById('juice-ide-tabs');
  var vulnEl = document.getElementById('juice-ide-vuln');
  var fixEl = document.getElementById('juice-ide-fix');
  var vulnPanel = vulnEl && vulnEl.closest('.ide-split-code');
  var fixPanel = fixEl && fixEl.closest('.ide-split-code');
  var metaEl = document.getElementById('juice-ide-meta');
  var termOut = document.getElementById('juice-ide-term');
  var statusEl = document.getElementById('juice-ide-status');
  var fnameEl = document.getElementById('juice-ide-fname');
  var lineEl = document.getElementById('juice-ide-line-badge');
  var vulnLabel = document.getElementById('juice-ide-vuln-label');
  var fixHint = document.getElementById('juice-ide-fix-hint');
  var syncCb = document.getElementById('juice-ide-sync');

  var activeId = null;
  var fixApplied = {};
  var animTimers = [];
  var typing = false;
  var syncing = false;

  function esc(s) {
    return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
  }

  function labById(id) {
    for (var i = 0; i < JUICE_IDE.length; i++) {
      if (JUICE_IDE[i].id === id) return JUICE_IDE[i];
    }
    return null;
  }

  function cancelAnim() {
    animTimers.forEach(clearTimeout);
    animTimers = [];
    typing = false;
  }

  function termLine(text, cls) {
    if (!termOut) return;
    var line = document.createElement('div');
    line.className = 'line ' + (cls || 'out');
    line.textContent = text;
    termOut.appendChild(line);
    termOut.scrollTop = termOut.scrollHeight;
  }

  function clearTerm() {
    if (termOut) termOut.innerHTML = '';
  }

  function focusRange(lab) {
    var start = lab.focus_start || lab.line || 1;
    var end = lab.focus_end || start;
    return { start: start, end: end };
  }

  function renderCode(target, code, opts) {
    opts = opts || {};
    if (!target) return;
    var lines = String(code || '').split('\n');
    var focus = opts.focus;
    var mode = opts.mode || 'vuln';
    var showCursor = opts.showCursor;
    var html = '';

    if (!lines.length || (lines.length === 1 && !lines[0])) {
      target.innerHTML = '<span class="ide-placeholder">Clique em <strong>Aplicar correção</strong> para digitar o patch aqui…</span>';
      return;
    }

    lines.forEach(function (ln, i) {
      var n = i + 1;
      var isFocus = focus && n >= focus.start && n <= focus.end;
      var cls = 'ide-row';
      if (isFocus) cls += mode === 'fix' ? ' focus-fix' : ' focus-vuln';
      if (showCursor && i === lines.length - 1) cls += ' typing';
      html += '<span class="' + cls + '"><span class="ide-ln">' + String(n).padStart(3, ' ') + '</span><span class="ide-lc">' + esc(ln) + '</span></span>';
    });
    target.innerHTML = html;
  }

  function setFixHint(state) {
    if (!fixHint) return;
    fixHint.className = 'ide-split-hint' + (state === 'typing' ? ' typing' : state === 'done' ? ' done' : '');
    if (state === 'typing') fixHint.textContent = 'digitando patch…';
    else if (state === 'done') fixHint.textContent = '✓ correção aplicada';
    else fixHint.textContent = '— aplique o patch';
  }

  function setStatus(mode) {
    if (!statusEl) return;
    statusEl.className = 'juice-ide-status ' + mode;
    if (mode === 'vuln') statusEl.textContent = '● Vulnerável';
    else if (mode === 'fix') statusEl.textContent = '● Corrigido';
    else if (mode === 'applying') statusEl.textContent = '◌ Aplicando patch…';
    else statusEl.textContent = '● Pronto';
  }

  function renderMeta(lab) {
    if (!metaEl || !lab) return;
    var payload = lab.payload && lab.payload !== 'N/A'
      ? '<p class="juice-ide-payload">Payload: <code>' + esc(lab.payload) + '</code></p>' : '';
    var steps = (lab.steps || []).map(function (s) { return '<li>' + esc(s) + '</li>'; }).join('');
    metaEl.innerHTML =
      '<div class="juice-ide-meta-grid">' +
      '<span class="ok-badge accent pill">' + esc(lab.owasp || 'OWASP') + '</span>' +
      '<span class="ok-badge pill">' + esc(lab.challenge) + '</span>' +
      payload +
      '<ol class="juice-ide-steps">' + steps + '</ol></div>';
  }

  function scrollToFocus(panel, focusStart) {
    if (!panel) return;
    var row = panel.querySelector('.ide-row.focus-vuln, .ide-row.focus-fix');
    if (!row) {
      var rows = panel.querySelectorAll('.ide-row');
      if (rows[focusStart - 1]) row = rows[focusStart - 1];
    }
    if (!row) return;
    var top = row.offsetTop - (panel.clientHeight - row.offsetHeight) / 2;
    panel.scrollTop = Math.max(0, top);
  }

  function showVuln(lab) {
    var focus = focusRange(lab);
    renderCode(vulnEl, lab.code, { focus: focus, mode: 'vuln' });
    if (vulnLabel) vulnLabel.textContent = lab.file;
    setTimeout(function () { scrollToFocus(vulnPanel, focus.start); }, 50);
  }

  function showFixPlaceholder() {
    renderCode(fixEl, '');
    setFixHint('');
  }

  function showFixInstant(lab) {
    var focus = focusRange(lab);
    renderCode(fixEl, lab.fix, { focus: focus, mode: 'fix' });
    setFixHint('done');
    setTimeout(function () { scrollToFocus(fixPanel, focus.start); }, 50);
  }

  function typewriterFix(lab, onDone) {
    cancelAnim();
    typing = true;
    setFixHint('typing');
    var focus = focusRange(lab);
    var lines = String(lab.fix).split('\n');
    var built = [];
    var lineIdx = 0;
    var charIdx = 0;

    function renderPartial() {
      var text = built.join('\n');
      if (lineIdx < lines.length && charIdx > 0) {
        text += (built.length ? '\n' : '') + lines[lineIdx].slice(0, charIdx);
      }
      renderCode(fixEl, text, {
        focus: focus,
        mode: 'fix',
        showCursor: true
      });
      if (fixPanel && syncCb && syncCb.checked && vulnPanel) {
        syncing = true;
        fixPanel.scrollTop = vulnPanel.scrollTop;
        syncing = false;
      }
    }

    function nextChar() {
      if (lineIdx >= lines.length) {
        typing = false;
        renderCode(fixEl, lab.fix, { focus: focus, mode: 'fix' });
        setFixHint('done');
        if (onDone) onDone();
        return;
      }
      var line = lines[lineIdx];
      if (charIdx < line.length) {
        charIdx++;
        renderPartial();
        var delay = line.charAt(charIdx - 1) === ' ' ? 8 : (14 + Math.floor(Math.random() * 10));
        animTimers.push(setTimeout(nextChar, delay));
      } else {
        built.push(line);
        lineIdx++;
        charIdx = 0;
        renderPartial();
        animTimers.push(setTimeout(nextChar, lineIdx >= lines.length ? 120 : 60));
      }
    }

    renderCode(fixEl, '', { focus: focus, mode: 'fix', showCursor: true });
    animTimers.push(setTimeout(nextChar, 200));
  }

  function bindSyncScroll() {
    if (!vulnPanel || !fixPanel || !syncCb) return;
    vulnPanel.addEventListener('scroll', function () {
      if (!syncCb.checked || syncing || typing) return;
      syncing = true;
      fixPanel.scrollTop = vulnPanel.scrollTop;
      syncing = false;
    });
    fixPanel.addEventListener('scroll', function () {
      if (!syncCb.checked || syncing || typing) return;
      syncing = true;
      vulnPanel.scrollTop = fixPanel.scrollTop;
      syncing = false;
    });
  }

  function openLab(id) {
    var lab = labById(id);
    if (!lab) return;
    activeId = id;
    cancelAnim();
    showVuln(lab);
    if (fixApplied[id]) showFixInstant(lab);
    else showFixPlaceholder();
    if (fnameEl) fnameEl.textContent = lab.file;
    if (lineEl) lineEl.textContent = 'L' + (lab.focus_start || lab.line);
    var gh = document.getElementById('juice-ide-github');
    if (gh) gh.href = 'https://github.com/juice-shop/juice-shop/blob/master/' + lab.file + '#L' + (lab.focus_start || lab.line);
    renderMeta(lab);
    setStatus(fixApplied[id] ? 'fix' : 'vuln');
    treeEl.querySelectorAll('.ide-tree-file').forEach(function (btn) {
      btn.classList.toggle('active', btn.getAttribute('data-juice-id') === id);
    });
    if (tabEl) {
      tabEl.innerHTML = '<button type="button" class="ide-tab active"><span class="ide-tab-icon">◆</span>' +
        esc(lab.file.split('/').pop()) + '<span class="ide-tab-sub"> · ' + esc(lab.challenge.slice(0, 28)) + '</span></button>';
    }
    clearTerm();
    termLine('Juice Shop IDE — ' + lab.file + ':' + (lab.focus_start || lab.line), 'dim');
    termLine('Vulnerável à esquerda · correção digitada à direita ao aplicar patch.', 'dim');
  }

  function buildTree() {
    var folders = {};
    JUICE_IDE.forEach(function (lab) {
      var parts = lab.file.split('/');
      var dir = parts.length > 1 ? parts.slice(0, -1).join('/') : '';
      var fname = parts[parts.length - 1];
      if (!folders[dir]) folders[dir] = [];
      folders[dir].push({ lab: lab, fname: fname });
    });
    var dirs = Object.keys(folders).sort();
    var html = '';
    dirs.forEach(function (dir) {
      var label = dir || 'root';
      html += '<div class="ide-tree-folder open" data-folder="' + esc(dir) + '">';
      html += '<button type="button" class="ide-tree-dir" aria-expanded="true"><span class="ide-chevron">▼</span> ' + esc(label) + '</button>';
      html += '<div class="ide-tree-children">';
      folders[dir].forEach(function (item) {
        var hot = item.lab.id === activeId ? ' active' : '';
        var fixed = fixApplied[item.lab.id] ? ' fixed' : '';
        html += '<button type="button" class="ide-tree-file' + hot + fixed + '" data-juice-id="' + esc(item.lab.id) + '">' +
          '<span class="ide-file-ico">TS</span>' + esc(item.fname) +
          '<span class="ide-file-rank">#' + (item.lab.focus_start || item.lab.line) + '</span></button>';
      });
      html += '</div></div>';
    });
    treeEl.innerHTML = html;
  }

  function runSteps(steps, onDone, opts) {
    opts = opts || {};
    cancelAnim();
    if (!opts.noClear) clearTerm();
    var delay = opts.initialDelay || 0;
    steps.forEach(function (step, i) {
      delay += step.t === 'cmd' ? 700 : (step.t === 'dim' ? 350 : 480);
      animTimers.push(setTimeout(function () {
        termLine(step.x, step.t === 'add' ? 'add' : (step.t === 'del' ? 'del' : step.t));
        if (i === steps.length - 1 && onDone) onDone();
      }, delay));
    });
  }

  function applyFix() {
    if (!activeId || typing) return;
    var lab = labById(activeId);
    if (!lab) return;
    setStatus('applying');
    showFixPlaceholder();
    typewriterFix(lab, function () {
      fixApplied[activeId] = true;
      setStatus('fix');
      buildTree();
      clearTerm();
      termLine('Patch digitado — executando validação local…', 'dim');
      runSteps(lab.apply || [], function () {
        setStatus('fix');
      }, { noClear: true, initialDelay: 400 });
    });
  }

  function validateFix() {
    if (!activeId || typing) return;
    var lab = labById(activeId);
    if (!lab || !lab.validate) return;
    var script = fixApplied[activeId] ? lab.validate.fix : lab.validate.vuln;
    setStatus('applying');
    runSteps(script, function () {
      setStatus(fixApplied[activeId] ? 'fix' : 'vuln');
    });
  }

  treeEl.addEventListener('click', function (e) {
    var dirBtn = e.target.closest('.ide-tree-dir');
    if (dirBtn) {
      var folder = dirBtn.closest('.ide-tree-folder');
      if (folder) {
        folder.classList.toggle('open');
        dirBtn.setAttribute('aria-expanded', folder.classList.contains('open'));
        var ch = dirBtn.querySelector('.ide-chevron');
        if (ch) ch.textContent = folder.classList.contains('open') ? '▼' : '▶';
      }
      return;
    }
    var fileBtn = e.target.closest('.ide-tree-file');
    if (fileBtn) openLab(fileBtn.getAttribute('data-juice-id'));
  });

  document.getElementById('juice-ide-apply')?.addEventListener('click', applyFix);
  document.getElementById('juice-ide-validate')?.addEventListener('click', validateFix);
  document.getElementById('juice-ide-show-vuln')?.addEventListener('click', function () {
    if (!activeId) return;
    var lab = labById(activeId);
    if (!lab) return;
    cancelAnim();
    fixApplied[activeId] = false;
    showFixPlaceholder();
    setStatus('vuln');
    buildTree();
  });
  document.getElementById('juice-ide-show-fix')?.addEventListener('click', function () {
    if (!activeId || typing) return;
    var lab = labById(activeId);
    if (!lab) return;
    cancelAnim();
    fixApplied[activeId] = true;
    showFixInstant(lab);
    setStatus('fix');
    buildTree();
  });

  document.addEventListener('click', function (e) {
    var link = e.target.closest('[data-juice-ide]');
    if (!link) return;
    var id = link.getAttribute('data-juice-ide');
    if (!id) return;
    e.preventDefault();
    openLab(id);
    shell.scrollIntoView({ behavior: 'smooth', block: 'start' });
  });

  bindSyncScroll();
  buildTree();

  var ideBooted = false;
  function bootIde() {
    if (ideBooted) return;
    ideBooted = true;
    openLab(JUICE_IDE[0].id);
  }

  if ('IntersectionObserver' in window) {
    var ideObs = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) {
          bootIde();
          ideObs.disconnect();
        }
      });
    }, { rootMargin: '120px', threshold: 0.01 });
    ideObs.observe(shell);
  }
})();