  var CWE_SIM_KINDS = [
    'c79', 'c89', 'c352', 'c862', 'c787', 'c22', 'c416', 'c125', 'c78', 'c94',
    'c120', 'c434', 'c476', 'c121', 'c502', 'c122', 'c863', 'c20', 'c284', 'c200',
    'c306', 'c918', 'c77', 'c639', 'c770'
  ];

  function cweStatus(exploited, fixed, cwe) {
    if (fixed) return { mode: exploited ? 'fixed' : 'fixed', text: '✓ CORRIGIDO · re-execute para validar', cls: 'fixed' };
    return {
      mode: exploited ? 'exploit' : 'latent',
      text: exploited ? '⚠ EXPLOITADO · ' + cwe : '⚠ VULNERÁVEL · clique Fix',
      cls: exploited ? 'danger' : 'latent'
    };
  }

  function cweMitiga(cwe, file, vuln, tips, ref) {
    return { cwe: cwe, file: file, vuln: vuln, tips: tips, ref: ref, asvs: 'MITRE ' + cwe };
  }

  var CWE_SIM_MITIGA = {
    c79: cweMitiga('CWE-79', 'routes/track-order.ts:41', 'res.send(`<div>${req.query.id}</div>`)  // sem encode HTML',
      ['Encode por contexto', 'CSP nonce', 'DOMPurify allowlist'], 'https://cwe.mitre.org/data/definitions/79.html'),
    c89: cweMitiga('CWE-89', 'routes/login.ts:34', "sequelize.query(`SELECT * FROM Users WHERE email = '${email}'...`)",
      ['Prepared statements', 'ORM sem raw SQL', 'Least privilege DB'], 'https://cwe.mitre.org/data/definitions/89.html'),
    c352: cweMitiga('CWE-352', 'routes/wallet.ts:35', "router.post('/transfer', transfer)  // sem CSRF token",
      ['Anti-CSRF token', 'SameSite=Strict', 'Origin check'], 'https://cwe.mitre.org/data/definitions/352.html'),
    c862: cweMitiga('CWE-862', 'routes/scoreBoard.ts:8', 'router.get("/api/Challenges", (req,res) => res.json(challenges))',
      ['AuthZ em todo endpoint', 'Deny-by-default', 'Role matrix tests'], 'https://cwe.mitre.org/data/definitions/862.html'),
    c787: cweMitiga('CWE-787', 'native/parser.c:88', 'memcpy(buf, input, strlen(input))  // sem checar len',
      ['memcpy_s / bounds check', 'ASAN no CI', 'Rust para parsers'], 'https://cwe.mitre.org/data/definitions/787.html'),
    c22: cweMitiga('CWE-22', 'routes/fileServer.ts:15', "const path = req.query.file  // sem canonicalize",
      ['path.resolve + prefix check', 'chroot por tenant', 'deny ..'], 'https://cwe.mitre.org/data/definitions/22.html'),
    c416: cweMitiga('CWE-416', 'native/decoder.c:52', 'free(chunk); use(chunk->data)  // dangling pointer',
      ['Smart pointers', 'ASAN UAF', 'Patch acelerado'], 'https://cwe.mitre.org/data/definitions/416.html'),
    c125: cweMitiga('CWE-125', 'native/tls.c:1024', 'memcpy(out, payload, user_len)  // len não validado',
      ['Validar length', 'Safe TLS libs', 'Sandbox parsers'], 'https://cwe.mitre.org/data/definitions/125.html'),
    c78: cweMitiga('CWE-78', 'routes/checkKeys.ts:22', "exec(`gpg --list-keys ${req.body.user}`)",
      ['spawn sem shell', 'Allowlist args', 'Sandbox'], 'https://cwe.mitre.org/data/definitions/78.html'),
    c94: cweMitiga('CWE-94', 'routes/profile.ts:18', "eval('var bio = ' + req.body.bio)  // code injection",
      ['Proibir eval', 'JSON.parse + schema', 'Logic-less templates'], 'https://cwe.mitre.org/data/definitions/94.html'),
    c120: cweMitiga('CWE-120', 'native/legacy.c:31', 'strcpy(buf, input)  // classic overflow',
      ['strncpy/snprintf', 'FORTIFY_SOURCE', 'Memory-safe rewrite'], 'https://cwe.mitre.org/data/definitions/120.html'),
    c434: cweMitiga('CWE-434', 'routes/fileUpload.ts:44', "if (file.endsWith('.pdf')) save(file)  // bypass .php.jpg",
      ['Magic bytes check', 'UUID rename', 'Fora do docroot'], 'https://cwe.mitre.org/data/definitions/434.html'),
    c476: cweMitiga('CWE-476', 'native/handler.c:67', 'process(req->ctx->data)  // ctx pode ser NULL',
      ['Null guards', 'Optional types', 'Fail-closed'], 'https://cwe.mitre.org/data/definitions/476.html'),
    c121: cweMitiga('CWE-121', 'native/stack.c:19', 'char buf[64]; gets(buf)  // stack overflow',
      ['-fstack-protector', 'ASLR+DEP', 'fgets bounded'], 'https://cwe.mitre.org/data/definitions/121.html'),
    c502: cweMitiga('CWE-502', 'routes/fileUpload.ts:72', "yaml.load(data) + vm.runInContext(...)",
      ['JSON only', 'Rejeitar YAML upload', 'ObjectInputFilter'], 'https://cwe.mitre.org/data/definitions/502.html'),
    c122: cweMitiga('CWE-122', 'native/heap.c:44', 'realloc(buf, user_size)  // heap metadata corrupt',
      ['Heap sanitizer', 'jemalloc hardening', 'Safe allocators'], 'https://cwe.mitre.org/data/definitions/122.html'),
    c863: cweMitiga('CWE-863', 'routes/feedback.ts:28', "if (req.body.role == 'admin') deleteFeedback()  // client role",
      ['Role do JWT only', 'Server-side policy', 'Unit tests role×action'], 'https://cwe.mitre.org/data/definitions/863.html'),
    c20: cweMitiga('CWE-20', 'routes/userRegistration.ts:12', 'User.create(req.body)  // sem schema validation',
      ['Zod/Pydantic schema', 'Server-side only', 'Allowlist tipos'], 'https://cwe.mitre.org/data/definitions/20.html'),
    c284: cweMitiga('CWE-284', 'routes/userProfile.ts:9', 'User.findByPk(req.params.id)  // ACL vazia',
      ['RBAC centralizado', 'mTLS service mesh', 'IAM least privilege'], 'https://cwe.mitre.org/data/definitions/284.html'),
    c200: cweMitiga('CWE-200', 'routes/accessLog.ts:8', "res.send(fs.readFileSync('logs/access.log'))",
      ['Redact tokens', 'Admin-only logs', 'Generic errors'], 'https://cwe.mitre.org/data/definitions/200.html'),
    c306: cweMitiga('CWE-306', 'routes/admin.ts:5', "router.get('/admin/...', handler)  // sem authenticate",
      ['Auth em todo /admin', 'API gateway', 'Network segmentation'], 'https://cwe.mitre.org/data/definitions/306.html'),
    c918: cweMitiga('CWE-918', 'routes/redirect.ts:11', "fetch(req.query.url)  // URL controlada pelo user",
      ['Allowlist destinos', 'Block RFC1918', 'Sem file:// gopher://'], 'https://cwe.mitre.org/data/definitions/918.html'),
    c77: cweMitiga('CWE-77', 'routes/webhook.ts:33', "spawn('sh', ['-c', 'notify ' + req.body.target])",
      ['Sem shell', 'Parameterized CLI', 'CI secret isolation'], 'https://cwe.mitre.org/data/definitions/77.html'),
    c639: cweMitiga('CWE-639', 'routes/basket.ts:19', 'BasketModel.findOne({ where: { id } })  // id do path',
      ['bid do JWT', 'UUID não sequencial', 'BOLA tests'], 'https://cwe.mitre.org/data/definitions/639.html'),
    c770: cweMitiga('CWE-770', 'routes/login.ts:8', '// sem rate limit, sem lockout, sem CAPTCHA server',
      ['Token bucket 429', 'CAPTCHA após N falhas', 'WAF rate rules'], 'https://cwe.mitre.org/data/definitions/770.html')
  };

  function cweFix(cwe, file, steps) {
    return [{ t: 'dim', x: 'IDE · ' + cwe + ' · ' + file }].concat(steps).concat([
      { t: 'ok', x: '✓ ' + cwe + ' mitigado' }
    ]);
  }

  var CWE_SIM_FIX_STEPS = {
    c79: cweFix('CWE-79', 'track-order.ts', [
      { t: 'warn', x: 'res.send com template string — XSS refletido' },
      { t: 'add', x: '+ const safe = encodeURIComponent(req.query.id)' },
      { t: 'add', x: "+ res.setHeader('Content-Security-Policy', \"default-src 'self'\")" },
      { t: 'ok', x: '→ payload renderizado como texto, não executado' }
    ]),
    c89: cweFix('CWE-89', 'login.ts', [
      { t: 'warn', x: 'SQL montada por concatenação' },
      { t: 'add', x: '+ UserModel.findOne({ where: { email, password: hash(pw) } })' },
      { t: 'http', x: "HTTP/1.1 401 — payload ' OR 1=1-- tratado literal" }
    ]),
    c352: cweFix('CWE-352', 'wallet.ts', [
      { t: 'add', x: '+ verifyCsrfToken + SameSite=Strict' },
      { t: 'http', x: 'HTTP/1.1 403 — CSRF token missing' }
    ]),
    c862: cweFix('CWE-862', 'scoreBoard.ts', [
      { t: 'add', x: "+ router.get('/api/Challenges', security.isAuthorized(['admin']), ...)" },
      { t: 'http', x: 'HTTP/1.1 403 Forbidden' }
    ]),
    c787: cweFix('CWE-787', 'parser.c', [
      { t: 'add', x: '+ if (len > sizeof(buf)) return ERROR_OVERFLOW' },
      { t: 'add', x: '+ memcpy_s(buf, sizeof(buf), input, len)' },
      { t: 'cmd', x: '$ clang -fsanitize=address parser.c && ./fuzz' }
    ]),
    c22: cweFix('CWE-22', 'fileServer.ts', [
      { t: 'add', x: '+ const safe = path.resolve(BASE, path.normalize(file))' },
      { t: 'add', x: '+ if (!safe.startsWith(BASE)) return 403' }
    ]),
    c416: cweFix('CWE-416', 'decoder.c', [
      { t: 'del', x: '- use after free path' },
      { t: 'add', x: '+ std::unique_ptr<Chunk> chunk; // RAII' },
      { t: 'cmd', x: '$ ASAN=1 ./decoder-fuzz' }
    ]),
    c125: cweFix('CWE-125', 'tls.c', [
      { t: 'add', x: '+ if (user_len > payload_len) return TLS_ALERT_DECODE_ERROR' },
      { t: 'ok', x: '→ OOB read bloqueado (Heartbleed class)' }
    ]),
    c78: cweFix('CWE-78', 'checkKeys.ts', [
      { t: 'add', x: "+ spawn('gpg', ['--list-keys', sanitize(user)])  // sem shell" }
    ]),
    c94: cweFix('CWE-94', 'profile.ts', [
      { t: 'del', x: '- eval(...)' },
      { t: 'add', x: '+ const bio = JSON.parse(req.body.bio)' }
    ]),
    c120: cweFix('CWE-120', 'legacy.c', [
      { t: 'add', x: '+ strncpy(buf, input, sizeof(buf)-1)' },
      { t: 'cmd', x: '$ gcc -D_FORTIFY_SOURCE=2 legacy.c' }
    ]),
    c434: cweFix('CWE-434', 'fileUpload.ts', [
      { t: 'add', x: '+ assertMagicBytes(file) && allowlistExt(file)' },
      { t: 'add', x: '+ storeAsUUID(file) // fora do docroot' }
    ]),
    c476: cweFix('CWE-476', 'handler.c', [
      { t: 'add', x: '+ if (!req || !req->ctx) return ERROR_INVALID' }
    ]),
    c121: cweFix('CWE-121', 'stack.c', [
      { t: 'add', x: '+ fgets(buf, sizeof(buf), stdin)' },
      { t: 'add', x: '+ __stack_chk_fail() habilitado' }
    ]),
    c502: cweFix('CWE-502', 'fileUpload.ts', [
      { t: 'del', x: '- yaml.load + vm.runInContext' },
      { t: 'add', x: '+ JSON.parse + schema validate only' }
    ]),
    c122: cweFix('CWE-122', 'heap.c', [
      { t: 'add', x: '+ size_t cap = MIN(user_size, HEAP_MAX)' },
      { t: 'cmd', x: '$ H/WASAN=1 ./heap-fuzz' }
    ]),
    c863: cweFix('CWE-863', 'feedback.ts', [
      { t: 'add', x: "+ const role = req.user.role  // do JWT, não do body" },
      { t: 'add', x: "+ if (role !== 'admin') return 403" }
    ]),
    c20: cweFix('CWE-20', 'userRegistration.ts', [
      { t: 'add', x: '+ const schema = z.object({ email: z.string().email(), qty: z.number().min(0) })' },
      { t: 'http', x: 'HTTP/1.1 400 — validation failed' }
    ]),
    c284: cweFix('CWE-284', 'userProfile.ts', [
      { t: 'add', x: '+ enforcePolicy(req.user, resource, "read")' }
    ]),
    c200: cweFix('CWE-200', 'accessLog.ts', [
      { t: 'add', x: '+ redactTokens(tailLog(100)) + isAuthorized(admin)' }
    ]),
    c306: cweFix('CWE-306', 'admin.ts', [
      { t: 'add', x: '+ security.authenticate() em router.use("/admin", ...)' },
      { t: 'http', x: 'HTTP/1.1 401 Unauthorized' }
    ]),
    c918: cweFix('CWE-918', 'redirect.ts', [
      { t: 'add', x: '+ if (!allowlistHost(url)) return 400' },
      { t: 'add', x: '+ block 169.254.0.0/16, 10.0.0.0/8' }
    ]),
    c77: cweFix('CWE-77', 'webhook.ts', [
      { t: 'add', x: "+ execFile('notify', [sanitize(target)])  // sem pipe shell" }
    ]),
    c639: cweFix('CWE-639', 'basket.ts', [
      { t: 'add', x: '+ if (parseInt(id) !== req.user.bid) return 403' }
    ]),
    c770: cweFix('CWE-770', 'login.ts', [
      { t: 'add', x: '+ rateLimit({ windowMs: 60000, max: 10 })' },
      { t: 'add', x: '+ captchaAfter(5, failures)' },
      { t: 'http', x: 'HTTP/1.1 429 Too Many Requests' }
    ])
  };

  var CWE_EVAL = {
    c79: function (v, fixed) {
      var exploited = /<|script|onerror|javascript:|iframe/i.test(v);
      var html = fixed
        ? '<span class="q">Track order: ' + escHtml(v || '') + '</span><br/><span class="ok">→ PATCH: encode + CSP · renderizado como texto</span>'
        : '<span class="q">GET /track-order?id=' + escHtml(v || '') + '</span><br/><span class="warn">→ HTML injetado sem escape</span><br/>' +
          (exploited ? '<span class="attack">→ EXPLOITADO: script executa no browser da vítima</span>' : '<span class="warn">→ Injete tag/script ou Fix</span>');
      var st = cweStatus(exploited, fixed, 'CWE-79');
      return { exploited: exploited, html: html, statusText: st.text, statusCls: st.cls };
    },
    c89: function (v, fixed) {
      var exploited = isSqliPayload(v);
      var html = fixed
        ? '<span class="ok">→ PATCH: query parametrizada · login falha com payload</span>'
        : '<span class="q">SELECT * FROM Users WHERE email = \'' + escHtml(v || '') + '\'</span><br/>' +
          (exploited ? '<span class="attack">→ EXPLOITADO: auth bypass · JWT admin</span>' : '<span class="warn">→ SQLi latente</span>');
      var st = cweStatus(exploited, fixed, 'CWE-89');
      return { exploited: exploited, html: html, statusText: st.text, statusCls: st.cls };
    },
    c352: function (v, fixed) {
      var exploited = parseInt(v, 10) > 0;
      var html = fixed
        ? '<span class="ok">→ PATCH: CSRF token · HTTP 403 cross-origin</span>'
        : '<span class="q">POST /transfer amount=' + escHtml(v || '0') + '</span><br/>' +
          (exploited ? '<span class="attack">→ EXPLOITADO: wallet drenada via form forjado</span>' : '<span class="warn">→ Valor &gt; 0 simula ataque</span>');
      var st = cweStatus(exploited, fixed, 'CWE-352');
      return { exploited: exploited, html: html, statusText: st.text, statusCls: st.cls };
    },
    c862: function (v, fixed) {
      var exploited = /challenge|admin|score|api/i.test(v);
      var html = fixed
        ? '<span class="ok">→ PATCH: isAuthorized · HTTP 403</span>'
        : '<span class="q">GET ' + escHtml(v || '/') + '</span><br/>' +
          (exploited ? '<span class="attack">→ EXPLOITADO: função admin sem checagem de permissão</span>' : '<span class="warn">→ Endpoint sensível sem authZ</span>');
      var st = cweStatus(exploited, fixed, 'CWE-862');
      return { exploited: exploited, html: html, statusText: st.text, statusCls: st.cls };
    },
    c787: function (v, fixed) {
      var exploited = v.length >= 48;
      var html = fixed
        ? '<span class="ok">→ PATCH: bounds check · memcpy_s · ASAN clean</span>'
        : '<span class="q">parser input (' + v.length + ' bytes)</span><br/><span class="warn">→ memcpy sem validar tamanho</span><br/>' +
          (exploited ? '<span class="attack">→ EXPLOITADO: OOB write · corrupção de heap</span>' : '<span class="warn">→ Envie ≥48 bytes ou Fix</span>');
      var st = cweStatus(exploited, fixed, 'CWE-787');
      return { exploited: exploited, html: html, statusText: st.text, statusCls: st.cls };
    },
    c22: function (v, fixed) {
      var exploited = /\.\.|%2e%2e|etc\/passwd/i.test(v);
      var html = fixed
        ? '<span class="ok">→ PATCH: path canonicalizado · fora de BASE → 403</span>'
        : '<span class="q">GET /ftp/' + escHtml(v || '') + '</span><br/>' +
          (exploited ? '<span class="attack">→ EXPLOITADO: leitura de arquivo fora do diretório</span>' : '<span class="warn">→ Tente ../ ou Fix</span>');
      var st = cweStatus(exploited, fixed, 'CWE-22');
      return { exploited: exploited, html: html, statusText: st.text, statusCls: st.cls };
    },
    c416: function (v, fixed) {
      var exploited = /free|reuse|0x|uaf/i.test(v);
      var html = fixed
        ? '<span class="ok">→ PATCH: RAII/smart ptr · ASAN sem UAF</span>'
        : '<span class="q">decoder: ' + escHtml(v || '') + '</span><br/>' +
          (exploited ? '<span class="attack">→ EXPLOITADO: use-after-free · RCE em código nativo</span>' : '<span class="warn">→ Padrão UAF ou Fix</span>');
      var st = cweStatus(exploited, fixed, 'CWE-416');
      return { exploited: exploited, html: html, statusText: st.text, statusCls: st.cls };
    },
    c125: function (v, fixed) {
      var exploited = parseInt(v, 10) > 1024 || v === '65535';
      var html = fixed
        ? '<span class="ok">→ PATCH: length validado · sem vazamento de memória</span>'
        : '<span class="q">TLS heartbeat len=' + escHtml(v || '0') + '</span><br/>' +
          (exploited ? '<span class="attack">→ EXPLOITADO: OOB read · 64KB memória vazada (Heartbleed-class)</span>' : '<span class="warn">→ Len &gt; 1024 ou Fix</span>');
      var st = cweStatus(exploited, fixed, 'CWE-125');
      return { exploited: exploited, html: html, statusText: st.text, statusCls: st.cls };
    },
    c78: function (v, fixed) {
      var exploited = /;|\||`|\$\(|&&|cat |id/.test(v);
      var html = fixed
        ? '<span class="ok">→ PATCH: spawn sem shell · arg sanitizado</span>'
        : '<span class="q">gpg --list-keys ' + escHtml(v || '') + '</span><br/>' +
          (exploited ? '<span class="attack">→ EXPLOITADO: comando OS injetado</span>' : '<span class="warn">→ Metachar ; | ` ou Fix</span>');
      var st = cweStatus(exploited, fixed, 'CWE-78');
      return { exploited: exploited, html: html, statusText: st.text, statusCls: st.cls };
    },
    c94: function (v, fixed) {
      var exploited = /eval|Function|require|exec|process\./i.test(v);
      var html = fixed
        ? '<span class="ok">→ PATCH: JSON.parse + schema · eval removido</span>'
        : '<span class="q">bio = ' + escHtml(v || '') + '</span><br/>' +
          (exploited ? '<span class="attack">→ EXPLOITADO: código executado no runtime Node</span>' : '<span class="warn">→ Code injection latente</span>');
      var st = cweStatus(exploited, fixed, 'CWE-94');
      return { exploited: exploited, html: html, statusText: st.text, statusCls: st.cls };
    },
    c120: function (v, fixed) {
      var exploited = v.length >= 96;
      var html = fixed
        ? '<span class="ok">→ PATCH: strncpy bounded · FORTIFY ativo</span>'
        : '<span class="q">input ' + v.length + ' bytes → strcpy(buf)</span><br/>' +
          (exploited ? '<span class="attack">→ EXPLOITADO: classic buffer overflow</span>' : '<span class="warn">→ ≥96 bytes ou Fix</span>');
      var st = cweStatus(exploited, fixed, 'CWE-120');
      return { exploited: exploited, html: html, statusText: st.text, statusCls: st.cls };
    },
    c434: function (v, fixed) {
      var exploited = /\.php|\.jsp|\.asp|\.exe/i.test(v);
      var html = fixed
        ? '<span class="ok">→ PATCH: magic bytes + UUID · extensão irrelevante</span>'
        : '<span class="q">Upload: ' + escHtml(v || '') + '</span><br/>' +
          (exploited ? '<span class="attack">→ EXPLOITADO: webshell armazenado no servidor</span>' : '<span class="warn">→ .php/.jsp bypass ou Fix</span>');
      var st = cweStatus(exploited, fixed, 'CWE-434');
      return { exploited: exploited, html: html, statusText: st.text, statusCls: st.cls };
    },
    c476: function (v, fixed) {
      var exploited = /null|nil|0x0|deref/i.test(v);
      var html = fixed
        ? '<span class="ok">→ PATCH: null guard · erro controlado</span>'
        : '<span class="q">handler(' + escHtml(v || '') + ')</span><br/>' +
          (exploited ? '<span class="attack">→ EXPLOITADO: crash/DoS por NULL deref · stack trace vazado</span>' : '<span class="warn">→ Trigger null path ou Fix</span>');
      var st = cweStatus(exploited, fixed, 'CWE-476');
      return { exploited: exploited, html: html, statusText: st.text, statusCls: st.cls };
    },
    c121: function (v, fixed) {
      var exploited = v.length >= 200;
      var html = fixed
        ? '<span class="ok">→ PATCH: fgets + stack canary</span>'
        : '<span class="q">stack buf[64] ← ' + v.length + ' bytes</span><br/>' +
          (exploited ? '<span class="attack">→ EXPLOITADO: return address sobrescrito</span>' : '<span class="warn">→ ≥200 bytes ou Fix</span>');
      var st = cweStatus(exploited, fixed, 'CWE-121');
      return { exploited: exploited, html: html, statusText: st.text, statusCls: st.cls };
    },
    c502: function (v, fixed) {
      var exploited = /!!js|yaml\.load|function\s*>|process\.env/i.test(v);
      var html = fixed
        ? '<span class="ok">→ PATCH: JSON only · deserialização insegura removida</span>'
        : '<span class="q">complaint.yml: ' + escHtml(v || '') + '</span><br/>' +
          (exploited ? '<span class="attack">→ EXPLOITADO: gadget chain · RCE via deserialize</span>' : '<span class="warn">→ YAML gadget ou Fix</span>');
      var st = cweStatus(exploited, fixed, 'CWE-502');
      return { exploited: exploited, html: html, statusText: st.text, statusCls: st.cls };
    },
    c122: function (v, fixed) {
      var exploited = v.length >= 400;
      var html = fixed
        ? '<span class="ok">→ PATCH: cap realloc · H/WASAN</span>'
        : '<span class="q">heap alloc ' + v.length + ' bytes</span><br/>' +
          (exploited ? '<span class="attack">→ EXPLOITADO: heap metadata corruption</span>' : '<span class="warn">→ ≥400 bytes ou Fix</span>');
      var st = cweStatus(exploited, fixed, 'CWE-122');
      return { exploited: exploited, html: html, statusText: st.text, statusCls: st.cls };
    },
    c863: function (v, fixed) {
      var exploited = /admin|role=|isAdmin/i.test(v);
      var html = fixed
        ? '<span class="ok">→ PATCH: role do JWT · HTTP 403 para user</span>'
        : '<span class="q">DELETE /feedback? ' + escHtml(v || '') + '</span><br/>' +
          (exploited ? '<span class="attack">→ EXPLOITADO: ação admin com role forjada no body</span>' : '<span class="warn">→ role=admin ou Fix</span>');
      var st = cweStatus(exploited, fixed, 'CWE-863');
      return { exploited: exploited, html: html, statusText: st.text, statusCls: st.cls };
    },
    c20: function (v, fixed) {
      var exploited = v.length > 0 && (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v) || v === '-1' || parseInt(v, 10) < 0);
      var html = fixed
        ? '<span class="ok">→ PATCH: Zod schema · HTTP 400 entrada inválida</span>'
        : '<span class="q">POST /register email=' + escHtml(v || '') + '</span><br/>' +
          (exploited ? '<span class="attack">→ EXPLOITADO: dado inválido aceito · logic flaw</span>' : '<span class="warn">→ Email inválido ou qty negativa</span>');
      var st = cweStatus(exploited, fixed, 'CWE-20');
      return { exploited: exploited, html: html, statusText: st.text, statusCls: st.cls };
    },
    c284: function (v, fixed) {
      var exploited = /\/user\/\d+|\/order\/\d+/i.test(v) && !/\/user\/1\b/.test(v);
      var html = fixed
        ? '<span class="ok">→ PATCH: policy engine · acesso negado cross-user</span>'
        : '<span class="q">GET ' + escHtml(v || '') + '</span><br/>' +
          (exploited ? '<span class="attack">→ EXPLOITADO: ACL vazia permite leitura alheia</span>' : '<span class="warn">→ Recurso de outro user ou Fix</span>');
      var st = cweStatus(exploited, fixed, 'CWE-284');
      return { exploited: exploited, html: html, statusText: st.text, statusCls: st.cls };
    },
    c200: function (v, fixed) {
      var exploited = /log|support|metrics|\.env/i.test(v);
      var html = fixed
        ? '<span class="ok">→ PATCH: tokens redacted · admin-only</span>'
        : '<span class="q">GET ' + escHtml(v || '') + '</span><br/>' +
          (exploited ? '<span class="attack">→ EXPLOITADO: PII/tokens expostos na resposta</span>' : '<span class="warn">→ /support/logs ou Fix</span>');
      var st = cweStatus(exploited, fixed, 'CWE-200');
      return { exploited: exploited, html: html, statusText: st.text, statusCls: st.cls };
    },
    c306: function (v, fixed) {
      var exploited = /admin|configuration|internal/i.test(v);
      var html = fixed
        ? '<span class="ok">→ PATCH: authenticate() · HTTP 401 sem token</span>'
        : '<span class="q">GET ' + escHtml(v || '') + '</span> (sem Authorization)<br/>' +
          (exploited ? '<span class="attack">→ EXPLOITADO: endpoint crítico sem autenticação</span>' : '<span class="warn">→ Path admin ou Fix</span>');
      var st = cweStatus(exploited, fixed, 'CWE-306');
      return { exploited: exploited, html: html, statusText: st.text, statusCls: st.cls };
    },
    c918: function (v, fixed) {
      var exploited = /169\.254|localhost|127\.0\.0\.1|file:\/\/|metadata/i.test(v);
      var html = fixed
        ? '<span class="ok">→ PATCH: allowlist host · RFC1918 bloqueado</span>'
        : '<span class="q">fetch("' + escHtml(v || '') + '")</span><br/>' +
          (exploited ? '<span class="attack">→ EXPLOITADO: SSRF → metadata cloud / rede interna</span>' : '<span class="warn">→ URL interna ou Fix</span>');
      var st = cweStatus(exploited, fixed, 'CWE-918');
      return { exploited: exploited, html: html, statusText: st.text, statusCls: st.cls };
    },
    c77: function (v, fixed) {
      var exploited = /\||;|&&|`|\$\(|curl|sh\b/i.test(v);
      var html = fixed
        ? '<span class="ok">→ PATCH: execFile sem shell · arg allowlist</span>'
        : '<span class="q">webhook notify ' + escHtml(v || '') + '</span><br/>' +
          (exploited ? '<span class="attack">→ EXPLOITADO: command interpreter hijacked</span>' : '<span class="warn">→ Pipe/shell metachar ou Fix</span>');
      var st = cweStatus(exploited, fixed, 'CWE-77');
      return { exploited: exploited, html: html, statusText: st.text, statusCls: st.cls };
    },
    c639: function (v, fixed) {
      var exploited = v !== '1' && v !== '';
      var html = fixed
        ? '<span class="ok">→ PATCH: bid do JWT · HTTP 403 ID alheio</span>'
        : '<span class="q">GET /rest/basket/' + escHtml(v || '1') + '</span><br/>' +
          (exploited ? '<span class="attack">→ EXPLOITADO: user key no path sem ownership</span>' : '<span class="warn">→ ID ≠ seu basket ou Fix</span>');
      var st = cweStatus(exploited, fixed, 'CWE-639');
      return { exploited: exploited, html: html, statusText: st.text, statusCls: st.cls };
    },
    c770: function (v, fixed) {
      var exploited = parseInt(v, 10) >= 10;
      var html = fixed
        ? '<span class="ok">→ PATCH: HTTP 429 após 10 req/min · CAPTCHA ativo</span>'
        : '<span class="q">POST /login × ' + escHtml(v || '0') + ' tentativas</span><br/>' +
          (exploited ? '<span class="attack">→ EXPLOITADO: brute force / credential stuffing sem limite</span>' : '<span class="warn">→ ≥10 tentativas ou Fix</span>');
      var st = cweStatus(exploited, fixed, 'CWE-770');
      return { exploited: exploited, html: html, statusText: st.text, statusCls: st.cls };
    }
  };

  function runCweSim(kind) {
    var fn = CWE_EVAL[kind];
    var out = simOutEl(kind);
    if (!fn) return;
    var r = fn(simInput(kind), !!simFixed[kind]);
    applySimResult(kind, r.exploited ? 'exploit' : 'latent', r.statusText, r.statusCls);
    if (out) out.innerHTML = r.html;
  }

  function initCweSimulators() {
    var simMap = {};
    CWE_SIM_KINDS.forEach(function (k) {
      simMap['sim-' + k] = k;
    });
    bindSimSection('simuladores-cwe', simMap, CWE_SIM_KINDS, runCweSim, CWE_SIM_MITIGA, CWE_SIM_FIX_STEPS);
  }

  initCweSimulators();