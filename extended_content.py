# Conteúdo expandido: Juice Shop, padrões, terminais, pesquisa densa

JUICE_EXTRA = {
  "feedback_xss": {
    "file": "routes/track-result.ts", "line": 18, "challenge": "DOM XSS / Reflected XSS em feedback",
    "code": "res.send(`<h1>Resultado</h1><p>Seu feedback: ${req.query.id}</p>`)  // id refletido sem encode",
    "fix": "res.json({ id: esc(req.query.id) })  // JSON API, sem HTML\n// ou: encodeURIComponent + DOMPurify no client",
    "payload": "<iframe src=\"javascript:alert(document.cookie)\">",
    "steps": ["Acesse /track-result?id=<payload>", "Observe reflexão no HTML", "Teste stored em /api/Feedbacks", "Mapeie CWE-79"]
  },
  "profile_dom": {
    "file": "routes/userProfile.ts", "line": 42, "challenge": "DOM XSS via username binding",
    "code": "res.send(`<script>var user = '${userData.username}'</script>`)  // sink em contexto JS",
    "fix": "res.json(userData)  // SPA consome JSON\n// ou JSON.stringify(userData) em script type=application/json",
    "payload": "';alert(1)//",
    "steps": ["Registre user com payload no username", "Abra perfil público", "Quebra contexto JS", "Burp DOM Invader confirma sink"]
  },
  "admin_config": {
    "file": "routes/appConfiguration.ts", "line": 12, "challenge": "Admin Section / Missing AuthZ",
    "code": "router.get('/', (req, res) => {\n  res.json({ config: req.app.get('config') })  // sem middleware isAuthorized\n})",
    "fix": "router.get('/', security.isAuthorized(['admin']), (req, res) => {\n  res.json({ config: sanitize(req.app.get('config')) })\n})",
    "payload": "GET /rest/admin/application-configuration",
    "steps": ["Sem token, chame endpoint admin", "Config interna vaza", "CWE-306 + CWE-862", "Compare com ASVS V4.1"]
  },
  "password_weak": {
    "file": "lib/insecurity.ts", "line": 18, "challenge": "Weak Password Policy",
    "code": "export const isAuthorized = () => true  // stub\n// bcrypt rounds = 1 em config de teste",
    "fix": "bcrypt.hashSync(pw, 12)\n// + zxcvbn score >= 3, breach check (HIBP k-anonymity)",
    "payload": "admin / admin123",
    "steps": ["Registre senha de 1 caractere", "Confirme hash com rounds baixos", "Credential stuffing com rockyou", "A07 + CWE-521"]
  },
  "access_log_leak": {
    "file": "routes/accessLog.ts", "line": 8, "challenge": "Access Log Exposure",
    "code": "router.get('/', (req, res) => {\n  res.send(fs.readFileSync('logs/access.log', 'utf8'))  // tokens JWT em claro\n})",
    "fix": "router.get('/', security.isAuthorized(['admin']), (req, res) => {\n  res.json(redactTokens(tailLog(100)))  // últimas 100 linhas, PII redacted\n})",
    "payload": "GET /support/logs",
    "steps": ["Login e gere tráfego autenticado", "Abra /support/logs sem admin", "Extraia Bearer tokens", "A09 + CWE-200"]
  },
  "deluxe_coupon": {
    "file": "routes/coupon.ts", "line": 25, "challenge": "Business Logic / Negative Quantity",
    "code": "if (req.body.coupon) { discount = coupons[req.body.coupon] }\n// quantity do basket aceita negativo",
    "fix": "if (!Number.isInteger(qty) || qty < 1 || qty > MAX_QTY) return res.status(400).json({error:'invalid'})",
    "payload": "quantity: -10 no PUT /api/BasketItems",
    "steps": ["Adicione item com qty negativa", "Total do basket fica negativo", "Checkout com saldo a favor", "A06 design flaw"]
  },
  "mass_assignment": {
    "file": "routes/updateUserProfile.ts", "line": 31, "challenge": "Mass Assignment / Role Escalation",
    "code": "UserModel.update(req.body, { where: { id: req.body.id } })  // role vem do client",
    "fix": "const { email, username } = req.body\nUserModel.update({ email, username }, { where: { id: user.id } })",
    "payload": '{"role":"admin","email":"x@y.z"}',
    "steps": ["Intercepte PUT /api/Users", "Injete role: admin", "Confirme privilégios elevados", "CWE-20 + A01"]
  },
  "path_ftp": {
    "file": "routes/fileServer.ts", "line": 14, "challenge": "Path Traversal /ftp",
    "code": "const file = req.params.file\nres.sendFile(path.resolve('ftp/', file))  // sem canonicalize",
    "fix": "const safe = path.basename(file)\nconst full = path.join(ftpRoot, safe)\nif (!full.startsWith(ftpRoot)) return res.status(403).end()",
    "payload": "/ftp/../../../../../../etc/passwd",
    "steps": ["Enumere /ftp", "Tente ../ encadeado", "Baixe package.json.bak", "CWE-22"]
  },
  "error_stack": {
    "file": "routes/search.ts", "line": 28, "challenge": "Verbose Error / Stack Trace",
    "code": "}).catch((err) => {\n  res.status(500).json({ error: err.stack, query: criteria })  // vaza SQL\n})",
    "fix": "}).catch((err) => {\n  logger.error({ err, criteria, userId: req.user?.id })\n  res.status(500).json({ error: 'Internal error', ref: req.id })\n})",
    "payload": "busca com ' provoca syntax error",
    "steps": ["Provoque erro SQL na busca", "Leia stack + query no JSON", "Reconstrua schema", "A10 + CWE-209"]
  },
  "ssrf_profile": {
    "file": "routes/profileImageUrlUpload.ts", "line": 22, "challenge": "SSRF via Image URL",
    "code": "const url = req.body.imageUrl\nconst buf = await download(url)  // fetch sem allowlist",
    "fix": "const u = new URL(url)\nif (!ALLOWED_HOSTS.has(u.hostname)) throw new Error('forbidden')\nif (isPrivateIP(u.hostname)) throw new Error('forbidden')",
    "payload": "http://169.254.169.254/latest/meta-data/iam/security-credentials/",
    "steps": ["POST imageUrl com metadata AWS", "Observe resposta do servidor", "Blind SSRF com Burp Collaborator", "CWE-918"]
  },
  "csrf_transfer": {
    "file": "routes/wallet.ts", "line": 35, "challenge": "CSRF em transferência",
    "code": "router.post('/transfer', (req, res) => {\n  WalletModel.transfer(req.body)  // sem anti-CSRF token\n})",
    "fix": "router.post('/transfer', verifyCsrfToken, (req, res) => {\n  WalletModel.transfer({ ...req.body, from: req.user.id })\n})",
    "payload": "<form action='http://juice/transfer' method='POST'><input name='amount' value='999'>",
    "steps": ["Capture POST autenticado", "Gere PoC HTML cross-origin", "SameSite=Lax não protege POST?", "CWE-352"]
  },
  "npm_audit": {
    "file": "package.json", "line": 1, "challenge": "Vulnerable Dependencies",
    "code": '"dependencies": {\n  "sanitize-html": "1.4.2",\n  "jsonwebtoken": "0.4.0"\n}',
    "fix": '"dependencies": {\n  "sanitize-html": "^2.13.0",\n  "jsonwebtoken": "^9.0.2"\n}\n// + npm audit ci --audit-level=high no pipeline',
    "payload": "npm audit --json | jq '.vulnerabilities'",
    "steps": ["Clone repo local", "npm audit", "Correlacione advisory com CVE", "A03 supply chain"]
  },
}

CODE_PATTERNS = [
  {"id": "py-sqli", "owasp": "A05", "cwe": "CWE-89", "lang": "Python/Flask",
   "title": "SQLi em query raw",
   "vuln": "cursor.execute(f\"SELECT * FROM users WHERE email = '{email}'\")",
   "fix": "cursor.execute('SELECT * FROM users WHERE email = %s', (email,))",
   "note": "Mesmo com ORM, .raw() e text() com f-string reintroduzem CWE-89."},
  {"id": "node-sqli", "owasp": "A05", "cwe": "CWE-89", "lang": "Node/Sequelize",
   "title": "SQLi — Juice Shop login.ts",
   "vuln": "sequelize.query(`SELECT * FROM Users WHERE email = '${email}'`)",
   "fix": "User.findOne({ where: { email, password: hash(pw) } })",
   "note": "Padrão exato do Juice Shop — concatenação em template literal."},
  {"id": "java-sqli", "owasp": "A05", "cwe": "CWE-89", "lang": "Java/JDBC",
   "title": "SQLi clássico JDBC",
   "vuln": "stmt.executeQuery(\"SELECT * FROM users WHERE id=\" + userId)",
   "fix": "PreparedStatement ps = conn.prepareStatement(\"SELECT * FROM users WHERE id=?\");\nps.setInt(1, userId);",
   "note": "MOVEit e Struts exploraram variantes similares em produção."},
  {"id": "py-cmdi", "owasp": "A05", "cwe": "CWE-78", "lang": "Python",
   "title": "OS Command Injection",
   "vuln": "os.system(f'ping -c 1 {host}')",
   "fix": "subprocess.run(['ping', '-c', '1', host], check=True)  # lista, sem shell",
   "note": "shell=True em subprocess equivale a system()."},
  {"id": "node-xss", "owasp": "A05", "cwe": "CWE-79", "lang": "Node/Express",
   "title": "Reflected XSS",
   "vuln": "res.send(`<p>Olá ${req.query.name}</p>`)",
   "fix": "res.json({ greeting: escapeHtml(req.query.name) })",
   "note": "Context matters: HTML ≠ JS ≠ URL encoding."},
  {"id": "react-xss", "owasp": "A05", "cwe": "CWE-79", "lang": "React",
   "title": "DOM XSS via dangerouslySetInnerHTML",
   "vuln": "<div dangerouslySetInnerHTML={{ __html: userBio }} />",
   "fix": "<div>{userBio}</div>  // React escapa por default\n// ou DOMPurify.sanitize(userBio)",
   "note": "Bypass de sanitização Angular [innerHTML] é vetor similar."},
  {"id": "py-idor", "owasp": "A01", "cwe": "CWE-639", "lang": "Python/FastAPI",
   "title": "IDOR em API REST",
   "vuln": "@app.get('/orders/{order_id}')\ndef get_order(order_id):\n    return db.get_order(order_id)",
   "fix": "@app.get('/orders/{order_id}')\ndef get_order(order_id, user=Depends(auth)):\n    o = db.get_order(order_id)\n    if o.user_id != user.id: raise HTTPException(403)\n    return o",
   "note": "Padrão BOLA — derive identity do token, não do path."},
  {"id": "go-authz", "owasp": "A01", "cwe": "CWE-862", "lang": "Go",
   "title": "Missing Authorization middleware",
   "vuln": "http.HandleFunc(\"/api/admin\", adminHandler)",
   "fix": "admin := http.NewServeMux()\nadmin.HandleFunc(\"/\", adminHandler)\nhttp.Handle(\"/api/admin/\", authz.RequireRole(\"admin\", admin))",
   "note": "Deny-by-default: rotas sensíveis atrás de middleware explícito."},
  {"id": "java-deser", "owasp": "A08", "cwe": "CWE-502", "lang": "Java",
   "title": "Desserialização insegura",
   "vuln": "ObjectInputStream ois = new ObjectInputStream(req.getInputStream());\nObject obj = ois.readObject();",
   "fix": "// Use JSON + schema validation\nUserDto u = mapper.readValue(req.getInputStream(), UserDto.class);\n// ou ObjectInputFilter allowlist",
   "note": "Commons Collections gadget chain — ysoserial PoC."},
  {"id": "node-deser", "owasp": "A08", "cwe": "CWE-502", "lang": "Node",
   "title": "YAML + vm — Juice Shop",
   "vuln": "vm.runInContext('JSON.stringify(yaml.load(data))', sandbox)",
   "fix": "const doc = yaml.load(data, { schema: yaml.JSON_SCHEMA, maxAliasCount: 0 })\n// sem vm, sem tipos customizados",
   "note": "yaml.load ≠ safeLoad. vm não é sandbox real."},
  {"id": "py-crypto", "owasp": "A04", "cwe": "CWE-327", "lang": "Python",
   "title": "MD5 para senha",
   "vuln": "hashlib.md5(password.encode()).hexdigest()",
   "fix": "ph.hash(password)  # Argon2 via argon2-cffi\n# verify: ph.verify(hash, password)",
   "note": "Juice Shop insecurity.ts usa MD5 — mesmo antipadrão."},
  {"id": "node-jwt", "owasp": "A04", "cwe": "CWE-347", "lang": "Node/JWT",
   "title": "JWT alg:none / sem allowlist",
   "vuln": "jwt.verify(token, publicKey)  // sem algorithms",
   "fix": "jwt.verify(token, publicKey, { algorithms: ['RS256'], issuer: 'juice-shop' })",
   "note": "Ataque alg:none troca RS256 por none."},
  {"id": "k8s-misconfig", "owasp": "A02", "cwe": "CWE-200", "lang": "Kubernetes",
   "title": "Secret em ConfigMap",
   "vuln": "apiVersion: v1\nkind: ConfigMap\ndata:\n  DB_PASSWORD: prod-secret-123",
   "fix": "kind: Secret\ntype: Opaque\n# + external-secrets operator / Vault CSI",
   "note": "15% incidentes web — misconfig (Verizon DBIR 2024)."},
  {"id": "tf-s3", "owasp": "A02", "cwe": "CWE-200", "lang": "Terraform",
   "title": "S3 bucket público",
   "vuln": "acl = \"public-read\"\nblock_public_acls = false",
   "fix": "acl = \"private\"\nblock_public_acls = true\nblock_public_policy = true",
   "note": "Accenture AWS 2017 — bucket aberto com chaves API."},
  {"id": "py-ssrf", "owasp": "A01", "cwe": "CWE-918", "lang": "Python",
   "title": "SSRF em requests.get",
   "vuln": "requests.get(user_supplied_url)",
   "fix": "parsed = urlparse(url)\nif parsed.hostname not in ALLOWED: raise ValueError()\nif ip_address(parsed.hostname).is_private: raise ValueError()",
   "note": "Capital One — SSRF → IAM role → 106M registros."},
  {"id": "node-csrf", "owasp": "A06", "cwe": "CWE-352", "lang": "Express",
   "title": "POST sem CSRF token",
   "vuln": "app.post('/transfer', (req, res) => transfer(req.body))",
   "fix": "const csrf = require('csurf')()\napp.post('/transfer', csrf, (req, res) => transfer(req.body))",
   "note": "SameSite=Strict em cookies de sessão + token synchronizer."},
  {"id": "py-rate", "owasp": "A06", "cwe": "CWE-770", "lang": "Python",
   "title": "Login sem rate limit",
   "vuln": "@app.post('/login')\ndef login(): ...  # ilimitado",
   "fix": "@limiter.limit('5/minute')\n@app.post('/login')\ndef login(): ...",
   "note": "16% breaches via credential stuffing (DBIR 2024)."},
  {"id": "java-log", "owasp": "A09", "cwe": "CWE-532", "lang": "Java",
   "title": "Log com PII/token",
   "vuln": "log.info(\"Login OK user=\" + user + \" token=\" + jwt)",
   "fix": "log.info(\"Login OK userId={}\", user.getId());  // MDC, sem token",
   "note": "Juice Shop access.log expõe Bearer tokens."},
  {"id": "py-error", "owasp": "A10", "cwe": "CWE-209", "lang": "Python",
   "title": "Stack trace ao cliente",
   "vuln": "except Exception as e:\n    return jsonify({\"error\": traceback.format_exc()})",
   "fix": "except Exception:\n    logger.exception('request failed', extra={'ref': g.request_id})\n    return jsonify({\"error\": \"internal\", \"ref\": g.request_id}), 500",
   "note": "Equifax Struts — erro verboso precedeu RCE."},
  {"id": "c-buffer", "owasp": "A10", "cwe": "CWE-787", "lang": "C",
   "title": "OOB write — strcpy",
   "vuln": "char buf[16];\nstrcpy(buf, user_input);",
   "fix": "char buf[16];\nstrncpy(buf, user_input, sizeof(buf)-1);\nbuf[sizeof(buf)-1] = '\\0';",
   "note": "12 CVEs KEV em CWE-787 — parsers nativos em APIs web."},
  {"id": "node-supply", "owasp": "A03", "cwe": "CWE-829", "lang": "Node/npm",
   "title": "Dependência não verificada — typosquat",
   "vuln": '"dependencies": {\n  "lodash": "4.17.4",\n  "event-steam": "1.0.0"\n}',
   "fix": '"dependencies": {\n  "lodash": "4.17.21"\n}\n// package-lock.json + npm audit ci + Socket.dev',
   "note": "event-stream (2018) e XZ Utils (2024) — supply chain em maintainer/dep."},
  {"id": "ci-unsigned", "owasp": "A03", "cwe": "CWE-494", "lang": "GitHub Actions",
   "title": "Artefato sem assinatura/provenance",
   "vuln": "- uses: actions/download-artifact@v4\n  with: { name: build }\n- run: ./deploy.sh dist/",
   "fix": "- uses: sigstore/gh-action-sigstore-python@v1\n- run: cosign verify-blob --certificate-oidc-issuer https://token.actions.githubusercontent.com dist/*",
   "note": "SLSA L3: provenance assinada antes do deploy. SolarWinds = update assinado comprometido."},
  {"id": "node-noauth", "owasp": "A07", "cwe": "CWE-306", "lang": "Node/Express",
   "title": "Rota admin sem autenticação",
   "vuln": "router.get('/rest/admin/application-configuration', (req, res) => {\n  res.json(req.app.get('config'))\n})",
   "fix": "router.get('/rest/admin/application-configuration',\n  security.isAuthorized(['admin']),\n  (req, res) => res.json(sanitizeConfig(req.app.get('config')))\n)",
   "note": "Juice Shop appConfiguration.ts — CWE-306 subiu +4 no MITRE 2025."},
  {"id": "py-session", "owasp": "A07", "cwe": "CWE-287", "lang": "Python/FastAPI",
   "title": "Session fixation / token fraco",
   "vuln": "session_id = request.cookies.get('sid') or uuid4()\nresponse.set_cookie('sid', session_id, httponly=False)",
   "fix": "session_id = secrets.token_urlsafe(32)\nresponse.set_cookie('sid', session_id, httponly=True, secure=True, samesite='Strict')",
   "note": "Credential stuffing 16% breaches (DBIR) — sessão deve rotacionar pós-login."},
  {"id": "go-mfa", "owasp": "A07", "cwe": "CWE-521", "lang": "Go",
   "title": "Senha fraca sem MFA",
   "vuln": "if user.Password == req.Password { issueJWT(user) }",
   "fix": "if !bcrypt.CompareHashAndPassword(user.Hash, []byte(req.Password)) { return 401 }\nif !totp.Validate(req.Code, user.MFASecret) { return 403 }\nissueJWT(user)",
   "note": "MFA FIDO2 reduz 99%+ account takeover — NIST 800-63B AAL2."},
]

TERMINAL_LABS = {
  "sqli": {"title": "SQLi — login.ts", "owasp": "A05", "cwe": "CWE-89",
    "welcome": "Lab Juice Shop · SQL Injection\nDigite help ou experimente curl/sqlmap.",
    "cmds": {
      "help": "Comandos: curl, sqlmap, cat routes/login.ts, fix",
      "cat routes/login.ts": "L34: sequelize.query(`SELECT * FROM Users WHERE email = '${email}'...`)",
      "curl -X POST http://localhost:3000/rest/user/login -H 'Content-Type: application/json' -d '{\"email\":\"'\\'' OR 1=1--\",\"password\":\"x\"}'":
        "HTTP/1.1 200 OK\n{\"authentication\":{\"token\":\"eyJhbG...\",\"bid\":1}}\n# Bypass — query retornou primeiro user",
      "sqlmap -u 'http://localhost:3000/rest/user/login' --data='{\"email\":\"*\",\"password\":\"x\"}' --dbms=sqlite --batch":
        "Parameter: email (JSON)\nType: boolean-based blind + UNION\nPayload: email=' OR 1=1--\n[INFO] DBMS: SQLite",
      "fix": "# Correção:\nUserModel.findOne({ where: { email, password: hash(pw) } })\n# + prepared statements, least privilege DB user"
    }},
  "idor": {"title": "IDOR — basket.ts", "owasp": "A01", "cwe": "CWE-639",
    "welcome": "Lab IDOR · Broken Object Level Authorization",
    "cmds": {
      "help": "Comandos: curl (com token), ffuf, fix",
      "curl -H 'Authorization: Bearer TOKEN' http://localhost:3000/rest/basket/1":
        "{\"id\":1,\"UserId\":1,\"Products\":[{\"id\":1,\"name\":\"Apple Juice\"}]}",
      "curl -H 'Authorization: Bearer TOKEN' http://localhost:3000/rest/basket/2":
        "{\"id\":2,\"UserId\":2,\"Products\":[...]}  # Carrinho de OUTRO usuário",
      "ffuf -u http://localhost:3000/rest/basket/FUZZ -H 'Authorization: Bearer TOKEN' -w ids.txt":
        "basket/1 [200] basket/2 [200] basket/3 [200]  # Todos acessíveis",
      "fix": "if (parseInt(id) !== user.bid) return res.status(403).json({ error: 'Forbidden' })"
    }},
  "xss": {"title": "XSS — busca e feedback", "owasp": "A05", "cwe": "CWE-79",
    "welcome": "Lab XSS · CWE #1 MITRE 2025 (score 60.38)",
    "cmds": {
      "help": "Comandos: curl, payload, fix, csp",
      "curl 'http://localhost:3000/rest/products/search?q=%3Cimg%20src=x%20onerror=alert(1)%3E'":
        "HTML refletido sem encode no campo de busca",
      "payload": "<img src=x onerror=alert(document.cookie)>\n<svg onload=alert(1)>",
      "fix": "res.json({ results })  // API JSON, sem HTML\n+ CSP: default-src 'self'; script-src 'nonce-{random}'",
      "csp": "Content-Security-Policy: default-src 'self'; script-src 'self' 'nonce-abc'; report-uri /csp-report"
    }},
  "jwt": {"title": "JWT — insecurity.ts", "owasp": "A04", "cwe": "CWE-347",
    "welcome": "Lab JWT · weak crypto + alg confusion",
    "cmds": {
      "help": "Comandos: decode, alg-none, fix",
      "decode eyJhbG...": "Header: {\"alg\":\"RS256\",\"typ\":\"JWT\"}\nPayload: {\"data\":{\"email\":\"user@test.com\"}}",
      "alg-none": "# Troque header para {\"alg\":\"none\"}\n# Remova assinatura\n# Servidor aceita se verify() não fixa algorithms",
      "fix": "jwt.verify(token, publicKey, { algorithms: ['RS256'], issuer: 'juice-shop' })"
    }},
  "supply": {"title": "Supply Chain — npm audit", "owasp": "A03", "cwe": "CWE-829",
    "welcome": "Lab Supply Chain · SBOM + audit",
    "cmds": {
      "help": "Comandos: npm audit, cyclonedx, slsa",
      "npm audit": "sanitize-html <2.0.0  XSS\ndottie <2.0.0  Prototype pollution\njsonwebtoken <5.0.0  JWT bypass",
      "npm audit fix --dry-run": "Would update 47 packages",
      "cyclonedx-npm --output-file sbom.json": "SBOM gerado — 312 componentes",
      "slsa": "SLSA L3: hermetic build + provenance assinada\nSigstore cosign verify artifact"
    }},
  "ssrf": {"title": "SSRF — profile image", "owasp": "A01", "cwe": "CWE-918",
    "welcome": "Lab SSRF · metadata cloud",
    "cmds": {
      "help": "Comandos: curl, metadata, fix",
      "curl -X POST http://localhost:3000/profile/imageUrl -d '{\"imageUrl\":\"http://169.254.169.254/latest/meta-data/\"}'":
        "Servidor faz fetch interno — resposta AWS metadata (se cloud)",
      "metadata": "169.254.169.254 — link-local AWS\nmetadata.google.internal — GCP",
      "fix": "Allowlist de hostnames + block private IP ranges + sem redirects"
    }},
  "auth": {"title": "Auth — login + admin", "owasp": "A07", "cwe": "CWE-306",
    "welcome": "Lab Authentication · CWE-306 Missing Auth\nClique nos comandos ou ▶ Demo.",
    "cmds": {
      "help": "Comandos: curl admin, hydra, jwt, fix",
      "curl http://localhost:3000/rest/admin/application-configuration":
        "HTTP/1.1 200 OK\n{\"config\":{\"server\":{\"port\":3000},\"security\":{\"domain\":\"juice\"}}}\n# SEM TOKEN — CWE-306",
      "hydra -l admin -P rockyou.txt localhost -s 3000 http-post-form '/rest/user/login:email=^USER^&password=^PASS^:F=Invalid'":
        "[3000][http-post-form] host: localhost   login: admin   password: admin123\n# Brute force sem rate limit",
      "curl -X POST http://localhost:3000/rest/user/login -H 'Content-Type: application/json' -d '{\"email\":\"admin@juice-sh.op\",\"password\":\"admin123\"}'":
        "HTTP/1.1 200 OK\n{\"authentication\":{\"token\":\"eyJhbGciOiJSUzI1NiIs...\",\"bid\":1,\"umail\":\"admin@juice-sh.op\"}}",
      "fix": "# 1. Auth middleware em TODA rota /admin\n# 2. MFA + rate limit 5/min no login\n# 3. bcrypt rounds >= 12\n# 4. jwt.verify(..., { algorithms: ['RS256'] })"
    }},
}

# Prevalência oficial OWASP Top 10:2025 (dados contribuídos — owasp.org)
OWASP_PREVALENCE = [
  ("A01", "Broken Access Control", "3,73%", "40 CWEs", "SSRF incorporado nesta categoria"),
  ("A02", "Security Misconfiguration", "3,00%", "16 CWEs", "Subiu de #5 (2021) para #2"),
  ("A03", "Software Supply Chain Failures", "—", "5 CWEs", "Menor incidência nos dados, maior exploit/impact score"),
  ("A04", "Cryptographic Failures", "3,80%", "32 CWEs", "Caiu de #2 para #4"),
  ("A05", "Injection", "—", "38 CWEs", "Mais CVEs associadas; XSS alta freq / SQLi alto impacto"),
  ("A06", "Insecure Design", "—", "—", "Caiu de #4 para #6"),
  ("A07", "Authentication Failures", "—", "36 CWEs", "Frameworks padronizados reduzem ocorrências"),
  ("A08", "Software/Data Integrity Failures", "—", "—", "Integridade em runtime, abaixo de supply chain"),
  ("A09", "Logging & Alerting Failures", "—", "—", "Sub-representado nos dados automatizados"),
  ("A10", "Mishandling of Exceptions", "—", "24 CWEs", "Nova categoria 2025"),
]

RESEARCH_DEEP = [
  {"id": "mitre2025", "source": "MITRE CWE TOP 25 2025", "tag": "cwe",
   "headline": "39.080 CVEs analisados — CWE-79 lidera com score 60,38",
   "stats": [("39.080", "CVE Records no dataset"), ("67%", "CVEs com CWE mapeado pelo CNA (+14pp vs 2024)"), ("28.336", "Mapeamentos CWE no Top 25"), ("71,82%", "Mappings em nível Base (actionable)")],
   "body": [
     "O CWE TOP 25 2025 reflete mapeamentos reais de CNAs — sem normalização forçada para View-1003 do NVD. Isso traz CWEs mais precisos (Base/Variant) ao ranking, explicando a entrada de buffer overflows clássicos (#11, #14, #16) e a saída de abstrações como CWE-119 e CWE-287.",
     "CWE-862 (Missing Authorization) subiu 5 posições para #4 — o maior salto. CWE-476 (NULL deref) subiu 8 posições. CWE-306 (Missing Authentication) subiu 4 posições. Isso confirma que falhas de authZ/authN dominam o ecossistema web/API.",
     "Mapeamentos para CWEs 'Discouraged' caíram de 10,19% (2024) para 5,42% (2025) — melhoria na qualidade de root cause mapping pela comunidade CVE.",
     "CWE-79 manteve #1 apesar de +3.000 CVEs adicionais mapeadas. CWE-787 caiu de #2 para #5; CWE-20 caiu 6 posições; SSRF (CWE-918) caiu para #22 mas permanece crítico em cloud."
   ],
   "actions": ["Investir em authZ server-side (CWE-862/639)", "Encoding context-aware para XSS", "Memory-safe para parsers nativos", "Exigir CWE Base/Variant em CVE disclosures"],
   "link": "https://cwe.mitre.org/top25/archive/2025/2025_key_insights.html"},
  {"id": "owasp2025", "source": "OWASP Top 10:2025", "tag": "owasp",
   "headline": "2,8 milhões de aplicações testadas — 2 categorias novas",
   "stats": [("2,8M+", "Apps no dataset"), ("248", "CWEs nas 10 categorias"), ("589", "CWEs analisados"), ("175k", "CVEs mapeados no NVD")],
   "body": [
     "8ª edição do OWASP Top Ten. Metodologia data-informed + community survey: 8 categorias vêm dos dados, 2 da pesquisa comunitária (supply chain e logging/alerting sub-representados em testes automatizados).",
     "A01 mantém #1: 3,73% das apps testadas tinham pelo menos uma das 40 CWEs de Broken Access Control. SSRF foi consolidado em A01 (saiu como categoria própria do Top 10).",
     "A03 Software Supply Chain Failures expande A06:2021 (Vulnerable Components) para pipeline, build e distribuição. Tem as menores ocorrências nos dados mas os maiores scores médios de exploit e impacto.",
     "A10 Mishandling of Exceptional Conditions é nova: 24 CWEs cobrindo error handling, fail-open, race conditions e estados inconsistentes após exceções.",
     "Contribuidores de dados: Accenture, Bugcrowd, Contrast, Semgrep, Sonar, Veracode, Orca Security e outros."
   ],
   "actions": ["Mapear 248 CWEs do Top 10 no seu stack", "Threat model para supply chain (SLSA/SBOM)", "Fail-closed em authZ e error paths"],
   "link": "https://owasp.org/Top10/2025/0x00_2025-Introduction/"},
  {"id": "dbir2024", "source": "Verizon DBIR 2024", "tag": "mercado",
   "headline": "Ataques web e credenciais continuam dominando breaches",
   "stats": [("16%", "Breaches via credential stuffing"), ("15%", "Web attacks — misconfiguration"), ("32%", "Breaches envolvendo ransomware"), ("3ª", "Posição de erros humanos como vetor")],
   "body": [
     "O DBIR 2024 analisa milhares de incidentes reais. Credential stuffing e uso de credenciais roubadas permanecem no topo — reforçando A07 e a necessidade de MFA + rate limiting.",
     "Misconfiguration em aplicações web responde por ~15% dos ataques web — alinhado com A02 subindo para #2 no OWASP 2025.",
     "O relatório destaca que vulnerabilidades exploradas (não zero-days) continuam sendo o vetor principal — patch management e hardening baseline são ROI alto.",
     "Setor financeiro: 94% dos breaches envolvem sistema web, aplicativo ou API como vetor principal."
   ],
   "actions": ["MFA obrigatório (FIDO2)", "CIS Benchmarks automatizados", "Monitoramento de credenciais vazadas (CTI)"],
   "link": "https://www.verizon.com/business/resources/reports/dbir/"},
  {"id": "ibm2024", "source": "IBM Cost of Data Breach 2024", "tag": "mercado",
   "headline": "US$ 4,88M custo médio — automação reduz US$ 1,76M",
   "stats": [("US$ 4,88M", "Custo médio global"), ("US$ 9,48M", "Custo médio EUA"), ("277 dias", "MTTI médio"), ("US$ 1,76M", "Economia com automação IR")],
   "body": [
     "Breaches com security AI/automação tiveram ciclo de vida 108 dias menor. Logging sem alerting (A09) perpetua MTTI alto.",
     "43% dos breaches envolvem terceiros — supply chain não é só dependência npm, é ecossistema inteiro.",
     "Shadow data (dados não catalogados) aparece em 35% dos breaches — correlaciona com A02 e A09."
   ],
   "actions": ["SIEM + SOAR com playbooks", "SBOM + vendor risk assessment", "Data discovery e classificação"],
   "link": "https://www.ibm.com/reports/data-breach"},
  {"id": "cisa_kev", "source": "CISA KEV Catalog 2025", "tag": "cwe",
   "headline": "Memory corruption e command injection ativamente explorados",
   "stats": [("20", "KEV em CWE-78 OS Command Injection"), ("14", "KEV em CWE-416 Use After Free"), ("12", "KEV em CWE-787 OOB Write"), ("11", "KEV em CWE-502 Deserialization")],
   "body": [
     "O catálogo KEV da CISA lista vulnerabilidades com exploit conhecido in-the-wild. CWEs de memory safety e command injection dominam — relevante mesmo em apps web com bindings nativos (imagem, PDF, Node addons).",
     "Deserialização (CWE-502) mantém 11 entradas KEV — Java, .NET e Node gadget chains continuam ativos.",
     "Priorize patch de KEV antes de hardening genérico — ROI imediato em redução de superfície explorável."
   ],
   "actions": ["Pipeline de patch KEV < 48h", "WAF rules para CVEs KEV sem patch", "Inventário de parsers nativos"],
   "link": "https://www.cisa.gov/known-exploited-vulnerabilities-catalog"},
  {"id": "portswigger", "source": "PortSwigger Web Security 2024", "tag": "owasp",
   "headline": "IDOR em 94% dos apps — SSRF crescendo em APIs",
   "stats": [("94%", "Apps com IDOR em pentest"), ("↓", "HTTP request smuggling em decline"), ("↑", "SSRF em APIs cloud-native")],
   "body": [
     "A pesquisa anual do PortSwigger confirma que Broken Access Control não é hype — é a falha mais encontrada em testes manuais, alinhado com A01 #1.",
     "SSRF migrou de categoria Top 10 para sub-item de A01, mas continua crescendo com adoção de microserviços e funções serverless que fazem fetch de URLs.",
     "Business logic flaws (preço negativo, race conditions) aparecem em ~40% dos testes — A06 Insecure Design."
   ],
   "actions": ["AuthZ matrix automatizada em CI", "Block metadata IPs em fetchers", "Abuse case testing no backlog"],
   "link": "https://portswigger.net/research"},
  {"id": "nist_ssdf", "source": "NIST SSDF 800-218", "tag": "design",
   "headline": "Corrigir em design custa fração do patch em produção",
   "stats": [("PW.1", "Design software seguro"), ("PO.3", "Revisar código"), ("RV.1", "Identificar vulnerabilidades"), ("100×", "Estimativa custo design vs prod (indústria)")],
   "body": [
     "O Secure Software Development Framework define práticas: preparar organização (PO), proteger software (PS), produzir software seguro (PW), responder a vulnerabilidades (RV).",
     "Threat modeling antes do sprint 1 (PW.1.2) e revisão de requisitos de segurança (PW.1.1) são práticas de alto impacto mapeáveis a A06.",
     "Organizações maduras integram SSDF em pipeline CI/CD com gates bloqueantes — não checklist anual."
   ],
   "actions": ["Threat Dragon no repo", "Security champions por squad", "Gates SAST/SCA bloqueantes"],
   "link": "https://csrc.nist.gov/Projects/ssdf"},
  {"id": "lgpd_gdpr", "source": "LGPD Art. 46 / GDPR Art. 32", "tag": "compliance",
   "headline": "Detecção de incidentes é obrigação legal, não opcional",
   "stats": [("Art. 46", "LGPD — segurança e boas práticas"), ("Art. 32", "GDPR — medidas técnicas adequadas"), ("72h", "Prazo notificação GDPR")],
   "body": [
     "Ambos os marcos exigem medidas técnicas para proteger dados pessoais E capacidade de detectar incidentes. Logging sem alerting (A09) é gap de compliance.",
     "ANPD orienta que exposição por misconfiguration (A02) pode exigir comunicação aos titulares se houver risco relevante.",
     "Na prática: correlacione cada OWASP com artigo LGPD/GDPR aplicável."
   ],
   "actions": ["DPIA para features com PII", "Runbook de incidente com ANPD", "Redação de PII em logs"],
   "link": "https://www.gov.br/anpd/pt-br"},
]

BREACH_TIMELINE = [
  ("2024", "XZ Utils", "Supply Chain", "Backdoor em liblzma inserido por maintainer comprometido após anos de pressão social. Detectado por engenheiro Microsoft (anomalia em sshd). Afetou distros Linux mainstream.", "A03", "CWE-829", "3 anos", "CVE-2024-3094", "https://nvd.nist.gov/vuln/detail/CVE-2024-3094"),
  ("2024", "Snowflake tenants", "Misconfig", "Campanha UNC5537: centenas de clientes Snowflake sem MFA obrigatório. Ticketmaster, Santander, Advance Auto Parts. Credenciais vazadas + session hijack.", "A02", "CWE-306", "165+", "MFA bypass", "https://www.cisa.gov/news-events/cybersecurity-advisories"),
  ("2023", "MOVEit SQLi", "Injection", "Zero-day SQLi em Progress MOVEit Transfer. Cl0p ransomware exfiltrou dados de 2.500+ organizações incluindo BBC, British Airways, Maximus.", "A05", "CWE-89", "2.500+", "CVE-2023-34362", "https://nvd.nist.gov/vuln/detail/CVE-2023-34362"),
  ("2023", "3CX Desktop", "Supply Chain", "App de telefonia assinado distribuído com malware. Supply chain via biblioteca third-party comprometida.", "A03", "CWE-494", "600k+", "Signed malware", "https://www.cisa.gov/news-events/cybersecurity-advisories"),
  ("2022", "Okta Support", "Auth", "Sistema de suporte Okta comprometido — acesso a sessões de clientes enterprise. Lapsus$ group.", "A07", "CWE-200", "—", "Support breach", "https://sec.okta.com/"),
  ("2022", "Optus API", "Access Control", "API exposta sem authZ retornou dados de 11,2M clientes australianos. Multa recorde proposta.", "A01", "CWE-862", "11,2M", "API aberta", "https://www.oaic.gov.au/"),
  ("2021", "Codecov CI", "Integrity", "Script bash uploader modificado por atacante — credenciais CI e secrets exfiltrados por meses.", "A08", "CWE-345", "29k+", "CI compromise", "https://about.codecov.io/security-update"),
  ("2021", "Microsoft Power Apps", "Misconfig", "Listas Power Apps configuradas como públicas — 38M registros (PII, COVID, dados corporativos).", "A02", "CWE-200", "38M", "Default public", "https://upguard.com/"),
  ("2020", "SolarWinds", "Supply Chain", "SUNBURST: código malicioso em update assinado Orion. 18.000+ organizações, incluindo agências US gov.", "A03", "CWE-829", "18k+", "Nation-state", "https://www.cisa.gov/news-events/cybersecurity-advisories/aa20-352a"),
  ("2019", "Capital One", "SSRF", "Ex-funcionária AWS explorou SSRF em WAF para obter credenciais IAM via metadata 169.254.169.254. 106M registros.", "A01", "CWE-918", "106M", "CVE-2019-1227", "https://www.justice.gov/usao-wdwa/pr/former-amazon-employee-convicted-hacking-capital-one-and-other-companies"),
  ("2019", "First American", "Exposure", "885M documentos financeiros acessíveis sem autenticação — ID sequencial na URL.", "A02", "CWE-200", "885M", "No auth", "https://www.krebsonsecurity.com/"),
  ("2018", "British Airways", "XSS", "Magecart: script injetado via comprometimento de third-party (payment page). 380k cartões por 15 dias.", "A05", "CWE-79", "380k", "Magecart", "https://www.ico.org.uk/"),
  ("2017", "Equifax", "Exceptions", "Apache Struts CVE-2017-5638 (OGNL injection) não patcheado por 2 meses. 147M registros US/UK/CA.", "A10", "CWE-94", "147M", "CVE-2017-5638", "https://nvd.nist.gov/vuln/detail/CVE-2017-5638"),
  ("2014", "Heartbleed", "OOB Read", "OpenSSL TLS heartbeat extension — leak de 64KB de memória por request. Chaves privadas, sessões, credenciais.", "A10", "CWE-125", "500k+", "CVE-2014-0160", "https://nvd.nist.gov/vuln/detail/CVE-2014-0160"),
]

SOURCE_LINKS = [
  ("OWASP Top 10:2025", "https://owasp.org/Top10/2025/", "Lista oficial"),
  ("MITRE CWE TOP 25 2025", "https://cwe.mitre.org/top25/archive/2025/2025_key_insights.html", "Ranking dez/2025"),
  ("Verizon DBIR 2024", "https://www.verizon.com/business/resources/reports/dbir/", "Relatório anual"),
  ("IBM Cost of Breach 2024", "https://www.ibm.com/reports/data-breach", "Custo médio"),
  ("CISA KEV Catalog", "https://www.cisa.gov/known-exploited-vulnerabilities-catalog", "Exploits ativos"),
  ("OWASP Juice Shop", "https://github.com/juice-shop/juice-shop", "Lab prático"),
  ("OWASP ASVS 4.0", "https://owasp.org/www-project-application-security-verification-standard/", "Verificação"),
  ("OWASP WSTG", "https://owasp.org/www-project-web-security-testing-guide/", "Testes"),
  ("NIST SSDF", "https://csrc.nist.gov/Projects/ssdf", "Dev seguro"),
  ("PortSwigger Research", "https://portswigger.net/research", "Tendências"),
]

MARKET_EXTRA = [
  ("2,8M+", "Apps testadas OWASP 2025", "OWASP Top 10:2025 Introduction", "https://owasp.org/Top10/2025/0x00_2025-Introduction/"),
  ("3,73%", "Apps com falha A01", "OWASP A01:2025", "https://owasp.org/Top10/2025/A01_2025-Broken_Access_Control/"),
  ("39.080", "CVEs no CWE TOP 25", "MITRE CWE TOP 25 2025", "https://cwe.mitre.org/top25/archive/2025/2025_key_insights.html"),
  ("67%", "CVEs com CNA mapping", "MITRE CWE TOP 25 2025", "https://cwe.mitre.org/top25/archive/2025/2025_key_insights.html"),
  ("94%", "Apps com IDOR em pentest", "PortSwigger Research 2024", "https://portswigger.net/research"),
  ("US$ 9,48M", "Custo breach EUA", "IBM Cost of Data Breach 2024", "https://www.ibm.com/reports/data-breach"),
  ("43%", "Breaches com terceiros", "IBM Cost of Data Breach 2024", "https://www.ibm.com/reports/data-breach"),
  ("248", "CWEs nas 10 categorias OWASP", "OWASP Top 10:2025", "https://owasp.org/Top10/2025/0x00_2025-Introduction/"),
]