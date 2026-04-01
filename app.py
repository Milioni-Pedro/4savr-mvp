import streamlit as st
import pandas as pd
import random
import time
from datetime import datetime, timedelta

# ─────────────────────────────────────────────────────────────────
#  HELPERS — cifrão seguro para HTML (evita conflito com LaTeX)
# ─────────────────────────────────────────────────────────────────
def fmt(valor):
    """R&#36; X,XX  — seguro para unsafe_allow_html=True"""
    return "R&#36;&nbsp;" + f"{valor:.2f}".replace(".", ",")

def rr(valor):
    """R[cifrão] X.XX  — para texto Python puro (st.write, st.success, etc.)"""
    return "R" + chr(36) + f" {valor:.2f}"

# ─────────────────────────────────────────────────────────────────
#  PAGE CONFIG
# ─────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="4SAVR v3.0 – BI & Inteligência de Estoque",
    page_icon="💚",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────────
#  SESSION STATE
# ─────────────────────────────────────────────────────────────────
if "ofertas_ativas" not in st.session_state:
    st.session_state.ofertas_ativas = [
        {"produto":"Café Torrado 500g","preco":13.90,"validade":"Hoje, até 22h",
         "lojista":"Mercado Boa Vista","emoji":"☕","validado":True,"alcance":342,"ts":"09h15"},
        {"produto":"Leite Integral 1L","preco":3.99,"validade":"Amanhã, dia todo",
         "lojista":"Supermercado Central","emoji":"🥛","validado":True,"alcance":218,"ts":"10h02"},
        {"produto":"Frango Congelado 1kg","preco":9.90,"validade":"Este fim de semana",
         "lojista":"Atacado do Bairro","emoji":"🍗","validado":False,"alcance":97,"ts":"11h30"},
    ]

if "precos_validados" not in st.session_state:
    st.session_state.precos_validados = {
        ("Leite Integral 1L","Supermercado Central"),
        ("Arroz Branco 5kg","Atacado do Bairro"),
        ("Café Torrado 500g","Mini Box Econômico"),
        ("Cerveja Lata 350ml","Mercado Família"),
        ("Óleo de Soja 900ml","Mercado Boa Vista"),
    }

if "pontos_usuario" not in st.session_state:
    st.session_state.pontos_usuario = 340

if "total_validacoes" not in st.session_state:
    st.session_state.total_validacoes = 7

# Contador de buscas por produto — alimenta o BI do lojista
if "search_counter" not in st.session_state:
    st.session_state.search_counter = {
        "Café Torrado 500g":       28,
        "Leite Integral 1L":       24,
        "Arroz Branco 5kg":        19,
        "Frango Congelado 1kg":    17,
        "Cerveja Lata 350ml":      15,
        "Feijão Carioca 1kg":      12,
        "Óleo de Soja 900ml":      10,
        "Açúcar Cristal 1kg":       8,
        "Pão de Forma 500g":        6,
        "Macarrão Espaguete 500g":  4,
    }

# ─────────────────────────────────────────────────────────────────
#  MOCK DATA
# ─────────────────────────────────────────────────────────────────
MERCADOS = {
    "Mercado Boa Vista":    "0m (referência)",
    "Supermercado Central": "180m",
    "Mini Box Econômico":   "300m",
    "Atacado do Bairro":    "520m",
    "Mercado Família":      "750m",
}

PRODUTOS_BASE = {
    "Leite Integral 1L":       {"emoji":"🥛","categoria":"Laticínios","unidade":"1L"},
    "Arroz Branco 5kg":        {"emoji":"🌾","categoria":"Grãos","unidade":"5kg"},
    "Feijão Carioca 1kg":      {"emoji":"🫘","categoria":"Grãos","unidade":"1kg"},
    "Cerveja Lata 350ml":      {"emoji":"🍺","categoria":"Bebidas","unidade":"lata"},
    "Café Torrado 500g":       {"emoji":"☕","categoria":"Bebidas","unidade":"500g"},
    "Óleo de Soja 900ml":      {"emoji":"🫙","categoria":"Condimentos","unidade":"900ml"},
    "Açúcar Cristal 1kg":      {"emoji":"🍬","categoria":"Açúcar","unidade":"1kg"},
    "Pão de Forma 500g":       {"emoji":"🍞","categoria":"Padaria","unidade":"500g"},
    "Macarrão Espaguete 500g": {"emoji":"🍝","categoria":"Massas","unidade":"500g"},
    "Frango Congelado 1kg":    {"emoji":"🍗","categoria":"Proteínas","unidade":"1kg"},
}

PRECOS_BASE = {
    "Leite Integral 1L":       [4.79,4.99,4.49,4.29,5.10],
    "Arroz Branco 5kg":        [22.90,23.50,21.80,20.50,24.00],
    "Feijão Carioca 1kg":      [8.99,8.49,9.20,7.99,9.50],
    "Cerveja Lata 350ml":      [3.89,3.99,3.79,3.59,4.10],
    "Café Torrado 500g":       [15.90,16.50,14.90,14.20,16.90],
    "Óleo de Soja 900ml":      [6.89,7.10,6.59,6.29,7.20],
    "Açúcar Cristal 1kg":      [3.49,3.59,3.39,3.19,3.70],
    "Pão de Forma 500g":       [7.49,7.99,7.29,6.99,8.10],
    "Macarrão Espaguete 500g": [4.29,4.49,4.09,3.89,4.59],
    "Frango Congelado 1kg":    [11.90,12.50,11.20,10.80,12.90],
}

TIMESTAMPS = [
    "Atualizado há 8 min","Atualizado há 15 min","Atualizado há 23 min",
    "Atualizado há 41 min","Atualizado há 1h 02min",
]

EMBAIXADORES = [
    {"nome":"Ana Paula M.","pts":1840,"badge":"🏆"},
    {"nome":"Ricardo S.",  "pts":1622,"badge":"🥈"},
    {"nome":"Fernanda L.", "pts":1405,"badge":"🥉"},
    {"nome":"João Victor", "pts":1298,"badge":"⭐"},
    {"nome":"Marcia T.",   "pts":1187,"badge":"⭐"},
]

# Dados de estoque simulados por produto
ESTOQUE_DATA = {
    "Leite Integral 1L":       {"estoque":48,"giro_dia":12,"validade_dias":3, "custo":3.20,"preco_venda":4.79,"pedido_min":24,"status":"ok"},
    "Arroz Branco 5kg":        {"estoque":32,"giro_dia":4, "validade_dias":180,"custo":17.00,"preco_venda":22.90,"pedido_min":12,"status":"ok"},
    "Feijão Carioca 1kg":      {"estoque":15,"giro_dia":3, "validade_dias":90, "custo":6.20,"preco_venda":8.99,"pedido_min":12,"status":"atencao"},
    "Cerveja Lata 350ml":      {"estoque":120,"giro_dia":20,"validade_dias":180,"custo":2.50,"preco_venda":3.89,"pedido_min":48,"status":"ok"},
    "Café Torrado 500g":       {"estoque":9, "giro_dia":8, "validade_dias":60, "custo":10.80,"preco_venda":15.90,"pedido_min":12,"status":"atencao"},
    "Óleo de Soja 900ml":      {"estoque":6, "giro_dia":2, "validade_dias":8,  "custo":4.80,"preco_venda":6.89,"pedido_min":12,"status":"risco"},
    "Açúcar Cristal 1kg":      {"estoque":22,"giro_dia":3, "validade_dias":365,"custo":2.30,"preco_venda":3.49,"pedido_min":12,"status":"ok"},
    "Pão de Forma 500g":       {"estoque":8, "giro_dia":5, "validade_dias":4,  "custo":5.20,"preco_venda":7.49,"pedido_min":12,"status":"risco"},
    "Macarrão Espaguete 500g": {"estoque":30,"giro_dia":4, "validade_dias":180,"custo":2.80,"preco_venda":4.29,"pedido_min":12,"status":"ok"},
    "Frango Congelado 1kg":    {"estoque":18,"giro_dia":6, "validade_dias":30, "custo":8.20,"preco_venda":11.90,"pedido_min":12,"status":"atencao"},
}

# Dados de marcas por categoria
MARCAS_DATA = {
    "Café Torrado 500g": {
        "marcas": ["Pilão","3 Corações","Melitta","Iguaçu","Café do Bairro"],
        "vendas": [42,35,28,18,12],
        "margem": [18,22,20,25,30],
    },
    "Leite Integral 1L": {
        "marcas": ["Italac","Piracanjuba","Vigor","Parmalat","Ninho"],
        "vendas": [55,48,32,25,18],
        "margem": [15,18,20,14,22],
    },
    "Arroz Branco 5kg": {
        "marcas": ["Camil","Tio João","Prato Fino","Namorado","A Granel"],
        "vendas": [38,34,22,16,8],
        "margem": [12,14,18,20,28],
    },
    "Cerveja Lata 350ml": {
        "marcas": ["Skol","Brahma","Itaipava","Original","Eisenbahn"],
        "vendas": [60,52,38,24,12],
        "margem": [20,18,22,28,35],
    },
}

def build_df():
    rows = []
    for prod, precos in PRECOS_BASE.items():
        for i, merc in enumerate(MERCADOS):
            rows.append({"Produto":prod,"Mercado":merc,
                         "Distancia":list(MERCADOS.values())[i],
                         "Preco":precos[i],"Timestamp":TIMESTAMPS[i]})
    return pd.DataFrame(rows)

def build_history(produto):
    dias  = [datetime.today() - timedelta(days=i) for i in range(13,-1,-1)]
    base  = PRECOS_BASE[produto][0]
    media = sum(PRECOS_BASE[produto]) / len(PRECOS_BASE[produto])
    random.seed(42)
    return pd.DataFrame({
        "Data":            [d.strftime("%d/%m") for d in dias],
        "Seu Mercado":     [round(base  + random.uniform(-.3, .4 ), 2) for _ in dias],
        "Media do Bairro": [round(media + random.uniform(-.15,.15), 2) for _ in dias],
    })

def build_reach_df(oferta):
    horas = [f"{h:02d}h" for h in range(8, 23)]
    alvo  = oferta.get("alcance", 100)
    vals, acc = [], 0
    for h in range(len(horas)):
        pico = 1 if h in [3,4,5,10,11] else 0
        acc  = min(acc + random.randint(8+pico*25, 20+pico*60), alvo)
        vals.append(acc)
    return pd.DataFrame({"Hora":horas,"Visualizações":vals}).set_index("Hora")

def build_vendas_historico(produto, dias=14):
    random.seed(hash(produto) % 999)
    base  = ESTOQUE_DATA[produto]["giro_dia"]
    datas = [(datetime.today()-timedelta(days=i)).strftime("%d/%m") for i in range(dias-1,-1,-1)]
    vendas = [max(0, round(base + random.gauss(0, base*0.3))) for _ in datas]
    return pd.DataFrame({"Data":datas,"Vendas":vendas}).set_index("Data")

DF = build_df()

# ─────────────────────────────────────────────────────────────────
#  CSS
# ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Sora:wght@300;400;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap');

  html,body,[class*="css"]{ font-family:'Sora',sans-serif; }
  .stApp{ background:linear-gradient(160deg,#020f1f 0%,#031a30 60%,#042440 100%); color:#e8f4f8; }
  [data-testid="stSidebar"]{ background:linear-gradient(180deg,#010d1c,#021525); border-right:1px solid #0d3a5c; }
  [data-testid="stSidebar"] *{ color:#c8e6f5 !important; }
  h1,h2,h3{ font-family:'Sora',sans-serif !important; }
  hr{ border-color:rgba(13,58,92,.6) !important; }

  /* ── Tabs ── */
  .stTabs [data-baseweb="tab-list"]{ background:rgba(13,58,92,.4); border-radius:12px; padding:4px; gap:4px; border:1px solid rgba(0,200,130,.15); }
  .stTabs [data-baseweb="tab"]{ background:transparent; border-radius:9px; color:#7fb8d4; font-weight:600; font-size:.88rem; padding:8px 18px; transition:.2s; }
  .stTabs [data-baseweb="tab"]:hover{ background:rgba(0,200,130,.1); color:#00c882; }
  .stTabs [aria-selected="true"]{ background:rgba(0,200,130,.18) !important; color:#00c882 !important; border:1px solid rgba(0,200,130,.4) !important; }
  .stTabs [data-baseweb="tab-panel"]{ padding:20px 0 0; }

  /* ── Hero ── */
  .hero{ background:linear-gradient(135deg,#00c882,#00a86b,#007a50); border-radius:16px; padding:28px 36px; margin-bottom:24px; box-shadow:0 8px 32px rgba(0,200,130,.25); }
  .hero h1{ color:#fff !important; font-size:2rem !important; font-weight:800 !important; margin:0 0 6px !important; }
  .hero p{ color:rgba(255,255,255,.9) !important; font-size:1.05rem; margin:0; }
  .hero-b2b{ background:linear-gradient(135deg,#0a2a4a,#0d3a5c,#042440) !important; border:1px solid rgba(0,200,130,.3); }
  .hero-tag{ display:inline-block; background:rgba(255,255,255,.2); color:#fff !important; font-size:.72rem; font-weight:600; letter-spacing:.12em; text-transform:uppercase; padding:4px 12px; border-radius:20px; margin-bottom:12px; }

  /* ── Metric cards ── */
  .mc{ background:linear-gradient(145deg,rgba(13,58,92,.6),rgba(4,36,64,.8)); border:1px solid rgba(0,200,130,.2); border-radius:14px; padding:18px 20px; text-align:center; backdrop-filter:blur(8px); transition:.2s; }
  .mc:hover{ transform:translateY(-3px); box-shadow:0 12px 28px rgba(0,200,130,.15); }
  .mc .v{ font-size:1.9rem; font-weight:800; color:#00c882; font-family:'JetBrains Mono',monospace; line-height:1.1; }
  .mc .l{ font-size:.74rem; color:#7fb8d4; text-transform:uppercase; letter-spacing:.08em; margin-top:5px; }
  .mc-warn .v{ color:#facc15; }
  .mc-danger .v{ color:#f87171; }

  /* ── Section title ── */
  .st{ font-size:1.05rem; font-weight:700; color:#00c882; text-transform:uppercase; letter-spacing:.1em; margin:26px 0 12px; padding-bottom:8px; border-bottom:1px solid rgba(0,200,130,.25); }

  /* ── Price boxes ── */
  .pb{ border-radius:10px; padding:13px 17px; margin-bottom:7px; }
  .pb-best{ background:rgba(0,200,130,.10); border:2px solid #00c882; }
  .pb-norm{ background:rgba(13,58,92,.40); border:1px solid rgba(13,58,92,.8); }
  .pn-best{ font-weight:700; font-size:.95rem; color:#00c882; }
  .pn-norm{ font-weight:700; font-size:.95rem; color:#e8f4f8; }
  .psub{ font-size:.76rem; color:#7fb8d4; margin-top:2px; }
  .pv{ font-family:'JetBrains Mono',monospace; font-size:1.3rem; font-weight:800; text-align:right; }
  .pv-best{ color:#00c882; } .pv-norm{ color:#e8f4f8; }
  .bge{ display:inline-block; background:#00c882; color:#010d1c; font-size:.6rem; font-weight:700; padding:2px 7px; border-radius:20px; text-transform:uppercase; margin-left:5px; vertical-align:middle; }
  .bgv{ display:inline-block; background:rgba(0,200,130,.15); border:1px solid #00c882; color:#00c882; font-size:.6rem; font-weight:700; padding:2px 7px; border-radius:20px; margin-left:5px; vertical-align:middle; }

  /* ── Cards ── */
  .alert-c{ background:linear-gradient(135deg,rgba(220,38,38,.15),rgba(153,27,27,.2)); border:1px solid rgba(220,38,38,.5); border-left:4px solid #dc2626; border-radius:12px; padding:16px 20px; margin:10px 0; }
  .alert-t{ color:#fca5a5; font-weight:700; font-size:.82rem; text-transform:uppercase; letter-spacing:.1em; margin-bottom:7px; }
  .alert-b{ color:#fecaca; font-size:.93rem; line-height:1.6; }
  .alert-i{ color:#f87171; font-weight:700; font-size:1.05rem; margin-top:7px; }
  .warn-c{ background:linear-gradient(135deg,rgba(250,204,21,.1),rgba(120,77,5,.18)); border:1px solid rgba(250,204,21,.4); border-left:4px solid #facc15; border-radius:12px; padding:16px 20px; margin:10px 0; }
  .warn-t{ color:#fcd34d; font-weight:700; font-size:.82rem; text-transform:uppercase; letter-spacing:.1em; margin-bottom:7px; }
  .warn-b{ color:#fef3c7; font-size:.93rem; line-height:1.6; }
  .succ-c{ background:linear-gradient(135deg,rgba(0,200,130,.15),rgba(0,120,80,.2)); border:1px solid rgba(0,200,130,.5); border-left:4px solid #00c882; border-radius:12px; padding:16px 20px; margin:10px 0; }
  .succ-t{ color:#6ee7b7; font-weight:700; font-size:.97rem; margin-bottom:5px; }
  .succ-b{ color:#a7f3d0; font-size:.88rem; line-height:1.5; }
  .info-c{ background:rgba(13,58,92,.5); border:1px solid rgba(0,200,130,.2); border-radius:12px; padding:14px 18px; margin:8px 0; }
  .info-t{ color:#7fb8d4; font-size:.74rem; text-transform:uppercase; letter-spacing:.08em; margin-bottom:3px; }
  .info-b{ color:#e8f4f8; font-size:.93rem; font-weight:500; }

  /* ── Offer cards ── */
  .oc{ background:linear-gradient(135deg,rgba(0,200,130,.10),rgba(4,36,64,.9)); border:1px solid rgba(0,200,130,.4); border-radius:14px; padding:16px 20px; margin-bottom:10px; position:relative; overflow:hidden; }
  .oc-unval{ border-color:rgba(250,204,21,.35); background:linear-gradient(135deg,rgba(250,204,21,.06),rgba(4,36,64,.9)); }
  .oc-bv{ position:absolute; top:12px; right:14px; background:#00c882; color:#010d1c; font-size:.6rem; font-weight:700; padding:2px 9px; border-radius:20px; text-transform:uppercase; }
  .oc-bp{ position:absolute; top:12px; right:14px; background:rgba(250,204,21,.18); border:1px solid #facc15; color:#facc15; font-size:.6rem; font-weight:700; padding:2px 9px; border-radius:20px; }
  .oc-prod{ font-size:1.05rem; font-weight:700; color:#fff; }
  .oc-loj{ font-size:.76rem; color:#7fb8d4; margin-top:2px; }
  .oc-pre{ font-family:'JetBrains Mono',monospace; font-size:1.5rem; font-weight:800; color:#00c882; margin-top:5px; }
  .oc-val{ font-size:.73rem; color:#7fb8d4; margin-top:3px; }
  .oc-alc{ font-size:.76rem; color:#a7f3d0; margin-top:3px; }

  /* ── Trust certificate ── */
  .trust{ background:linear-gradient(135deg,rgba(0,200,130,.15),rgba(0,80,50,.3)); border:2px solid #00c882; border-radius:16px; padding:22px 26px; margin:12px 0; text-align:center; }
  .trust .sc{ font-family:'JetBrains Mono',monospace; font-size:2.8rem; font-weight:800; color:#00c882; }
  .trust .sl{ font-size:.76rem; color:#7fb8d4; text-transform:uppercase; letter-spacing:.12em; }
  .trust .sm{ color:#a7f3d0; font-size:.92rem; margin-top:10px; line-height:1.6; }
  .trust .ss{ font-size:1.3rem; letter-spacing:4px; margin:7px 0; }

  /* ── Inventory table rows ── */
  .inv-ok  { background:rgba(0,200,130,.08); border:1px solid rgba(0,200,130,.25); border-radius:10px; padding:12px 16px; margin-bottom:8px; }
  .inv-warn{ background:rgba(250,204,21,.07); border:1px solid rgba(250,204,21,.3);  border-radius:10px; padding:12px 16px; margin-bottom:8px; }
  .inv-risk{ background:rgba(220,38,38,.08);  border:1px solid rgba(220,38,38,.35);  border-radius:10px; padding:12px 16px; margin-bottom:8px; }
  .inv-label{ font-size:.72rem; text-transform:uppercase; letter-spacing:.1em; font-weight:700; }
  .inv-ok   .inv-label{ color:#00c882; }
  .inv-warn .inv-label{ color:#facc15; }
  .inv-risk .inv-label{ color:#f87171; }
  .inv-prod { font-size:.97rem; font-weight:700; color:#e8f4f8; margin:3px 0; }
  .inv-meta { font-size:.78rem; color:#7fb8d4; }
  .inv-num  { font-family:'JetBrains Mono',monospace; font-size:1.1rem; font-weight:700; text-align:right; }
  .inv-ok   .inv-num{ color:#00c882; }
  .inv-warn .inv-num{ color:#facc15; }
  .inv-risk .inv-num{ color:#f87171; }

  /* ── Form box ── */
  .fb{ background:rgba(4,36,64,.7); border:1px solid rgba(0,200,130,.25); border-radius:14px; padding:20px 22px; margin:12px 0; }
  .fb-title{ color:#00c882; font-weight:700; font-size:.97rem; margin-bottom:12px; }

  /* ── Opt box ── */
  .ob{ background:linear-gradient(135deg,rgba(0,200,130,.08),rgba(4,36,64,.8)); border:1px solid rgba(0,200,130,.3); border-radius:14px; padding:20px 22px; margin:12px 0; }
  .ob-hi{ border-color:rgba(0,200,130,.65) !important; }
  .ob-title{ color:#00c882; font-weight:700; font-size:.97rem; margin-bottom:10px; }

  /* ── Rank ── */
  .rc{ display:flex; align-items:center; gap:12px; background:rgba(13,58,92,.4); border:1px solid rgba(13,58,92,.8); border-radius:10px; padding:11px 16px; margin-bottom:7px; }
  .rp{ font-family:'JetBrains Mono',monospace; font-size:1rem; font-weight:700; color:#00c882; width:26px; }
  .rn{ font-weight:600; color:#e8f4f8; flex:1; }
  .rpt{ font-family:'JetBrains Mono',monospace; font-size:.82rem; color:#7fb8d4; }

  /* ── Buttons ── */
  .stButton>button{ background:linear-gradient(135deg,#00c882,#00a86b) !important; color:#010d1c !important; font-weight:700 !important; font-family:'Sora',sans-serif !important; border:none !important; border-radius:10px !important; padding:10px 22px !important; box-shadow:0 4px 16px rgba(0,200,130,.3) !important; transition:.2s !important; }
  .stButton>button:hover{ transform:translateY(-2px) !important; }
  .stSelectbox>div>div,.stMultiSelect>div>div,.stTextInput>div>div,.stNumberInput>div>div{ background:rgba(13,58,92,.5) !important; border:1px solid rgba(0,200,130,.3) !important; border-radius:10px !important; }

  /* ── Live dot ── */
  .ld{ display:inline-block; width:7px; height:7px; border-radius:50%; background:#00c882; box-shadow:0 0 7px #00c882; margin-right:5px; animation:pulse 1.5s infinite; }
  @keyframes pulse{ 0%,100%{opacity:1}50%{opacity:.3} }

  /* ── Footer ── */
  .foot{ text-align:center; padding:18px; color:#2a5a7a; font-size:.73rem; margin-top:36px; border-top:1px solid rgba(13,58,92,.5); }
  .foot span{ color:#00c882; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────
#  SIDEBAR
# ─────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center;padding:14px 0 20px'>
      <div style='font-size:2.2rem;margin-bottom:4px'>💚</div>
      <div style='font-size:1.35rem;font-weight:800;color:#00c882;letter-spacing:.05em'>4SAVR</div>
      <div style='font-size:.7rem;color:#5a9ab8;letter-spacing:.12em;text-transform:uppercase'>For Saver · MVP v3.0</div>
    </div>""", unsafe_allow_html=True)
    st.markdown("---")

    visao = st.radio("Visão:", ["👤  Consumidor (B2C)","🏪  Lojista Parceiro (B2B)"],
                     label_visibility="collapsed")
    st.markdown("---")

    n_of  = len(st.session_state.ofertas_ativas)
    n_val = len(st.session_state.precos_validados)
    top_busca = max(st.session_state.search_counter, key=st.session_state.search_counter.get)

    st.markdown(f"""
    <div style='padding:11px;background:rgba(0,200,130,.08);border-radius:10px;border:1px solid rgba(0,200,130,.2);margin-bottom:9px'>
      <div style='font-size:.7rem;color:#5a9ab8;text-transform:uppercase;letter-spacing:.1em;margin-bottom:5px'>Bairro Ativo</div>
      <div style='color:#00c882;font-weight:700;font-size:.93rem'>📍 Bairro Boa Vista</div>
      <div style='color:#7fb8d4;font-size:.76rem;margin-top:2px'>Curitiba – PR</div>
    </div>
    <div style='padding:11px;background:rgba(13,58,92,.4);border-radius:10px;margin-bottom:9px'>
      <div style='font-size:.7rem;color:#5a9ab8;text-transform:uppercase;letter-spacing:.1em;margin-bottom:8px'>Rede em Tempo Real</div>
      <div style='display:flex;align-items:center;gap:6px;margin-bottom:5px'>
        <div class='ld'></div><span style='color:#e8f4f8;font-size:.83rem'>5 mercados online</span>
      </div>
      <div style='display:flex;justify-content:space-between;margin-bottom:4px'>
        <span style='color:#7fb8d4;font-size:.78rem'>🔥 Ofertas ativas</span>
        <span style='color:#00c882;font-weight:700;font-family:monospace'>{n_of}</span>
      </div>
      <div style='display:flex;justify-content:space-between;margin-bottom:4px'>
        <span style='color:#7fb8d4;font-size:.78rem'>✅ Preços validados</span>
        <span style='color:#00c882;font-weight:700;font-family:monospace'>{n_val}</span>
      </div>
      <div style='display:flex;justify-content:space-between'>
        <span style='color:#7fb8d4;font-size:.78rem'>⭐ Seus pontos</span>
        <span style='color:#00c882;font-weight:700;font-family:monospace'>{st.session_state.pontos_usuario}</span>
      </div>
    </div>
    <div style='padding:11px;background:rgba(13,58,92,.4);border-radius:10px;margin-bottom:9px'>
      <div style='font-size:.7rem;color:#5a9ab8;text-transform:uppercase;letter-spacing:.1em;margin-bottom:5px'>🔥 Mais buscado agora</div>
      <div style='color:#00c882;font-weight:700;font-size:.88rem'>{PRODUTOS_BASE[top_busca]["emoji"]} {top_busca}</div>
      <div style='color:#7fb8d4;font-size:.74rem;margin-top:2px'>{st.session_state.search_counter[top_busca]} buscas hoje</div>
    </div>
    <div style='margin-top:16px;text-align:center;font-size:.76rem;color:#2a5a7a;font-style:italic;line-height:1.6'>
      "Onde sua economia<br>fortalece o bairro."
    </div>""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════
#  VISÃO CONSUMIDOR (B2C)
# ═══════════════════════════════════════════════════════════════════
if "Consumidor" in visao:

    st.markdown("""
    <div class='hero'>
      <div class='hero-tag'>🛒 Modo Consumidor · v3.0</div>
      <h1>Economize no seu bairro, hoje</h1>
      <p>Preços em tempo real · Ofertas validadas pela comunidade · Dados que fortalecem o bairro</p>
    </div>""", unsafe_allow_html=True)

    c1,c2,c3,c4 = st.columns(4)
    for col,(v,l) in zip([c1,c2,c3,c4],[
        ("18,70","Economia média/semana"),
        (str(n_of),"Ofertas ativas agora"),
        (str(st.session_state.pontos_usuario),"Seus pontos"),
        (str(st.session_state.total_validacoes),"Suas validações"),
    ]):
        col.markdown(f"<div class='mc'><div class='v'>{v}</div><div class='l'>{l}</div></div>",
                     unsafe_allow_html=True)

    # ── 🔥 OFERTAS DO LOJISTA ──────────────────────────────────────
    st.markdown("<div class='st'>🔥 Ofertas Diretas do Lojista</div>", unsafe_allow_html=True)
    st.markdown("""
    <div class='info-c'>
      <div class='info-t'>Como funciona</div>
      <div class='info-b'>Lojistas parceiros publicam ofertas em tempo real. ✅ <strong>Verificado</strong>
      = confirmado por foto da comunidade com GPS + Timestamp.</div>
    </div>""", unsafe_allow_html=True)

    if not st.session_state.ofertas_ativas:
        st.info("Nenhuma oferta ativa no momento.")
    else:
        for i, of in enumerate(st.session_state.ofertas_ativas):
            val   = of.get("validado", False)
            cls   = "oc" if val else "oc oc-unval"
            badge = "<div class='oc-bv'>✅ Verificado</div>" if val else "<div class='oc-bp'>⏳ Pendente</div>"
            st.markdown(
                f"<div class='{cls}'>{badge}"
                f"<div style='display:flex;align-items:flex-start;gap:14px'>"
                f"  <div style='font-size:2rem;margin-top:2px'>{of['emoji']}</div>"
                f"  <div>"
                f"    <div class='oc-prod'>{of['produto']}</div>"
                f"    <div class='oc-loj'>📍 {of['lojista']} · {of.get('ts','—')}</div>"
                f"    <div class='oc-pre'>{fmt(of['preco'])}</div>"
                f"    <div class='oc-val'>⏰ {of['validade']}</div>"
                f"    <div class='oc-alc'>👁 {of['alcance']} pessoas viram esta oferta</div>"
                f"  </div></div></div>",
                unsafe_allow_html=True,
            )
            if not val:
                cb, _ = st.columns([1,4])
                with cb:
                    if st.button("📸 Validar oferta", key=f"vo_{i}"):
                        st.session_state.ofertas_ativas[i]["validado"] = True
                        st.session_state.pontos_usuario += 30
                        st.session_state.total_validacoes += 1
                        st.balloons()
                        st.success("✅ Oferta validada! +30 pontos. Obrigado por fortalecer o bairro!")
                        st.rerun()

    st.markdown("---")

    # ── COMPARADOR DE PREÇOS ────────────────────────────────────────
    st.markdown("<div class='st'>🔍 Comparador de Preços</div>", unsafe_allow_html=True)

    cs, ci = st.columns([2,1])
    with cs:
        produto_sel = st.selectbox(
            "Produto:",
            list(PRODUTOS_BASE.keys()),
            format_func=lambda x: f"{PRODUTOS_BASE[x]['emoji']}  {x}",
        )
    with ci:
        p = PRODUTOS_BASE[produto_sel]
        st.markdown(
            f"<div class='info-c' style='margin-top:28px'>"
            f"<div class='info-t'>Categoria · Unidade</div>"
            f"<div class='info-b'>{p['categoria']} · {p['unidade']}</div></div>",
            unsafe_allow_html=True,
        )

    # Incrementa contador de busca — alimenta BI do lojista em tempo real
    st.session_state.search_counter[produto_sel] = \
        st.session_state.search_counter.get(produto_sel, 0) + 1

    sub         = DF[DF["Produto"]==produto_sel].sort_values("Preco").reset_index(drop=True)
    menor_preco = sub["Preco"].min()
    economia_max = round(sub["Preco"].max() - menor_preco, 2)

    for _, row in sub.iterrows():
        best     = row["Preco"] == menor_preco
        validado = (produto_sel, row["Mercado"]) in st.session_state.precos_validados
        bc = "pb pb-best" if best else "pb pb-norm"
        nc = "pn-best"   if best else "pn-norm"
        pc = "pv pv-best" if best else "pv pv-norm"
        bb = "<span class='bge'>Melhor Preço</span>" if best     else ""
        bv = "<span class='bgv'>✅ Verificado</span>" if validado else ""
        st.markdown(
            f"<div class='{bc}'>"
            f"<div style='display:flex;justify-content:space-between;align-items:center'>"
            f"  <div><div class='{nc}'>{row['Mercado']} {bb} {bv}</div>"
            f"      <div class='psub'>📍 {row['Distancia']} &nbsp;⏱ {row['Timestamp']}</div></div>"
            f"  <div class='{pc}'>{fmt(row['Preco'])}</div>"
            f"</div></div>",
            unsafe_allow_html=True,
        )

    if economia_max > 0:
        st.markdown(
            f"<div class='succ-c'><div class='succ-t'>💡 Economia de {fmt(economia_max)} possível</div>"
            f"<div class='succ-b'>Comprando no <strong>{sub.iloc[0]['Mercado']}</strong> você economiza "
            f"<strong>{fmt(economia_max)}</strong> — equivale a "
            f"<strong>{fmt(economia_max*4)}</strong>/mês comprando 4x.</div></div>",
            unsafe_allow_html=True,
        )

    st.markdown("---")

    # ── VALIDAÇÃO MULTICANAL ───────────────────────────────────────
    st.markdown("<div class='st'>📸 Validação Multicanal de Preços</div>", unsafe_allow_html=True)
    st.markdown("""
    <div class='info-c'>
      <div class='info-t'>Crowdsourcing de Confiança</div>
      <div class='info-b'>Suas fotos validam preços para toda a comunidade e geram
      dados reais que o lojista usa para tomar decisões. Você é parte da inteligência do bairro.</div>
    </div>""", unsafe_allow_html=True)

    tipo_up = st.radio("Tipo de envio:", [
        "🧾  Nota Fiscal (NF) – Leitura de preço de compra",
        "🏷️  Gôndola / Anúncio Físico – Validação de promoção",
    ], label_visibility="collapsed")

    cu1, cu2 = st.columns(2)
    with cu1:
        prod_val = st.selectbox("Produto:", list(PRODUTOS_BASE.keys()),
                                format_func=lambda x: f"{PRODUTOS_BASE[x]['emoji']} {x}", key="pv")
        merc_val = st.selectbox("Mercado:", list(MERCADOS.keys()), key="mv")
    with cu2:
        st.markdown("""
        <div class='info-c' style='margin-top:4px;border-style:dashed'>
          <div class='info-t'>📤 Simulando upload de imagem</div>
          <div class='info-b' style='font-size:.82rem'>No app real: câmera abre com geolocalização
          ativada, OCR extrai dados automaticamente e assina com hash criptográfico.</div>
        </div>""", unsafe_allow_html=True)

    ce, _ = st.columns([1,3])
    with ce:
        tipo_label = "NF" if "Nota Fiscal" in tipo_up else "Gôndola"
        if st.button(f"📤 Simular Foto de {tipo_label}", use_container_width=True):
            with st.spinner("🤖 Analisando imagem com IA…"):
                prog  = st.progress(0)
                etapas = ["Detectando produto…","Lendo preço…","Validando GPS…","Confirmando timestamp…","Gerando certificado…"]
                for pct, et in zip(range(0,101,20), etapas):
                    time.sleep(0.28)
                    prog.progress(pct, text=et)
                prog.empty()

            chave = (prod_val, merc_val)
            st.session_state.precos_validados.add(chave)
            st.session_state.pontos_usuario    += 50
            st.session_state.total_validacoes  += 1
            preco_val_item = PRECOS_BASE[prod_val][list(MERCADOS.keys()).index(merc_val)]
            st.balloons()
            st.success(f"✅ Você fez o bairro mais inteligente! +50 pontos creditados.")
            tipo_txt = "Nota Fiscal" if "Nota Fiscal" in tipo_up else "Foto de Gôndola"
            st.markdown(
                f"<div class='trust'>"
                f"<div class='sl'>Trust Score — {tipo_txt}</div>"
                f"<div class='ss'>⭐⭐⭐⭐⭐</div>"
                f"<div class='sc'>9.8<span style='font-size:1.1rem;color:#7fb8d4'>/10</span></div>"
                f"<div class='sm'>Foto validada via <strong>GPS + Timestamp</strong>.<br>"
                f"O preço de <strong>{fmt(preco_val_item)}</strong> no <strong>{merc_val}</strong>"
                f" é agora <strong>oficial para todo o bairro!</strong> 🎉</div>"
                f"</div>",
                unsafe_allow_html=True,
            )

    st.markdown("---")

    # ── OTIMIZADOR DE CESTA ────────────────────────────────────────
    st.markdown("<div class='st'>🧺 Otimizador de Cesta</div>", unsafe_allow_html=True)
    itens_sel = st.multiselect(
        "Produtos:",
        list(PRODUTOS_BASE.keys()),
        default=list(PRODUTOS_BASE.keys())[:3],
        format_func=lambda x: f"{PRODUTOS_BASE[x]['emoji']} {x}",
        max_selections=5,
    )
    if itens_sel:
        mlist  = list(MERCADOS.keys())
        totais = sorted([(m, sum(PRECOS_BASE[p][i] for p in itens_sel))
                         for i,m in enumerate(mlist)], key=lambda x: x[1])
        bm, bt  = totais[0];  sm, _ = totais[1]
        mid     = max(len(itens_sel)//2, 1)
        ia, ib  = mlist.index(bm), mlist.index(sm)
        tdiv    = (sum(PRECOS_BASE[p][ia] for p in itens_sel[:mid])
                 + sum(PRECOS_BASE[p][ib] for p in itens_sel[mid:]))
        ediv    = max(round(bt - tdiv, 2), 0)
        xdist   = random.randint(300,600)
        o1,o2   = st.columns(2)
        with o1:
            st.markdown(
                f"<div class='ob'><div class='ob-title'>🏪 Compra única</div>"
                f"<table style='width:100%;font-size:.86rem;border-spacing:0 5px'>"
                f"<tr><td style='color:#7fb8d4'>Melhor mercado</td><td style='text-align:right;font-weight:700;color:#e8f4f8'>{bm[:22]}</td></tr>"
                f"<tr><td style='color:#7fb8d4'>Total</td><td style='text-align:right;font-weight:700;color:#e8f4f8'>{fmt(bt)}</td></tr>"
                f"<tr><td style='color:#7fb8d4'>Distância extra</td><td style='text-align:right;font-weight:700;color:#e8f4f8'>0m</td></tr>"
                f"</table></div>",
                unsafe_allow_html=True,
            )
        with o2:
            st.markdown(
                f"<div class='ob ob-hi'><div class='ob-title'>🗺️ Dividir entre 2</div>"
                f"<table style='width:100%;font-size:.86rem;border-spacing:0 5px'>"
                f"<tr><td style='color:#7fb8d4'>{bm[:14]}+{sm[:12]}</td><td></td></tr>"
                f"<tr><td style='color:#7fb8d4'>Total</td><td style='text-align:right;font-weight:700;color:#e8f4f8'>{fmt(tdiv)}</td></tr>"
                f"<tr><td style='color:#7fb8d4'>+Distância</td><td style='text-align:right;font-weight:700;color:#e8f4f8'>+{xdist}m</td></tr>"
                f"</table>"
                f"<div style='text-align:center;margin-top:12px'>"
                f"  <div style='font-size:.73rem;color:#7fb8d4;margin-bottom:2px'>Economia ao dividir</div>"
                f"  <div style='font-family:monospace;font-size:1.4rem;font-weight:800;color:#00c882'>+ {fmt(ediv)} 💚</div>"
                f"</div></div>",
                unsafe_allow_html=True,
            )

    st.markdown("---")

    # ── RANKING ────────────────────────────────────────────────────
    st.markdown("<div class='st'>🏆 Embaixadores de Economia do Bairro</div>", unsafe_allow_html=True)
    ranking = sorted(
        EMBAIXADORES + [{"nome":"Você 🎯","pts":st.session_state.pontos_usuario,"badge":"🟢"}],
        key=lambda x: x["pts"], reverse=True,
    )
    for i, emb in enumerate(ranking):
        dest = "border-color:rgba(0,200,130,.6);background:rgba(0,200,130,.07);" if emb["nome"]=="Você 🎯" else ""
        st.markdown(
            f"<div class='rc' style='{dest}'>"
            f"<div class='rp'>#{i+1}</div>"
            f"<div style='font-size:1.1rem'>{emb['badge']}</div>"
            f"<div class='rn'>{emb['nome']}</div>"
            f"<div class='rpt'>{emb['pts']:,} pts</div>"
            f"</div>",
            unsafe_allow_html=True,
        )


# ═══════════════════════════════════════════════════════════════════
#  VISÃO LOJISTA (B2B) — com st.tabs
# ═══════════════════════════════════════════════════════════════════
else:
    st.markdown("""
    <div class='hero hero-b2b'>
      <div class='hero-tag'>🏪 Lojista Parceiro · v3.0</div>
      <h1>BI, Estoque e Inteligência Competitiva</h1>
      <p>Lance promoções · Monitore o bairro · Gerencie estoque com dados reais</p>
    </div>""", unsafe_allow_html=True)

    n_of    = len(st.session_state.ofertas_ativas)
    n_val   = sum(1 for o in st.session_state.ofertas_ativas if o.get("validado"))
    t_alc   = sum(o.get("alcance",0) for o in st.session_state.ofertas_ativas)
    n_risco = sum(1 for e in ESTOQUE_DATA.values() if e["status"]=="risco")

    c1,c2,c3,c4 = st.columns(4)
    for col,(v,l,extra) in zip([c1,c2,c3,c4],[
        (str(n_of),"Ofertas ativas",""),
        (str(n_val),"Verificadas",""),
        (str(t_alc),"Alcance total hoje",""),
        (str(n_risco),"Alertas de estoque","mc-danger"),
    ]):
        col.markdown(f"<div class='mc {extra}'><div class='v'>{v}</div><div class='l'>{l}</div></div>",
                     unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ══ TABS ══════════════════════════════════════════════════════
    tab1, tab2, tab3 = st.tabs([
        "📣  Promoções & Alcance",
        "📊  Análise de Mercado",
        "📦  Gestão de Estoque",
    ])

    # ─────────────────────────────────────────────────────────────
    #  TAB 1 — PROMOÇÕES & ALCANCE
    # ─────────────────────────────────────────────────────────────
    with tab1:

        # ── Lançar Nova Oferta ─────────────────────────────────
        st.markdown("<div class='st'>📣 Lançar Nova Oferta</div>", unsafe_allow_html=True)
        st.markdown("<div class='fb'>", unsafe_allow_html=True)
        st.markdown("<div class='fb-title'>✏️ Configure o anúncio</div>", unsafe_allow_html=True)

        f1, f2 = st.columns(2)
        with f1:
            novo_prod = st.selectbox("Produto:", list(PRODUTOS_BASE.keys()),
                                     format_func=lambda x: f"{PRODUTOS_BASE[x]['emoji']} {x}", key="np")
            p_orig    = PRECOS_BASE[novo_prod][0]
            novo_preco = st.number_input("Preço promocional:", min_value=0.50,
                                         max_value=float(p_orig)*1.5,
                                         value=round(p_orig*0.92, 2), step=0.10, key="npr")
        with f2:
            nova_val  = st.selectbox("Validade:", ["Hoje, até 22h","Amanhã, dia todo",
                                                   "Este fim de semana","Próximos 3 dias"], key="nv")
            raio      = st.slider("Raio (m):", 200, 1000, 500, 50, key="raio")

        desc_pct    = round((p_orig - novo_preco)/p_orig*100, 1)
        alc_est     = int(raio*1.8 + random.randint(60,140))
        hora_atual  = datetime.now().strftime("%Hh%M")
        enovo       = PRODUTOS_BASE[novo_prod]["emoji"]
        pns         = f"{novo_preco:.2f}".replace(".",",")
        pos         = f"{p_orig:.2f}".replace(".",",")

        st.markdown(
            f"<div style='margin-top:10px;padding:14px;background:rgba(0,200,130,.06);"
            f"border:1px dashed rgba(0,200,130,.3);border-radius:11px'>"
            f"<div style='font-size:.7rem;color:#5a9ab8;text-transform:uppercase;letter-spacing:.1em;margin-bottom:9px'>Preview ao vivo</div>"
            f"<div style='display:flex;align-items:center;gap:14px'>"
            f"<div style='font-size:2rem'>{enovo}</div>"
            f"<div><div style='font-weight:700;color:#fff;font-size:.97rem'>{novo_prod}</div>"
            f"<div style='font-family:monospace;font-size:1.45rem;font-weight:800;color:#00c882'>R&#36;&nbsp;{pns}</div>"
            f"<div style='font-size:.76rem;color:#fca5a5'><s>R&#36;&nbsp;{pos}</s>"
            f"&nbsp;<span style='color:#00c882;font-weight:700'>{desc_pct:.1f}% OFF</span></div>"
            f"<div style='font-size:.73rem;color:#7fb8d4;margin-top:2px'>⏰ {nova_val} &nbsp;·&nbsp; 👁 ~{alc_est} visualizações</div>"
            f"</div></div></div>",
            unsafe_allow_html=True,
        )
        st.markdown("</div>", unsafe_allow_html=True)

        cb, _ = st.columns([1,3])
        with cb:
            if st.button("🚀 Publicar Oferta Agora", use_container_width=True):
                st.session_state.ofertas_ativas.append({
                    "produto":novo_prod,"preco":novo_preco,"validade":nova_val,
                    "lojista":"Mercado Boa Vista","emoji":enovo,
                    "validado":False,"alcance":alc_est,"ts":hora_atual,
                })
                st.balloons()
                st.success(
                    f"✅ Oferta publicada! {enovo} **{novo_prod}** por **{rr(novo_preco)}** "
                    f"está visível para **{alc_est} consumidores** num raio de {raio}m. "
                    f"Peça um cliente para validar com foto e eleve o Trust Score!"
                )

        st.markdown("---")

        # ── Alcance das Ofertas ────────────────────────────────
        st.markdown("<div class='st'>📈 Alcance das Ofertas Ativas</div>", unsafe_allow_html=True)

        if not st.session_state.ofertas_ativas:
            st.info("Nenhuma oferta ativa ainda.")
        else:
            sel_idx = st.selectbox(
                "Oferta:",
                range(len(st.session_state.ofertas_ativas)),
                format_func=lambda i: (
                    f"{st.session_state.ofertas_ativas[i]['emoji']} "
                    f"{st.session_state.ofertas_ativas[i]['produto']} — "
                    + rr(st.session_state.ofertas_ativas[i]['preco'])
                ),
                key="sel_of",
            )
            od      = st.session_state.ofertas_ativas[sel_idx]
            conv    = round(random.uniform(6.5,14.2), 1)
            vt      = od["validado"]
            vc, vl  = ("✅ Verificada","#00c882") if vt else ("⏳ Pendente","#facc15")

            r1,r2,r3 = st.columns(3)
            r1.markdown(f"<div class='mc'><div class='v'>{od['alcance']}</div><div class='l'>Visualizações</div></div>", unsafe_allow_html=True)
            r2.markdown(f"<div class='mc'><div class='v'>{conv}%</div><div class='l'>Taxa de conversão</div></div>", unsafe_allow_html=True)
            r3.markdown(f"<div class='mc'><div class='v' style='color:{vl};font-size:1.1rem'>{vc}</div><div class='l'>Status</div></div>", unsafe_allow_html=True)

            random.seed(sel_idx+7)
            st.area_chart(build_reach_df(od), use_container_width=True, height=200)

        st.markdown("---")

        # ── Alertas ────────────────────────────────────────────
        st.markdown("<div class='st'>🚨 Alertas de Mercado</div>", unsafe_allow_html=True)
        st.markdown("""
        <div class='alert-c'>
          <div class='alert-t'>⚠️ Perda de Conversão Detectada</div>
          <div class='alert-b'>Você perdeu <strong>12% de conversão</strong> em
          <strong>Café Torrado 500g</strong>. O concorrente <em>Mini Box Econômico</em>
          a 300m baixou o preço em <strong>R&#36;&nbsp;0,40</strong> às 09h15.</div>
          <div class='alert-i'>📉 Impacto estimado: -R&#36;&nbsp;280 em vendas hoje</div>
        </div>""", unsafe_allow_html=True)
        st.markdown("""
        <div class='warn-c'>
          <div class='warn-t'>⚡ Oportunidade: Ruptura no Concorrente</div>
          <div class='warn-b'><em>Atacado do Bairro</em> está sem
          <strong>Óleo de Soja 900ml</strong> desde às 11h00.
          Consumidores buscam alternativa num raio de 700m.</div>
        </div>""", unsafe_allow_html=True)

    # ─────────────────────────────────────────────────────────────
    #  TAB 2 — ANÁLISE DE MERCADO
    # ─────────────────────────────────────────────────────────────
    with tab2:

        # ── Tendências de Busca (Data-Driven, em tempo real) ───
        st.markdown("<div class='st'>🔍 Tendências de Busca no Bairro</div>", unsafe_allow_html=True)
        st.markdown("""
        <div class='info-c'>
          <div class='info-t'>Dados em tempo real</div>
          <div class='info-b'>Este gráfico se atualiza conforme os consumidores buscam produtos
          no app. Cada busca na Visão Consumidor incrementa o contador aqui. Use isso para
          decidir quais produtos impulsionar.</div>
        </div>""", unsafe_allow_html=True)

        busca_df = (
            pd.DataFrame.from_dict(
                st.session_state.search_counter, orient="index", columns=["Buscas"]
            )
            .sort_values("Buscas", ascending=False)
        )
        busca_df.index = [f"{PRODUTOS_BASE[p]['emoji']} {p[:22]}" for p in busca_df.index]

        col_bg, col_bi = st.columns([3,1])
        with col_bg:
            st.bar_chart(busca_df, use_container_width=True, height=280)
        with col_bi:
            top3 = busca_df.head(3)
            st.markdown("<div style='margin-top:8px'>", unsafe_allow_html=True)
            for rank,(idx,row) in enumerate(top3.iterrows()):
                medals = ["🥇","🥈","🥉"]
                st.markdown(
                    f"<div style='background:rgba(0,200,130,.08);border:1px solid rgba(0,200,130,.2);"
                    f"border-radius:10px;padding:10px 14px;margin-bottom:8px'>"
                    f"<div style='font-size:.7rem;color:#7fb8d4;text-transform:uppercase'>#{rank+1} mais buscado</div>"
                    f"<div style='font-weight:700;color:#e8f4f8;font-size:.88rem;margin-top:3px'>{medals[rank]} {idx}</div>"
                    f"<div style='font-family:monospace;color:#00c882;font-weight:700'>{int(row['Buscas'])} buscas</div>"
                    f"</div>",
                    unsafe_allow_html=True,
                )
            st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("---")

        # ── Performance de Marcas ──────────────────────────────
        st.markdown("<div class='st'>🏷️ Performance de Marcas por Produto</div>", unsafe_allow_html=True)
        st.markdown("""
        <div class='info-c'>
          <div class='info-t'>Como usar</div>
          <div class='info-b'>Compare vendas vs. margem de lucro por marca. Marcas com
          <strong>alta margem e baixa venda</strong> precisam de ação promocional.
          Marcas com <strong>alta venda e baixa margem</strong> são âncoras de tráfego.</div>
        </div>""", unsafe_allow_html=True)

        prod_marcas = st.selectbox(
            "Produto para análise de marcas:",
            list(MARCAS_DATA.keys()),
            format_func=lambda x: f"{PRODUTOS_BASE[x]['emoji']} {x}",
            key="pm",
        )
        md = MARCAS_DATA[prod_marcas]

        m1, m2 = st.columns(2)
        with m1:
            st.markdown("<div style='font-size:.78rem;color:#7fb8d4;text-transform:uppercase;letter-spacing:.08em;margin-bottom:6px'>📦 Volume de Vendas (unid/semana)</div>", unsafe_allow_html=True)
            df_v = pd.DataFrame({"Vendas":md["vendas"]}, index=md["marcas"])
            st.bar_chart(df_v, use_container_width=True, height=220)
        with m2:
            st.markdown("<div style='font-size:.78rem;color:#7fb8d4;text-transform:uppercase;letter-spacing:.08em;margin-bottom:6px'>💰 Margem de Lucro (%)</div>", unsafe_allow_html=True)
            df_m = pd.DataFrame({"Margem (%)":md["margem"]}, index=md["marcas"])
            st.bar_chart(df_m, use_container_width=True, height=220)

        # Tabela síntese com análise automática
        st.markdown("<div style='margin-top:6px;font-size:.78rem;color:#7fb8d4;text-transform:uppercase;letter-spacing:.08em;margin-bottom:8px'>📋 Síntese Estratégica</div>", unsafe_allow_html=True)
        rows_marca = []
        for marca, venda, margem in zip(md["marcas"],md["vendas"],md["margem"]):
            if venda >= max(md["vendas"])*0.7:
                status, rec = "🟢 Alto giro", "Manter estoque"
            elif margem >= max(md["margem"])*0.75:
                status, rec = "🟡 Alta margem", "Impulsionar com promoção"
            else:
                status, rec = "🔴 Baixo desempenho", "Avaliar substituição"
            rows_marca.append({"Marca":marca,"Vendas/sem":venda,
                                "Margem (%)":f"{margem}%","Status":status,"Recomendação":rec})
        st.dataframe(pd.DataFrame(rows_marca), use_container_width=True, hide_index=True)

        st.markdown("---")

        # ── KPIs Bairro ────────────────────────────────────────
        st.markdown("<div class='st'>📊 KPIs de Vendas vs. Procura do Bairro</div>", unsafe_allow_html=True)

        total_buscas = sum(st.session_state.search_counter.values())
        kpi_data = []
        for prod, cnt in sorted(st.session_state.search_counter.items(),
                                 key=lambda x: x[1], reverse=True)[:6]:
            e    = ESTOQUE_DATA[prod]
            giro = e["giro_dia"] * 7
            conv = round(giro / cnt * 100, 1) if cnt > 0 else 0
            rec  = min(100, int(cnt/total_buscas*100*5))
            kpi_data.append({
                "Produto": f"{PRODUTOS_BASE[prod]['emoji']} {prod[:22]}",
                "Buscas": cnt,
                "Vendas/semana": giro,
                "Conversão (%)": f"{conv}%",
                "Relevância": f"{rec}%",
            })
        st.dataframe(pd.DataFrame(kpi_data), use_container_width=True, hide_index=True)

        st.markdown("---")

        # ── Posicionamento de Preço ────────────────────────────
        st.markdown("<div class='st'>📈 Posicionamento de Preço vs. Concorrência</div>", unsafe_allow_html=True)
        cg1, cg2 = st.columns([3,1])
        with cg1:
            prod_b2b = st.selectbox("Produto:", list(PRODUTOS_BASE.keys()),
                                    format_func=lambda x: f"{PRODUTOS_BASE[x]['emoji']} {x}", key="pb2b")
        with cg2:
            periodo  = st.selectbox("Período:", ["14 dias","7 dias","30 dias"], key="per")
        n_dias = 7 if "7" in periodo else (30 if "30" in periodo else 14)
        hist   = build_history(prod_b2b)
        st.line_chart(hist.tail(n_dias).set_index("Data"), use_container_width=True)

        sub_b2b = DF[DF["Produto"]==prod_b2b].sort_values("Preco").reset_index(drop=True)
        sub_b2b["Curto"] = sub_b2b["Mercado"].str[:18]
        st.bar_chart(sub_b2b.set_index("Curto")[["Preco"]], use_container_width=True)
        tab = sub_b2b[["Mercado","Distancia","Timestamp"]].copy()
        tab.insert(1,"Preço", sub_b2b["Preco"].apply(lambda x: "R" + chr(36) + f" {x:.2f}"))
        tab.columns = ["Mercado","Preço","Distância","Atualização"]
        st.dataframe(tab, use_container_width=True, hide_index=True)

    # ─────────────────────────────────────────────────────────────
    #  TAB 3 — GESTÃO DE ESTOQUE
    # ─────────────────────────────────────────────────────────────
    with tab3:

        # ── KPIs de estoque ────────────────────────────────────
        ok_ct    = sum(1 for e in ESTOQUE_DATA.values() if e["status"]=="ok")
        warn_ct  = sum(1 for e in ESTOQUE_DATA.values() if e["status"]=="atencao")
        risk_ct  = sum(1 for e in ESTOQUE_DATA.values() if e["status"]=="risco")
        valor_est = sum(e["estoque"]*e["custo"] for e in ESTOQUE_DATA.values())

        s1,s2,s3,s4 = st.columns(4)
        s1.markdown(f"<div class='mc'><div class='v'>{ok_ct}</div><div class='l'>Itens em bom giro</div></div>",   unsafe_allow_html=True)
        s2.markdown(f"<div class='mc mc-warn'><div class='v'>{warn_ct}</div><div class='l'>Atenção</div></div>",  unsafe_allow_html=True)
        s3.markdown(f"<div class='mc mc-danger'><div class='v'>{risk_ct}</div><div class='l'>Risco de validade</div></div>", unsafe_allow_html=True)
        s4.markdown(f"<div class='mc'><div class='v'>{fmt(valor_est)}</div><div class='l'>Valor em estoque</div></div>", unsafe_allow_html=True)

        st.markdown("---")

        # ── Alertas de risco de vencimento ────────────────────
        st.markdown("<div class='st'>🚨 Alertas de Risco de Vencimento / Estoque Parado</div>", unsafe_allow_html=True)

        for prod, e in ESTOQUE_DATA.items():
            emoji = PRODUTOS_BASE[prod]["emoji"]
            dias_restantes = e["validade_dias"]
            dias_estoque   = round(e["estoque"] / e["giro_dia"], 1) if e["giro_dia"] > 0 else 99

            if e["status"] == "risco":
                st.markdown(
                    f"<div class='alert-c'>"
                    f"<div class='alert-t'>🔴 RISCO ALTO — {emoji} {prod}</div>"
                    f"<div class='alert-b'>"
                    f"Estoque atual: <strong>{e['estoque']} unidades</strong> · "
                    f"Giro: <strong>{e['giro_dia']} unid/dia</strong> · "
                    f"Validade em: <strong>{dias_restantes} dias</strong><br>"
                    f"⚠️ Com o giro atual, o estoque dura <strong>{dias_estoque} dias</strong> — "
                    f"<span style='color:#f87171;font-weight:700'>RISCO REAL DE PERDA POR VENCIMENTO.</span>"
                    f"</div>"
                    f"<div class='alert-i'>💡 Sugestão: Lance promoção relâmpago agora. "
                    f"Reduzir para {fmt(e['preco_venda']*0.82)} aumenta giro em ~40%.</div>"
                    f"</div>",
                    unsafe_allow_html=True,
                )
            elif e["status"] == "atencao":
                st.markdown(
                    f"<div class='warn-c'>"
                    f"<div class='warn-t'>🟡 ATENÇÃO — {emoji} {prod}</div>"
                    f"<div class='warn-b'>"
                    f"Estoque: <strong>{e['estoque']} unidades</strong> · "
                    f"Giro: <strong>{e['giro_dia']} unid/dia</strong> · "
                    f"Duração estimada: <strong>{dias_estoque} dias</strong><br>"
                    f"Monitore o giro nos próximos 2 dias. "
                    f"Considere pedido ao distribuidor caso o ritmo caia."
                    f"</div></div>",
                    unsafe_allow_html=True,
                )

        st.markdown("---")

        # ── Painel completo de estoque ─────────────────────────
        st.markdown("<div class='st'>📋 Painel de Giro e Status de Estoque</div>", unsafe_allow_html=True)

        filtro = st.radio("Filtrar por status:", ["Todos","✅ Bom Giro","⚠️ Atenção","🔴 Risco"],
                          horizontal=True, label_visibility="collapsed")

        for prod, e in ESTOQUE_DATA.items():
            emoji = PRODUTOS_BASE[prod]["emoji"]
            if filtro == "✅ Bom Giro"   and e["status"] != "ok":      continue
            if filtro == "⚠️ Atenção"   and e["status"] != "atencao": continue
            if filtro == "🔴 Risco"      and e["status"] != "risco":   continue

            dias_duracao = round(e["estoque"]/e["giro_dia"],1) if e["giro_dia"]>0 else 99
            cls_map = {"ok":"inv-ok","atencao":"inv-warn","risco":"inv-risk"}
            lbl_map = {"ok":"✅ BOM GIRO","atencao":"⚠️ ATENÇÃO","risco":"🔴 RISCO"}
            cls     = cls_map[e["status"]]
            lbl     = lbl_map[e["status"]]

            c_left, c_right = st.columns([3,1])
            with c_left:
                st.markdown(
                    f"<div class='{cls}'>"
                    f"<div class='inv-label'>{lbl}</div>"
                    f"<div class='inv-prod'>{emoji} {prod}</div>"
                    f"<div class='inv-meta'>"
                    f"Estoque: <strong>{e['estoque']} un</strong> &nbsp;·&nbsp; "
                    f"Giro: <strong>{e['giro_dia']} un/dia</strong> &nbsp;·&nbsp; "
                    f"Dura: <strong>{dias_duracao} dias</strong> &nbsp;·&nbsp; "
                    f"Validade: <strong>{e['validade_dias']} dias</strong>"
                    f"</div></div>",
                    unsafe_allow_html=True,
                )
            with c_right:
                margem_pct = round((e["preco_venda"]-e["custo"])/e["preco_venda"]*100,1)
                st.markdown(
                    f"<div class='{cls}' style='text-align:right'>"
                    f"<div class='inv-label'>Margem</div>"
                    f"<div class='inv-num'>{margem_pct}%</div>"
                    f"<div class='inv-meta'>PV: {fmt(e['preco_venda'])}<br>Custo: {fmt(e['custo'])}</div>"
                    f"</div>",
                    unsafe_allow_html=True,
                )

        st.markdown("---")

        # ── Sugestão de Pedido ao Distribuidor ────────────────
        st.markdown("<div class='st'>🚛 Sugestão de Pedido ao Distribuidor</div>", unsafe_allow_html=True)
        st.markdown("""
        <div class='info-c'>
          <div class='info-t'>Como é calculado</div>
          <div class='info-b'>O sistema usa o <strong>giro diário médio</strong> + margem de segurança
          de 3 dias + pedido mínimo do fornecedor para gerar a sugestão ideal.
          Fórmula: <em>Qtd Ideal = max(mínimo, (giro × 7) − estoque_atual)</em></div>
        </div>""", unsafe_allow_html=True)

        pedido_rows = []
        for prod, e in ESTOQUE_DATA.items():
            emoji    = PRODUTOS_BASE[prod]["emoji"]
            qtd_ideal = max(e["pedido_min"], int(e["giro_dia"]*7) - e["estoque"])
            custo_ped = qtd_ideal * e["custo"]
            urgencia  = "🔴 Urgente" if e["status"]=="risco" else ("🟡 Planejar" if e["status"]=="atencao" else "🟢 Normal")
            pedido_rows.append({
                "Produto":         f"{emoji} {prod}",
                "Estoque Atual":   e["estoque"],
                "Giro (un/dia)":   e["giro_dia"],
                "Qtd. Sugerida":   qtd_ideal,
                "Custo do Pedido": "R" + chr(36) + f" {custo_ped:.2f}",
                "Urgência":        urgencia,
            })

        df_pedido = pd.DataFrame(pedido_rows)
        st.dataframe(df_pedido, use_container_width=True, hide_index=True)

        total_pedido = sum(
            max(e["pedido_min"], int(e["giro_dia"]*7)-e["estoque"]) * e["custo"]
            for e in ESTOQUE_DATA.values()
        )
        st.markdown(
            f"<div class='succ-c'>"
            f"<div class='succ-t'>💼 Valor total do pedido sugerido: {fmt(total_pedido)}</div>"
            f"<div class='succ-b'>Pedido cobre aproximadamente <strong>7 dias</strong> de operação "
            f"para todos os itens. Priorize os marcados como <strong>🔴 Urgente</strong> "
            f"para evitar perda de vendas e vencimento de produtos.</div></div>",
            unsafe_allow_html=True,
        )

        st.markdown("---")

        # ── Histórico de Vendas ────────────────────────────────
        st.markdown("<div class='st'>📈 Histórico de Vendas por Produto</div>", unsafe_allow_html=True)
        prod_hist = st.selectbox("Produto:", list(PRODUTOS_BASE.keys()),
                                 format_func=lambda x: f"{PRODUTOS_BASE[x]['emoji']} {x}", key="ph")
        st.line_chart(build_vendas_historico(prod_hist), use_container_width=True, height=220)

        e_sel = ESTOQUE_DATA[prod_hist]
        h1,h2,h3 = st.columns(3)
        h1.markdown(f"<div class='mc'><div class='v'>{e_sel['giro_dia']}</div><div class='l'>Giro médio/dia</div></div>", unsafe_allow_html=True)
        h2.markdown(f"<div class='mc'><div class='v'>{e_sel['giro_dia']*7}</div><div class='l'>Projeção semanal</div></div>", unsafe_allow_html=True)
        h3.markdown(f"<div class='mc'><div class='v'>{round((e_sel['preco_venda']-e_sel['custo'])/e_sel['preco_venda']*100,1)}%</div><div class='l'>Margem atual</div></div>", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────
#  FOOTER
# ─────────────────────────────────────────────────────────────────
st.markdown("""
<div class='foot'>
  <span>4SAVR</span> · MVP v3.0 · BI & Inteligência de Estoque ·
  Dados fictícios para demonstração a parceiros e investidores<br>
  <em>"Onde sua economia fortalece o bairro."</em>
</div>""", unsafe_allow_html=True)
