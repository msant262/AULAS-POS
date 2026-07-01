#!/usr/bin/env python3
"""Gera aula-owasp-cwe.html — arquivo único autocontido."""
import json, html, pathlib

ROOT = pathlib.Path(__file__).parent
OKAMI = (ROOT / "okami.css").read_text()
PATTERNS = (ROOT / "okami-patterns.css").read_text()

OWASP = [
    {"id":"A01","title":"Broken Access Control","pt":"Controle de Acesso Quebrado",
     "sum":"Falhas de autorização continuam no topo do ranking OWASP 2025. O problema não é autenticação: é a ausência de checagem server-side em cada operação sensível. IDOR, escalação horizontal e vertical, e bypass de rotas administrativas aparecem em 94% dos apps testados (OWASP Testing Guide, 2024).",
     "cwes":["CWE-862","CWE-863","CWE-639","CWE-284","CWE-22"],
     "cases":[("Optus (Austrália, 2022)","11,2M clientes expostos por API sem autorização"),("Capital One (2019)","106M registros via SSRF + metadata AWS")],
     "juice":{"name":"View Basket of another User","diff":"★★☆","route":"GET /rest/basket/{id}","code":"// routes/basket.ts — sem checagem de ownership\nBasketModel.find({id: req.params.id})","hint":"Troque o ID no DevTools e observe o carrinho alheio."},
     "prev":["Enforce deny-by-default em cada endpoint","Testes de autorização por role (BOLA/BFLA)","Mapa de superfície com path enumeration","Logs de tentativas de acesso negado"],
     "refs":[("OWASP A01:2025","https://owasp.org/Top10/2025/A01_2025-Broken_Access_Control/"),("CWE-862","https://cwe.mitre.org/data/definitions/862.html"),("Verizon DBIR 2024","https://www.verizon.com/business/resources/reports/dbir/")]},
    {"id":"A02","title":"Security Misconfiguration","pt":"Configuração Insegura",
     "sum":"Headers ausentes, CORS permissivo, diretórios listáveis e credenciais default em produção. O Verizon DBIR 2024 aponta misconfiguration como vetor em 15% dos incidentes web. Cloud buckets públicos e painéis de debug expostos seguem recorrentes.",
     "cwes":["CWE-16","CWE-200","CWE-1188"],
     "cases":[("Microsoft Power Apps, 2021","38M registros por listas configuradas como públicas"),("Accenture, 2017","Servidor AWS sem autenticação com chaves API")],
     "juice":{"name":"Misplaced Signature File","diff":"★☆☆","route":"/ftp/suspicious.pcap","code":"// server.ts — express.static sem restrição\napp.use('/ftp', express.static('ftp/'))","hint":"Enumere /ftp e /encryptionkeys após o scan de diretórios."},
     "prev":["Hardening checklist por ambiente (dev/stage/prod)","CSP, HSTS, X-Frame-Options via pipeline","Scanner de config (Prowler, ScoutSuite)","Remover features de debug antes do deploy"],
     "refs":[("OWASP A02:2025","https://owasp.org/Top10/2025/A02_2025-Security_Misconfiguration/"),("CIS Benchmarks","https://www.cisecurity.org/cis-benchmarks")]},
    {"id":"A03","title":"Software Supply Chain Failures","pt":"Falhas na Cadeia de Suprimentos",
     "sum":"Nova categoria em 2025. Cobre dependências comprometidas, typosquatting, build pipelines adulterados e SBOM incompletos. O ataque SolarWinds (2020) e o incidente XZ Utils (2024) mostram que um único pacote malicioso afeta milhões de deploys.",
     "cwes":["CWE-829","CWE-494","CWE-502"],
     "cases":[("SolarWinds SUNBURST, 2020","18.000+ organizações via update assinado"),("3CX supply chain, 2023","App desktop comprometido distribuído oficialmente")],
     "juice":{"name":"Vulnerable Library","diff":"★★☆","route":"/package.json","code":"\"dependencies\": {\n  \"sanitize-html\": \"1.4.2\"  // CVE conhecida\n}","hint":"Compare versões do package.json com advisory do npm."},
     "prev":["SBOM + assinatura de artefatos (Sigstore, SLSA L3+)","Pin de versões e renovate com advisory review","Dependency-Track / OSV-Scanner no CI","Verificação de integridade de releases upstream"],
     "refs":[("OWASP A03:2025","https://owasp.org/Top10/2025/A03_2025-Software_Supply_Chain_Failures/"),("SLSA","https://slsa.dev/")]},
    {"id":"A04","title":"Cryptographic Failures","pt":"Falhas Criptográficas",
     "sum":"Dados sensíveis trafegam ou repousam sem proteção adequada: TLS legado, hashing MD5/SHA1 para senhas, chaves hardcoded. IBM Cost of a Data Breach 2024: custo médio global de US$ 4,88M por incidente com exposição de PII.",
     "cwes":["CWE-327","CWE-328","CWE-798","CWE-311"],
     "cases":[("Equifax, 2017","147M registros; certificado TLS expirado facilitou exploração"),("RockYou2024 leak","10B+ senhas em texto claro agregadas")],
     "juice":{"name":"Access Log","diff":"★☆☆","route":"/support/logs","code":"// access.log em texto claro\nGET /rest/user/1 HTTP/1.1 Authorization: Bearer eyJhbG...","hint":"Leia o access.log e extraia tokens JWT."},
     "prev":["TLS 1.3 + HSTS obrigatório","Argon2id/bcrypt com salt por registro","KMS/HSM para chaves; rotação automatizada","Classificação de dados e criptografia em repouso"],
     "refs":[("OWASP A04:2025","https://owasp.org/Top10/2025/A04_2025-Cryptographic_Failures/"),("NIST SP 800-57","https://csrc.nist.gov/publications/detail/sp/800-57-part-1/rev-5/final")]},
    {"id":"A05","title":"Injection","pt":"Injeção",
     "sum":"SQLi, XSS, command injection e LDAP injection persistem porque entrada do usuário vira parte de comandos interpretados. CWE-79 lidera o TOP 25 MITRE 2025 com score 60,38. Prepared statements e output encoding fecham a maioria dos vetores.",
     "cwes":["CWE-79","CWE-89","CWE-78","CWE-94","CWE-77"],
     "cases":[("MOVEit SQLi, 2023","Cl0p explorou zero-day; 2.500+ organizações"),("British Airways Magecart, 2018","380.000 cartões via XSS supply chain")],
     "juice":{"name":"Login Admin","diff":"★★☆","route":"POST /rest/user/login","code":"`SELECT * FROM Users WHERE email='${email}' AND password='${hash}'`","hint":"Payload: ' OR 1=1-- no campo email."},
     "prev":["Parameterized queries / ORM seguro","Context-aware output encoding (OWASP XSS Prevention)","Shell=false em Runtime.exec","SAST + DAST no pipeline"],
     "refs":[("OWASP A05:2025","https://owasp.org/Top10/2025/A05_2025-Injection/"),("OWASP SQLi Cheat Sheet","https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html")]},
    {"id":"A06","title":"Insecure Design","pt":"Design Inseguro",
     "sum":"Defeitos arquiteturais que nenhum patch corrige: fluxos sem rate limit, recuperação de senha previsível, lógica de negócio explorável. Threat modeling no design phase reduz custo de correção em até 100× versus produção (NIST SSDF).",
     "cwes":["CWE-840","CWE-770","CWE-352","CWE-20"],
     "cases":[("Uber breach, 2016","57M usuários; credenciais AWS em repositório Git"),("Twitter 2020","Social engineering + design fraco de admin tools")],
     "juice":{"name":"CAPTCHA Bypass","diff":"★★☆","route":"/rest/user/registration","code":"// CAPTCHA validado só no client\nif (req.body.captchaId) { register(user) }","hint":"Reenvie o POST sem resolver o CAPTCHA."},
     "prev":["Threat modeling (STRIDE/PASTA) no design","Abuse cases documentados por feature","Rate limiting e anti-automation","Security user stories no backlog"],
     "refs":[("OWASP A06:2025","https://owasp.org/Top10/2025/A06_2025-Insecure_Design/"),("OWASP Threat Dragon","https://owasp.org/www-project-threat-dragon/")]},
    {"id":"A07","title":"Authentication Failures","pt":"Falhas de Autenticação",
     "sum":"Senhas fracas, MFA ausente, session fixation e JWT mal implementado. CWE-306 (Missing Authentication) subiu 4 posições no TOP 25 2025. Ataques de credential stuffing representam 16% dos breaches analisados pelo Verizon DBIR.",
     "cwes":["CWE-306","CWE-287","CWE-384","CWE-521"],
     "cases":[("Okta support breach, 2023","Sessões de suporte comprometidas"),("LastPass, 2022","Vault keys derivadas de senha master fraca")],
     "juice":{"name":"Password Strength","diff":"★☆☆","route":"/rest/user/change-password","code":"// bcrypt rounds = 1 (intencionalmente fraco)\nbcrypt.hash(password, 1)","hint":"Registre conta e observe tempo de hash no response."},
     "prev":["MFA obrigatório para contas privilegiadas","Session rotation pós-login","Bloqueio progressivo + detecção de stuffing","OAuth2/OIDC com PKCE"],
     "refs":[("OWASP A07:2025","https://owasp.org/Top10/2025/A07_2025-Authentication_Failures/"),("OWASP ASVS V2","https://owasp.org/www-project-application-security-verification-standard/")]},
    {"id":"A08","title":"Software or Data Integrity Failures","pt":"Falhas de Integridade",
     "sum":"Updates sem verificação, desserialização insegura e CI/CD sem proteção. CWE-502 (deserialization) tem 11 CVEs no KEV catalog. Inclui também integridade de dados em trânsito entre microsserviços.",
     "cwes":["CWE-502","CWE-345","CWE-829"],
     "cases":[("Codecov bash uploader, 2021","Script de CI comprometido exfiltrou secrets"),("Atlassian Confluence OGNL, 2022","RCE via desserialização")],
     "juice":{"name":"Unsigned JWT","diff":"★★★","route":"Authorization: Bearer ...","code":"jwt.verify(token, publicKey) // alg: none aceito","hint":"Altere header alg para none e remova a assinatura."},
     "prev":["Assinatura digital de releases e configs","Deserialização allowlist","Proteção de pipeline (branch protection, OIDC)","mTLS entre serviços internos"],
     "refs":[("OWASP A08:2025","https://owasp.org/Top10/2025/A08_2025-Software_or_Data_Integrity_Failures/")]},
    {"id":"A09","title":"Security Logging and Alerting Failures","pt":"Falhas de Logging e Alerta",
     "sum":"Sem telemetria de segurança, o MTTD explode. IBM 2024: organizações com automação de resposta reduzem custo de breach em US$ 1,76M. Logs sem correlação, sem retention e sem alertas acionáveis são o padrão em PMEs.",
     "cwes":["CWE-778","CWE-117","CWE-532"],
     "cases":[("Target breach, 2013)","Alertas FireEye ignorados; 40M cartões"),("Marriott, 2018","4 anos até detecção de acesso não autorizado")],
     "juice":{"name":"Privacy Policy Inspection","diff":"★☆☆","route":"/rest/admin/application-configuration","code":"// endpoint admin sem log de auditoria\nif (req.user.role === 'admin') { return config }","hint":"Observe ausência de log ao acessar config sensível."},
     "prev":["Log estruturado (JSON) com userId, action, outcome","SIEM com regras de correlação","Retention alinhada a LGPD/compliance","Tabletop exercises com logs reais"],
     "refs":[("OWASP A09:2025","https://owasp.org/Top10/2025/A09_2025-Security_Logging_and_Alerting_Failures/"),("NIST AU family","https://csrc.nist.gov/Projects/risk-management/sp800-53-controls/release-search#!/control?version=5.1&number=AU")]},
    {"id":"A10","title":"Mishandling of Exceptional Conditions","pt":"Tratamento Incorreto de Exceções",
     "sum":"Nova em 2025. Stack traces em produção, fail-open em erros, race conditions e estados inconsistentes após falha parcial. Diferente de misconfiguration: é lógica de tratamento de erro que vaza informação ou abre janela de ataque.",
     "cwes":["CWE-209","CWE-755","CWE-400","CWE-476"],
     "cases":[("Struts Equifax RCE, 2017","Exceção não tratada levou a execução remota"),("Heartbleed OpenSSL, 2014","Leitura OOB por bounds check ausente")],
     "juice":{"name":"Error Handling","diff":"★★☆","route":"/api/Feedbacks","code":"catch(e) { res.status(500).send(e.stack) }","hint":"Provoke erro com payload malformado e leia o stack trace."},
     "prev":["Mensagens genéricas ao cliente; detalhe só em log interno","Fail-closed em componentes de segurança","Circuit breakers e timeouts","Fuzzing de error paths"],
     "refs":[("OWASP A10:2025","https://owasp.org/Top10/2025/A10_2025-Mishandling_of_Exceptional_Conditions/")]},
]

CWE_TOP25 = [
    (1,"CWE-79","Cross-site Scripting (XSS)",60.38,7,"0","A05"),
    (2,"CWE-89","SQL Injection",28.72,4,"+1","A05"),
    (3,"CWE-352","Cross-Site Request Forgery",13.64,0,"+1","A06"),
    (4,"CWE-862","Missing Authorization",13.28,0,"+5","A01"),
    (5,"CWE-787","Out-of-bounds Write",12.68,12,"-3","A10"),
    (6,"CWE-22","Path Traversal",8.99,10,"-1","A01"),
    (7,"CWE-416","Use After Free",8.47,14,"+1","A10"),
    (8,"CWE-125","Out-of-bounds Read",7.88,3,"-2","A10"),
    (9,"CWE-78","OS Command Injection",7.85,20,"-2","A05"),
    (10,"CWE-94","Code Injection",7.57,7,"+1","A05"),
    (11,"CWE-120","Classic Buffer Overflow",6.96,0,"N/A","A10"),
    (12,"CWE-434","Unrestricted File Upload",6.87,4,"-2","A01"),
    (13,"CWE-476","NULL Pointer Dereference",6.41,0,"+8","A10"),
    (14,"CWE-121","Stack-based Buffer Overflow",5.75,4,"N/A","A10"),
    (15,"CWE-502","Deserialization of Untrusted Data",5.23,11,"+1","A08"),
    (16,"CWE-122","Heap-based Buffer Overflow",5.21,6,"N/A","A10"),
    (17,"CWE-863","Incorrect Authorization",4.14,4,"+1","A01"),
    (18,"CWE-20","Improper Input Validation",4.09,2,"-6","A05"),
    (19,"CWE-284","Improper Access Control",4.07,1,"N/A","A01"),
    (20,"CWE-200","Sensitive Information Exposure",4.01,1,"-3","A02"),
    (21,"CWE-306","Missing Authentication",3.47,11,"+4","A07"),
    (22,"CWE-918","Server-Side Request Forgery",3.36,0,"-3","A01"),
    (23,"CWE-77","Command Injection",3.15,2,"-10","A05"),
    (24,"CWE-639","Authorization Bypass via User Key",2.62,0,"+6","A01"),
    (25,"CWE-770","Resource Allocation Without Limits",2.54,0,"+1","A06"),
]

CWE_DETAILS = {
    "CWE-79": ("Entrada não neutralizada vira HTML/JS executável no browser da vítima. Stored, reflected e DOM-based. Mitigação: encoding contextual + CSP.", "DOM XSS no search", "★★★"),
    "CWE-89": ("Concatenação de SQL com input do usuário. Impacto: leitura, escrita, RCE em alguns SGBDs.", "Login Admin", "★★☆"),
    "CWE-352": ("Força o browser autenticado a executar ação não intencional. Mitigação: token anti-CSRF + SameSite cookies.", "CSRF", "★★☆"),
    "CWE-862": ("Endpoint executa ação sem verificar se o caller tem permissão.", "View Basket", "★★☆"),
    "CWE-787": ("Escrita além dos limites do buffer. Classe memory corruption em C/C++.", None, None),
    "CWE-22": ("../ em paths permite leitura arbitrária de arquivos.", "Directory Traversal", "★★☆"),
    "CWE-416": ("Ponteiro usado após free(). Exploração complexa em código nativo.", None, None),
    "CWE-125": ("Leitura além dos limites. Pode vazar memória adjacente.", None, None),
    "CWE-78": ("Input vira argumento de shell. Mitigação: APIs sem shell, allowlist.", "Admin Registration", "★★★"),
    "CWE-94": ("Input gera código executável (eval, template injection).", "Premium Paywall", "★★★"),
    "CWE-120": ("memcpy/strcpy sem checagem de tamanho.", None, None),
    "CWE-434": ("Upload aceita .php, .jsp sem validação de tipo e local.", "Upload Size", "★★☆"),
    "CWE-476": ("Dereference de ponteiro NULL causa crash ou execução.", None, None),
    "CWE-121": ("Overflow na stack. Vetor clássico de RCE.", None, None),
    "CWE-502": ("Objeto desserializado de fonte não confiável executa código.", "Blocked RCE", "★★★"),
    "CWE-122": ("Overflow no heap. Exploração via heap spraying.", None, None),
    "CWE-863": ("Checagem de autorização existe mas está errada (lógica invertida, role errada).", "Admin Section", "★★☆"),
    "CWE-20": ("Validação ausente ou incompleta na entrada.", "Password Strength", "★☆☆"),
    "CWE-284": ("Política de acesso não restringe atores não autorizados.", "Five-Star Feedback", "★★☆"),
    "CWE-200": ("Resposta ou log expõe dados que deveriam ser restritos.", "Access Log", "★☆☆"),
    "CWE-306": ("Função crítica acessível sem autenticação.", "Score Board", "★☆☆"),
    "CWE-918": ("App faz request server-side para URL controlada pelo atacante.", "SSRF", "★★★"),
    "CWE-77": ("Injeção em comandos genéricos (não só OS).", "Weird Crypto", "★★☆"),
    "CWE-639": ("Chave controlada pelo usuário (userId) usada sem validar ownership.", "View Basket", "★★☆"),
    "CWE-770": ("Sem throttling: brute force, DoS, resource exhaustion.", "CAPTCHA Bypass", "★★☆"),
}

MARKET = [
    ("US$ 4,88M","Custo médio global de breach (IBM, 2024)"),
    ("277 dias","MTTI médio para identificar breach (IBM, 2024)"),
    ("15%","Incidentes web com misconfiguration (Verizon DBIR, 2024)"),
    ("94%","Apps com alguma falha de access control (OWASP WSTG)"),
    ("60,38","Score CWE-79 no TOP 25 MITRE 2025"),
]

def esc(s): return html.escape(str(s))

def render_owasp(o):
    cases = "".join(f'<li><b>{esc(c[0])}</b> — {esc(c[1])}</li>' for c in o["cases"])
    cwes = "".join(f'<a href="#cwe-{c.split("-")[1]}" class="ok-badge cyan pill cwe-link" data-cwe="{c}">{c}</a> ' for c in o["cwes"])
    refs = "".join(f'<li><a href="{esc(r[1])}" target="_blank" rel="noopener">{esc(r[0])}</a></li>' for r in o["refs"])
    prev = "".join(f'<li>{esc(p)}</li>' for p in o["prev"])
    j = o["juice"]
    return f'''
<section class="lesson-sec" id="owasp-{o["id"]}" data-owasp="{o["id"]}" data-search="{esc(o["id"]+" "+o["title"]+" "+o["pt"])}">
  <div class="ok-sec-hd"><div class="ok-left">
    <div class="ok-sec-num"><b>{o["id"]}</b><span>·</span><span>owasp 2025</span></div>
    <h2>{esc(o["pt"])}</h2>
  </div><div class="ok-right">{esc(o["title"])}</div></div>
  <p class="ok-t-body lead">{esc(o["sum"])}</p>
  <div class="grid-2 lesson-grid">
    <div class="ok-card striped"><span class="ok-tag">// cwe correlacionadas</span><div class="tag-row">{cwes}</div></div>
    <div class="ok-card"><span class="ok-tag">// casos reais</span><ul class="ok-deliverables single">{cases}</ul></div>
  </div>
  <div class="ok-terminal" style="margin-top:var(--ok-s-6)">
    <div class="topbar"><span class="dots"><span></span><span></span><span></span></span>
      <span>juice-shop · {esc(j["name"])} · {esc(j["diff"])}</span>
      <span class="status">● lab</span></div>
    <div class="body">
      <div class="line"><span class="prompt">$</span><span class="cmd">curl -X GET https://juice-shop.local{esc(j["route"])}</span></div>
      <div class="line out"><pre class="code-snippet">{esc(j["code"])}</pre></div>
      <div class="line out"><span class="ok-cyan">hint:</span> {esc(j["hint"])}</div>
    </div>
  </div>
  <div class="grid-2 lesson-grid" style="margin-top:var(--ok-s-6)">
    <div class="ok-card featured"><span class="ok-tag">// controles</span><ul class="ok-deliverables single">{prev}</ul></div>
    <div class="ok-card"><span class="ok-tag">// referências</span><ul class="ok-deliverables single ref-list">{refs}</ul></div>
  </div>
</section>'''

def render_cwe(row):
    rank, cid, name, score, kev, trend, owasp = row
    num = cid.split("-")[1]
    det = CWE_DETAILS.get(cid, ("", None, None))
    summary, juice_name, juice_diff = det
    juice_block = ""
    if juice_name:
        juice_block = f'<div class="ok-badge accent pill" style="margin-top:12px">Juice Shop: {esc(juice_name)} {esc(juice_diff or "")}</div>'
    trend_cls = "up" if trend.startswith("+") else ("down" if trend.startswith("-") else "flat")
    return f'''
<section class="lesson-sec cwe-sec" id="cwe-{num}" data-cwe="{cid}" data-owasp="{owasp}" data-search="{esc(cid+" "+name)}">
  <div class="ok-sec-hd"><div class="ok-left">
    <div class="ok-sec-num"><b>#{rank}</b><span>·</span><span>{cid}</span></div>
    <h2>{esc(name)}</h2>
  </div><div class="ok-right">
    <span class="ok-badge accent">score {score}</span>
    <span class="ok-badge {'success' if kev else 'ghost'}">KEV: {kev}</span>
    <a href="#owasp-{owasp}" class="ok-badge magenta pill owasp-link">{owasp}</a>
  </div></div>
  <p class="ok-t-body lead">{esc(summary)}</p>
  <div class="cwe-meta">
    <span class="trend {trend_cls}">vs 2024: {esc(trend)}</span>
    {juice_block}
  </div>
</section>'''

owasp_html = "\n".join(render_owasp(o) for o in OWASP)
cwe_html = "\n".join(render_cwe(r) for r in CWE_TOP25)

bars = ""
max_s = 60.38
for r in CWE_TOP25[:10]:
    pct = round(r[3]/max_s*100)
    bars += f'<div class="ok-bar-row" data-cwe="{r[1]}"><span class="ok-bar-label">{r[1]}</span><span class="ok-bar-track"><span class="ok-bar-fill" style="width:{pct}%"></span></span><span class="ok-bar-value">{r[3]}</span></div>\n'

market_cards = "".join(f'<div class="ok-card"><span class="ok-tag">// mercado</span><h4 class="stat-num">{esc(m[0])}</h4><p>{esc(m[1])}</p></div>' for m in MARKET)

# Correlation matrix rows
corr_rows = ""
for o in OWASP:
    for c in o["cwes"]:
        corr_rows += f'<tr data-owasp="{o["id"]}" data-cwe="{c}"><td><a href="#owasp-{o["id"]}">{o["id"]}</a></td><td><a href="#cwe-{c.split("-")[1]}">{c}</a></td><td>{o["pt"]}</td></tr>'

DATA_JSON = json.dumps({"owasp":[o["id"] for o in OWASP],"cwe":[r[1] for r in CWE_TOP25]}, ensure_ascii=False)

OUT = f'''<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>OWASP Top 10:2025 + CWE TOP 25 — Referência AppSec</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=JetBrains+Mono:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<style>
{OKAMI}
{PATTERNS}
/* === AULA PAGE === */
body.ok.theme-light{{
  --ok-bg-0:#f0f0f5;--ok-bg-1:#ffffff;--ok-bg-2:#f8f8fc;--ok-bg-3:#e8e8f0;
  --ok-line:#d8d8e4;--ok-line-soft:#e8e8f0;--ok-grid:rgba(0,0,0,0.04);
  --ok-fg:#11111b;--ok-fg-soft:#3d3e50;--ok-fg-mute:#6c6d80;--ok-fg-dim:#b9bac8;
  --ok-glow:0.25;
}}
body.ok.theme-light::before,body.ok.theme-light::after{{opacity:.3}}
.toolbar{{
  position:fixed;top:0;left:0;right:0;z-index:100;
  background:color-mix(in srgb,var(--ok-bg-1) 92%,transparent);
  backdrop-filter:blur(12px);border-bottom:1px solid var(--ok-line);
  padding:10px var(--ok-s-7);display:flex;align-items:center;gap:12px;flex-wrap:wrap;
}}
.toolbar .brand{{font-family:var(--ok-mono);font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:var(--ok-accent);margin-right:auto}}
.toolbar .ok-input{{max-width:220px;padding:8px 12px;font-size:12px}}
.progress-bar{{height:2px;background:var(--ok-bg-3);flex:1;max-width:120px;min-width:60px}}
.progress-bar i{{display:block;height:100%;background:var(--ok-accent);width:0%;transition:width .3s}}
.layout{{display:grid;grid-template-columns:260px 1fr;gap:0;padding-top:56px;min-height:100vh}}
.sidebar{{
  position:sticky;top:56px;height:calc(100vh - 56px);overflow-y:auto;
  border-right:1px solid var(--ok-line);padding:var(--ok-s-6);background:var(--ok-bg-1);
}}
.sidebar h3{{font-family:var(--ok-mono);font-size:10px;letter-spacing:.14em;text-transform:uppercase;color:var(--ok-fg-mute);margin:var(--ok-s-5) 0 var(--ok-s-3)}}
.nav-link{{
  display:block;padding:8px 10px;font-family:var(--ok-mono);font-size:11px;
  color:var(--ok-fg-soft);border-left:2px solid transparent;margin-bottom:2px;
}}
.nav-link:hover,.nav-link.active{{color:var(--ok-fg);border-left-color:var(--ok-accent);background:color-mix(in oklch,var(--ok-accent) 6%,transparent)}}
.nav-link.done{{color:var(--ok-success)}}
.main{{padding:var(--ok-s-8) var(--ok-s-9);max-width:960px}}
.hero{{padding:var(--ok-s-10) 0 var(--ok-s-9);border-bottom:1px solid var(--ok-line)}}
.hero h1{{font-family:var(--ok-display);font-weight:500;font-size:clamp(36px,5vw,64px);letter-spacing:-.035em;line-height:1;margin:var(--ok-s-5) 0}}
.hero h1 em{{color:var(--ok-accent);font-style:normal}}
.hero .lede{{max-width:680px;color:var(--ok-fg-soft);font-size:18px;line-height:1.55}}
.meta-row{{display:flex;flex-wrap:wrap;gap:var(--ok-s-6);margin-top:var(--ok-s-7);font-family:var(--ok-mono);font-size:11px;letter-spacing:.1em;text-transform:uppercase;color:var(--ok-fg-mute)}}
.lesson-sec{{padding:var(--ok-s-10) 0;border-bottom:1px solid var(--ok-line-soft);scroll-margin-top:72px}}
.lesson-sec.highlight{{background:color-mix(in oklch,var(--ok-cyan) 5%,transparent);margin:0 -var(--ok-s-6);padding-left:var(--ok-s-6);padding-right:var(--ok-s-6)}}
.lead{{margin-bottom:var(--ok-s-6)}}
.grid-2{{display:grid;grid-template-columns:1fr 1fr;gap:var(--ok-s-5)}}
.lesson-grid{{margin-top:var(--ok-s-5)}}
.tag-row{{display:flex;flex-wrap:wrap;gap:8px}}
.ok-deliverables.single{{grid-template-columns:1fr}}
.ref-list a{{color:var(--ok-cyan);border-bottom:1px dashed var(--ok-line)}}
.code-snippet{{margin:12px 0 0;padding:0;background:transparent;border:0;font-size:12px;color:var(--ok-fg-soft);white-space:pre-wrap}}
.stat-num{{font-family:var(--ok-display);font-size:32px;color:var(--ok-accent);margin:8px 0}}
.corr-table{{width:100%;border-collapse:collapse;font-family:var(--ok-mono);font-size:12px}}
.corr-table th,.corr-table td{{padding:10px 12px;border-bottom:1px solid var(--ok-line-soft);text-align:left}}
.corr-table th{{color:var(--ok-fg-mute);font-size:10px;letter-spacing:.12em;text-transform:uppercase}}
.corr-table tr:hover{{background:color-mix(in oklch,var(--ok-accent) 5%,transparent)}}
.corr-table a{{color:var(--ok-cyan)}}
.trend{{font-family:var(--ok-mono);font-size:12px}}
.trend.up{{color:var(--ok-danger)}}.trend.down{{color:var(--ok-success)}}.trend.flat{{color:var(--ok-fg-mute)}}
.cwe-meta{{margin-top:var(--ok-s-4)}}
.quiz-box{{border:1px solid var(--ok-line);padding:var(--ok-s-6);margin-top:var(--ok-s-6);background:var(--ok-bg-1)}}
.quiz-box h4{{margin:0 0 var(--ok-s-4)}}
.present-mode .sidebar,.present-mode .toolbar .hide-present{{display:none!important}}
.present-mode .layout{{grid-template-columns:1fr}}
.present-mode .main{{max-width:100%;padding:var(--ok-s-10)}}
@media(max-width:900px){{.layout{{grid-template-columns:1fr}}.sidebar{{position:relative;height:auto;top:0}}.grid-2{{grid-template-columns:1fr}}}}
@media print{{
  .toolbar,.sidebar,.no-print{{display:none!important}}
  .layout{{grid-template-columns:1fr;padding:0}}
  .main{{max-width:100%;padding:20px}}
  body.ok{{background:#fff;color:#000}}
  .lesson-sec{{page-break-inside:avoid}}
}}
</style>
</head>
<body class="ok">
<header class="toolbar no-print">
  <span class="brand">// appsec · owasp + cwe top 25</span>
  <input type="search" class="ok-input" id="search" placeholder="Buscar OWASP, CWE…" aria-label="Buscar"/>
  <div class="progress-bar" title="Progresso de leitura"><i id="progress"></i></div>
  <button class="ok-btn ghost sm hide-present" id="btn-theme" type="button">Tema</button>
  <button class="ok-btn cyan sm hide-present" id="btn-present" type="button">Modo apresentação</button>
  <button class="ok-btn solid sm" id="btn-pdf" type="button">Exportar PDF</button>
</header>
<div class="layout">
<aside class="sidebar no-print" id="sidebar">
  <h3>// navegação</h3>
  <a class="nav-link" href="#intro">Introdução</a>
  <a class="nav-link" href="#mercado">Mercado</a>
  <a class="nav-link" href="#correlacao">Correlação</a>
  <h3>// owasp top 10</h3>
  {"".join(f'<a class="nav-link" href="#owasp-{o["id"]}" data-nav="{o["id"]}">{o["id"]} {o["pt"]}</a>' for o in OWASP)}
  <h3>// cwe top 25</h3>
  {"".join(f'<a class="nav-link" href="#cwe-{r[1].split("-")[1]}" data-nav-cwe="{r[1]}">#{r[0]} {r[1]}</a>' for r in CWE_TOP25)}
  <h3>// laboratório</h3>
  <a class="nav-link" href="#juice">Juice Shop</a>
  <a class="nav-link" href="#quiz">Quiz</a>
</aside>
<main class="main" id="main">

<section class="hero" id="intro">
  <div class="ok-eyebrow">Segurança de aplicações · Referência interativa</div>
  <h1>OWASP Top 10<em>:</em>2025<br/>+ CWE TOP 25</h1>
  <p class="lede">Guia que cruza as 10 categorias do OWASP Top 10 com as 25 fraquezas do CWE TOP 25 (MITRE). Cada item reúne conceitos, exemplos de código, casos documentados, dados de mercado e labs práticos no OWASP Juice Shop.</p>
  <div class="meta-row">
    <span>OWASP <b style="color:var(--ok-fg)">10 categorias</b></span>
    <span>CWE <b style="color:var(--ok-fg)">25 fraquezas</b></span>
    <span>Fonte <b style="color:var(--ok-fg)">MITRE · Dez/2025</b></span>
    <span>Lab <b style="color:var(--ok-fg)">Juice Shop</b></span>
  </div>
</section>

<section class="lesson-sec" id="mercado">
  <div class="ok-sec-hd"><div class="ok-left"><div class="ok-sec-num"><b>§00</b><span>·</span><span>mercado</span></div><h2>Panorama <em>2024–2025</em></h2></div>
  <div class="ok-right">Dados citados com fonte. Não são projeção.</div></div>
  <div class="grid-2" style="grid-template-columns:repeat(auto-fit,minmax(180px,1fr))">{market_cards}</div>
  <div class="ok-meter" style="margin-top:var(--ok-s-7)">
    <div class="ok-meter-head"><span class="label">// maturidade appsec típica em PMEs</span></div>
    <div class="ok-meter-track">
      <div class="ok-meter-line"></div>
      <div class="ok-meter-bar from" style="left:0;width:40%"></div>
      <div class="ok-meter-bar to" style="left:0;width:80%"></div>
      <div class="ok-meter-step now" style="left:0%"><span class="dot"></span><span class="lvl">0</span><span class="nm">Ad-hoc</span></div>
      <div class="ok-meter-step now" style="left:20%"><span class="dot"></span><span class="lvl">1</span><span class="nm">Reativo</span></div>
      <div class="ok-meter-step now target" style="left:40%"><span class="dot"></span><span class="lvl">2</span><span class="nm">Definido</span></div>
      <div class="ok-meter-step target" style="left:60%"><span class="dot"></span><span class="lvl">3</span><span class="nm">Gerenciado</span></div>
      <div class="ok-meter-step target" style="left:80%"><span class="dot"></span><span class="lvl">4</span><span class="nm">Otimizado</span></div>
    </div>
    <div class="ok-meter-caption">Meta de maturidade: sair do nível 2 (checklist sem contexto) para o 3 (controles medidos, threat model por feature, pipeline com gate de segurança).</div>
  </div>
</section>

<section class="lesson-sec" id="correlacao">
  <div class="ok-sec-hd"><div class="ok-left"><div class="ok-sec-num"><b>§mapa</b><span>·</span><span>correlação</span></div><h2>OWASP <em>↔</em> CWE</h2></div>
  <div class="ok-right">Clique numa linha para destacar as seções ligadas.</div></div>
  <div class="grid-2">
    <div><div class="sub-h" style="font-family:var(--ok-mono);font-size:10px;color:var(--ok-fg-mute);margin-bottom:12px">_ top 10 cwe por score</div><div class="ok-bars">{bars}</div></div>
    <div class="ok-card striped" style="max-height:400px;overflow:auto">
      <span class="ok-tag">// matriz de correlação</span>
      <table class="corr-table" id="corr-table">
        <thead><tr><th>OWASP</th><th>CWE</th><th>Categoria</th></tr></thead>
        <tbody>{corr_rows}</tbody>
      </table>
    </div>
  </div>
</section>

<div class="ok-sec-hd" style="margin-top:var(--ok-s-10)"><div class="ok-left"><div class="ok-sec-num"><b>§owasp</b><span>·</span><span>top 10</span></div><h2>Riscos <em>2025</em></h2></div></div>
{owasp_html}

<div class="ok-sec-hd" style="margin-top:var(--ok-s-10)"><div class="ok-left"><div class="ok-sec-num"><b>§cwe</b><span>·</span><span>top 25</span></div><h2>Fraquezas <em>MITRE</em></h2></div>
<div class="ok-right">Ranking oficial dezembro/2025. Score = frequência × impacto.</div></div>
{cwe_html}

<section class="lesson-sec" id="juice">
  <div class="ok-sec-hd"><div class="ok-left"><div class="ok-sec-num"><b>§lab</b><span>·</span><span>juice shop</span></div><h2>Laboratório <em>prático</em></h2></div></div>
  <p class="ok-t-body lead">OWASP Juice Shop é uma SPA intencionalmente vulnerável em Node.js/Angular. Rode localmente com Docker e mapeie cada challenge ao OWASP/CWE visto em sala.</p>
  <div class="ok-terminal">
    <div class="topbar"><span class="dots"><span></span><span></span><span></span></span><span>setup · docker</span><span class="status">● ready</span></div>
    <div class="body">
      <div class="line"><span class="prompt">$</span><span class="cmd">docker run -d -p 3000:3000 bkimminich/juice-shop</span></div>
      <div class="line out"><span class="ok-ok">→</span> http://localhost:3000</div>
      <div class="line"><span class="prompt">$</span><span class="cmd">git clone https://github.com/juice-shop/juice-shop.git</span></div>
      <div class="line out">Código-fonte em TypeScript. Busque rotas em <b>routes/</b>, modelos em <b>models/</b>, filtros em <b>lib/</b>.</div>
    </div>
  </div>
  <div class="ok-stack" style="margin-top:var(--ok-s-6)">
    <div class="ok-stack-card"><div class="ok-stack-h">// recon</div><h4>Enumeração</h4><ul><li>Score Board</li><li>Directory scan</li><li>package.json</li></ul></div>
    <div class="ok-stack-card cyan"><div class="ok-stack-h">// exploit</div><h4>Exploração</h4><ul><li>SQLi login</li><li>XSS search</li><li>IDOR basket</li></ul></div>
    <div class="ok-stack-card magenta"><div class="ok-stack-h">// analyze</div><h4>Análise</h4><ul><li>Diff com fix</li><li>Mapa CWE</li><li>Relatório</li></ul></div>
    <div class="ok-stack-card"><div class="ok-stack-h">// report</div><h4>Entrega</h4><ul><li>PoC + impacto</li><li>Remediação</li><li>Referência OWASP</li></ul></div>
  </div>
</section>

<section class="lesson-sec" id="quiz">
  <div class="ok-sec-hd"><div class="ok-left"><div class="ok-sec-num"><b>§?</b><span>·</span><span>quiz</span></div><h2>Quiz de verificação</h2></div></div>
  <div class="quiz-box" id="quiz-box">
    <h4 id="quiz-q">Carregando…</h4>
    <div id="quiz-opts"></div>
    <p class="ok-hint" id="quiz-fb" style="margin-top:12px"></p>
    <button class="ok-btn cyan sm" id="quiz-next" type="button" style="margin-top:16px">Próxima →</button>
  </div>
</section>

<footer class="foot" style="margin-top:var(--ok-s-10);padding:var(--ok-s-8) 0;border-top:1px solid var(--ok-line);font-family:var(--ok-mono);font-size:11px;color:var(--ok-fg-mute)">
  <span>OWASP Top 10:2025 · CWE TOP 25:2025 · Referência AppSec</span>
  <span>Fontes: owasp.org · cwe.mitre.org · github.com/juice-shop/juice-shop</span>
</footer>
</main>
</div>
<script>
const QUIZ=[
  {{q:"Qual OWASP 2025 permanece no topo?",opts:["A05 Injection","A01 Broken Access Control","A04 Crypto Failures"],a:1}},
  {{q:"CWE com maior score no TOP 25 2025?",opts:["CWE-89 SQLi","CWE-79 XSS","CWE-862"],a:1}},
  {{q:"Nova categoria OWASP 2025 ligada a npm/SolarWinds?",opts:["A03 Supply Chain","A08 Integrity","A02 Misconfig"],a:0}},
  {{q:"Challenge Juice Shop para IDOR?",opts:["Login Admin","View Basket","CAPTCHA Bypass"],a:1}},
  {{q:"CWE-502 relaciona-se principalmente a qual OWASP?",opts:["A08 Integrity","A09 Logging","A10 Exceptions"],a:0}}
];
let qi=0;const qEl=document.getElementById('quiz-q'),oEl=document.getElementById('quiz-opts'),fEl=document.getElementById('quiz-fb');
function showQuiz(){{
  const q=QUIZ[qi];qEl.textContent=q.q;fEl.textContent='';
  oEl.innerHTML=q.opts.map((t,i)=>`<button class="ok-btn ghost sm quiz-opt" data-i="${{i}}" type="button">${{t}}</button>`).join(' ');
}}
oEl.addEventListener('click',e=>{{
  const b=e.target.closest('.quiz-opt');if(!b)return;
  const i=+b.dataset.i;const q=QUIZ[qi];
  fEl.textContent=i===q.a?'Correto.':'Incorreto. Resposta: '+q.opts[q.a];
  fEl.style.color=i===q.a?'var(--ok-success)':'var(--ok-magenta)';
}});
document.getElementById('quiz-next').onclick=()=>{{qi=(qi+1)%QUIZ.length;showQuiz();}};
showQuiz();

document.getElementById('btn-theme').onclick=()=>document.body.classList.toggle('theme-light');
document.getElementById('btn-pdf').onclick=()=>window.print();
document.getElementById('btn-present').onclick=()=>document.body.classList.toggle('present-mode');

const search=document.getElementById('search');
search.addEventListener('input',()=>{{
  const q=search.value.toLowerCase();
  document.querySelectorAll('.lesson-sec').forEach(s=>{{
    const m=!q||((s.dataset.search||s.textContent).toLowerCase().includes(q));
    s.style.display=m?'':'none';
  }});
}});

document.getElementById('corr-table').addEventListener('click',e=>{{
  const tr=e.target.closest('tr');if(!tr||!tr.dataset.owasp)return;
  document.querySelectorAll('.lesson-sec').forEach(s=>s.classList.remove('highlight'));
  const o=document.getElementById('owasp-'+tr.dataset.owasp);
  const c=document.querySelector('[data-cwe="'+tr.dataset.cwe+'"]');
  if(o){{o.classList.add('highlight');o.scrollIntoView({{behavior:'smooth',block:'start'}});}}
  if(c)c.classList.add('highlight');
}});

document.querySelectorAll('.cwe-link').forEach(a=>a.addEventListener('click',e=>{{
  e.preventDefault();
  const id=a.dataset.cwe.split('-')[1];
  document.getElementById('cwe-'+id)?.scrollIntoView({{behavior:'smooth'}});
}}));

const seen=new Set();
const obs=new IntersectionObserver(entries=>{{
  entries.forEach(en=>{{
    if(en.isIntersecting){{
      const id=en.target.id;if(id)seen.add(id);
      const pct=Math.round(seen.size/45*100);
      document.getElementById('progress').style.width=pct+'%';
      document.querySelectorAll('.nav-link').forEach(l=>{{
        if(l.getAttribute('href')==='#'+id)l.classList.add('done');
      }});
    }}
  }});
}},{{threshold:0.3}});
document.querySelectorAll('.lesson-sec,.hero').forEach(s=>obs.observe(s));
</script>
</body>
</html>'''

(ROOT / "aula-owasp-cwe.html").write_text(OUT, encoding="utf-8")
print(f"Gerado: {ROOT / 'aula-owasp-cwe.html'} ({len(OUT):,} bytes)")