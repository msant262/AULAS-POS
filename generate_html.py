#!/usr/bin/env python3
"""Gera owasp-cwe-guia.html — arquivo HTML único, autocontido, abrível direto no navegador."""
import base64, html as H, json, pathlib, re, urllib.request

ROOT = pathlib.Path(__file__).parent
OUT_DIR = ROOT / "OWASP-CWE"
OUT_FILE = OUT_DIR / "owasp-cwe-guia.html"
FONTS_CACHE = ROOT / ".fonts-embedded.css"
FONTS_URL = (
    "https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700"
    "&family=JetBrains+Mono:wght@300;400;500;600;700&display=swap"
)

def build_embedded_fonts():
    if FONTS_CACHE.exists():
        return FONTS_CACHE.read_text(encoding="utf-8")
    req = urllib.request.Request(
        FONTS_URL,
        headers={"User-Agent": "Mozilla/5.0 (compatible; OkamiFontEmbed/1.0)"},
    )
    css = urllib.request.urlopen(req, timeout=60).read().decode("utf-8")

    def embed_url(match):
        font_url = match.group(1)
        data = urllib.request.urlopen(font_url, timeout=60).read()
        b64 = base64.b64encode(data).decode("ascii")
        if font_url.endswith(".woff2"):
            mime = "font/woff2"
        elif font_url.endswith(".woff"):
            mime = "font/woff"
        else:
            mime = "font/ttf"
        return f"url(data:{mime};base64,{b64})"

    css = re.sub(r"url\((https://[^)]+)\)", embed_url, css)
    FONTS_CACHE.write_text(css, encoding="utf-8")
    return css

EMBEDDED_FONTS = build_embedded_fonts()
OKAMI = (ROOT / "okami.css").read_text()
PATTERNS = (ROOT / "okami-patterns.css").read_text()
def _inject_js(app_path, *inject_paths):
    text = (ROOT / app_path).read_text()
    for p in inject_paths:
        text = text.replace(f"/*{p}_INJECT*/", (ROOT / f"{p}.js").read_text())
    return text

APP_JS = _inject_js("app.js", "simulators", "cwe-simulators", "owasp-hub", "cwe-hub", "juice-ide")

def esc(s): return H.escape(str(s))

def json_script_embed(data):
    """JSON seguro dentro de <script> — evita truncar em </script> no payload."""
    return json.dumps(data, ensure_ascii=False).replace("</", "<\\/")

def sim_ide_panel(kind, filename):
    return f'''<div class="sim-panel fix"><div class="sim-panel-hd">IDE · correção</div>
        <div class="sim-ide"><div class="sim-ide-topbar"><span class="dots"><span></span><span></span><span></span></span><span class="fname" id="sim-{kind}-ide-file">{esc(filename)}</span></div>
        <div class="sim-ide-out" id="sim-{kind}-ide"></div></div></div>'''

g = globals()
exec((ROOT / "generate_html_data.py").read_text(), g)
exec((ROOT / "simulators_config.py").read_text(), g)
exec((ROOT / "cwe_simulators_config.py").read_text(), g)
exec((ROOT / "intel_expansion.py").read_text(), g)
exec((ROOT / "extended_content.py").read_text(), g)
exec((ROOT / "course_highlights.py").read_text(), g)
exec((ROOT / "juice_ide_data.py").read_text(), g)
exec((ROOT / "cwe_top25_full.py").read_text(), g)
exec((ROOT / "lesson_plans.py").read_text(), g)
exec((ROOT / "generate_html_render.py").read_text(), g)

OWASP_LIST = g["OWASP_LIST"]
CWE_TOP25_FULL = g["CWE_TOP25_FULL"]
LESSON_PLANS = g["build_all_lesson_plans"](OWASP_LIST, CWE_TOP25_FULL)
g["LESSON_PLANS"] = LESSON_PLANS
JUICE = {**g["JUICE"], **g["JUICE_EXTRA"]}
g["JUICE"] = JUICE
CORRELATIONS = g["CORRELATIONS"]
MARKET = g["MARKET"] + g.get("MARKET_EXTRA", []) + g.get("MARKET_2025", [])
g["MARKET"] = MARKET
RESEARCH_DEEP = g["RESEARCH_DEEP"] + g.get("RESEARCH_EXTRA", [])
g["RESEARCH_DEEP"] = RESEARCH_DEEP
BREACH_TIMELINE = g["BREACH_TIMELINE"] + g.get("BREACH_EXTRA", [])
g["BREACH_TIMELINE"] = BREACH_TIMELINE
SOURCE_LINKS = g["SOURCE_LINKS"] + g.get("SOURCE_LINKS_EXTRA", [])
g["SOURCE_LINKS"] = SOURCE_LINKS
NEWS_FEED = g.get("NEWS_FEED", [])
g["CODE_PATTERNS"] = g["CODE_PATTERNS"]
g["TERMINAL_LABS"] = g["TERMINAL_LABS"]
g["BREACH_TIMELINE"] = g["BREACH_TIMELINE"]
g["RESEARCH_DEEP"] = g["RESEARCH_DEEP"]
QUIZ = g["QUIZ"]
OWASP_2021_VS_2025 = g["OWASP_2021_VS_2025"]
CODE_PATTERNS = g["CODE_PATTERNS"]
TERMINAL_LABS = g["TERMINAL_LABS"]
BREACH_TIMELINE = g["BREACH_TIMELINE"]
RESEARCH_DEEP = g["RESEARCH_DEEP"]
SOURCE_LINKS = g["SOURCE_LINKS"]
NEWS_FEED = g.get("NEWS_FEED", [])
chart_cwe_kev = g.get("chart_cwe_kev", lambda x: [])
chart_owasp_prev = g.get("chart_owasp_prev", lambda: [])
chart_breach_vectors = g.get("chart_breach_vectors", lambda: [])
chart_cwe_delta = g.get("chart_cwe_delta", lambda x: [])
cwe_chart_label = g.get("cwe_chart_label", lambda c: c["id"])
render_news_feed = g["render_news_feed"]
render_chart_box = g["render_chart_box"]
render_cwe_rank_ladder = g["render_cwe_rank_ladder"]
render_juice_ide = g["render_juice_ide"]
build_juice_ide_entries = g["build_juice_ide_entries"]
OWASP_PREVALENCE = g["OWASP_PREVALENCE"]
g["OWASP_PREVALENCE"] = OWASP_PREVALENCE
g["SOURCE_LINKS"] = SOURCE_LINKS
render_owasp_hub = g["render_owasp_hub"]
render_cwe_hub = g["render_cwe_hub"]
render_cwe_full = g["render_cwe_full"]
render_heatmap = g["render_heatmap"]
render_corr_detail = g["render_corr_detail"]
render_terminal_full = g["render_terminal_full"]
render_breach_timeline = g["render_breach_timeline"]
render_research_hub = g["render_research_hub"]
render_market_strip = g["render_market_strip"]
render_owasp_prevalence = g["render_owasp_prevalence"]
render_code_vault = g["render_code_vault"]
render_sim_grid = g["render_sim_grid"]
SIMULATORS = g["SIMULATORS"]
CWE_SIMULATORS = g["CWE_SIMULATORS"]
render_source_links = g["render_source_links"]
render_market_sources = g["render_market_sources"]
render_section_highlights = g["render_section_highlights"]
render_section_highlight_rails = g["render_section_highlight_rails"]
render_sidebar = g["render_sidebar"]
source_links_html = render_source_links()
market_sources_html = render_market_sources()

PAGE_CSS = """
html{overflow-anchor:none}
.toolbar{position:fixed;top:0;left:0;right:0;z-index:200;background:color-mix(in srgb,var(--ok-bg-1) 94%,transparent);backdrop-filter:blur(14px);border-bottom:1px solid var(--ok-line);padding:10px clamp(16px,3vw,40px);display:flex;align-items:center;gap:12px;flex-wrap:wrap}
.toolbar .brand{font-family:var(--ok-mono);font-size:12px;letter-spacing:.12em;text-transform:uppercase;color:var(--ok-accent);margin-right:auto}
.toolbar .ok-input{min-width:200px;flex:1;max-width:360px}
body.ok.theme-light{
  --ok-bg-0:#dce0ea;--ok-bg-1:#ffffff;--ok-bg-2:#f0f2f8;--ok-bg-3:#c8cedc;
  --ok-line:#6e7388;--ok-line-soft:#9aa0b4;--ok-grid:rgba(22,26,48,.11);
  --ok-fg:#0c0e16;--ok-fg-soft:#1e2130;--ok-fg-mute:#3a3e50;--ok-fg-dim:#5c6074;
  --ok-orange:oklch(52% .20 42);--ok-magenta:oklch(48% .24 338);--ok-cyan:oklch(42% .13 208);
  --ok-success:oklch(42% .14 152);--ok-warning:oklch(48% .14 78);--ok-danger:oklch(48% .21 25);
  --ok-accent:var(--ok-orange);--ok-accent-2:var(--ok-magenta);--ok-glow:.22;
  --ok-surface:var(--ok-bg-1);
  color:var(--ok-fg);
}
body.sidebar-collapsed .layout{grid-template-columns:0 1fr}
body.sidebar-collapsed .sidebar{opacity:0;pointer-events:none;overflow:hidden}
.layout{display:grid;grid-template-columns:minmax(248px,292px) minmax(0,1fr);padding-top:56px;min-height:100vh;transition:grid-template-columns .25s}
.sidebar{position:sticky;top:56px;height:calc(100vh - 56px);overflow-y:auto;overflow-x:hidden;border-right:1px solid var(--ok-line);padding:0;background:linear-gradient(180deg,color-mix(in oklch,var(--ok-bg-1) 96%,var(--ok-cyan) 4%) 0%,color-mix(in oklch,var(--ok-bg-0) 98%,var(--ok-magenta) 2%) 100%);transition:opacity .25s;scrollbar-width:thin;scrollbar-color:var(--ok-line) transparent}
.sidebar::-webkit-scrollbar{width:5px}
.sidebar::-webkit-scrollbar-thumb{background:var(--ok-line);border-radius:4px}
.sidebar-head{padding:16px 14px 14px;border-bottom:1px solid var(--ok-line-soft);background:linear-gradient(135deg,color-mix(in oklch,var(--ok-accent) 12%,transparent),color-mix(in oklch,var(--ok-magenta) 8%,transparent),color-mix(in oklch,var(--ok-cyan) 6%,transparent))}
.sidebar-kicker{display:block;font-family:var(--ok-mono);font-size:9px;letter-spacing:.16em;text-transform:uppercase;color:var(--ok-cyan);margin-bottom:4px}
.sidebar-title{display:block;font-size:15px;font-weight:600;color:var(--ok-fg);letter-spacing:-.02em}
.sidebar-ver{display:block;font-family:var(--ok-mono);font-size:10px;color:var(--ok-fg-mute);margin-top:2px}
.nav-group{padding:10px 8px 6px;border-bottom:1px solid var(--ok-line-soft)}
.nav-group[data-group="bridge"]{padding:4px 8px;background:linear-gradient(90deg,color-mix(in oklch,var(--ok-accent) 6%,transparent),color-mix(in oklch,var(--ok-magenta) 6%,transparent))}
.nav-group-hd{display:flex;align-items:center;gap:8px;font-family:var(--ok-mono);font-size:10px;letter-spacing:.12em;text-transform:uppercase;color:var(--ok-fg-mute);margin:0 0 8px 6px;font-weight:600}
.nav-group-dot{width:6px;height:6px;border-radius:50%;background:var(--ok-line);flex-shrink:0}
.nav-group-hd.nav-tone-cyan .nav-group-dot{background:var(--ok-cyan);box-shadow:0 0 8px color-mix(in oklch,var(--ok-cyan) 50%,transparent)}
.nav-group-hd.nav-tone-accent .nav-group-dot{background:var(--ok-accent);box-shadow:0 0 8px color-mix(in oklch,var(--ok-accent) 50%,transparent)}
.nav-group-hd.nav-tone-magenta .nav-group-dot{background:var(--ok-magenta);box-shadow:0 0 8px color-mix(in oklch,var(--ok-magenta) 50%,transparent)}
.nav-group-hd.nav-tone-success .nav-group-dot{background:var(--ok-success);box-shadow:0 0 8px color-mix(in oklch,var(--ok-success) 50%,transparent)}
.nav-group-body{display:flex;flex-direction:column;gap:2px}
.nav-scroll-block{max-height:min(42vh,360px);overflow-y:auto;padding-right:2px;scrollbar-width:thin}
.nav-link{display:flex;align-items:flex-start;gap:8px;padding:7px 10px 7px 8px;font-family:var(--ok-mono);font-size:10px;color:var(--ok-fg-soft);border-radius:var(--ok-r-1);border:1px solid transparent;line-height:1.35;text-decoration:none;transition:background .15s,border-color .15s,color .15s,transform .12s}
.nav-link:hover{transform:translateX(2px)}
.nav-badge{flex-shrink:0;min-width:34px;padding:2px 6px;border-radius:var(--ok-r-1);font-size:9px;font-weight:600;text-align:center;line-height:1.3;background:var(--ok-bg-3);border:1px solid var(--ok-line);color:var(--ok-fg-mute)}
.nav-label{flex:1;min-width:0;word-break:break-word}
.nav-link.nav-hub .nav-badge{background:color-mix(in oklch,var(--ok-accent) 18%,var(--ok-bg-2));border-color:color-mix(in oklch,var(--ok-accent) 35%,var(--ok-line));color:var(--ok-accent)}
.nav-link.nav-bridge .nav-badge{background:linear-gradient(135deg,color-mix(in oklch,var(--ok-accent) 20%,var(--ok-bg-2)),color-mix(in oklch,var(--ok-magenta) 20%,var(--ok-bg-2)));border-color:color-mix(in oklch,var(--ok-magenta) 30%,var(--ok-line));color:var(--ok-fg)}
.nav-tone-cyan .nav-badge{border-color:color-mix(in oklch,var(--ok-cyan) 30%,var(--ok-line));color:var(--ok-cyan)}
.nav-tone-accent .nav-badge{border-color:color-mix(in oklch,var(--ok-accent) 30%,var(--ok-line));color:var(--ok-accent)}
.nav-tone-magenta .nav-badge{border-color:color-mix(in oklch,var(--ok-magenta) 30%,var(--ok-line));color:var(--ok-magenta)}
.nav-tone-warning .nav-badge{border-color:color-mix(in oklch,var(--ok-warning) 30%,var(--ok-line));color:var(--ok-warning)}
.nav-tone-danger .nav-badge{border-color:color-mix(in oklch,var(--ok-danger) 30%,var(--ok-line));color:var(--ok-danger)}
.nav-tone-success .nav-badge{border-color:color-mix(in oklch,var(--ok-success) 30%,var(--ok-line));color:var(--ok-success)}
.nav-tone-hot .nav-badge{background:color-mix(in oklch,var(--ok-magenta) 14%,var(--ok-bg-2));border-color:color-mix(in oklch,var(--ok-magenta) 40%,var(--ok-line));color:var(--ok-magenta)}
.nav-tone-mid .nav-badge{border-color:color-mix(in oklch,var(--ok-cyan) 28%,var(--ok-line));color:var(--ok-cyan)}
.nav-tone-base .nav-badge{opacity:.85}
.nav-link.nav-tone-cyan:hover,.nav-link.nav-tone-cyan.active{background:color-mix(in oklch,var(--ok-cyan) 10%,transparent);border-color:color-mix(in oklch,var(--ok-cyan) 25%,var(--ok-line));color:var(--ok-fg)}
.nav-link.nav-tone-accent:hover,.nav-link.nav-tone-accent.active{background:color-mix(in oklch,var(--ok-accent) 10%,transparent);border-color:color-mix(in oklch,var(--ok-accent) 28%,var(--ok-line));color:var(--ok-fg)}
.nav-link.nav-tone-magenta:hover,.nav-link.nav-tone-magenta.active{background:color-mix(in oklch,var(--ok-magenta) 10%,transparent);border-color:color-mix(in oklch,var(--ok-magenta) 28%,var(--ok-line));color:var(--ok-fg)}
.nav-link.nav-tone-warning:hover,.nav-link.nav-tone-warning.active{background:color-mix(in oklch,var(--ok-warning) 10%,transparent);border-color:color-mix(in oklch,var(--ok-warning) 28%,var(--ok-line));color:var(--ok-fg)}
.nav-link.nav-tone-danger:hover,.nav-link.nav-tone-danger.active{background:color-mix(in oklch,var(--ok-danger) 10%,transparent);border-color:color-mix(in oklch,var(--ok-danger) 28%,var(--ok-line));color:var(--ok-fg)}
.nav-link.nav-tone-success:hover,.nav-link.nav-tone-success.active{background:color-mix(in oklch,var(--ok-success) 10%,transparent);border-color:color-mix(in oklch,var(--ok-success) 28%,var(--ok-line));color:var(--ok-fg)}
.nav-link.nav-tone-hot:hover,.nav-link.nav-tone-hot.active{background:color-mix(in oklch,var(--ok-magenta) 12%,transparent);border-color:color-mix(in oklch,var(--ok-magenta) 32%,var(--ok-line));color:var(--ok-fg)}
.nav-link.nav-tone-mid:hover,.nav-link.nav-tone-mid.active{background:color-mix(in oklch,var(--ok-cyan) 8%,transparent);border-color:color-mix(in oklch,var(--ok-cyan) 22%,var(--ok-line));color:var(--ok-fg)}
.nav-link.nav-tone-base:hover,.nav-link.nav-tone-base.active{background:color-mix(in oklch,var(--ok-bg-3) 80%,transparent);border-color:var(--ok-line);color:var(--ok-fg)}
.nav-link.nav-tone-bridge:hover,.nav-link.nav-tone-bridge.active{background:linear-gradient(90deg,color-mix(in oklch,var(--ok-accent) 10%,transparent),color-mix(in oklch,var(--ok-magenta) 10%,transparent));border-color:color-mix(in oklch,var(--ok-magenta) 25%,var(--ok-line));color:var(--ok-fg)}
.nav-link.active .nav-label{font-weight:600}
.nav-link.done .nav-label::after{content:" ✓";color:var(--ok-success);font-size:9px}
.main{padding:clamp(24px,3vw,48px) clamp(20px,4vw,64px) var(--ok-s-12);max-width:none;width:100%}
.hero{padding:var(--ok-s-8) 0 var(--ok-s-9);border-bottom:1px solid var(--ok-line)}
.hero h1{font-size:clamp(36px,4.5vw,64px);font-weight:500;letter-spacing:-.035em;line-height:1.05;margin:16px 0}
.hero h1 em{color:var(--ok-accent);font-style:normal}
.lede{color:var(--ok-fg-soft);font-size:clamp(17px,1.4vw,20px);line-height:1.65;max-width:820px}
.lesson-sec{padding:clamp(40px,5vw,72px) 0;border-bottom:1px solid var(--ok-line-soft);scroll-margin-top:68px}
.section-label{display:block;font-family:var(--ok-mono);font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:var(--ok-cyan);margin:0 0 12px}
.muted{color:var(--ok-fg-mute);font-size:15px}
body.corr-filtering .lesson-sec:not(.filter-match):not([id="correlacao"]):not([id="mercado"]):not([id="pesquisa"]):not([id="noticias"]):not([id="terminal-lab"]):not([id="code-vault"]):not([id="simuladores"]):not([id="simuladores-cwe"]):not([id="owasp-hub"]):not([id="ponte-owasp-cwe"]):not([id="cwe-hub"]):not([id="intro"]):not([id="juice-setup"]):not([id="juice-ide"]):not([id="quiz"]){display:none}
body.corr-filtering .lesson-sec.filter-match{border-left:4px solid var(--ok-cyan);padding-left:var(--ok-s-6)}
body.search-active .lesson-sec.search-hide{display:none}

.tab-panel{display:none;margin-top:var(--ok-s-6)}
.tab-panel.active{display:block;animation:fadeIn .25s ease}
@keyframes fadeIn{from{opacity:0;transform:translateY(6px)}to{opacity:1;transform:none}}
.tab-panel p,.research-body p{color:var(--ok-fg-soft);line-height:1.72;margin:0 0 16px;font-size:16px}
.ok-tab{cursor:pointer;background:none;border:none;font:inherit;font-size:14px}
.tag-row{display:flex;flex-wrap:wrap;gap:8px;margin-top:16px}
.corr-chip{cursor:pointer}
.ok-link-btn{background:none;border:none;padding:0;font:inherit;color:var(--ok-cyan);cursor:pointer;text-align:left;font-size:16px}
.ok-link-btn:hover{text-decoration:underline}
.grid-2,.split-2{display:grid;grid-template-columns:1fr 1fr;gap:clamp(16px,3vw,32px)}
.dense-list{list-style:none;padding:0;margin:0}
.dense-list li{padding:10px 0;border-bottom:1px solid var(--ok-line-soft);font-size:15px;line-height:1.6;color:var(--ok-fg-soft)}
.dense-list li b{color:var(--ok-fg)}
.ref-list a{color:var(--ok-cyan);text-decoration:underline;text-underline-offset:3px}
.diff-panels{position:relative;min-height:140px}
.diff-panels.tall{min-height:200px}
.diff-panels .code-panel{position:absolute;inset:0;margin:0;padding:18px;overflow:auto;font-family:var(--ok-mono);font-size:13px;line-height:1.65;transition:clip-path .35s ease;background:var(--ok-bg-0)}
.diff-panels .vuln code{color:var(--ok-magenta)}
.diff-panels .fix code{color:var(--ok-success)}
.diff-slider{flex:1;max-width:180px;accent-color:var(--ok-cyan)}
.diff-label{font-family:var(--ok-mono);font-size:11px;color:var(--ok-fg-mute);min-width:80px}
.code-toolbar{display:flex;gap:10px;padding:12px 14px;border-bottom:1px solid var(--ok-line);flex-wrap:wrap;align-items:center;background:var(--ok-bg-2)}
.code-wrap{border:1px solid var(--ok-line);background:var(--ok-bg-0);margin:16px 0;border-radius:var(--ok-r-2)}
.payload-hint{font-family:var(--ok-mono);font-size:13px;color:var(--ok-fg-mute);margin:8px 0}
.payload-hint code{color:var(--ok-magenta)}
.corr-hub{border:1px solid var(--ok-line);background:var(--ok-bg-1);border-radius:var(--ok-r-2);padding:clamp(16px,2vw,28px)}
.corr-toolbar{display:flex;flex-wrap:wrap;align-items:center;gap:12px;margin-bottom:20px;font-size:14px}
.corr-layout{display:grid;grid-template-columns:minmax(0,1fr) minmax(280px,360px);gap:clamp(16px,2vw,28px);align-items:start}
.heatmap-wrap{overflow:auto;max-height:min(75vh,680px);border:1px solid var(--ok-line);background:var(--ok-bg-0);border-radius:var(--ok-r-2);padding:8px;position:sticky;top:68px}
.corr-sidebar{position:sticky;top:68px;max-height:min(75vh,680px);display:flex;flex-direction:column;border:1px solid var(--ok-line);background:var(--ok-bg-0);border-radius:var(--ok-r-2);overflow:hidden}
.corr-list-hd{display:flex;justify-content:space-between;align-items:center;gap:8px;padding:12px 14px;border-bottom:1px solid var(--ok-line);background:var(--ok-bg-2);font-family:var(--ok-mono);font-size:11px;color:var(--ok-fg-mute);flex-shrink:0}
.corr-list-hd strong{color:var(--ok-fg);font-size:12px}
.corr-list-hd span:last-child{color:var(--ok-cyan)}
.heatmap{border-collapse:separate;border-spacing:2px;font-family:var(--ok-mono);font-size:10px;width:100%}
.heatmap th,.heatmap td{padding:0;border:none}
.heatmap .hm-corner{width:48px}
.heatmap .hm-owasp,.heatmap .hm-cwe{cursor:pointer;position:sticky;z-index:3;background:var(--ok-bg-2)}
.heatmap .hm-owasp{left:0;z-index:4}
.heatmap .hm-owasp span,.heatmap .hm-cwe span{display:flex;align-items:center;justify-content:center;padding:6px 4px;font-weight:600;font-size:11px}
.heatmap .hm-owasp span{color:var(--ok-accent)}
.heatmap .hm-cwe span{color:var(--ok-cyan);writing-mode:vertical-rl;height:80px}
.heatmap .hm-owasp.sel span,.heatmap .hm-cwe.sel span{background:color-mix(in oklch,var(--ok-accent) 25%,var(--ok-bg-2))}
.heatmap .hm-cell{width:18px;height:18px;cursor:pointer;transition:transform .12s,box-shadow .12s;border-radius:2px}
.heatmap .hm-cell.s1{background:color-mix(in oklch,var(--ok-cyan) 50%,transparent)}
.heatmap .hm-cell.s2{background:color-mix(in oklch,var(--ok-magenta) 60%,transparent)}
.heatmap .hm-cell.s3{background:var(--ok-accent);box-shadow:0 0 8px color-mix(in oklch,var(--ok-accent) 60%,transparent)}
.heatmap .hm-cell.empty{background:var(--ok-bg-3)}
.heatmap .hm-cell.sel,.heatmap .hm-cell:hover{transform:scale(1.2);outline:2px solid var(--ok-fg);z-index:2}
.corr-list{flex:1;overflow-y:auto;display:flex;flex-direction:column;gap:4px;padding:8px}
.corr-item{display:grid;grid-template-columns:auto 1fr auto;gap:8px 12px;align-items:center;text-align:left;padding:10px 12px;border:1px solid var(--ok-line);background:var(--ok-bg-1);cursor:pointer;font-size:13px;border-radius:var(--ok-r-1);transition:border-color .15s,background .15s,opacity .15s;flex-shrink:0}
.corr-item:hover{border-color:var(--ok-cyan);background:color-mix(in oklch,var(--ok-cyan) 6%,var(--ok-bg-1))}
.corr-item.sel{border-color:var(--ok-accent);background:color-mix(in oklch,var(--ok-accent) 12%,var(--ok-bg-1));box-shadow:0 0 0 1px color-mix(in oklch,var(--ok-accent) 40%,transparent)}
.corr-item.hl{border-color:var(--ok-cyan);background:color-mix(in oklch,var(--ok-cyan) 8%,var(--ok-bg-1))}
.corr-item.dim{opacity:.38}
.corr-id{font-family:var(--ok-mono);font-size:11px;color:var(--ok-accent);white-space:nowrap}
.corr-name{color:var(--ok-fg-soft);line-height:1.4}
.corr-str{font-family:var(--ok-mono);font-size:10px;color:var(--ok-fg-mute)}
.corr-detail{min-height:120px;padding:var(--ok-s-6);border:1px solid var(--ok-line);margin-top:var(--ok-s-5);background:var(--ok-bg-0);border-radius:var(--ok-r-2);font-size:15px;line-height:1.6}
.charts-grid{display:grid;grid-template-columns:minmax(0,2fr) minmax(280px,1fr);gap:var(--ok-s-6);margin:var(--ok-s-6) 0}
.charts-inline-2{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:var(--ok-s-6);margin:var(--ok-s-6) 0;align-items:stretch}
.charts-stack{display:flex;flex-direction:column;gap:var(--ok-s-7);margin:var(--ok-s-6) 0}
.chart-box{border:1px solid var(--ok-line);padding:clamp(18px,2.5vw,28px);background:linear-gradient(165deg,color-mix(in oklch,var(--ok-cyan) 4%,var(--ok-bg-1)) 0%,var(--ok-bg-1) 55%);border-radius:var(--ok-r-2);transition:border-color .2s,box-shadow .2s;display:flex;flex-direction:column;gap:0}
.chart-box:hover{border-color:color-mix(in oklch,var(--ok-cyan) 45%,var(--ok-line));box-shadow:0 8px 32px rgba(0,0,0,.22)}
.chart-hd{margin:0 0 clamp(14px,2vw,20px)}
.chart-hd .section-label{margin-bottom:0}
.chart-sub{margin:8px 0 0;font-size:14px;line-height:1.55;color:var(--ok-fg-soft);max-width:62ch}
.chart-body-split{display:grid;grid-template-columns:minmax(0,1.15fr) minmax(240px,360px);gap:clamp(20px,3vw,32px);align-items:stretch;flex:1}
.chart-body-bar{display:flex;flex-direction:column;gap:14px;flex:1}
.chart-ring-wrap{display:flex;align-items:center;justify-content:center;min-height:300px;padding:clamp(16px,2.5vw,28px);border:1px solid var(--ok-line-soft);border-radius:var(--ok-r-2);background:radial-gradient(ellipse 75% 65% at 50% 42%,color-mix(in oklch,var(--ok-cyan) 9%,transparent) 0%,transparent 70%),var(--ok-bg-0)}
.chart-plot-ranked{padding:clamp(14px,2vw,22px) clamp(12px,1.5vw,18px);border:1px solid var(--ok-line-soft);border-radius:var(--ok-r-2);background:var(--ok-bg-0);min-height:0;display:block;overflow:visible}
.chart-plot{padding:clamp(10px,1.5vw,18px) clamp(6px,1vw,12px);border:1px solid var(--ok-line-soft);border-radius:var(--ok-r-2);background:var(--ok-bg-0);min-height:200px}
.chart-wrap{width:100%;max-width:min(340px,100%);margin:0 auto}
.chart-wrap>canvas,.chart-plot-ranked canvas,.chart-plot canvas,.chart-body-bar canvas{display:block;max-width:100%;margin:0 auto;touch-action:none;cursor:crosshair}
.chart-ranked-wrap .chart-legend-item,.chart-cwe-scores-wrap .chart-legend-item,.chart-delta-wrap .chart-legend-item{grid-template-columns:28px 12px minmax(0,1fr) auto;grid-template-rows:auto auto auto;gap:1px 8px;padding:10px 10px}
.chart-ranked-wrap .chart-legend-rank,.chart-cwe-scores-wrap .chart-legend-rank,.chart-delta-wrap .chart-legend-rank{grid-column:1;grid-row:1;font-size:10px;color:var(--ok-fg-mute);font-weight:700;text-align:center;align-self:center}
.chart-ranked-wrap .chart-legend-swatch,.chart-cwe-scores-wrap .chart-legend-swatch,.chart-delta-wrap .chart-legend-swatch{grid-column:2;grid-row:1;align-self:center;width:12px;height:12px}
.chart-ranked-wrap .chart-legend-label,.chart-cwe-scores-wrap .chart-legend-label,.chart-delta-wrap .chart-legend-label{grid-column:3;grid-row:1;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.chart-ranked-wrap .chart-legend-val,.chart-cwe-scores-wrap .chart-legend-val,.chart-delta-wrap .chart-legend-val{grid-column:4;grid-row:1;white-space:nowrap}
.chart-legend-sub{grid-column:3/span 2;grid-row:2;font-size:10px;color:var(--ok-fg-mute);line-height:1.3;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.chart-ranked-wrap .chart-legend-meter,.chart-cwe-scores-wrap .chart-legend-meter,.chart-delta-wrap .chart-legend-meter{grid-column:2/span 3;grid-row:3;height:3px;margin-top:2px}
.chart-donut-wrap .chart-body-split{grid-template-columns:minmax(0,1fr) minmax(280px,400px)}
.chart-donut-wrap .chart-legend-list{gap:6px;max-height:min(480px,62vh)}
.chart-donut-wrap .chart-legend-item{grid-template-columns:16px minmax(0,1fr) auto;grid-template-rows:auto auto auto;gap:5px 12px;padding:11px 13px;border:1px solid var(--ok-line-soft);background:var(--ok-bg-1);font-size:13px;color:var(--ok-fg)}
.chart-donut-wrap .chart-legend-swatch{grid-column:1;grid-row:1;width:16px;height:16px;border-radius:4px;align-self:center;box-shadow:none;border:1px solid color-mix(in oklch,#000 14%,transparent)}
.chart-donut-wrap .chart-legend-label{grid-column:2;grid-row:1;color:var(--ok-fg);font-size:14px;font-weight:700;letter-spacing:.05em}
.chart-donut-wrap .chart-legend-val{grid-column:3;grid-row:1;color:var(--ok-fg);font-size:14px;font-weight:800;font-variant-numeric:tabular-nums}
.chart-donut-wrap .chart-legend-sub{grid-column:2/span 2;grid-row:2;font-size:11px;color:var(--ok-fg-mute);font-weight:500}
.chart-donut-wrap .chart-legend-meter{grid-column:1/span 3;grid-row:3;height:6px;background:var(--ok-bg-3);margin-top:0}
.chart-donut-wrap .chart-legend-meter i{opacity:1;min-height:6px}
.chart-ranked-wrap .chart-body-split,.chart-cwe-scores-wrap .chart-body-split,.chart-delta-wrap .chart-body-split{align-items:start}
.chart-cwe-scores-wrap .chart-body-split{grid-template-columns:minmax(0,1.35fr) minmax(260px,340px)}
.chart-delta-wrap .chart-body-split{grid-template-columns:minmax(0,1.2fr) minmax(280px,380px)}
.chart-delta-wrap .chart-legend-list{max-height:min(420px,58vh)}
.chart-cwe-scores-wrap .chart-legend-list{max-height:min(440px,58vh)}

.chart-legend-panel{border:1px solid var(--ok-line-soft);border-radius:var(--ok-r-2);padding:14px 16px;background:var(--ok-bg-0);display:flex;flex-direction:column;min-height:0}
.chart-legend-panel--compact{padding:10px 12px;margin-top:2px}
.chart-legend-title{display:block;font-family:var(--ok-mono);font-size:10px;letter-spacing:.14em;text-transform:uppercase;color:var(--ok-fg-mute);margin-bottom:12px;padding-bottom:8px;border-bottom:1px solid var(--ok-line-soft)}
.chart-legend-list{display:flex;flex-direction:column;gap:3px;flex:1;overflow-y:auto;max-height:min(300px,50vh)}
.chart-legend-panel--compact .chart-legend-list{display:grid;grid-template-columns:repeat(auto-fill,minmax(128px,1fr));gap:6px 10px;max-height:none;overflow:visible}
.chart-legend-item{display:grid;grid-template-columns:12px 1fr auto;grid-template-rows:auto auto;gap:2px 10px;align-items:center;width:100%;padding:8px 10px;border:1px solid transparent;border-radius:var(--ok-r-1);background:transparent;cursor:pointer;text-align:left;font-family:var(--ok-mono);font-size:11px;color:var(--ok-fg-soft);transition:background .15s,border-color .15s}
.chart-legend-item:hover,.chart-legend-item.active{background:color-mix(in oklch,var(--ok-cyan) 11%,var(--ok-bg-1));border-color:color-mix(in oklch,var(--ok-cyan) 38%,var(--ok-line))}
.chart-legend-swatch{grid-row:1/span 2;width:12px;height:12px;border-radius:3px;box-shadow:0 0 0 1px var(--ok-line)}
.chart-legend-label{grid-column:2;color:var(--ok-fg);font-size:13px;line-height:1.3;font-weight:600}
.chart-legend-val{grid-column:3;grid-row:1;color:var(--ok-fg);font-weight:800;font-size:13px;font-variant-numeric:tabular-nums}
.chart-legend-meter{grid-column:2/span 2;height:5px;border-radius:99px;background:var(--ok-bg-3);overflow:hidden;margin-top:2px}
.chart-legend-meter i{display:block;height:100%;border-radius:99px;opacity:1;transition:width .25s ease}
.chart-legend{font-family:var(--ok-mono);font-size:13px;color:var(--ok-fg-soft);margin-top:10px;line-height:1.5}
.chart-hint{display:flex;align-items:center;gap:8px;font-family:var(--ok-mono);font-size:10px;letter-spacing:.06em;text-transform:uppercase;color:var(--ok-fg-mute);margin:14px 0 0;padding-top:12px;border-top:1px solid var(--ok-line-soft)}
.chart-hint-ico{color:var(--ok-cyan);font-size:12px}
.chart-guide{margin:10px 0 0;font-size:13px;line-height:1.55;color:var(--ok-fg-soft);max-width:68ch}
.chart-guide strong{color:var(--ok-cyan);font-weight:600}
.chart-takeaway{margin:8px 0 0;padding:10px 14px;font-size:13px;line-height:1.5;color:var(--ok-fg);border-left:3px solid var(--ok-magenta);background:color-mix(in oklch,var(--ok-magenta) 6%,var(--ok-bg-0));border-radius:0 var(--ok-r-1) var(--ok-r-1) 0;max-width:68ch}
.chart-delta-key{display:flex;flex-wrap:wrap;align-items:center;justify-content:center;gap:12px 20px;margin:0 0 14px;padding:10px 14px;border:1px solid var(--ok-line-soft);border-radius:var(--ok-r-1);background:var(--ok-bg-0);font-family:var(--ok-mono);font-size:11px}
.delta-key.up{color:#ff8f5c}.delta-key.down{color:var(--ok-cyan)}.delta-key.mid{color:var(--ok-fg-mute);opacity:.7}
.chart-delta-wrap .chart-plot-ranked{min-height:320px}
.chart-cwe-scores-wrap .chart-plot-ranked,.chart-delta-wrap .chart-plot-ranked{min-height:0}
.cwe-ladder-box{padding-bottom:clamp(18px,2.5vw,24px)}
.cwe-rank-ladder{display:flex;flex-direction:column;gap:6px}
.cwe-ladder-row{display:grid;grid-template-columns:44px 1fr auto auto;gap:10px 14px;align-items:center;width:100%;padding:12px 14px;border:1px solid var(--ok-line-soft);border-radius:var(--ok-r-2);background:var(--ok-bg-0);cursor:pointer;text-align:left;transition:border-color .15s,background .15s}
.cwe-ladder-row:hover,.cwe-ladder-row:focus-visible{border-color:var(--ok-cyan);background:color-mix(in oklch,var(--ok-cyan) 7%,var(--ok-bg-0));outline:none}
.cwe-ladder-rank{font-family:var(--ok-mono);font-size:20px;font-weight:700;color:var(--ok-magenta);line-height:1}
.cwe-ladder-body{display:flex;flex-direction:column;gap:2px;min-width:0}
.cwe-ladder-id{font-family:var(--ok-mono);font-size:10px;color:var(--ok-fg-mute);letter-spacing:.04em}
.cwe-ladder-name{font-size:14px;font-weight:600;color:var(--ok-fg);line-height:1.3}
.cwe-ladder-move{font-size:12px;color:var(--ok-fg-soft);line-height:1.35}
.cwe-ladder-move strong{color:var(--ok-cyan);font-weight:600}
.cwe-ladder-score{font-family:var(--ok-mono);font-size:12px;font-weight:700;color:var(--ok-magenta);white-space:nowrap}
.cwe-ladder-trend{font-family:var(--ok-mono);font-size:11px;font-weight:700;padding:4px 8px;border-radius:99px;white-space:nowrap}
.cwe-ladder-trend.up{color:#ff8f5c;background:color-mix(in oklch,#ff6b35 14%,transparent)}
.cwe-ladder-trend.down{color:var(--ok-cyan);background:color-mix(in oklch,var(--ok-cyan) 12%,transparent)}
.cwe-ladder-trend.flat{color:var(--ok-fg-mute);background:var(--ok-bg-3)}
@media(max-width:700px){.cwe-ladder-row{grid-template-columns:40px 1fr;grid-template-rows:auto auto}.cwe-ladder-score,.cwe-ladder-trend{grid-column:2}}
.chart-tooltip{position:fixed;z-index:500;pointer-events:none;padding:12px 16px;max-width:280px;background:var(--ok-bg-0);border:1px solid var(--ok-cyan);border-radius:var(--ok-r-2);font-family:var(--ok-mono);font-size:12px;line-height:1.55;opacity:0;transform:translateY(4px);transition:opacity .12s,transform .12s;box-shadow:0 16px 40px rgba(0,0,0,.5)}
.chart-tooltip.visible{opacity:1;transform:translateY(0)}
.chart-tooltip strong{display:block;font-size:14px;color:var(--ok-fg);margin-bottom:6px;font-weight:600}
.chart-tooltip span{display:block;color:var(--ok-fg-soft);margin-top:2px}
.chart-tooltip em{font-style:normal;color:var(--ok-cyan)}
.chart-corr-viz{width:100%;margin-bottom:var(--ok-s-6)}
.news-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(min(100%,420px),1fr));gap:var(--ok-s-6);margin-top:var(--ok-s-6)}
.news-card{position:relative;border:1px solid var(--ok-line);background:var(--ok-bg-1);border-radius:var(--ok-r-2);overflow:hidden;transition:border-color .2s,transform .15s,box-shadow .2s;min-height:320px}
.news-card:hover{border-color:color-mix(in oklch,var(--ok-cyan) 40%,var(--ok-line));transform:translateY(-3px);box-shadow:0 12px 40px color-mix(in oklch,#000 18%,transparent)}
.news-card.search-hide{display:none}
.news-card-accent{position:absolute;left:0;top:0;bottom:0;width:4px;background:var(--ok-line)}
.news-tag-mercado .news-card-accent{background:var(--ok-cyan)}
.news-tag-cwe .news-card-accent{background:var(--ok-magenta)}
.news-tag-owasp .news-card-accent{background:var(--ok-accent)}
.news-tag-incidente .news-card-accent{background:var(--ok-warning)}
.news-tag-pesquisa .news-card-accent{background:var(--ok-success)}
.news-card-inner{display:flex;flex-direction:column;min-height:100%;padding:22px 24px 20px 28px;gap:0}
.news-card-hd{margin-bottom:14px}
.news-card-top{display:flex;align-items:center;justify-content:space-between;gap:10px;margin-bottom:10px}
.news-date{font-family:var(--ok-mono);font-size:12px;color:var(--ok-fg-mute)}
.news-tag{font-family:var(--ok-mono);font-size:10px;text-transform:uppercase;letter-spacing:.08em;padding:4px 10px;border-radius:var(--ok-r-1);border:1px solid var(--ok-line);font-weight:500}
.news-tag.mercado{color:var(--ok-cyan);border-color:color-mix(in oklch,var(--ok-cyan) 35%,var(--ok-line));background:color-mix(in oklch,var(--ok-cyan) 8%,transparent)}
.news-tag.cwe{color:var(--ok-magenta);border-color:color-mix(in oklch,var(--ok-magenta) 35%,var(--ok-line));background:color-mix(in oklch,var(--ok-magenta) 8%,transparent)}
.news-tag.owasp{color:var(--ok-accent);border-color:color-mix(in oklch,var(--ok-accent) 35%,var(--ok-line));background:color-mix(in oklch,var(--ok-accent) 8%,transparent)}
.news-tag.incidente{color:var(--ok-warning);border-color:color-mix(in oklch,var(--ok-warning) 35%,var(--ok-line));background:color-mix(in oklch,var(--ok-warning) 8%,transparent)}
.news-tag.pesquisa{color:var(--ok-success);border-color:color-mix(in oklch,var(--ok-success) 35%,var(--ok-line));background:color-mix(in oklch,var(--ok-success) 8%,transparent)}
.news-source{display:block;font-family:var(--ok-mono);font-size:11px;color:var(--ok-cyan);letter-spacing:.06em;text-transform:uppercase;margin-bottom:8px}
.news-title{font-size:clamp(18px,2vw,22px);font-weight:600;margin:0 0 8px;line-height:1.3;color:var(--ok-fg)}
.news-impact{display:inline-block;font-family:var(--ok-mono);font-size:11px;color:var(--ok-warning);background:color-mix(in oklch,var(--ok-warning) 10%,transparent);padding:4px 10px;border-radius:var(--ok-r-1);border:1px solid color-mix(in oklch,var(--ok-warning) 25%,var(--ok-line))}
.news-card-body{flex:1;display:flex;flex-direction:column;gap:12px}
.news-summary{font-size:15px;color:var(--ok-fg-soft);line-height:1.65;margin:0}
.news-body{font-size:14px;color:var(--ok-fg-mute);line-height:1.6;margin:0}
.news-stats{display:flex;flex-wrap:wrap;gap:8px}
.news-stat{font-family:var(--ok-mono);font-size:11px;padding:6px 12px;border-radius:var(--ok-r-1);background:var(--ok-bg-2);border:1px solid var(--ok-line-soft);color:var(--ok-fg-soft)}
.news-stat b{color:var(--ok-fg);font-weight:600;margin-right:4px}
.news-bullets{margin:0;padding:0 0 0 18px;display:flex;flex-direction:column;gap:6px}
.news-bullets li{font-size:14px;line-height:1.55;color:var(--ok-fg-soft)}
.news-meta{display:flex;align-items:center;justify-content:space-between;gap:12px;flex-wrap:wrap;margin-top:18px;padding-top:16px;border-top:1px solid var(--ok-line-soft)}
.news-corr{display:flex;flex-wrap:wrap;gap:6px}
.news-source-btn{flex-shrink:0}
.methodology-note{margin-top:var(--ok-s-6);padding:var(--ok-s-5) var(--ok-s-6);border:1px solid var(--ok-line);background:color-mix(in oklch,var(--ok-cyan) 6%,var(--ok-bg-1));border-radius:var(--ok-r-2);font-size:15px;line-height:1.7;color:var(--ok-fg-soft)}
.methodology-note strong{color:var(--ok-fg)}
.hl-section{margin:var(--ok-s-7) 0 var(--ok-s-8)}
.hl-stack{display:flex;flex-direction:column;gap:var(--ok-s-5)}
.hl-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:var(--ok-s-5)}
.hl-grid.hl-grid-single{grid-template-columns:repeat(2,minmax(0,1fr))}
.hl-grid.hl-grid-single .hl-block{grid-column:1/-1;max-width:calc(50% - var(--ok-s-5)/2)}
.hl-rail-spread+.hl-rail-spread{margin-top:var(--ok-s-6)}
.hl-sec-bridge{padding:var(--ok-s-6) 0;border-top:1px solid var(--ok-line-soft);border-bottom:1px solid var(--ok-line-soft);margin:var(--ok-s-7) 0;background:color-mix(in oklch,var(--ok-bg-2) 40%,transparent)}
.hl-block{border:1px solid var(--ok-line);border-radius:var(--ok-r-2);background:var(--ok-bg-1);overflow:hidden;display:flex;flex-direction:column;min-height:280px;transition:border-color .2s,box-shadow .2s,transform .15s}
.hl-block:hover{box-shadow:0 10px 36px color-mix(in oklch,#000 16%,transparent);transform:translateY(-2px)}
.hl-block.hl-highlight{border-top:3px solid var(--ok-cyan)}
.hl-block.hl-caso{border-top:3px solid var(--ok-magenta)}
.hl-block.hl-aprendizado{border-top:3px solid var(--ok-success)}
.hl-block.hl-pos{border-top:3px solid var(--ok-accent);background:color-mix(in oklch,var(--ok-accent) 5%,var(--ok-bg-1))}
.hl-block.hl-quote{border-top:3px solid var(--ok-fg-mute)}
.hl-block.hl-excerpt{border-top:3px solid color-mix(in oklch,var(--ok-cyan) 60%,var(--ok-line))}
.hl-block.hl-mencao{border-top:3px solid var(--ok-warning);background:color-mix(in oklch,var(--ok-warning) 4%,var(--ok-bg-1))}
.hl-quote-text{margin:0;padding:16px 20px;border-left:3px solid var(--ok-fg-mute);background:color-mix(in oklch,var(--ok-bg-2) 80%,transparent);border-radius:0 var(--ok-r-1) var(--ok-r-1) 0;font-size:16px;line-height:1.7;color:var(--ok-fg-soft);font-style:italic}
.hl-mencao-lede{margin-bottom:8px!important}
.hl-mencao-author{display:block;font-family:var(--ok-mono);font-size:12px;color:var(--ok-fg-mute);font-style:normal;margin-top:4px}
.hl-rail{margin:var(--ok-s-6) 0}
.hl-rail-hd{display:flex;align-items:baseline;justify-content:space-between;gap:12px;margin-bottom:var(--ok-s-4)}
.hl-rail-hd .section-label{margin:0}
.hl-rail-sub{font-size:13px;color:var(--ok-fg-mute)}
.hl-hd{padding:20px 24px 16px;border-bottom:1px solid var(--ok-line-soft);background:color-mix(in oklch,var(--ok-bg-2) 50%,transparent)}
.hl-hd-top{display:flex;align-items:flex-start;justify-content:space-between;gap:12px;margin-bottom:10px}
.hl-kicker{display:inline-flex;align-items:center;gap:8px;font-family:var(--ok-mono);font-size:11px;letter-spacing:.1em;text-transform:uppercase;color:var(--ok-fg-mute)}
.hl-ico{font-size:15px;letter-spacing:0;text-transform:none}
.hl-title{margin:10px 0 0;font-size:clamp(18px,2vw,22px);font-weight:600;line-height:1.3;color:var(--ok-fg)}
.hl-tags{display:flex;flex-wrap:wrap;gap:8px;margin-top:10px}
.hl-tag{font-size:11px!important;cursor:pointer}
.hl-source-link{display:inline-flex;align-items:center;gap:6px;font-family:var(--ok-mono);font-size:11px;color:var(--ok-cyan);text-decoration:none;padding:6px 12px;border:1px solid color-mix(in oklch,var(--ok-cyan) 30%,var(--ok-line));border-radius:var(--ok-r-1);background:color-mix(in oklch,var(--ok-cyan) 6%,transparent);flex-shrink:0;transition:background .15s,border-color .15s}
.hl-source-link:hover{background:color-mix(in oklch,var(--ok-cyan) 12%,transparent);border-color:var(--ok-cyan)}
.hl-source-link.muted{color:var(--ok-fg-mute);cursor:default;border-color:var(--ok-line-soft);background:transparent}
.hl-source-ico{font-size:12px}
.hl-body{padding:18px 24px 20px;flex:1;display:flex;flex-direction:column;gap:14px}
.hl-lede{margin:0;font-size:15px;line-height:1.7;color:var(--ok-fg-soft)}
.hl-detail p{margin:0 0 10px;font-size:14px;line-height:1.65;color:var(--ok-fg-mute)}
.hl-detail p:last-child{margin-bottom:0}
.hl-stats{display:grid;grid-template-columns:repeat(auto-fill,minmax(100px,1fr));gap:10px}
.hl-stat{padding:12px 14px;border-radius:var(--ok-r-1);background:var(--ok-bg-2);border:1px solid var(--ok-line-soft);text-align:center}
.hl-stat-val{display:block;font-family:var(--ok-mono);font-size:18px;font-weight:700;color:var(--ok-fg);line-height:1.2}
.hl-stat-lbl{display:block;font-size:10px;color:var(--ok-fg-mute);margin-top:4px;line-height:1.3}
.hl-bullets-wrap{padding:14px 16px;border-radius:var(--ok-r-1);background:color-mix(in oklch,var(--ok-bg-2) 90%,transparent);border:1px solid var(--ok-line-soft)}
.hl-bullets-k{display:block;font-family:var(--ok-mono);font-size:10px;letter-spacing:.1em;text-transform:uppercase;color:var(--ok-fg-mute);margin-bottom:10px}
.hl-bullets{margin:0;padding:0 0 0 18px;display:flex;flex-direction:column;gap:8px}
.hl-bullets li{font-size:14px;line-height:1.55;color:var(--ok-fg-soft)}
.hl-why{padding:12px 14px;border-left:2px solid var(--ok-accent);background:color-mix(in oklch,var(--ok-accent) 6%,transparent);border-radius:0 var(--ok-r-1) var(--ok-r-1) 0}
.hl-why-k{display:block;font-family:var(--ok-mono);font-size:10px;letter-spacing:.1em;text-transform:uppercase;color:var(--ok-accent);margin-bottom:8px}
.hl-why p{margin:0;font-size:14px;line-height:1.6;color:var(--ok-fg-soft)}
.hl-takeaway{padding:16px 24px 20px;border-top:1px solid var(--ok-line-soft);background:color-mix(in oklch,var(--ok-bg-2) 70%,transparent);margin-top:auto}
.hl-takeaway-k{display:block;font-family:var(--ok-mono);font-size:10px;letter-spacing:.12em;text-transform:uppercase;color:var(--ok-accent);margin-bottom:8px;font-weight:600}
.hl-takeaway p{margin:0;font-size:15px;line-height:1.55;color:var(--ok-fg)}
.hl-modal-stack{display:flex;flex-direction:column;gap:var(--ok-s-4);margin-top:var(--ok-s-4)}
.modal-hl-section{margin:var(--ok-s-6) 0 var(--ok-s-4)}
.modal-hl-section.caso-extra{margin-top:var(--ok-s-6);padding-top:var(--ok-s-5);border-top:1px solid var(--ok-line-soft)}
.hl-block.hl-compact{min-height:0}
.hl-block.hl-compact .hl-hd{padding:14px 18px 12px}
.hl-block.hl-compact .hl-body{padding:12px 18px}
.hl-block.hl-compact .hl-title{font-size:17px}
@media(max-width:768px){.hl-grid{grid-template-columns:1fr}.hl-grid.hl-grid-single .hl-block{max-width:100%}}
.trend.up{color:var(--ok-danger)}.trend.down{color:var(--ok-success)}.trend.flat{color:var(--ok-fg-mute)}
.source-bar{display:flex;flex-wrap:wrap;gap:10px;margin:var(--ok-s-6) 0 var(--ok-s-7)}
.source-link{display:flex;flex-direction:column;padding:12px 16px;border:1px solid var(--ok-line);background:var(--ok-bg-1);border-radius:var(--ok-r-2);text-decoration:none;min-width:160px;flex:1;transition:border-color .15s,background .15s}
.source-link:hover{border-color:var(--ok-cyan);background:color-mix(in oklch,var(--ok-cyan) 6%,var(--ok-bg-1))}
.source-name{font-size:14px;font-weight:500;color:var(--ok-fg)}
.source-desc{font-family:var(--ok-mono);font-size:10px;color:var(--ok-fg-mute);margin-top:4px}
.sim-grid{display:grid;grid-template-columns:1fr;gap:var(--ok-s-6)}
#simuladores{--sim-accent:var(--ok-orange);--sim-accent-soft:color-mix(in oklch,var(--ok-orange) 4%,var(--ok-bg-2));padding-top:var(--ok-s-6);border-top:2px solid color-mix(in oklch,var(--ok-orange) 28%,var(--ok-line))}
#simuladores-cwe{--sim-accent:oklch(72% 0.18 292);--sim-accent-soft:color-mix(in oklch,oklch(72% 0.18 292) 4%,var(--ok-bg-2));margin-top:var(--ok-s-9);padding:clamp(18px,2.5vw,28px);border:1px solid var(--ok-line);border-radius:var(--ok-r-2);background:var(--ok-bg-1);box-shadow:none}
#simuladores-cwe::before{content:"";display:block;height:2px;margin:0 0 var(--ok-s-5);border-radius:2px;background:linear-gradient(90deg,color-mix(in oklch,var(--sim-accent) 35%,transparent),transparent 70%)}
#simuladores-cwe .ok-sec-hd h2 em{color:var(--sim-accent)}
#simuladores .ok-sec-hd h2 em{color:var(--ok-orange)}
.sim-owasp-badge{font-family:var(--ok-mono);font-size:10px;padding:2px 8px;border:1px solid var(--ok-cyan);border-radius:var(--ok-r-1);color:var(--ok-cyan);margin-left:6px;letter-spacing:.06em}
.sim-cwe-badge{font-family:var(--ok-mono);font-size:10px;padding:2px 8px;border:1px solid var(--sim-accent,oklch(72% 0.22 292));border-radius:var(--ok-r-1);color:var(--sim-accent,oklch(72% 0.22 292));letter-spacing:.06em}
.sim-cwe-id{font-family:var(--ok-mono);font-size:10px;color:var(--ok-fg-mute);margin-left:4px}
.sim-sec-divider{height:1px;background:var(--ok-line);margin:var(--ok-s-8) 0;border:none}
.sim-box .section-label{display:flex;align-items:center;flex-wrap:wrap;gap:4px}
.sim-box{padding:var(--ok-s-5);border:1px solid var(--ok-line);background:var(--ok-bg-1);border-radius:var(--ok-r-2);transition:border-color .2s,box-shadow .2s}
#simuladores .sim-box-owasp,#simuladores-cwe .sim-box-cwe{background:var(--ok-bg-1)}
#simuladores .sim-box.vuln,#simuladores-cwe .sim-box.vuln{border-color:color-mix(in oklch,var(--sim-accent) 45%,var(--ok-line));box-shadow:none}
.sim-box.latent{border-color:var(--ok-warning);box-shadow:0 0 0 1px color-mix(in oklch,var(--ok-warning) 25%,transparent)}
.sim-box.fixed{border-color:var(--ok-success);box-shadow:0 0 0 1px color-mix(in oklch,var(--ok-success) 30%,transparent)}
.sim-box.safe{border-color:var(--ok-success)}
.sim-box.sim-flash{animation:simFlash .5s ease}
@keyframes simFlash{0%{box-shadow:0 0 0 0 transparent}40%{box-shadow:0 0 0 2px color-mix(in oklch,var(--sim-accent) 22%,transparent)}100%{box-shadow:none}}
#simuladores .sim-run-owasp{--c:var(--ok-orange)}
#simuladores-cwe .sim-run-cwe{--c:var(--sim-accent);background:color-mix(in oklch,var(--sim-accent) 88%,var(--ok-bg-0));color:var(--ok-bg-0);font-weight:600;border:1px solid color-mix(in oklch,var(--sim-accent) 55%,var(--ok-line))}
#simuladores-cwe .sim-run-cwe:hover{box-shadow:0 0 calc(var(--ok-glow-px) * 0.6) -2px color-mix(in oklch,var(--sim-accent) 45%,transparent)}
.sim-output .dim,.jwt-decode .dim{color:var(--ok-fg-mute);font-style:italic}
.sim-box .section-label{margin-bottom:8px}
.sim-actions button{position:relative;z-index:3}
.sim-actions{display:flex;gap:8px;margin-top:10px;flex-wrap:wrap;align-items:center}
.sim-actions .sim-btn-info{font-weight:600;letter-spacing:.02em}
.sim-preview{margin-top:10px;padding:14px;background:var(--ok-bg-0);border:1px solid var(--ok-line);border-radius:var(--ok-r-1);min-height:60px;font-size:14px}
.sim-preview.xss-frame{border:2px dashed var(--ok-line);background:#fff;color:#111}
.sim-status{display:inline-block;margin-top:10px;padding:6px 12px;font-family:var(--ok-mono);font-size:11px;border-radius:var(--ok-r-1);letter-spacing:.04em}
#simuladores .sim-status.danger,#simuladores-cwe .sim-status.danger{background:color-mix(in oklch,var(--sim-accent) 8%,var(--ok-bg-2));color:var(--sim-accent);border:1px solid color-mix(in oklch,var(--sim-accent) 22%,var(--ok-line))}
.sim-status.safe{background:color-mix(in oklch,var(--ok-success) 8%,var(--ok-bg-2));color:var(--ok-success);border:1px solid color-mix(in oklch,var(--ok-success) 22%,var(--ok-line))}
.sim-status.latent{background:color-mix(in oklch,var(--ok-warning) 8%,var(--ok-bg-2));color:var(--ok-warning);border:1px solid color-mix(in oklch,var(--ok-warning) 22%,var(--ok-line))}
.sim-status.fixed{background:color-mix(in oklch,var(--ok-success) 8%,var(--ok-bg-2));color:var(--ok-success);border:1px solid color-mix(in oklch,var(--ok-success) 22%,var(--ok-line))}
.sim-status.warn{background:color-mix(in oklch,var(--ok-warning) 8%,var(--ok-bg-2));color:var(--ok-warning);border:1px solid color-mix(in oklch,var(--ok-warning) 22%,var(--ok-line))}
.sim-panels{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-top:10px}
.sim-panel{border:1px solid var(--ok-line);border-radius:var(--ok-r-1);overflow:hidden;min-height:120px}
.sim-panel-hd{padding:8px 12px;font-family:var(--ok-mono);font-size:10px;letter-spacing:.1em;text-transform:uppercase;border-bottom:1px solid var(--ok-line)}
#simuladores .sim-panel.vuln .sim-panel-hd,#simuladores-cwe .sim-panel.vuln .sim-panel-hd{background:var(--ok-bg-2);color:var(--sim-accent);border-left:3px solid color-mix(in oklch,var(--sim-accent) 55%,var(--ok-line))}
.sim-panel.fix .sim-panel-hd{background:var(--ok-bg-2);color:var(--ok-success);border-left:3px solid color-mix(in oklch,var(--ok-success) 50%,var(--ok-line))}
.sim-output,.jwt-decode,.sim-ide-out{font-family:var(--ok-mono);font-size:12px;line-height:1.6;color:var(--ok-fg-soft)}
.sim-output,.jwt-decode{background:var(--ok-bg-0);min-height:100px;padding:14px}
.sim-ide{background:var(--ok-bg-0);min-height:180px;display:flex;flex-direction:column}
.sim-ide-topbar{display:flex;align-items:center;gap:10px;padding:8px 12px;border-bottom:1px solid var(--ok-line);background:var(--ok-bg-2);font-family:var(--ok-mono);font-size:10px;color:var(--ok-fg-mute)}
.sim-ide-topbar .dots span{display:inline-block;width:8px;height:8px;border-radius:50%;margin-right:4px;background:var(--ok-line)}
.sim-ide-topbar .dots span:nth-child(1){background:#ff5f57}.sim-ide-topbar .dots span:nth-child(2){background:#febc2e}.sim-ide-topbar .dots span:nth-child(3){background:#28c840}
.sim-ide-topbar .fname{color:var(--ok-cyan);margin-left:4px}
.sim-ide-out{flex:1;padding:12px 14px;max-height:280px;overflow-y:auto;background:var(--ok-bg-0)}
.sim-ide-out .line{padding:2px 0;white-space:pre-wrap;word-break:break-word}
.sim-ide-out .line.cmd{color:var(--ok-accent)}
.sim-ide-out .line.out{color:var(--ok-fg-soft)}
.sim-ide-out .line.ok{color:var(--ok-success)}
.sim-ide-out .line.warn{color:var(--ok-warning)}
.sim-ide-out .line.err{color:var(--ok-magenta)}
.sim-ide-out .line.dim{color:var(--ok-fg-mute);font-style:italic}
.sim-ide-out .line.http{color:var(--ok-cyan);font-weight:500}
.sim-ide-out .line.del{color:var(--ok-magenta);background:color-mix(in oklch,var(--ok-magenta) 8%,transparent);padding:2px 6px;border-radius:2px;margin:2px 0}
.sim-ide-out .line.add{color:var(--ok-success);background:color-mix(in oklch,var(--ok-success) 8%,transparent);padding:2px 6px;border-radius:2px;margin:2px 0}
.sim-vuln-idle{padding:14px}
.sim-fix-hint{margin:12px 0 0;font-size:12px;color:var(--ok-fg-mute);font-family:var(--ok-sans,var(--ok-display))}
.sim-fix-hint strong{color:var(--ok-success)}
.sim-btn-fix{background:var(--ok-success)!important;color:var(--ok-bg-0)!important;border-color:var(--ok-success)!important}
.sim-btn-fix:disabled{opacity:.5;cursor:not-allowed}
.sim-output .q{color:var(--ok-cyan)}#simuladores .sim-output .attack,#simuladores-cwe .sim-output .attack{color:var(--sim-accent);font-weight:500}.sim-output .warn{color:var(--ok-warning)}.sim-output .ok{color:var(--ok-success)}
.sim-code-label{font-family:var(--ok-mono);font-size:9px;letter-spacing:.12em;text-transform:uppercase;margin:10px 0 4px}
#simuladores .sim-code-label.vuln,#simuladores-cwe .sim-code-label.vuln{color:var(--sim-accent)}.sim-code-label.fix{color:var(--ok-success)}
.sim-vuln-idle code,.sim-ide-out code{display:block;margin:4px 0 8px;padding:10px;background:var(--ok-bg-1);border:1px solid var(--ok-line);border-radius:var(--ok-r-1);white-space:pre-wrap;font-size:11px}
#simuladores .sim-code-vuln,#simuladores-cwe .sim-code-vuln{color:var(--sim-accent);border-color:color-mix(in oklch,var(--sim-accent) 22%,var(--ok-line))!important;background:var(--ok-bg-1)!important}
.sim-code-fix{color:var(--ok-success);border-color:color-mix(in oklch,var(--ok-success) 22%,var(--ok-line))!important;background:var(--ok-bg-1)!important}
.sim-mitiga-result{margin:10px 0;padding:10px 12px;border-radius:var(--ok-r-1);font-size:11px;line-height:1.55;white-space:pre-wrap;border:1px solid var(--ok-line)}
.sim-mitiga-result.blocked{background:var(--ok-bg-1);color:var(--ok-success);border-color:color-mix(in oklch,var(--ok-success) 22%,var(--ok-line))}
.sim-mitiga-result.latent{background:var(--ok-bg-1);color:var(--ok-warning);border-color:color-mix(in oklch,var(--ok-warning) 22%,var(--ok-line))}
#simuladores .sim-mitiga-result.invalid,#simuladores-cwe .sim-mitiga-result.invalid{background:var(--ok-bg-1);color:var(--sim-accent);border-color:color-mix(in oklch,var(--sim-accent) 18%,var(--ok-line))}

.jwt-decode .danger{color:var(--ok-magenta)}.jwt-decode .ok{color:var(--ok-success)}
@media(max-width:900px){.sim-panels{grid-template-columns:1fr}}
.juice-ide-lede{font-size:15px;line-height:1.6;color:var(--ok-fg-soft);margin:0 0 var(--ok-s-6);max-width:72ch}
.vscode-shell{display:grid;grid-template-columns:minmax(200px,260px) minmax(0,1fr);min-height:min(78vh,820px);border:1px solid var(--ok-line);border-radius:var(--ok-r-2);overflow:hidden;background:var(--ok-bg-0);box-shadow:0 12px 40px rgba(0,0,0,.28)}
.vscode-sidebar{display:flex;flex-direction:column;border-right:1px solid var(--ok-line);background:var(--ok-bg-1);min-height:0}
.vscode-sidebar-hd{display:flex;flex-direction:column;gap:2px;padding:12px 14px 10px;font-family:var(--ok-mono);font-size:10px;letter-spacing:.12em;text-transform:uppercase;color:var(--ok-fg-mute);border-bottom:1px solid var(--ok-line-soft)}
.vscode-root{color:var(--ok-cyan);font-size:9px;letter-spacing:.08em;text-transform:none}
.vscode-tree{flex:1;overflow-y:auto;padding:8px 6px 12px}
.ide-tree-folder{margin-bottom:4px}
.ide-tree-dir{display:flex;align-items:center;gap:6px;width:100%;padding:6px 8px;border:none;background:transparent;color:var(--ok-fg-soft);font-family:var(--ok-mono);font-size:11px;text-align:left;cursor:pointer;border-radius:var(--ok-r-1)}
.ide-tree-dir:hover{background:var(--ok-bg-2);color:var(--ok-fg)}
.ide-chevron{font-size:8px;color:var(--ok-fg-mute);width:10px}
.ide-tree-children{display:none;padding-left:8px}
.ide-tree-folder.open .ide-tree-children{display:block}
.ide-tree-file{display:flex;align-items:center;gap:8px;width:100%;padding:7px 10px;border:none;background:transparent;color:var(--ok-fg-soft);font-family:var(--ok-mono);font-size:11px;text-align:left;cursor:pointer;border-radius:var(--ok-r-1);border-left:2px solid transparent}
.ide-tree-file:hover{background:color-mix(in oklch,var(--ok-cyan) 8%,var(--ok-bg-2));color:var(--ok-fg)}
.ide-tree-file.active{background:color-mix(in oklch,var(--ok-cyan) 12%,var(--ok-bg-2));color:var(--ok-fg);border-left-color:var(--ok-cyan)}
.ide-tree-file.fixed .ide-file-ico::after{content:"✓";margin-left:4px;color:var(--ok-success);font-size:9px}
.ide-file-ico{font-size:9px;color:var(--ok-cyan);font-weight:700;min-width:18px}
.ide-file-rank{margin-left:auto;font-size:9px;color:var(--ok-fg-mute)}
.vscode-main{display:flex;flex-direction:column;min-width:0;min-height:0}
.vscode-tabs{display:flex;gap:2px;padding:8px 10px 0;border-bottom:1px solid var(--ok-line-soft);background:var(--ok-bg-2);overflow-x:auto}
.ide-tab{display:inline-flex;align-items:center;gap:8px;padding:8px 14px;border:1px solid var(--ok-line-soft);border-bottom:none;border-radius:var(--ok-r-1) var(--ok-r-1) 0 0;background:var(--ok-bg-0);color:var(--ok-fg);font-family:var(--ok-mono);font-size:11px;white-space:nowrap}
.ide-tab-icon{color:var(--ok-cyan);font-size:8px}
.ide-tab-sub{color:var(--ok-fg-mute);font-size:10px}
.vscode-editor{flex:1;display:flex;flex-direction:column;min-height:0;background:var(--ok-bg-0)}
.vscode-editor-bar{display:flex;align-items:center;flex-wrap:wrap;gap:10px;padding:10px 14px;border-bottom:1px solid var(--ok-line-soft);font-family:var(--ok-mono);font-size:11px}
.vscode-breadcrumb{color:var(--ok-cyan);font-weight:600}
.juice-ide-status{font-size:10px;letter-spacing:.06em;padding:3px 8px;border-radius:99px;border:1px solid var(--ok-line)}
.juice-ide-status.vuln{color:var(--ok-magenta);border-color:color-mix(in oklch,var(--ok-magenta) 40%,var(--ok-line));background:color-mix(in oklch,var(--ok-magenta) 10%,transparent)}
.juice-ide-status.fix{color:var(--ok-success);border-color:color-mix(in oklch,var(--ok-success) 40%,var(--ok-line));background:color-mix(in oklch,var(--ok-success) 10%,transparent)}
.juice-ide-status.applying{color:var(--ok-warning);border-color:color-mix(in oklch,var(--ok-warning) 40%,var(--ok-line))}
.ide-line-badge{color:var(--ok-fg-mute);font-size:10px}
.vscode-toolbar{padding:10px 14px;border-bottom:1px solid var(--ok-line-soft);display:flex;align-items:center;gap:10px;flex-wrap:wrap}
.ide-sync-scroll{display:inline-flex;align-items:center;gap:6px;margin-left:auto;font-family:var(--ok-mono);font-size:10px;color:var(--ok-fg-mute);cursor:pointer;user-select:none}
.ide-sync-scroll input{accent-color:var(--ok-cyan)}
.ide-split-wrap{flex:1;display:grid;grid-template-columns:1fr 3px 1fr;min-height:min(52vh,480px);max-height:min(58vh,560px);overflow:hidden;border-top:1px solid var(--ok-line-soft)}
.ide-split-panel{display:flex;flex-direction:column;min-width:0;min-height:0;background:var(--ok-bg-0)}
.ide-split-panel.vuln{border-right:1px solid var(--ok-line-soft)}
.ide-split-panel.fix{background:color-mix(in oklch,var(--ok-success) 3%,var(--ok-bg-0))}
.ide-split-hd{display:flex;align-items:center;gap:8px;padding:8px 12px;border-bottom:1px solid var(--ok-line-soft);font-family:var(--ok-mono);font-size:10px;letter-spacing:.08em;text-transform:uppercase;color:var(--ok-fg-mute);flex-shrink:0;background:var(--ok-bg-2)}
.ide-split-dot{width:8px;height:8px;border-radius:50%;flex-shrink:0}
.ide-split-dot.vuln{background:var(--ok-magenta);box-shadow:0 0 8px color-mix(in oklch,var(--ok-magenta) 50%,transparent)}
.ide-split-dot.fix{background:var(--ok-success);box-shadow:0 0 8px color-mix(in oklch,var(--ok-success) 50%,transparent)}
.ide-split-file,.ide-split-hint{margin-left:auto;font-size:9px;text-transform:none;letter-spacing:0;color:var(--ok-fg-mute)}
.ide-split-hint.typing{color:var(--ok-warning);font-style:italic}
.ide-split-hint.done{color:var(--ok-success)}
.ide-split-gutter{background:var(--ok-line);opacity:.6}
.ide-split-code{flex:1;margin:0;padding:10px 8px;overflow:auto;font-family:var(--ok-mono);font-size:11px;line-height:1.35;tab-size:2}
.ide-split-code code{display:block}
.ide-split-code .ide-row{display:flex;align-items:baseline;gap:0;min-height:0;margin:0;padding:0}
.ide-split-code .ide-ln{display:inline-block;width:30px;margin-right:8px;color:var(--ok-fg-mute);user-select:none;text-align:right;flex-shrink:0;line-height:1.35}
.ide-split-code .ide-lc{white-space:pre;word-break:normal;line-height:1.35;flex:1;min-width:0}
.ide-split-code .ide-row.focus-vuln .ide-lc{background:color-mix(in oklch,var(--ok-magenta) 14%,transparent);border-left:2px solid var(--ok-magenta);padding-left:6px;margin-left:-8px}
.ide-split-code .ide-row.focus-fix .ide-lc{background:color-mix(in oklch,var(--ok-success) 14%,transparent);border-left:2px solid var(--ok-success);padding-left:6px;margin-left:-8px}
.ide-split-code .ide-row.typing .ide-lc::after{content:"▌";color:var(--ok-cyan);animation:ide-blink .9s step-end infinite}
.ide-split-code .ide-placeholder{color:var(--ok-fg-mute);font-style:italic;padding:20px 12px;display:block}
@keyframes ide-blink{50%{opacity:0}}
.juice-ide-meta{padding:12px 14px 14px;border-top:1px solid var(--ok-line-soft);background:var(--ok-bg-1);max-height:140px;overflow-y:auto}
.juice-ide-meta-grid{display:flex;flex-wrap:wrap;gap:8px;align-items:flex-start}
.juice-ide-payload{width:100%;margin:4px 0 0;font-size:12px;color:var(--ok-fg-soft)}
.juice-ide-steps{width:100%;margin:8px 0 0;padding-left:18px;font-size:12px;color:var(--ok-fg-soft);line-height:1.5}
.vscode-terminal{border-top:1px solid var(--ok-line);background:var(--ok-bg-1);min-height:200px;max-height:280px;display:flex;flex-direction:column}
.vscode-term-hd{display:flex;align-items:center;justify-content:space-between;gap:12px;padding:10px 14px;border-bottom:1px solid var(--ok-line-soft);flex-shrink:0}
.vscode-term-title{font-family:var(--ok-mono);font-size:10px;letter-spacing:.12em;text-transform:uppercase;color:var(--ok-fg-mute)}
.vscode-term-actions{display:flex;gap:8px;flex-wrap:wrap}
#juice-ide-apply{--c:var(--ok-success);background:var(--ok-success)!important;color:var(--ok-bg-0)!important;border-color:var(--ok-success)!important}
.vscode-term-out{flex:1;overflow-y:auto;padding:12px 14px;font-family:var(--ok-mono);font-size:12px;line-height:1.55;background:var(--ok-bg-0)}
.vscode-term-out .line{padding:2px 0;white-space:pre-wrap;word-break:break-word}
.vscode-term-out .line.cmd{color:var(--ok-accent)}
.vscode-term-out .line.dim{color:var(--ok-fg-mute);font-style:italic}
.vscode-term-out .line.ok{color:var(--ok-success)}
.vscode-term-out .line.warn{color:var(--ok-warning)}
.vscode-term-out .line.err{color:var(--ok-magenta)}
.vscode-term-out .line.attack{color:var(--ok-magenta);font-weight:600}
.vscode-term-out .line.http{color:var(--ok-cyan)}
.vscode-term-out .line.add{color:var(--ok-success);background:color-mix(in oklch,var(--ok-success) 8%,transparent);padding:2px 6px;border-radius:2px}
@media(max-width:900px){.vscode-shell{grid-template-columns:1fr;min-height:auto}.vscode-sidebar{max-height:220px;border-right:none;border-bottom:1px solid var(--ok-line)}.ide-split-wrap{grid-template-columns:1fr;grid-template-rows:1fr 1fr;max-height:none}.ide-split-gutter{display:none}.ide-split-panel{max-height:min(40vh,320px)}}
.metric-row{display:flex;flex-wrap:wrap;gap:12px;margin:16px 0}
.metric{padding:14px 18px;border:1px solid var(--ok-line);background:var(--ok-bg-0);border-radius:var(--ok-r-2);min-width:120px;flex:1}
.metric.compact{min-width:140px;max-width:200px}
.metric-val{display:block;font-family:var(--ok-mono);font-size:clamp(20px,2vw,28px);font-weight:600;color:var(--ok-accent);line-height:1.1}
.metric-lbl{display:block;font-size:13px;color:var(--ok-fg-soft);margin-top:6px;line-height:1.35}
.metric-src{display:block;font-family:var(--ok-mono);font-size:10px;color:var(--ok-fg-mute);margin-top:4px}
.market-strip{display:flex;flex-wrap:wrap;gap:12px;margin-bottom:var(--ok-s-5)}
.metric-link{text-decoration:none;color:inherit;cursor:pointer;transition:border-color .15s,background .15s,transform .12s}
.metric-link:hover{border-color:var(--ok-cyan);background:color-mix(in oklch,var(--ok-cyan) 6%,var(--ok-bg-0));transform:translateY(-2px)}
.metric-link .metric-src{color:var(--ok-cyan)}
.market-sources{display:flex;flex-wrap:wrap;gap:8px;margin-bottom:var(--ok-s-7);padding:12px 0;border-bottom:1px solid var(--ok-line-soft)}
.market-src-link{font-family:var(--ok-mono);font-size:11px;padding:6px 12px;border:1px solid var(--ok-line);border-radius:var(--ok-r-1);color:var(--ok-fg-soft);text-decoration:none;transition:border-color .15s,color .15s}
.market-src-link:hover{border-color:var(--ok-cyan);color:var(--ok-cyan)}
.table-caption{font-size:14px;color:var(--ok-fg-soft);margin:var(--ok-s-6) 0 12px;line-height:1.6}
.table-caption a,.prevalence-table a,.compare-table a{color:var(--ok-cyan);text-decoration:underline;text-underline-offset:3px}
.data-table,.compare-table{width:100%;border-collapse:collapse;font-size:14px}
.data-table th,.data-table td,.compare-table th,.compare-table td{padding:12px 14px;border-bottom:1px solid var(--ok-line-soft);text-align:left;vertical-align:top}
.data-table th,.compare-table th{font-family:var(--ok-mono);font-size:11px;letter-spacing:.08em;text-transform:uppercase;color:var(--ok-fg-mute);background:var(--ok-bg-2)}
.prevalence-table{margin-top:var(--ok-s-6)}
.research-hub{display:grid;grid-template-columns:minmax(280px,340px) minmax(0,1fr);min-height:520px;border:1px solid var(--ok-line);border-radius:var(--ok-r-2);overflow:hidden;background:var(--ok-bg-1)}
.research-nav{display:flex;flex-direction:column;border-right:1px solid var(--ok-line);overflow-y:auto;max-height:720px}
.research-nav-item{display:block;text-align:left;padding:14px 16px;border:none;border-bottom:1px solid var(--ok-line-soft);background:transparent;cursor:pointer;transition:background .15s}
.research-nav-item:hover,.research-nav-item.active{background:color-mix(in oklch,var(--ok-cyan) 8%,var(--ok-bg-1))}
.research-nav-item.active{border-left:3px solid var(--ok-accent);padding-left:13px}
.research-nav-src{display:block;font-family:var(--ok-mono);font-size:10px;letter-spacing:.1em;text-transform:uppercase;color:var(--ok-cyan);margin-bottom:6px}
.research-nav-hl{display:block;font-size:14px;line-height:1.45;color:var(--ok-fg-soft)}
.research-nav-item.active .research-nav-hl{color:var(--ok-fg)}
.research-panels{padding:clamp(20px,3vw,32px);overflow-y:auto;max-height:720px}
.research-panel{display:none}
.research-panel.active{display:block;animation:fadeIn .2s ease}
.research-panel-hd h3{font-size:clamp(22px,2.2vw,30px);font-weight:500;margin:8px 0 0;line-height:1.25}
.research-actions{margin:24px 0;border-top:1px solid var(--ok-line-soft);padding-top:20px}
.research-actions ul{margin:8px 0 0;padding-left:20px;color:var(--ok-fg-soft);font-size:15px;line-height:1.65}
.breach-explorer{display:grid;grid-template-columns:minmax(320px,1fr) minmax(300px,400px);gap:var(--ok-s-6);margin-top:var(--ok-s-6)}
.timeline-vertical{display:flex;flex-direction:column;gap:8px;max-height:640px;overflow-y:auto;padding:8px;border:1px solid var(--ok-line);background:var(--ok-bg-0);border-radius:var(--ok-r-2)}
.timeline-node{display:grid;grid-template-columns:24px 1fr;gap:12px;align-items:start;text-align:left;padding:12px 14px;border:none;background:transparent;cursor:pointer;border-radius:var(--ok-r-1);transition:background .15s;width:100%}
.timeline-node:hover,.timeline-node.sel{background:color-mix(in oklch,var(--ok-accent) 8%,var(--ok-bg-0))}
.timeline-rail{grid-row:1/span 2;width:2px;background:var(--ok-line);margin:0 auto;height:100%;min-height:48px}
.timeline-dot{width:14px;height:14px;border-radius:50%;background:var(--ok-bg-3);border:2px solid var(--ok-line);transition:all .2s;margin-top:4px}
.timeline-node:hover .timeline-dot,.timeline-node.sel .timeline-dot{background:var(--ok-accent);border-color:var(--ok-accent);box-shadow:0 0 10px color-mix(in oklch,var(--ok-accent) 50%,transparent)}
.timeline-card{display:flex;flex-direction:column;gap:4px}
.timeline-year{font-family:var(--ok-mono);font-size:11px;color:var(--ok-accent)}
.timeline-node strong{font-size:15px;line-height:1.3;color:var(--ok-fg)}
.timeline-cat{font-family:var(--ok-mono);font-size:10px;text-transform:uppercase;letter-spacing:.08em;color:var(--ok-fg-mute)}
.timeline-impact{font-size:12px;color:var(--ok-fg-soft)}
.breach-detail{padding:var(--ok-s-6);border:1px solid var(--ok-line);background:var(--ok-bg-1);border-radius:var(--ok-r-2);font-size:15px;line-height:1.65}
.breach-detail h4{font-size:22px;margin:0 0 12px}
.breach-detail-placeholder{color:var(--ok-fg-mute);font-size:15px;line-height:1.6}
.breach-meta{display:flex;flex-wrap:wrap;gap:8px;margin:16px 0}
.vault-split{display:grid;grid-template-columns:minmax(260px,320px) minmax(0,1fr);min-height:480px;border:1px solid var(--ok-line);border-radius:var(--ok-r-2);overflow:hidden}
.vault-list{display:flex;flex-direction:column;overflow-y:auto;border-right:1px solid var(--ok-line);background:var(--ok-bg-0);max-height:640px}
.vault-item{display:block;text-align:left;padding:12px 14px;border:none;border-bottom:1px solid var(--ok-line-soft);background:transparent;cursor:pointer}
.vault-item:hover,.vault-item.active{background:color-mix(in oklch,var(--ok-cyan) 8%,var(--ok-bg-0))}
.vault-item.active{border-left:3px solid var(--ok-cyan);padding-left:11px}
.vault-item-id{display:block;font-family:var(--ok-mono);font-size:10px;color:var(--ok-accent)}
.vault-item strong{display:block;font-size:14px;margin:4px 0;color:var(--ok-fg)}
.vault-item-lang{font-size:12px;color:var(--ok-fg-mute)}
.vault-detail{padding:var(--ok-s-6);overflow-y:auto;max-height:640px}
.pattern-detail{display:none}
.pattern-detail.active{display:block}
.pattern-inline{border:1px solid var(--ok-line);background:var(--ok-bg-1);border-radius:var(--ok-r-2);padding:var(--ok-s-5);margin-bottom:var(--ok-s-5)}
.pattern-detail-hd h3,.pattern-inline .pattern-detail-hd h3{font-size:22px;margin:12px 0 8px}
.pattern-detail-hd p,.pattern-inline .pattern-detail-hd p{font-size:15px;color:var(--ok-fg-soft)}
.pattern-stack,.lab-stack{display:flex;flex-direction:column;gap:var(--ok-s-6)}
.mitiga-checklist{list-style:none;padding:0;margin:8px 0 0}
.mitiga-checklist li{padding:10px 0;border-bottom:1px solid var(--ok-line-soft);font-size:15px;color:var(--ok-fg-soft)}
.mitiga-checklist label{cursor:pointer;display:flex;gap:10px;align-items:flex-start}
.mitiga-checklist input{margin-top:3px;accent-color:var(--ok-cyan)}
.lab-panel{border:1px solid var(--ok-line);background:var(--ok-bg-1);border-radius:var(--ok-r-2);padding:var(--ok-s-6)}
.lab-panel-hd{margin-bottom:12px}
.lab-file{font-family:var(--ok-mono);font-size:11px;color:var(--ok-magenta)}
.lab-panel h4{font-size:20px;margin:8px 0 0}
.vault-filters{display:flex;flex-wrap:wrap;gap:8px;margin-bottom:var(--ok-s-5)}
.term-panel{display:none}.term-panel.active{display:block}
.term-tabs{margin-bottom:var(--ok-s-5)}
.interactive-term .term-output,.term-embed-out{max-height:360px;overflow-y:auto;font-family:var(--ok-mono);font-size:13px;line-height:1.55}
.interactive-term .line,.term-embed-out .line{padding:2px 0}
.interactive-term .line.cmd,.term-embed-out .line.cmd{color:var(--ok-accent)}
.interactive-term .line.out,.term-embed-out .line.out{color:var(--ok-fg-soft)}
.interactive-term .line.ok,.term-embed-out .line.ok{color:var(--ok-success)}
.interactive-term .line.warn,.term-embed-out .line.warn{color:var(--ok-warning)}
.interactive-term .line.err,.term-embed-out .line.err{color:var(--ok-magenta)}
.interactive-term .line.dim,.term-embed-out .line.dim{color:var(--ok-fg-mute)}
.interactive-term .line.http,.term-embed-out .line.http{color:var(--ok-cyan);font-weight:500}
.term-cmd-palette{display:flex;flex-wrap:wrap;gap:6px;padding:10px 12px;border-top:1px solid var(--ok-line);background:var(--ok-bg-2);max-height:120px;overflow-y:auto}
.term-input-row{display:flex;align-items:center;gap:10px;padding:12px;border-top:1px solid var(--ok-line);background:var(--ok-bg-2)}
.term-input-row .term-input{flex:1;margin:0;font-size:14px}
.term-input-row .prompt{color:var(--ok-accent);font-family:var(--ok-mono);font-size:14px}
.term-embed{padding:var(--ok-s-5);border:1px solid var(--ok-line);border-radius:var(--ok-r-2);background:var(--ok-bg-1);margin-bottom:16px}
.term-embed-hd{display:flex;justify-content:space-between;align-items:center;margin-bottom:10px;flex-wrap:wrap;gap:8px}
.term-embed-out{font-family:var(--ok-mono);font-size:12px;padding:12px;background:var(--ok-bg-0);border:1px solid var(--ok-line);min-height:100px;max-height:200px;overflow-y:auto;border-radius:var(--ok-r-1)}
.term-cmd-row{display:flex;flex-wrap:wrap;gap:6px;margin-top:10px}
.heatmap .hm-cell.dim{opacity:.25}
.heatmap .hm-cell.hl{opacity:1;outline:1px solid color-mix(in oklch,var(--ok-cyan) 50%,transparent)}
.corr-detail .corr-mini{display:block;text-align:left;padding:8px 10px;margin:4px 0;border:1px solid var(--ok-line);background:var(--ok-bg-1);border-radius:var(--ok-r-1);cursor:pointer;font-size:13px;width:100%}
.corr-detail .corr-mini:hover{border-color:var(--ok-accent)}
.present-mode .sidebar,.present-mode .no-print{display:none!important}
.present-mode .layout{grid-template-columns:1fr}
@media(max-width:1100px){.research-hub,.vault-split,.breach-explorer,.corr-layout{grid-template-columns:1fr}.research-nav{max-height:240px;flex-direction:row;overflow-x:auto;border-right:none;border-bottom:1px solid var(--ok-line)}.research-nav-item{flex:0 0 240px;border-bottom:none;border-right:1px solid var(--ok-line-soft)}}
.owasp-hub-hint{font-size:14px;color:var(--ok-fg-mute);margin:0 0 var(--ok-s-6)}
.owasp-bento{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:var(--ok-s-5)}
@media(min-width:1200px){.owasp-bento{grid-template-columns:repeat(5,minmax(0,1fr))}}
.owasp-card{display:flex;flex-direction:column;text-align:left;padding:var(--ok-s-5);border:1px solid var(--ok-line);background:var(--ok-bg-1);border-radius:var(--ok-r-2);transition:border-color .2s,transform .15s,box-shadow .2s;min-height:220px;position:relative;overflow:hidden}
.owasp-card::before{content:"";position:absolute;inset:0;background:linear-gradient(135deg,color-mix(in oklch,var(--ok-cyan) 6%,transparent),transparent 55%);opacity:0;transition:opacity .2s;pointer-events:none}
.owasp-card:hover,.owasp-card:focus-visible{border-color:var(--ok-cyan);transform:translateY(-3px);box-shadow:0 8px 28px color-mix(in oklch,var(--ok-cyan) 12%,transparent);outline:none}
.owasp-card:hover::before,.owasp-card.filter-match::before{opacity:1}
.owasp-card.filter-match{border-color:var(--ok-cyan);box-shadow:0 0 0 1px var(--ok-cyan)}
.owasp-card.dimmed{opacity:.42}
.owasp-card.search-hide{display:none}
.owasp-card-top{display:flex;align-items:center;gap:8px;margin-bottom:10px}
.owasp-card-rank{font-family:var(--ok-mono);font-size:22px;font-weight:700;color:var(--ok-accent);line-height:1}
.owasp-card-id{font-family:var(--ok-mono);font-size:11px;color:var(--ok-cyan);border:1px solid color-mix(in oklch,var(--ok-cyan) 35%,var(--ok-line));padding:2px 8px;border-radius:var(--ok-r-1)}
.owasp-card-trend{margin-left:auto;font-family:var(--ok-mono);font-size:10px;letter-spacing:.04em}
.owasp-card-trend.up{color:var(--ok-warning)}.owasp-card-trend.down{color:var(--ok-success)}.owasp-card-trend.flat{color:var(--ok-fg-mute)}
.owasp-card-title{font-size:15px;font-weight:600;margin:0 0 4px;line-height:1.3;color:var(--ok-fg)}
.owasp-card-en{font-family:var(--ok-mono);font-size:10px;color:var(--ok-fg-mute);margin:0 0 10px;text-transform:uppercase;letter-spacing:.06em}
.owasp-card-teaser{font-size:13px;color:var(--ok-fg-soft);line-height:1.5;margin:0 0 12px;flex:1;display:-webkit-box;-webkit-line-clamp:3;-webkit-box-orient:vertical;overflow:hidden}
.owasp-card-meta{display:flex;align-items:center;gap:12px;margin-bottom:10px}
.owasp-prev-wrap{flex:1;min-width:0}
.owasp-prev-bar{height:4px;background:var(--ok-bg-0);border-radius:2px;overflow:hidden}
.owasp-prev-fill{display:block;height:100%;background:var(--ok-cyan);border-radius:2px}
.owasp-prev-val{font-family:var(--ok-mono);font-size:10px;color:var(--ok-fg-mute)}
.owasp-card-labs{font-family:var(--ok-mono);font-size:10px;color:var(--ok-success);white-space:nowrap}
.owasp-card-cwes{display:flex;flex-wrap:wrap;gap:4px;margin-bottom:8px}
.owasp-card-cwe{font-family:var(--ok-mono);font-size:9px;padding:2px 6px;background:var(--ok-bg-0);border:1px solid var(--ok-line-soft);border-radius:var(--ok-r-1);color:var(--ok-fg-mute)}
.hub-card-actions{display:flex;gap:8px;margin-top:auto;padding-top:12px;border-top:1px solid var(--ok-line-soft)}
.hub-card-actions .hub-btn-info{flex:1;justify-content:center;font-weight:600;letter-spacing:.02em}
.hub-card-actions .hub-btn-sim{flex:1;justify-content:center}
.owasp-card:hover .hub-btn-info,.cwe-card:hover .hub-btn-info{box-shadow:0 0 0 1px color-mix(in oklch,var(--ok-cyan) 35%,transparent)}
.cwe-card:hover .hub-btn-info{box-shadow:0 0 0 1px color-mix(in oklch,var(--ok-magenta) 35%,transparent)}
.owasp-anchors,.cwe-anchors{height:0;overflow:hidden;margin:0;padding:0}
.owasp-anchor{height:0;overflow:hidden;scroll-margin-top:80px}
.owasp-modal{position:fixed;inset:0;z-index:500;display:flex;align-items:center;justify-content:center;padding:20px;opacity:0;visibility:hidden;transition:opacity .25s,visibility .25s}
.owasp-modal.open{opacity:1;visibility:visible}
.owasp-modal-backdrop{position:absolute;inset:0;background:color-mix(in oklch,var(--ok-bg-0) 55%,transparent);backdrop-filter:blur(8px)}
.owasp-modal-dialog{position:relative;width:min(1040px,100%);height:min(90vh,920px);max-height:min(90vh,920px);background:var(--ok-bg-1);border:1px solid var(--ok-line);border-radius:var(--ok-r-2);box-shadow:0 24px 80px color-mix(in oklch,#000 45%,transparent);display:flex;flex-direction:column;overflow:hidden;transform:translateY(16px) scale(.98);transition:transform .25s}
.owasp-modal.open .owasp-modal-dialog{transform:translateY(0) scale(1)}
.owasp-modal-toolbar{display:flex;align-items:center;gap:10px;padding:12px 16px;border-bottom:1px solid var(--ok-line);background:var(--ok-bg-2);flex-shrink:0}
.owasp-modal-toolbar-title{flex:1;font-family:var(--ok-mono);font-size:13px;color:var(--ok-fg-soft);text-align:center}
.owasp-modal-close{margin-left:auto}
.owasp-modal-panels{flex:1;min-height:0;overflow:hidden;display:flex;flex-direction:column}
.owasp-modal-panel{display:flex;flex-direction:column;flex:1;min-height:0;overflow:hidden}
.owasp-modal-panel[hidden]{display:none!important}
.owasp-modal-hd{padding:20px 24px 12px;border-bottom:1px solid var(--ok-line-soft);flex-shrink:0}
.owasp-modal-rank{font-family:var(--ok-mono);font-size:32px;font-weight:700;color:var(--ok-accent);float:left;margin-right:16px;line-height:1}
.owasp-modal-titles h2{margin:0;font-size:clamp(20px,2.5vw,26px)}
.owasp-modal-en{font-family:var(--ok-mono);font-size:12px;color:var(--ok-fg-mute);margin:4px 0 0}
.owasp-modal-diff{font-size:13px;color:var(--ok-fg-soft);margin:12px 0 0;clear:both}
.owasp-modal-actions{display:flex;flex-wrap:wrap;gap:8px;padding:0 24px 12px;flex-shrink:0}
.owasp-modal-tabs{padding:0 24px;flex-shrink:0;overflow-x:auto}
.owasp-modal-scroll{flex:1;min-height:0;overflow-y:auto;overscroll-behavior:contain;-webkit-overflow-scrolling:touch;padding:16px 24px 24px}
.owasp-modal-scroll .tab-panel,.cwe-modal-scroll .tab-panel{margin-top:0}
.owasp-modal-scroll .tab-panel p,.cwe-modal-scroll .tab-panel p{font-size:15px;line-height:1.58;margin:0}
.modal-diff-pill{display:inline-block;font-family:var(--ok-mono);font-size:9px;letter-spacing:.1em;text-transform:uppercase;padding:3px 8px;margin-right:8px;border-radius:99px;background:color-mix(in oklch,var(--ok-accent) 14%,transparent);border:1px solid color-mix(in oklch,var(--ok-accent) 35%,var(--ok-line));color:var(--ok-accent);vertical-align:middle}
.owasp-modal-diff,.cwe-modal-diff{font-size:14px;line-height:1.55;color:var(--ok-fg-soft)}
.owasp-modal-tabs,.cwe-modal-tabs{border-bottom:1px solid var(--ok-line-soft);gap:4px;padding-bottom:0}
.owasp-modal-tabs .ok-tab,.cwe-modal-tabs .ok-tab{font-family:var(--ok-mono);font-size:11px;letter-spacing:.04em;padding:10px 14px;border-radius:var(--ok-r-1) var(--ok-r-1) 0 0;border:1px solid transparent;border-bottom:none;color:var(--ok-fg-mute);transition:color .15s,background .15s,border-color .15s}
.owasp-modal-tabs .ok-tab:hover,.cwe-modal-tabs .ok-tab:hover{color:var(--ok-fg);background:var(--ok-bg-2)}
.owasp-modal-tabs .ok-tab.active,.cwe-modal-tabs .ok-tab.active{color:var(--ok-fg);background:var(--ok-bg-0);border-color:var(--ok-line-soft);box-shadow:inset 0 2px 0 var(--ok-cyan)}
.cwe-modal-tabs .ok-tab.active{box-shadow:inset 0 2px 0 var(--ok-magenta)}
.modal-tab-count{display:inline-flex;align-items:center;justify-content:center;min-width:18px;height:18px;margin-left:6px;padding:0 5px;font-size:9px;border-radius:99px;background:var(--ok-bg-3);color:var(--ok-fg-mute)}
.ok-tab.active .modal-tab-count{background:color-mix(in oklch,var(--ok-cyan) 20%,var(--ok-bg-3));color:var(--ok-cyan)}
.modal-tab-intro{font-size:14px;line-height:1.55;color:var(--ok-fg-mute);margin:0 0 16px;padding:10px 14px;border-left:3px solid var(--ok-line);background:color-mix(in oklch,var(--ok-bg-2) 80%,transparent);border-radius:0 var(--ok-r-1) var(--ok-r-1) 0}
.modal-tab-intro strong{color:var(--ok-fg)}
.modal-prose-flow{display:flex;flex-direction:column;gap:12px}
.modal-lead{padding:16px 18px;border-radius:var(--ok-r-2);background:linear-gradient(135deg,color-mix(in oklch,var(--ok-accent) 10%,var(--ok-bg-0)),var(--ok-bg-0));border:1px solid color-mix(in oklch,var(--ok-accent) 22%,var(--ok-line))}
.modal-lead p{font-size:16px!important;line-height:1.55!important;color:var(--ok-fg)!important;font-weight:500}
.modal-prose-card{padding:14px 16px;border-radius:var(--ok-r-1);background:var(--ok-bg-0);border:1px solid var(--ok-line-soft)}
.modal-prose-card p{color:var(--ok-fg-soft)!important;font-size:15px!important;line-height:1.55!important}
.modal-callout{padding:14px 16px;border-radius:var(--ok-r-1);border:1px solid var(--ok-line)}
.modal-callout.juice{background:color-mix(in oklch,var(--ok-warning) 8%,var(--ok-bg-0));border-color:color-mix(in oklch,var(--ok-warning) 28%,var(--ok-line))}
.modal-callout.stat{background:color-mix(in oklch,var(--ok-cyan) 8%,var(--ok-bg-0));border-color:color-mix(in oklch,var(--ok-cyan) 28%,var(--ok-line))}
.modal-callout-kicker{display:block;font-family:var(--ok-mono);font-size:10px;letter-spacing:.1em;text-transform:uppercase;color:var(--ok-fg-mute);margin-bottom:8px}
.modal-callout p{font-size:14px!important;line-height:1.55!important;color:var(--ok-fg-soft)!important}
.modal-hl{padding:1px 5px;border-radius:3px;font-style:normal;font-weight:600;font-family:var(--ok-mono);font-size:.92em}
.modal-hl.cwe{background:color-mix(in oklch,var(--ok-magenta) 18%,transparent);color:var(--ok-magenta)}
.modal-hl.owasp{background:color-mix(in oklch,var(--ok-accent) 18%,transparent);color:var(--ok-accent)}
.modal-hl.path{background:color-mix(in oklch,var(--ok-warning) 14%,transparent);color:var(--ok-warning)}
.modal-hl.stat{background:color-mix(in oklch,var(--ok-cyan) 18%,transparent);color:var(--ok-cyan)}
.modal-hl.juice{background:color-mix(in oklch,var(--ok-warning) 18%,transparent);color:var(--ok-warning)}
.modal-hl.attack{background:color-mix(in oklch,var(--ok-magenta) 14%,transparent);color:var(--ok-magenta)}
.modal-hl.wstg,.modal-hl.asvs{background:color-mix(in oklch,var(--ok-success) 14%,transparent);color:var(--ok-success)}
.modal-tags-block{margin-top:20px;padding-top:16px;border-top:1px solid var(--ok-line-soft)}
.modal-tag-row{margin-top:8px}
.modal-cwe-chip,.modal-tool-chip{cursor:pointer;transition:transform .12s}
.modal-cwe-chip:hover,.modal-tool-chip:hover{transform:translateY(-1px)}
.modal-tech-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:14px}
@media(max-width:760px){.modal-tech-grid{grid-template-columns:1fr}}
.modal-tech-card{padding:14px 16px;border-radius:var(--ok-r-2);background:var(--ok-bg-0);border:1px solid var(--ok-line-soft)}
.modal-tech-card.detect{border-top:3px solid var(--ok-cyan)}
.modal-tech-card.test{border-top:3px solid var(--ok-warning)}
.modal-tech-card.asvs{border-top:3px solid var(--ok-success)}
.modal-tech-hd{display:flex;align-items:center;gap:8px;margin-bottom:12px}
.modal-tech-ico{font-size:14px;color:var(--ok-fg-mute)}
.modal-tech-hd .section-label{margin:0}
.modal-bullet-list{list-style:none;padding:0;margin:0}
.modal-bullet-list li{display:flex;gap:10px;align-items:flex-start;padding:9px 0;border-bottom:1px solid var(--ok-line-soft);font-size:13px;line-height:1.5;color:var(--ok-fg-soft)}
.modal-bullet-list li:last-child{border-bottom:none}
.modal-li-ico{flex-shrink:0;font-family:var(--ok-mono);font-size:11px;color:var(--ok-cyan);margin-top:2px}
.modal-case-list .owasp-case-item{padding:16px 14px;border:1px solid var(--ok-line-soft);border-radius:var(--ok-r-1);margin-bottom:10px;background:var(--ok-bg-0)}
.modal-case-impact{display:block;font-size:15px;color:var(--ok-fg);margin-bottom:4px}
.modal-case-desc{display:block;font-size:14px;line-height:1.5;color:var(--ok-fg-soft)}
.modal-mitiga-wrap{display:grid;grid-template-columns:1.2fr 1fr;gap:16px}
@media(max-width:760px){.modal-mitiga-wrap{grid-template-columns:1fr}}
.modal-mitiga-card{padding:16px 18px;border-radius:var(--ok-r-2);background:var(--ok-bg-0);border:1px solid var(--ok-line-soft)}
.modal-mitiga-hint{font-size:13px;color:var(--ok-fg-mute);margin:0 0 12px;line-height:1.45}
.modal-checklist{list-style:none;padding:0;margin:0}
.modal-checklist li{padding:0;border-bottom:1px solid var(--ok-line-soft)}
.modal-checklist li:last-child{border-bottom:none}
.modal-check{display:flex;gap:12px;align-items:flex-start;padding:12px 0;cursor:pointer;font-size:14px;line-height:1.5;color:var(--ok-fg-soft)}
.modal-check input{position:absolute;opacity:0;width:0;height:0}
.modal-check-box{flex-shrink:0;width:18px;height:18px;margin-top:2px;border:2px solid var(--ok-line);border-radius:4px;background:var(--ok-bg-1);transition:border-color .15s,background .15s}
.modal-check input:checked+.modal-check-box{background:var(--ok-success);border-color:var(--ok-success);box-shadow:inset 0 0 0 2px var(--ok-bg-0)}
.modal-check input:checked~.modal-check-txt{color:var(--ok-fg);text-decoration:line-through;text-decoration-color:color-mix(in oklch,var(--ok-success) 50%,transparent)}
.modal-ref-list{list-style:none;padding:0;margin:8px 0 0}
.modal-ref-list li{padding:10px 0;border-bottom:1px solid var(--ok-line-soft)}
.modal-ref-list a{display:flex;align-items:center;gap:8px;color:var(--ok-cyan);font-size:14px;text-decoration:none}
.modal-ref-list a:hover{text-decoration:underline}
.modal-ref-ico{font-family:var(--ok-mono);font-size:11px;opacity:.7}
.modal-ref-list.standalone{margin-top:4px}
.modal-owasp-primary{margin-bottom:20px}
.modal-owasp-hero{display:flex;flex-direction:column;align-items:flex-start;gap:4px;width:100%;margin-top:8px;padding:16px 18px;border:1px solid color-mix(in oklch,var(--ok-accent) 30%,var(--ok-line));border-radius:var(--ok-r-2);background:color-mix(in oklch,var(--ok-accent) 8%,var(--ok-bg-0));cursor:pointer;text-align:left;transition:border-color .15s,transform .12s}
.modal-owasp-hero:hover{border-color:var(--ok-accent);transform:translateY(-1px)}
.modal-owasp-id{font-family:var(--ok-mono);font-size:18px;font-weight:700;color:var(--ok-accent)}
.modal-owasp-name{font-size:14px;color:var(--ok-fg-soft)}
.owasp-case-list{list-style:none;padding:0;margin:0}
.owasp-case-item{display:grid;grid-template-columns:140px 1fr;gap:16px;padding:14px 0;border-bottom:1px solid var(--ok-line-soft)}
.owasp-case-year{font-family:var(--ok-mono);font-size:12px;color:var(--ok-cyan)}
.owasp-case-detail{display:block;font-size:13px;color:var(--ok-fg-mute);margin-top:4px}
.info-guide-wrap{display:flex;flex-direction:column;gap:22px}
.info-guide-hd{padding:16px 18px;border-radius:var(--ok-r-2);background:linear-gradient(135deg,color-mix(in oklch,var(--ok-cyan) 10%,var(--ok-bg-0)),var(--ok-bg-0));border:1px solid color-mix(in oklch,var(--ok-cyan) 22%,var(--ok-line))}
.cwe-modal-panel .info-guide-hd{background:linear-gradient(135deg,color-mix(in oklch,var(--ok-magenta) 10%,var(--ok-bg-0)),var(--ok-bg-0));border-color:color-mix(in oklch,var(--ok-magenta) 22%,var(--ok-line))}
.info-guide-summary{font-size:16px!important;line-height:1.55!important;color:var(--ok-fg)!important;font-weight:500;margin:0 0 12px!important}
.info-meta-chips{display:flex;flex-wrap:wrap;gap:6px;margin-bottom:8px}
.info-meta-diff{font-size:13px;line-height:1.5;color:var(--ok-fg-soft);margin:8px 0 0}
.info-panel-sec>.section-label{display:block;margin-bottom:10px}
.info-takeaways{padding:14px 16px;border-radius:var(--ok-r-1);border:1px solid color-mix(in oklch,var(--ok-accent) 22%,var(--ok-line));background:color-mix(in oklch,var(--ok-accent) 6%,var(--ok-bg-0))}
.info-takeaway-list,.info-bullet-list,.info-practice-list,.info-reflection-list{list-style:none;padding:0;margin:0}
.info-takeaway-list li,.info-bullet-list li,.info-practice-list li,.info-reflection-list li{padding:10px 0 10px 16px;border-bottom:1px solid var(--ok-line-soft);font-size:14px;line-height:1.5;color:var(--ok-fg-soft);position:relative}
.info-takeaway-list li::before,.info-bullet-list li::before,.info-practice-list li::before,.info-reflection-list li::before{content:"";position:absolute;left:0;top:16px;width:6px;height:6px;border-radius:50%;background:var(--ok-cyan)}
.cwe-modal-panel .info-takeaway-list li::before,.cwe-modal-panel .info-bullet-list li::before,.cwe-modal-panel .info-practice-list li::before,.cwe-modal-panel .info-reflection-list li::before{background:var(--ok-magenta)}
.info-attack{padding:14px 16px;border-radius:var(--ok-r-1);border:1px solid color-mix(in oklch,var(--ok-warning) 28%,var(--ok-line));background:color-mix(in oklch,var(--ok-warning) 6%,var(--ok-bg-0))}
.info-attack p{font-size:14px!important;line-height:1.55!important;color:var(--ok-fg-soft)!important;margin:8px 0 0!important}
.info-concepts-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:10px}
@media(max-width:700px){.info-concepts-grid{grid-template-columns:1fr}}
.info-concept-card{padding:12px 14px;border-radius:var(--ok-r-1);background:var(--ok-bg-0);border:1px solid var(--ok-line-soft)}
.info-concept-card h4{margin:0 0 6px;font-size:13px;color:var(--ok-fg)}
.info-concept-card p{font-size:13px!important;line-height:1.5!important;color:var(--ok-fg-soft)!important;margin:0!important}
.info-panel-cols{display:grid;grid-template-columns:1fr 1fr;gap:16px}
@media(max-width:760px){.info-panel-cols{grid-template-columns:1fr}}
.info-practice .ok-btn{margin-top:12px}
.info-mitiga-hint{font-size:13px;color:var(--ok-fg-mute);margin:0 0 10px;line-height:1.45}
.info-case-list{list-style:none;padding:0;margin:0}
.info-case-item{display:grid;grid-template-columns:120px 1fr;gap:12px;padding:12px 0;border-bottom:1px solid var(--ok-line-soft)}
.info-case-who{font-family:var(--ok-mono);font-size:11px;color:var(--ok-cyan);line-height:1.4}
.cwe-modal-panel .info-case-who{color:var(--ok-magenta)}
.info-case-body strong{display:block;font-size:14px;color:var(--ok-fg);margin-bottom:4px}
.info-case-body p{font-size:13px!important;line-height:1.5!important;color:var(--ok-fg-soft)!important;margin:0!important}
.info-case-extra{display:block;font-size:12px;color:var(--ok-fg-mute);margin-top:4px}
.info-code-stack .pattern-inline{margin-bottom:14px}
.owasp-modal-tabs .ok-tab[data-tab="guia"],.cwe-modal-tabs .ok-tab[data-tab="guia"]{font-weight:600;color:var(--ok-fg)}
html.owasp-modal-open,html.cwe-modal-open,body.owasp-modal-open,body.cwe-modal-open{overflow:hidden;overscroll-behavior:none}
.cwe-hub-hint{font-size:14px;color:var(--ok-fg-mute);margin:0 0 var(--ok-s-6)}
.cwe-bento{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:var(--ok-s-5)}
@media(min-width:900px){.cwe-bento{grid-template-columns:repeat(3,minmax(0,1fr))}}
@media(min-width:1200px){.cwe-bento{grid-template-columns:repeat(5,minmax(0,1fr))}}
.cwe-card{display:flex;flex-direction:column;text-align:left;padding:var(--ok-s-5);border:1px solid var(--ok-line);background:var(--ok-bg-1);border-radius:var(--ok-r-2);transition:border-color .2s,transform .15s,box-shadow .2s;min-height:200px;position:relative;overflow:hidden}
.cwe-card::before{content:"";position:absolute;inset:0;background:linear-gradient(135deg,color-mix(in oklch,var(--ok-magenta) 6%,transparent),transparent 55%);opacity:0;transition:opacity .2s;pointer-events:none}
.cwe-card:hover,.cwe-card:focus-visible{border-color:var(--ok-magenta);transform:translateY(-3px);box-shadow:0 8px 28px color-mix(in oklch,var(--ok-magenta) 12%,transparent);outline:none}
.cwe-card:hover::before,.cwe-card.filter-match::before{opacity:1}
.cwe-card.filter-match{border-color:var(--ok-magenta);box-shadow:0 0 0 1px var(--ok-magenta)}
.cwe-card.dimmed{opacity:.42}
.cwe-card.search-hide{display:none}
.cwe-card-top{display:flex;align-items:center;gap:8px;margin-bottom:10px}
.cwe-card-rank{font-family:var(--ok-mono);font-size:22px;font-weight:700;color:var(--ok-magenta);line-height:1}
.cwe-card-id{font-family:var(--ok-mono);font-size:11px;color:var(--ok-magenta);border:1px solid color-mix(in oklch,var(--ok-magenta) 35%,var(--ok-line));padding:2px 8px;border-radius:var(--ok-r-1)}
.cwe-card-trend{margin-left:auto;font-family:var(--ok-mono);font-size:10px;letter-spacing:.04em}
.cwe-card-trend.up{color:var(--ok-warning)}.cwe-card-trend.down{color:var(--ok-success)}.cwe-card-trend.flat{color:var(--ok-fg-mute)}
.cwe-card-title{font-size:14px;font-weight:600;margin:0 0 4px;line-height:1.3;color:var(--ok-fg)}
.cwe-card-en{font-family:var(--ok-mono);font-size:10px;color:var(--ok-fg-mute);margin:0 0 8px;text-transform:uppercase;letter-spacing:.06em}
.cwe-card-teaser{font-size:12px;color:var(--ok-fg-soft);line-height:1.45;margin:0 0 10px;flex:1;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}
.cwe-card-meta{display:flex;align-items:center;gap:12px;margin-bottom:8px}
.cwe-score-wrap{flex:1;min-width:0}
.cwe-score-bar{height:4px;background:var(--ok-bg-0);border-radius:2px;overflow:hidden}
.cwe-score-fill{display:block;height:100%;background:linear-gradient(90deg,var(--ok-magenta),color-mix(in oklch,var(--ok-magenta) 60%,var(--ok-cyan)))}
.cwe-score-val{font-family:var(--ok-mono);font-size:10px;color:var(--ok-fg-mute)}
.cwe-card-kev{font-family:var(--ok-mono);font-size:10px;color:var(--ok-success);white-space:nowrap}
.cwe-card-owasps{display:flex;flex-wrap:wrap;gap:4px;margin-bottom:8px}
.cwe-card-owasp{font-family:var(--ok-mono);font-size:9px;padding:2px 6px;background:var(--ok-bg-0);border:1px solid var(--ok-line-soft);border-radius:var(--ok-r-1);color:var(--ok-fg-mute)}
.cwe-card-cta{font-family:var(--ok-mono);font-size:11px;color:var(--ok-magenta);letter-spacing:.04em}
.cwe-anchor{height:0;overflow:hidden;scroll-margin-top:80px;position:absolute;width:0}
.cwe-modal{position:fixed;inset:0;z-index:500;display:flex;align-items:center;justify-content:center;padding:20px;opacity:0;visibility:hidden;transition:opacity .25s,visibility .25s}
.cwe-modal.open{opacity:1;visibility:visible}
.cwe-modal-backdrop{position:absolute;inset:0;background:color-mix(in oklch,var(--ok-bg-0) 55%,transparent);backdrop-filter:blur(8px)}
.cwe-modal-dialog{position:relative;width:min(960px,100%);height:min(88vh,900px);max-height:min(88vh,900px);background:var(--ok-bg-1);border:1px solid var(--ok-line);border-radius:var(--ok-r-2);box-shadow:0 24px 80px color-mix(in oklch,#000 45%,transparent);display:flex;flex-direction:column;overflow:hidden;transform:translateY(16px) scale(.98);transition:transform .25s}
.cwe-modal.open .cwe-modal-dialog{transform:translateY(0) scale(1)}
.cwe-modal-toolbar{display:flex;align-items:center;gap:10px;padding:12px 16px;border-bottom:1px solid var(--ok-line);background:var(--ok-bg-2);flex-shrink:0}
.cwe-modal-toolbar-title{flex:1;font-family:var(--ok-mono);font-size:13px;color:var(--ok-fg-soft);text-align:center}
.cwe-modal-close{margin-left:auto}
.cwe-modal-panels{flex:1;min-height:0;overflow:hidden;display:flex;flex-direction:column}
.cwe-modal-panel{display:flex;flex-direction:column;flex:1;min-height:0;overflow:hidden}
.cwe-modal-panel[hidden]{display:none!important}
.cwe-modal-hd{padding:20px 24px 12px;border-bottom:1px solid var(--ok-line-soft);flex-shrink:0}
.cwe-modal-rank{font-family:var(--ok-mono);font-size:32px;font-weight:700;color:var(--ok-magenta);float:left;margin-right:16px;line-height:1}
.cwe-modal-titles h2{margin:0;font-size:clamp(20px,2.5vw,26px)}
.cwe-modal-en{font-family:var(--ok-mono);font-size:12px;color:var(--ok-fg-mute);margin:4px 0 0}
.cwe-modal-badges{display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin-top:12px;clear:both}
.cwe-modal-actions{display:flex;flex-wrap:wrap;gap:8px;padding:0 24px 12px;flex-shrink:0}
.cwe-modal-tabs{padding:0 24px;flex-shrink:0;overflow-x:auto}
.cwe-modal-scroll{flex:1;min-height:0;overflow-y:auto;overscroll-behavior:contain;-webkit-overflow-scrolling:touch;padding:16px 24px 24px}
@media(max-width:900px){.layout{grid-template-columns:1fr}.sidebar{position:relative;height:auto;top:0;max-height:min(55vh,480px)}.nav-scroll-block{max-height:200px}.grid-2,.split-2,.charts-grid,.charts-inline-2,.sim-grid,.owasp-bento,.cwe-bento,.news-grid{grid-template-columns:1fr}.chart-body-split{grid-template-columns:1fr}.chart-ring-wrap{min-height:260px}.chart-wrap{max-width:min(300px,92vw)}}

/* ===== TEMA CLARO — elegância OKAMI com contraste legível ===== */
body.ok.theme-light::before{opacity:.12}
body.ok.theme-light::after{opacity:0}
body.ok.theme-light{background:var(--ok-bg-1)}
body.ok.theme-light .toolbar{background:color-mix(in srgb,var(--ok-bg-1) 90%,transparent);border-bottom:1px solid var(--ok-line)}
body.ok.theme-light .ok-input,body.ok.theme-light .ok-select,body.ok.theme-light .ok-textarea{background:var(--ok-bg-1);border:1px solid var(--ok-line);color:var(--ok-fg)}
body.ok.theme-light .ok-input:focus,body.ok.theme-light .ok-select:focus,body.ok.theme-light .ok-textarea:focus{border-color:var(--ok-cyan);box-shadow:0 0 0 1px var(--ok-cyan),0 0 calc(14px * var(--ok-glow)) -4px color-mix(in oklch,var(--ok-cyan) 50%,transparent)}
body.ok.theme-light .sidebar{background:linear-gradient(180deg,color-mix(in oklch,var(--ok-bg-1) 94%,var(--ok-cyan)) 0%,color-mix(in oklch,var(--ok-bg-0) 96%,var(--ok-magenta)) 100%);border-right:1px solid var(--ok-line)}
body.ok.theme-light .sidebar-head{background:linear-gradient(135deg,color-mix(in oklch,var(--ok-accent) 11%,var(--ok-bg-1)),color-mix(in oklch,var(--ok-magenta) 8%,var(--ok-bg-2)),color-mix(in oklch,var(--ok-cyan) 7%,var(--ok-bg-1)));border-bottom:1px solid var(--ok-line)}
body.ok.theme-light .nav-group{border-bottom:1px solid var(--ok-line-soft)}
body.ok.theme-light .nav-group[data-group="bridge"]{background:linear-gradient(90deg,color-mix(in oklch,var(--ok-accent) 8%,var(--ok-bg-1)),color-mix(in oklch,var(--ok-magenta) 8%,var(--ok-bg-1)))}
body.ok.theme-light .nav-link{border:1px solid transparent}
body.ok.theme-light .nav-link.nav-tone-cyan:hover,body.ok.theme-light .nav-link.nav-tone-cyan.active{background:color-mix(in oklch,var(--ok-cyan) 12%,var(--ok-bg-1));border-color:color-mix(in oklch,var(--ok-cyan) 38%,var(--ok-line))}
body.ok.theme-light .nav-link.nav-tone-accent:hover,body.ok.theme-light .nav-link.nav-tone-accent.active{background:color-mix(in oklch,var(--ok-accent) 12%,var(--ok-bg-1));border-color:color-mix(in oklch,var(--ok-accent) 40%,var(--ok-line))}
body.ok.theme-light .nav-link.nav-tone-magenta:hover,body.ok.theme-light .nav-link.nav-tone-magenta.active,body.ok.theme-light .nav-link.nav-tone-hot:hover,body.ok.theme-light .nav-link.nav-tone-hot.active{background:color-mix(in oklch,var(--ok-magenta) 11%,var(--ok-bg-1));border-color:color-mix(in oklch,var(--ok-magenta) 38%,var(--ok-line))}
body.ok.theme-light .nav-link.nav-tone-warning:hover,body.ok.theme-light .nav-link.nav-tone-warning.active{background:color-mix(in oklch,var(--ok-warning) 12%,var(--ok-bg-1));border-color:color-mix(in oklch,var(--ok-warning) 38%,var(--ok-line))}
body.ok.theme-light .nav-link.nav-tone-success:hover,body.ok.theme-light .nav-link.nav-tone-success.active{background:color-mix(in oklch,var(--ok-success) 12%,var(--ok-bg-1));border-color:color-mix(in oklch,var(--ok-success) 38%,var(--ok-line))}
body.ok.theme-light .nav-link.nav-tone-mid:hover,body.ok.theme-light .nav-link.nav-tone-mid.active{background:color-mix(in oklch,var(--ok-cyan) 9%,var(--ok-bg-1));border-color:color-mix(in oklch,var(--ok-cyan) 32%,var(--ok-line))}
body.ok.theme-light .nav-link.nav-tone-base:hover,body.ok.theme-light .nav-link.nav-tone-base.active{background:color-mix(in oklch,var(--ok-bg-3) 55%,var(--ok-bg-1));border-color:var(--ok-line)}
body.ok.theme-light .nav-link.nav-tone-bridge:hover,body.ok.theme-light .nav-link.nav-tone-bridge.active{background:linear-gradient(90deg,color-mix(in oklch,var(--ok-accent) 10%,var(--ok-bg-1)),color-mix(in oklch,var(--ok-magenta) 10%,var(--ok-bg-1)));border-color:color-mix(in oklch,var(--ok-magenta) 35%,var(--ok-line))}
body.ok.theme-light .hero{border-bottom:1px solid var(--ok-line)}
body.ok.theme-light .lesson-sec{border-bottom:1px solid var(--ok-line-soft)}
body.ok.theme-light .hl-block,body.ok.theme-light .ok-card,body.ok.theme-light .owasp-card,body.ok.theme-light .cwe-card,body.ok.theme-light .news-card,body.ok.theme-light .chart-box,body.ok.theme-light .corr-hub,body.ok.theme-light .sim-box,body.ok.theme-light .cwe-ladder-row,body.ok.theme-light .term-embed{border:1px solid var(--ok-line);background:var(--ok-bg-1);box-shadow:none}
body.ok.theme-light .hl-block:hover,body.ok.theme-light .owasp-card:hover,body.ok.theme-light .cwe-card:hover,body.ok.theme-light .news-card:hover{border-color:color-mix(in oklch,var(--ok-cyan) 42%,var(--ok-line));box-shadow:0 0 0 1px color-mix(in oklch,var(--ok-cyan) 18%,var(--ok-line))}
body.ok.theme-light .hl-hd{background:color-mix(in oklch,var(--ok-bg-2) 85%,var(--ok-bg-1));border-bottom:1px solid var(--ok-line-soft)}
body.ok.theme-light .hl-takeaway,body.ok.theme-light .hl-bullets-wrap,body.ok.theme-light .hl-quote-text{background:color-mix(in oklch,var(--ok-bg-2) 80%,var(--ok-bg-1));border:1px solid var(--ok-line-soft)}
body.ok.theme-light .hl-source-link{background:color-mix(in oklch,var(--ok-cyan) 8%,var(--ok-bg-1));border:1px solid color-mix(in oklch,var(--ok-cyan) 35%,var(--ok-line))}
body.ok.theme-light .hl-why{background:color-mix(in oklch,var(--ok-accent) 7%,var(--ok-bg-1));border-left:2px solid var(--ok-accent)}
body.ok.theme-light .hl-block.hl-pos{background:color-mix(in oklch,var(--ok-accent) 5%,var(--ok-bg-1))}
body.ok.theme-light .hl-block.hl-mencao{background:color-mix(in oklch,var(--ok-warning) 5%,var(--ok-bg-1))}
body.ok.theme-light .hl-sec-bridge{background:color-mix(in oklch,var(--ok-bg-2) 70%,var(--ok-bg-1));border-top:1px solid var(--ok-line);border-bottom:1px solid var(--ok-line)}
body.ok.theme-light .ok-btn.solid{color:#fff}
body.ok.theme-light .ok-btn.solid:hover,body.ok.theme-light .ok-btn.cyan:not(.ghost):hover,body.ok.theme-light .ok-btn.magenta:not(.ghost):hover,body.ok.theme-light .ok-btn.danger:not(.ghost):hover{color:#fff!important}
body.ok.theme-light .ok-btn.ghost{border:1px solid var(--ok-line);background:#fff;color:var(--ok-fg-soft)}
body.ok.theme-light .ok-btn.ghost:hover,body.ok.theme-light .ok-btn.ghost:focus-visible{color:var(--ok-fg)!important;background:var(--ok-bg-2)!important;border-color:var(--ok-cyan)!important;box-shadow:0 0 0 1px color-mix(in oklch,var(--ok-cyan) 28%,var(--ok-line))!important}
body.ok.theme-light .ok-btn.ghost:active{color:var(--ok-fg)!important;background:color-mix(in oklch,var(--ok-cyan) 14%,#fff)!important;border-color:var(--ok-cyan)!important}
body.ok.theme-light .heatmap-wrap,body.ok.theme-light .corr-sidebar,body.ok.theme-light .corr-detail,body.ok.theme-light .corr-hub{border:1px solid var(--ok-line);background:var(--ok-bg-1)}
body.ok.theme-light .heatmap-wrap{background:var(--ok-bg-2);padding:12px}
body.ok.theme-light .corr-sidebar{background:#fff}
body.ok.theme-light .heatmap{border-spacing:3px}
body.ok.theme-light .heatmap .hm-owasp,body.ok.theme-light .heatmap .hm-cwe{background:var(--ok-bg-1);border:1px solid var(--ok-line)}
body.ok.theme-light .heatmap .hm-owasp.sel span,body.ok.theme-light .heatmap .hm-cwe.sel span{background:color-mix(in oklch,var(--ok-accent) 18%,var(--ok-bg-2));color:var(--ok-fg);border-radius:2px}
body.ok.theme-light .heatmap .hm-cell{width:20px;height:20px;border-radius:3px}
body.ok.theme-light .heatmap .hm-cell.s1{background:oklch(90% .06 208);border:1px solid oklch(68% .11 208)}
body.ok.theme-light .heatmap .hm-cell.s2{background:oklch(89% .07 338);border:1px solid oklch(65% .14 338)}
body.ok.theme-light .heatmap .hm-cell.s3{background:oklch(78% .14 42);border:1px solid var(--ok-accent);box-shadow:inset 0 0 0 1px color-mix(in oklch,#fff 35%,transparent)}
body.ok.theme-light .heatmap .hm-cell.empty{background:#fff;border:1px solid var(--ok-line-soft)}
body.ok.theme-light .heatmap .hm-cell.dim{opacity:.4}
body.ok.theme-light .heatmap .hm-cell.sel{outline:3px solid var(--ok-fg);outline-offset:1px;transform:scale(1.15);z-index:3}
body.ok.theme-light .heatmap .hm-cell.hl{outline:2px solid var(--ok-cyan);outline-offset:0;opacity:1}
body.ok.theme-light .corr-list{gap:6px;padding:10px;background:#fff}
body.ok.theme-light .corr-item{border:1px solid var(--ok-line);background:#fff;font-size:14px;padding:11px 13px}
body.ok.theme-light .corr-item:hover{background:color-mix(in oklch,var(--ok-cyan) 12%,#fff);border-color:var(--ok-cyan)}
body.ok.theme-light .corr-item.sel{background:color-mix(in oklch,var(--ok-accent) 22%,#fff);border:2px solid var(--ok-accent);box-shadow:0 2px 10px color-mix(in oklch,var(--ok-accent) 18%,transparent)}
body.ok.theme-light .corr-item.sel .corr-id,body.ok.theme-light .corr-item.sel .corr-name{font-weight:600;color:var(--ok-fg)}
body.ok.theme-light .corr-item.hl{background:color-mix(in oklch,var(--ok-cyan) 16%,#fff);border-color:color-mix(in oklch,var(--ok-cyan) 55%,var(--ok-line))}
body.ok.theme-light .corr-item.hl .corr-id{font-weight:600}
body.ok.theme-light .corr-item.dim{opacity:1;background:var(--ok-bg-2);border-color:var(--ok-line-soft)}
body.ok.theme-light .corr-item.dim .corr-name{color:var(--ok-fg-dim)}
body.ok.theme-light .corr-item.dim .corr-id,body.ok.theme-light .corr-item.dim .corr-str{color:var(--ok-fg-mute)}
body.ok.theme-light .corr-id{font-weight:600;color:var(--ok-accent)}
body.ok.theme-light .corr-name{color:var(--ok-fg);line-height:1.45}
body.ok.theme-light .corr-str{color:var(--ok-fg-mute);font-weight:500}
body.ok.theme-light .corr-list-hd{background:var(--ok-bg-2);color:var(--ok-fg-mute);border-bottom:2px solid var(--ok-line)}
body.ok.theme-light .corr-list-hd strong{color:var(--ok-fg);font-size:13px}
body.ok.theme-light .corr-list-hd span:last-child{color:var(--ok-cyan);font-weight:600}
body.ok.theme-light .chart-box{background:linear-gradient(165deg,color-mix(in oklch,var(--ok-cyan) 5%,var(--ok-bg-1)) 0%,var(--ok-bg-1) 55%);border:1px solid var(--ok-line)}
body.ok.theme-light .chart-box:hover{border-color:color-mix(in oklch,var(--ok-cyan) 40%,var(--ok-line));box-shadow:0 0 0 1px color-mix(in oklch,var(--ok-cyan) 15%,var(--ok-line))}
body.ok.theme-light .chart-ring-wrap,body.ok.theme-light .chart-plot,body.ok.theme-light .chart-plot-ranked,body.ok.theme-light .chart-legend-panel,body.ok.theme-light .chart-delta-key{border:1px solid var(--ok-line);background:#fff}
body.ok.theme-light .chart-legend-panel{background:#fff}
body.ok.theme-light .chart-legend-title{color:var(--ok-fg-mute);font-weight:700;border-bottom-color:var(--ok-line)}
body.ok.theme-light .chart-legend-item{border:1px solid transparent;color:var(--ok-fg-soft)}
body.ok.theme-light .chart-legend-item:hover,body.ok.theme-light .chart-legend-item.active,body.ok.theme-light .chart-legend-item:focus-visible{background:color-mix(in oklch,var(--ok-cyan) 10%,#fff);border-color:color-mix(in oklch,var(--ok-cyan) 45%,var(--ok-line));color:var(--ok-fg)!important}
body.ok.theme-light .chart-legend-item:hover .chart-legend-label,body.ok.theme-light .chart-legend-item.active .chart-legend-label,body.ok.theme-light .chart-legend-item:hover .chart-legend-val,body.ok.theme-light .chart-legend-item.active .chart-legend-val,body.ok.theme-light .chart-legend-item:hover .chart-legend-sub,body.ok.theme-light .chart-legend-item.active .chart-legend-sub{color:var(--ok-fg)!important}
body.ok.theme-light .chart-legend-label{color:var(--ok-fg);font-weight:700;font-size:14px}
body.ok.theme-light .chart-legend-val{color:var(--ok-fg);font-weight:800;font-size:14px}
body.ok.theme-light .chart-legend-sub{color:var(--ok-fg-mute);font-size:11px;font-weight:600}
body.ok.theme-light .chart-legend-rank{color:var(--ok-fg-mute);font-weight:800}
body.ok.theme-light .chart-legend-swatch{box-shadow:0 0 0 1px var(--ok-line);border:1px solid color-mix(in oklch,#000 10%,transparent)}
body.ok.theme-light .chart-legend-meter{background:#b0b8cc}
body.ok.theme-light .chart-legend-item{border-color:var(--ok-line-soft);background:#fff;color:var(--ok-fg)}
body.ok.theme-light .chart-donut-wrap .chart-legend-item{background:#fff;border:1px solid var(--ok-line)}
body.ok.theme-light .chart-donut-wrap .chart-legend-item:hover,body.ok.theme-light .chart-donut-wrap .chart-legend-item.active{background:var(--ok-bg-2);border-color:var(--ok-cyan)}
body.ok.theme-light .chart-donut-wrap .chart-legend-meter{background:#aeb6ca}
body.ok.theme-light .delta-key.up{color:var(--ok-accent);font-weight:700}
body.ok.theme-light .delta-key.down{color:var(--ok-cyan);font-weight:700}
body.ok.theme-light .delta-key.mid{color:var(--ok-fg-mute);opacity:1;font-weight:600}
body.ok.theme-light .chart-hint{color:var(--ok-fg-mute);border-top-color:var(--ok-line)}
body.ok.theme-light .chart-guide{color:var(--ok-fg-soft)}
body.ok.theme-light .chart-guide strong{color:var(--ok-cyan);font-weight:700}
body.ok.theme-light .chart-sub{color:var(--ok-fg-soft)}
body.ok.theme-light .chart-takeaway{border-left:3px solid var(--ok-magenta);background:color-mix(in oklch,var(--ok-magenta) 6%,var(--ok-bg-0))}
body.ok.theme-light .chart-tooltip{border:1px solid var(--ok-cyan);background:var(--ok-bg-1);box-shadow:0 12px 32px rgba(16,20,40,.14)}
body.ok.theme-light .news-tag{border:1px solid color-mix(in oklch,currentColor 30%,var(--ok-line))}
body.ok.theme-light .news-tag.mercado{background:color-mix(in oklch,var(--ok-cyan) 9%,var(--ok-bg-1))}
body.ok.theme-light .news-tag.cwe{background:color-mix(in oklch,var(--ok-magenta) 9%,var(--ok-bg-1))}
body.ok.theme-light .news-tag.owasp{background:color-mix(in oklch,var(--ok-accent) 9%,var(--ok-bg-1))}
body.ok.theme-light .news-tag.incidente{background:color-mix(in oklch,var(--ok-warning) 9%,var(--ok-bg-1))}
body.ok.theme-light .news-tag.pesquisa{background:color-mix(in oklch,var(--ok-success) 9%,var(--ok-bg-1))}
body.ok.theme-light .owasp-card-id{border:1px solid color-mix(in oklch,var(--ok-cyan) 35%,var(--ok-line));background:color-mix(in oklch,var(--ok-cyan) 7%,var(--ok-bg-1))}
body.ok.theme-light .owasp-card-cwe{border:1px solid var(--ok-line-soft);background:var(--ok-bg-0)}
body.ok.theme-light .ok-terminal,body.ok.theme-light .vscode-shell,body.ok.theme-light .interactive-term{border:1px solid var(--ok-line);box-shadow:0 0 0 1px color-mix(in oklch,var(--ok-cyan) calc(12% * var(--ok-glow)),transparent),0 0 calc(32px * var(--ok-glow)) -10px color-mix(in oklch,var(--ok-cyan) 40%,transparent),0 14px 36px -18px rgba(16,20,40,.14)}
body.ok.theme-light .ok-terminal::before{opacity:.35}
body.ok.theme-light .code-wrap,body.ok.theme-light .diff-panels{border:1px solid var(--ok-line)}
body.ok.theme-light .code-toolbar{border-bottom:1px solid var(--ok-line)}
body.ok.theme-light .research-nav{border-right:1px solid var(--ok-line)}
body.ok.theme-light .research-nav-item{border-bottom:1px solid var(--ok-line-soft)}
body.ok.theme-light .research-nav-item:hover,body.ok.theme-light .research-nav-item.active{background:color-mix(in oklch,var(--ok-cyan) 9%,var(--ok-bg-1))}
body.ok.theme-light .research-nav-item.active{border-left:3px solid var(--ok-accent)}
body.ok.theme-light .owasp-modal-dialog,body.ok.theme-light .cwe-modal-dialog{border:1px solid var(--ok-line);box-shadow:0 24px 64px rgba(16,20,40,.2)}
body.ok.theme-light .owasp-modal-backdrop{background:color-mix(in oklch,var(--ok-bg-0) 78%,transparent)}
body.ok.theme-light .modal-lead{background:linear-gradient(135deg,color-mix(in oklch,var(--ok-accent) 9%,var(--ok-bg-0)),var(--ok-bg-0));border:1px solid color-mix(in oklch,var(--ok-accent) 22%,var(--ok-line))}
body.ok.theme-light .modal-prose-card{border:1px solid var(--ok-line-soft);background:var(--ok-bg-0)}
body.ok.theme-light .modal-callout{border:1px solid var(--ok-line)}
body.ok.theme-light .modal-callout.juice{background:color-mix(in oklch,var(--ok-warning) 7%,var(--ok-bg-0));border-color:color-mix(in oklch,var(--ok-warning) 28%,var(--ok-line))}
body.ok.theme-light .modal-callout.stat{background:color-mix(in oklch,var(--ok-cyan) 7%,var(--ok-bg-0));border-color:color-mix(in oklch,var(--ok-cyan) 28%,var(--ok-line))}
body.ok.theme-light .modal-hl.cwe{background:color-mix(in oklch,var(--ok-magenta) 16%,var(--ok-bg-2))}
body.ok.theme-light .modal-hl.owasp{background:color-mix(in oklch,var(--ok-accent) 16%,var(--ok-bg-2))}
body.ok.theme-light .modal-hl.stat{background:color-mix(in oklch,var(--ok-cyan) 16%,var(--ok-bg-2))}
body.ok.theme-light .ide-split-panel.fix{background:color-mix(in oklch,var(--ok-success) 4%,var(--ok-bg-0))}
body.ok.theme-light .ide-split-code .ide-row.focus-vuln .ide-lc{background:color-mix(in oklch,var(--ok-magenta) 12%,var(--ok-bg-1));border-left:2px solid var(--ok-magenta)}
body.ok.theme-light .ide-split-code .ide-row.focus-fix .ide-lc{background:color-mix(in oklch,var(--ok-success) 12%,var(--ok-bg-1));border-left:2px solid var(--ok-success)}
body.ok.theme-light .cwe-ladder-trend.up{background:color-mix(in oklch,var(--ok-accent) 12%,var(--ok-bg-1));border:1px solid color-mix(in oklch,var(--ok-accent) 30%,var(--ok-line))}
body.ok.theme-light .cwe-ladder-trend.down{background:color-mix(in oklch,var(--ok-cyan) 12%,var(--ok-bg-1));border:1px solid color-mix(in oklch,var(--ok-cyan) 30%,var(--ok-line))}
body.ok.theme-light .market-src-link{border:1px solid var(--ok-line)}
body.ok.theme-light .corr-detail .corr-mini{border:1px solid var(--ok-line)}
body.ok.theme-light .corr-detail .corr-mini:hover{border-color:var(--ok-accent);background:color-mix(in oklch,var(--ok-accent) 7%,var(--ok-bg-1))}

body.ok.theme-light .owasp-card.filter-match{border-color:var(--ok-cyan);box-shadow:0 0 0 1px var(--ok-cyan)}
body.ok.theme-light .cwe-card.filter-match{border-color:var(--ok-magenta);box-shadow:0 0 0 1px var(--ok-magenta)}
body.ok.theme-light .vault-item{border:1px solid var(--ok-line-soft)}
body.ok.theme-light .vault-item.active{border-left:3px solid var(--ok-accent);background:color-mix(in oklch,var(--ok-accent) 7%,var(--ok-bg-1))}
body.ok.theme-light .timeline-node{border:1px solid var(--ok-line)}
body.ok.theme-light .timeline-node.sel{border-color:var(--ok-accent);box-shadow:0 0 0 1px color-mix(in oklch,var(--ok-accent) 30%,var(--ok-line))}
body.ok.theme-light .sim-box.latent{border-color:var(--ok-warning);box-shadow:0 0 0 1px color-mix(in oklch,var(--ok-warning) 35%,var(--ok-line))}
body.ok.theme-light .sim-box.fixed{border-color:var(--ok-success);box-shadow:0 0 0 1px color-mix(in oklch,var(--ok-success) 35%,var(--ok-line))}
body.ok.theme-light .ok-tab.active{border-bottom:2px solid var(--ok-accent)}
body.ok.theme-light .owasp-modal-tabs .ok-tab.active,body.ok.theme-light .cwe-modal-tabs .ok-tab.active{border:1px solid var(--ok-line-soft);border-bottom:none;background:var(--ok-bg-0)}
/* Simuladores — accent escuro no claro (lavanda 72% era ilegível em fundo branco) */
body.ok.theme-light #simuladores-cwe{--sim-accent:oklch(38% .26 292);--sim-accent-soft:color-mix(in oklch,var(--sim-accent) 7%,var(--ok-bg-2))}
body.ok.theme-light #simuladores-cwe .ok-sec-hd h2 em,body.ok.theme-light #simuladores-cwe .section-label{color:var(--sim-accent)}
body.ok.theme-light #simuladores .sim-box.vuln,body.ok.theme-light #simuladores-cwe .sim-box.vuln{border-color:color-mix(in oklch,var(--sim-accent) 55%,var(--ok-line));box-shadow:0 1px 0 color-mix(in oklch,var(--sim-accent) 12%,transparent)}
body.ok.theme-light .sim-panel{border:1px solid var(--ok-line);box-shadow:0 1px 3px rgba(16,20,40,.05)}
body.ok.theme-light #simuladores .sim-panel.vuln .sim-panel-hd,body.ok.theme-light #simuladores-cwe .sim-panel.vuln .sim-panel-hd{background:color-mix(in oklch,var(--sim-accent) 9%,var(--ok-bg-2));color:var(--sim-accent);font-weight:600;border-bottom-color:color-mix(in oklch,var(--sim-accent) 28%,var(--ok-line))}
body.ok.theme-light .sim-panel.fix .sim-panel-hd{background:color-mix(in oklch,var(--ok-success) 8%,var(--ok-bg-2));color:var(--ok-success);font-weight:600}
body.ok.theme-light .sim-output,body.ok.theme-light .jwt-decode,body.ok.theme-light .sim-ide-out{background:var(--ok-bg-2);color:var(--ok-fg);border-top:1px solid var(--ok-line-soft)}
body.ok.theme-light .sim-ide{background:var(--ok-bg-2);border-top:1px solid var(--ok-line-soft)}
body.ok.theme-light .sim-ide-topbar{background:var(--ok-bg-3);color:var(--ok-fg-mute);border-bottom-color:var(--ok-line)}
body.ok.theme-light .sim-ide-out .line.out{color:var(--ok-fg-soft)}
body.ok.theme-light .sim-ide-out .line.cmd{color:var(--ok-accent)}
body.ok.theme-light #simuladores .sim-output .attack,body.ok.theme-light #simuladores-cwe .sim-output .attack{color:var(--sim-accent);font-weight:600}
body.ok.theme-light #simuladores .sim-code-label.vuln,body.ok.theme-light #simuladores-cwe .sim-code-label.vuln{color:var(--sim-accent);font-weight:600}
body.ok.theme-light #simuladores .sim-code-vuln,body.ok.theme-light #simuladores-cwe .sim-code-vuln{color:var(--ok-fg);background:var(--ok-bg-1)!important;border-color:color-mix(in oklch,var(--sim-accent) 35%,var(--ok-line))!important}
body.ok.theme-light #simuladores .sim-code-vuln .attack,body.ok.theme-light #simuladores-cwe .sim-code-vuln .attack,body.ok.theme-light .sim-vuln-idle code{color:var(--sim-accent)}
body.ok.theme-light #simuladores .sim-status.danger,body.ok.theme-light #simuladores-cwe .sim-status.danger{background:color-mix(in oklch,var(--sim-accent) 12%,var(--ok-bg-2));color:var(--sim-accent);font-weight:600;border-color:color-mix(in oklch,var(--sim-accent) 38%,var(--ok-line))}
body.ok.theme-light #simuladores-cwe .sim-run-cwe{background:var(--sim-accent);color:#fff;border-color:color-mix(in oklch,var(--sim-accent) 75%,var(--ok-fg))}
body.ok.theme-light .sim-cwe-badge{color:var(--sim-accent);border-color:color-mix(in oklch,var(--sim-accent) 45%,var(--ok-line));background:color-mix(in oklch,var(--sim-accent) 7%,var(--ok-bg-1));font-weight:600}
body.ok.theme-light .sim-preview{background:var(--ok-bg-2);border-color:var(--ok-line);color:var(--ok-fg)}
body.ok.theme-light .sim-fix-hint{color:var(--ok-fg-mute)}
body.ok.theme-light .heatmap .hm-owasp span{color:var(--ok-accent);font-weight:700}
body.ok.theme-light .heatmap .hm-cwe span{color:var(--ok-cyan);font-weight:600}
/* Highlights e modais — texto de destaque legível */
body.ok.theme-light .hl-takeaway-k,body.ok.theme-light .hl-why-k{color:var(--ok-accent);font-weight:700}
body.ok.theme-light .hl-lede,body.ok.theme-light .hl-takeaway p{color:var(--ok-fg)}
body.ok.theme-light .hl-detail p{color:var(--ok-fg-soft)}
body.ok.theme-light .modal-hl.cwe{color:var(--ok-magenta);background:color-mix(in oklch,var(--ok-magenta) 14%,var(--ok-bg-2))}
body.ok.theme-light .modal-hl.owasp{color:var(--ok-accent);background:color-mix(in oklch,var(--ok-accent) 14%,var(--ok-bg-2))}
body.ok.theme-light .modal-hl.stat{color:var(--ok-cyan);background:color-mix(in oklch,var(--ok-cyan) 14%,var(--ok-bg-2))}
body.ok.theme-light .modal-hl.attack{color:var(--ok-magenta);background:color-mix(in oklch,var(--ok-magenta) 12%,var(--ok-bg-2))}
body.ok.theme-light .modal-hl.path,body.ok.theme-light .modal-hl.juice{color:var(--ok-warning);background:color-mix(in oklch,var(--ok-warning) 12%,var(--ok-bg-2))}
body.ok.theme-light .section-label{color:var(--ok-cyan);font-weight:600}
body.ok.theme-light .lede,body.ok.theme-light .muted,body.ok.theme-light .tab-panel p,body.ok.theme-light .research-body p{color:var(--ok-fg-soft)}
body.ok.theme-light .ok-sec-hd h2{color:var(--ok-fg)}
body.ok.theme-light .ok-sec-hd .ok-right{color:var(--ok-fg-soft)}
body.ok.theme-light .ok-sec-num{color:var(--ok-fg-mute)}
body.ok.theme-light .ok-badge{color:var(--ok-fg-soft);background:#fff;border-color:var(--ok-line)}
body.ok.theme-light .ok-badge.accent,body.ok.theme-light .ok-badge.orange{color:var(--ok-accent);border-color:color-mix(in oklch,var(--ok-accent) 45%,var(--ok-line));font-weight:600}
body.ok.theme-light .ok-badge.magenta{color:var(--ok-magenta);border-color:color-mix(in oklch,var(--ok-magenta) 45%,var(--ok-line));font-weight:600}
body.ok.theme-light .ok-badge.cyan{color:var(--ok-cyan);border-color:color-mix(in oklch,var(--ok-cyan) 45%,var(--ok-line));font-weight:600}
body.ok.theme-light .ok-btn{color:var(--ok-fg)}
body.ok.theme-light .nav-link.active,body.ok.theme-light .nav-link:hover{color:var(--ok-fg)!important}
body.ok.theme-light .research-nav-item:hover,body.ok.theme-light .research-nav-item.active{color:var(--ok-fg)}
body.ok.theme-light .vault-item:hover,body.ok.theme-light .vault-item.active{color:var(--ok-fg)}
body.ok.theme-light .corr-item:hover,body.ok.theme-light .corr-item.sel,body.ok.theme-light .corr-item.hl{color:var(--ok-fg)}
body.ok.theme-light .ok-tab:hover,body.ok.theme-light .ok-tab.active{color:var(--ok-fg)}
body.ok.theme-light .term-cmd-palette .ok-btn.ghost,body.ok.theme-light .sim-actions .ok-btn.ghost{color:var(--ok-fg-soft)}
body.ok.theme-light .term-cmd-palette .ok-btn.ghost:hover,body.ok.theme-light .sim-actions .ok-btn.ghost:hover,body.ok.theme-light .term-cmd-palette .ok-btn.ghost:focus-visible,body.ok.theme-light .sim-actions .ok-btn.ghost:focus-visible{color:var(--ok-fg)!important}
body.ok.theme-light .cwe-ladder-row{background:#fff;border-color:var(--ok-line)}
body.ok.theme-light .cwe-ladder-name,body.ok.theme-light .cwe-ladder-move{color:var(--ok-fg-soft)}
body.ok.theme-light .cwe-ladder-id{color:var(--ok-cyan);font-weight:600}
body.ok.theme-light .cwe-ladder-score{color:var(--ok-fg);font-weight:600}
body.ok.theme-light .owasp-card-rank,body.ok.theme-light .cwe-card-rank{color:var(--ok-accent)}
body.ok.theme-light .owasp-card-title,body.ok.theme-light .cwe-card-title{color:var(--ok-fg)}
body.ok.theme-light .owasp-card-teaser,body.ok.theme-light .cwe-card-teaser{color:var(--ok-fg-soft)}
body.ok.theme-light .news-summary,body.ok.theme-light .news-body{color:var(--ok-fg-soft)}
body.ok.theme-light .news-source{color:var(--ok-cyan);font-weight:600}
body.ok.theme-light .corr-detail{color:var(--ok-fg-soft)}
body.ok.theme-light .corr-toolbar{color:var(--ok-fg)}
.print-cover{display:none}
@media print{
  @page{size:A4 portrait;margin:0}
  .toolbar,.sidebar,.no-print,.chart-tooltip,.owasp-modal,.cwe-modal,.chart-hint,.research-nav,.vault-list,.term-cmd-palette{display:none!important}
  html,body{height:auto!important;overflow:visible!important;margin:0!important;padding:0!important;width:auto!important}
  body.ok,body.ok.theme-light,body.ok.print-mode{
    background:var(--ok-bg-0)!important;color:var(--ok-fg)!important;
    -webkit-print-color-adjust:exact;print-color-adjust:exact;
  }
  body.ok::before,body.ok::after{display:none!important}
  body.ok.print-mode::before{content:""!important;display:block!important;position:fixed!important;top:0!important;left:0!important;right:0!important;width:auto!important;height:16mm!important;margin:0!important;padding:0!important;background:var(--ok-bg-0)!important;z-index:2147483647!important;opacity:1!important;pointer-events:none!important;mask:none!important;-webkit-mask:none!important;animation:none!important;inset:auto!important}
  body.ok.print-mode::after{content:""!important;display:block!important;position:fixed!important;bottom:0!important;left:0!important;right:0!important;width:auto!important;height:18mm!important;margin:0!important;padding:0!important;background:var(--ok-bg-0)!important;z-index:2147483647!important;opacity:1!important;pointer-events:none!important;animation:none!important;inset:auto!important}
  .layout{display:block!important;grid-template-columns:1fr!important;min-height:auto!important;box-sizing:border-box!important;width:100%!important;max-width:100%!important;margin:0!important;padding:16mm 14mm 18mm!important;-webkit-box-decoration-break:clone;box-decoration-break:clone}
  .main{padding:0!important;margin:0!important;max-width:100%!important;width:100%!important;overflow:visible!important;box-sizing:border-box!important}
  .print-cover{display:flex!important;flex-direction:column;align-items:center;justify-content:center;box-sizing:border-box;width:100%!important;min-height:calc(297mm - 34mm);max-height:calc(297mm - 34mm);padding:8mm 6mm 10mm;margin:0!important;text-align:center;background:var(--ok-bg-0)!important;border:1px solid var(--ok-line);border-radius:var(--ok-r-2);page-break-after:always;break-after:page}
  .print-cover-kicker{font-family:var(--ok-mono);font-size:11px;letter-spacing:.16em;text-transform:uppercase;color:var(--ok-fg-mute);margin-bottom:28px}
  .print-cover-title{font-size:clamp(36px,8vw,52px);font-weight:500;letter-spacing:-.035em;line-height:1.08;margin:0 0 20px;color:var(--ok-fg)}
  .print-cover-title em{color:var(--ok-accent);font-style:normal}
  .print-cover-sub{font-size:17px;line-height:1.6;color:var(--ok-fg-soft);max-width:480px;margin:0 auto 32px}
  .print-cover-stats{display:flex;flex-wrap:wrap;justify-content:center;gap:10px 20px;margin-bottom:36px}
  .print-cover-stats span{font-family:var(--ok-mono);font-size:11px;letter-spacing:.06em;color:var(--ok-cyan);padding:6px 12px;border:1px solid var(--ok-line);border-radius:var(--ok-r-1);background:var(--ok-bg-1)}
  .print-cover-rule{width:80px;height:2px;background:linear-gradient(90deg,var(--ok-accent),var(--ok-magenta),transparent);margin:0 auto 24px;opacity:.85}
  .print-cover-foot{font-family:var(--ok-mono);font-size:11px;letter-spacing:.1em;text-transform:uppercase;color:var(--ok-fg-mute)}
  body.corr-filtering .lesson-sec,body.search-active .lesson-sec,.lesson-sec.search-hide{display:block!important}
  body.corr-filtering .lesson-sec:not(.filter-match){border-left:none!important;padding-left:0!important}
  .owasp-card.search-hide,.cwe-card.search-hide{display:flex!important}
  .news-card.search-hide{display:block!important}
  .owasp-card.dimmed,.cwe-card.dimmed{opacity:1!important}
  .ok-sec-hd{display:block!important;margin-bottom:18px!important;page-break-after:avoid;break-after:avoid-page}
  .ok-sec-hd .ok-right{max-width:100%!important;margin-top:10px!important}
  .ok-sec-hd h2{orphans:2;widows:2}
  .ok-sec-hd+.market-strip,.ok-sec-hd+.hl-rail,.ok-sec-hd+.charts-stack,.ok-sec-hd+.corr-hub,.ok-sec-hd+.research-hub,.ok-sec-hd+.grid-2,.ok-sec-hd+.ok-terminal,.section-label+.source-bar,.section-label+.hl-section{page-break-before:avoid;break-before:avoid-page}
  #intro.hero{page-break-before:always;break-before:page;padding:0 0 20px!important}
  .hero{padding:0 0 20px!important;page-break-inside:auto;break-inside:auto}
  .lesson-sec{padding:5mm 0 4mm!important;page-break-before:auto;break-before:auto;page-break-inside:auto;break-inside:auto;overflow:visible!important}
  #mercado,#pesquisa,#noticias,#correlacao,#terminal-lab,#code-vault,#simuladores,#simuladores-cwe,#owasp-hub,#ponte-owasp-cwe,#cwe-hub,#juice-setup,#juice-ide,#quiz{page-break-before:always;break-before:page;padding-top:0!important}
  .lesson-sec[id^="owasp-A"],.lesson-sec.cwe-sec{page-break-before:auto;break-before:auto;padding-top:4mm!important}
  .lesson-sec[id^="owasp-A"] .ok-sec-hd,.lesson-sec.cwe-sec .ok-sec-hd{page-break-before:avoid;break-before:avoid-page}
  .hl-block,.source-link,.metric,.metric-link,.market-src-link,.ok-card,.news-card,.owasp-card,.cwe-card,.hl-rail-hd,.methodology-note{page-break-inside:avoid;break-inside:avoid-page}
  .chart-box,.chart-embed,.chart-body-split,.chart-body-bar,.chart-ring-wrap,.chart-legend-panel,.chart-plot,.chart-plot-ranked,.chart-wrap,.chart-hd,.chart-hint,.chart-guide,.chart-takeaway,.chart-delta-key{page-break-inside:avoid!important;break-inside:avoid-page!important}
  .chart-box{display:block!important;page-break-before:auto;break-before:auto;margin:0 0 10mm!important}
  .chart-hd,.chart-sub,.section-label+.chart-box{page-break-after:avoid;break-after:avoid-page}
  .charts-stack,.charts-grid,.charts-inline-2{page-break-inside:auto;break-inside:auto}
  .charts-stack>.chart-box,.charts-grid>.chart-box,.charts-inline-2>.chart-box,.corr-hub .chart-box{page-break-inside:avoid!important;break-inside:avoid-page!important}
  .sim-box,.vscode-shell,.ok-terminal,.compare-table,.data-table,.research-panel{page-break-inside:avoid;break-inside:avoid-page}
  .sim-box,.vscode-shell{page-break-before:auto;break-before:auto}
  p,li{orphans:3;widows:3}
  .hl-rail+.hl-rail,.market-strip+.hl-rail,.source-bar+.hl-rail{margin-top:16px!important}
  .heatmap-wrap,.corr-sidebar,.corr-layout>*,.sidebar{position:static!important;max-height:none!important;overflow:visible!important;top:auto!important;transform:none!important}
  .research-hub,.research-panels,.vault-split,.vault-detail,.timeline-vertical,.corr-list,.vscode-shell,.ide-split-wrap,.juice-ide-meta,.sim-ide-out,.sim-output,.term-embed-out,.vscode-term-out,.chart-legend-list,.chart-legend-panel,.interactive-term .term-output,.diff-panels{max-height:none!important;overflow:visible!important;min-height:0!important}
  .research-hub,.vault-split,.hl-block,.chart-box,.corr-hub,.news-card,.vscode-shell{overflow:visible!important;box-shadow:none!important}
  .source-bar{display:grid!important;grid-template-columns:repeat(3,minmax(0,1fr))!important;gap:12px!important;margin:0 0 20px!important}
  .source-link{min-width:0!important;flex:none!important;width:auto!important;background:var(--ok-bg-1)!important;border:1px solid var(--ok-line)!important;color:var(--ok-fg)!important;box-shadow:none!important;transform:none!important}
  .source-name,.metric-val,.hl-title,.hero h1,.ok-sec-hd h2,.chart-legend-label,.chart-legend-val,.hl-kicker,.hl-stat-val{color:var(--ok-fg)!important}
  .source-desc,.metric-lbl,.metric-src,.hl-lede,.hl-quote-text,.hl-body p,.hl-takeaway p,.hl-rail-sub,.hl-mencao-author,.hl-bullets li,.hl-detail p,.lede,.muted,.chart-sub,.chart-guide,.news-summary{color:var(--ok-fg-soft)!important}
  .hl-block{min-height:0!important;overflow:visible!important;background:var(--ok-bg-1)!important;border:1px solid var(--ok-line)!important;color:var(--ok-fg)!important;box-shadow:none!important;transform:none!important}
  .hl-block:hover{box-shadow:none!important;transform:none!important}
  .hl-grid{display:grid!important;grid-template-columns:1fr!important;gap:12px!important}
  .hl-grid.hl-grid-single .hl-block{grid-column:1!important;max-width:100%!important;width:100%!important}
  .hl-rail{margin:20px 0 0!important;clear:both;overflow:visible!important}
  .hl-rail-hd{display:block!important;margin-bottom:12px!important}
  .hl-rail-sub{display:block!important;margin-top:4px!important;color:var(--ok-fg-mute)!important}
  .hl-hd-top{display:block!important}
  .hl-source-link{display:inline-block!important;max-width:100%!important;word-break:break-word!important;margin-top:8px!important}
  .hl-quote-text,.hl-takeaway,.hl-bullets-wrap,.hl-hd,.hl-stat,.hl-bullets-wrap,.hl-why{background:var(--ok-bg-2)!important;border-color:var(--ok-line-soft)!important}
  .hl-source-link{background:color-mix(in oklch,var(--ok-cyan) 8%,var(--ok-bg-1))!important;border:1px solid var(--ok-line)!important;color:var(--ok-cyan)!important}
  .metric,.metric-link,.market-src-link,.ok-card,.news-card,.owasp-card,.cwe-card,.chart-box,.corr-hub,.methodology-note{background:var(--ok-bg-1)!important;border:1px solid var(--ok-line)!important;color:var(--ok-fg)!important;box-shadow:none!important;transform:none!important}
  .corr-layout,.charts-grid,.charts-inline-2,.chart-body-split,.sim-panels,.grid-2,.owasp-bento,.cwe-bento,.news-grid,.charts-stack{grid-template-columns:1fr!important;gap:12px!important;display:grid!important}
  .market-strip{display:grid!important;grid-template-columns:repeat(3,minmax(0,1fr))!important;gap:12px!important;margin:0 0 20px!important}
  .market-sources{display:grid!important;grid-template-columns:repeat(2,minmax(0,1fr))!important;gap:10px!important}
  .metric,.metric-link,.market-src-link{min-width:0!important;max-width:none!important;flex:none!important}
  .research-hub,.vault-split{display:block!important;border:1px solid var(--ok-line)!important;background:var(--ok-bg-1)!important}
  .research-panels,.vault-detail{display:block!important;padding:16px!important;border:none!important}
  .research-panel,.vault-detail .pattern-detail.active{display:block!important;margin-bottom:20px!important;page-break-inside:avoid}
  .tab-panel,.term-panel{display:block!important}
  .pattern-detail{display:none!important}
  .pattern-detail.active{display:block!important}
  .owasp-card-teaser,.cwe-card-teaser{-webkit-line-clamp:unset!important;display:block!important;overflow:visible!important}
  .news-card,.owasp-card,.cwe-card{min-height:0!important}
  canvas{max-width:100%!important}
  .chart-ring-wrap{min-height:0!important;max-height:72mm!important;padding:10px!important}
  .chart-plot,.chart-plot-ranked{min-height:0!important;padding:8px 10px!important}
  .chart-plot-ranked canvas,.chart-ring-wrap canvas,.chart-body-bar canvas{max-height:68mm!important;width:100%!important;height:auto!important}
  .chart-legend-list{max-height:none!important}
  .chart-donut-wrap .chart-legend-list,.chart-cwe-scores-wrap .chart-legend-list,.chart-delta-wrap .chart-legend-list{max-height:none!important}
  .vscode-shell,.ok-terminal,.interactive-term,.sim-box,.chart-box{border:1px solid var(--ok-line)!important}
  .hl-rail,.hl-section,.market-strip,.source-bar,.news-grid,.owasp-bento,.cwe-bento{page-break-inside:auto;break-inside:auto}
  h1,h2,h3,h4,.section-label,.ok-eyebrow,.hl-rail-hd,.print-cover-title{page-break-after:avoid;break-after:avoid-page}
  .lede,.hero h1,.ok-eyebrow{page-break-after:avoid;break-after:avoid-page}
  tr{page-break-inside:avoid;break-inside:avoid-page}
  .section-label,.chart-legend-title,.ok-eyebrow{color:var(--ok-fg-mute)!important}
  p,li,td,th{color:var(--ok-fg-soft)!important}
  .data-table th,.data-table td,.compare-table th,.compare-table td{border-color:var(--ok-line)!important}
  .data-table th{background:var(--ok-bg-2)!important;color:var(--ok-fg-mute)!important}
  a{color:var(--ok-cyan)!important;text-decoration:underline}
  a[href^="http"]::after{content:none!important}
  .lede a::after,.source-link::after,.metric-link::after,.market-src-link::after,.hl-source-link::after,.table-caption a::after,.methodology-note a::after,.nav-link::after,.ok-btn::after{content:none!important}
}
"""

owasp_html = render_owasp_hub(OWASP_LIST, OWASP_PREVALENCE)
cwe_charts_html = f'''<div class="charts-stack">
{render_chart_box(
  "chart-cwe-scores",
  "Top 10 CWE — score MITRE 2025",
  "Quanto maior o score, mais CVEs reais usam essa fraqueza · 39.080 CVEs analisados",
  440, True, "chart-cwe-scores-wrap", False, True,
  guide="Barras = score MITRE (quanto maior, mais prevalente em CVEs reais). Nomes completos ficam na legenda à direita.",
  takeaway="XSS (CWE-79) tem score 60,38 — mais que o dobro do segundo colocado. Priorize correção e testes nessas 10 primeiras.",
)}
{render_chart_box(
  "chart-cwe-delta",
  "Quem mais subiu e desceu no ranking",
  "Comparativo MITRE TOP 25 2025 vs 2024 · só fraquezas que mudaram de posição",
  360, True, "", False, False,
  guide="Centro = ranking 2024. Laranja à direita = subiu (mais crítica). Ciano à esquerda = desceu. Detalhes na legenda.",
  takeaway="Maior queda: CWE-77 (−10 pos.). Maior subida: CWE-476 (+8). CWE-862 (+5) reforça o foco em autorização (A01 OWASP).",
  delta_key=True,
  delta=True,
)}
</div>
{render_cwe_rank_ladder(CWE_TOP25_FULL)}'''
cwe_html = cwe_charts_html + render_cwe_hub(CWE_TOP25_FULL)
assert len(CWE_TOP25_FULL) == 25, f"Esperado 25 CWE, got {len(CWE_TOP25_FULL)}"

sidebar_html = render_sidebar(OWASP_LIST, CWE_TOP25_FULL)
market_strip_html = render_market_strip()
compare_rows = "".join(f'<tr><td>{a}</td><td>{esc(o21)}</td><td>{esc(o25)}</td><td>{esc(chg)}</td></tr>' for a,o21,o25,chg in OWASP_2021_VS_2025)

quiz_json = json.dumps([{"q":q,"opts":[o1,o2,o3],"a":a} for q,o1,o2,o3,a in QUIZ], ensure_ascii=False)
corr_json = json.dumps([{"o":a,"c":c,"s":s,"n":n} for a,c,s,n in CORRELATIONS], ensure_ascii=False)
cwe_chart = json.dumps([{
  "l": cwe_chart_label(c),
  "id": c["id"],
  "name_pt": c["name_pt"],
  "name": c["name"],
  "v": c["score"],
  "rank": c["rank"],
  "trend": c["trend"],
  "kev": c["kev"],
} for c in CWE_TOP25_FULL], ensure_ascii=False)
owasp_chart = json.dumps([{"l":o["id"],"v":len([1 for a,cc,s,n in CORRELATIONS if a==o["id"]])} for o in OWASP_LIST], ensure_ascii=False)
kev_chart = json.dumps(chart_cwe_kev(CWE_TOP25_FULL), ensure_ascii=False)
prev_chart = json.dumps(chart_owasp_prev(), ensure_ascii=False)
breach_chart = json.dumps(chart_breach_vectors(), ensure_ascii=False)
delta_chart = json.dumps(chart_cwe_delta(CWE_TOP25_FULL), ensure_ascii=False)
term_json = json_script_embed(TERMINAL_LABS)
juice_ide_json = json_script_embed(build_juice_ide_entries(JUICE, OWASP_LIST))

OUT = f"""<!DOCTYPE html>
<!-- Arquivo único autocontido: CSS, JS, dados e fontes embutidos. Abra com duplo clique no navegador — não precisa de servidor nem de outros arquivos. -->
<html lang="pt-BR">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>OWASP Top 10:2025 + CWE TOP 25 — Referência AppSec</title>
<style>{EMBEDDED_FONTS}</style>
<style>{OKAMI}{PATTERNS}{PAGE_CSS}</style>
<script>(function(){{if('scrollRestoration' in history)history.scrollRestoration='manual';if(location.hash&&location.hash.length>1)history.replaceState(null,'',location.pathname+location.search);window.scrollTo(0,0);document.documentElement.scrollTop=0;}})();</script>
</head>
<body class="ok">
<header class="toolbar no-print">
  <span class="brand">// appsec · owasp + cwe top 25</span>
  <input class="ok-input" id="search" type="search" placeholder="Buscar OWASP, CWE…"/>
  <div class="progress-bar" style="width:80px;height:3px;background:var(--ok-bg-3)"><i id="progress" style="display:block;height:100%;background:var(--ok-accent);width:0"></i></div>
  <button class="ok-btn ghost sm" id="btn-sidebar" type="button" title="Menu">☰</button>
  <button class="ok-btn ghost sm" id="btn-theme" type="button">Tema</button>
  <button class="ok-btn cyan sm" id="btn-present" type="button">Modo apresentação</button>
  <button class="ok-btn solid sm" id="btn-pdf" type="button">Exportar PDF</button>
</header>
<div class="layout">
{sidebar_html}
<main class="main">

<section class="print-cover" aria-hidden="true">
  <span class="print-cover-kicker">Segurança de Aplicações · Referência interativa</span>
  <h1 class="print-cover-title">OWASP Top 10<em>:</em>2025<br/>+ CWE TOP 25</h1>
  <p class="print-cover-sub">Material de referência com categorias OWASP Top 10:2025, fraquezas CWE MITRE, correlações, laboratórios e checklist de mitigação.</p>
  <div class="print-cover-stats">
    <span>2,8M+ apps testadas</span>
    <span>39.080 CVEs analisados</span>
    <span>10 OWASP · 25 CWE</span>
  </div>
  <div class="print-cover-rule"></div>
  <p class="print-cover-foot">AppSec · Segurança de Aplicações</p>
</section>

<section class="hero" id="intro">
  <div class="ok-eyebrow">Segurança de aplicações · Referência interativa</div>
  <h1>OWASP Top 10<em>:</em>2025<br/>+ CWE TOP 25</h1>
  <p class="lede">Guia que cruza as <strong>10 categorias do OWASP Top 10</strong> com as <strong>25 fraquezas do CWE TOP 25 (MITRE)</strong>. Cada item reúne conceitos, exemplos de código vulnerável e correção, casos documentados, matriz OWASP↔CWE, simuladores, terminais interativos e checklist de mitigação — com labs práticos no <a href="https://github.com/juice-shop/juice-shop" style="color:var(--ok-cyan)">OWASP Juice Shop</a>.</p>
  <span class="section-label">Fontes primárias e referências</span>
  <div class="source-bar">{source_links_html}</div>
  {render_section_highlight_rails("intro", title="Comece por aqui", subtitle="2 trechos por linha — contexto e fundamentos")}
</section>

<section class="lesson-sec" id="mercado">
  <div class="ok-sec-hd"><div class="ok-left"><div class="ok-sec-num"><b>§00</b><span>·</span><span>mercado</span></div><h2>Panorama <em>2024–2025</em></h2></div>
  <div class="ok-right">Dados OWASP Top 10:2025 (2,8M+ apps), MITRE CWE TOP 25 (39.080 CVEs), DBIR, IBM.</div></div>
  <div class="market-strip">{market_strip_html}</div>
  {render_section_highlights("mercado", layout="grid", offset=0, limit=2)}
  <span class="section-label">Fontes dos dados — clique para abrir o relatório</span>
  <div class="market-sources">{market_sources_html}</div>
  {render_owasp_prevalence()}
  <div class="charts-stack">
  {render_chart_box("chart-owasp-prev", "OWASP 2025 — prevalência publicada (%)", "Somente A01, A02 e A04 têm % em testes (2,8M+ apps). As outras 7 categorias vêm do community survey — veja a tabela acima · clique para filtrar", 240, True, "", False, True)}
  {render_chart_box("chart-breach-vectors", "Vetores de breach — DBIR 2025", "Distribuição didática de vetores iniciais (credenciais, phishing, vuln, misconfig)", 300, True, "", True)}
  </div>
  {render_section_highlights("mercado", layout="grid", offset=2, limit=2)}
  <div class="methodology-note"><strong>Metodologia OWASP Top 10:2025</strong> (<a href="https://owasp.org/Top10/2025/0x00_2025-Introduction/" target="_blank" rel="noopener">documento oficial</a>): ranking data-informed com 8 categorias vindas de testes em 2,8M+ aplicações e 2 promovidas pela pesquisa comunitária (supply chain e logging/alerting). Dados IBM: <a href="https://www.ibm.com/reports/data-breach" target="_blank" rel="noopener">Cost of a Data Breach 2025</a> (US$ 4,4M médio, gap de governança IA). DBIR: <a href="https://www.verizon.com/business/resources/reports/dbir/" target="_blank" rel="noopener">Verizon DBIR 2025</a>. CWE: <a href="https://cwe.mitre.org/top25/archive/2025/2025_key_insights.html" target="_blank" rel="noopener">MITRE TOP 25 2025</a> (67% CNA mapping).</div>
  <p class="table-caption" style="margin-top:var(--ok-s-7)">Comparativo de ranking — <a href="https://owasp.org/Top10/2021/" target="_blank" rel="noopener">OWASP 2021</a> vs <a href="https://owasp.org/Top10/2025/" target="_blank" rel="noopener">OWASP 2025</a>.</p>
  <table class="compare-table"><thead><tr><th>Pos.</th><th>OWASP 2021</th><th>OWASP 2025</th><th>Evolução</th></tr></thead><tbody>{compare_rows}</tbody></table>
</section>

<section class="lesson-sec" id="pesquisa">
  <div class="ok-sec-hd"><div class="ok-left"><div class="ok-sec-num"><b>§R</b><span>·</span><span>intel</span></div><h2>Inteligência de <em>ameaças</em></h2></div>
  <div class="ok-right">Análise consolidada MITRE, OWASP, Verizon DBIR, IBM, CISA, PortSwigger — selecione à esquerda.</div></div>
  {render_section_highlights("pesquisa", layout="grid", offset=0, limit=2, title="Trechos da inteligência", subtitle="Citações e menções — primeira leva")}
  {render_research_hub()}
  {render_chart_box("chart-cwe-kev", "CWE com CVEs no CISA KEV", "Fraquezas do TOP 25 com exploit confirmado in-the-wild · prioridade de patch", 260)}
  {render_section_highlights("pesquisa", layout="grid", offset=2, limit=2)}
  <span class="section-label" style="margin-top:var(--ok-s-8)">Timeline de breaches — clique para filtrar OWASP↔CWE</span>
  {render_breach_timeline()}
</section>

<section class="lesson-sec" id="noticias">
  <div class="ok-sec-hd"><div class="ok-left"><div class="ok-sec-num"><b>§N</b><span>·</span><span>news</span></div><h2>Notícias &amp; <em>pesquisa</em></h2></div>
  <div class="ok-right">Curadoria 2024–2026 · MITRE, OWASP, IBM, Verizon, CISA · clique para filtrar na matriz</div></div>
  {render_section_highlight_rails("noticias", title="Trechos e citações", subtitle="Contexto editorial — 2 por linha")}
  {render_news_feed(NEWS_FEED)}
</section>

<section class="lesson-sec" id="correlacao">
  <div class="ok-sec-hd"><div class="ok-left"><div class="ok-sec-num"><b>§mapa</b><span>·</span><span>owasp ↔ cwe</span></div><h2>Matriz de <em>correlação</em></h2></div>
  <div class="ok-right">Clique na célula, no cabeçalho OWASP/CWE ou na lista lateral.</div></div>
  {render_section_highlights("correlacao", layout="grid")}
  <div class="corr-hub">
    <div class="corr-toolbar">
      <span>{len(CORRELATIONS)} correlações · filtro: <strong id="filter-label">nenhum</strong></span>
      <button type="button" class="ok-btn ghost sm" id="filter-clear">Limpar filtro</button>
    </div>
    {render_chart_box("chart-owasp-donut", "Correlações por categoria OWASP", "Quantidade de CWEs correlacionadas em cada categoria · clique para filtrar", 220, True, "chart-corr-viz", True)}
    <div class="corr-layout">
      <div class="heatmap-wrap">{render_heatmap()}</div>
      <aside class="corr-sidebar">
        <div class="corr-list-hd"><strong>{len(CORRELATIONS)} correlações</strong><span id="corr-list-count">todas visíveis</span></div>
        <div class="corr-list" id="corr-list">{render_corr_detail()}</div>
      </aside>
    </div>
    <div class="corr-detail" id="corr-detail">Selecione uma correlação na matriz 10×25 para filtrar as seções e ver a explicação.</div>
  </div>
</section>

<section class="lesson-sec" id="terminal-lab">
  <div class="ok-sec-hd"><div class="ok-left"><div class="ok-sec-num"><b>§term</b><span>·</span><span>cli</span></div><h2>Terminal <em>Lab</em></h2></div>
  <div class="ok-right">Simulador interativo — digite comandos (help, curl, sqlmap, npm audit…)</div></div>
  {render_section_highlights("terminal-lab", layout="grid")}
  {render_terminal_full()}
</section>

<section class="lesson-sec" id="code-vault">
  <div class="ok-sec-hd"><div class="ok-left"><div class="ok-sec-num"><b>§code</b><span>·</span><span>vault</span></div><h2>Cofre de <em>código</em></h2></div>
  <div class="ok-right">{len(CODE_PATTERNS)} padrões vulnerável→correção · {len(JUICE)} labs Juice Shop</div></div>
  <div class="vault-filters">
    <button type="button" class="ok-btn sm solid vault-filter" data-vault="">Todos ({len(CODE_PATTERNS)})</button>
    {"".join(f'<button type="button" class="ok-btn sm ghost vault-filter" data-vault="{o["id"]}">{o["id"]}</button>' for o in OWASP_LIST)}
  </div>
  {render_section_highlights("code-vault", layout="grid")}
  {render_code_vault()}
</section>

<section class="lesson-sec lesson-sec-sim-owasp" id="simuladores">
  <div class="ok-sec-hd"><div class="ok-left"><div class="ok-sec-num"><b>§sim</b><span>·</span><span>owasp</span></div><h2>Simuladores <em>OWASP Top 10</em></h2></div>
  <div class="ok-right">10 labs · 1 por categoria OWASP:2025 · ▶ Executar ataque · <strong>Fix</strong> corrige na IDE.</div></div>
  {render_section_highlights("simuladores", layout="grid")}
  <div class="sim-grid">
{render_sim_grid(SIMULATORS, esc, sim_ide_panel)}
  </div>
</section>

<section class="lesson-sec lesson-sec-sim-cwe" id="simuladores-cwe">
  <div class="ok-sec-hd"><div class="ok-left"><div class="ok-sec-num"><b>§sim</b><span>·</span><span>cwe</span></div><h2>Simuladores <em>CWE TOP 25</em></h2></div>
  <div class="ok-right">25 labs · 1 por fraqueza MITRE 2025 · Juice Shop + cenários nativos · <strong>Fix</strong> passo a passo.</div></div>
  {render_section_highlights("simuladores-cwe", layout="grid")}
  <div class="sim-grid">
{render_sim_grid(CWE_SIMULATORS, esc, sim_ide_panel, variant="cwe")}
  </div>
</section>

{owasp_html}

<section class="lesson-sec hl-sec-bridge" id="ponte-owasp-cwe">
  {render_section_highlights("ponte-owasp-cwe", layout="grid", title="Da categoria OWASP à fraqueza CWE", subtitle="Ponte entre os dois hubs — leia antes de abrir o TOP 25")}
</section>

{cwe_html}

<section class="lesson-sec" id="juice-setup">
  <div class="ok-sec-hd"><div class="ok-left"><div class="ok-sec-num"><b>§lab</b><span>·</span><span>setup</span></div><h2>Juice Shop <em>— setup</em></h2></div></div>
  {render_section_highlights("juice-setup", layout="grid")}
  <div class="grid-2">
    <div class="ok-terminal"><div class="topbar"><span class="dots"><span></span><span></span><span></span></span><span>docker · deploy</span></div>
    <div class="body">
      <div class="line"><span class="prompt">$</span><span class="cmd">docker run --rm -p 3000:3000 bkimminich/juice-shop</span></div>
      <div class="line out"><span class="ok-ok">→</span> http://localhost:3000</div>
      <div class="line"><span class="prompt">$</span><span class="cmd">docker compose up -d</span></div>
      <div class="line out"><span class="ok-ok">→</span> Score Board em /#/score-board</div>
    </div></div>
    <div class="ok-terminal"><div class="topbar"><span class="dots"><span></span><span></span><span></span></span><span>source · audit</span></div>
    <div class="body">
      <div class="line"><span class="prompt">$</span><span class="cmd">git clone https://github.com/juice-shop/juice-shop.git && cd juice-shop</span></div>
      <div class="line"><span class="prompt">$</span><span class="cmd">npm install && npm audit --audit-level=moderate</span></div>
      <div class="line out"><span class="ok-warn">!</span> Dezenas de CVEs intencionais — correlacione com A03</div>
      <div class="line"><span class="prompt">$</span><span class="cmd">grep -r "sequelize.query" routes/ lib/</span></div>
      <div class="line out"><span class="ok-ok">→</span> login.ts, search.ts — SQLi</div>
    </div></div>
  </div>
</section>

{render_juice_ide(len(JUICE))}

<section class="lesson-sec" id="quiz">
  <div class="ok-sec-hd"><div class="ok-left"><div class="ok-sec-num"><b>§?</b><span>·</span><span>quiz</span></div><h2>Quiz de verificação</h2></div></div>
  {render_section_highlights("quiz", layout="grid")}
  <div class="ok-card"><h4 id="quiz-q">Carregando…</h4><div id="quiz-opts" style="display:flex;flex-wrap:wrap;gap:8px;margin:12px 0"></div><p id="quiz-fb" class="ok-hint"></p><button class="ok-btn cyan sm" id="quiz-next" type="button">Próxima →</button></div>
</section>

</main></div>

<script type="application/json" id="data-quiz">{quiz_json}</script>
<script type="application/json" id="data-corr">{corr_json}</script>
<script type="application/json" id="data-cwe-chart">{cwe_chart}</script>
<script type="application/json" id="data-owasp-chart">{owasp_chart}</script>
<script type="application/json" id="data-kev-chart">{kev_chart}</script>
<script type="application/json" id="data-prev-chart">{prev_chart}</script>
<script type="application/json" id="data-breach-chart">{breach_chart}</script>
<script type="application/json" id="data-delta-chart">{delta_chart}</script>
<script type="application/json" id="data-terminals">{term_json}</script>
<script type="application/json" id="data-juice-ide">{juice_ide_json}</script>
<script>{APP_JS}</script>
</body>
</html>"""

OUT_DIR.mkdir(parents=True, exist_ok=True)
OUT_FILE.write_text(OUT, encoding="utf-8")
print(f"OK: {OUT_FILE} ({len(OUT):,} bytes) | standalone | CWE: {len(CWE_TOP25_FULL)} | OWASP: {len(OWASP_LIST)} | Juice: {len(JUICE)} | Patterns: {len(CODE_PATTERNS)}")