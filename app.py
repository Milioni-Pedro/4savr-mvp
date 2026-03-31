import streamlit as st
import pandas as pd
import time
import random
from datetime import datetime, timedelta

# ─────────────────────────────────────────────────────────────────
#  CIFRÃO SEGURO — nunca usar $ literal em strings HTML do Streamlit
#  pois o parser LaTeX o interpreta como delimitador matemático.
# ─────────────────────────────────────────────────────────────────
def fmt(valor):
    """Formata valor monetário como HTML seguro: R&#36; X,XX"""
    return "R&#36;&nbsp;" + f"{valor:.2f}".replace(".", ",")

def fmt_py(valor):
    """Formata valor monetário para texto Python puro (não-HTML)."""
    return "R" + chr(36) + f" {valor:.2f}"

# ─────────────────────────────────────────────────────────────────
#  PAGE CONFIG
# ─────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="4SAVR v2.0 – Inteligência de Preços do Bairro",
    page_icon="💚",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────────
#  SESSION STATE — inicializa ofertas fictícias para não começar vazio
# ─────────────────────────────────────────────────────────────────
if "ofertas_ativas" not in st.session_state:
    st.session_state.ofertas_ativas = [
        {
            "produto":    "Café Torrado 500g",
            "preco":      13.90,
            "validade":   "Hoje, até 22h",
            "lojista":    "Mercado Boa Vista",
            "emoji":      "☕",
            "validado":   True,
            "alcance":    342,
            "ts":         "09h15",
        },
        {
            "produto":    "Leite Integral 1L",
            "preco":      3.99,
            "validade":   "Amanhã, dia todo",
            "lojista":    "Supermercado Central",
            "emoji":      "🥛",
            "validado":   True,
            "alcance":    218,
            "ts":         "10h02",
        },
        {
            "produto":    "Frango Congelado 1kg",
            "preco":      9.90,
            "validade":   "Este fim de semana",
            "lojista":    "Atacado do Bairro",
            "emoji":      "🍗",
            "validado":   False,
            "alcance":    97,
            "ts":         "11h30",
        },
    ]

if "precos_validados" not in st.session_state:
    # Guarda quais (produto, mercado) foram validados por foto de usuário
    st.session_state.precos_validados = {
        ("Leite Integral 1L",       "Supermercado Central"),
        ("Arroz Branco 5kg",        "Atacado do Bairro"),
        ("Café Torrado 500g",       "Mini Box Econômico"),
        ("Cerveja Lata 350ml",      "Mercado Família"),
        ("Óleo de Soja 900ml",      "Mercado Boa Vista"),
    }

if "pontos_usuario" not in st.session_state:
    st.session_state.pontos_usuario = 340

if "total_validacoes" not in st.session_state:
    st.session_state.total_validacoes = 7

# ─────────────────────────────────────────────────────────────────
#  CSS
# ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Sora:wght@300;400;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap');

  html, body, [class*="css"] { font-family:'Sora',sans-serif; }
  .stApp { background:linear-gradient(160deg,#020f1f 0%,#031a30 60%,#042440 100%); color:#e8f4f8; }
  [data-testid="stSidebar"] { background:linear-gradient(180deg,#010d1c,#021525); border-right:1px solid #0d3a5c; }
  [data-testid="stSidebar"] * { color:#c8e6f5 !important; }
  h1,h2,h3 { font-family:'Sora',sans-serif !important; }

  /* ── Hero ── */
  .hero { background:linear-gradient(135deg,#00c882,#00a86b,#007a50); border-radius:16px; padding:28px 36px; margin-bottom:24px; box-shadow:0 8px 32px rgba(0,200,130,.25); }
  .hero h1 { color:#fff !important; font-size:2rem !important; font-weight:800 !important; margin:0 0 6px !important; }
  .hero p  { color:rgba(255,255,255,.9) !important; font-size:1.05rem; margin:0; }
  .hero-b2b { background:linear-gradient(135deg,#0a2a4a,#0d3a5c,#042440) !important; border:1px solid rgba(0,200,130,.3); }
  .hero-tag { display:inline-block; background:rgba(255,255,255,.2); color:#fff !important; font-size:.72rem; font-weight:600; letter-spacing:.12em; text-transform:uppercase; padding:4px 12px; border-radius:20px; margin-bottom:12px; }

  /* ── Metric ── */
  .metric-card { background:linear-gradient(145deg,rgba(13,58,92,.6),rgba(4,36,64,.8)); border:1px solid rgba(0,200,130,.2); border-radius:14px; padding:20px 22px; text-align:center; backdrop-filter:blur(8px); transition:.2s; }
  .metric-card:hover { transform:translateY(-3px); box-shadow:0 12px 28px rgba(0,200,130,.15); }
  .metric-card .value { font-size:2rem; font-weight:800; color:#00c882; font-family:'JetBrains Mono',monospace; }
  .metric-card .label { font-size:.78rem; color:#7fb8d4; text-transform:uppercase; letter-spacing:.08em; margin-top:6px; }

  /* ── Section title ── */
  .section-title { font-size:1.1rem; font-weight:700; color:#00c882; text-transform:uppercase; letter-spacing:.1em; margin:28px 0 14px; padding-bottom:8px; border-bottom:1px solid rgba(0,200,130,.25); }

  /* ── Price boxes ── */
  .price-box { border-radius:10px; padding:14px 18px; margin-bottom:8px; }
  .price-box-best { background:rgba(0,200,130,.10); border:2px solid #00c882; }
  .price-box-norm { background:rgba(13,58,92,.40); border:1px solid rgba(13,58,92,.8); }
  .price-name-best { font-weight:700; font-size:.97rem; color:#00c882; }
  .price-name      { font-weight:700; font-size:.97rem; color:#e8f4f8; }
  .price-sub  { font-size:.78rem; color:#7fb8d4; margin-top:2px; }
  .price-num  { font-family:'JetBrains Mono',monospace; font-size:1.35rem; font-weight:800; text-align:right; }
  .price-num-best { color:#00c882; }
  .price-num-norm { color:#e8f4f8; }
  .badge-best { display:inline-block; background:#00c882; color:#010d1c; font-size:.65rem; font-weight:700; padding:3px 8px; border-radius:20px; text-transform:uppercase; letter-spacing:.08em; margin-left:6px; vertical-align:middle; }
  .badge-val  { display:inline-block; background:rgba(0,200,130,.15); border:1px solid #00c882; color:#00c882; font-size:.65rem; font-weight:700; padding:2px 7px; border-radius:20px; margin-left:6px; vertical-align:middle; }

  /* ── Offer cards ── */
  .offer-card { background:linear-gradient(135deg,rgba(0,200,130,.12),rgba(4,36,64,.9)); border:1px solid rgba(0,200,130,.4); border-radius:14px; padding:18px 22px; margin-bottom:12px; position:relative; }
  .offer-card-unval { border-color:rgba(250,204,21,.35); background:linear-gradient(135deg,rgba(250,204,21,.07),rgba(4,36,64,.9)); }
  .offer-emoji { font-size:2rem; float:left; margin-right:14px; margin-top:2px; }
  .offer-produto { font-size:1.1rem; font-weight:700; color:#fff; }
  .offer-lojista { font-size:.78rem; color:#7fb8d4; margin-top:2px; }
  .offer-preco  { font-family:'JetBrains Mono',monospace; font-size:1.6rem; font-weight:800; color:#00c882; margin-top:6px; }
  .offer-validade { font-size:.75rem; color:#7fb8d4; margin-top:4px; }
  .offer-badge-val { position:absolute; top:14px; right:16px; background:#00c882; color:#010d1c; font-size:.65rem; font-weight:700; padding:3px 10px; border-radius:20px; text-transform:uppercase; }
  .offer-badge-pen { position:absolute; top:14px; right:16px; background:rgba(250,204,21,.2); border:1px solid #facc15; color:#facc15; font-size:.65rem; font-weight:700; padding:3px 10px; border-radius:20px; }
  .offer-alcance  { font-size:.78rem; color:#a7f3d0; margin-top:6px; }

  /* ── Trust certificate ── */
  .trust-cert {
    background:linear-gradient(135deg,rgba(0,200,130,.15),rgba(0,80,50,.3));
    border:2px solid #00c882; border-radius:16px; padding:24px 28px; margin:14px 0;
    text-align:center;
  }
  .trust-cert .score { font-family:'JetBrains Mono',monospace; font-size:3rem; font-weight:800; color:#00c882; }
  .trust-cert .score-label { font-size:.8rem; color:#7fb8d4; text-transform:uppercase; letter-spacing:.12em; }
  .trust-cert .msg { color:#a7f3d0; font-size:.95rem; margin-top:10px; line-height:1.5; }
  .trust-cert .stars { font-size:1.4rem; letter-spacing:4px; margin:8px 0; }

  /* ── Alert / success / info cards ── */
  .alert-card { background:linear-gradient(135deg,rgba(220,38,38,.15),rgba(153,27,27,.2)); border:1px solid rgba(220,38,38,.5); border-left:4px solid #dc2626; border-radius:12px; padding:18px 22px; margin:12px 0; }
  .alert-card .alert-title { color:#fca5a5; font-weight:700; font-size:.85rem; text-transform:uppercase; letter-spacing:.1em; margin-bottom:8px; }
  .alert-card .alert-body  { color:#fecaca; font-size:.95rem; line-height:1.6; }
  .alert-card .alert-impact{ color:#f87171; font-weight:700; font-size:1.1rem; margin-top:8px; }
  .success-card { background:linear-gradient(135deg,rgba(0,200,130,.15),rgba(0,120,80,.2)); border:1px solid rgba(0,200,130,.5); border-left:4px solid #00c882; border-radius:12px; padding:18px 22px; margin:12px 0; }
  .success-card .s-title { color:#6ee7b7; font-weight:700; font-size:1rem; margin-bottom:6px; }
  .success-card .s-body  { color:#a7f3d0; font-size:.9rem; line-height:1.5; }
  .info-card { background:rgba(13,58,92,.5); border:1px solid rgba(0,200,130,.2); border-radius:12px; padding:16px 20px; margin:8px 0; }
  .info-card .i-title { color:#7fb8d4; font-size:.78rem; text-transform:uppercase; letter-spacing:.08em; margin-bottom:4px; }
  .info-card .i-body  { color:#e8f4f8; font-size:.95rem; font-weight:500; }

  /* ── Form container ── */
  .form-box { background:rgba(4,36,64,.7); border:1px solid rgba(0,200,130,.25); border-radius:14px; padding:22px 24px; margin:14px 0; }
  .form-box-title { color:#00c882; font-weight:700; font-size:1rem; margin-bottom:14px; }

  /* ── Upload option buttons ── */
  .upload-opt { background:rgba(13,58,92,.5); border:1px solid rgba(0,200,130,.25); border-radius:12px; padding:16px 18px; margin-bottom:10px; cursor:pointer; transition:.2s; }
  .upload-opt:hover { border-color:rgba(0,200,130,.6); background:rgba(0,200,130,.08); }
  .upload-opt .upt { font-weight:700; color:#e8f4f8; font-size:.95rem; }
  .upload-opt .upd { font-size:.78rem; color:#7fb8d4; margin-top:3px; }

  /* ── Optimizer box ── */
  .opt-box { background:linear-gradient(135deg,rgba(0,200,130,.1),rgba(4,36,64,.8)); border:1px solid rgba(0,200,130,.35); border-radius:14px; padding:22px 24px; margin:14px 0; }
  .opt-box-hi { border-color:rgba(0,200,130,.65) !important; }
  .opt-title { color:#00c882; font-weight:700; font-size:1rem; margin-bottom:12px; }

  /* ── Rank ── */
  .rank-card { display:flex; align-items:center; gap:14px; background:rgba(13,58,92,.4); border:1px solid rgba(13,58,92,.8); border-radius:10px; padding:12px 18px; margin-bottom:8px; }
  .rank-pos  { font-family:'JetBrains Mono',monospace; font-size:1.1rem; font-weight:700; color:#00c882; width:28px; }
  .rank-name { font-weight:600; color:#e8f4f8; flex:1; }
  .rank-pts  { font-family:'JetBrains Mono',monospace; font-size:.85rem; color:#7fb8d4; }

  /* ── Reach chart box ── */
  .reach-box { background:rgba(13,58,92,.5); border:1px solid rgba(0,200,130,.2); border-radius:12px; padding:16px 20px; margin:12px 0; }
  .reach-box-title { color:#7fb8d4; font-size:.78rem; text-transform:uppercase; letter-spacing:.08em; margin-bottom:12px; }

  /* ── Buttons ── */
  .stButton > button { background:linear-gradient(135deg,#00c882,#00a86b) !important; color:#010d1c !important; font-weight:700 !important; font-family:'Sora',sans-serif !important; border:none !important; border-radius:10px !important; padding:10px 22px !important; box-shadow:0 4px 16px rgba(0,200,130,.3) !important; transition:.2s !important; }
  .stButton > button:hover { transform:translateY(-2px) !important; box-shadow:0 8px 24px rgba(0,200,130,.45) !important; }
  .stSelectbox > div > div, .stMultiSelect > div > div, .stTextInput > div > div, .stNumberInput > div > div { background:rgba(13,58,92,.5) !important; border:1px solid rgba(0,200,130,.3) !important; border-radius:10px !important; }

  /* ── Footer ── */
  .footer-bar { text-align:center; padding:20px; color:#2a5a7a; font-size:.75rem; margin-top:40px; border-top:1px solid rgba(13,58,92,.5); }
  .footer-bar span { color:#00c882; }

  /* ── Live dot ── */
  .live-dot { display:inline-block; width:8px; height:8px; border-radius:50%; background:#00c882; box-shadow:0 0 8px #00c882; margin-right:6px; animation:pulse 1.5s infinite; }
  @keyframes pulse { 0%,100%{opacity:1}50%{opacity:.4} }

  /* ── Pill tags ── */
  .pill { display:inline-block; padding:2px 10px; border-radius:20px; font-size:.68rem; font-weight:700; letter-spacing:.06em; text-transform:uppercase; }
  .pill-green  { background:rgba(0,200,130,.15); color:#00c882; border:1px solid rgba(0,200,130,.4); }
  .pill-yellow { background:rgba(250,204,21,.12); color:#facc15; border:1px solid rgba(250,204,21,.4); }
  .pill-red    { background:rgba(220,38,38,.15);  color:#f87171; border:1px solid rgba(220,38,38,.4); }
</style>
""", unsafe_allow_html=True)

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

def build_df():
    rows = []
    mlist = list(MERCADOS.keys())
    for prod, precos in PRECOS_BASE.items():
        for i, merc in enumerate(mlist):
            rows.append({"Produto":prod,"Mercado":merc,"Distancia":MERCADOS[merc],
                         "Preco":precos[i],"Timestamp":TIMESTAMPS[i]})
    return pd.DataFrame(rows)

def build_history(produto):
    dias  = [datetime.today() - timedelta(days=i) for i in range(13,-1,-1)]
    base  = PRECOS_BASE[produto][0]
    media = sum(PRECOS_BASE[produto]) / len(PRECOS_BASE[produto])
    random.seed(42)
    return pd.DataFrame({
        "Data":           [d.strftime("%d/%m") for d in dias],
        "Seu Mercado":    [round(base +random.uniform(-.3,.4),2) for _ in dias],
        "Media do Bairro":[round(media+random.uniform(-.15,.15),2) for _ in dias],
    })

def build_reach_df(oferta):
    """Simula acumulação de visualizações ao longo do dia."""
    horas = [f"{h:02d}h" for h in range(8,23)]
    alcance_max = oferta.get("alcance", 100)
    vals = []
    acumulado = 0
    for h in range(len(horas)):
        pico = 1 if (h in [3,4,5,10,11]) else 0   # picos às 11h, 12h, 13h, 18h, 19h
        incremento = random.randint(8+pico*25, 20+pico*60)
        acumulado  = min(acumulado + incremento, alcance_max)
        vals.append(acumulado)
    return pd.DataFrame({"Hora": horas, "Visualizações": vals}).set_index("Hora")

DF = build_df()

# ─────────────────────────────────────────────────────────────────
#  SIDEBAR
# ─────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center;padding:16px 0 24px'>
      <div style='font-size:2.4rem;margin-bottom:4px'>💚</div>
      <div style='font-size:1.4rem;font-weight:800;color:#00c882;letter-spacing:.05em'>4SAVR</div>
      <div style='font-size:.72rem;color:#5a9ab8;letter-spacing:.12em;text-transform:uppercase'>
        For Saver · MVP v2.0
      </div>
    </div>""", unsafe_allow_html=True)

    st.markdown("---")
    visao = st.radio("Visão:", ["👤  Consumidor (B2C)","🏪  Lojista Parceiro (B2B)"],
                     label_visibility="collapsed")
    st.markdown("---")

    n_ofertas = len(st.session_state.ofertas_ativas)
    n_val     = len(st.session_state.precos_validados)

    st.markdown(f"""
    <div style='padding:12px;background:rgba(0,200,130,.08);border-radius:10px;border:1px solid rgba(0,200,130,.2);margin-bottom:10px'>
      <div style='font-size:.72rem;color:#5a9ab8;text-transform:uppercase;letter-spacing:.1em;margin-bottom:6px'>Bairro Ativo</div>
      <div style='color:#00c882;font-weight:700;font-size:.95rem'>📍 Bairro Boa Vista</div>
      <div style='color:#7fb8d4;font-size:.78rem;margin-top:2px'>Curitiba – PR</div>
    </div>
    <div style='padding:12px;background:rgba(13,58,92,.4);border-radius:10px;margin-bottom:10px'>
      <div style='font-size:.72rem;color:#5a9ab8;text-transform:uppercase;letter-spacing:.1em;margin-bottom:8px'>Status da Rede</div>
      <div style='display:flex;align-items:center;gap:6px;margin-bottom:4px'>
        <div class='live-dot'></div>
        <span style='color:#e8f4f8;font-size:.85rem'>5 mercados online</span>
      </div>
      <div style='color:#7fb8d4;font-size:.75rem'>Última sync: agora mesmo</div>
    </div>
    <div style='padding:12px;background:rgba(13,58,92,.4);border-radius:10px'>
      <div style='font-size:.72rem;color:#5a9ab8;text-transform:uppercase;letter-spacing:.1em;margin-bottom:8px'>Atividade em Tempo Real</div>
      <div style='display:flex;justify-content:space-between;margin-bottom:6px'>
        <span style='color:#7fb8d4;font-size:.8rem'>🔥 Ofertas ativas</span>
        <span style='color:#00c882;font-weight:700;font-family:monospace'>{n_ofertas}</span>
      </div>
      <div style='display:flex;justify-content:space-between;margin-bottom:6px'>
        <span style='color:#7fb8d4;font-size:.8rem'>✅ Preços validados</span>
        <span style='color:#00c882;font-weight:700;font-family:monospace'>{n_val}</span>
      </div>
      <div style='display:flex;justify-content:space-between'>
        <span style='color:#7fb8d4;font-size:.8rem'>⭐ Seus pontos</span>
        <span style='color:#00c882;font-weight:700;font-family:monospace'>{st.session_state.pontos_usuario}</span>
      </div>
    </div>
    <div style='margin-top:20px;text-align:center;font-size:.78rem;color:#2a5a7a;font-style:italic;line-height:1.5'>
      "Onde sua economia<br>fortalece o bairro."
    </div>""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════
#  VISÃO CONSUMIDOR (B2C)
# ═══════════════════════════════════════════════════════════════════
if "Consumidor" in visao:

    st.markdown("""
    <div class='hero'>
      <div class='hero-tag'>🛒 Modo Consumidor · v2.0</div>
      <h1>Economize no seu bairro, hoje</h1>
      <p>Preços em tempo real · Ofertas validadas pela comunidade · Reputação que rende prêmios</p>
    </div>""", unsafe_allow_html=True)

    c1,c2,c3,c4 = st.columns(4)
    for col,(val,lbl) in zip([c1,c2,c3,c4],[
        ("18,70","Economia média/semana"),
        (str(len(st.session_state.ofertas_ativas)),"Ofertas ativas agora"),
        (str(st.session_state.pontos_usuario),"Seus pontos de reputação"),
        (str(st.session_state.total_validacoes),"Validações enviadas"),
    ]):
        col.markdown(f"<div class='metric-card'><div class='value'>{val}</div><div class='label'>{lbl}</div></div>",
                     unsafe_allow_html=True)

    # ── 🔥 OFERTAS DIRETAS DO LOJISTA ─────────────────────────────
    st.markdown("<div class='section-title'>🔥 Ofertas Diretas do Lojista</div>", unsafe_allow_html=True)
    st.markdown("""
    <div class='info-card'>
      <div class='i-title'>Como funciona</div>
      <div class='i-body'>Lojistas parceiros publicam ofertas diretamente no app. As marcadas com
      ✅ <strong>Verificado</strong> foram confirmadas por fotos da comunidade e têm
      <strong>Trust Score alto</strong>.</div>
    </div>""", unsafe_allow_html=True)

    if not st.session_state.ofertas_ativas:
        st.info("Nenhuma oferta ativa no momento. Volte em breve!")
    else:
        for i, oferta in enumerate(st.session_state.ofertas_ativas):
            val    = oferta.get("validado", False)
            cls    = "offer-card" if val else "offer-card offer-card-unval"
            badge  = "<div class='offer-badge-val'>✅ Verificado</div>" if val else "<div class='offer-badge-pen'>⏳ Pendente</div>"
            preco_h = fmt(oferta["preco"])

            st.markdown(
                f"<div class='{cls}'>{badge}"
                f"<div style='overflow:hidden'>"
                f"  <div class='offer-emoji'>{oferta['emoji']}</div>"
                f"  <div>"
                f"    <div class='offer-produto'>{oferta['produto']}</div>"
                f"    <div class='offer-lojista'>📍 {oferta['lojista']} · publicado às {oferta.get('ts','—')}</div>"
                f"    <div class='offer-preco'>{preco_h}</div>"
                f"    <div class='offer-validade'>⏰ Válido: {oferta['validade']}</div>"
                f"    <div class='offer-alcance'>👁 {oferta['alcance']} pessoas viram esta oferta</div>"
                f"  </div>"
                f"</div></div>",
                unsafe_allow_html=True,
            )

            # Botão para validar oferta não verificada
            if not val:
                col_btn, _ = st.columns([1, 3])
                with col_btn:
                    if st.button(f"📸 Validar esta oferta", key=f"val_oferta_{i}"):
                        st.session_state.ofertas_ativas[i]["validado"] = True
                        st.session_state.pontos_usuario += 30
                        st.session_state.total_validacoes += 1
                        st.balloons()
                        st.success("✅ Oferta validada! +30 pontos de reputação creditados. Obrigado por fortalecer o bairro!")
                        st.rerun()

    st.markdown("---")

    # ── COMPARADOR DE PREÇOS ───────────────────────────────────────
    st.markdown("<div class='section-title'>🔍 Comparador de Preços</div>", unsafe_allow_html=True)

    col_sel, col_info = st.columns([2,1])
    with col_sel:
        produto_sel = st.selectbox(
            "Produto:",
            list(PRODUTOS_BASE.keys()),
            format_func=lambda x: f"{PRODUTOS_BASE[x]['emoji']}  {x}",
        )
    with col_info:
        p = PRODUTOS_BASE[produto_sel]
        st.markdown(
            f"<div class='info-card' style='margin-top:28px'>"
            f"<div class='i-title'>Categoria · Unidade</div>"
            f"<div class='i-body'>{p['categoria']} · {p['unidade']}</div></div>",
            unsafe_allow_html=True,
        )

    sub         = DF[DF["Produto"]==produto_sel].sort_values("Preco").reset_index(drop=True)
    menor_preco = sub["Preco"].min()
    maior_preco = sub["Preco"].max()
    economia_max = round(maior_preco - menor_preco, 2)

    for _, row in sub.iterrows():
        best       = row["Preco"] == menor_preco
        validado   = (produto_sel, row["Mercado"]) in st.session_state.precos_validados
        box_cls    = "price-box price-box-best" if best else "price-box price-box-norm"
        nm_cls     = "price-name-best" if best else "price-name"
        pr_cls     = "price-num price-num-best" if best else "price-num price-num-norm"
        badge_best = "<span class='badge-best'>Melhor Preço</span>" if best else ""
        badge_val  = "<span class='badge-val'>✅ Verificado</span>" if validado else ""
        preco_html = fmt(row["Preco"])

        st.markdown(
            f"<div class='{box_cls}'>"
            f"  <div style='display:flex;justify-content:space-between;align-items:center'>"
            f"    <div>"
            f"      <div class='{nm_cls}'>{row['Mercado']} {badge_best} {badge_val}</div>"
            f"      <div class='price-sub'>📍 {row['Distancia']} &nbsp;⏱ {row['Timestamp']}</div>"
            f"    </div>"
            f"    <div class='{pr_cls}'>{preco_html}</div>"
            f"  </div>"
            f"</div>",
            unsafe_allow_html=True,
        )

    if economia_max > 0:
        st.markdown(
            f"<div class='success-card'>"
            f"<div class='s-title'>💡 Você pode economizar {fmt(economia_max)} neste item</div>"
            f"<div class='s-body'>Comprando no <strong>{sub.iloc[0]['Mercado']}</strong> em vez do mais caro, "
            f"você economiza <strong>{fmt(economia_max)}</strong> por unidade — "
            f"equivale a <strong>{fmt(economia_max*4)}</strong> por mês comprando 4 vezes.</div>"
            f"</div>",
            unsafe_allow_html=True,
        )

    st.markdown("---")

    # ── VALIDAÇÃO MULTICANAL + TRUST SCORE ────────────────────────
    st.markdown("<div class='section-title'>📸 Validação Multicanal de Preços</div>", unsafe_allow_html=True)
    st.markdown("""
    <div class='info-card'>
      <div class='i-title'>Crowdsourcing de Confiança</div>
      <div class='i-body'>Suas fotos validam preços para toda a comunidade. Escolha o tipo de envio
      abaixo, simule o upload e ganhe pontos de reputação + Trust Score oficial.</div>
    </div>""", unsafe_allow_html=True)

    tipo_upload = st.radio(
        "Tipo de envio:",
        ["🧾  Foto da Nota Fiscal (NF) – Leitura de preço de compra",
         "🏷️  Foto da Gôndola / Anúncio Físico – Validação de promoção"],
        label_visibility="collapsed",
    )

    col_up1, col_up2 = st.columns([1,1])
    with col_up1:
        produto_val = st.selectbox(
            "Produto a validar:",
            list(PRODUTOS_BASE.keys()),
            format_func=lambda x: f"{PRODUTOS_BASE[x]['emoji']} {x}",
            key="prod_val",
        )
        mercado_val = st.selectbox("Mercado:", list(MERCADOS.keys()), key="merc_val")

    with col_up2:
        st.markdown("""
        <div class='upload-opt'>
          <div class='upt'>📤 Simular Envio de Imagem</div>
          <div class='upd'>No app real: câmera abre automaticamente com geolocalização ativada</div>
        </div>""", unsafe_allow_html=True)

    col_enviar, _ = st.columns([1,3])
    with col_enviar:
        tipo_label = "NF" if "Nota Fiscal" in tipo_upload else "Gôndola"
        if st.button(f"📤 Simular Envio de Foto ({tipo_label})", use_container_width=True):
            with st.spinner("🤖 Analisando imagem com IA..."):
                time.sleep(0.5)
                prog = st.progress(0)
                etapas = ["Detectando produto…","Lendo preço…","Validando GPS…","Confirmando timestamp…","Gerando certificado…"]
                for pct, etapa in zip(range(0,101,20), etapas):
                    time.sleep(0.3)
                    prog.progress(pct, text=etapa)
                time.sleep(0.4)
                prog.empty()

            # Adiciona à lista de preços validados
            chave = (produto_val, mercado_val)
            st.session_state.precos_validados.add(chave)
            st.session_state.pontos_usuario += 50
            st.session_state.total_validacoes += 1

            st.balloons()
            st.success(f"✅ Você fez a comunidade mais forte! +50 pontos creditados.")

            # Certificado de confiança
            tipo_txt = "Nota Fiscal" if "Nota Fiscal" in tipo_upload else "Foto de Gôndola"
            st.markdown(
                f"<div class='trust-cert'>"
                f"  <div class='score-label'>Trust Score — {tipo_txt}</div>"
                f"  <div class='stars'>⭐⭐⭐⭐⭐</div>"
                f"  <div class='score'>9.8<span style='font-size:1.2rem;color:#7fb8d4'>/10</span></div>"
                f"  <div class='msg'>"
                f"    Foto validada via <strong>GPS + Timestamp</strong>.<br>"
                f"    O preço de <strong>{fmt(PRECOS_BASE[produto_val][list(MERCADOS.keys()).index(mercado_val)])}</strong>"
                f"    no <strong>{mercado_val}</strong>"
                f"    agora é <strong>oficial para todo o bairro!</strong> 🎉"
                f"  </div>"
                f"</div>",
                unsafe_allow_html=True,
            )

    st.markdown("---")

    # ── OTIMIZADOR DE CESTA ────────────────────────────────────────
    st.markdown("<div class='section-title'>🧺 Otimizador de Cesta</div>", unsafe_allow_html=True)
    itens_sel = st.multiselect(
        "Produtos da cesta:",
        list(PRODUTOS_BASE.keys()),
        default=list(PRODUTOS_BASE.keys())[:3],
        format_func=lambda x: f"{PRODUTOS_BASE[x]['emoji']} {x}",
        max_selections=5,
    )

    if itens_sel:
        mlist  = list(MERCADOS.keys())
        totais = sorted(
            [(m, sum(PRECOS_BASE[p][i] for p in itens_sel)) for i,m in enumerate(mlist)],
            key=lambda x: x[1],
        )
        melhor_m, melhor_t = totais[0]
        segundo_m, _       = totais[1]
        mid     = max(len(itens_sel)//2, 1)
        idx_a   = mlist.index(melhor_m)
        idx_b   = mlist.index(segundo_m)
        total_div    = (sum(PRECOS_BASE[p][idx_a] for p in itens_sel[:mid])
                      + sum(PRECOS_BASE[p][idx_b] for p in itens_sel[mid:]))
        economia_div = max(round(melhor_t - total_div, 2), 0)
        extra_dist   = random.randint(300,600)

        col1,col2 = st.columns(2)
        with col1:
            st.markdown(
                f"<div class='opt-box'><div class='opt-title'>🏪 Estratégia 1 — Compra única</div>"
                f"<table style='width:100%;color:#e8f4f8;font-size:.88rem;border-spacing:0 6px'>"
                f"<tr><td style='color:#7fb8d4'>Melhor mercado</td><td style='text-align:right;font-weight:700'>{melhor_m[:22]}</td></tr>"
                f"<tr><td style='color:#7fb8d4'>Total estimado</td><td style='text-align:right;font-weight:700'>{fmt(melhor_t)}</td></tr>"
                f"<tr><td style='color:#7fb8d4'>Distância extra</td><td style='text-align:right;font-weight:700'>0m</td></tr>"
                f"</table></div>",
                unsafe_allow_html=True,
            )
        with col2:
            st.markdown(
                f"<div class='opt-box opt-box-hi'><div class='opt-title'>🗺️ Estratégia 2 — Dividir entre 2</div>"
                f"<table style='width:100%;color:#e8f4f8;font-size:.88rem;border-spacing:0 6px'>"
                f"<tr><td style='color:#7fb8d4'>{melhor_m[:14]}+{segundo_m[:12]}</td><td></td></tr>"
                f"<tr><td style='color:#7fb8d4'>Total estimado</td><td style='text-align:right;font-weight:700'>{fmt(total_div)}</td></tr>"
                f"<tr><td style='color:#7fb8d4'>Distância extra</td><td style='text-align:right;font-weight:700'>+{extra_dist}m</td></tr>"
                f"</table>"
                f"<div style='text-align:center;margin-top:14px'>"
                f"  <div style='font-size:.75rem;color:#7fb8d4;margin-bottom:2px'>Economia ao dividir</div>"
                f"  <div style='font-family:monospace;font-size:1.5rem;font-weight:800;color:#00c882'>+ {fmt(economia_div)} 💚</div>"
                f"</div></div>",
                unsafe_allow_html=True,
            )

    st.markdown("---")

    # ── RANKING ────────────────────────────────────────────────────
    st.markdown("<div class='section-title'>🏆 Embaixadores de Economia do Bairro</div>", unsafe_allow_html=True)
    # Injeta o usuário atual no ranking
    ranking = sorted(
        EMBAIXADORES + [{"nome":"Você 🎯","pts":st.session_state.pontos_usuario,"badge":"🟢"}],
        key=lambda x: x["pts"], reverse=True,
    )
    for i, emb in enumerate(ranking):
        pts_fmt = f"{emb['pts']:,}".replace(",",".")
        destaque = "border-color:rgba(0,200,130,.6);background:rgba(0,200,130,.08);" if emb["nome"]=="Você 🎯" else ""
        st.markdown(
            f"<div class='rank-card' style='{destaque}'>"
            f"<div class='rank-pos'>#{i+1}</div>"
            f"<div style='font-size:1.2rem'>{emb['badge']}</div>"
            f"<div class='rank-name'>{emb['nome']}</div>"
            f"<div class='rank-pts'>{pts_fmt} pts</div>"
            f"</div>",
            unsafe_allow_html=True,
        )


# ═══════════════════════════════════════════════════════════════════
#  VISÃO LOJISTA (B2B)
# ═══════════════════════════════════════════════════════════════════
else:
    st.markdown("""
    <div class='hero hero-b2b'>
      <div class='hero-tag'>🏪 Modo Lojista Parceiro · v2.0</div>
      <h1>Inteligência Competitiva em Tempo Real</h1>
      <p>Lance ofertas, monitore o alcance e reaja à concorrência com dados do bairro.</p>
    </div>""", unsafe_allow_html=True)

    n_of  = len(st.session_state.ofertas_ativas)
    n_val = sum(1 for o in st.session_state.ofertas_ativas if o.get("validado"))
    total_alcance = sum(o.get("alcance",0) for o in st.session_state.ofertas_ativas)

    c1,c2,c3,c4 = st.columns(4)
    for col,(val,lbl) in zip([c1,c2,c3,c4],[
        (str(n_of),"Ofertas ativas"),
        (str(n_val),"Ofertas verificadas"),
        (str(total_alcance),"Alcance total hoje"),
        (str(len(st.session_state.precos_validados)),"Preços validados bairro"),
    ]):
        col.markdown(f"<div class='metric-card'><div class='value'>{val}</div><div class='label'>{lbl}</div></div>",
                     unsafe_allow_html=True)

    st.markdown("---")

    # ── 📣 LANÇAR NOVA OFERTA ─────────────────────────────────────
    st.markdown("<div class='section-title'>📣 Lançar Nova Oferta / Anúncio</div>", unsafe_allow_html=True)
    st.markdown("""
    <div class='info-card' style='margin-bottom:16px'>
      <div class='i-title'>Como funciona</div>
      <div class='i-body'>Publique uma oferta aqui e ela aparece <strong>imediatamente</strong>
      na seção "🔥 Ofertas Diretas do Lojista" do Consumidor. A comunidade pode validá-la
      com foto para elevar o Trust Score.</div>
    </div>""", unsafe_allow_html=True)

    st.markdown("<div class='form-box'>", unsafe_allow_html=True)
    st.markdown("<div class='form-box-title'>✏️ Preencha os dados da oferta</div>", unsafe_allow_html=True)

    col_f1, col_f2 = st.columns(2)
    with col_f1:
        novo_produto = st.selectbox(
            "Produto em oferta:",
            list(PRODUTOS_BASE.keys()),
            format_func=lambda x: f"{PRODUTOS_BASE[x]['emoji']} {x}",
            key="novo_prod",
        )
        preco_orig   = PRECOS_BASE[novo_produto][0]
        novo_preco   = st.number_input(
            "Preço promocional:",
            min_value=0.50, max_value=float(preco_orig)*1.5,
            value=round(preco_orig*0.92, 2), step=0.10, key="novo_preco",
        )
    with col_f2:
        nova_validade = st.selectbox(
            "Validade:",
            ["Hoje, até 22h","Amanhã, dia todo","Este fim de semana","Próximos 3 dias"],
            key="nova_val",
        )
        raio_alcance = st.slider("Raio de alcance (m):", 200, 1000, 500, 50, key="raio")

    desconto    = round((preco_orig - novo_preco)/preco_orig*100, 1)
    alcance_est = int(raio_alcance * 1.8 + random.randint(60, 140))
    hora_atual  = datetime.now().strftime("%Hh%M")

    # Preview ao vivo
    preco_novo_str  = f"{novo_preco:.2f}".replace(".",",")
    preco_orig_str  = f"{preco_orig:.2f}".replace(".",",")
    emoji_novo      = PRODUTOS_BASE[novo_produto]["emoji"]

    st.markdown(
        f"<div style='margin-top:10px;padding:16px;background:rgba(0,200,130,.06);"
        f"border:1px dashed rgba(0,200,130,.3);border-radius:12px'>"
        f"<div style='font-size:.72rem;color:#5a9ab8;text-transform:uppercase;letter-spacing:.1em;margin-bottom:10px'>Preview do Anúncio (ao vivo)</div>"
        f"<div style='display:flex;align-items:center;gap:14px'>"
        f"  <div style='font-size:2.2rem'>{emoji_novo}</div>"
        f"  <div>"
        f"    <div style='font-weight:700;color:#fff;font-size:1rem'>{novo_produto}</div>"
        f"    <div style='font-family:monospace;font-size:1.5rem;font-weight:800;color:#00c882'>R&#36;&nbsp;{preco_novo_str}</div>"
        f"    <div style='font-size:.78rem;color:#fca5a5'><s>R&#36;&nbsp;{preco_orig_str}</s>"
        f"    &nbsp;<span style='color:#00c882;font-weight:700'>{desconto:.1f}% OFF</span></div>"
        f"    <div style='font-size:.75rem;color:#7fb8d4;margin-top:2px'>⏰ {nova_validade} &nbsp;·&nbsp; 👁 Est. {alcance_est} visualizações</div>"
        f"  </div>"
        f"</div></div>",
        unsafe_allow_html=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)

    col_pub, _ = st.columns([1,3])
    with col_pub:
        if st.button("🚀  Publicar Oferta Agora", use_container_width=True):
            nova_oferta = {
                "produto":  novo_produto,
                "preco":    novo_preco,
                "validade": nova_validade,
                "lojista":  "Mercado Boa Vista",
                "emoji":    PRODUTOS_BASE[novo_produto]["emoji"],
                "validado": False,
                "alcance":  alcance_est,
                "ts":       hora_atual,
            }
            st.session_state.ofertas_ativas.append(nova_oferta)
            st.balloons()
            st.success(
                f"✅ Oferta publicada! {emoji_novo} **{novo_produto}** por "
                f"**R" + chr(36) + f" {novo_preco:.2f}** está visível para "
                f"**{alcance_est} consumidores** num raio de {raio_alcance}m. "
                f"Peça a um cliente para validar com foto e eleve o Trust Score! 💚"
            )

    st.markdown("---")

    # ── 📊 ALCANCE DAS OFERTAS ATIVAS ─────────────────────────────
    st.markdown("<div class='section-title'>📊 Alcance das Ofertas em Tempo Real</div>", unsafe_allow_html=True)

    if not st.session_state.ofertas_ativas:
        st.info("Lance uma oferta acima para ver o gráfico de alcance.")
    else:
        oferta_sel_idx = st.selectbox(
            "Selecione a oferta para detalhar:",
            range(len(st.session_state.ofertas_ativas)),
            format_func=lambda i: (
                f"{st.session_state.ofertas_ativas[i]['emoji']} "
                f"{st.session_state.ofertas_ativas[i]['produto']} — "
                f"R" + chr(36) + f" {st.session_state.ofertas_ativas[i]['preco']:.2f}"
            ),
            key="oferta_detalhe",
        )
        oferta_detalhe = st.session_state.ofertas_ativas[oferta_sel_idx]

        col_r1, col_r2, col_r3 = st.columns(3)
        val_txt  = "✅ Verificada" if oferta_detalhe["validado"] else "⏳ Pendente"
        val_cor  = "#00c882"       if oferta_detalhe["validado"] else "#facc15"
        conversao = round(random.uniform(6.5, 14.2), 1)

        col_r1.markdown(f"<div class='metric-card'><div class='value'>{oferta_detalhe['alcance']}</div><div class='label'>Visualizações totais</div></div>", unsafe_allow_html=True)
        col_r2.markdown(f"<div class='metric-card'><div class='value'>{conversao}%</div><div class='label'>Taxa de conversão</div></div>", unsafe_allow_html=True)
        col_r3.markdown(f"<div class='metric-card'><div class='value' style='color:{val_cor};font-size:1.2rem'>{val_txt}</div><div class='label'>Status da oferta</div></div>", unsafe_allow_html=True)

        random.seed(oferta_sel_idx + 7)
        reach_df = build_reach_df(oferta_detalhe)
        st.markdown("<div class='reach-box'><div class='reach-box-title'>📈 Curva de Visualizações por Hora (simulado)</div>", unsafe_allow_html=True)
        st.area_chart(reach_df, use_container_width=True, height=220)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("---")

    # ── 🚨 ALERTAS DE MERCADO ──────────────────────────────────────
    st.markdown("<div class='section-title'>🚨 Alertas de Mercado</div>", unsafe_allow_html=True)
    st.markdown("""
    <div class='alert-card'>
      <div class='alert-title'>⚠️ Perda de Conversão Detectada</div>
      <div class='alert-body'>Você perdeu <strong>12% de conversão</strong> no item
      <strong>Café Torrado 500g</strong> hoje. O concorrente <em>Mini Box Econômico</em>
      a <strong>300m</strong> baixou o preço em <strong>R&#36;&nbsp;0,40</strong> às 09h15.</div>
      <div class='alert-impact'>📉 Impacto estimado: -R&#36;&nbsp;280 em vendas hoje</div>
    </div>""", unsafe_allow_html=True)
    st.markdown("""
    <div class='alert-card' style='border-left-color:#f59e0b;background:linear-gradient(135deg,rgba(245,158,11,.1),rgba(120,77,5,.15))'>
      <div class='alert-title' style='color:#fcd34d'>⚡ Oportunidade: Ruptura de Estoque no Concorrente</div>
      <div class='alert-body' style='color:#fef3c7'><em>Atacado do Bairro</em> está sem
      <strong>Óleo de Soja 900ml</strong> desde às 11h00. Consumidores buscam alternativa num raio de 700m.</div>
      <div class='alert-impact' style='color:#fbbf24'>📈 Oportunidade de +R&#36;&nbsp;190 em vendas extras</div>
    </div>""", unsafe_allow_html=True)

    st.markdown("---")

    # ── 📊 DASHBOARD DE PREÇOS ─────────────────────────────────────
    st.markdown("<div class='section-title'>📊 Posicionamento de Preço vs. Bairro</div>", unsafe_allow_html=True)

    col_g1, col_g2 = st.columns([3,1])
    with col_g1:
        produto_b2b = st.selectbox(
            "Produto:",
            list(PRODUTOS_BASE.keys()),
            format_func=lambda x: f"{PRODUTOS_BASE[x]['emoji']} {x}",
            key="b2b_prod",
        )
    with col_g2:
        periodo = st.selectbox("Período:", ["14 dias","7 dias","30 dias"], key="periodo")

    hist = build_history(produto_b2b)
    n    = 7 if "7" in periodo else (30 if "30" in periodo else 14)
    st.line_chart(hist.tail(n).set_index("Data"), use_container_width=True)

    sub_b2b = DF[DF["Produto"]==produto_b2b].sort_values("Preco").reset_index(drop=True)
    sub_b2b["Mercado Curto"] = sub_b2b["Mercado"].str[:18]
    st.bar_chart(sub_b2b.set_index("Mercado Curto")[["Preco"]], use_container_width=True)

    tabela = sub_b2b[["Mercado","Distancia","Timestamp"]].copy()
    tabela.insert(1, "Preco", sub_b2b["Preco"].apply(lambda x: "R" + chr(36) + f" {x:.2f}"))
    tabela.columns = ["Mercado","Preço","Distância","Atualização"]
    st.dataframe(tabela, use_container_width=True, hide_index=True)


# ─────────────────────────────────────────────────────────────────
#  FOOTER
# ─────────────────────────────────────────────────────────────────
st.markdown("""
<div class='footer-bar'>
  <span>4SAVR</span> · MVP Simulado v2.0 · Dados fictícios para fins de demonstração ·
  Construído com Streamlit + Python<br>
  <em>"Onde sua economia fortalece o bairro."</em>
</div>""", unsafe_allow_html=True)
