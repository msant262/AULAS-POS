# Expansão de inteligência — pesquisa extra, notícias, mercado 2025, gráficos

RESEARCH_EXTRA = [
  {"id": "llm_top10", "source": "OWASP LLM Top 10", "tag": "design",
   "headline": "GenAI expande superfície — prompt injection e data leakage",
   "stats": [("LLM01", "Prompt Injection"), ("LLM02", "Sensitive Info Disclosure"), ("LLM06", "Excessive Agency"), ("10", "Riscos LLM")],
   "body": [
     "Aplicações com LLM introduzem vetores fora do Top 10 web clássico: jailbreak, tool abuse, training data extraction e RAG poisoning.",
     "Na prática: trate copilot interno como microserviço Tier-0 — threat model, logging, rate limit e revisão de system prompt."
   ],
   "actions": ["LLM firewall (input/output)", "Segregar collections por tenant", "Audit trail de tool calls", "Benchmark de jailbreak no CI"],
   "link": "https://owasp.org/www-project-top-10-for-large-language-model-applications/"},
]

NEWS_FEED = [
  {"date": "2025-12", "source": "MITRE", "title": "CWE TOP 25 2025 publicado",
   "summary": "Ranking definitivo com 39.080 CVEs analisados. CWE-79 (XSS) mantém liderança com score 60,38 — mais que o dobro do segundo colocado.",
   "body": "Destaques: CNA mapping subiu de 53% para 67% (+14pp). CWE-862 (Missing Authorization) subiu 5 posições para #4. Buffer overflows clássicos retornam ao TOP 25. Mapeamentos para CWEs 'Discouraged' caíram para 5,42%.",
   "stats": [("39.080", "CVEs"), ("67%", "CNA map"), ("#1", "CWE-79")],
   "bullets": ["Priorize authZ server-side (CWE-862)", "Exija CWE Base/Variant em disclosures", "Correlacione com a matriz OWASP desta página"],
   "impact": "Maior salto: CWE-862 (+5 pos.)",
   "owasp": "A05", "cwe": "CWE-79", "url": "https://cwe.mitre.org/top25/archive/2025/2025_key_insights.html", "tag": "cwe"},
  {"date": "2025-07", "source": "IBM", "title": "Cost of a Data Breach Report 2025",
   "summary": "Custo médio global cai 9% para US$ 4,4M, mas incidentes envolvendo IA sem controles atingem 97% das organizações analisadas.",
   "body": "Organizações com IA defensiva extensiva economizam US$ 1,9M e reduzem ciclo de vida do incidente. Shadow data e terceiros continuam amplificando impacto. Logging sem alerting perpetua MTTI alto — gap direto em A09.",
   "stats": [("US$ 4,4M", "Custo médio"), ("97%", "IA sem controles"), ("US$ 1,9M", "Economia IA def.")],
   "bullets": ["SIEM + SOAR com playbooks acionáveis", "DPIA para features com GenAI", "Vendor risk em cadeia de terceiros"],
   "impact": "Gap de governança IA é novo vetor de custo",
   "owasp": "A09", "cwe": "CWE-200", "url": "https://www.ibm.com/reports/data-breach", "tag": "mercado"},
  {"date": "2025-04", "source": "Verizon", "title": "DBIR 2025 — terceiros e vulnerabilidades em alta",
   "summary": "Ameaças via terceiros dobraram no período. Intrusão em sistemas responde por 81% dos breaches analisados.",
   "body": "Exploração de vulnerabilidades conhecidas volta a crescer — reforça patch management e hardening baseline como ROI alto. Setor financeiro: 94% dos breaches envolvem web, app ou API como vetor.",
   "stats": [("2×", "Terceiros"), ("81%", "Intrusão sistema"), ("94%", "Fin. web/API")],
   "bullets": ["MFA obrigatório (FIDO2)", "SBOM + avaliação de fornecedores", "Monitoramento CTI de credenciais vazadas"],
   "impact": "Vuln explorada > zero-day na maioria dos casos",
   "owasp": "A03", "cwe": "CWE-89", "url": "https://www.verizon.com/business/resources/reports/dbir/", "tag": "mercado"},
  {"date": "2025-03", "source": "OWASP", "title": "OWASP Top 10:2025 — versão final",
   "summary": "8ª edição publicada com 2 categorias novas promovidas pela pesquisa comunitária e metodologia data-informed em 2,8M+ apps.",
   "body": "A03 Software Supply Chain Failures e A09 Logging and Alerting entram via survey — sub-representados em testes automatizados. A10 Mishandling of Exceptional Conditions é categoria inédita com 24 CWEs. SSRF consolidado em A01.",
   "stats": [("2,8M+", "Apps testadas"), ("248", "CWEs mapeadas"), ("2", "Categorias novas")],
   "bullets": ["Mapear 248 CWEs no seu stack", "Threat model supply chain (SLSA/SBOM)", "Fail-closed em authZ e error paths"],
   "impact": "A02 misconfig sobe para #2",
   "owasp": "A10", "cwe": "CWE-209", "url": "https://owasp.org/Top10/2025/", "tag": "owasp"},
  {"date": "2025-01", "source": "CISA", "title": "Snowflake — campanha MFA bypass",
   "summary": "UNC5537 explorou centenas de tenants Snowflake com credenciais sem MFA obrigatório e reutilização de senhas.",
   "body": "Ticketmaster, Santander, Advance Auto Parts entre afetados. Não houve zero-day — vetor foi credencial vazada + configuração permissiva de autenticação. Lição direta para A07 + A02 em ambientes SaaS multi-tenant.",
   "stats": [("165+", "Clientes"), ("A07", "Auth failure"), ("A02", "Misconfig")],
   "bullets": ["MFA obrigatório em todos os tenants", "Rate limit e lockout no login", "Monitoramento de credenciais em CTI"],
   "impact": "Maior campanha SaaS de 2024–2025",
   "owasp": "A07", "cwe": "CWE-306", "url": "https://www.cisa.gov/news-events/cybersecurity-advisories", "tag": "incidente"},
  {"date": "2024-12", "source": "NVD", "title": "CVE-2024-3094 — backdoor XZ Utils",
   "summary": "Backdoor inserido em liblzma após comprometimento social do maintainer solo — detectado por anomalia em sshd, não por scanner.",
   "body": "Atacante acumulou confiança por anos antes de inserir código malicioso. Afetou distros Linux mainstream. Marco definitivo de supply chain em open source — motivação direta para A03:2025 no OWASP Top 10.",
   "stats": [("3 anos", "Infiltração"), ("A03", "Supply chain"), ("CWE-829", "Dep. maliciosa")],
   "bullets": ["Pin + hash verification em deps nativas", "Revisão humana de mudanças críticas", "Proveniência SLSA nível 3+"],
   "impact": "Maior incidente supply chain OSS de 2024",
   "owasp": "A03", "cwe": "CWE-829", "url": "https://nvd.nist.gov/vuln/detail/CVE-2024-3094", "tag": "incidente"},
  {"date": "2024-10", "source": "PortSwigger", "title": "Web Security Academy — novos labs SSRF/IDOR",
   "summary": "Conteúdo 2024–2025 reforça APIs cloud-native, JWT abuse e GraphQL BOLA — alinhado a A01 como #1 em pentests manuais.",
   "body": "Pesquisa anual confirma IDOR em 94% dos apps testados. SSRF cresce com microserviços e serverless que fazem fetch de URLs. Business logic flaws em ~40% dos escopos — overlap com A06 Insecure Design.",
   "stats": [("94%", "IDOR"), ("↑", "SSRF APIs"), ("40%", "Logic flaws")],
   "bullets": ["AuthZ matrix automatizada em CI", "Block metadata IPs em fetchers", "Abuse case testing no backlog"],
   "impact": "Broken Access Control domina pentest manual",
   "owasp": "A01", "cwe": "CWE-639", "url": "https://portswigger.net/web-security", "tag": "pesquisa"},
  {"date": "2024-02", "source": "Change Healthcare", "title": "Maior breach saúde EUA — credenciais sem MFA",
   "summary": "Ransomware ALPHV/BlackCat via credencial Citrix comprometida sem MFA. Paralisou pagamentos de saúde por semanas.",
   "body": "Maior incidente do setor saúde nos EUA. Vetor inicial: credencial válida sem segundo fator em portal exposto. Impacto em cadeia: farmácias, hospitais e processamento de claims. Caso emblemático de A07 em ambientes críticos.",
   "stats": [("100M+", "Registros"), ("Semanas", "Paralisação"), ("A07", "Auth failure")],
   "bullets": ["MFA em todo acesso remoto", "Segmentação de rede para Citrix/RDP", "Backup offline testado"],
   "impact": "Maior breach healthcare EUA",
   "owasp": "A07", "cwe": "CWE-306", "url": "https://www.hhs.gov/hipaa/for-professionals/special-topics/change-healthcare-cybersecurity-incident-frequently-asked-questions/index.html", "tag": "incidente"},
  {"date": "2025-06", "source": "Oracle", "title": "Oracle Health — breach em hospitais",
   "summary": "Até 80 hospitais potencialmente impactados por falhas em integração legada e exposição de dados clínicos.",
   "body": "Ambientes healthcare combinam sistemas legados, integrações HL7/FHIR mal protegidas e superfície exposta. Correlaciona A02 (misconfig) com CWE-200 (exposure) — dados clínicos sem controles proporcionais ao risco.",
   "stats": [("80", "Hospitais"), ("A02", "Misconfig"), ("PII/PHI", "Dados")],
   "bullets": ["Inventário de integrações legadas", "Criptografia em trânsito e repouso", "Auditoria de permissões em APIs clínicas"],
   "impact": "Healthcare continua alvo de alto impacto",
   "owasp": "A02", "cwe": "CWE-200", "url": "https://www.oracle.com/security-alerts/", "tag": "incidente"},
  {"date": "2025-02", "source": "OWASP", "title": "ASVS 5.0 em desenvolvimento",
   "summary": "Nova versão do Application Security Verification Standard incorpora APIs, cloud, containers e requisitos para GenAI/LLM.",
   "body": "ASVS 5.0 expande cobertura para arquiteturas modernas: microserviços, serverless, service mesh e copilots internos. Use como checklist de verificação cruzada com cada categoria OWASP:2025 neste guia.",
   "stats": [("5.0", "Versão"), ("API", "Cobertura"), ("LLM", "Novos reqs")],
   "bullets": ["Mapear ASVS level alvo por aplicação", "Gates bloqueantes em CI por capítulo", "Security champions por squad"],
   "impact": "Checklist evolui para stack 2025+",
   "owasp": "A06", "cwe": "CWE-20", "url": "https://owasp.org/www-project-application-security-verification-standard/", "tag": "owasp"},
  {"date": "2025-05", "source": "CISA", "title": "KEV catalog — recorde de adições Q1",
   "summary": "Catálogo de vulnerabilidades exploradas ativamente cresce em ritmo recorde. Software de borda e VPN lideram entradas.",
   "body": "CWE-78 (OS Command Injection) e memory corruption dominam KEV. Prioridade de patch para CVEs listadas deve ser < 48h — antes de hardening genérico. Correlacione com o gráfico CWE↔KEV nesta página.",
   "stats": [("20", "CWE-78 KEV"), ("<48h", "SLA patch"), ("CWE", "TOP 25 overlap")],
   "bullets": ["Pipeline de patch KEV automatizado", "WAF temporário só sem patch", "Inventário de parsers nativos"],
   "impact": "Exploit in-the-wild = prioridade zero",
   "owasp": "A02", "cwe": "CWE-78", "url": "https://www.cisa.gov/known-exploited-vulnerabilities-catalog", "tag": "cwe"},
  {"date": "2024-11", "source": "IETF", "title": "OAuth 2.1 draft — simplificação PKCE",
   "summary": "Consolidação de boas práticas OAuth para SPAs, mobile e APIs — PKCE obrigatório, implicit flow removido.",
   "body": "OAuth 2.1 simplifica implementações seguras e elimina fluxos deprecados. Impacto direto em A07 (Authentication Failures) e A01 (Broken Access Control) em APIs que usam tokens sem validação rigorosa de audience e scope.",
   "stats": [("PKCE", "Obrigatório"), ("2.1", "Draft"), ("A07", "OWASP")],
   "bullets": ["Migrar implicit → authorization code + PKCE", "Validar audience e scope no resource server", "Rotacionar refresh tokens"],
   "impact": "Padrão OAuth amadurece para APIs modernas",
   "owasp": "A07", "cwe": "CWE-287", "url": "https://datatracker.ietf.org/doc/html/draft-ietf-oauth-v2-1-12", "tag": "pesquisa"},
]

BREACH_EXTRA = [
  ("2025", "Oracle Health", "Exposure", "Possível exfiltração de dados clínicos em dezenas de hospitais US. Falhas em integração legada e controles de acesso em ambientes healthcare.", "A02", "CWE-200", "80 hosp.", "Healthcare", "https://www.oracle.com/security-alerts/"),
  ("2024", "Change Healthcare", "Auth", "Credencial Citrix sem MFA → ransomware ALPHV. Maior incidente saúde US. Pagamentos e farmácias paralisados por semanas.", "A07", "CWE-306", "100M+", "No MFA", "https://www.hhs.gov/hipaa/for-professionals/special-topics/change-healthcare-cybersecurity-incident-frequently-asked-questions/index.html"),
  ("2024", "CrowdStrike outage", "Integrity", "Update de canal Fastly/Sensor com erro — indisponibilidade global. Não foi breach malicioso, mas lição em supply chain e rollout.", "A08", "CWE-754", "8,5M devices", "Bad update", "https://www.crowdstrike.com/blog/"),
  ("2023", "Okta breach cascade", "Supply Chain", "Suporte Okta comprometido → acesso a clientes downstream (1Password, BeyondTrust). Cadeia de confiança SaaS.", "A03", "CWE-200", "—", "Support breach", "https://sec.okta.com/"),
]

MARKET_2025 = [
  ("US$ 4,4M", "Custo médio breach 2025", "IBM Cost of Data Breach 2025", "https://www.ibm.com/reports/data-breach"),
  ("97%", "Incidentes IA sem controles", "IBM Cost of Data Breach 2025", "https://www.ibm.com/reports/data-breach"),
  ("US$ 1,9M", "Economia com IA defensiva", "IBM Cost of Data Breach 2025", "https://www.ibm.com/reports/data-breach"),
  ("81%", "Breaches — intrusão sistema", "Verizon DBIR 2025", "https://www.verizon.com/business/resources/reports/dbir/"),
  ("2×", "Ameaças via terceiros", "Verizon DBIR 2025", "https://www.verizon.com/business/resources/reports/dbir/"),
  ("67%", "CVEs com CNA mapping", "MITRE CWE TOP 25 2025", "https://cwe.mitre.org/top25/archive/2025/2025_key_insights.html"),
  ("53%→67%", "CNA mapping YoY", "MITRE CWE TOP 25 2025", "https://cwe.mitre.org/top25/archive/2025/2025_key_insights.html"),
  ("5,42%", "Mappings Discouraged CWE", "MITRE CWE TOP 25 2025", "https://cwe.mitre.org/top25/archive/2025/2025_key_insights.html"),
]

SOURCE_LINKS_EXTRA = [
  ("Verizon DBIR 2025", "https://www.verizon.com/business/resources/reports/dbir/", "Relatório anual"),
  ("IBM Cost of Breach 2025", "https://www.ibm.com/reports/data-breach", "Custo + IA"),
  ("OWASP LLM Top 10", "https://owasp.org/www-project-top-10-for-large-language-model-applications/", "GenAI risks"),
  ("MITRE CWE KEV Top 10", "https://cwe.mitre.org/top25/archive/2025/2025_kev_list.html", "Exploits ativos"),
  ("OWASP Top 10:2025", "https://owasp.org/Top10/2025/", "Lista oficial"),
]

# Dados para gráficos adicionais (injetados como JSON)
def chart_cwe_kev(cwe_list):
    items = [{"l": c["id"].replace("CWE-", "#"), "v": c["kev"], "id": c["id"]} for c in cwe_list if c["kev"] > 0]
    items.sort(key=lambda x: -x["v"])
    return items[:12]

def chart_owasp_prev():
    """Somente categorias com % publicado em testes automatizados (OWASP 2025)."""
    from extended_content import OWASP_PREVALENCE
    out = []
    for oid, name, prev, cwes, _note in OWASP_PREVALENCE:
        if not prev or prev in ("—", "-", ""):
            continue
        out.append({
            "l": oid,
            "name": name,
            "cwes": cwes,
            "v": float(prev.replace("%", "").replace(",", ".")),
        })
    return out

def chart_breach_vectors():
    return [
        {"l": "Credenciais", "v": 28}, {"l": "Phishing", "v": 22},
        {"l": "Vuln. explorada", "v": 18}, {"l": "Misconfig", "v": 15},
        {"l": "Malware", "v": 10}, {"l": "Outros", "v": 7},
    ]

def chart_cwe_delta(cwe_list):
    out = []
    for c in cwe_list:
        t = str(c.get("trend", "0")).strip()
        if t in ("0", "→", "N/A", "", "—"):
            continue
        if not (t.startswith("+") or t.startswith("-") or t.startswith("−")):
            continue
        sign = 1 if t.startswith("+") else -1
        try:
            delta = int(t[1:].replace("−", ""))
        except ValueError:
            continue
        rank = c["rank"]
        prev = rank + delta if sign > 0 else rank - delta
        out.append({
            "l": c["id"].replace("CWE-", "#"),
            "v": delta,
            "dir": "up" if sign > 0 else "down",
            "id": c["id"],
            "rank": rank,
            "prev": prev,
            "name_pt": c.get("name_pt", c.get("name", "")),
            "short": c["id"],
        })
    out.sort(key=lambda x: -x["v"])
    return out[:10]