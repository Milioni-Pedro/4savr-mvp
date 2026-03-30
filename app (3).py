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
#  CUSTOM CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Sora:wght@300;400;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap');
  html, body, [class*="css"] { font-family: 'Sora', sans-serif; }
  .stApp { background: linear-gradient(160deg,#020f1f 0%,#031a30 60%,#042440 100%); color:#e8f4f8; }
  [data-testid="stSidebar"] { background: linear-gradient(180deg,#010d1c 0%,#021525 100%); border-right:1px solid #0d3a5c; }
  [data-testid="stSidebar"] * { color:#c8e6f5 !important; }
  h1,h2,h3 { font-family:'Sora',sans-serif !important; }

  .hero-banner {
    background: linear-gradient(135deg,#00c882 0%,#00a86b 40%,#007a50 100%);
    border-radius:16px; padding:28px 36px; margin-bottom:24px;
    box-shadow:0 8px 32px rgba(0,200,130,0.25);
  }
  .hero-banner h1 { color:#fff !important; font-size:2rem !important; font-weight:800 !important; margin:0 0 6px !important; }
  .hero-banner p  { color:rgba(255,255,255,0.9) !important; font-size:1.05rem; margin:0; }
  .hero-tag {
    display:inline-block; background:rgba(255,255,255,0.2); color:#fff !important;
    font-size:0.72rem; font-weight:600; letter-spacing:0.12em; text-transform:uppercase;
    padding:4px 12px; border-radius:20px; margin-bottom:12px;
  }
  .metric-card {
    background:linear-gradient(145deg,rgba(13,58,92,0.6),rgba(4,36,64,0.8));
    border:1px solid rgba(0,200,130,0.2); border-radius:14px;
    padding:20px 22px; text-align:center; backdrop-filter:blur(8px);
  }
  .metric-card .value { font-size:2rem; font-weight:800; color:#00c882; font-family:'JetBrains Mono',monospace; }
  .metric-card .label { font-size:0.78rem; color:#7fb8d4; text-transform:uppercase; letter-spacing:0.08em; margin-top:6px; }
  .section-title {
    font-size:1.1rem; font-weight:700; color:#00c882; text-transform:uppercase;
    letter-spacing:0.1em; margin:28px 0 14px; padding-bottom:8px;
    border-bottom:1px solid rgba(0,200,130,0.25);
  }
  .price-box      { border-radius:10px; padding:14px 18px; margin-bottom:8px; }
  .price-box-best { background:rgba(0,200,130,0.10); border:2px solid #00c882; }
  .price-box-norm { background:rgba(13,58,92,0.40);  border:1px solid rgba(13,58,92,0.8); }
  .price-name      { font-weight:700; font-size:0.97rem; color:#e8f4f8; }
  .price-name-best { font-weight:700; font-size:0.97rem; color:#00c882; }
  .price-sub  { font-size:0.78rem; color:#7fb8d4; margin-top:2px; }
  .price-num  { font-family:'JetBrains Mono',monospace; font-size:1.35rem; font-weight:800; text-align:right; }
  .price-num-best { color:#00c882; }
  .price-num-norm { color:#e8f4f8; }
  .badge-best {
    display:inline-block; background:#00c882; color:#010d1c;
    font-size:0.65rem; font-weight:700; padding:3px 8px; border-radius:20px;
    text-transform:uppercase; letter-spacing:0.08em; margin-left:8px; vertical-align:middle;
  }
  .alert-card {
    background:linear-gradient(135deg,rgba(220,38,38,0.15),rgba(153,27,27,0.2));
    border:1px solid rgba(220,38,38,0.5); border-left:4px solid #dc2626;
    border-radius:12px; padding:18px 22px; margin:12px 0;
  }
  .alert-card .alert-title { color:#fca5a5; font-weight:700; font-size:0.85rem; text-transform:uppercase; letter-spacing:0.1em; margin-bottom:8px; }
  .alert-card .alert-body  { color:#fecaca; font-size:0.95rem; line-height:1.6; }
  .alert-card .alert-impact{ color:#f87171; font-weight:700; font-size:1.1rem; margin-top:8px; }
  .success-card {
    background:linear-gradient(135deg,rgba(0,200,130,0.15),rgba(0,120,80,0.2));
    border:1px solid rgba(0,200,130,0.5); border-left:4px solid #00c882;
    border-radius:12px; padding:18px 22px; margin:12px 0;
  }
  .success-card .s-title { color:#6ee7b7; font-weight:700; font-size:1rem; margin-bottom:6px; }
  .success-card .s-body  { color:#a7f3d0; font-size:0.9rem; line-height:1.5; }
  .info-card {
    background:rgba(13,58,92,0.5); border:1px solid rgba(0,200,130,0.2);
    border-radius:12px; padding:16px 20px; margin:8px 0;
  }
  .info-card .i-title { color:#7fb8d4; font-size:0.78rem; text-transform:uppercase; letter-spacing:0.08em; margin-bottom:4px; }
  .info-card .i-body  { color:#e8f4f8; font-size:0.95rem; font-weight:500; }
  .opt-box {
    background:linear-gradient(135deg,rgba(0,200,130,0.1),rgba(4,36,64,0.8));
    border:1px solid rgba(0,200,130,0.35); border-radius:14px; padding:22px 24px; margin:14px 0;
  }
  .opt-box-hi { border-color:rgba(0,200,130,0.6) !important; }
  .opt-title { color:#00c882; font-weight:700; font-size:1rem; margin-bottom:12px; }
  .rank-card {
    display:flex; align-items:center; gap:14px;
    background:rgba(13,58,92,0.4); border:1px solid rgba(13,58,92,0.8);
    border-radius:10px; padding:12px 18px; margin-bottom:8px;
  }
  .rank-pos  { font-family:'JetBrains Mono',monospace; font-size:1.1rem; font-weight:700; color:#00c882; width:28px; }
  .rank-name { font-weight:600; color:#e8f4f8; flex:1; }
  .rank-pts  { font-family:'JetBrains Mono',monospace; font-size:0.85rem; color:#7fb8d4; }
  .ad-preview {
    background:linear-gradient(135deg,#021525,#031a30);
    border:2px solid #00c882; border-radius:14px; padding:20px 24px;
    margin:12px 0; position:relative; box-shadow:0 0 24px rgba(0,200,130,0.15);
  }
  .ad-label {
    position:absolute; top:-10px; left:20px;
    background:#00c882; color:#010d1c; font-size:0.65rem; font-weight:700;
    padding:2px 10px; border-radius:20px; text-transform:uppercase; letter-spacing:0.1em;
  }
  .ad-store   { font-size:1rem; font-weight:700; color:#00c882; margin-bottom:4px; }
  .ad-product { font-size:1.3rem; font-weight:800; color:#fff; margin-bottom:4px; }
  .ad-price   { font-family:'JetBrains Mono',monospace; font-size:2rem; font-weight:800; color:#00c882; }
  .ad-validity{ font-size:0.75rem; color:#7fb8d4; margin-top:6px; }
  .ad-reach   { font-size:0.8rem; color:#a7f3d0; margin-top:8px; font-weight:500; }
  .stButton > button {
    background:linear-gradient(135deg,#00c882,#00a86b) !important;
    color:#010d1c !important; font-weight:700 !important;
    font-family:'Sora',sans-serif !important; border:none !important;
    border-radius:10px !important; padding:10px 22px !important;
    box-shadow:0 4px 16px rgba(0,200,130,0.3) !important;
  }
  .footer-bar {
    text-align:center; padding:20px; color:#2a5a7a;
    font-size:0.75rem; margin-top:40px; border-top:1px solid rgba(13,58,92,0.5);
  }
  .footer-bar span { color:#00c882; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  MOCK DATA
# ─────────────────────────────────────────────
MERCADOS = {
    "Mercado Boa Vista":    "0m (referência)",
    "Supermercado Central": "180m",
    "Mini Box Econômico":   "300m",
    "Atacado do Bairro":    "520m",
    "Mercado Família":      "750m",
}
PRODUTOS_BASE = {
    "Leite Integral 1L":       {"emoji": "🥛", "categoria": "Laticínios",  "unidade": "1L"},
    "Arroz Branco 5kg":        {"emoji": "🌾", "categoria": "Grãos",       "unidade": "5kg"},
    "Feijão Carioca 1kg":      {"emoji": "🫘", "categoria": "Grãos",       "unidade": "1kg"},
    "Cerveja Lata 350ml":      {"emoji": "🍺", "categoria": "Bebidas",     "unidade": "lata"},
    "Café Torrado 500g":       {"emoji": "☕", "categoria": "Bebidas",     "unidade": "500g"},
    "Óleo de Soja 900ml":      {"emoji": "🫙", "categoria": "Condimentos", "unidade": "900ml"},
    "Açúcar Cristal 1kg":      {"emoji": "🍬", "categoria": "Açúcar",      "unidade": "1kg"},
    "Pão de Forma 500g":       {"emoji": "🍞", "categoria": "Padaria",     "unidade": "500g"},
    "Macarrão Espaguete 500g": {"emoji": "🍝", "categoria": "Massas",      "unidade": "500g"},
    "Frango Congelado 1kg":    {"emoji": "🍗", "categoria": "Proteínas",   "unidade": "1kg"},
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
    "Atualizado há 8 min", "Atualizado há 15 min", "Atualizado há 23 min",
    "Atualizado há 41 min", "Atualizado há 1h 02min",
]
EMBAIXADORES = [
    {"nome": "Ana Paula M.", "pts": 1840, "badge": "🏆"},
    {"nome": "Ricardo S.",   "pts": 1622, "badge": "🥈"},
    {"nome": "Fernanda L.",  "pts": 1405, "badge": "🥉"},
    {"nome": "João Victor",  "pts": 1298, "badge": "⭐"},
    {"nome": "Marcia T.",    "pts": 1187, "badge": "⭐"},
]

def build_df():
    rows = []
    mercados_list = list(MERCADOS.keys())
    for prod, precos in PRECOS_BASE.items():
        for i, merc in enumerate(mercados_list):
            rows.append({
                "Produto":   prod,
                "Mercado":   merc,
                "Distancia": MERCADOS[merc],
                "Preco":     precos[i],
                "Timestamp": TIMESTAMPS[i],
            })
    return pd.DataFrame(rows)

def build_history(produto):
    dias  = [datetime.today() - timedelta(days=i) for i in range(13, -1, -1)]
    base  = PRECOS_BASE[produto][0]
    media = sum(PRECOS_BASE[produto]) / len(PRECOS_BASE[produto])
    random.seed(42)
    return pd.DataFrame({
        "Data":            [d.strftime("%d/%m") for d in dias],
        "Seu Mercado":     [round(base  + random.uniform(-0.3,  0.4), 2) for _ in dias],
        "Media do Bairro": [round(media + random.uniform(-0.15, 0.15), 2) for _ in dias],
    })

DF = build_df()

# Função auxiliar: formata preço SEM usar $ em f-strings de HTML
def fmt(valor):
    """Retorna string 'R&#36; X,XX' segura para uso em HTML do Streamlit."""
    return "R&#36;&nbsp;" + f"{valor:.2f}".replace(".", ",")

# ─────────────────────────────────────────────
#  SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center;padding:16px 0 24px'>
      <div style='font-size:2.4rem;margin-bottom:4px'>💚</div>
      <div style='font-size:1.4rem;font-weight:800;color:#00c882;letter-spacing:0.05em'>4SAVR</div>
      <div style='font-size:0.72rem;color:#5a9ab8;letter-spacing:0.12em;text-transform:uppercase'>For Saver · MVP v0.1</div>
    </div>""", unsafe_allow_html=True)
    st.markdown("---")
    visao = st.radio("Visão:", ["👤  Consumidor (B2C)", "🏪  Lojista Parceiro (B2B)"], label_visibility="collapsed")
    st.markdown("---")
    st.markdown("""
    <div style='padding:12px;background:rgba(0,200,130,0.08);border-radius:10px;border:1px solid rgba(0,200,130,0.2)'>
      <div style='font-size:0.72rem;color:#5a9ab8;text-transform:uppercase;letter-spacing:0.1em;margin-bottom:6px'>Bairro Ativo</div>
      <div style='color:#00c882;font-weight:700;font-size:0.95rem'>📍 Bairro Boa Vista</div>
      <div style='color:#7fb8d4;font-size:0.78rem;margin-top:2px'>Curitiba – PR</div>
    </div>
    <div style='margin-top:12px;padding:12px;background:rgba(13,58,92,0.4);border-radius:10px'>
      <div style='font-size:0.72rem;color:#5a9ab8;text-transform:uppercase;letter-spacing:0.1em;margin-bottom:6px'>Status da Rede</div>
      <div style='display:flex;align-items:center;gap:8px'>
        <div style='width:8px;height:8px;border-radius:50%;background:#00c882;box-shadow:0 0 8px #00c882'></div>
        <span style='color:#e8f4f8;font-size:0.85rem'>5 mercados online</span>
      </div>
    </div>
    <div style='margin-top:20px;text-align:center;font-size:0.78rem;color:#2a5a7a;font-style:italic;line-height:1.5'>
      "Onde sua economia<br>fortalece o bairro."
    </div>""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════
#  VISÃO CONSUMIDOR
# ═══════════════════════════════════════════════════════
if "Consumidor" in visao:

    st.markdown("""
    <div class='hero-banner'>
      <div class='hero-tag'>🛒 Modo Consumidor</div>
      <h1>Economize no seu bairro, hoje</h1>
      <p>Compare preços em tempo real nos mercados a menos de 1km de você.</p>
    </div>""", unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    cards = [
        ("18,70", "Economia média/semana"),
        ("5",     "Mercados monitorados"),
        ("10",    "Produtos rastreados"),
        ("340",   "Seus pontos de reputação"),
    ]
    for col, (val, lbl) in zip([c1, c2, c3, c4], cards):
        col.markdown(f"<div class='metric-card'><div class='value'>{val}</div><div class='label'>{lbl}</div></div>", unsafe_allow_html=True)

    # ── Comparador ────────────────────────────────────────────────
    st.markdown("<div class='section-title'>🔍 Comparador de Preços</div>", unsafe_allow_html=True)

    col_sel, col_info = st.columns([2, 1])
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

    sub         = DF[DF["Produto"] == produto_sel].sort_values("Preco").reset_index(drop=True)
    menor_preco = sub["Preco"].min()
    maior_preco = sub["Preco"].max()
    economia_max = round(maior_preco - menor_preco, 2)

    # Renderiza cada linha de preço — cifrão via entidade HTML
    for _, row in sub.iterrows():
        best    = row["Preco"] == menor_preco
        box_cls = "price-box price-box-best" if best else "price-box price-box-norm"
        nm_cls  = "price-name-best"          if best else "price-name"
        pr_cls  = "price-num price-num-best" if best else "price-num price-num-norm"
        badge   = "<span class='badge-best'>Melhor Preço</span>" if best else ""
        preco_html = fmt(row["Preco"])

        st.markdown(
            f"<div class='{box_cls}'>"
            f"  <div style='display:flex;justify-content:space-between;align-items:center'>"
            f"    <div>"
            f"      <div class='{nm_cls}'>{row['Mercado']} {badge}</div>"
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
            f"<div class='s-body'>Comprando no <strong>{sub.iloc[0]['Mercado']}</strong> em vez do mais caro "
            f"você economiza <strong>{fmt(economia_max)}</strong> por unidade — "
            f"equivale a <strong>{fmt(economia_max * 4)}</strong> por mês comprando 4 vezes.</div>"
            f"</div>",
            unsafe_allow_html=True,
        )

    st.markdown("---")

    # ── Simulador OCR ─────────────────────────────────────────────
    st.markdown("<div class='section-title'>📷 Cupom Fiscal Inteligente</div>", unsafe_allow_html=True)
    st.markdown("""
    <div class='info-card'>
      <div class='i-title'>Como funciona</div>
      <div class='i-body'>Tire foto do seu cupom fiscal. Nossa IA extrai os preços, valida os dados
      e credita pontos de reputação na sua conta. Cada cupom = dados frescos para toda a comunidade.</div>
    </div>""", unsafe_allow_html=True)

    col_ocr, _ = st.columns([1, 2])
    with col_ocr:
        if st.button("📤  Simular Envio de Cupom Fiscal", use_container_width=True):
            with st.spinner("🤖 Processando Inteligência de Dados..."):
                time.sleep(0.6)
                prog = st.progress(0)
                for pct in range(0, 101, 20):
                    time.sleep(0.18)
                    prog.progress(pct)
                time.sleep(0.3)
                prog.empty()
            st.markdown("""
            <div class='success-card'>
              <div class='s-title'>✅ Cupom validado com sucesso!</div>
              <div class='s-body'>
                <strong>7 itens</strong> extraídos &nbsp;·&nbsp;
                <strong>R&#36;&nbsp;87,40</strong> processados<br>
                Mercado identificado: <strong>Supermercado Central</strong><br>
                <span style='color:#00c882;font-weight:700;font-size:1.05rem'>
                  +50 pontos de reputação creditados 🎉
                </span>
              </div>
            </div>""", unsafe_allow_html=True)

    st.markdown("---")

    # ── Otimizador de Cesta ───────────────────────────────────────
    st.markdown("<div class='section-title'>🧺 Otimizador de Cesta</div>", unsafe_allow_html=True)
    st.markdown("""
    <div class='info-card'>
      <div class='i-title'>Como funciona</div>
      <div class='i-body'>Selecione até 5 produtos. O 4SAVR calcula se vale comprar tudo num lugar
      ou dividir entre dois mercados próximos.</div>
    </div>""", unsafe_allow_html=True)

    itens_sel = st.multiselect(
        "Produtos da cesta:",
        list(PRODUTOS_BASE.keys()),
        default=list(PRODUTOS_BASE.keys())[:3],
        format_func=lambda x: f"{PRODUTOS_BASE[x]['emoji']} {x}",
        max_selections=5,
    )

    if itens_sel:
        mercados_list = list(MERCADOS.keys())
        totais = sorted(
            [(m, sum(PRECOS_BASE[p][i] for p in itens_sel))
             for i, m in enumerate(mercados_list)],
            key=lambda x: x[1],
        )
        melhor_m, melhor_total = totais[0]
        segundo_m, _           = totais[1]
        mid     = max(len(itens_sel) // 2, 1)
        grupo_a = itens_sel[:mid]
        grupo_b = itens_sel[mid:]
        idx_a   = mercados_list.index(melhor_m)
        idx_b   = mercados_list.index(segundo_m)
        total_div    = sum(PRECOS_BASE[p][idx_a] for p in grupo_a) + sum(PRECOS_BASE[p][idx_b] for p in grupo_b)
        economia_div = max(round(melhor_total - total_div, 2), 0)
        extra_dist   = random.randint(300, 600)

        col_opt1, col_opt2 = st.columns(2)
        with col_opt1:
            st.markdown(
                f"<div class='opt-box'>"
                f"<div class='opt-title'>🏪 Estratégia 1 — Compra única</div>"
                f"<table style='width:100%;color:#e8f4f8;font-size:0.88rem;border-spacing:0 6px'>"
                f"<tr><td style='color:#7fb8d4'>Melhor mercado</td>"
                f"    <td style='text-align:right;font-weight:700'>{melhor_m[:22]}</td></tr>"
                f"<tr><td style='color:#7fb8d4'>Total estimado</td>"
                f"    <td style='text-align:right;font-weight:700'>{fmt(melhor_total)}</td></tr>"
                f"<tr><td style='color:#7fb8d4'>Distância extra</td>"
                f"    <td style='text-align:right;font-weight:700'>0m</td></tr>"
                f"</table></div>",
                unsafe_allow_html=True,
            )
        with col_opt2:
            st.markdown(
                f"<div class='opt-box opt-box-hi'>"
                f"<div class='opt-title'>🗺️ Estratégia 2 — Dividir entre 2</div>"
                f"<table style='width:100%;color:#e8f4f8;font-size:0.88rem;border-spacing:0 6px'>"
                f"<tr><td style='color:#7fb8d4'>{melhor_m[:16]} + {segundo_m[:14]}</td><td></td></tr>"
                f"<tr><td style='color:#7fb8d4'>Total estimado</td>"
                f"    <td style='text-align:right;font-weight:700'>{fmt(total_div)}</td></tr>"
                f"<tr><td style='color:#7fb8d4'>Distância extra</td>"
                f"    <td style='text-align:right;font-weight:700'>+{extra_dist}m</td></tr>"
                f"</table>"
                f"<div style='text-align:center;margin-top:14px'>"
                f"  <div style='font-size:0.75rem;color:#7fb8d4;margin-bottom:2px'>Economia ao dividir</div>"
                f"  <div style='font-family:monospace;font-size:1.5rem;font-weight:800;color:#00c882'>"
                f"    + {fmt(economia_div)} 💚"
                f"  </div></div></div>",
                unsafe_allow_html=True,
            )

    st.markdown("---")

    # ── Ranking Embaixadores ──────────────────────────────────────
    st.markdown("<div class='section-title'>🏆 Embaixadores de Economia do Bairro</div>", unsafe_allow_html=True)
    st.markdown("""
    <div class='info-card' style='margin-bottom:14px'>
      <div class='i-title'>Gamificação Comunitária</div>
      <div class='i-body'>Envie cupons, valide preços e suba no ranking. Quanto mais você contribui,
      mais o bairro economiza. 🎖️</div>
    </div>""", unsafe_allow_html=True)

    for i, emb in enumerate(EMBAIXADORES):
        pts_fmt = f"{emb['pts']:,}".replace(",", ".")
        st.markdown(
            f"<div class='rank-card'>"
            f"<div class='rank-pos'>#{i+1}</div>"
            f"<div style='font-size:1.2rem'>{emb['badge']}</div>"
            f"<div class='rank-name'>{emb['nome']}</div>"
            f"<div class='rank-pts'>{pts_fmt} pts</div>"
            f"</div>",
            unsafe_allow_html=True,
        )

# ═══════════════════════════════════════════════════════
#  VISÃO LOJISTA
# ═══════════════════════════════════════════════════════
else:
    st.markdown("""
    <div class='hero-banner' style='background:linear-gradient(135deg,#0a2a4a,#0d3a5c,#042440);border:1px solid rgba(0,200,130,0.3)'>
      <div class='hero-tag'>🏪 Modo Lojista Parceiro</div>
      <h1>Inteligência Competitiva em Tempo Real</h1>
      <p>Monitore o mercado, reaja à concorrência e atraia clientes com ofertas inteligentes.</p>
    </div>""", unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    for col, (val, lbl) in zip([c1, c2, c3, c4], [
        ("+127", "Clientes atraídos hoje"), ("3", "Alertas competitivos ativos"),
        ("2,4k", "Receita influenciada/semana"), ("8,4%", "Share of shelf digital"),
    ]):
        col.markdown(f"<div class='metric-card'><div class='value'>{val}</div><div class='label'>{lbl}</div></div>", unsafe_allow_html=True)

    st.markdown("---")

    # ── Alertas ───────────────────────────────────────────────────
    st.markdown("<div class='section-title'>🚨 Alertas de Mercado</div>", unsafe_allow_html=True)
    st.markdown("""
    <div class='alert-card'>
      <div class='alert-title'>⚠️ Alerta: Perda de Conversão Detectada</div>
      <div class='alert-body'>
        Você perdeu <strong>12% de conversão</strong> no item <strong>Café Torrado 500g</strong> hoje.
        O concorrente <em>Mini Box Econômico</em> a <strong>300m</strong> baixou o preço em
        <strong>R&#36;&nbsp;0,40</strong> às 09h15.
      </div>
      <div class='alert-impact'>📉 Impacto estimado: -R&#36;&nbsp;280 em vendas hoje</div>
    </div>""", unsafe_allow_html=True)

    st.markdown("""
    <div class='alert-card' style='border-left-color:#f59e0b;background:linear-gradient(135deg,rgba(245,158,11,0.1),rgba(120,77,5,0.15))'>
      <div class='alert-title' style='color:#fcd34d'>⚡ Oportunidade: Concorrente com Ruptura de Estoque</div>
      <div class='alert-body' style='color:#fef3c7'>
        <em>Atacado do Bairro</em> está sem estoque de <strong>Óleo de Soja 900ml</strong> desde às 11h00.
        Consumidores buscam alternativas no raio de 700m.
      </div>
      <div class='alert-impact' style='color:#fbbf24'>📈 Oportunidade de +R&#36;&nbsp;190 em vendas extras</div>
    </div>""", unsafe_allow_html=True)

    st.markdown("---")

    # ── Dashboard Preços ──────────────────────────────────────────
    st.markdown("<div class='section-title'>📊 Dashboard de Posicionamento de Preço</div>", unsafe_allow_html=True)

    col_g1, col_g2 = st.columns([3, 1])
    with col_g1:
        produto_b2b = st.selectbox(
            "Produto:",
            list(PRODUTOS_BASE.keys()),
            format_func=lambda x: f"{PRODUTOS_BASE[x]['emoji']} {x}",
            key="b2b_prod",
        )
    with col_g2:
        periodo = st.selectbox("Período:", ["14 dias", "7 dias", "30 dias"], key="periodo")

    hist = build_history(produto_b2b)
    n    = 7 if "7" in periodo else (30 if "30" in periodo else 14)
    st.line_chart(hist.tail(n).set_index("Data"), use_container_width=True)

    st.markdown("<div class='section-title'>📊 Comparativo de Preços – Todos os Mercados</div>", unsafe_allow_html=True)
    sub_b2b = DF[DF["Produto"] == produto_b2b].sort_values("Preco").reset_index(drop=True)
    sub_b2b["Mercado Curto"] = sub_b2b["Mercado"].str[:18]
    st.bar_chart(sub_b2b.set_index("Mercado Curto")[["Preco"]], use_container_width=True)

    tabela = sub_b2b[["Mercado", "Distancia", "Timestamp"]].copy()
    tabela.insert(1, "Preco", sub_b2b["Preco"].apply(lambda x: "R" + chr(36) + f" {x:.2f}".replace("$", chr(36))))
    tabela.columns = ["Mercado", "Preço", "Distância", "Atualização"]
    st.dataframe(tabela, use_container_width=True, hide_index=True)

    st.markdown("---")

    # ── Simulador de Anúncio ──────────────────────────────────────
    st.markdown("<div class='section-title'>📣 Simulador de Oferta Impulsionada</div>", unsafe_allow_html=True)
    st.markdown("""
    <div class='info-card' style='margin-bottom:16px'>
      <div class='i-title'>Como funciona</div>
      <div class='i-body'>Configure sua oferta e veja o preview de como ela aparece
      para consumidores do bairro no app 4SAVR.</div>
    </div>""", unsafe_allow_html=True)

    col_ad1, col_ad2 = st.columns(2)
    with col_ad1:
        ad_produto = st.selectbox(
            "Produto em oferta:",
            list(PRODUTOS_BASE.keys()),
            format_func=lambda x: f"{PRODUTOS_BASE[x]['emoji']} {x}",
            key="ad_prod",
        )
        preco_orig  = PRECOS_BASE[ad_produto][0]
        ad_preco    = st.number_input("Preço promocional:", min_value=0.50,
                                      max_value=float(preco_orig) * 1.5,
                                      value=round(preco_orig * 0.95, 2), step=0.10)
        ad_validade = st.selectbox("Validade:", ["Hoje, até 22h", "Amanhã, dia todo",
                                                  "Este fim de semana", "Próximos 3 dias"])
        raio        = st.slider("Raio de alcance (m):", 200, 1000, 500, 50)

    with col_ad2:
        emoji_prod  = PRODUTOS_BASE[ad_produto]["emoji"]
        desconto    = round((preco_orig - ad_preco) / preco_orig * 100, 1)
        alcance_est = int(raio * 1.8 + random.randint(80, 150))
        preco_novo  = f"{ad_preco:.2f}".replace(".", ",")
        preco_velho = f"{preco_orig:.2f}".replace(".", ",")

        st.markdown(
            f"<div style='margin-top:4px'>"
            f"<div style='font-size:0.75rem;color:#5a9ab8;margin-bottom:8px;"
            f"text-transform:uppercase;letter-spacing:0.1em'>Preview do Anúncio</div>"
            f"<div class='ad-preview'>"
            f"  <div class='ad-label'>Oferta Impulsionada</div>"
            f"  <div class='ad-store'>📍 Mercado Boa Vista · {raio}m de raio</div>"
            f"  <div class='ad-product'>{emoji_prod} {ad_produto}</div>"
            f"  <div class='ad-price'>R&#36;&nbsp;{preco_novo}</div>"
            f"  <div style='color:#fca5a5;font-size:0.8rem;margin-top:4px'>"
            f"    <s>R&#36;&nbsp;{preco_velho}</s> &nbsp;·&nbsp;"
            f"    <span style='color:#00c882;font-weight:700'>{desconto:.1f}% OFF</span>"
            f"  </div>"
            f"  <div class='ad-validity'>⏰ {ad_validade}</div>"
            f"  <div class='ad-reach'>👁 Alcance estimado: <strong>{alcance_est} consumidores</strong></div>"
            f"</div></div>",
            unsafe_allow_html=True,
        )

    col_btn, _ = st.columns([1, 2])
    with col_btn:
        if st.button("🚀  Ativar Oferta", use_container_width=True):
            with st.spinner("Publicando oferta na rede 4SAVR..."):
                time.sleep(1.2)
            st.markdown(
                f"<div class='success-card'>"
                f"<div class='s-title'>✅ Oferta publicada com sucesso!</div>"
                f"<div class='s-body'>"
                f"<strong>{emoji_prod} {ad_produto}</strong> por <strong>R&#36;&nbsp;{preco_novo}</strong> "
                f"está visível para <strong>{alcance_est} consumidores</strong> num raio de {raio}m.<br>"
                f"Validade: <strong>{ad_validade}</strong>.</div></div>",
                unsafe_allow_html=True,
            )

# ─────────────────────────────────────────────
#  FOOTER
# ─────────────────────────────────────────────
st.markdown("""
<div class='footer-bar'>
  <span>4SAVR</span> · MVP Simulado v0.1 · Dados fictícios para fins de demonstração<br>
  <em>"Onde sua economia fortalece o bairro."</em>
</div>""", unsafe_allow_html=True)
