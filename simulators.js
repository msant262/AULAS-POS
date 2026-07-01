  function escHtml(s) {
    return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
  }

  var SIM_KINDS = ['a01', 'a02', 'a03', 'a04', 'a05', 'a06', 'a07', 'a08', 'a09', 'a10'];
  var simFixed = {};
  var simFixTimers = {};

  function setSimStatus(id, text, cls) {
    var el = document.getElementById(id);
    if (el) { el.textContent = text; el.className = 'sim-status ' + (cls || ''); }
  }

  function setSimBox(id, state) {
    var box = document.getElementById(id);
    if (!box) return;
    box.classList.toggle('vuln', state === 'exploit');
    box.classList.toggle('latent', state === 'latent');
    box.classList.toggle('fixed', state === 'fixed');
    box.classList.remove('safe');
  }

  function simInput(kind) {
    var el = document.getElementById('sim-' + kind);
    return el ? String(el.value || '').trim() : '';
  }

  function simOutEl(kind) {
    return document.getElementById('sim-' + kind + '-out');
  }

  function isSqliPayload(s) {
    if (!String(s).trim()) return false;
    return /'(\s*(OR|or)\s+|\s*;|--)|1\s*=\s*1|UNION\s+SELECT/i.test(s);
  }

  function flashSimBox(kind) {
    var box = document.getElementById('sim-box-' + kind);
    if (!box) return;
    box.classList.remove('sim-flash');
    void box.offsetWidth;
    box.classList.add('sim-flash');
  }

  function applySimResult(kind, mode, statusText, statusCls) {
    if (simFixed[kind]) {
      setSimBox('sim-box-' + kind, 'fixed');
      return;
    }
    if (statusText) setSimStatus('sim-' + kind + '-status', statusText, statusCls);
    setSimBox('sim-box-' + kind, mode);
  }

  var SIM_MITIGA = {
    a01: {
      file: 'routes/basket.ts:19',
      vuln: 'const basket = await BasketModel.findOne({ where: { id } })\nres.json(basket)  // sem checar req.user.bid',
      tips: ['Derive identity do JWT, não do path', 'BOLA test em toda API REST', 'Matrix de roles automatizada'],
      ref: 'https://owasp.org/API-Security/editions/2023/en/0xa1-broken-object-level-authorization/',
      asvs: 'ASVS V4.1'
    },
    a02: {
      file: 'routes/appConfiguration.ts:12',
      vuln: "router.get('/', (req, res) => res.json({ config: req.app.get('config') }))  // sem isAuthorized",
      tips: ['Deny-by-default em rotas /admin', 'Segredos só via vault', 'Scanner de superfície no CI'],
      ref: 'https://owasp.org/Top10/2025/A02_2025-Security_Misconfiguration/',
      asvs: 'ASVS V14.2'
    },
    a03: {
      file: 'package.json',
      vuln: '"jsonwebtoken": "0.4.0",\n"sanitize-html": "1.4.2"  // CVEs conhecidos',
      tips: ['npm audit ci --audit-level=high', 'SBOM CycloneDX por release', 'Renovate/Dependabot com SLA'],
      ref: 'https://owasp.org/Top10/2025/A03_2025-Software_Supply_Chain_Failures/',
      asvs: 'ASVS V14.2.1'
    },
    a04: {
      file: 'lib/insecurity.ts:47',
      vuln: "export const hash = (data) => crypto.createHash('md5').update(data).digest('hex')",
      tips: ['Argon2id ou bcrypt cost ≥ 12', 'Nunca MD5/SHA1 para senhas', 'Pepper em KMS'],
      ref: 'https://owasp.org/Top10/2025/A04_2025-Cryptographic_Failures/',
      asvs: 'ASVS V2.4'
    },
    a05: {
      file: 'routes/login.ts:34',
      vuln: "sequelize.query(`SELECT * FROM Users WHERE email = '${req.body.email}' AND password = '${hash(pw)}'`)",
      tips: ['ORM/param binding exclusivo', 'Least privilege no usuário DB', 'Rate limit no login'],
      ref: 'https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html',
      asvs: 'ASVS V5.3'
    },
    a06: {
      file: 'routes/wallet.ts:35',
      vuln: "router.post('/transfer', (req, res) => WalletModel.transfer(req.body))  // sem CSRF token",
      tips: ['CSRF token em mutações', 'SameSite=Strict em cookies sensíveis', 'Re-authentication em transferências'],
      ref: 'https://owasp.org/Top10/2025/A06_2025-Insecure_Design/',
      asvs: 'ASVS V4.2'
    },
    a07: {
      file: 'lib/insecurity.ts:18',
      vuln: '// bcrypt rounds = 1 em teste\n// aceita senha de 1 caractere no registro',
      tips: ['zxcvbn score ≥ 3', 'MFA em contas sensíveis', 'HIBP k-anonymity check'],
      ref: 'https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html',
      asvs: 'ASVS V2.1'
    },
    a08: {
      file: 'routes/fileUpload.ts:72',
      vuln: "vm.runInContext('JSON.stringify(yaml.load(data))', sandbox)  // deserialização perigosa",
      tips: ['Rejeitar YAML de usuário', 'Parser sem vm/exec', 'Limite de tamanho e profundidade'],
      ref: 'https://owasp.org/Top10/2025/A08_2025-Software_or_Data_Integrity_Failures/',
      asvs: 'ASVS V8.3'
    },
    a09: {
      file: 'routes/accessLog.ts:8',
      vuln: "res.send(fs.readFileSync('logs/access.log', 'utf8'))  // JWT Bearer em claro",
      tips: ['Logs estruturados com redaction', 'Acesso admin-only aos logs', 'Nunca logar Authorization header'],
      ref: 'https://owasp.org/Top10/2025/A09_2025-Security_Logging_and_Alerting_Failures/',
      asvs: 'ASVS V7.1'
    },
    a10: {
      file: 'routes/search.ts:28',
      vuln: 'res.status(500).json({ error: err.stack, query: criteria })  // vaza stack + SQL',
      tips: ['Mensagem genérica ao cliente', 'ref/id para correlação interna', 'Logger com contexto, não com stack ao user'],
      ref: 'https://owasp.org/Top10/2025/A10_2025-Mishandling_of_Exceptional_Conditions/',
      asvs: 'ASVS V7.4'
    }
  };

  function simIdeLine(out, text, cls) {
    if (!out) return;
    var line = document.createElement('div');
    line.className = 'line ' + (cls || classifyLine(text));
    line.textContent = text;
    out.appendChild(line);
    out.scrollTop = out.scrollHeight;
  }

  function renderVulnPanel(kind, mitigaMap) {
    mitigaMap = mitigaMap || SIM_MITIGA;
    var el = document.getElementById('sim-' + kind + '-ide');
    var m = mitigaMap[kind];
    if (!el || !m || simFixed[kind]) return;
    el.innerHTML =
      '<div class="sim-vuln-idle">' +
      '<div class="sim-code-label vuln">Código vulnerável · ' + escHtml(m.file) + '</div>' +
      '<code class="sim-code-vuln">' + escHtml(m.vuln) + '</code>' +
      '<p class="sim-fix-hint">Clique <strong>Fix</strong> para abrir a IDE e corrigir passo a passo.</p>' +
      '</div>';
  }

  var SIM_FIX_STEPS = {
    a01: [
      { t: 'dim', x: 'IDE · A01 Broken Access Control · basket.ts' },
      { t: 'cmd', x: '$ code routes/basket.ts:19' },
      { t: 'warn', x: 'L19  findOne({ where: { id } }) — sem ownership check' },
      { t: 'cmd', x: '$ git checkout -b fix/idor-basket' },
      { t: 'add', x: '+ if (parseInt(id, 10) !== req.user.bid) return res.status(403).json({ error: "Forbidden" })' },
      { t: 'cmd', x: '$ curl -H "Authorization: Bearer $TOKEN" localhost:3000/rest/basket/2' },
      { t: 'http', x: 'HTTP/1.1 403 Forbidden' },
      { t: 'ok', x: '✓ IDOR mitigado · ASVS V4.1' }
    ],
    a02: [
      { t: 'dim', x: 'IDE · A02 Security Misconfiguration · appConfiguration.ts' },
      { t: 'cmd', x: '$ code routes/appConfiguration.ts' },
      { t: 'warn', x: "GET /rest/admin/application-configuration — sem isAuthorized(['admin'])" },
      { t: 'del', x: "- router.get('/', (req, res) => res.json({ config: req.app.get('config') }))" },
      { t: 'add', x: "+ router.get('/', security.isAuthorized(['admin']), (req, res) => res.json(sanitizeConfig(config)))" },
      { t: 'cmd', x: '$ curl localhost:3000/rest/admin/application-configuration' },
      { t: 'http', x: 'HTTP/1.1 401 Unauthorized' },
      { t: 'ok', x: '✓ Config admin protegida · ASVS V14.2' }
    ],
    a03: [
      { t: 'dim', x: 'IDE · A03 Supply Chain · package.json' },
      { t: 'cmd', x: '$ npm audit --json' },
      { t: 'warn', x: 'jsonwebtoken <5.0.0 — JWT bypass · sanitize-html <2.0 — XSS' },
      { t: 'cmd', x: '$ npm install jsonwebtoken@^9.0.2 sanitize-html@^2.13.0' },
      { t: 'add', x: '+ "scripts": { "audit:ci": "npm audit --audit-level=high" }' },
      { t: 'cmd', x: '$ npm audit' },
      { t: 'ok', x: 'found 0 vulnerabilities' },
      { t: 'ok', x: '✓ Supply chain endurecida · ASVS V14.2.1' }
    ],
    a04: [
      { t: 'dim', x: 'IDE · A04 Cryptographic Failures · insecurity.ts' },
      { t: 'cmd', x: '$ code lib/insecurity.ts:47' },
      { t: 'warn', x: "export const hash = (d) => crypto.createHash('md5').update(d).digest('hex')" },
      { t: 'del', x: "- crypto.createHash('md5')" },
      { t: 'add', x: '+ bcrypt.hashSync(data, 12)  // ou Argon2id' },
      { t: 'cmd', x: '$ npm test -- --grep "password hash"' },
      { t: 'ok', x: '✓ rainbow table ineficaz contra Argon2id/bcrypt' },
      { t: 'ok', x: '✓ ASVS V2.4 — storage seguro' }
    ],
    a05: [
      { t: 'dim', x: 'IDE · A05 Injection · login.ts' },
      { t: 'cmd', x: '$ code routes/login.ts:34' },
      { t: 'warn', x: "sequelize.query(`SELECT * FROM Users WHERE email = '${email}'...`)" },
      { t: 'del', x: '- sequelize.query(`SELECT * FROM Users WHERE email = ...`)' },
      { t: 'add', x: '+ UserModel.findOne({ where: { email, password: security.hash(pw), deletedAt: null } })' },
      { t: 'cmd', x: "$ curl -X POST localhost:3000/rest/user/login -d '{\"email\":\"' OR 1=1--\",\"password\":\"x\"}'" },
      { t: 'http', x: 'HTTP/1.1 401 Unauthorized' },
      { t: 'ok', x: '✓ SQLi bloqueado · ASVS V5.3' }
    ],
    a06: [
      { t: 'dim', x: 'IDE · A06 Insecure Design · wallet.ts' },
      { t: 'cmd', x: '$ code routes/wallet.ts' },
      { t: 'warn', x: "POST /transfer — sem anti-CSRF, sem re-auth" },
      { t: 'add', x: '+ router.post("/transfer", verifyCsrfToken, requireRecentAuth, transferHandler)' },
      { t: 'add', x: '+ res.cookie("csrf", token, { sameSite: "strict", httpOnly: true })' },
      { t: 'cmd', x: '$ curl -X POST localhost:3000/transfer -d "amount=999"  # sem token' },
      { t: 'http', x: 'HTTP/1.1 403 Forbidden — CSRF token missing' },
      { t: 'ok', x: '✓ CSRF mitigado · ASVS V4.2' }
    ],
    a07: [
      { t: 'dim', x: 'IDE · A07 Authentication Failures · registro' },
      { t: 'cmd', x: '$ code routes/userRegistration.ts lib/insecurity.ts' },
      { t: 'warn', x: 'Aceita senha de 1 caractere · bcrypt rounds=1' },
      { t: 'add', x: '+ const schema = z.object({ password: z.string().min(12).refine(zxcvbnScore3) })' },
      { t: 'add', x: '+ bcrypt.hashSync(pw, 12)' },
      { t: 'cmd', x: '$ curl -X POST localhost:3000/api/Users -d \'{"password":"a"}\'' },
      { t: 'http', x: 'HTTP/1.1 400 Bad Request — password policy' },
      { t: 'ok', x: '✓ Política de senha · ASVS V2.1' }
    ],
    a08: [
      { t: 'dim', x: 'IDE · A08 Data Integrity · fileUpload.ts' },
      { t: 'cmd', x: '$ code routes/fileUpload.ts:72' },
      { t: 'warn', x: 'yaml.load(data) dentro de vm.runInContext' },
      { t: 'del', x: "- vm.runInContext('JSON.stringify(yaml.load(data))', sandbox)" },
      { t: 'add', x: '+ if (!isSafeYaml(data)) return res.status(400).json({ error: "invalid" })' },
      { t: 'add', x: '+ JSON.parse(data)  // rejeitar YAML de upload externo' },
      { t: 'ok', x: '✓ Deserialização insegura removida · ASVS V8.3' }
    ],
    a09: [
      { t: 'dim', x: 'IDE · A09 Logging Failures · accessLog.ts' },
      { t: 'cmd', x: '$ code routes/accessLog.ts' },
      { t: 'warn', x: "GET /support/logs retorna access.log com Bearer tokens" },
      { t: 'del', x: "- res.send(fs.readFileSync('logs/access.log', 'utf8'))" },
      { t: 'add', x: "+ router.get('/', security.isAuthorized(['admin']), (req, res) => res.json(redactTokens(tailLog(100))))" },
      { t: 'cmd', x: '$ curl localhost:3000/support/logs' },
      { t: 'http', x: 'HTTP/1.1 401 Unauthorized' },
      { t: 'ok', x: '✓ Logs protegidos e redacted · ASVS V7.1' }
    ],
    a10: [
      { t: 'dim', x: 'IDE · A10 Exception Handling · search.ts' },
      { t: 'cmd', x: '$ code routes/search.ts:28' },
      { t: 'warn', x: 'catch: res.json({ error: err.stack, query: criteria })' },
      { t: 'del', x: '- res.status(500).json({ error: err.stack, query: criteria })' },
      { t: 'add', x: "+ logger.error({ err, criteria, reqId: req.id })" },
      { t: 'add', x: "+ res.status(500).json({ error: 'Internal error', ref: req.id })" },
      { t: 'cmd', x: "$ curl 'localhost:3000/rest/products/search?q=%27'" },
      { t: 'out', x: '{"error":"Internal error","ref":"req-8f3a2"}  // sem stack' },
      { t: 'ok', x: '✓ CWE-209 mitigado · ASVS V7.4' }
    ]
  };

  function cancelSimFix(kind) {
    if (simFixTimers[kind]) {
      simFixTimers[kind].forEach(clearTimeout);
      simFixTimers[kind] = [];
    }
  }

  function setFixBtn(kind, running, done) {
    var btn = document.querySelector('.sim-fix[data-sim="' + kind + '"]');
    if (!btn) return;
    btn.disabled = !!running;
    btn.textContent = done ? '✓ Fixed' : (running ? 'Corrigindo…' : 'Fix');
  }

  function runSimFix(kind, stepsMap) {
    stepsMap = stepsMap || SIM_FIX_STEPS;
    var steps = stepsMap[kind];
    var out = document.getElementById('sim-' + kind + '-ide');
    if (!steps || !out) return;
    cancelSimFix(kind);
    simFixed[kind] = false;
    setFixBtn(kind, true, false);
    out.innerHTML = '';
    simFixTimers[kind] = [];
    var delay = 0;
    steps.forEach(function (step, i) {
      delay += step.t === 'dim' ? 400 : (step.t === 'cmd' ? 650 : 500);
      var tid = setTimeout(function () {
        simIdeLine(out, step.x, step.t);
        if (i === steps.length - 1) {
          simFixed[kind] = true;
          setFixBtn(kind, false, true);
          setSimStatus('sim-' + kind + '-status', '✓ CORRIGIDO · re-execute para validar', 'fixed');
          setSimBox('sim-box-' + kind, 'fixed');
          runSim(kind);
        }
      }, delay);
      simFixTimers[kind].push(tid);
    });
  }

  function runSim(kind) {
    var v = simInput(kind);
    var out = simOutEl(kind);
    var fixed = !!simFixed[kind];
    var exploited = false;
    var html = '';

    if (kind === 'a01') {
      exploited = v !== '1' && v !== '';
      if (fixed) {
        html = '<span class="q">GET /rest/basket/' + escHtml(v || '1') + '</span><br/>' +
          (exploited
            ? '<span class="ok">→ PATCH: ownership check · HTTP 403</span>'
            : '<span class="ok">→ PATCH: acesso ao seu bid autorizado</span>');
      } else {
        html = '<span class="q">GET /rest/basket/' + escHtml(v || '1') + '</span><br/><span class="warn">→ basket.ts sem validar token.bid</span><br/>' +
          (exploited ? '<span class="attack">→ EXPLOITADO: JSON da cesta alheia retornado</span>' : '<span class="warn">→ Clique Fix — IDOR latente</span>');
      }
      applySimResult(kind, exploited ? 'exploit' : 'latent', exploited ? '⚠ EXPLOITADO · A01' : '⚠ VULNERÁVEL · clique Fix', exploited ? 'danger' : 'latent');
    }

    if (kind === 'a02') {
      exploited = /admin|configuration|encryptionkey/i.test(v);
      if (fixed) {
        html = '<span class="q">GET ' + escHtml(v || '/') + '</span><br/><span class="ok">→ PATCH: isAuthorized(admin) · HTTP 401</span>';
      } else {
        html = '<span class="q">GET ' + escHtml(v || '/') + '</span><br/><span class="warn">→ Endpoint admin sem middleware</span><br/>' +
          (exploited ? '<span class="attack">→ EXPLOITADO: config interna exposta em JSON</span>' : '<span class="warn">→ Teste path /admin/... ou Fix</span>');
      }
      applySimResult(kind, exploited ? 'exploit' : 'latent', exploited ? '⚠ EXPLOITADO · A02' : '⚠ VULNERÁVEL · clique Fix', exploited ? 'danger' : 'latent');
    }

    if (kind === 'a03') {
      exploited = /jsonwebtoken@0|sanitize-html@1|0\.4\.0|1\.4\.2/i.test(v) || /audit/i.test(v);
      if (fixed) {
        html = '<span class="q">$ npm audit</span><br/><span class="ok">→ PATCH: 0 vulnerabilities · SBOM no CI</span>';
      } else {
        html = '<span class="q">Pacote: ' + escHtml(v || '—') + '</span><br/><span class="warn">→ package.json com versões vulneráveis</span><br/>' +
          (exploited ? '<span class="attack">→ EXPLOITADO: CVE em ' + escHtml(v) + ' explorável em runtime</span>' : '<span class="warn">→ Informe pacote vulnerável ou Fix</span>');
      }
      applySimResult(kind, exploited ? 'exploit' : 'latent', exploited ? '⚠ EXPLOITADO · A03' : '⚠ VULNERÁVEL · clique Fix', exploited ? 'danger' : 'latent');
    }

    if (kind === 'a04') {
      exploited = v.length > 0;
      var fakeMd5 = '5f4dcc3b5aa765d61d8327deb882cf99';
      if (fixed) {
        html = '<span class="q">hash("' + escHtml(v || 'pw') + '")</span><br/><span class="ok">→ PATCH: bcrypt $2b$12$... (irreversível)</span>';
      } else {
        html = '<span class="q">MD5("' + escHtml(v || '(vazio)') + '") = ' + fakeMd5 + '</span><br/><span class="warn">→ MD5 quebrável por rainbow table</span><br/>' +
          (exploited ? '<span class="attack">→ EXPLOITADO: hash fraco armazenado no DB</span>' : '<span class="warn">→ Digite senha ou Fix</span>');
      }
      applySimResult(kind, exploited ? 'exploit' : 'latent', exploited ? '⚠ EXPLOITADO · A04' : '⚠ VULNERÁVEL · clique Fix', exploited ? 'danger' : 'latent');
    }

    if (kind === 'a05') {
      exploited = isSqliPayload(v);
      if (fixed) {
        html = '<span class="q">UserModel.findOne({ email: \'' + escHtml(v || '') + '\' })</span><br/>' +
          (exploited ? '<span class="ok">→ PATCH: payload literal · HTTP 401</span>' : '<span class="ok">→ PATCH: query parametrizada</span>');
      } else {
        html = '<span class="q">SELECT * FROM Users WHERE email = \'' + escHtml(v || '') + '\'</span><br/><span class="warn">→ login.ts concatena input</span><br/>' +
          (exploited ? '<span class="attack">→ EXPLOITADO: bypass admin · JWT emitido</span>' : '<span class="warn">→ Injete payload ou Fix</span>');
      }
      applySimResult(kind, exploited ? 'exploit' : 'latent', exploited ? '⚠ EXPLOITADO · A05' : '⚠ VULNERÁVEL · clique Fix', exploited ? 'danger' : 'latent');
    }

    if (kind === 'a06') {
      exploited = parseInt(v, 10) > 0;
      if (fixed) {
        html = '<span class="q">POST /transfer amount=' + escHtml(v || '0') + '</span><br/><span class="ok">→ PATCH: CSRF token obrigatório · HTTP 403</span>';
      } else {
        html = '<span class="q">POST /transfer { amount: ' + escHtml(v || '0') + ' }</span><br/><span class="warn">→ Sem verifyCsrfToken</span><br/>' +
          (exploited ? '<span class="attack">→ EXPLOITADO: HTML cross-origin drenaria wallet</span>' : '<span class="warn">→ Valor &gt; 0 simula CSRF · Fix</span>');
      }
      applySimResult(kind, exploited ? 'exploit' : 'latent', exploited ? '⚠ EXPLOITADO · A06' : '⚠ VULNERÁVEL · clique Fix', exploited ? 'danger' : 'latent');
    }

    if (kind === 'a07') {
      exploited = v.length > 0 && v.length < 8;
      if (fixed) {
        html = '<span class="q">Registro password="' + escHtml(v || '') + '"</span><br/><span class="ok">→ PATCH: min 12 chars + zxcvbn · HTTP 400 se fraca</span>';
      } else {
        html = '<span class="q">Registro password="' + escHtml(v || '(vazio)') + '"</span><br/><span class="warn">→ Política inexistente · bcrypt rounds=1</span><br/>' +
          (exploited ? '<span class="attack">→ EXPLOITADO: conta criada com senha trivial</span>' : '<span class="warn">→ Senha curta ou Fix</span>');
      }
      applySimResult(kind, exploited ? 'exploit' : 'latent', exploited ? '⚠ EXPLOITADO · A07' : '⚠ VULNERÁVEL · clique Fix', exploited ? 'danger' : 'latent');
    }

    if (kind === 'a08') {
      exploited = /!!js|yaml\.load|function\s*>|process\.env/i.test(v);
      if (fixed) {
        html = '<span class="q">Upload rejeitado: YAML não permitido</span><br/><span class="ok">→ PATCH: parser seguro · HTTP 400</span>';
      } else {
        html = '<span class="q">complaint.yml: ' + escHtml(v || '(vazio)') + '</span><br/><span class="warn">→ yaml.load em vm sandbox</span><br/>' +
          (exploited ? '<span class="attack">→ EXPLOITADO: RCE via deserialização</span>' : '<span class="warn">→ Payload YAML ou Fix</span>');
      }
      applySimResult(kind, exploited ? 'exploit' : 'latent', exploited ? '⚠ EXPLOITADO · A08' : '⚠ VULNERÁVEL · clique Fix', exploited ? 'danger' : 'latent');
    }

    if (kind === 'a09') {
      exploited = /log|support/i.test(v);
      if (fixed) {
        html = '<span class="q">GET ' + escHtml(v || '/') + '</span><br/><span class="ok">→ PATCH: admin-only + tokens redacted</span>';
      } else {
        html = '<span class="q">GET ' + escHtml(v || '/') + '</span><br/><span class="warn">→ access.log servido sem auth</span><br/>' +
          (exploited ? '<span class="attack">→ EXPLOITADO: Bearer eyJhbG... extraído do log</span>' : '<span class="warn">→ Path /support/logs ou Fix</span>');
      }
      applySimResult(kind, exploited ? 'exploit' : 'latent', exploited ? '⚠ EXPLOITADO · A09' : '⚠ VULNERÁVEL · clique Fix', exploited ? 'danger' : 'latent');
    }

    if (kind === 'a10') {
      exploited = /'|union|select|--/i.test(v);
      if (fixed) {
        html = '<span class="q">Busca: ' + escHtml(v || '') + '</span><br/><span class="ok">→ PATCH: {"error":"Internal error","ref":"req-…"} — sem stack</span>';
      } else {
        html = '<span class="q">Busca: ' + escHtml(v || '(vazio)') + '</span><br/><span class="warn">→ catch expõe err.stack + query SQL</span><br/>' +
          (exploited ? '<span class="attack">→ EXPLOITADO: schema DB vazado no JSON 500</span>' : '<span class="warn">→ Provoke erro SQL ou Fix</span>');
      }
      applySimResult(kind, exploited ? 'exploit' : 'latent', exploited ? '⚠ EXPLOITADO · A10' : '⚠ VULNERÁVEL · clique Fix', exploited ? 'danger' : 'latent');
    }

    if (out) out.innerHTML = html;
  }

  function bindSimSection(sectionId, simMap, kinds, runFn, mitigaMap, stepsMap) {
    var simSec = document.getElementById(sectionId);
    if (!simSec) return;

    simSec.addEventListener('click', function (e) {
      var fixBtn = e.target.closest('.sim-fix');
      if (fixBtn && !fixBtn.disabled) {
        e.preventDefault();
        e.stopPropagation();
        var fkind = fixBtn.getAttribute('data-sim');
        flashSimBox(fkind);
        runSimFix(fkind, stepsMap);
        return;
      }
      var runBtn = e.target.closest('.sim-run');
      if (runBtn) {
        e.preventDefault();
        e.stopPropagation();
        flashSimBox(runBtn.getAttribute('data-sim'));
        runFn(runBtn.getAttribute('data-sim'));
        return;
      }
      var presetBtn = e.target.closest('.sim-preset');
      if (presetBtn) {
        e.preventDefault();
        e.stopPropagation();
        var tgt = document.getElementById(presetBtn.getAttribute('data-target'));
        var val = presetBtn.getAttribute('data-val');
        if (tgt && val !== null) {
          tgt.value = val;
          var box = presetBtn.closest('.sim-box');
          var kind = box && box.id ? box.id.replace('sim-box-', '') : '';
          flashSimBox(kind);
          runFn(kind);
        }
      }
    });

    Object.keys(simMap).forEach(function (id) {
      var el = document.getElementById(id);
      if (el) el.addEventListener('input', function () {
        flashSimBox(simMap[id]);
        runFn(simMap[id]);
      });
    });

    kinds.forEach(function (k) {
      renderVulnPanel(k, mitigaMap);
      runFn(k);
    });
  }

  function initSimulators() {
    var simMap = {
      'sim-a01': 'a01', 'sim-a02': 'a02', 'sim-a03': 'a03', 'sim-a04': 'a04', 'sim-a05': 'a05',
      'sim-a06': 'a06', 'sim-a07': 'a07', 'sim-a08': 'a08', 'sim-a09': 'a09', 'sim-a10': 'a10'
    };
    bindSimSection('simuladores', simMap, SIM_KINDS, runSim);
  }

  initSimulators();