import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random
import time

# ─────────────────────────────────────────────
#  PAGE CONFIG & GLOBAL THEME
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="4SAVR · Inteligência de Varejo",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─────────────────────────────────────────────
#  CUSTOM CSS – Navy + Emerald, clean & modern
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=Inter:wght@300;400;500;600&display=swap');

:root {
    --navy:    #0B1E3F;
    --navy2:   #112952;
    --emerald: #00C48C;
    --emerald2:#00A876;
    --gold:    #FFB547;
    --red:     #FF5252;
    --bg:      #0D1B2A;
    --card:    #132237;
    --card2:   #1A2E48;
    --text:    #E8EFF7;
    --muted:   #7A9ABF;
    --border:  rgba(0,196,140,0.18);
}

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    background-color: var(--bg) !important;
    color: var(--text) !important;
}

/* hide streamlit chrome */
#MainMenu, footer, header {visibility: hidden;}
.block-container {padding: 1.5rem 2.5rem 3rem !important; max-width: 1400px !important;}

/* headings */
h1,h2,h3 { font-family: 'Syne', sans-serif !important; }

/* ── HERO HEADER ── */
.hero {
    background: linear-gradient(135deg, var(--navy) 0%, #0f3460 60%, #0d2137 100%);
    border-radius: 18px;
    padding: 2.2rem 2.8rem;
    margin-bottom: 1.8rem;
    border: 1px solid var(--border);
    position: relative;
    overflow: hidden;
}
.hero::before {
    content:'';
    position:absolute; inset:0;
    background: radial-gradient(ellipse at 80% 50%, rgba(0,196,140,0.12) 0%, transparent 70%);
}
.hero-title {
    font-family:'Syne',sans-serif;
    font-size:2.6rem; font-weight:800;
    background: linear-gradient(90deg, #fff 0%, var(--emerald) 100%);
    -webkit-background-clip:text; -webkit-text-fill-color:transparent;
    margin:0; line-height:1.1;
}
.hero-sub { color:var(--muted); font-size:1.05rem; margin-top:.5rem; }
.hero-badge {
    display:inline-block; background:rgba(0,196,140,.15);
    color:var(--emerald); border:1px solid var(--emerald2);
    border-radius:20px; padding:.25rem .8rem;
    font-size:.8rem; font-weight:600; letter-spacing:.04em;
    margin-bottom:.6rem;
}

/* ── CARDS ── */
.card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 1.4rem 1.6rem;
    margin-bottom: 1rem;
}
.card-sm {
    background: var(--card2);
    border: 1px solid rgba(255,255,255,.06);
    border-radius: 10px;
    padding: 1rem 1.2rem;
    margin-bottom: .6rem;
}

/* ── METRIC BOXES ── */
.metric-box {
    background: linear-gradient(135deg, var(--card) 0%, var(--card2) 100%);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1.2rem 1.4rem;
    text-align: center;
}
.metric-val { font-family:'Syne',sans-serif; font-size:2rem; font-weight:700; color:var(--emerald); }
.metric-lbl { font-size:.82rem; color:var(--muted); margin-top:.15rem; }

/* ── PRICE RANKING ── */
.rank-item {
    display:flex; align-items:center; justify-content:space-between;
    background: var(--card2);
    border: 1px solid rgba(255,255,255,.06);
    border-radius: 10px;
    padding: .85rem 1.2rem;
    margin-bottom: .5rem;
    transition: border-color .2s;
}
.rank-item:hover { border-color: var(--emerald); }
.rank-badge {
    width:28px; height:28px; border-radius:50%;
    display:flex; align-items:center; justify-content:center;
    font-weight:700; font-size:.85rem;
    flex-shrink:0; margin-right:.9rem;
}
.rank-1 { background:linear-gradient(135deg,#FFB547,#FF8C00); color:#000; }
.rank-2 { background:linear-gradient(135deg,#aaa,#666); color:#fff; }
.rank-3 { background:linear-gradient(135deg,#cd7f32,#a0522d); color:#fff; }
.rank-other { background:var(--card); color:var(--muted); border:1px solid rgba(255,255,255,.1); }
.rank-name  { flex:1; font-weight:500; font-size:.95rem; }
.rank-price { font-family:'Syne',sans-serif; font-weight:700; font-size:1.1rem; color:var(--emerald); }
.rank-best  { font-size:.75rem; color:var(--emerald); background:rgba(0,196,140,.12); padding:.15rem .5rem; border-radius:20px; margin-left:.6rem; }

/* ── OFFER FEED ── */
.offer-card {
    background: linear-gradient(135deg, var(--card) 60%, rgba(0,196,140,.08));
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1rem 1.3rem;
    margin-bottom: .7rem;
    position:relative;
}
.offer-badge {
    display:inline-block;
    background:linear-gradient(90deg,var(--emerald),var(--emerald2));
    color:#000; font-weight:700; font-size:.72rem;
    padding:.2rem .6rem; border-radius:20px;
    text-transform:uppercase; letter-spacing:.05em;
}
.offer-flash { color:var(--gold); font-size:.82rem; }
.score-bar-wrap { background:rgba(255,255,255,.06); border-radius:20px; height:8px; margin-top:.4rem; }
.score-bar { height:8px; border-radius:20px; background:linear-gradient(90deg,var(--emerald),#00ff9f); }

/* ── POINTS BANNER ── */
.points-banner {
    background: linear-gradient(135deg,rgba(255,181,71,.15),rgba(255,181,71,.05));
    border: 1px solid rgba(255,181,71,.3);
    border-radius: 12px;
    padding: 1rem 1.4rem;
    display:flex; align-items:center; gap:1rem;
}
.points-val { font-family:'Syne',sans-serif; font-size:2rem; font-weight:800; color:var(--gold); }

/* ── ALERT CARDS ── */
.alert-warn {
    background:rgba(255,82,82,.1);
    border:1px solid rgba(255,82,82,.3);
    border-radius:10px; padding:.9rem 1.2rem;
    margin-bottom:.5rem;
}
.alert-ok {
    background:rgba(0,196,140,.08);
    border:1px solid var(--border);
    border-radius:10px; padding:.9rem 1.2rem;
    margin-bottom:.5rem;
}

/* ── TABS ── */
.stTabs [data-baseweb="tab-list"] {
    gap:.5rem;
    background:var(--card);
    border-radius:12px; padding:.4rem .5rem;
    border:1px solid var(--border);
}
.stTabs [data-baseweb="tab"] {
    border-radius:8px !important;
    color:var(--muted) !important;
    font-weight:500 !important;
    font-family:'Inter',sans-serif !important;
    padding:.45rem 1.2rem !important;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg,var(--emerald),var(--emerald2)) !important;
    color:#000 !important; font-weight:700 !important;
}

/* ── BUTTONS ── */
.stButton > button {
    background: linear-gradient(135deg,var(--emerald),var(--emerald2));
    color:#000 !important; font-weight:700 !important;
    border:none !important; border-radius:10px !important;
    padding:.6rem 1.6rem !important;
    font-family:'Inter',sans-serif !important;
    transition: opacity .2s, transform .15s !important;
}
.stButton > button:hover { opacity:.88; transform:translateY(-1px); }

/* inputs */
.stTextInput input, .stSelectbox select, .stNumberInput input {
    background: var(--card2) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    color: var(--text) !important;
}
.stTextInput input:focus, .stSelectbox select:focus {
    border-color: var(--emerald) !important;
    box-shadow: 0 0 0 2px rgba(0,196,140,.2) !important;
}

/* dataframe */
.stDataFrame { border-radius: 10px; overflow: hidden; }
[data-testid="stDataFrameResizable"] { background: var(--card2); }

/* divider */
hr { border-color: rgba(255,255,255,.06) !important; }

/* section titles */
.sec-title {
    font-family:'Syne',sans-serif;
    font-size:1.15rem; font-weight:700;
    color:var(--text);
    margin-bottom: .8rem;
    display:flex; align-items:center; gap:.5rem;
}
.sec-title::after {
    content:''; flex:1; height:1px;
    background:linear-gradient(90deg,var(--border),transparent);
    margin-left:.4rem;
}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  SESSION STATE INITIALIZATION
# ─────────────────────────────────────────────
def init_state():
    defaults = {
        "consumer_points": 340,
        "validated_offers": 7,
        "search_log": {},          # {item: count}
        "flash_offers": [],
        "lojista_store": "Condor",
        "offer_posted": False,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()

MERCADOS = ["Condor", "Muffato", "Angeloni", "Festival", "Atacadão", "Max Atacadista"]
ITENS_CESTA = ["Arroz 5kg", "Feijão 1kg", "Óleo 900ml", "Leite 1L", "Açúcar 1kg", "Café 500g"]

MARCAS = {
    "Arroz 5kg":  ["Tio João", "Camil", "Kika"],
    "Feijão 1kg": ["Camil", "Coqueiro", "Jurere"],
    "Óleo 900ml": ["Liza", "Soya", "Salada"],
    "Leite 1L":   ["Tirol", "Parmalat", "Batavo"],
    "Açúcar 1kg": ["União", "Guarani", "Caravelas"],
    "Café 500g":  ["Pilão", "3 Corações", "Melitta"],
}

# ─────────────────────────────────────────────
#  MOCK DATA GENERATION (simula scraping diário)
# ─────────────────────────────────────────────
@st.cache_data(ttl=300)
def gerar_precos_mock():
    """
    Simula dados coletados via scraping (BeautifulSoup / Selenium).
    Em produção, substituir pelo scraper real de cada site.
    """
    random.seed(42)
    base_prices = {
        "Arroz 5kg":  {"Condor":22.9,"Muffato":21.5,"Angeloni":24.9,"Festival":23.4,"Atacadão":19.9,"Max Atacadista":20.5},
        "Feijão 1kg": {"Condor":8.9,"Muffato":8.5,"Angeloni":9.9,"Festival":8.7,"Atacadão":7.2,"Max Atacadista":7.5},
        "Óleo 900ml": {"Condor":7.9,"Muffato":7.5,"Angeloni":8.9,"Festival":7.8,"Atacadão":6.9,"Max Atacadista":7.1},
        "Leite 1L":   {"Condor":4.9,"Muffato":4.7,"Angeloni":5.4,"Festival":4.8,"Atacadão":4.2,"Max Atacadista":4.3},
        "Açúcar 1kg": {"Condor":3.9,"Muffato":3.7,"Angeloni":4.2,"Festival":3.8,"Atacadão":3.2,"Max Atacadista":3.4},
        "Café 500g":  {"Condor":18.9,"Muffato":17.9,"Angeloni":21.5,"Festival":19.2,"Atacadão":15.9,"Max Atacadista":16.5},
    }
    rows = []
    for item, prices in base_prices.items():
        for mercado, base in prices.items():
            variacao = random.uniform(-0.05, 0.05)
            preco = round(base * (1 + variacao), 2)
            rows.append({
                "item": item,
                "mercado": mercado,
                "preco": preco,
                "em_oferta": random.random() < 0.2,
                "estoque": random.choice(["Alto","Médio","Baixo"]),
                "ultima_atualizacao": datetime.now().strftime("%d/%m %H:%M"),
            })
    return pd.DataFrame(rows)

@st.cache_data(ttl=60)
def gerar_flash_offers():
    offers = [
        {"produto":"Arroz 5kg Tio João","mercado":"Condor","preco_de":22.90,"preco_por":17.90,
         "validade":"Hoje até 22h","score":94,"usuario":"Fernanda R.","validacoes":23},
        {"produto":"Café Pilão 500g","mercado":"Muffato","preco_de":18.90,"preco_por":13.99,
         "validade":"Amanhã","score":87,"usuario":"Lojista Oficial","validacoes":41},
        {"produto":"Leite Tirol 6un","mercado":"Atacadão","preco_de":29.40,"preco_por":22.90,
         "validade":"Fim de semana","score":91,"usuario":"Carlos M.","validacoes":17},
        {"produto":"Óleo Liza 900ml","mercado":"Festival","preco_de":7.90,"preco_por":5.99,
         "validade":"Hoje até 20h","score":78,"usuario":"Ana P.","validacoes":9},
    ]
    return offers

@st.cache_data(ttl=120)
def gerar_tendencia_bairro():
    items = ITENS_CESTA
    dias = [(datetime.now() - timedelta(days=i)).strftime("%d/%m") for i in range(6, -1, -1)]
    rows = []
    random.seed(7)
    for item in items:
        base = random.randint(30, 120)
        for d in dias:
            rows.append({"item":item,"dia":d,"buscas":max(5, base + random.randint(-15,20))})
    return pd.DataFrame(rows)

@st.cache_data(ttl=120)
def gerar_giro_marcas(item="Café 500g"):
    marcas = MARCAS.get(item, ["A","B","C"])
    random.seed(99)
    data = []
    for m in marcas:
        data.append({"marca":m,"buscas":random.randint(40,200),"conversoes":random.randint(10,80)})
    return pd.DataFrame(data)

@st.cache_data(ttl=120)
def gerar_historico_precos(mercado="Condor", item="Café 500g"):
    dias = [(datetime.now()-timedelta(days=i)).strftime("%d/%m") for i in range(29,-1,-1)]
    random.seed(hash(mercado+item)%100)
    base = 18.0
    data = []
    for d in dias:
        base += random.uniform(-0.5, 0.5)
        data.append({"dia":d,"preco":round(base,2)})
    return pd.DataFrame(data)

# ─────────────────────────────────────────────
#  PLACEHOLDER DE SCRAPING (estrutura real)
# ─────────────────────────────────────────────
def scraper_placeholder(mercado: str, item: str) -> dict | None:
    """
    SCRAPER PLACEHOLDER — estrutura pronta para produção.
    Substituir o bloco 'return mock' pela lógica real de cada site.

    Para ativar:
      pip install requests beautifulsoup4 selenium playwright
      playwright install chromium

    Cada mercado tem seu próprio seletor CSS:
    """
    SCRAPER_CONFIG = {
        "Condor":          {"url": "https://www.condor.com.br/busca?q={item}", "css_price": ".price-value"},
        "Muffato":         {"url": "https://www.muffato.com.br/search?term={item}", "css_price": ".price"},
        "Angeloni":        {"url": "https://www.angeloni.com.br/super/busca?q={item}", "css_price": ".product-price"},
        "Festival":        {"url": "https://www.superfestival.com.br/?busca={item}", "css_price": ".preco"},
        "Atacadão":        {"url": "https://www.atacadao.com.br/search?q={item}", "css_price": ".valornormal"},
        "Max Atacadista":  {"url": "https://www.maxatacadista.com.br/busca/{item}", "css_price": ".ProductPrice"},
    }
    # ── PRODUCTION CODE (uncomment to activate) ──────────────────────────
    # import requests
    # from bs4 import BeautifulSoup
    # cfg = SCRAPER_CONFIG.get(mercado)
    # if not cfg: return None
    # url = cfg["url"].format(item=item.replace(" ", "+"))
    # headers = {"User-Agent": "Mozilla/5.0 (compatible; 4SAVR-bot/1.0)"}
    # try:
    #     r = requests.get(url, headers=headers, timeout=10)
    #     soup = BeautifulSoup(r.text, "html.parser")
    #     el = soup.select_one(cfg["css_price"])
    #     price_raw = el.text.strip() if el else None
    #     price = float(price_raw.replace("R$","").replace(",",".").strip()) if price_raw else None
    #     return {"mercado": mercado, "item": item, "preco": price, "url": url}
    # except Exception as e:
    #     return {"mercado": mercado, "item": item, "preco": None, "erro": str(e)}
    # ─────────────────────────────────────────────────────────────────────
    return None   # usa mock em demo

# ─────────────────────────────────────────────
#  HELPERS DE UI
# ─────────────────────────────────────────────
def fmt_brl(v): return f"R$ {v:.2f}".replace(".",",")

def render_rank_list(df_item):
    df_sorted = df_item.sort_values("preco").reset_index(drop=True)
    html = ""
    for i, row in df_sorted.iterrows():
        rank = i + 1
        badge_cls = {1:"rank-1",2:"rank-2",3:"rank-3"}.get(rank,"rank-other")
        badge_txt = {1:"🥇",2:"🥈",3:"🥉"}.get(rank, str(rank))
        best_tag = '<span class="rank-best">✓ Melhor</span>' if rank == 1 else ""
        oferta = ' <span style="color:#FFB547;font-size:.75rem">⚡ Oferta</span>' if row.em_oferta else ""
        html += f"""
        <div class="rank-item">
            <div class="rank-badge {badge_cls}">{badge_txt}</div>
            <div class="rank-name">{row.mercado}{oferta}</div>
            <div class="rank-price">{fmt_brl(row.preco)}{best_tag}</div>
        </div>"""
    st.markdown(html, unsafe_allow_html=True)

def plotly_dark_layout(fig, height=360, showlegend=True):
    fig.update_layout(
        height=height,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(13,27,42,0.6)",
        font=dict(family="Inter", color="#7A9ABF", size=12),
        legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color="#E8EFF7")) if showlegend else dict(visible=False),
        margin=dict(l=10,r=10,t=30,b=10),
        xaxis=dict(gridcolor="rgba(255,255,255,.05)", linecolor="rgba(255,255,255,.08)"),
        yaxis=dict(gridcolor="rgba(255,255,255,.05)", linecolor="rgba(255,255,255,.08)"),
    )
    return fig


# ─────────────────────────────────────────────
#  HERO HEADER
# ─────────────────────────────────────────────
st.markdown("""
<div class="hero">
  <span class="hero-badge">🛒 MVP · Beta</span>
  <div class="hero-title">4SAVR</div>
  <div class="hero-sub">Inteligência de Varejo Alimentar · Cesta Básica em Curitiba & Região</div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  TABS PRINCIPAIS
# ─────────────────────────────────────────────
tab_consumer, tab_lojista = st.tabs(["🛍️  Consumidor", "📊  Lojista / BI"])

df_all = gerar_precos_mock()

# ══════════════════════════════════════════════
#  TAB 1 — CONSUMIDOR
# ══════════════════════════════════════════════
with tab_consumer:

    # ── POINTS BANNER ──────────────────────────
    pts = st.session_state.consumer_points
    val = st.session_state.validated_offers
    st.markdown(f"""
    <div class="points-banner">
        <div>
            <div class="points-val">⭐ {pts}</div>
            <div style="color:#7A9ABF;font-size:.82rem">Seus pontos acumulados</div>
        </div>
        <div style="width:1px;height:48px;background:rgba(255,181,71,.2)"></div>
        <div>
            <div style="font-family:'Syne',sans-serif;font-size:1.4rem;font-weight:700;color:#FFB547">{val}</div>
            <div style="color:#7A9ABF;font-size:.82rem">Ofertas validadas</div>
        </div>
        <div style="flex:1;padding-left:1rem;color:#7A9ABF;font-size:.9rem">
            🏆 Você ajudou <b style="color:#FFB547">{val * 3} vizinhos</b> esta semana!
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    col_left, col_right = st.columns([3, 2], gap="large")

    # ── LEFT COLUMN ─────────────────────────────
    with col_left:

        # ── 1. CONSULTA DE PREÇOS ──────────────
        st.markdown('<div class="sec-title">🔍 Comparar Preços por Item</div>', unsafe_allow_html=True)

        with st.container():
            c1, c2 = st.columns([2, 1])
            with c1:
                item_sel = st.selectbox("Produto", ITENS_CESTA, label_visibility="collapsed")
            with c2:
                buscar = st.button("Buscar Preços", use_container_width=True)

            if buscar or item_sel:
                # registra busca no log (para BI do lojista)
                st.session_state.search_log[item_sel] = st.session_state.search_log.get(item_sel, 0) + 1

                df_item = df_all[df_all.item == item_sel].copy()

                with st.spinner("Atualizando preços..."):
                    time.sleep(0.3)

                render_rank_list(df_item)

                # mini stats
                m1, m2, m3 = st.columns(3)
                min_p = df_item.preco.min()
                max_p = df_item.preco.max()
                eco = max_p - min_p
                m1.markdown(f'<div class="metric-box"><div class="metric-val">{fmt_brl(min_p)}</div><div class="metric-lbl">Menor preço</div></div>', unsafe_allow_html=True)
                m2.markdown(f'<div class="metric-box"><div class="metric-val">{fmt_brl(max_p)}</div><div class="metric-lbl">Maior preço</div></div>', unsafe_allow_html=True)
                m3.markdown(f'<div class="metric-box"><div class="metric-val">{fmt_brl(eco)}</div><div class="metric-lbl">Você economiza</div></div>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # ── 2. MELHOR CESTA COMPLETA ───────────
        st.markdown('<div class="sec-title">🧺 Menor Preço da Cesta Completa</div>', unsafe_allow_html=True)

        if st.button("🧮 Calcular Melhor Mercado para a Cesta", use_container_width=True):
            with st.spinner("Calculando..."):
                time.sleep(0.5)
            totais = df_all.groupby("mercado")["preco"].sum().reset_index()
            totais.columns = ["mercado","total_cesta"]
            totais = totais.sort_values("total_cesta").reset_index(drop=True)
            vencedor = totais.iloc[0]
            segundo  = totais.iloc[1]
            economia = round(segundo.total_cesta - vencedor.total_cesta, 2)

            st.markdown(f"""
            <div class="card" style="border-color:var(--emerald);border-width:2px">
                <div style="font-size:.82rem;color:var(--muted);margin-bottom:.3rem">🏆 MELHOR MERCADO PARA CESTA COMPLETA</div>
                <div style="font-family:'Syne',sans-serif;font-size:2rem;font-weight:800;color:var(--emerald)">{vencedor.mercado}</div>
                <div style="font-size:1.5rem;font-weight:700;color:#fff;margin:.2rem 0">{fmt_brl(vencedor.total_cesta)}</div>
                <div style="color:var(--gold);font-size:.92rem">💰 Você economiza <b>{fmt_brl(economia)}</b> vs. {segundo.mercado}</div>
            </div>
            """, unsafe_allow_html=True)

            fig = px.bar(
                totais, x="mercado", y="total_cesta",
                color="total_cesta",
                color_continuous_scale=["#00C48C","#0B1E3F"],
                labels={"total_cesta":"Total (R$)","mercado":"Mercado"},
                title="Custo Total da Cesta Básica por Mercado"
            )
            fig = plotly_dark_layout(fig, showlegend=False)
            fig.update_coloraxes(showscale=False)
            fig.update_traces(text=[fmt_brl(v) for v in totais.total_cesta], textposition="outside",
                              marker_line_width=0)
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar":False})

        st.markdown("<br>", unsafe_allow_html=True)

        # ── 3. VALIDAÇÃO DE OFERTA ─────────────
        st.markdown('<div class="sec-title">📸 Validar Oferta (Upload / Foto)</div>', unsafe_allow_html=True)

        with st.container():
            c1, c2 = st.columns(2)
            with c1:
                mercado_val = st.selectbox("Mercado", MERCADOS, key="val_mercado")
                item_val    = st.selectbox("Produto", ITENS_CESTA, key="val_item")
                preco_val   = st.number_input("Preço visto (R$)", min_value=0.01, value=15.99, step=0.01, key="val_preco")
            with c2:
                foto_val = st.file_uploader("📷 Foto ou Nota Fiscal (opcional)", type=["jpg","jpeg","png","pdf"], key="foto_upload")
                st.markdown('<div style="color:var(--muted);font-size:.82rem;margin-top:.3rem">Opcional — aumenta o Score de Confiança</div>', unsafe_allow_html=True)

            if st.button("✅ Enviar Validação", use_container_width=True, key="btn_validar"):
                with st.spinner("Verificando localização e timestamp..."):
                    time.sleep(0.8)

                score_base = 65
                if foto_val: score_base += 20
                score_base += random.randint(0, 15)
                score = min(score, 99) if (score := score_base) > 99 else score_base

                st.session_state.consumer_points += 50
                st.session_state.validated_offers += 1

                st.markdown(f"""
                <div class="card" style="border-color:var(--emerald)">
                    <div style="font-size:.9rem;color:var(--emerald);font-weight:600;margin-bottom:.6rem">✅ Oferta validada com sucesso! +50 pontos</div>
                    <div style="display:flex;align-items:center;gap:.8rem">
                        <div style="font-family:'Syne',sans-serif;font-size:2.2rem;font-weight:800;color:{'#00C48C' if score>=80 else '#FFB547'}">{score}%</div>
                        <div>
                            <div style="font-weight:500">{mercado_val} · {item_val} · {fmt_brl(preco_val)}</div>
                            <div style="color:var(--muted);font-size:.82rem">Score de Confiança (geo + timestamp + foto)</div>
                        </div>
                    </div>
                    <div class="score-bar-wrap"><div class="score-bar" style="width:{score}%"></div></div>
                </div>
                """, unsafe_allow_html=True)
                st.rerun()

    # ── RIGHT COLUMN ────────────────────────────
    with col_right:

        # ── FEED DE OFERTAS RELÂMPAGO ──────────
        st.markdown('<div class="sec-title">⚡ Ofertas Relâmpago</div>', unsafe_allow_html=True)

        offers = gerar_flash_offers()
        for o in offers:
            desc = round((1 - o["preco_por"]/o["preco_de"])*100)
            st.markdown(f"""
            <div class="offer-card">
                <span class="offer-badge">⚡ -{desc}% OFF</span>
                <div style="font-weight:600;margin:.4rem 0 .1rem">{o['produto']}</div>
                <div style="color:var(--muted);font-size:.85rem">{o['mercado']}</div>
                <div style="display:flex;align-items:baseline;gap:.5rem;margin:.35rem 0">
                    <span style="text-decoration:line-through;color:var(--muted);font-size:.9rem">{fmt_brl(o['preco_de'])}</span>
                    <span style="font-family:'Syne',sans-serif;font-size:1.3rem;font-weight:700;color:var(--emerald)">{fmt_brl(o['preco_por'])}</span>
                </div>
                <div style="display:flex;justify-content:space-between;font-size:.78rem;color:var(--muted)">
                    <span>🕐 {o['validade']}</span>
                    <span>👍 {o['validacoes']} confirmaram</span>
                </div>
                <div style="font-size:.78rem;color:var(--muted);margin-top:.3rem">por {o['usuario']}</div>
                <div class="score-bar-wrap" style="margin-top:.5rem"><div class="score-bar" style="width:{o['score']}%"></div></div>
                <div style="font-size:.75rem;color:var(--muted);text-align:right;margin-top:.2rem">Score {o['score']}%</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # ── TENDÊNCIA DE BUSCAS ────────────────
        st.markdown('<div class="sec-title">📈 Mais Buscados Hoje</div>', unsafe_allow_html=True)

        busca_counts = {i: st.session_state.search_log.get(i, random.randint(20,120)) for i in ITENS_CESTA}
        df_bc = pd.DataFrame(list(busca_counts.items()), columns=["item","buscas"]).sort_values("buscas", ascending=True)

        fig_bc = px.bar(df_bc, x="buscas", y="item", orientation="h",
                        color_discrete_sequence=["#00C48C"])
        fig_bc = plotly_dark_layout(fig_bc, height=280, showlegend=False)
        fig_bc.update_traces(marker_line_width=0)
        st.plotly_chart(fig_bc, use_container_width=True, config={"displayModeBar":False})


# ══════════════════════════════════════════════
#  TAB 2 — LOJISTA / BI
# ══════════════════════════════════════════════
with tab_lojista:

    # ── STORE SELECTOR ────────────────────────
    col_store, col_space = st.columns([2, 5])
    with col_store:
        st.session_state.lojista_store = st.selectbox(
            "Sua loja:", MERCADOS, index=MERCADOS.index(st.session_state.lojista_store)
        )

    loja = st.session_state.lojista_store
    st.markdown("<br>", unsafe_allow_html=True)

    # ── KPI ROW ───────────────────────────────
    k1, k2, k3, k4 = st.columns(4)
    kpis = [
        ("📦", "127", "Produtos monitorados"),
        ("⚡", "3",   "Alertas ativos"),
        ("👁️",  "842", "Visualizações hoje"),
        ("💰", "R$ 1.247", "Economia gerada/dia"),
    ]
    for col, (icon, val, lbl) in zip([k1,k2,k3,k4], kpis):
        col.markdown(f"""
        <div class="metric-box">
            <div style="font-size:1.6rem">{icon}</div>
            <div class="metric-val" style="font-size:1.6rem">{val}</div>
            <div class="metric-lbl">{lbl}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    col_bi1, col_bi2 = st.columns(2, gap="large")

    # ── BI LEFT ──────────────────────────────
    with col_bi1:

        # ── PAINEL COMPETITIVO ────────────────
        st.markdown('<div class="sec-title">🏁 Painel Competitivo de Preços</div>', unsafe_allow_html=True)

        item_comp = st.selectbox("Produto para comparar:", ITENS_CESTA, key="comp_item")
        df_comp   = df_all[df_all.item == item_comp].copy()
        df_comp["minha_loja"] = df_comp.mercado == loja

        colors = [("#00C48C" if r else "#264D73") for r in df_comp.minha_loja]
        fig_comp = go.Figure(go.Bar(
            x=df_comp.mercado,
            y=df_comp.preco,
            marker_color=colors,
            text=[fmt_brl(v) for v in df_comp.preco],
            textposition="outside",
        ))
        fig_comp = plotly_dark_layout(fig_comp, height=320, showlegend=False)
        fig_comp.update_layout(title=f"Preço de {item_comp} — verde = {loja}")
        fig_comp.update_traces(marker_line_width=0)
        st.plotly_chart(fig_comp, use_container_width=True, config={"displayModeBar":False})

        meu_preco  = df_comp[df_comp.mercado == loja].preco.values[0]
        min_preco  = df_comp.preco.min()
        rival_min  = df_comp[df_comp.mercado != loja].preco.min()
        rival_nome = df_comp[df_comp.preco == rival_min].mercado.values[0]

        if meu_preco <= min_preco:
            st.markdown(f'<div class="alert-ok">✅ <b>{loja}</b> tem o <b>menor preço</b> do mercado para {item_comp}! Ótima posição.</div>', unsafe_allow_html=True)
        else:
            diff = round(meu_preco - rival_min, 2)
            st.markdown(f'<div class="alert-warn">⚠️ <b>{rival_nome}</b> está {fmt_brl(diff)} mais barato em <b>{item_comp}</b>. Considere ajustar o preço.</div>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # ── HISTÓRICO DE PREÇOS ───────────────
        st.markdown('<div class="sec-title">📉 Histórico de Preços (30 dias)</div>', unsafe_allow_html=True)

        df_hist = gerar_historico_precos(loja, item_comp)
        fig_hist = px.area(df_hist, x="dia", y="preco", line_shape="spline",
                           color_discrete_sequence=["#00C48C"])
        fig_hist.update_traces(fill="tozeroy", fillcolor="rgba(0,196,140,.12)", line=dict(width=2))
        fig_hist = plotly_dark_layout(fig_hist, height=240, showlegend=False)
        fig_hist.update_layout(xaxis=dict(tickangle=-45, nticks=10))
        st.plotly_chart(fig_hist, use_container_width=True, config={"displayModeBar":False})

    # ── BI RIGHT ─────────────────────────────
    with col_bi2:

        # ── GIRO DE MARCAS ────────────────────
        st.markdown('<div class="sec-title">📊 Giro de Marcas (Demanda no App)</div>', unsafe_allow_html=True)

        item_marca = st.selectbox("Produto:", ITENS_CESTA, key="marca_item")
        df_marcas  = gerar_giro_marcas(item_marca)

        fig_marcas = go.Figure()
        fig_marcas.add_trace(go.Bar(name="Buscas", x=df_marcas.marca, y=df_marcas.buscas,
                                     marker_color="#264D73"))
        fig_marcas.add_trace(go.Bar(name="Compras", x=df_marcas.marca, y=df_marcas.conversoes,
                                     marker_color="#00C48C"))
        fig_marcas.update_layout(barmode="group")
        fig_marcas = plotly_dark_layout(fig_marcas, height=280)
        fig_marcas.update_traces(marker_line_width=0)
        st.plotly_chart(fig_marcas, use_container_width=True, config={"displayModeBar":False})

        st.markdown("<br>", unsafe_allow_html=True)

        # ── ALERTAS DE PERDA / VALIDADE ───────
        st.markdown('<div class="sec-title">🚨 Gestão de Perdas & Validade</div>', unsafe_allow_html=True)

        alertas = [
            {"produto":"Leite Tirol 1L","estoque":"Baixa saída","dias":3,"severidade":"alta"},
            {"produto":"Pão de Forma Wickbold","estoque":"Crítico","dias":1,"severidade":"critica"},
            {"produto":"Iogurte Natural Batavo","estoque":"Moderado","dias":5,"severidade":"media"},
        ]

        for a in alertas:
            border = {"alta":"rgba(255,82,82,.4)","critica":"rgba(255,82,82,.7)","media":"rgba(255,181,71,.4)"}[a["severidade"]]
            icon   = {"alta":"⚠️","critica":"🔴","media":"🟡"}[a["severidade"]]
            action = f'<span style="color:var(--emerald);cursor:pointer;font-size:.8rem">→ Lançar Promoção Relâmpago</span>'
            st.markdown(f"""
            <div class="card-sm" style="border-color:{border}">
                <div style="display:flex;justify-content:space-between;align-items:center">
                    <div>
                        <span style="font-weight:600">{icon} {a['produto']}</span>
                        <div style="color:var(--muted);font-size:.8rem">{a['estoque']} · vence em {a['dias']} dia(s)</div>
                    </div>
                    {action}
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # ── LANÇAR OFERTA RELÂMPAGO ───────────
        st.markdown('<div class="sec-title">⚡ Lançar Oferta Relâmpago</div>', unsafe_allow_html=True)

        with st.container():
            o_produto  = st.selectbox("Produto:", ITENS_CESTA, key="o_prod")
            o_de, o_por = st.columns(2)
            with o_de:
                o_preco_de  = st.number_input("Preço De (R$)", min_value=0.01, value=18.90, key="o_de")
            with o_por:
                o_preco_por = st.number_input("Preço Por (R$)", min_value=0.01, value=14.90, key="o_por")
            o_validade  = st.selectbox("Validade:", ["Hoje até 22h","Amanhã","Fim de semana","3 dias"], key="o_val")
            o_descricao = st.text_area("Mensagem (opcional):", placeholder="Ex: Estoque limitado! Últimas unidades.", key="o_desc", height=68)

            if st.button("📢 Publicar Oferta Agora", use_container_width=True, key="btn_oferta"):
                desc_pct = round((1 - o_preco_por/o_preco_de)*100)
                st.markdown(f"""
                <div class="card" style="border-color:var(--emerald)">
                    <div style="color:var(--emerald);font-weight:700;margin-bottom:.4rem">✅ Oferta publicada com sucesso!</div>
                    <div style="color:var(--muted);font-size:.85rem">
                        {o_produto} · {loja} · <b style="color:var(--gold)">-{desc_pct}%</b><br>
                        {fmt_brl(o_preco_de)} → <b style="color:var(--emerald)">{fmt_brl(o_preco_por)}</b><br>
                        Válida: {o_validade}
                    </div>
                    <div style="margin-top:.5rem;font-size:.8rem;color:var(--muted)">
                        📱 Notificação enviada a todos os consumidores do bairro.
                    </div>
                </div>
                """, unsafe_allow_html=True)
                st.session_state.offer_posted = True

    st.markdown("<br>", unsafe_allow_html=True)

    # ── TENDÊNCIA DE BUSCAS (FULL WIDTH) ─────
    st.markdown('<div class="sec-title">📡 Tendência de Buscas no Bairro (últimos 7 dias)</div>', unsafe_allow_html=True)

    df_tend = gerar_tendencia_bairro()
    fig_tend = px.line(df_tend, x="dia", y="buscas", color="item",
                       line_shape="spline", markers=True,
                       color_discrete_sequence=px.colors.qualitative.Set2)
    fig_tend = plotly_dark_layout(fig_tend, height=320)
    fig_tend.update_traces(line=dict(width=2.5))
    st.plotly_chart(fig_tend, use_container_width=True, config={"displayModeBar":False})

# ─────────────────────────────────────────────
#  FOOTER
# ─────────────────────────────────────────────
st.markdown("""
<hr>
<div style="text-align:center;color:#3A5A7A;font-size:.8rem;padding:.8rem 0">
    4SAVR · MVP Beta · Dados simulados para demonstração · 
    <span style="color:#00C48C">Scraper estruturado pronto para ativação em produção</span>
</div>
""", unsafe_allow_html=True)
