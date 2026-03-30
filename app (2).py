import streamlit as st
import pandas as pd
import time
import random
from datetime import datetime, timedelta

# ─────────────────────────────────────────────
#  PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="4SAVR – Inteligência de Preços do Bairro",
    page_icon="💚",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
#  CUSTOM CSS – Navy + Emerald, Executive Style
# ─────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Sora:wght@300;400;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap');

  /* ── Base ── */
  html, body, [class*="css"] { font-family: 'Sora', sans-serif; }

  .stApp {
    background: linear-gradient(160deg, #020f1f 0%, #031a30 60%, #042440 100%);
    color: #e8f4f8;
  }

  /* ── Sidebar ── */
  [data-testid="stSidebar"] {
    background: linear-gradient(180deg, #010d1c 0%, #021525 100%);
    border-right: 1px solid #0d3a5c;
  }
  [data-testid="stSidebar"] * { color: #c8e6f5 !important; }
  [data-testid="stSidebar"] .stRadio label {
    background: rgba(13,58,92,0.3);
    border: 1px solid #0d3a5c;
    border-radius: 10px;
    padding: 10px 16px;
    margin-bottom: 6px;
    transition: all 0.2s;
    cursor: pointer;
    display: block;
  }
  [data-testid="stSidebar"] .stRadio label:hover {
    background: rgba(0,200,130,0.15);
    border-color: #00c882;
  }

  /* ── Headers ── */
  h1, h2, h3 { font-family: 'Sora', sans-serif !important; }

  /* ── Hero Banner ── */
  .hero-banner {
    background: linear-gradient(135deg, #00c882 0%, #00a86b 40%, #007a50 100%);
    border-radius: 16px;
    padding: 28px 36px;
    margin-bottom: 24px;
    position: relative;
    overflow: hidden;
    box-shadow: 0 8px 32px rgba(0,200,130,0.25);
  }
  .hero-banner::before {
    content: '';
    position: absolute;
    top: -40px; right: -40px;
    width: 180px; height: 180px;
    border-radius: 50%;
    background: rgba(255,255,255,0.08);
  }
  .hero-banner::after {
    content: '';
    position: absolute;
    bottom: -60px; right: 80px;
    width: 240px; height: 240px;
    border-radius: 50%;
    background: rgba(255,255,255,0.05);
  }
  .hero-banner h1 {
    color: #ffffff !important;
    font-size: 2rem !important;
    font-weight: 800 !important;
    margin: 0 0 6px 0 !important;
    text-shadow: 0 2px 8px rgba(0,0,0,0.2);
  }
  .hero-banner p {
    color: rgba(255,255,255,0.9) !important;
    font-size: 1.05rem;
    margin: 0;
    font-weight: 300;
  }
  .hero-tag {
    display: inline-block;
    background: rgba(255,255,255,0.2);
    color: #fff !important;
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    padding: 4px 12px;
    border-radius: 20px;
    margin-bottom: 12px;
  }

  /* ── Metric Cards ── */
  .metric-card {
    background: linear-gradient(145deg, rgba(13,58,92,0.6) 0%, rgba(4,36,64,0.8) 100%);
    border: 1px solid rgba(0,200,130,0.2);
    border-radius: 14px;
    padding: 20px 22px;
    text-align: center;
    transition: transform 0.2s, box-shadow 0.2s;
    backdrop-filter: blur(8px);
  }
  .metric-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 12px 28px rgba(0,200,130,0.15);
    border-color: rgba(0,200,130,0.5);
  }
  .metric-card .value {
    font-size: 2rem;
    font-weight: 800;
    color: #00c882;
    line-height: 1;
    font-family: 'JetBrains Mono', monospace;
  }
  .metric-card .label {
    font-size: 0.78rem;
    color: #7fb8d4;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-top: 6px;
  }

  /* ── Section Title ── */
  .section-title {
    font-size: 1.1rem;
    font-weight: 700;
    color: #00c882;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin: 28px 0 14px 0;
    padding-bottom: 8px;
    border-bottom: 1px solid rgba(0,200,130,0.25);
  }

  /* ── Price Table ── */
  .price-table-wrapper { margin: 12px 0; }
  .price-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    background: rgba(13,58,92,0.4);
    border: 1px solid rgba(13,58,92,0.8);
    border-radius: 10px;
    padding: 14px 20px;
    margin-bottom: 8px;
    transition: all 0.2s;
  }
  .price-row:hover { border-color: rgba(0,200,130,0.4); background: rgba(0,200,130,0.07); }
  .price-row.best { border-color: #00c882; background: rgba(0,200,130,0.12); }
  .price-row .market-name { font-weight: 600; font-size: 0.95rem; color: #e8f4f8; }
  .price-row .market-dist { font-size: 0.78rem; color: #7fb8d4; margin-top: 2px; }
  .price-row .price-val { font-family: 'JetBrains Mono', monospace; font-size: 1.25rem; font-weight: 700; }
  .price-row.best .price-val { color: #00c882; }
  .price-row .badge-best {
    background: #00c882; color: #010d1c;
    font-size: 0.65rem; font-weight: 700;
    padding: 3px 8px; border-radius: 20px;
    text-transform: uppercase; letter-spacing: 0.08em;
  }
  .price-row .badge-update { font-size: 0.7rem; color: #5a9ab8; }

  /* ── Alert Card ── */
  .alert-card {
    background: linear-gradient(135deg, rgba(220,38,38,0.15) 0%, rgba(153,27,27,0.2) 100%);
    border: 1px solid rgba(220,38,38,0.5);
    border-left: 4px solid #dc2626;
    border-radius: 12px;
    padding: 18px 22px;
    margin: 12px 0;
  }
  .alert-card .alert-title {
    color: #fca5a5;
    font-weight: 700;
    font-size: 0.85rem;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin-bottom: 8px;
  }
  .alert-card .alert-body { color: #fecaca; font-size: 0.95rem; line-height: 1.6; }
  .alert-card .alert-impact { color: #f87171; font-weight: 700; font-size: 1.1rem; margin-top: 8px; }

  /* ── Success Card ── */
  .success-card {
    background: linear-gradient(135deg, rgba(0,200,130,0.15) 0%, rgba(0,120,80,0.2) 100%);
    border: 1px solid rgba(0,200,130,0.5);
    border-left: 4px solid #00c882;
    border-radius: 12px;
    padding: 18px 22px;
    margin: 12px 0;
  }
  .success-card .s-title { color: #6ee7b7; font-weight: 700; font-size: 1rem; margin-bottom: 6px; }
  .success-card .s-body { color: #a7f3d0; font-size: 0.9rem; line-height: 1.5; }

  /* ── Info Card ── */
  .info-card {
    background: rgba(13,58,92,0.5);
    border: 1px solid rgba(0,200,130,0.2);
    border-radius: 12px;
    padding: 16px 20px;
    margin: 8px 0;
  }
  .info-card .i-title { color: #7fb8d4; font-size: 0.78rem; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 4px; }
  .info-card .i-body  { color: #e8f4f8; font-size: 0.95rem; font-weight: 500; }

  /* ── Optimizer Box ── */
  .optimizer-box {
    background: linear-gradient(135deg, rgba(0,200,130,0.1) 0%, rgba(4,36,64,0.8) 100%);
    border: 1px solid rgba(0,200,130,0.35);
    border-radius: 14px;
    padding: 22px 24px;
    margin: 14px 0;
  }
  .optimizer-box .opt-title { color: #00c882; font-weight: 700; font-size: 1rem; margin-bottom: 12px; }
  .optimizer-box .opt-row { display: flex; justify-content: space-between; align-items: center; margin: 8px 0; }
  .optimizer-box .opt-label { color: #7fb8d4; font-size: 0.85rem; }
  .optimizer-box .opt-val { font-family: 'JetBrains Mono', monospace; font-weight: 700; font-size: 1.05rem; color: #e8f4f8; }
  .optimizer-box .opt-savings { color: #00c882; font-size: 1.5rem; font-weight: 800; font-family: 'JetBrains Mono', monospace; }

  /* ── Ranking Card ── */
  .rank-card {
    display: flex; align-items: center; gap: 14px;
    background: rgba(13,58,92,0.4);
    border: 1px solid rgba(13,58,92,0.8);
    border-radius: 10px;
    padding: 12px 18px;
    margin-bottom: 8px;
    transition: all 0.2s;
  }
  .rank-card:hover { border-color: rgba(0,200,130,0.3); }
  .rank-card .rank-pos { font-family: 'JetBrains Mono', monospace; font-size: 1.1rem; font-weight: 700; color: #00c882; width: 28px; }
  .rank-card .rank-name { font-weight: 600; color: #e8f4f8; flex: 1; }
  .rank-card .rank-pts { font-family: 'JetBrains Mono', monospace; font-size: 0.85rem; color: #7fb8d4; }
  .rank-card .rank-badge { font-size: 1.2rem; }

  /* ── Ad Preview ── */
  .ad-preview {
    background: linear-gradient(135deg, #021525, #031a30);
    border: 2px solid #00c882;
    border-radius: 14px;
    padding: 20px 24px;
    margin: 12px 0;
    position: relative;
    box-shadow: 0 0 24px rgba(0,200,130,0.15);
  }
  .ad-preview .ad-label {
    position: absolute; top: -10px; left: 20px;
    background: #00c882; color: #010d1c;
    font-size: 0.65rem; font-weight: 700;
    padding: 2px 10px; border-radius: 20px;
    text-transform: uppercase; letter-spacing: 0.1em;
  }
  .ad-preview .ad-store { font-size: 1rem; font-weight: 700; color: #00c882; margin-bottom: 4px; }
  .ad-preview .ad-product { font-size: 1.3rem; font-weight: 800; color: #ffffff; margin-bottom: 4px; }
  .ad-preview .ad-price { font-family: 'JetBrains Mono', monospace; font-size: 2rem; font-weight: 800; color: #00c882; }
  .ad-preview .ad-validity { font-size: 0.75rem; color: #7fb8d4; margin-top: 6px; }
  .ad-preview .ad-reach { font-size: 0.8rem; color: #a7f3d0; margin-top: 8px; font-weight: 500; }

  /* ── Stbutton overrides ── */
  .stButton > button {
    background: linear-gradient(135deg, #00c882, #00a86b) !important;
    color: #010d1c !important;
    font-weight: 700 !important;
    font-family: 'Sora', sans-serif !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 10px 22px !important;
    transition: all 0.2s !important;
    box-shadow: 0 4px 16px rgba(0,200,130,0.3) !important;
  }
  .stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 24px rgba(0,200,130,0.45) !important;
  }

  /* ── Selectbox / Multiselect ── */
  .stSelectbox > div > div, .stMultiSelect > div > div {
    background: rgba(13,58,92,0.5) !important;
    border: 1px solid rgba(0,200,130,0.3) !important;
    border-radius: 10px !important;
    color: #e8f4f8 !important;
  }

  /* ── Divider ── */
  hr { border-color: rgba(13,58,92,0.8) !important; }

  /* ── Spinner ── */
  .stSpinner { color: #00c882 !important; }

  /* ── Footer ── */
  .footer-bar {
    text-align: center;
    padding: 20px;
    color: #2a5a7a;
    font-size: 0.75rem;
    margin-top: 40px;
    border-top: 1px solid rgba(13,58,92,0.5);
  }
  .footer-bar span { color: #00c882; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  MOCK DATA
# ─────────────────────────────────────────────
MERCADOS = {
    "Mercado Boa Vista": {"dist": "0m (referência)", "lat": -25.43, "lon": -49.27},
    "Supermercado Central": {"dist": "180m", "lat": -25.432, "lon": -49.271},
    "Mini Box Econômico": {"dist": "300m", "lat": -25.434, "lon": -49.269},
    "Atacado do Bairro": {"dist": "520m", "lat": -25.435, "lon": -49.272},
    "Mercado Família": {"dist": "750m", "lat": -25.436, "lon": -49.268},
}

PRODUTOS_BASE = {
    "Leite Integral 1L":       {"emoji": "🥛", "categoria": "Laticínios",    "unidade": "1L"},
    "Arroz Branco 5kg":        {"emoji": "🌾", "categoria": "Grãos",         "unidade": "5kg"},
    "Feijão Carioca 1kg":      {"emoji": "🫘", "categoria": "Grãos",         "unidade": "1kg"},
    "Cerveja Lata 350ml":      {"emoji": "🍺", "categoria": "Bebidas",        "unidade": "lata"},
    "Café Torrado 500g":       {"emoji": "☕", "categoria": "Bebidas",        "unidade": "500g"},
    "Óleo de Soja 900ml":      {"emoji": "🫙", "categoria": "Condimentos",    "unidade": "900ml"},
    "Açúcar Cristal 1kg":      {"emoji": "🍬", "categoria": "Açúcar",         "unidade": "1kg"},
    "Pão de Forma 500g":       {"emoji": "🍞", "categoria": "Padaria",        "unidade": "500g"},
    "Macarrão Espaguete 500g": {"emoji": "🍝", "categoria": "Massas",         "unidade": "500g"},
    "Frango Congelado 1kg":    {"emoji": "🍗", "categoria": "Proteínas",      "unidade": "1kg"},
}

PRECOS_BASE = {
    "Leite Integral 1L":       [4.79, 4.99, 4.49, 4.29, 5.10],
    "Arroz Branco 5kg":        [22.90, 23.50, 21.80, 20.50, 24.00],
    "Feijão Carioca 1kg":      [8.99, 8.49, 9.20, 7.99, 9.50],
    "Cerveja Lata 350ml":      [3.89, 3.99, 3.79, 3.59, 4.10],
    "Café Torrado 500g":       [15.90, 16.50, 14.90, 14.20, 16.90],
    "Óleo de Soja 900ml":      [6.89, 7.10, 6.59, 6.29, 7.20],
    "Açúcar Cristal 1kg":      [3.49, 3.59, 3.39, 3.19, 3.70],
    "Pão de Forma 500g":       [7.49, 7.99, 7.29, 6.99, 8.10],
    "Macarrão Espaguete 500g": [4.29, 4.49, 4.09, 3.89, 4.59],
    "Frango Congelado 1kg":    [11.90, 12.50, 11.20, 10.80, 12.90],
}

TIMESTAMPS = [
    "Atualizado há 8 min",
    "Atualizado há 15 min",
    "Atualizado há 23 min",
    "Atualizado há 41 min",
    "Atualizado há 1h 02min",
]

def build_price_dataframe():
    """Build a tidy DataFrame with all product × market prices."""
    rows = []
    mercados_list = list(MERCADOS.keys())
    for produto, precos in PRECOS_BASE.items():
        for i, mercado in enumerate(mercados_list):
            rows.append({
                "Produto": produto,
                "Mercado": mercado,
                "Distância": MERCADOS[mercado]["dist"],
                "Preço (R$)": precos[i],
                "Timestamp": TIMESTAMPS[i],
                "Emoji": PRODUTOS_BASE[produto]["emoji"],
                "Categoria": PRODUTOS_BASE[produto]["categoria"],
            })
    return pd.DataFrame(rows)

def build_history_df(produto, mercado_ref="Mercado Boa Vista"):
    """Simulate 14-day price history for a product in 2 markets."""
    dias = [datetime.today() - timedelta(days=i) for i in range(13, -1, -1)]
    base = PRECOS_BASE[produto][0]
    media_bairro = sum(PRECOS_BASE[produto]) / len(PRECOS_BASE[produto])
    random.seed(42)
    preco_ref = [round(base + random.uniform(-0.3, 0.4), 2) for _ in dias]
    preco_med = [round(media_bairro + random.uniform(-0.15, 0.15), 2) for _ in dias]
    return pd.DataFrame({
        "Data": [d.strftime("%d/%m") for d in dias],
        mercado_ref: preco_ref,
        "Média do Bairro": preco_med,
    })

DF = build_price_dataframe()

EMBAIXADORES = [
    {"nome": "Ana Paula M.", "pts": 1_840, "badge": "🏆"},
    {"nome": "Ricardo S.",   "pts": 1_622, "badge": "🥈"},
    {"nome": "Fernanda L.",  "pts": 1_405, "badge": "🥉"},
    {"nome": "João Victor",  "pts": 1_298, "badge": "⭐"},
    {"nome": "Marcia T.",    "pts": 1_187, "badge": "⭐"},
]


# ─────────────────────────────────────────────
#  SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding: 16px 0 24px'>
      <div style='font-size:2.4rem; margin-bottom:4px'>💚</div>
      <div style='font-size:1.4rem; font-weight:800; color:#00c882; letter-spacing:0.05em'>4SAVR</div>
      <div style='font-size:0.72rem; color:#5a9ab8; letter-spacing:0.12em; text-transform:uppercase'>For Saver · MVP v0.1</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    visao = st.radio(
        "Selecionar Visão:",
        ["👤  Consumidor (B2C)", "🏪  Lojista Parceiro (B2B)"],
        label_visibility="collapsed",
    )

    st.markdown("---")
    st.markdown("""
    <div style='padding:12px; background:rgba(0,200,130,0.08); border-radius:10px; border:1px solid rgba(0,200,130,0.2)'>
      <div style='font-size:0.72rem; color:#5a9ab8; text-transform:uppercase; letter-spacing:0.1em; margin-bottom:6px'>Bairro Ativo</div>
      <div style='color:#00c882; font-weight:700; font-size:0.95rem'>📍 Bairro Boa Vista</div>
      <div style='color:#7fb8d4; font-size:0.78rem; margin-top:2px'>Curitiba – PR</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style='margin-top:16px; padding:12px; background:rgba(13,58,92,0.4); border-radius:10px;'>
      <div style='font-size:0.72rem; color:#5a9ab8; text-transform:uppercase; letter-spacing:0.1em; margin-bottom:6px'>Status da Rede</div>
      <div style='display:flex; align-items:center; gap:8px'>
        <div style='width:8px;height:8px;border-radius:50%;background:#00c882;box-shadow:0 0 8px #00c882'></div>
        <span style='color:#e8f4f8; font-size:0.85rem'>5 mercados online</span>
      </div>
      <div style='color:#7fb8d4; font-size:0.75rem; margin-top:4px'>Última sync: agora mesmo</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style='margin-top:24px; text-align:center'>
      <div style='font-size:0.78rem; color:#2a5a7a; font-style:italic; line-height:1.5'>
        "Onde sua economia<br>fortalece o bairro."
      </div>
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  ██████  VISÃO CONSUMIDOR (B2C)  ██████
# ─────────────────────────────────────────────
if "Consumidor" in visao:

    # Hero
    st.markdown("""
    <div class='hero-banner'>
      <div class='hero-tag'>🛒 Modo Consumidor</div>
      <h1>Economize no seu bairro, hoje</h1>
      <p>Compare preços em tempo real nos mercados a menos de 1km de você.</p>
    </div>
    """, unsafe_allow_html=True)

    # Top Metrics
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown("""<div class='metric-card'>
          <div class='value'>R&#36; 18,70</div>
          <div class='label'>Economia média/semana</div>
        </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown("""<div class='metric-card'>
          <div class='value'>5</div>
          <div class='label'>Mercados monitorados</div>
        </div>""", unsafe_allow_html=True)
    with c3:
        st.markdown("""<div class='metric-card'>
          <div class='value'>10</div>
          <div class='label'>Produtos rastreados</div>
        </div>""", unsafe_allow_html=True)
    with c4:
        st.markdown("""<div class='metric-card'>
          <div class='value'>340</div>
          <div class='label'>Seus pontos de reputação</div>
        </div>""", unsafe_allow_html=True)

    # ── BUSCA DE PRODUTO ──────────────────────────────────────────
    st.markdown("<div class='section-title'>🔍 Comparador de Preços</div>", unsafe_allow_html=True)

    col_sel, col_info = st.columns([2, 1])
    with col_sel:
        produto_sel = st.selectbox(
            "Selecione o produto:",
            list(PRODUTOS_BASE.keys()),
            format_func=lambda x: f"{PRODUTOS_BASE[x]['emoji']}  {x}",
        )

    with col_info:
        cat = PRODUTOS_BASE[produto_sel]["categoria"]
        und = PRODUTOS_BASE[produto_sel]["unidade"]
        st.markdown(f"""
        <div class='info-card' style='margin-top:28px'>
          <div class='i-title'>Categoria · Unidade</div>
          <div class='i-body'>{cat} · {und}</div>
        </div>""", unsafe_allow_html=True)

    sub = DF[DF["Produto"] == produto_sel].sort_values("Preço (R$)").reset_index(drop=True)
    menor_preco = sub["Preço (R$)"].min()
    maior_preco = sub["Preço (R$)"].max()
    economia_max = round(maior_preco - menor_preco, 2)

    rows_html = ""
    for i, row in sub.iterrows():
        is_best = row["Preço (R$)"] == menor_preco
        badge = "<span class='badge-best'>Melhor Preco</span>" if is_best else ""
        cls = "price-row best" if is_best else "price-row"
        preco_fmt = f"{row['Preço (R$)']:.2f}".replace(".", ",")
        rows_html += f"<div class='{cls}'>"
        rows_html += f"<div><div class='market-name'>{row['Mercado']}</div>"
        rows_html += f"<div class='market-dist'>📍 {row['Distância']} <span class='badge-update'>⏱ {row['Timestamp']}</span></div></div>"
        rows_html += f"<div style='display:flex;align-items:center;gap:12px'>{badge}"
        rows_html += f"<div class='price-val'>R&#36; {preco_fmt}</div></div></div>"
    st.markdown(f"<div class='price-table-wrapper'>{rows_html}</div>", unsafe_allow_html=True)

    if economia_max > 0:
        st.markdown(f"""
        <div class='success-card'>
          <div class='s-title'>💡 Você pode economizar R&#36; {economia_max:.2f} neste item</div>
          <div class='s-body'>Comprando no {sub.iloc[0]['Mercado']} em vez do mais caro, você economiza
          <strong>R&#36; {economia_max:.2f}</strong> por unidade — equivale a <strong>R&#36; {economia_max*4:.2f}</strong>
          por mês se você comprar 4 vezes.</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("---")

    # ── SIMULADOR OCR ──────────────────────────────────────────────
    st.markdown("<div class='section-title'>📷 Cupom Fiscal Inteligente</div>", unsafe_allow_html=True)
    st.markdown("""
    <div class='info-card'>
      <div class='i-title'>Como funciona</div>
      <div class='i-body'>Tire foto do seu cupom fiscal. Nossa IA extrai os preços, valida os dados e credita pontos de reputação na sua conta. Cada cupom = dados frescos para toda a comunidade.</div>
    </div>""", unsafe_allow_html=True)

    col_ocr1, col_ocr2 = st.columns([1, 2])
    with col_ocr1:
        if st.button("📤  Simular Envio de Cupom Fiscal", use_container_width=True):
            with st.spinner("🤖 Processando Inteligência de Dados..."):
                time.sleep(0.6)
                progress = st.progress(0)
                for pct in range(0, 101, 20):
                    time.sleep(0.18)
                    progress.progress(pct)
                time.sleep(0.3)
                progress.empty()
            st.markdown("""
            <div class='success-card'>
              <div class='s-title'>✅ Cupom validado com sucesso!</div>
              <div class='s-body'>
                <strong>7 itens</strong> extraídos · <strong>R&#36; 87,40</strong> processados<br>
                Mercado identificado: <strong>Supermercado Central</strong><br>
                <span style='color:#00c882; font-weight:700; font-size:1.05rem'>+50 pontos de reputação creditados 🎉</span>
              </div>
            </div>""", unsafe_allow_html=True)

    st.markdown("---")

    # ── OTIMIZADOR DE CESTA ──────────────────────────────────────────
    st.markdown("<div class='section-title'>🧺 Otimizador de Cesta</div>", unsafe_allow_html=True)
    st.markdown("""
    <div class='info-card'>
      <div class='i-title'>Como funciona</div>
      <div class='i-body'>Selecione até 5 produtos. O 4SAVR calcula se vale mais a pena comprar tudo num lugar ou dividir entre dois mercados próximos.</div>
    </div>""", unsafe_allow_html=True)

    itens_sel = st.multiselect(
        "Escolha os produtos da sua cesta:",
        list(PRODUTOS_BASE.keys()),
        default=list(PRODUTOS_BASE.keys())[:3],
        format_func=lambda x: f"{PRODUTOS_BASE[x]['emoji']} {x}",
        max_selections=5,
    )

    if itens_sel:
        mercados_list = list(MERCADOS.keys())

        def total_em_mercado(m_idx, produtos):
            return sum(PRECOS_BASE[p][m_idx] for p in produtos)

        totais = [(m, total_em_mercado(i, itens_sel)) for i, m in enumerate(mercados_list)]
        totais_sorted = sorted(totais, key=lambda x: x[1])

        melhor_unico = totais_sorted[0]
        melhor_div_a = totais_sorted[0]
        melhor_div_b = totais_sorted[1]

        # Split strategy: first half items in market A, rest in B
        mid = len(itens_sel) // 2
        grupo_a = itens_sel[:mid] if mid > 0 else itens_sel[:1]
        grupo_b = itens_sel[mid:] if mid > 0 else itens_sel[1:]

        idx_a = mercados_list.index(melhor_div_a[0])
        idx_b = mercados_list.index(melhor_div_b[0])

        total_div = sum(PRECOS_BASE[p][idx_a] for p in grupo_a) + \
                    sum(PRECOS_BASE[p][idx_b] for p in grupo_b if p)

        economia_div = round(melhor_unico[1] - total_div, 2)
        economia_div = max(economia_div, 0)

        col_opt1, col_opt2 = st.columns(2)
        with col_opt1:
            st.markdown(f"""
            <div class='optimizer-box'>
              <div class='opt-title'>🏪 Estratégia 1 — Compra única</div>
              <div class='opt-row'>
                <span class='opt-label'>Melhor mercado</span>
                <span class='opt-val'>{melhor_unico[0][:20]}</span>
              </div>
              <div class='opt-row'>
                <span class='opt-label'>Total estimado</span>
                <span class='opt-val'>R&#36; {melhor_unico[1]:.2f}</span>
              </div>
              <div class='opt-row'>
                <span class='opt-label'>Distância extra</span>
                <span class='opt-val'>0m</span>
              </div>
            </div>""", unsafe_allow_html=True)

        with col_opt2:
            extra_dist = random.randint(300, 600)
            st.markdown(f"""
            <div class='optimizer-box' style='border-color:rgba(0,200,130,0.6)'>
              <div class='opt-title'>🗺️ Estratégia 2 — Dividir entre 2</div>
              <div class='opt-row'>
                <span class='opt-label'>{melhor_div_a[0][:18]} + {melhor_div_b[0][:12]}</span>
                <span class='opt-val'></span>
              </div>
              <div class='opt-row'>
                <span class='opt-label'>Total estimado</span>
                <span class='opt-val'>R&#36; {total_div:.2f}</span>
              </div>
              <div class='opt-row'>
                <span class='opt-label'>Distância extra</span>
                <span class='opt-val'>+{extra_dist}m</span>
              </div>
              <div style='margin-top:12px; text-align:center'>
                <div style='font-size:0.75rem; color:#7fb8d4; margin-bottom:2px'>Economia ao dividir</div>
                <div class='opt-savings'>+ R&#36; {economia_div:.2f} 💚</div>
              </div>
            </div>""", unsafe_allow_html=True)

    st.markdown("---")

    # ── RANKING EMBAIXADORES ──────────────────────────────────────────
    st.markdown("<div class='section-title'>🏆 Embaixadores de Economia do Bairro</div>", unsafe_allow_html=True)
    st.markdown("""
    <div class='info-card' style='margin-bottom:14px'>
      <div class='i-title'>Gamificação Comunitária</div>
      <div class='i-body'>Envie cupons, valide preços e suba no ranking. Quanto mais você contribui, mais o bairro economiza — e mais você é reconhecido. 🎖️</div>
    </div>""", unsafe_allow_html=True)

    for i, emb in enumerate(EMBAIXADORES):
        st.markdown(f"""
        <div class='rank-card'>
          <div class='rank-pos'>#{i+1}</div>
          <div class='rank-badge'>{emb['badge']}</div>
          <div class='rank-name'>{emb['nome']}</div>
          <div class='rank-pts'>{emb['pts']:,} pts</div>
        </div>""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  ██████  VISÃO LOJISTA (B2B)  ██████
# ─────────────────────────────────────────────
else:
    st.markdown("""
    <div class='hero-banner' style='background:linear-gradient(135deg, #0a2a4a 0%, #0d3a5c 40%, #042440 100%); border:1px solid rgba(0,200,130,0.3)'>
      <div class='hero-tag'>🏪 Modo Lojista Parceiro</div>
      <h1>Inteligência Competitiva em Tempo Real</h1>
      <p>Monitore o mercado, reaja a movimentos da concorrência e atraia mais clientes com ofertas inteligentes.</p>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown("""<div class='metric-card'>
          <div class='value'>+127</div>
          <div class='label'>Clientes atraídos hoje</div>
        </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown("""<div class='metric-card'>
          <div class='value'>3</div>
          <div class='label'>Alertas competitivos ativos</div>
        </div>""", unsafe_allow_html=True)
    with c3:
        st.markdown("""<div class='metric-card'>
          <div class='value'>R&#36; 2,4k</div>
          <div class='label'>Receita influenciada/semana</div>
        </div>""", unsafe_allow_html=True)
    with c4:
        st.markdown("""<div class='metric-card'>
          <div class='value'>8.4%</div>
          <div class='label'>Share of shelf digital</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("---")

    # ── ALERTA PERDA DE VENDA ──────────────────────────────────────────
    st.markdown("<div class='section-title'>🚨 Alertas de Mercado</div>", unsafe_allow_html=True)

    st.markdown("""
    <div class='alert-card'>
      <div class='alert-title'>⚠️ Alerta: Perda de Conversão Detectada</div>
      <div class='alert-body'>
        Você perdeu <strong>12% de conversão</strong> no item <strong>Café Torrado 500g</strong> hoje.
        O concorrente <em>Mini Box Econômico</em> a <strong>300m</strong> baixou o preço em <strong>R&#36; 0,40</strong> às 09h15.
      </div>
      <div class='alert-impact'>📉 Impacto estimado: -R&#36; 280 em vendas hoje</div>
    </div>""", unsafe_allow_html=True)

    st.markdown("""
    <div class='alert-card' style='border-left-color:#f59e0b; background:linear-gradient(135deg,rgba(245,158,11,0.1),rgba(120,77,5,0.15))'>
      <div class='alert-title' style='color:#fcd34d'>⚡ Oportunidade: Concorrente com Ruptura de Estoque</div>
      <div class='alert-body' style='color:#fef3c7'>
        <em>Atacado do Bairro</em> está sem estoque de <strong>Óleo de Soja 900ml</strong> desde às 11h00.
        Consumidores estão buscando alternativas no raio de 700m.
      </div>
      <div class='alert-impact' style='color:#fbbf24'>📈 Oportunidade de +R&#36; 190 em vendas extras</div>
    </div>""", unsafe_allow_html=True)

    st.markdown("---")

    # ── DASHBOARD DE PREÇOS ──────────────────────────────────────────
    st.markdown("<div class='section-title'>📊 Dashboard de Posicionamento de Preço</div>", unsafe_allow_html=True)

    col_g1, col_g2 = st.columns([3, 1])
    with col_g1:
        produto_b2b = st.selectbox(
            "Produto para analisar:",
            list(PRODUTOS_BASE.keys()),
            format_func=lambda x: f"{PRODUTOS_BASE[x]['emoji']} {x}",
            key="b2b_prod",
        )
    with col_g2:
        periodo = st.selectbox("Período:", ["14 dias", "7 dias", "30 dias"], key="periodo")

    hist_df = build_history_df(produto_b2b)
    n_dias = 7 if "7" in periodo else (30 if "30" in periodo else 14)
    hist_df = hist_df.tail(n_dias)

    # Gráfico de linha nativo Streamlit – Seu Mercado vs Média do Bairro
    chart_df = hist_df.set_index("Data")[["Mercado Boa Vista", "Média do Bairro"]]
    st.line_chart(chart_df, use_container_width=True)

    # ── BAR CHART – Comparativo Atual ──────────────────────────────
    st.markdown("<div class='section-title'>📊 Comparativo de Preços Atual – Todos os Mercados</div>", unsafe_allow_html=True)

    sub_b2b = DF[DF["Produto"] == produto_b2b].sort_values("Preço (R$)").reset_index(drop=True)
    # Encurta nomes para caber no eixo
    sub_b2b["Mercado Curto"] = sub_b2b["Mercado"].apply(lambda x: x[:18])
    bar_df = sub_b2b.set_index("Mercado Curto")[["Preço (R$)"]]
    st.bar_chart(bar_df, use_container_width=True)

    # Tabela de apoio com preços formatados
    tabela_display = sub_b2b[["Mercado", "Preço (R$)", "Distância", "Timestamp"]].copy()
    tabela_display["Preço (R$)"] = tabela_display["Preço (R$)"].apply(lambda x: f"R$ {x:.2f}")
    tabela_display.columns = ["Mercado", "Preço", "Distância", "Atualização"]
    st.dataframe(tabela_display, use_container_width=True, hide_index=True)

    st.markdown("---")

    # ── SIMULADOR DE ANÚNCIO ──────────────────────────────────────────
    st.markdown("<div class='section-title'>📣 Simulador de Oferta Impulsionada</div>", unsafe_allow_html=True)
    st.markdown("""
    <div class='info-card' style='margin-bottom:16px'>
      <div class='i-title'>Como funciona</div>
      <div class='i-body'>Configure sua oferta abaixo e veja um preview de como ela aparece para os consumidores do bairro no aplicativo 4SAVR.</div>
    </div>""", unsafe_allow_html=True)

    col_ad1, col_ad2 = st.columns(2)
    with col_ad1:
        ad_produto = st.selectbox(
            "Produto em oferta:",
            list(PRODUTOS_BASE.keys()),
            format_func=lambda x: f"{PRODUTOS_BASE[x]['emoji']} {x}",
            key="ad_prod",
        )
        idx_ref = 0
        preco_orig = PRECOS_BASE[ad_produto][idx_ref]
        ad_preco = st.number_input(
            "Preço promocional (R$):",
            min_value=0.50,
            max_value=preco_orig * 1.5,
            value=round(preco_orig * 0.95, 2),
            step=0.10,
        )
        ad_validade = st.selectbox("Validade da oferta:", ["Hoje, até 22h", "Amanhã, dia todo", "Este fim de semana", "Próximos 3 dias"])
        raio_alcance = st.slider("Raio de alcance (metros):", 200, 1000, 500, 50)

    with col_ad2:
        emoji_prod = PRODUTOS_BASE[ad_produto]["emoji"]
        desconto = round((preco_orig - ad_preco) / preco_orig * 100, 1)
        alcance_est = int(raio_alcance * 1.8 + random.randint(80, 150))
        preco_formatado = f"{ad_preco:.2f}".replace(".", ",")

        st.markdown(f"""
        <div style='margin-top:4px'>
          <div style='font-size:0.75rem; color:#5a9ab8; margin-bottom:8px; text-transform:uppercase; letter-spacing:0.1em'>Preview do Anúncio</div>
          <div class='ad-preview'>
            <div class='ad-label'>Oferta Impulsionada</div>
            <div class='ad-store'>📍 Mercado Boa Vista · {raio_alcance}m de raio</div>
            <div class='ad-product'>{emoji_prod} {ad_produto}</div>
            <div class='ad-price'>R&#36; {preco_formatado}</div>
            <div style='color:#fca5a5; font-size:0.8rem; margin-top:4px'>
              ~~R&#36; {preco_orig:.2f}~~ &nbsp;·&nbsp;
              <span style='color:#00c882; font-weight:700'>{desconto:.1f}% OFF</span>
            </div>
            <div class='ad-validity'>⏰ {ad_validade}</div>
            <div class='ad-reach'>👁 Alcance estimado: <strong>{alcance_est} consumidores</strong> no bairro</div>
          </div>
        </div>""", unsafe_allow_html=True)

    col_btn1, col_btn2 = st.columns([1, 2])
    with col_btn1:
        if st.button("🚀  Ativar Oferta", use_container_width=True):
            with st.spinner("Publicando oferta na rede 4SAVR..."):
                time.sleep(1.2)
            st.markdown(f"""
            <div class='success-card'>
              <div class='s-title'>✅ Oferta publicada com sucesso!</div>
              <div class='s-body'>
                <strong>{emoji_prod} {ad_produto}</strong> por <strong>R&#36; {ad_preco:.2f}</strong>
                está visível para <strong>{alcance_est} consumidores</strong> num raio de {raio_alcance}m.<br>
                Validade: <strong>{ad_validade}</strong>.<br>
                Acompanhe o desempenho em tempo real neste painel.
              </div>
            </div>""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  FOOTER
# ─────────────────────────────────────────────
st.markdown("""
<div class='footer-bar'>
  <span>4SAVR</span> · MVP Simulado v0.1 · Dados fictícios para fins de demonstração ·
  Desenvolvido para demonstração a parceiros e investidores<br>
  <em>"Onde sua economia fortalece o bairro."</em>
</div>
""", unsafe_allow_html=True)
