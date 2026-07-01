# Conteúdo expandido por item — material de referência reutilizável em qualquer contexto

_OWASP_ATTACK = {
    "A01": "Recon → enumerar IDs/recursos → trocar chave controlada pelo usuário (basketId, orderId) → escalar para /admin ou SSRF interno → exfiltrar dados de outro tenant.",
    "A02": "Scan de superfície (headers, buckets, /.git) → misconfig expõe credencial ou log → pivot para acesso privilegiado ou vazamento em massa.",
    "A03": "Comprometer maintainer ou pipeline CI → inserir artefato malicioso → consumidores instalam update → RCE ou backdoor em escala.",
    "A04": "Tráfego TLS fraco ou hash quebrado (MD5) → offline crack ou interceptação → reutilização de credencial → acesso indevido.",
    "A05": "Parâmetro refletido ou armazenado → payload de injeção (SQL, XSS, comando) → bypass de autenticação, execução ou exfiltração de dados.",
    "A06": "Mapear fluxos de negócio → abusar ausência de rate limit, CSRF ou regras de cupom → impacto financeiro ou escalação lógica.",
    "A07": "Credencial obtida (phishing, leak, stuffing) → MFA fraco ou JWT mal validado → sessão fixada → impersonação.",
    "A08": "Input não confiável desserializado ou update sem verificação → integridade do runtime comprometida → persistência ou RCE.",
    "A09": "Ataque sem correlação em logs → ausência de alerta → detecção tardia → impacto regulatório e operacional.",
    "A10": "Condição de erro (input malformado, race, OOB) → stack trace ou fail-open → vazamento de schema/credencial ou crash/RCE.",
}

_CWE_ATTACK = {
    "CWE-79": "Dado não confiável entra no DOM → encoding inadequado ao contexto → execução de script → roubo de sessão ou skimmer.",
    "CWE-89": "Query montada por concatenação → UNION ou error-based → dump de tabelas → bypass de login ou escrita no SGBD.",
    "CWE-352": "Vítima autenticada visita página maliciosa → request forjado com cookies → ação não intencionada no servidor.",
    "CWE-862": "Operação executada sem checagem de permissão → BOLA/IDOR → leitura ou escrita de recurso alheio.",
    "CWE-787": "Input maior que o buffer → escrita fora dos limites → corrupção de memória → RCE em código nativo.",
    "CWE-22": "Sequências ../ em path → sem canonicalização → leitura de arquivos sensíveis fora do diretório permitido.",
    "CWE-416": "Uso de ponteiro após free → heap grooming → execução arbitrária em browser, kernel ou runtime nativo.",
    "CWE-125": "Leitura além do buffer → vazamento de memória adjacente → tokens, chaves ou ponteiros para exploit chain.",
    "CWE-78": "Metacaracteres de shell em input → execução de comando do SO → id, reverse shell ou pivot.",
    "CWE-94": "eval, OGNL ou template com input → código executado no runtime da aplicação → RCE lógico.",
    "CWE-120": "Cópia sem verificação de tamanho → overflow clássico → controle de fluxo ou execução.",
    "CWE-434": "Upload sem validação rigorosa → webshell ou polyglot → RCE no servidor web.",
    "CWE-476": "Desreferência de NULL → crash (DoS) ou caminho de erro que deixa estado inconsistente.",
    "CWE-121": "Overflow na pilha → sobrescrever endereço de retorno → ROP ou shellcode (cenários avançados).",
    "CWE-502": "Objeto de fonte não confiável desserializado → gadget chain → RCE em Java, .NET, Node, Python etc.",
    "CWE-122": "Overflow no heap → corrupção de metadata → arbitrary write → controle de execução.",
    "CWE-863": "Lógica de autorização incorreta → usuário comum executa ação restrita apesar de existir checagem.",
    "CWE-20": "Validação ausente, só no client ou por blacklist → tipos/ranges incorretos → injeção ou abuso de lógica.",
    "CWE-284": "Política de acesso ampla ou ausente → ator não autorizado acessa recurso em cloud, API ou mesh.",
    "CWE-200": "Resposta, log, backup ou métrica expõe dado sensível → recon ampliado → breach maior.",
    "CWE-306": "Função crítica sem autenticação → /admin, /debug ou Swagger exposto → acesso anônimo.",
    "CWE-918": "URL controlada pelo atacante → fetch no servidor → metadata cloud ou serviço interno.",
    "CWE-77": "Input em interpreter de comando (CI, SNMP, DSL) → execução fora do shell HTTP clássico.",
    "CWE-639": "ID no path/body sem vínculo ao token → recurso de outro usuário acessível.",
    "CWE-770": "Sem throttling → brute force, flood ou chamadas caras ilimitadas → DoS ou abuso econômico.",
}

_OWASP_ROOT = {
    "A01": ["Confiar que login implica permissão em todo endpoint", "IDs sequenciais ou previsíveis em APIs REST", "Autorização só no frontend ou em gateway genérico", "Ausência de testes por matriz role × recurso × ação"],
    "A02": ["Defaults inseguros em cloud, K8s e frameworks", "Headers de segurança não configurados", "Secrets em repositório ou ConfigMap", "Superfície de admin/debug exposta em produção"],
    "A03": ["Dependências sem inventário (SBOM) ou pin de versão", "Pipeline CI com permissões excessivas", "Artefatos sem assinatura ou proveniência", "Confiança cega em pacotes npm/PyPI sem auditoria"],
    "A04": ["Algoritmos obsoletos (MD5, SHA1, DES)", "TLS legado ou certificados mal gerenciados", "Secrets hardcoded ou em logs", "JWT sem validação de algoritmo, audience e expiração"],
    "A05": ["Concatenação de SQL ou comandos de shell", "Encoding único para todos os contextos HTML/JS/URL", "ORM com raw queries em input do usuário", "Confiança em WAF sem correção na origem"],
    "A06": ["Backlog sem abuse cases ou threat modeling", "Mutações state-changing sem anti-CSRF", "CAPTCHA ou rate limit só no client", "Regras de negócio não validadas server-side"],
    "A07": ["Política de senha fraca ou hashing rápido", "MFA opcional ou implementação TOTP frágil", "Sessão não rotacionada após login", "OAuth/OIDC com fluxos deprecados"],
    "A08": ["Desserialização de input externo", "Updates sem verificação de assinatura", "CDN sem Subresource Integrity", "Integridade entre microsserviços assumida por rede interna"],
    "A09": ["Logs sem estrutura, retenção ou proteção", "Tokens e PII gravados em claro", "SIEM sem regras acionáveis", "Ausência de runbooks ligados a alertas"],
    "A10": ["Stack traces e queries em respostas 500", "Fail-open quando authZ ou validação falha", "Código nativo sem sanitizers/fuzzing", "Race conditions e estados parciais após timeout"],
}

_CWE_REFLECTION = {
    "A01": ["Por que autenticação forte não elimina IDOR?", "Como derivar identidade do token em vez do body/path?", "Diferença entre BOLA e BFLA em APIs REST."],
    "A05": ["Prepared statements resolvem todos os cenários de SQLi?", "Por que CSP não substitui output encoding?", "Quando um ORM ainda é vulnerável?"],
    "CWE-79": ["Quais contextos de saída exigem encoding diferente?", "DOM XSS em SPA: onde fica o sink?", "Como CSP nonce interage com SSR?"],
    "CWE-89": ["ORDER BY dinâmico pode ser seguro?", "O que é second-order SQLi?", "Qual privilégio mínimo para o usuário do banco?"],
}


def _root_causes(item_id, variant, item):
    if variant == "owasp":
        return _OWASP_ROOT.get(item_id, [
            "Validação ou controle aplicado tarde no ciclo de desenvolvimento",
            "Assumir que framework ou cloud 'já resolve' o risco",
            "Falta de testes de segurança específicos para esta categoria",
        ])
    return [
        "Entrada ou estado não validado na fronteira de confiança",
        "Reuso de código legado em caminhos expostos à web",
        "Controles genéricos que não cobrem esta fraqueza específica",
    ]


def _reflection(item_id, variant, item):
    if variant == "owasp":
        base = _CWE_REFLECTION.get(item_id, [
            f"Onde {item['pt']} costuma aparecer em APIs e microsserviços?",
            "Qual CWE correlata tem maior impacto no seu stack?",
            "Qual controle preventivo tem melhor custo-benefício?",
        ])
    else:
        base = _CWE_REFLECTION.get(item_id, [
            f"Como {item['name_pt']} aparece em código moderno (Node, Java, Go)?",
            f"O que o score {item['score']} do TOP 25 indica em termos de prevalência?",
            "Detecção estática vs dinâmica: qual falha primeiro?",
        ])
    return base[:4]


def _takeaways(item, variant):
    if variant == "owasp":
        prev = item.get("prev", [])[:3]
        return [
            item["p"][0][:180] + ("…" if len(item["p"][0]) > 180 else ""),
            f"CWEs centrais: {', '.join(item['cwes'][:4])}",
            item.get("diff", ""),
        ] + prev
    mit = item.get("mit", [])[:3]
    kev = f"{item['kev']} CVE(s) no CISA KEV — priorizar patch." if item.get("kev") else ""
    out = [
        item["p"][0][:180] + ("…" if len(item["p"][0]) > 180 else ""),
        f"Rank #{item['rank']} · score MITRE {item['score']}",
        f"OWASP: {', '.join(item['owasp'])}",
    ]
    if kev:
        out.append(kev)
    return out + mit


def _practice_owasp(o):
    labs = o.get("juice", [])
    out = []
    if labs:
        out.append(f"Juice Shop: challenges ligados a {', '.join(labs[:3])}{'…' if len(labs) > 3 else ''}")
    out.append(f"Simulador interativo: sim-box-{o['id'].lower()}")
    out.append("Cofre de Código: compare o mesmo antipadrão em Python, Java, Node e Go")
    if o.get("test"):
        out.append(f"Guia de testes: {o['test'][0]}")
    return out


def _practice_cwe(c):
    out = []
    if c.get("juice"):
        out.append(f"Juice Shop: lab {c['juice']}")
    out.append(f"Simulador: sim-box-c{c['id'].replace('CWE-', '')}")
    if c.get("tools"):
        out.append(f"Ferramentas sugeridas: {', '.join(c['tools'][:4])}")
    out.append(f"Definição oficial MITRE: {c['id']}")
    return out


def _concept_blocks(paragraphs):
    labels = ("Visão geral", "Contexto técnico", "Impacto e prevalência", "Ecossistema e labs")
    out = []
    for i, p in enumerate(paragraphs):
        lbl = labels[i] if i < len(labels) else f"Detalhe {i + 1}"
        out.append({"title": lbl, "body": p})
    return out


def build_owasp_lesson(o):
    return {
        "summary": o["p"][0],
        "concepts": _concept_blocks(o["p"]),
        "attack_chain": _OWASP_ATTACK.get(o["id"], f"Exploração típica de {o['pt']} com impacto em confidencialidade, integridade ou disponibilidade."),
        "root_causes": _root_causes(o["id"], "owasp", o),
        "detection": o.get("det", []) + [f"WSTG: {t}" for t in o.get("test", [])],
        "mitigation": o.get("prev", []),
        "asvs": o.get("asvs", []),
        "cases": o.get("cases", []),
        "refs": o.get("refs", []),
        "cwes": o.get("cwes", []),
        "diff": o.get("diff", ""),
        "reflection": _reflection(o["id"], "owasp", o),
        "takeaways": _takeaways(o, "owasp"),
        "practice": _practice_owasp(o),
    }


def build_cwe_lesson(c):
    meta = []
    if c.get("kev"):
        meta.append(f"{c['kev']} entradas no CISA KEV (exploração ativa)")
    if c.get("trend") and str(c["trend"]) not in ("0", "→", "N/A", "", "—"):
        meta.append(f"Tendência vs 2024: {c['trend']}")
    return {
        "summary": c["p"][0],
        "concepts": _concept_blocks(c["p"]),
        "attack_chain": _CWE_ATTACK.get(c["id"], f"Cadeia de ataque comum para {c['id']} em aplicações web."),
        "root_causes": _root_causes(c["id"], "cwe", c),
        "detection": c.get("det", []),
        "mitigation": c.get("mit", []),
        "tools": c.get("tools", []),
        "cases": c.get("cases", []),
        "refs": c.get("refs", []),
        "owasp": c.get("owasp", []),
        "rank": c.get("rank"),
        "score": c.get("score"),
        "meta": meta,
        "reflection": _reflection(c["id"], "cwe", c),
        "takeaways": _takeaways(c, "cwe"),
        "practice": _practice_cwe(c),
    }


def build_all_lesson_plans(owasp_list, cwe_list):
    return {
        **{o["id"]: build_owasp_lesson(o) for o in owasp_list},
        **{c["id"]: build_cwe_lesson(c) for c in cwe_list},
    }