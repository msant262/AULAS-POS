# Render functions
import re

_RICH_PATTERNS = (
    (r"CWE-\d+", "cwe"),
    (r"A0\d", "owasp"),
    (r"routes/[\w./-]+\.ts", "path"),
    (r"lib/[\w./-]+\.ts", "path"),
    (r"/admin", "path"),
    (r"\d+,\d+%", "stat"),
    (r"\d+,\d+M\+", "stat"),
    (r"Juice Shop", "juice"),
    (r"OWASP Top 10:?\d{0,4}", "owasp"),
    (r"\b(IDOR|BOLA|SSRF|XSS|SQLi|CSRF|RCE|LFI|RFI)\b", "attack"),
    (r"WSTG-[A-Z0-9-]+", "wstg"),
    (r"\bASVS\b", "asvs"),
    (r"MITRE", "cwe"),
    (r"DBIR", "stat"),
)


def format_rich_text(text):
    out = esc(str(text))
    for pat, kind in _RICH_PATTERNS:
        out = re.sub(
            rf"({pat})",
            rf'<mark class="modal-hl {kind}">\1</mark>',
            out,
        )
    return out


_HL_TYPE_META = {
    "highlight": ("💡", "Destaque", "hl-highlight"),
    "caso": ("📰", "Caso famoso", "hl-caso"),
    "aprendizado": ("✓", "Aprendizado", "hl-aprendizado"),
    "pos": ("🎓", "Discussão", "hl-pos"),
    "quote": ("❝", "Citação", "hl-quote"),
    "excerpt": ("📄", "Trecho da matéria", "hl-excerpt"),
    "mencao": ("📌", "Menção · referência", "hl-mencao"),
}


def _hl_matches(h, section=None, owasp=None, cwe=None, types=None):
    if section and section not in h.get("sections", []):
        return False
    if owasp and h.get("owasp") != owasp:
        return False
    if cwe and h.get("cwe") != cwe:
        return False
    if types and h.get("type") not in types:
        return False
    return True


def _course_highlights():
    return globals().get("COURSE_HIGHLIGHTS", [])


def _hl_detail_html(h):
    detail = h.get("detail")
    if not detail:
        return ""
    paras = detail if isinstance(detail, list) else [detail]
    rows = "".join(f"<p>{format_rich_text(p)}</p>" for p in paras if p)
    return f'<div class="hl-detail">{rows}</div>' if rows else ""


def _hl_bullets_html(h):
    bullets = h.get("bullets") or []
    if not bullets:
        return ""
    rows = "".join(f"<li>{format_rich_text(b)}</li>" for b in bullets)
    return f'<div class="hl-bullets-wrap"><span class="hl-bullets-k">Na prática</span><ul class="hl-bullets">{rows}</ul></div>'


def _hl_stats_html(h):
    stats = h.get("stats") or []
    if not stats:
        return ""
    chips = "".join(
        f'<div class="hl-stat"><span class="hl-stat-val">{esc(s[0])}</span>'
        f'<span class="hl-stat-lbl">{esc(s[1])}</span></div>'
        for s in stats
    )
    return f'<div class="hl-stats">{chips}</div>'


def render_highlight_block(h, compact=False):
    ico, lbl, cls = _HL_TYPE_META.get(h.get("type", "highlight"), ("•", "Destaque", "hl-highlight"))
    takeaway = h.get("takeaway", "")
    link = h.get("link")
    tags = []
    if h.get("owasp"):
        tags.append(
            f'<button type="button" class="ok-badge accent pill hl-tag corr-chip" '
            f'data-owasp="{esc(h["owasp"])}" data-cwe="{esc(h.get("cwe", ""))}">{esc(h["owasp"])}</button>'
        )
    if h.get("cwe"):
        tags.append(
            f'<button type="button" class="ok-badge cyan pill hl-tag corr-chip" '
            f'data-owasp="{esc(h.get("owasp", ""))}" data-cwe="{esc(h["cwe"])}">{esc(h["cwe"])}</button>'
        )
    tag_row = f'<div class="hl-tags">{"".join(tags)}</div>' if tags else ""
    takeaway_html = (
        f'<footer class="hl-takeaway"><span class="hl-takeaway-k">Ponto-chave</span>'
        f'<p>{format_rich_text(takeaway)}</p></footer>'
        if takeaway else ""
    )
    link_html = (
        f'<a class="hl-source-link" href="{esc(link)}" target="_blank" rel="noopener">'
        f'<span class="hl-source-name">{esc(h.get("source", "Fonte"))}</span><span class="hl-source-ico">↗</span></a>'
        if link
        else f'<span class="hl-source-link muted"><span class="hl-source-name">{esc(h.get("source", ""))}</span></span>'
    )
    why_html = (
        f'<div class="hl-why"><span class="hl-why-k">Por que importa</span>'
        f'<p>{format_rich_text(h["why"])}</p></div>'
        if h.get("why") else ""
    )
    excerpt = h.get("excerpt", "")
    if h.get("type") == "quote":
        lede_html = f'<blockquote class="hl-quote-text">{format_rich_text(excerpt)}</blockquote>'
    elif h.get("type") == "mencao" and h.get("author"):
        lede_html = (
            f'<p class="hl-lede hl-mencao-lede">{format_rich_text(excerpt)}</p>'
            f'<cite class="hl-mencao-author">— {esc(h["author"])}</cite>'
        )
    else:
        lede_html = f'<p class="hl-lede">{format_rich_text(excerpt)}</p>'
    compact_cls = " hl-compact" if compact else ""
    owasp_attr = f' data-owasp="{esc(h["owasp"])}"' if h.get("owasp") else ""
    cwe_attr = f' data-cwe="{esc(h["cwe"])}"' if h.get("cwe") else ""
    return f'''<article class="hl-block {cls}{compact_cls}" data-hl-type="{esc(h.get("type", ""))}"{owasp_attr}{cwe_attr} id="hl-{esc(h["id"])}">
      <header class="hl-hd">
        <div class="hl-hd-top">
          <span class="hl-kicker"><span class="hl-ico" aria-hidden="true">{ico}</span>{lbl}</span>
          {link_html}
        </div>
        {tag_row}
        <h4 class="hl-title">{esc(h.get("title", ""))}</h4>
      </header>
      <div class="hl-body">
        {lede_html}
        {_hl_detail_html(h)}
        {_hl_stats_html(h)}
        {_hl_bullets_html(h)}
        {why_html}
      </div>
      {takeaway_html}
    </article>'''


def _hl_even_chunk(items, offset=0, limit=None):
    """Retorna fatia com contagem par — nunca 2+1 órfão."""
    chunk = items[offset:]
    if limit is not None:
        chunk = chunk[:limit]
    if len(chunk) % 2 == 1:
        chunk = chunk[:-1]
    return chunk


def render_section_highlights(section, limit=None, layout="stack", title=None, subtitle=None, offset=0):
    items = [h for h in _course_highlights() if _hl_matches(h, section=section)]
    if not items:
        return ""
    if layout == "grid":
        items = _hl_even_chunk(items, offset=offset, limit=limit)
    elif offset or limit is not None:
        items = items[offset:(offset + limit) if limit is not None else None]
        if limit is not None:
            items = items[:limit]
    elif limit:
        items = items[:limit]
    if not items:
        return ""
    blocks = "".join(render_highlight_block(h) for h in items)
    if layout == "grid":
        single_cls = " hl-grid-single" if len(items) == 1 else ""
        layout_cls = f"hl-grid{single_cls}"
    else:
        layout_cls = "hl-stack"
    hdr = ""
    if title:
        sub = f'<span class="hl-rail-sub">{esc(subtitle)}</span>' if subtitle else ""
        hdr = f'<div class="hl-rail-hd"><span class="section-label">{esc(title)}</span>{sub}</div>'
    return f'<div class="hl-rail">{hdr}<div class="hl-section {layout_cls}" data-hl-section="{esc(section)}">{blocks}</div></div>'


def render_section_highlight_rails(section, title=None, subtitle=None, items_per_rail=2):
    """Vários rails de 2 cards — espalha matérias dentro da mesma seção."""
    items = [h for h in _course_highlights() if _hl_matches(h, section=section)]
    if len(items) % 2 == 1:
        items = items[:-1]
    if not items:
        return ""
    rails = []
    for i in range(0, len(items), items_per_rail):
        chunk = items[i:i + items_per_rail]
        if len(chunk) < 2:
            break
        blocks = "".join(render_highlight_block(h) for h in chunk)
        rail_title = title if i == 0 else None
        rail_sub = subtitle if i == 0 else None
        hdr = ""
        if rail_title:
            sub = f'<span class="hl-rail-sub">{esc(rail_sub)}</span>' if rail_sub else ""
            hdr = f'<div class="hl-rail-hd"><span class="section-label">{esc(rail_title)}</span>{sub}</div>'
        rails.append(
            f'<div class="hl-rail hl-rail-spread">{hdr}'
            f'<div class="hl-section hl-grid" data-hl-section="{esc(section)}">{blocks}</div></div>'
        )
    return "".join(rails)


def render_owasp_highlights(owasp_id, types=None, compact=False):
    items = [
        h for h in _course_highlights()
        if _hl_matches(h, section="owasp-modal", owasp=owasp_id, types=types)
    ]
    if not items:
        return ""
    blocks = "".join(render_highlight_block(h, compact=compact) for h in items)
    return f'<div class="hl-modal-stack">{blocks}</div>'


def render_cwe_highlights(cwe_id, types=None, compact=False):
    items = [
        h for h in _course_highlights()
        if _hl_matches(h, section="cwe-modal", cwe=cwe_id, types=types)
    ]
    if not items:
        return ""
    blocks = "".join(render_highlight_block(h, compact=compact) for h in items)
    return f'<div class="hl-modal-stack">{blocks}</div>'


def render_modal_prose(paragraphs):
    blocks = []
    for i, p in enumerate(paragraphs):
        rich = format_rich_text(p)
        if i == 0:
            blocks.append(f'<div class="modal-lead"><p>{rich}</p></div>')
        elif re.search(r"Juice Shop|routes/|lib/", p, re.I):
            blocks.append(
                f'<aside class="modal-callout juice"><span class="modal-callout-kicker">🧃 Lab prático</span><p>{rich}</p></aside>'
            )
        elif re.search(r"\d+,\d+%|\d+M\+|dados oficiais|OWASP 2025|score MITRE", p, re.I):
            blocks.append(
                f'<aside class="modal-callout stat"><span class="modal-callout-kicker">📊 Prevalência</span><p>{rich}</p></aside>'
            )
        else:
            blocks.append(f'<article class="modal-prose-card"><p>{rich}</p></article>')
    return '<div class="modal-prose-flow">' + "".join(blocks) + "</div>"


def render_modal_bullets(items, icon="→"):
    if not items:
        return '<p class="muted">Sem itens nesta seção.</p>'
    rows = "".join(
        f'<li><span class="modal-li-ico" aria-hidden="true">{icon}</span><span>{format_rich_text(x)}</span></li>'
        for x in items
    )
    return f'<ul class="modal-bullet-list">{rows}</ul>'


def render_modal_tech_grid(det, test, asvs):
    return f'''<div class="modal-tech-grid">
      <section class="modal-tech-card detect">
        <header class="modal-tech-hd"><span class="modal-tech-ico">◎</span><span class="section-label">Detecção</span></header>
        {render_modal_bullets(det, "◈")}
      </section>
      <section class="modal-tech-card test">
        <header class="modal-tech-hd"><span class="modal-tech-ico">⚡</span><span class="section-label">Testes WSTG</span></header>
        {render_modal_bullets(test, "▸")}
      </section>
      <section class="modal-tech-card asvs">
        <header class="modal-tech-hd"><span class="modal-tech-ico">✓</span><span class="section-label">ASVS</span></header>
        {render_modal_bullets(asvs, "◇")}
      </section>
    </div>'''


def render_modal_mitiga(items, refs):
    checks = "".join(
        f'<li><label class="modal-check"><input type="checkbox"/><span class="modal-check-box"></span><span class="modal-check-txt">{format_rich_text(x)}</span></label></li>'
        for x in items
    )
    ref_rows = "".join(
        f'<li><a href="{esc(r[1])}" target="_blank" rel="noopener"><span class="modal-ref-ico">↗</span>{esc(r[0])}</a></li>'
        for r in refs
    )
    return f'''<div class="modal-mitiga-wrap">
      <section class="modal-mitiga-card">
        <span class="section-label">Checklist de controles</span>
        <p class="modal-mitiga-hint">Marque cada controle ao revisar o design ou o código da aplicação.</p>
        <ul class="modal-checklist">{checks}</ul>
      </section>
      <section class="modal-mitiga-card refs">
        <span class="section-label">Referências</span>
        <ul class="modal-ref-list">{ref_rows}</ul>
      </section>
    </div>'''


def modal_tab_btn(key, label, active=False, count=None):
    act = " active" if active else ""
    badge = f'<span class="modal-tab-count">{count}</span>' if count else ""
    return f'<button class="ok-tab modal-tab{act}" data-tab="{key}" type="button">{label}{badge}</button>'


def _lesson_plans():
    return globals().get("LESSON_PLANS", {})


def _info_cases_html(cases):
    if not cases:
        return ""
    rows = []
    for cs in cases:
        year = esc(cs[0]) if len(cs) > 0 else ""
        impact = esc(cs[1]) if len(cs) > 1 else ""
        desc = format_rich_text(cs[2]) if len(cs) > 2 else ""
        extra = f'<span class="info-case-extra">{format_rich_text(cs[3])}</span>' if len(cs) > 3 else ""
        rows.append(
            f'<li class="info-case-item"><span class="info-case-who">{year}</span>'
            f'<div class="info-case-body"><strong>{impact}</strong>'
            f'<p>{desc}</p>{extra}</div></li>'
        )
    return f'<ul class="info-case-list">{"".join(rows)}</ul>'


def render_lesson_plan(plan, item_id, variant="owasp", code_html=""):
    if not plan:
        return '<p class="muted">Material em preparação.</p>'
    summary = format_rich_text(plan.get("summary", ""))
    concepts = "".join(
        f'<article class="info-concept-card"><h4>{esc(c["title"])}</h4><p>{format_rich_text(c["body"])}</p></article>'
        for c in plan.get("concepts", [])
    )
    attack = plan.get("attack_chain", "")
    attack_html = (
        f'<section class="info-panel-sec info-attack"><span class="section-label">Como o ataque funciona</span>'
        f'<p>{format_rich_text(attack)}</p></section>'
        if attack else ""
    )
    roots = "".join(f"<li>{format_rich_text(r)}</li>" for r in plan.get("root_causes", []))
    detection = render_modal_bullets(plan.get("detection", []), "◈")
    mitigation = "".join(
        f'<li><label class="modal-check"><input type="checkbox"/><span class="modal-check-box"></span>'
        f'<span class="modal-check-txt">{format_rich_text(m)}</span></label></li>'
        for m in plan.get("mitigation", [])
    )
    takeaways = "".join(f"<li>{format_rich_text(t)}</li>" for t in plan.get("takeaways", []))
    reflection = "".join(f"<li>{format_rich_text(q)}</li>" for q in plan.get("reflection", []))
    practice = "".join(f"<li>{format_rich_text(p)}</li>" for p in plan.get("practice", []))
    cases_html = _info_cases_html(plan.get("cases", []))
    refs = "".join(
        f'<li><a href="{esc(r[1])}" target="_blank" rel="noopener"><span class="modal-ref-ico">↗</span>{esc(r[0])}</a></li>'
        for r in plan.get("refs", [])
    )
    asvs = render_modal_bullets(plan.get("asvs", []), "◇")
    tools = plan.get("tools", [])
    tools_html = (
        '<div class="tag-row modal-tag-row">'
        + "".join(f'<span class="ok-badge pill modal-tool-chip">{esc(t)}</span>' for t in tools)
        + "</div>"
        if tools else ""
    )
    meta_chips = ""
    if variant == "owasp":
        diff = plan.get("diff", "")
        diff_html = (
            f'<p class="info-meta-diff"><span class="modal-diff-pill">vs 2021</span>{format_rich_text(diff)}</p>'
            if diff else ""
        )
        cwes = "".join(f'<span class="ok-badge cyan pill">{esc(c)}</span> ' for c in plan.get("cwes", []))
        meta_chips = f'<div class="info-meta-chips">{cwes}</div>{diff_html}'
    else:
        rank = plan.get("rank", "")
        score = plan.get("score", "")
        meta_lines = "".join(f'<span class="ok-badge pill">{format_rich_text(m)}</span> ' for m in plan.get("meta", []))
        owasp = "".join(f'<span class="ok-badge accent pill">{esc(a)}</span> ' for a in plan.get("owasp", []))
        meta_chips = (
            f'<div class="info-meta-chips">'
            f'<span class="ok-badge accent">#{rank:02d}</span> '
            f'<span class="ok-badge cyan">score {score}</span> {meta_lines}{owasp}</div>'
        )
    sim_kind = item_id.lower() if variant == "owasp" else "c" + item_id.replace("CWE-", "")
    sim_cls = "owasp-open-sim" if variant == "owasp" else "cwe-open-sim"
    juice_html = ""
    if variant == "owasp":
        owasp_o = next((x for x in OWASP_LIST if x["id"] == item_id), None)
        if owasp_o:
            juice_html = "".join(render_juice_block(k) for k in owasp_o.get("juice", []))
    else:
        cwe_c = next((x for x in CWE_TOP25_FULL if x["id"] == item_id), None)
        if cwe_c and cwe_c.get("juice"):
            juice_html = render_juice_block(cwe_c["juice"])
    return f'''<div class="info-guide-wrap" data-guide="{esc(item_id)}">
  <header class="info-guide-hd">
    <p class="info-guide-summary">{summary}</p>
    {meta_chips}
  </header>
  <section class="info-panel-sec info-takeaways">
    <span class="section-label">Pontos-chave</span>
    <ul class="info-takeaway-list">{takeaways}</ul>
  </section>
  <section class="info-panel-sec">
    <span class="section-label">Conceitos</span>
    <div class="info-concepts-grid">{concepts}</div>
  </section>
  {attack_html}
  <section class="info-panel-sec">
    <span class="section-label">Causas raiz frequentes</span>
    <ul class="info-bullet-list">{roots}</ul>
  </section>
  {"<section class='info-panel-sec'><span class='section-label'>Exemplos de código · vulnerável → correção</span><div class='pattern-stack info-code-stack'>" + code_html + "</div></section>" if code_html.strip() else ""}
  {("<section class='info-panel-sec'><span class='section-label'>Juice Shop · código real</span><div class='lab-stack'>" + juice_html + "</div></section>") if juice_html.strip() else ""}
  {"<section class='info-panel-sec'><span class='section-label'>Incidentes documentados</span>" + cases_html + "</section>" if cases_html else ""}
  <div class="info-panel-cols">
    <section class="info-panel-sec">
      <span class="section-label">Como detectar</span>
      {detection}
    </section>
    <section class="info-panel-sec">
      <span class="section-label">Ferramentas</span>
      {tools_html if tools_html else '<p class="muted">Ver aba Técnico / Detecção.</p>'}
    </section>
  </div>
  <section class="info-panel-sec">
    <span class="section-label">Como mitigar</span>
    <p class="info-mitiga-hint">Checklist de controles — marque ao revisar código ou arquitetura.</p>
    <ul class="modal-checklist">{mitigation}</ul>
  </section>
  {"<section class='info-panel-sec'><span class='section-label'>ASVS · requisitos de verificação</span>" + asvs + "</section>" if asvs else ""}
  <section class="info-panel-sec info-practice">
    <span class="section-label">Prática recomendada</span>
    <ul class="info-practice-list">{practice}</ul>
    <button type="button" class="ok-btn sm cyan {sim_cls}" data-sim-box="sim-box-{sim_kind}">Abrir simulador</button>
  </section>
  <section class="info-panel-sec">
    <span class="section-label">Para refletir</span>
    <ul class="info-reflection-list">{reflection}</ul>
  </section>
  {"<section class='info-panel-sec'><span class='section-label'>Referências</span><ul class='modal-ref-list'>" + refs + "</ul></section>" if refs else ""}
</div>'''


def render_juice_block(key):
    if not key or key not in JUICE:
        return ''
    j = JUICE[key]
    steps = "".join(f"<li>{esc(s)}</li>" for s in j["steps"])
    return f'''
    <article class="juice-lab lab-panel" data-juice="{esc(key)}">
      <header class="lab-panel-hd">
        <span class="lab-file">{esc(j["file"])} · L{j["line"]}</span>
        <h4>{esc(j["challenge"])}</h4>
      </header>
      <div class="code-wrap diff-wrap">
        <div class="code-toolbar">
          <button type="button" class="ok-btn sm cyan code-toggle solid" data-show="vuln">Vulnerável</button>
          <button type="button" class="ok-btn sm ghost code-toggle" data-show="fix">Correção</button>
          <span class="diff-label">Vulnerável</span>
          <input type="range" class="diff-slider" min="0" max="100" value="0" aria-label="Comparar código"/>
          <button type="button" class="ok-btn sm ghost" data-juice-ide="{esc(key)}">Abrir na IDE →</button>
          <a class="ok-btn sm ghost" href="https://github.com/juice-shop/juice-shop/blob/master/{esc(j["file"])}" target="_blank" rel="noopener">GitHub →</a>
        </div>
        <div class="diff-panels">
          <pre class="code-panel vuln active"><code>{esc(j["code"])}</code></pre>
          <pre class="code-panel fix"><code>{esc(j["fix"])}</code></pre>
        </div>
      </div>
      {"<p class='payload-hint'>Payload: <code>"+esc(j.get("payload",""))+"</code></p>" if j.get("payload") else ""}
      <ol class="lab-steps">{steps}</ol>
    </article>'''

def render_pattern_block(p, mode="detail"):
    if mode == "list":
        return f'''<button type="button" class="vault-item" data-pattern="{p["id"]}" data-owasp="{p["owasp"]}" data-cwe="{p["cwe"]}">
          <span class="vault-item-id">{p["owasp"]} · {p["cwe"]}</span>
          <strong>{esc(p["title"])}</strong>
          <span class="vault-item-lang">{esc(p["lang"])}</span>
        </button>'''
    wrap_cls = "pattern-inline" if mode == "inline" else "pattern-detail"
    return f'''
    <div class="{wrap_cls}" data-pattern-id="{p["id"]}">
      <header class="pattern-detail-hd">
        <span class="ok-badge accent">{p["owasp"]}</span>
        <span class="ok-badge cyan">{p["cwe"]}</span>
        <span class="ok-badge pill">{esc(p["lang"])}</span>
        <h3>{esc(p["title"])}</h3>
        <p>{esc(p["note"])}</p>
      </header>
      <div class="code-wrap diff-wrap">
        <div class="code-toolbar">
          <button type="button" class="ok-btn sm cyan code-toggle solid" data-show="vuln">Vulnerável</button>
          <button type="button" class="ok-btn sm ghost code-toggle" data-show="fix">Correção</button>
          <input type="range" class="diff-slider" min="0" max="100" value="0" aria-label="Comparar"/>
        </div>
        <div class="diff-panels tall">
          <pre class="code-panel vuln active"><code>{esc(p["vuln"])}</code></pre>
          <pre class="code-panel fix"><code>{esc(p["fix"])}</code></pre>
        </div>
      </div>
    </div>'''

def render_terminal_mini(lab_id, lab):
    cmds = "".join(
        f'<button type="button" class="ok-btn ghost sm term-embed-cmd" data-term="{lab_id}" data-cmd="{esc(c)}">{esc(c[:36])}{"…" if len(c)>36 else ""}</button> '
        for c in list(lab["cmds"].keys())[:6] if c != "help")
    welcome = esc(lab["welcome"].split(chr(10))[0])
    return f'''
    <div class="term-embed" data-term-id="{lab_id}">
      <header class="term-embed-hd"><span class="section-label">{esc(lab["title"])}</span>
        <a class="ok-btn ghost sm" href="#terminal-lab" data-scroll="terminal-lab">Lab completo →</a></header>
      <div class="term-embed-out" id="term-embed-{lab_id}"><div class="line out dim">{welcome}</div></div>
      <div class="term-cmd-row">{cmds}</div>
    </div>'''

def render_terminal_full():
    tabs = "".join(
        f'<button type="button" class="ok-tab term-tab{" active" if i==0 else ""}" data-term-tab="{tid}">{esc(lab["title"])}</button>'
        for i, (tid, lab) in enumerate(TERMINAL_LABS.items()))
    panels = ""
    for i, (tid, lab) in enumerate(TERMINAL_LABS.items()):
        cmd_btns = "".join(
            f'<button type="button" class="ok-btn sm ghost term-cmd" data-term="{tid}" data-cmd="{esc(c)}">{esc(c[:44])}{"…" if len(c)>44 else ""}</button> '
            for c in lab["cmds"] if c != "help")
        demo = next((c for c in lab["cmds"] if c != "help"), "help")
        panels += f'''
        <div class="term-panel{" active" if i==0 else ""}" data-term-panel="{tid}" data-term-demo="{esc(demo)}">
          <div class="ok-terminal interactive-term" data-term="{tid}">
            <div class="topbar"><span class="dots"><span></span><span></span><span></span></span><span>{esc(lab["title"])}</span>
              <span class="ok-badge pill">{lab.get("owasp","")} · {lab.get("cwe","")}</span>
              <button type="button" class="ok-btn ghost sm term-demo" data-term="{tid}">▶ Demo</button>
              <button type="button" class="ok-btn ghost sm term-clear" data-term="{tid}">clear</button></div>
            <div class="body term-output" id="term-out-{tid}"><div class="line out dim">{esc(lab["welcome"])}</div></div>
            <div class="term-cmd-palette">{cmd_btns}</div>
            <div class="term-input-row">
              <span class="prompt">$</span>
              <input class="ok-input term-input" data-term="{tid}" placeholder="Ou clique nos comandos acima…" autocomplete="off" spellcheck="false"/>
            </div>
          </div>
        </div>'''
    return f'<div class="ok-tabs term-tabs">{tabs}</div>{panels}'

def render_chart_box(canvas_id, title, legend="", height=220, hint=True, extra_class="", donut=False, ranked=False, guide="", takeaway="", delta_key=False, delta=False):
    sub_html = f'<p class="chart-sub">{esc(legend)}</p>' if legend else ''
    guide_html = f'<p class="chart-guide"><strong>Como ler:</strong> {esc(guide)}</p>' if guide else ''
    takeaway_html = f'<p class="chart-takeaway">{esc(takeaway)}</p>' if takeaway else ''
    delta_key_html = '''<div class="chart-delta-key" aria-hidden="true">
    <span class="delta-key up">↑ Subiu — ficou mais crítica</span>
    <span class="delta-key mid">| ranking 2024</span>
    <span class="delta-key down">↓ Desceu — menos crítica</span>
  </div>''' if delta_key else ''
    hint_html = '<p class="chart-hint"><span class="chart-hint-ico" aria-hidden="true">↗</span> Interativo — passe o mouse ou clique na legenda</p>' if hint else ''
    meta_html = guide_html + takeaway_html
    if donut:
        cls = f"chart-box chart-embed chart-donut-wrap {extra_class}".strip()
        return f'''<div class="{cls}" data-chart="{esc(canvas_id)}">
  <header class="chart-hd">
    <span class="section-label">{esc(title)}</span>
    {sub_html}
    {meta_html}
  </header>
  <div class="chart-body-split">
    <div class="chart-ring-wrap">
      <div class="chart-wrap"><canvas id="{esc(canvas_id)}"></canvas></div>
    </div>
    <div class="chart-legend-panel">
      <span class="chart-legend-title">Distribuição</span>
      <div class="chart-legend-list" id="{esc(canvas_id)}-legend" aria-label="Legenda do gráfico"></div>
    </div>
  </div>
  {hint_html}
</div>'''
    if ranked:
        cls = f"chart-box chart-embed chart-ranked-wrap {extra_class}".strip()
        return f'''<div class="{cls}" data-chart="{esc(canvas_id)}">
  <header class="chart-hd">
    <span class="section-label">{esc(title)}</span>
    {sub_html}
    {meta_html}
  </header>
  <div class="chart-body-split">
    <div class="chart-plot-ranked"><canvas id="{esc(canvas_id)}" height="{height}"></canvas></div>
    <div class="chart-legend-panel">
      <span class="chart-legend-title">Ranking</span>
      <div class="chart-legend-list" id="{esc(canvas_id)}-legend" aria-label="Legenda do gráfico"></div>
    </div>
  </div>
  {hint_html}
</div>'''
    if delta:
        cls = f"chart-box chart-embed chart-delta-wrap {extra_class}".strip()
        return f'''<div class="{cls}" data-chart="{esc(canvas_id)}">
  <header class="chart-hd">
    <span class="section-label">{esc(title)}</span>
    {sub_html}
    {meta_html}
  </header>
  {delta_key_html}
  <div class="chart-body-split">
    <div class="chart-plot-ranked"><canvas id="{esc(canvas_id)}" height="{height}"></canvas></div>
    <div class="chart-legend-panel">
      <span class="chart-legend-title">Mudanças 2024→2025</span>
      <div class="chart-legend-list" id="{esc(canvas_id)}-legend" aria-label="Legenda do gráfico"></div>
    </div>
  </div>
  {hint_html}
</div>'''
    cls = f"chart-box chart-embed {extra_class}".strip()
    leg_below = f'<p class="chart-legend">{esc(legend)}</p>' if legend else ''
    return f'''<div class="{cls}" data-chart="{esc(canvas_id)}">
  <header class="chart-hd">
    <span class="section-label">{esc(title)}</span>
    {sub_html if not legend else ""}
    {meta_html}
  </header>
  {delta_key_html}
  <div class="chart-body-bar">
    <div class="chart-plot"><canvas id="{esc(canvas_id)}" height="{height}"></canvas></div>
    <div class="chart-legend-panel chart-legend-panel--compact">
      <div class="chart-legend-list" id="{esc(canvas_id)}-legend" aria-label="Legenda do gráfico"></div>
    </div>
  </div>
  {leg_below}
  {hint_html}
</div>'''


def render_cwe_rank_ladder(cwe_list, n=10):
    rows = []
    for c in cwe_list[:n]:
        trend = _cwe_trend_cls(c["trend"])
        trend_lbl = _cwe_trend_lbl(c["trend"])
        prev = c["rank"]
        t = str(c["trend"])
        if t.startswith("+"):
            prev = c["rank"] + int(t[1:])
            move = f"Era <strong>#{prev}</strong>, agora <strong>#{c['rank']}</strong>"
        elif t.startswith("-"):
            prev = c["rank"] - int(t[1:])
            move = f"Era <strong>#{prev}</strong>, agora <strong>#{c['rank']}</strong>"
        else:
            move = f"Mantém a posição <strong>#{c['rank']}</strong>"
        rows.append(f'''
    <button type="button" class="cwe-ladder-row trend-{trend}" data-cwe-open="{c["id"]}" data-cwe="{c["id"]}" aria-label="Abrir {esc(c["name_pt"])}">
      <span class="cwe-ladder-rank">{c["rank"]:02d}</span>
      <span class="cwe-ladder-body">
        <span class="cwe-ladder-id">{c["id"]}</span>
        <span class="cwe-ladder-name">{esc(c["name_pt"])}</span>
        <span class="cwe-ladder-move">{move}</span>
      </span>
      <span class="cwe-ladder-score">{c["score"]} pts</span>
      <span class="cwe-ladder-trend {trend}">{trend_lbl}</span>
    </button>''')
    return f'''<div class="chart-box cwe-ladder-box">
  <header class="chart-hd">
    <span class="section-label">Top 10 — quem subiu e quem desceu</span>
    <p class="chart-sub">Posição atual no MITRE TOP 25 e mudança vs. edição 2024. Posição <em>menor</em> = mais crítica.</p>
    <p class="chart-guide"><strong>Como ler:</strong> Cada linha é uma fraqueza. A seta mostra se ganhou ou perdeu posições no ranking anual. Clique para abrir o painel completo.</p>
    <p class="chart-takeaway">CWE-79 (XSS) lidera com folga. Entre as 10 primeiras, CWE-862 e CWE-352 subiram — sinal de que falhas de autorização e CSRF seguem em alta.</p>
  </header>
  <div class="cwe-rank-ladder">{"".join(rows)}
  </div>
</div>'''


def render_news_feed(news_items):
    cards = []
    for n in news_items:
        tag = n.get("tag", "news")
        body = n.get("body", "")
        body_html = f'<p class="news-body">{format_rich_text(body)}</p>' if body else ""
        bullets = n.get("bullets") or []
        bullets_html = ""
        if bullets:
            bl = "".join(f"<li>{format_rich_text(b)}</li>" for b in bullets)
            bullets_html = f'<ul class="news-bullets">{bl}</ul>'
        stats = n.get("stats") or []
        stats_html = ""
        if stats:
            chips = "".join(
                f'<span class="news-stat"><b>{esc(s[0])}</b> {esc(s[1])}</span>'
                for s in stats
            )
            stats_html = f'<div class="news-stats">{chips}</div>'
        impact = n.get("impact", "")
        impact_html = (
            f'<span class="news-impact">{format_rich_text(impact)}</span>'
            if impact else ""
        )
        search_blob = " ".join([
            n["title"], n["summary"], n["source"], body,
            " ".join(bullets), impact,
        ])
        cards.append(f'''
    <article class="news-card news-tag-{esc(tag)}" data-owasp="{n.get("owasp", "")}" data-cwe="{n.get("cwe", "")}" data-search="{esc(search_blob)}">
      <div class="news-card-accent" aria-hidden="true"></div>
      <div class="news-card-inner">
        <header class="news-card-hd">
          <div class="news-card-top">
            <time class="news-date" datetime="{esc(n["date"])}">{esc(n["date"])}</time>
            <span class="news-tag {esc(tag)}">{esc(tag)}</span>
          </div>
          <span class="news-source">{esc(n["source"])}</span>
          <h3 class="news-title">{esc(n["title"])}</h3>
          {impact_html}
        </header>
        <div class="news-card-body">
          <p class="news-summary">{format_rich_text(n["summary"])}</p>
          {body_html}
          {stats_html}
          {bullets_html}
        </div>
        <footer class="news-meta">
          <div class="news-corr">
            <button type="button" class="ok-badge accent pill corr-chip" data-owasp="{n.get("owasp", "")}" data-cwe="">{esc(n.get("owasp", ""))}</button>
            <button type="button" class="ok-badge cyan pill corr-chip" data-owasp="" data-cwe="{n.get("cwe", "")}">{esc(n.get("cwe", ""))}</button>
          </div>
          <a class="ok-btn sm cyan news-source-btn" href="{esc(n["url"])}" target="_blank" rel="noopener">Ler fonte →</a>
        </footer>
      </div>
    </article>''')
    return f'<div class="news-grid">{"".join(cards)}</div>'


def render_research_hub():
    nav = ""
    for i, r in enumerate(RESEARCH_DEEP):
        nav += f'''<button type="button" class="research-nav-item{" active" if i==0 else ""}" data-research="{r["id"]}">
          <span class="research-nav-src">{esc(r["source"])}</span>
          <span class="research-nav-hl">{esc(r["headline"][:72])}{"…" if len(r["headline"])>72 else ""}</span>
        </button>'''
    panels = ""
    for i, r in enumerate(RESEARCH_DEEP):
        stats = "".join(f'<div class="metric"><span class="metric-val">{esc(s[0])}</span><span class="metric-lbl">{esc(s[1])}</span></div>' for s in r["stats"])
        body = "".join(f"<p>{esc(p)}</p>" for p in r["body"])
        actions = "".join(f"<li>{esc(a)}</li>" for a in r["actions"])
        panels += f'''
        <div class="research-panel{" active" if i==0 else ""}" data-research-panel="{r["id"]}">
          <header class="research-panel-hd">
            <span class="section-label">{esc(r["source"])}</span>
            <h3>{esc(r["headline"])}</h3>
            <div class="metric-row">{stats}</div>
          </header>
          <div class="research-body">{body}</div>
          <div class="research-actions">
            <span class="section-label">Ações recomendadas</span>
            <ul>{actions}</ul>
          </div>
          <a href="{esc(r["link"])}" target="_blank" rel="noopener" class="ok-btn sm cyan">Abrir fonte primária →</a>
        </div>'''
    return f'<div class="research-hub"><nav class="research-nav">{nav}</nav><div class="research-panels">{panels}</div></div>'

def render_breach_timeline():
    track = ""
    for year, name, cat, desc, owasp, cwe, impact, ref, url in BREACH_TIMELINE:
        track += f'''
        <button type="button" class="timeline-node" data-owasp="{owasp}" data-cwe="{cwe}" data-year="{year}"
          data-name="{esc(name)}" data-cat="{esc(cat)}" data-desc="{esc(desc)}" data-impact="{esc(impact)}"
          data-ref="{esc(ref)}" data-url="{esc(url)}">
          <span class="timeline-rail"></span>
          <span class="timeline-dot"></span>
          <div class="timeline-card">
            <span class="timeline-year">{year}</span>
            <strong>{esc(name)}</strong>
            <span class="timeline-cat">{esc(cat)}</span>
            <span class="timeline-impact">{esc(impact)}</span>
          </div>
        </button>'''
    return f'''
    <div class="breach-explorer">
      <div class="timeline-vertical">{track}</div>
      <aside class="breach-detail" id="breach-detail">
        <p class="breach-detail-placeholder">Selecione um incidente na timeline para ver análise, impacto, links e correlação OWASP↔CWE.</p>
      </aside>
    </div>'''

def render_source_links():
    return "".join(
        f'<a class="source-link" href="{esc(url)}" target="_blank" rel="noopener" title="{esc(desc)}">'
        f'<span class="source-name">{esc(name)}</span><span class="source-desc">{esc(desc)}</span></a>'
        for name, url, desc in SOURCE_LINKS)

def render_market_strip():
    return "".join(
        f'<a class="metric compact metric-link" href="{esc(m[3])}" target="_blank" rel="noopener" title="Abrir fonte: {esc(m[2])}">'
        f'<span class="metric-val">{esc(m[0])}</span><span class="metric-lbl">{esc(m[1])}</span>'
        f'<span class="metric-src">{esc(m[2])} →</span></a>'
        for m in MARKET)

def render_market_sources():
    seen = set()
    links = []
    for m in MARKET:
        key = m[3]
        if key in seen:
            continue
        seen.add(key)
        links.append((m[2], m[3]))
    return "".join(
        f'<a class="market-src-link" href="{esc(url)}" target="_blank" rel="noopener">{esc(name)}</a>'
        for name, url in links)

def render_owasp_prevalence():
    owasp_intro = "https://owasp.org/Top10/2025/0x00_2025-Introduction/"
    rows = ""
    slug_map = {
            "A01": "A01_2025-Broken_Access_Control",
            "A02": "A02_2025-Security_Misconfiguration",
            "A03": "A03_2025-Software_Supply_Chain_Failures",
            "A04": "A04_2025-Cryptographic_Failures",
            "A05": "A05_2025-Injection",
            "A06": "A06_2025-Insecure_Design",
            "A07": "A07_2025-Authentication_Failures",
            "A08": "A08_2025-Software_or_Data_Integrity_Failures",
            "A09": "A09_2025-Security_Logging_and_Alerting_Failures",
            "A10": "A10_2025-Mishandling_of_Exceptional_Conditions",
        }
    for oid, name, prev, cwes, note in OWASP_PREVALENCE:
        row_url = f"https://owasp.org/Top10/2025/{slug_map.get(oid, oid)}/"
        rows += f'<tr><td><strong><a href="{row_url}" target="_blank" rel="noopener">{oid}</a></strong></td><td><a href="{row_url}" target="_blank" rel="noopener">{esc(name)}</a></td><td>{esc(prev)}</td><td>{esc(cwes)}</td><td>{esc(note)}</td></tr>'
    return f'''<p class="table-caption">Prevalência por categoria — dados contribuídos ao <a href="{owasp_intro}" target="_blank" rel="noopener">OWASP Top 10:2025 Introduction</a> (2,8M+ aplicações). Clique na categoria para abrir a página oficial.</p>
    <table class="data-table prevalence-table">
      <thead><tr><th>ID</th><th>Categoria</th><th>Prevalência</th><th>CWEs</th><th>Nota 2025</th></tr></thead>
      <tbody>{rows}</tbody></table>'''

def render_juice_ide(lab_count=0):
    return f'''<section class="lesson-sec" id="juice-ide" data-search="Juice Shop IDE VS Code compare diff terminal validação">
  <div class="ok-sec-hd"><div class="ok-left"><div class="ok-sec-num"><b>§IDE</b><span>·</span><span>juice shop</span></div><h2>IDE <em>— correção ao vivo</em></h2></div>
  <div class="ok-right">Explorer à esquerda · compare no centro · terminal de validação embaixo · {lab_count} arquivos vulneráveis do repositório oficial.</div></div>
  <p class="juice-ide-lede">Selecione um arquivo do Juice Shop: o código <strong>vulnerável</strong> fica à esquerda com contexto completo do arquivo; clique <strong>Aplicar correção</strong> para a versão segura ser digitada à direita, lado a lado. Use <strong>Validar</strong> para rodar o exploit no terminal.</p>
  {render_section_highlights("juice-ide")}
  <div class="vscode-shell">
    <aside class="vscode-sidebar" aria-label="Explorer Juice Shop">
      <header class="vscode-sidebar-hd"><span>EXPLORER</span><span class="vscode-root">juice-shop/</span></header>
      <div class="vscode-tree" id="juice-ide-tree"></div>
    </aside>
    <div class="vscode-main">
      <div class="vscode-tabs" id="juice-ide-tabs" role="tablist"></div>
      <div class="vscode-editor">
        <div class="vscode-editor-bar">
          <span class="vscode-breadcrumb" id="juice-ide-fname">routes/login.ts</span>
          <span class="juice-ide-status vuln" id="juice-ide-status">● Vulnerável</span>
          <span class="ide-line-badge" id="juice-ide-line-badge">L34</span>
          <a class="ok-btn sm ghost" id="juice-ide-github" href="https://github.com/juice-shop/juice-shop" target="_blank" rel="noopener">GitHub →</a>
        </div>
        <div class="vscode-toolbar code-toolbar">
          <button type="button" class="ok-btn sm solid cyan" id="juice-ide-show-vuln">Resetar</button>
          <button type="button" class="ok-btn sm ghost" id="juice-ide-show-fix">Mostrar correção</button>
          <label class="ide-sync-scroll"><input type="checkbox" id="juice-ide-sync" checked/> Sincronizar scroll</label>
        </div>
        <div class="ide-split-wrap" id="juice-ide-diff">
          <div class="ide-split-panel vuln">
            <header class="ide-split-hd"><span class="ide-split-dot vuln"></span> Vulnerável <span class="ide-split-file" id="juice-ide-vuln-label"></span></header>
            <pre class="ide-split-code"><code id="juice-ide-vuln"></code></pre>
          </div>
          <div class="ide-split-gutter" aria-hidden="true"></div>
          <div class="ide-split-panel fix">
            <header class="ide-split-hd"><span class="ide-split-dot fix"></span> Correção <span class="ide-split-hint" id="juice-ide-fix-hint">— aplique o patch</span></header>
            <pre class="ide-split-code"><code id="juice-ide-fix"></code></pre>
          </div>
        </div>
        <div class="juice-ide-meta" id="juice-ide-meta"></div>
      </div>
      <div class="vscode-terminal">
        <header class="vscode-term-hd">
          <span class="vscode-term-title">TERMINAL · validação</span>
          <div class="vscode-term-actions">
            <button type="button" class="ok-btn sm solid" id="juice-ide-apply">Aplicar correção</button>
            <button type="button" class="ok-btn sm cyan" id="juice-ide-validate">▶ Validar</button>
          </div>
        </header>
        <div class="vscode-term-out" id="juice-ide-term" aria-live="polite"></div>
      </div>
    </div>
  </div>
</section>'''


def render_sim_grid(SIMULATORS, esc, sim_ide_panel, variant="owasp"):
    rows = []
    for s in SIMULATORS:
        presets = "".join(
            f'<button type="button" class="ok-btn sm ghost sim-preset" data-target="{s["input_id"]}" data-val="{esc(p[1])}">{esc(p[0])}</button>'
            for p in s.get("presets", [])
        )
        box_cls = "sim-box sim-box-cwe" if variant == "cwe" else "sim-box sim-box-owasp"
        run_cls = "ok-btn sm sim-run sim-run-cwe" if variant == "cwe" else "ok-btn sm cyan sim-run sim-run-owasp"
        if variant == "cwe":
            badge = f'<span class="sim-cwe-badge">#{s["rank"]}</span> <span class="sim-cwe-id">{s["cwe"]}</span>'
            meta = f'{badge} <span class="sim-owasp-badge">{s.get("owasp", "")}</span>'
            info_btn = (
                f'<button type="button" class="ok-btn sm solid magenta sim-btn-info" '
                f'data-cwe-info="{s["cwe"]}" aria-label="Guia {esc(s["cwe"])}">+ Info</button>'
            )
        else:
            meta = f'<span class="sim-owasp-badge">{s["owasp"]}</span> · {s["cwe"]}'
            info_btn = (
                f'<button type="button" class="ok-btn sm solid cyan sim-btn-info" '
                f'data-owasp-info="{s["owasp"]}" aria-label="Guia {esc(s["owasp"])}">+ Info</button>'
            )
        rows.append(f'''    <div class="{box_cls}" id="sim-box-{s["kind"]}">
      <span class="section-label">{esc(s["title"])} {meta}</span>
      <input class="ok-input" id="{s["input_id"]}" type="{s.get("input_type", "text")}" value="{esc(s["input_value"])}" aria-label="{esc(s.get("input_aria", s["kind"]))}"/>
      <div class="sim-actions">
        {info_btn}
        <button type="button" class="{run_cls}" data-sim="{s["kind"]}">▶ {esc(s.get("run_label", "Executar"))}</button>
        <button type="button" class="ok-btn sm solid sim-btn-fix sim-fix" data-sim="{s["kind"]}">Fix</button>
        {presets}
      </div>
      <div class="sim-panels">
        <div class="sim-panel vuln"><div class="sim-panel-hd">Ataque simulado</div><div class="sim-output" id="sim-{s["kind"]}-out"></div></div>
        {sim_ide_panel(s["kind"], s["ide_file"])}
      </div>
      <span class="sim-status" id="sim-{s["kind"]}-status"></span>
    </div>''')
    return "\n".join(rows)


def render_code_vault():
    items = "".join(render_pattern_block(p, mode="list") for p in CODE_PATTERNS)
    details = "".join(render_pattern_block(p, mode="detail") for p in CODE_PATTERNS)
    return f'''<div class="vault-split">
      <aside class="vault-list" id="vault-list">{items}</aside>
      <div class="vault-detail" id="vault-detail">{details}</div>
    </div>'''

def patterns_for_owasp(oid):
    pats = [p for p in CODE_PATTERNS if p["owasp"] == oid]
    if not pats:
        return '<p class="muted">Padrões no Cofre de Código (§code-vault).</p>'
    return "".join(render_pattern_block(p, mode="inline") for p in pats)

def terminal_for_owasp(oid):
    labs = [(tid, lab) for tid, lab in TERMINAL_LABS.items() if lab.get("owasp") == oid]
    if not labs:
        return '<p class="muted">Terminal central em § Terminal Lab.</p>'
    return "".join(render_terminal_mini(tid, lab) for tid, lab in labs)

def _owasp_prev_pct(prev_str):
    if not prev_str or prev_str == "—":
        return 0.0
    try:
        return float(prev_str.replace("%", "").replace(",", ".").strip())
    except ValueError:
        return 0.0


def _owasp_trend_cls(diff):
    d = diff.lower()
    if "subiu" in d or "nova" in d:
        return "up"
    if "caiu" in d or "desceu" in d:
        return "down"
    return "flat"


def _cwe_trend_cls(trend):
    t = str(trend)
    if t.startswith("+"):
        return "up"
    if t.startswith("-"):
        return "down"
    return "flat"


def _cwe_trend_lbl(trend):
    t = str(trend)
    if t.startswith("+"):
        return f"↑ {t}"
    if t.startswith("-"):
        return f"↓ {t}"
    return "→ mantido"


def _cwe_score_pct(score):
    try:
        return min(100, int(float(score) / 60.38 * 100))
    except (TypeError, ValueError):
        return 8


def patterns_for_cwe(cid):
    pats = [p for p in CODE_PATTERNS if p["cwe"] == cid]
    if not pats:
        return '<p class="muted">Padrões no Cofre de Código (§code-vault).</p>'
    return "".join(render_pattern_block(p, mode="inline") for p in pats)


def render_owasp_modal_panel(o, rank):
    prose = render_modal_prose(o["p"])
    cases = "".join(
        f'<li class="owasp-case-item"><div class="owasp-case-year">{esc(c[0])}</div>'
        f'<div class="owasp-case-body"><strong class="modal-case-impact">{esc(c[1])}</strong>'
        f'<span class="modal-case-desc">{format_rich_text(c[2])}</span>'
        + (f'<span class="owasp-case-detail">{format_rich_text(c[3])}</span>' if len(c) > 3 else "")
        + "</div></li>"
        for c in o["cases"]
    )
    cwes = "".join(
        f'<button type="button" class="ok-badge cyan pill corr-chip modal-cwe-chip" data-cwe="{c}" data-owasp="{o["id"]}">{c}</button>'
        for c in o["cwes"]
    )
    juice_html = "".join(render_juice_block(k) for k in o["juice"])
    patterns_html = patterns_for_owasp(o["id"])
    term_html = terminal_for_owasp(o["id"])
    official = next((r[1] for r in o["refs"] if "OWASP" in r[0] and o["id"] in r[0]), o["refs"][0][1] if o["refs"] else "#")
    sim_kind = o["id"].lower()
    tech_html = render_modal_tech_grid(o["det"], o["test"], o["asvs"])
    mitiga_html = render_modal_mitiga(o["prev"], o["refs"])
    hl_visao = render_owasp_highlights(o["id"])
    hl_casos_extra = render_owasp_highlights(o["id"], types=["caso"])
    hl_visao_block = (
        f'<div class="modal-hl-section"><span class="section-label">Destaques da matéria</span>{hl_visao}</div>'
        if hl_visao else ""
    )
    hl_casos_block = (
        f'<div class="modal-hl-section caso-extra"><span class="section-label">Análise de caso</span>{hl_casos_extra}</div>'
        if hl_casos_extra else ""
    )
    n_juice = len(o["juice"])
    lesson_plan = _lesson_plans().get(o["id"])
    lesson_html = render_lesson_plan(lesson_plan, o["id"], variant="owasp", code_html=patterns_html)
    tabs = "".join([
        modal_tab_btn("guia", "+ Info", active=True),
        modal_tab_btn("visao", "Visão"),
        modal_tab_btn("tecnico", "Técnico"),
        modal_tab_btn("casos", "Casos", count=len(o["cases"])),
        modal_tab_btn("codigo", "Código"),
        modal_tab_btn("juice", "Juice Shop", count=n_juice),
        modal_tab_btn("terminal", "Terminal"),
        modal_tab_btn("mitiga", "Mitigação", count=len(o["prev"])),
    ])
    return f'''
  <div class="owasp-modal-panel" id="owasp-panel-{o["id"]}" data-owasp-panel="{o["id"]}" data-owasp="{o["id"]}" data-search="{esc(o["id"] + " " + o["pt"] + " " + o["en"] + " " + " ".join(o["cwes"]))}" hidden>
    <header class="owasp-modal-hd">
      <div class="owasp-modal-rank">#{rank:02d}</div>
      <div class="owasp-modal-titles">
        <span class="section-label">{o["id"]} · owasp 2025</span>
        <h2>{esc(o["pt"])}</h2>
        <p class="owasp-modal-en">{esc(o["en"])}</p>
      </div>
      <p class="owasp-modal-diff"><span class="modal-diff-pill">vs 2021</span>{format_rich_text(o["diff"])}</p>
    </header>
    <div class="owasp-modal-actions">
      <a class="ok-btn sm cyan" href="{esc(official)}" target="_blank" rel="noopener">Página oficial →</a>
      <button type="button" class="ok-btn sm ghost owasp-open-sim" data-sim-box="sim-box-{sim_kind}">Simulador §sim</button>
      <button type="button" class="ok-btn sm ghost owasp-open-corr" data-owasp-corr="{o["id"]}">Matriz correlação</button>
    </div>
    <div class="ok-tabs section-tabs owasp-modal-tabs" role="tablist">{tabs}</div>
    <div class="owasp-modal-scroll">
      <div class="tab-panel active" data-panel="guia">{lesson_html}</div>
      <div class="tab-panel" data-panel="visao">
        {prose}
        {hl_visao_block}
        <div class="modal-tags-block">
          <span class="section-label">CWEs relacionadas</span>
          <div class="tag-row modal-tag-row">{cwes}</div>
        </div>
      </div>
      <div class="tab-panel" data-panel="tecnico">{tech_html}</div>
      <div class="tab-panel" data-panel="casos">
        <p class="modal-tab-intro">Incidentes reais que ilustram <strong>{esc(o["pt"])}</strong> em produção.</p>
        <ul class="owasp-case-list modal-case-list">{cases}</ul>
        {hl_casos_block}
      </div>
      <div class="tab-panel" data-panel="codigo">
        <p class="modal-tab-intro">Padrões vulneráveis e correções do <strong>Cofre de Código</strong> mapeados para {o["id"]}.</p>
        <div class="pattern-stack">{patterns_html}</div>
      </div>
      <div class="tab-panel" data-panel="juice">
        <p class="modal-tab-intro"><strong>{n_juice} labs</strong> reproduzíveis no Juice Shop local — código real do repositório oficial.</p>
        <div class="lab-stack">{juice_html}</div>
      </div>
      <div class="tab-panel" data-panel="terminal">
        <p class="modal-tab-intro">Comandos guiados para validar exploits e mitigações desta categoria.</p>
        {term_html}
      </div>
      <div class="tab-panel" data-panel="mitiga">{mitiga_html}</div>
    </div>
  </div>'''


def render_owasp_hub(owasp_list, prevalence_rows):
    prev_map = {row[0]: row for row in prevalence_rows}
    cards = []
    anchors = []
    panels = []
    for i, o in enumerate(owasp_list):
        rank = i + 1
        oid = o["id"]
        prev_row = prev_map.get(oid, (oid, o["en"], "—", "—", ""))
        prev_val = prev_row[2]
        prev_note = prev_row[4] if len(prev_row) > 4 else ""
        pct = _owasp_prev_pct(prev_val)
        bar_w = min(100, int(pct / 4.0 * 100)) if pct else 8
        trend = _owasp_trend_cls(o["diff"])
        trend_lbl = {"up": "↑ subiu", "down": "↓ caiu", "flat": "→ mantido"}[trend]
        teaser = o["p"][0][:140] + ("…" if len(o["p"][0]) > 140 else "")
        cwe_preview = "".join(f'<span class="owasp-card-cwe">{c}</span>' for c in o["cwes"][:4])
        juice_n = len(o["juice"])
        search_blob = " ".join([oid, o["pt"], o["en"], teaser] + o["cwes"])
        sim_kind = oid.lower()
        cards.append(f'''
    <article class="owasp-card trend-{trend}" data-owasp="{oid}" data-search="{esc(search_blob)}">
      <div class="owasp-card-top">
        <span class="owasp-card-rank">{rank:02d}</span>
        <span class="owasp-card-id">{oid}</span>
        <span class="owasp-card-trend {trend}">{trend_lbl}</span>
      </div>
      <h3 class="owasp-card-title">{esc(o["pt"])}</h3>
      <p class="owasp-card-en">{esc(o["en"])}</p>
      <p class="owasp-card-teaser">{esc(teaser)}</p>
      <div class="owasp-card-meta">
        <div class="owasp-prev-wrap" title="Prevalência OWASP 2025">
          <div class="owasp-prev-bar"><span class="owasp-prev-fill" style="width:{bar_w}%"></span></div>
          <span class="owasp-prev-val">{esc(prev_val if prev_val != "—" else "survey")}</span>
        </div>
        <span class="owasp-card-labs">{juice_n} labs</span>
      </div>
      <div class="owasp-card-cwes">{cwe_preview}</div>
      <div class="hub-card-actions">
        <button type="button" class="ok-btn sm solid cyan hub-btn-info" data-owasp-info="{oid}" aria-label="Guia {esc(o["pt"])}">+ Info</button>
        <button type="button" class="ok-btn sm ghost hub-btn-sim" data-owasp-sim="{oid}" data-sim-box="sim-box-{sim_kind}" aria-label="Simulador {oid}">Simulador</button>
      </div>
    </article>''')
        anchors.append(f'<div id="owasp-{oid}" class="owasp-anchor" data-owasp="{oid}" aria-hidden="true"></div>')
        panels.append(render_owasp_modal_panel(o, rank))

    cards_html = "\n".join(cards)
    anchors_html = "\n".join(anchors)
    panels_html = "\n".join(panels)

    return f'''
<section class="lesson-sec" id="owasp-hub" data-search="OWASP Top 10 2025 Broken Access Control Injection">
  <div class="ok-sec-hd"><div class="ok-left"><div class="ok-sec-num"><b>§A</b><span>·</span><span>owasp</span></div><h2>Top 10 <em>2025</em></h2></div>
  <div class="ok-right">Clique em uma categoria para abrir o <strong>painel interativo</strong> — labs, código, terminal e mitigação.</div></div>
  <p class="owasp-hub-hint">10 categorias · <strong>+ Info</strong> abre guia completo · <strong>Simulador</strong> para prática · <kbd>←</kbd> <kbd>→</kbd> no modal</p>
  {render_section_highlights("owasp-hub", layout="grid")}
  <div class="owasp-anchors" aria-hidden="true">{anchors_html}</div>
  <div class="owasp-bento">{cards_html}
  </div>
</section>

<div id="owasp-modal" class="owasp-modal" aria-hidden="true" role="dialog" aria-modal="true" aria-labelledby="owasp-modal-title">
  <div class="owasp-modal-backdrop" data-owasp-close></div>
  <div class="owasp-modal-dialog">
    <header class="owasp-modal-toolbar">
      <button type="button" class="ok-btn sm ghost owasp-modal-prev" aria-label="Categoria anterior">←</button>
      <span id="owasp-modal-title" class="owasp-modal-toolbar-title">OWASP Top 10</span>
      <button type="button" class="ok-btn sm ghost owasp-modal-next" aria-label="Próxima categoria">→</button>
      <button type="button" class="owasp-modal-close ok-btn sm solid" data-owasp-close aria-label="Fechar">✕</button>
    </header>
    <div class="owasp-modal-panels">{panels_html}
    </div>
  </div>
</div>'''


def render_tabs_owasp(o):
    """Legado — use render_owasp_hub."""
    return render_owasp_modal_panel(o, int(o["id"].replace("A", "")))


def render_cwe_modal_panel(c):
    num = c["id"].split("-")[1]
    prose = render_modal_prose(c["p"])
    cases = "".join(
        f'<li class="owasp-case-item"><div class="owasp-case-year">{esc(cs[1])}</div>'
        f'<div class="owasp-case-body"><strong class="modal-case-impact">{esc(cs[0])}</strong>'
        f'<span class="modal-case-desc">{format_rich_text(cs[2])}</span></div></li>'
        for cs in c["cases"]
    )
    tools = "".join(f'<span class="ok-badge pill modal-tool-chip">{esc(t)}</span> ' for t in c["tools"])
    refs = "".join(f'<li><a href="{esc(r[1])}" target="_blank" rel="noopener">{esc(r[0])} →</a></li>' for r in c["refs"])
    juice = render_juice_block(c.get("juice"))
    pats = [p for p in CODE_PATTERNS if p["cwe"] == c["id"]]
    patterns_html = "".join(render_pattern_block(p, mode="inline") for p in pats)
    lab_content = (juice or "") + (f'<div class="pattern-stack">{patterns_html}</div>' if patterns_html else "")
    if not lab_content.strip():
        lab_content = '<p class="muted">Correlacione via OWASP ou Terminal Lab.</p>'
    owasp_links = "".join(
        f'<button type="button" class="ok-btn sm ghost cwe-open-owasp modal-owasp-link" data-owasp-jump="{oa}">{oa}</button> '
        for oa in c["owasp"])
    corr_extra = "".join(
        f'<button type="button" class="ok-badge cyan pill corr-chip" data-owasp="{a}" data-cwe="{c["id"]}">{a}↔{c["id"]}</button> '
        for a, cc, s, n in CORRELATIONS if cc == c["id"])
    primary_owasp = c["owasp"][0]
    owasp_o = next((x for x in OWASP_LIST if x["id"] == primary_owasp), None)
    owasp_name = owasp_o["pt"] if owasp_o else primary_owasp
    official = next((r[1] for r in c["refs"] if c["id"] in r[0]), c["refs"][0][1] if c["refs"] else "#")
    sim_kind = "c" + c["id"].replace("CWE-", "")
    trend_cls = _cwe_trend_cls(c["trend"])
    kev_badge = f'<span class="ok-badge success">KEV {c["kev"]}</span>' if c["kev"] else ""
    mitiga_html = render_modal_mitiga(c["mit"], c["refs"])
    det_html = render_modal_bullets(c["det"], "◈")
    hl_visao = render_cwe_highlights(c["id"])
    hl_casos_extra = render_cwe_highlights(c["id"], types=["caso"])
    hl_visao_block = (
        f'<div class="modal-hl-section"><span class="section-label">Destaques da matéria</span>{hl_visao}</div>'
        if hl_visao else ""
    )
    hl_casos_block = (
        f'<div class="modal-hl-section caso-extra"><span class="section-label">Análise de caso</span>{hl_casos_extra}</div>'
        if hl_casos_extra else ""
    )
    lesson_plan = _lesson_plans().get(c["id"])
    lesson_html = render_lesson_plan(lesson_plan, c["id"], variant="cwe", code_html=patterns_html)
    tabs = "".join([
        modal_tab_btn("guia", "+ Info", active=True),
        modal_tab_btn("visao", "Visão"),
        modal_tab_btn("owasp", "OWASP", count=len(c["owasp"])),
        modal_tab_btn("casos", "Casos", count=len(c["cases"])),
        modal_tab_btn("det", "Detecção"),
        modal_tab_btn("mit", "Mitigação", count=len(c["mit"])),
        modal_tab_btn("lab", "Código + Lab"),
        modal_tab_btn("refs", "Refs", count=len(c["refs"])),
    ])
    return f'''
  <div class="cwe-modal-panel" id="cwe-panel-{c["id"]}" data-cwe-panel="{c["id"]}" data-cwe="{c["id"]}" data-owasp="{primary_owasp}" data-search="{esc(c["id"] + " " + c["name_pt"] + " " + c["name"])}" hidden>
    <header class="cwe-modal-hd">
      <div class="cwe-modal-rank">#{c["rank"]:02d}</div>
      <div class="cwe-modal-titles">
        <span class="section-label">{c["id"]} · mitre 2025</span>
        <h2>{esc(c["name_pt"])}</h2>
        <p class="cwe-modal-en">{esc(c["name"])}</p>
      </div>
      <div class="cwe-modal-badges">
        <span class="ok-badge accent">score {c["score"]}</span>
        {kev_badge}
        <span class="cwe-card-trend {trend_cls}">vs 2024: {esc(c["trend"])}</span>
      </div>
    </header>
    <div class="cwe-modal-actions">
      <a class="ok-btn sm magenta" href="{esc(official)}" target="_blank" rel="noopener">MITRE CWE →</a>
      <button type="button" class="ok-btn sm ghost cwe-open-sim" data-sim-box="sim-box-{sim_kind}">Simulador §cwe-sim</button>
      <button type="button" class="ok-btn sm ghost cwe-open-owasp" data-owasp-jump="{primary_owasp}">OWASP {primary_owasp}</button>
      <button type="button" class="ok-btn sm ghost cwe-open-corr" data-cwe-corr="{c["id"]}">Matriz correlação</button>
    </div>
    <div class="ok-tabs section-tabs cwe-modal-tabs" role="tablist">{tabs}</div>
    <div class="cwe-modal-scroll">
      <div class="tab-panel active" data-panel="guia">{lesson_html}</div>
      <div class="tab-panel" data-panel="visao">
        {prose}
        {hl_visao_block}
        <div class="modal-tags-block">
          <span class="section-label">Ferramentas de detecção</span>
          <div class="tag-row modal-tag-row">{tools}</div>
        </div>
      </div>
      <div class="tab-panel" data-panel="owasp">
        <div class="modal-owasp-primary">
          <span class="section-label">Correlação primária</span>
          <button type="button" class="modal-owasp-hero cwe-open-owasp" data-owasp-jump="{primary_owasp}">
            <span class="modal-owasp-id">{primary_owasp}</span>
            <span class="modal-owasp-name">{esc(owasp_name)}</span>
          </button>
        </div>
        <div class="modal-tags-block">
          <span class="section-label">Todas as categorias OWASP</span>
          <div class="tag-row modal-tag-row">{owasp_links}</div>
        </div>
        <div class="modal-tags-block">
          <span class="section-label">Matriz OWASP ↔ CWE</span>
          <div class="tag-row modal-tag-row">{corr_extra}</div>
        </div>
      </div>
      <div class="tab-panel" data-panel="casos">
        <p class="modal-tab-intro">CVEs e incidentes que exemplificam <strong>{esc(c["id"])}</strong>.</p>
        <ul class="owasp-case-list modal-case-list">{cases}</ul>
        {hl_casos_block}
      </div>
      <div class="tab-panel" data-panel="det">
        <p class="modal-tab-intro">Como encontrar esta fraqueza em revisão de código, SAST/DAST e pentest.</p>
        {det_html}
      </div>
      <div class="tab-panel" data-panel="mit">{mitiga_html}</div>
      <div class="tab-panel" data-panel="lab">
        <p class="modal-tab-intro">Código vulnerável, correção e lab Juice Shop para {c["id"]}.</p>
        {lab_content}
      </div>
      <div class="tab-panel" data-panel="refs">
        <ul class="modal-ref-list standalone">{"".join(f'<li><a href="{esc(r[1])}" target="_blank" rel="noopener"><span class="modal-ref-ico">↗</span>{esc(r[0])}</a></li>' for r in c["refs"])}</ul>
      </div>
    </div>
  </div>'''


def render_cwe_hub(cwe_list):
    cards = []
    anchors = []
    panels = []
    for c in cwe_list:
        num = c["id"].split("-")[1]
        teaser = c["p"][0][:120] + ("…" if len(c["p"][0]) > 120 else "")
        bar_w = _cwe_score_pct(c["score"])
        trend = _cwe_trend_cls(c["trend"])
        trend_lbl = _cwe_trend_lbl(c["trend"])
        primary_owasp = c["owasp"][0]
        owasp_preview = "".join(f'<span class="cwe-card-owasp">{oa}</span>' for oa in c["owasp"][:3])
        kev_txt = f"KEV {c['kev']}" if c["kev"] else "sem KEV"
        search_blob = " ".join([c["id"], c["name_pt"], c["name"], teaser, primary_owasp])
        sim_kind = "c" + c["id"].replace("CWE-", "")
        cards.append(f'''
    <article class="cwe-card trend-{trend}" data-cwe="{c["id"]}" data-owasp="{primary_owasp}" data-search="{esc(search_blob)}">
      <div class="cwe-card-top">
        <span class="cwe-card-rank">{c["rank"]:02d}</span>
        <span class="cwe-card-id">{c["id"]}</span>
        <span class="cwe-card-trend {trend}">{trend_lbl}</span>
      </div>
      <h3 class="cwe-card-title">{esc(c["name_pt"])}</h3>
      <p class="cwe-card-en">{esc(c["name"])}</p>
      <p class="cwe-card-teaser">{esc(teaser)}</p>
      <div class="cwe-card-meta">
        <div class="cwe-score-wrap" title="Score MITRE 2025">
          <div class="cwe-score-bar"><span class="cwe-score-fill" style="width:{bar_w}%"></span></div>
          <span class="cwe-score-val">{c["score"]}</span>
        </div>
        <span class="cwe-card-kev">{kev_txt}</span>
      </div>
      <div class="cwe-card-owasps">{owasp_preview}</div>
      <div class="hub-card-actions">
        <button type="button" class="ok-btn sm solid magenta hub-btn-info" data-cwe-info="{c["id"]}" aria-label="Guia {esc(c["name_pt"])}">+ Info</button>
        <button type="button" class="ok-btn sm ghost hub-btn-sim" data-cwe-sim="{c["id"]}" data-sim-box="sim-box-{sim_kind}" aria-label="Simulador {c["id"]}">Simulador</button>
      </div>
    </article>''')
        anchors.append(f'<div id="cwe-{num}" class="cwe-anchor" data-cwe="{c["id"]}" aria-hidden="true"></div>')
        panels.append(render_cwe_modal_panel(c))

    cards_html = "\n".join(cards)
    anchors_html = "\n".join(anchors)
    panels_html = "\n".join(panels)

    return f'''
<section class="lesson-sec" id="cwe-hub" data-search="CWE TOP 25 MITRE 2025 Cross-site Scripting SQL Injection">
  <div class="ok-sec-hd"><div class="ok-left"><div class="ok-sec-num"><b>§C</b><span>·</span><span>cwe</span></div><h2>TOP 25 <em>MITRE 2025</em></h2></div>
  <div class="ok-right">Clique em uma fraqueza para abrir o <strong>painel interativo</strong> — OWASP, labs, detecção e mitigação.</div></div>
  <p class="cwe-hub-hint">25 fraquezas · <strong>+ Info</strong> abre guia completo · <strong>Simulador</strong> para prática · <kbd>←</kbd> <kbd>→</kbd> no modal</p>
  {render_section_highlights("cwe-hub", layout="grid")}
  <div class="cwe-anchors" aria-hidden="true">{anchors_html}</div>
  <div class="cwe-bento">{cards_html}
  </div>
</section>

<div id="cwe-modal" class="cwe-modal" aria-hidden="true" role="dialog" aria-modal="true" aria-labelledby="cwe-modal-title">
  <div class="cwe-modal-backdrop" data-cwe-close></div>
  <div class="cwe-modal-dialog">
    <header class="cwe-modal-toolbar">
      <button type="button" class="ok-btn sm ghost cwe-modal-prev" aria-label="Fraqueza anterior">←</button>
      <span id="cwe-modal-title" class="cwe-modal-toolbar-title">CWE TOP 25</span>
      <button type="button" class="ok-btn sm ghost cwe-modal-next" aria-label="Próxima fraqueza">→</button>
      <button type="button" class="cwe-modal-close ok-btn sm solid" data-cwe-close aria-label="Fechar">✕</button>
    </header>
    <div class="cwe-modal-panels">{panels_html}
    </div>
  </div>
</div>'''


def render_cwe_full(c):
    """Legado — use render_cwe_hub."""
    return render_cwe_modal_panel(c)

_OWASP_NAV_TONE = {
    "A01": "accent", "A02": "cyan", "A03": "warning", "A04": "magenta",
    "A05": "danger", "A06": "accent", "A07": "cyan", "A08": "warning",
    "A09": "success", "A10": "magenta",
}


def _cwe_nav_tone(rank):
    if rank <= 5:
        return "hot"
    if rank <= 10:
        return "mid"
    return "base"


def _nav_link(href, label, tone="soft", badge="", title="", extra_cls=""):
    badge_html = f'<span class="nav-badge">{esc(badge)}</span>' if badge else ""
    title_attr = f' title="{esc(title)}"' if title else ""
    return (
        f'<a class="nav-link nav-tone-{tone}{extra_cls}" href="{esc(href)}"{title_attr}>'
        f'{badge_html}<span class="nav-label">{esc(label)}</span></a>'
    )


def render_sidebar(owasp_list, cwe_list):
    index = [
        ("#intro", "Introdução", "cyan", ""),
        ("#mercado", "Mercado & dados", "accent", ""),
        ("#pesquisa", "Intel de ameaças", "magenta", ""),
        ("#noticias", "Notícias", "cyan", ""),
        ("#correlacao", "Matriz OWASP↔CWE", "accent", ""),
        ("#terminal-lab", "Terminal Lab", "success", ""),
        ("#code-vault", "Cofre de código", "warning", ""),
        ("#simuladores", "Simuladores OWASP", "accent", ""),
        ("#simuladores-cwe", "Simuladores CWE", "magenta", ""),
    ]
    index_html = "".join(_nav_link(h, lbl, t) for h, lbl, t, _ in index)

    owasp_hub = _nav_link("#owasp-hub", "Hub interativo · Top 10", "accent", "§A", "Painel OWASP 2025", " nav-hub")
    owasp_items = "".join(
        _nav_link(
            f"#owasp-{o['id']}",
            o["en"],
            _OWASP_NAV_TONE.get(o["id"], "soft"),
            o["id"],
            o["pt"],
            " nav-owasp",
        )
        for o in owasp_list
    )

    bridge = _nav_link("#ponte-owasp-cwe", "Ponte OWASP → CWE", "bridge", "↔", "Transição entre hubs", " nav-bridge")

    cwe_hub = _nav_link("#cwe-hub", "Hub interativo · TOP 25", "magenta", "§C", "Painel CWE MITRE 2025", " nav-hub")
    cwe_items = "".join(
        _nav_link(
            f"#cwe-{c['id'].split('-')[1]}",
            c["name_pt"][:28] + ("…" if len(c["name_pt"]) > 28 else ""),
            _cwe_nav_tone(c["rank"]),
            f"#{c['rank']}",
            f"{c['id']} · {c['name']}",
            " nav-cwe",
        )
        for c in cwe_list
    )

    labs = (
        _nav_link("#juice-setup", "Juice Shop · setup", "cyan", "🧃", "Docker e clone local", " nav-lab")
        + _nav_link("#juice-ide", "IDE Juice Shop", "cyan", "IDE", "Correção ao vivo", " nav-lab")
        + _nav_link("#quiz", "Quiz", "success", "?", "Quiz de verificação", " nav-lab")
    )

    return f'''<aside class="sidebar no-print" id="sidebar" aria-label="Índice de navegação">
  <div class="sidebar-head">
    <span class="sidebar-kicker">AppSec · OWASP + CWE</span>
    <strong class="sidebar-title">Top 10 + TOP 25</strong>
    <span class="sidebar-ver">referência interativa</span>
  </div>
  <nav class="nav-group" data-group="index">
    <h3 class="nav-group-hd nav-tone-cyan"><span class="nav-group-dot"></span>// índice</h3>
    <div class="nav-group-body">{index_html}</div>
  </nav>
  <nav class="nav-group" data-group="owasp">
    <h3 class="nav-group-hd nav-tone-accent"><span class="nav-group-dot"></span>// owasp top 10</h3>
    <div class="nav-group-body nav-scroll-block">{owasp_hub}{owasp_items}</div>
  </nav>
  <nav class="nav-group" data-group="bridge">
    <div class="nav-group-body nav-bridge-only">{bridge}</div>
  </nav>
  <nav class="nav-group" data-group="cwe">
    <h3 class="nav-group-hd nav-tone-magenta"><span class="nav-group-dot"></span>// cwe top 25</h3>
    <div class="nav-group-body nav-scroll-block">{cwe_hub}{cwe_items}</div>
  </nav>
  <nav class="nav-group" data-group="labs">
    <h3 class="nav-group-hd nav-tone-success"><span class="nav-group-dot"></span>// labs</h3>
    <div class="nav-group-body">{labs}</div>
  </nav>
</aside>'''


def render_heatmap():
    owasp_ids = [o["id"] for o in OWASP_LIST]
    cwe_ids = [c["id"] for c in CWE_TOP25_FULL]
    corr_map = {(a,cc): (s,n) for a,cc,s,n in CORRELATIONS}
    header = "<tr><th class='hm-corner'></th>" + "".join(
        f'<th class="hm-cwe" data-cwe="{cid}" title="{cid}"><span>{cid.replace("CWE-","")}</span></th>' for cid in cwe_ids) + "</tr>"
    rows = ""
    for oid in owasp_ids:
        cells = f'<th class="hm-owasp" data-owasp="{oid}"><span>{oid}</span></th>'
        for cid in cwe_ids:
            if (oid, cid) in corr_map:
                s, n = corr_map[(oid, cid)]
                cells += f'<td class="hm-cell s{s}" data-owasp="{oid}" data-cwe="{cid}" title="{esc(n)}"></td>'
            else:
                cells += f'<td class="hm-cell empty" data-owasp="{oid}" data-cwe="{cid}"></td>'
        rows += f"<tr>{cells}</tr>"
    return f'<table class="heatmap" id="heatmap"><thead>{header}</thead><tbody>{rows}</tbody></table>'

def render_corr_detail():
    return "".join(
        f'<button type="button" class="corr-item" data-owasp="{a}" data-cwe="{cc}"><span class="corr-id">{a}↔{cc}</span><span class="corr-name">{esc(n)}</span><span class="corr-str">força {s}/3</span></button>'
        for a, cc, s, n in CORRELATIONS)