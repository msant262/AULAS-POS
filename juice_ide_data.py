# Dados da IDE Juice Shop — validação por lab


def _indent_block(text, spaces=4):
    pad = " " * spaces
    return "\n".join(pad + line if line else pad for line in str(text).split("\n"))


def _assemble_shell(header, core, footer, indent=4):
    return header + "\n" + _indent_block(core, indent) + footer


def _focus_range(header, core):
    start = len(header.splitlines()) + 1
    end = start + max(0, len(str(core).splitlines()) - 1)
    return start, end


def _route_header(file, challenge, fn_name, marker):
    return f"""/**
 * {file} — Juice Shop (trecho educacional)
 * Challenge: {challenge}
 */
import {{ type Request, type Response, type NextFunction }} from 'express'
import * as security from '../lib/insecurity'
import * as utils from '../lib/utils'

export function {fn_name} () {{
  return async (req: Request, res: Response, next: NextFunction) => {{
    const user = security.authenticatedUsers.from(req)

    if (req.method === 'OPTIONS') {{
      res.status(204).end()
      return
    }}

    {marker}"""

_ROUTE_FOOTER = """
  }
}
"""

_LIB_HEADER_VULN = """/**
 * lib/insecurity.ts — Juice Shop (trecho educacional)
 * Challenge: __CHALLENGE__
 */
import crypto from 'node:crypto'
import jwt from 'jsonwebtoken'
import jws from 'jws'
import config from 'config'

const privateKey = 'private-key'
const publicKey = 'public-key'

// ⚠ VULNERÁVEL — trecho problemático"""

_LIB_HEADER_FIX = _LIB_HEADER_VULN.replace("⚠ VULNERÁVEL", "✓ CORRIGIDO")
_LIB_FOOTER = "\n\nexport { hash, authorize, verify, isAuthorized, isRedirectAllowed }"


def _pkg_header(challenge, marker):
    return f"""{{
  "name": "juice-shop",
  "version": "17.1.0",
  "description": "OWASP Juice Shop — intentionally insecure app",
  "license": "MIT",
  "engines": {{ "node": "20 - 24" }},
  "scripts": {{
    "start": "node app",
    "test": "npm run test:unit",
    "lint": "eslint routes/**/*.ts lib/**/*.ts"
  }},
  {marker}"""


_PKG_FOOTER = """
  "devDependencies": {
    "eslint": "^8.57.0",
    "typescript": "^5.4.0"
  }
}"""


def expand_juice_context(key, j):
    """Envolve o snippet em contexto de arquivo maior (vuln à esquerda, fix à direita)."""
    vuln, fix = j["code"], j["fix"]
    file, challenge = j["file"], j["challenge"]

    if file == "package.json":
        h_vuln = _pkg_header(challenge, '"// ⚠ VULNERÁVEL — dependências com CVE": true,')
        h_fix = _pkg_header(challenge, '"// ✓ CORRIGIDO — audit no CI": true,')
        code = _assemble_shell(h_vuln, vuln, _PKG_FOOTER, indent=2)
        fix_code = _assemble_shell(h_fix, fix, _PKG_FOOTER, indent=2)
        focus_start, focus_end = _focus_range(h_vuln, vuln)
        return code, fix_code, focus_start, focus_end

    if file == "lib/insecurity.ts":
        h_vuln = _LIB_HEADER_VULN.replace("__CHALLENGE__", challenge)
        h_fix = _LIB_HEADER_FIX.replace("__CHALLENGE__", challenge)
        code = _assemble_shell(h_vuln, vuln, _LIB_FOOTER)
        fix_code = _assemble_shell(h_fix, fix, _LIB_FOOTER)
        focus_start, focus_end = _focus_range(h_vuln, vuln)
        return code, fix_code, focus_start, focus_end

    fn_name = file.rsplit("/", 1)[-1].replace(".ts", "")
    h_vuln = _route_header(file, challenge, fn_name, "// ⚠ VULNERÁVEL — trecho problemático")
    h_fix = _route_header(file, challenge, fn_name, "// ✓ CORRIGIDO — patch aplicado")
    code = _assemble_shell(h_vuln, vuln, _ROUTE_FOOTER)
    fix_code = _assemble_shell(h_fix, fix, _ROUTE_FOOTER)
    focus_start, focus_end = _focus_range(h_vuln, vuln)
    return code, fix_code, focus_start, focus_end


def build_juice_validate(key, j):
    payload = j.get("payload", "")
    file = j["file"]
    challenge = j["challenge"]
    generic_vuln = [
        {"t": "cmd", "x": f"$ semgrep --config auto {file}"},
        {"t": "warn", "x": f"⚠ finding em {file}:{j['line']} — {challenge}"},
        {"t": "cmd", "x": f"$ # payload: {payload}" if payload and payload != "N/A" else f"$ curl -I http://localhost:3000"},
        {"t": "attack", "x": "→ Exploit reproduzível no Juice Shop local"},
        {"t": "err", "x": "✗ Validação FALHOU — código ainda vulnerável"},
    ]
    generic_fix = [
        {"t": "cmd", "x": f"$ semgrep --config auto {file}"},
        {"t": "ok", "x": "✓ No findings — padrão inseguro removido"},
        {"t": "cmd", "x": "$ npm test -- --grep security 2>/dev/null || echo 'tests OK'"},
        {"t": "http", "x": "HTTP/1.1 401/403 — ataque bloqueado"},
        {"t": "ok", "x": "✓ Validação OK — correção aceita"},
    ]
    scripts = {
        "login_sql": {
            "vuln": [
                {"t": "cmd", "x": "$ curl -s -X POST localhost:3000/rest/user/login -H 'Content-Type: application/json' -d '{\"email\":\"\\' OR 1=1--\",\"password\":\"x\"}'"},
                {"t": "http", "x": "HTTP/1.1 200 OK — token retornado"},
                {"t": "attack", "x": "→ SQLi em login.ts:34 — bypass de autenticação"},
                {"t": "err", "x": "✗ Validação FALHOU"},
            ],
            "fix": [
                {"t": "cmd", "x": "$ curl -s -X POST localhost:3000/rest/user/login -d '{\"email\":\"\\' OR 1=1--\",\"password\":\"x\"}'"},
                {"t": "http", "x": "HTTP/1.1 401 Unauthorized"},
                {"t": "ok", "x": "✓ Prepared statement / ORM — CWE-89 mitigado"},
            ],
        },
        "basket_idor": {
            "vuln": [
                {"t": "cmd", "x": "$ curl -s -H 'Authorization: Bearer $TOKEN' localhost:3000/rest/basket/2"},
                {"t": "attack", "x": "→ JSON da cesta alheia (bid ≠ 2)"},
                {"t": "err", "x": "✗ IDOR ativo em basket.ts"},
            ],
            "fix": [
                {"t": "cmd", "x": "$ curl -s -H 'Authorization: Bearer $TOKEN' localhost:3000/rest/basket/2"},
                {"t": "http", "x": "HTTP/1.1 403 Forbidden"},
                {"t": "ok", "x": "✓ Ownership check — CWE-639"},
            ],
        },
        "search_sqli": {
            "vuln": [
                {"t": "cmd", "x": "$ curl -s \"localhost:3000/rest/products/search?q=') UNION SELECT email,password FROM Users--\""},
                {"t": "attack", "x": "→ UNION injection em search.ts"},
                {"t": "err", "x": "✗ Validação FALHOU"},
            ],
            "fix": [
                {"t": "cmd", "x": "$ curl -s \"localhost:3000/rest/products/search?q=') UNION SELECT...\""},
                {"t": "http", "x": "HTTP/1.1 400 Bad Request"},
                {"t": "ok", "x": "✓ Query parametrizada"},
            ],
        },
        "feedback_xss": {
            "vuln": [
                {"t": "cmd", "x": "$ curl -s 'localhost:3000/track-result?id=<script>alert(1)</script>'"},
                {"t": "attack", "x": "→ Payload refletido sem encode no HTML"},
                {"t": "err", "x": "✗ XSS presente — CWE-79"},
            ],
            "fix": [
                {"t": "cmd", "x": "$ curl -s 'localhost:3000/track-result?id=<script>alert(1)</script>'"},
                {"t": "ok", "x": "✓ Resposta JSON / valor escapado"},
            ],
        },
        "csrf_transfer": {
            "vuln": [
                {"t": "cmd", "x": "$ curl -s -X POST localhost:3000/rest/wallet/transfer -d 'amount=999'"},
                {"t": "attack", "x": "→ POST sem CSRF token aceito"},
                {"t": "err", "x": "✗ CWE-352"},
            ],
            "fix": [
                {"t": "cmd", "x": "$ curl -s -X POST localhost:3000/rest/wallet/transfer -d 'amount=999'"},
                {"t": "http", "x": "HTTP/1.1 403 — CSRF token missing"},
                {"t": "ok", "x": "✓ Token synchronizer ativo"},
            ],
        },
        "npm_audit": {
            "vuln": [
                {"t": "cmd", "x": "$ npm audit --audit-level=high"},
                {"t": "warn", "x": "found 12 vulnerabilities (sanitize-html, jsonwebtoken...)"},
                {"t": "err", "x": "✗ Supply chain — A03"},
            ],
            "fix": [
                {"t": "cmd", "x": "$ npm audit --audit-level=high"},
                {"t": "ok", "x": "found 0 vulnerabilities"},
            ],
        },
    }
    if key in scripts:
        return scripts[key]
    return {"vuln": generic_vuln, "fix": generic_fix}


def build_juice_ide_entries(juice_dict, owasp_list):
    key_to_owasp = {}
    for o in owasp_list:
        for k in o.get("juice", []):
            key_to_owasp.setdefault(k, o["id"])
    entries = []
    for key, j in sorted(juice_dict.items(), key=lambda kv: (kv[1]["file"], kv[1]["line"])):
        validate = build_juice_validate(key, j)
        apply_steps = [
            {"t": "dim", "x": f"git checkout -b fix/{key}"},
            {"t": "cmd", "x": f"$ code {j['file']}:{j['line']}"},
            {"t": "warn", "x": f"// {j['challenge']}"},
        ]
        for i, line in enumerate(j["fix"].split("\n")[:6]):
            apply_steps.append({"t": "add", "x": f"+ {line}"})
        apply_steps.append({"t": "cmd", "x": "$ git diff --stat"})
        apply_steps.append({"t": "ok", "x": f"✓ Patch aplicado em {j['file']}"})
        code_full, fix_full, focus_start, focus_end = expand_juice_context(key, j)
        entries.append({
            "id": key,
            "file": j["file"],
            "line": j["line"],
            "focus_start": focus_start,
            "focus_end": focus_end,
            "challenge": j["challenge"],
            "owasp": key_to_owasp.get(key, ""),
            "code": code_full,
            "fix": fix_full,
            "payload": j.get("payload", ""),
            "steps": j.get("steps", []),
            "validate": validate,
            "apply": apply_steps,
        })
    return entries