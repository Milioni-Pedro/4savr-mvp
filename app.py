"""
4SAVR MVP v4.0 — Inteligência Total & Cesta Dinâmica
Streamlit app — 100% gratuito para hospedar no Streamlit Cloud
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from itertools import combinations
import random
import datetime

# ─────────────────────────────────────────────
# CONFIGURAÇÃO GLOBAL DA PÁGINA
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="4SAVR — Economize na Cesta Básica",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─────────────────────────────────────────────
# CSS PERSONALIZADO  (Navy #001f3f + Green #2ecc71)
# ─────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Sora:wght@400;600;700;800&family=Inter:wght@400;500&display=swap');

  html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

  /* Fundo geral */
  .stApp { background: #f0f4f8; }

  /* Header hero */
  .hero-banner {
    background: linear-gradient(135deg, #001f3f 0%, #003366 60%, #004080 100%);
    border-radius: 16px;
    padding: 2rem 2.5rem;
    margin-bottom: 1.5rem;
    color: white;
    display: flex;
    align-items: center;
    gap: 1.5rem;
  }
  .hero-title {
    font-family: 'Sora', sans-serif;
    font-size: 2.4rem;
    font-weight: 800;
    color: #2ecc71;
    margin: 0;
    line-height: 1.1;
  }
  .hero-sub {
    font-size: 1rem;
    color: #a8c8e8;
    margin-top: 0.3rem;
  }

  /* Tabs customizadas */
  .stTabs [data-baseweb="tab-list"] {
    background: #001f3f;
    border-radius: 12px 12px 0 0;
    gap: 4px;
    padding: 6px 8px 0;
  }
  .stTabs [data-baseweb="tab"] {
    color: #a8c8e8 !important;
    font-family: 'Sora', sans-serif;
    font-weight: 600;
    border-radius: 8px 8px 0 0;
    padding: 10px 24px;
  }
  .stTabs [aria-selected="true"] {
    background: #f0f4f8 !important;
    color: #001f3f !important;
  }

  /* Cards de cenário */
  .scenario-card {
    background: white;
    border-radius: 14px;
    padding: 1.4rem 1.6rem;
    box-shadow: 0 2px 12px rgba(0,31,63,0.08);
    border-left: 5px solid #001f3f;
    margin-bottom: 1rem;
  }
  .scenario-card.best {
    border-left: 5px solid #2ecc71;
    background: linear-gradient(135deg, #f0fff6 0%, #ffffff 100%);
  }
  .scenario-title {
    font-family: 'Sora', sans-serif;
    font-weight: 700;
    font-size: 1.05rem;
    color: #001f3f;
    margin-bottom: 0.5rem;
  }
  .scenario-price {
    font-family: 'Sora', sans-serif;
    font-size: 2rem;
    font-weight: 800;
    color: #001f3f;
  }
  .scenario-price.green { color: #2ecc71; }
  .economy-badge {
    background: #2ecc71;
    color: white;
    font-family: 'Sora', sans-serif;
    font-weight: 700;
    border-radius: 20px;
    padding: 6px 18px;
    display: inline-block;
    font-size: 1.1rem;
    margin-top: 0.8rem;
  }

  /* Tabela de split */
  .split-table { width: 100%; border-collapse: collapse; }
  .split-table th {
    background: #001f3f;
    color: white;
    padding: 8px 14px;
    text-align: left;
    font-family: 'Sora', sans-serif;
    font-size: 0.85rem;
  }
  .split-table td {
    padding: 8px 14px;
    border-bottom: 1px solid #e8eef4;
    font-size: 0.88rem;
  }
  .split-table tr:nth-child(even) td { background: #f8fafc; }

  /* Score badge */
  .score-badge {
    background: linear-gradient(135deg, #001f3f, #003366);
    color: white;
    border-radius: 50%;
    width: 80px; height: 80px;
    display: flex; align-items: center; justify-content: center;
    font-family: 'Sora', sans-serif;
    font-size: 1.5rem;
    font-weight: 800;
    margin: 0 auto;
  }

  /* Alert cards */
  .alert-card {
    background: #fff8e1;
    border: 1px solid #ffc107;
    border-radius: 10px;
    padding: 1rem 1.2rem;
    margin-bottom: 0.7rem;
  }
  .alert-card.danger {
    background: #fff3f3;
    border-color: #e74c3c;
  }

  /* KPI metric override */
  [data-testid="stMetric"] {
    background: white;
    border-radius: 12px;
    padding: 1rem 1.2rem;
    box-shadow: 0 2px 8px rgba(0,31,63,0.07);
  }
  [data-testid="stMetricLabel"] { font-family: 'Sora', sans-serif; font-weight: 600; }
  [data-testid="stMetricValue"] { font-family: 'Sora', sans-serif; font-weight: 800; }

  /* Botão principal */
  .stButton > button {
    background: linear-gradient(135deg, #2ecc71, #27ae60) !important;
    color: white !important;
    font-family: 'Sora', sans-serif !important;
    font-weight: 700 !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.6rem 1.8rem !important;
    font-size: 1rem !important;
    transition: all 0.2s ease !important;
  }
  .stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px rgba(46,204,113,0.4) !important;
  }

  div[data-testid="stSidebar"] { background: #001f3f; }

  .footer-note {
    text-align: center; color: #889aab; font-size: 0.78rem; margin-top: 2rem;
  }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# SESSION STATE INIT
# ─────────────────────────────────────────────
defaults = {
    "cesta_selecionada": [],
    "score_confianca": 0,
    "trafego_total": 47,
    "buscas_por_item": {},
    "historico_validacoes": [],
    "lojas_visitadas": [],
    "promo_relampago": [],
    "seed": 42,
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

random.seed(st.session_state["seed"])
np.random.seed(st.session_state["seed"])


# ─────────────────────────────────────────────
# DADOS SIMULADOS
# ─────────────────────────────────────────────
MERCADOS = ["Condor", "Muffato", "Angeloni", "Festival", "Atacadão", "Max Atacadista"]

CORES_MERCADO = {
    "Condor":          "#e74c3c",
    "Muffato":         "#3498db",
    "Angeloni":        "#9b59b6",
    "Festival":        "#f39c12",
    "Atacadão":        "#1abc9c",
    "Max Atacadista":  "#001f3f",
}

# Preços base por item (R$) — simulado mas realista para Curitiba 2024
PRECOS_BASE = {
    "Arroz 5kg":           {"Condor": 22.90, "Muffato": 21.50, "Angeloni": 24.99, "Festival": 23.40, "Atacadão": 18.90, "Max Atacadista": 19.50},
    "Feijão Preto 1kg":    {"Condor":  8.90, "Muffato":  9.20, "Angeloni":  9.99, "Festival":  8.50, "Atacadão":  7.40, "Max Atacadista":  7.80},
    "Feijão Carioca 1kg":  {"Condor":  7.90, "Muffato":  8.10, "Angeloni":  8.90, "Festival":  7.60, "Atacadão":  6.50, "Max Atacadista":  6.90},
    "Óleo de Soja 900ml":  {"Condor":  6.90, "Muffato":  6.50, "Angeloni":  7.49, "Festival":  6.80, "Atacadão":  5.90, "Max Atacadista":  6.20},
    "Leite Integral 1L":   {"Condor":  4.59, "Muffato":  4.89, "Angeloni":  5.29, "Festival":  4.40, "Atacadão":  3.99, "Max Atacadista":  4.10},
    "Açúcar Cristal 1kg":  {"Condor":  4.19, "Muffato":  4.50, "Angeloni":  4.89, "Festival":  4.00, "Atacadão":  3.49, "Max Atacadista":  3.60},
    "Farinha de Trigo 1kg":{"Condor":  4.39, "Muffato":  4.80, "Angeloni":  5.10, "Festival":  4.20, "Atacadão":  3.70, "Max Atacadista":  3.90},
    "Macarrão 500g":       {"Condor":  3.49, "Muffato":  3.70, "Angeloni":  3.99, "Festival":  3.30, "Atacadão":  2.99, "Max Atacadista":  3.10},
    "Café 500g":           {"Condor": 15.90, "Muffato": 16.50, "Angeloni": 17.99, "Festival": 15.00, "Atacadão": 13.90, "Max Atacadista": 14.50},
    "Sal 1kg":             {"Condor":  1.99, "Muffato":  2.10, "Angeloni":  2.29, "Festival":  1.90, "Atacadão":  1.59, "Max Atacadista":  1.70},
    "Manteiga 200g":       {"Condor":  8.99, "Muffato":  9.40, "Angeloni": 10.49, "Festival":  8.70, "Atacadão":  7.99, "Max Atacadista":  8.20},
    "Biscoito Cream Cracker":{"Condor":3.99, "Muffato": 4.20, "Angeloni":  4.49, "Festival":  3.80, "Atacadão":  3.29, "Max Atacadista":  3.40},
    "Sabonete (3un)":      {"Condor":  5.49, "Muffato":  5.80, "Angeloni":  6.29, "Festival":  5.20, "Atacadão":  4.50, "Max Atacadista":  4.70},
    "Detergente 500ml":    {"Condor":  2.49, "Muffato":  2.70, "Angeloni":  2.99, "Festival":  2.30, "Atacadão":  1.99, "Max Atacadista":  2.10},
    "Papel Higiênico 4un": {"Condor":  6.99, "Muffato":  7.40, "Angeloni":  7.99, "Festival":  6.80, "Atacadão":  5.90, "Max Atacadista":  6.20},
}

TODOS_ITENS = list(PRECOS_BASE.keys())

# Marcas por categoria (para aba de giro)
MARCAS = {
    "Café 500g":        ["Pilão", "3 Corações", "Café do Ponto", "Melitta"],
    "Arroz 5kg":        ["Tio João", "Prato Fino", "Camil", "Urbano"],
    "Feijão Preto 1kg": ["Camil", "Kicaldo", "Prato Fino", "Tangará"],
    "Óleo de Soja 900ml": ["Liza", "Soya", "Salada", "Purilev"],
    "Leite Integral 1L":  ["Piracanjuba", "Itambé", "Aurora", "Ninho"],
}

# Estoque simulado com data de validade para alertas
np.random.seed(10)
ESTOQUE_LOJISTA = []
hoje = datetime.date.today()
for item in TODOS_ITENS:
    dias_validade = random.randint(5, 120)
    giro_semanal = random.randint(1, 30)
    semanas_estoque = random.randint(1, 8)
    ESTOQUE_LOJISTA.append({
        "Item": item,
        "Estoque (un)": giro_semanal * semanas_estoque,
        "Giro Semanal": giro_semanal,
        "Semanas de Estoque": semanas_estoque,
        "Validade": hoje + datetime.timedelta(days=dias_validade),
        "Dias para Vencer": dias_validade,
    })
df_estoque = pd.DataFrame(ESTOQUE_LOJISTA)


# ─────────────────────────────────────────────
# FUNÇÕES AUXILIARES
# ─────────────────────────────────────────────
def get_df_precos(itens: list) -> pd.DataFrame:
    """Retorna DataFrame de preços filtrado pelos itens selecionados."""
    rows = []
    for item in itens:
        for mercado in MERCADOS:
            rows.append({
                "Item": item,
                "Mercado": mercado,
                "Preço": PRECOS_BASE[item][mercado],
            })
    return pd.DataFrame(rows)


def calcular_cesta_mercado(itens: list) -> dict:
    """Total da cesta em cada mercado."""
    totais = {}
    for m in MERCADOS:
        totais[m] = sum(PRECOS_BASE[item][m] for item in itens)
    return totais


def cenario_conveniencia(itens: list) -> tuple:
    """Retorna (mercado, total) onde a cesta é mais barata em 1 lugar."""
    totais = calcular_cesta_mercado(itens)
    melhor = min(totais, key=totais.get)
    return melhor, totais[melhor], totais


def cenario_economia_maxima(itens: list) -> dict:
    """
    Divide a compra em 2 mercados encontrando o mínimo absoluto.
    Para cada item, escolhe o mercado mais barato.
    Depois agrupa por mercado e retorna plano completo.
    """
    plano = {}
    total = 0.0
    for item in itens:
        precos_item = {m: PRECOS_BASE[item][m] for m in MERCADOS}
        melhor_m = min(precos_item, key=precos_item.get)
        plano[item] = {"Mercado": melhor_m, "Preço": precos_item[melhor_m]}
        total += precos_item[melhor_m]

    # Agrupar por mercado
    por_mercado = {}
    for item, info in plano.items():
        m = info["Mercado"]
        if m not in por_mercado:
            por_mercado[m] = {"itens": [], "subtotal": 0.0}
        por_mercado[m]["itens"].append({"item": item, "preco": info["Preço"]})
        por_mercado[m]["subtotal"] += info["Preço"]

    return {
        "plano_item": plano,
        "por_mercado": por_mercado,
        "total": total,
        "num_mercados": len(por_mercado),
    }


def radar_buscas() -> dict:
    """Retorna dict com contagem de buscas por item (session + simulado)."""
    base = {item: random.randint(3, 45) for item in TODOS_ITENS}
    for item in st.session_state["buscas_por_item"]:
        base[item] = base.get(item, 0) + st.session_state["buscas_por_item"][item]
    return base


def render_hero():
    st.markdown("""
    <div class="hero-banner">
      <div style="font-size:3.5rem">🛒</div>
      <div>
        <p class="hero-title">4SAVR</p>
        <p class="hero-sub">Compare preços, monte sua cesta e economize de verdade — Curitiba e Região</p>
      </div>
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
# HEADER GLOBAL
# ─────────────────────────────────────────────
render_hero()

# Tabs principais
tab_consumidor, tab_lojista = st.tabs([
    "🛍️  Consumidor — Montar minha Cesta",
    "📊  Lojista — BI & Gestão"
])


# ══════════════════════════════════════════════════════════════════════
#  ABA 1: CONSUMIDOR
# ══════════════════════════════════════════════════════════════════════
with tab_consumidor:
    st.markdown("### 🧺 Configure sua Cesta Básica")

    col_check, col_result = st.columns([1, 2], gap="large")

    with col_check:
        st.markdown("**Selecione os itens que precisa comprar:**")

        # Agrupamento visual
        grupos = {
            "🌾 Grãos & Farinhas": ["Arroz 5kg","Feijão Preto 1kg","Feijão Carioca 1kg","Farinha de Trigo 1kg","Macarrão 500g"],
            "🧴 Temperos & Óleos":  ["Óleo de Soja 900ml","Sal 1kg","Café 500g"],
            "🥛 Laticínios":        ["Leite Integral 1L","Manteiga 200g"],
            "🍬 Outros Alimentos":  ["Açúcar Cristal 1kg","Biscoito Cream Cracker"],
            "🧹 Higiene & Limpeza": ["Sabonete (3un)","Detergente 500ml","Papel Higiênico 4un"],
        }

        cesta_nova = []
        for grupo, itens_grupo in grupos.items():
            with st.expander(grupo, expanded=True):
                for item in itens_grupo:
                    checked = item in st.session_state["cesta_selecionada"]
                    if st.checkbox(item, value=checked, key=f"chk_{item}"):
                        cesta_nova.append(item)

        # Atualizar session state e radar de buscas
        novos = set(cesta_nova) - set(st.session_state["cesta_selecionada"])
        for item in novos:
            st.session_state["buscas_por_item"][item] = \
                st.session_state["buscas_por_item"].get(item, 0) + 1
        st.session_state["cesta_selecionada"] = cesta_nova

        n_itens = len(cesta_nova)
        if n_itens > 0:
            st.info(f"🛒 **{n_itens} item(ns)** selecionado(s)")
        else:
            st.warning("Selecione pelo menos 1 item para comparar.")

    # ── PAINEL DE RESULTADOS ──
    with col_result:
        if len(st.session_state["cesta_selecionada"]) == 0:
            st.markdown("""
            <div style="text-align:center;padding:3rem 1rem;color:#889aab">
              <div style="font-size:4rem">🔍</div>
              <p style="font-family:'Sora',sans-serif;font-size:1.2rem">
                Selecione itens ao lado para ver os <b>3 Cenários de Compra</b>
              </p>
            </div>
            """, unsafe_allow_html=True)
        else:
            itens = st.session_state["cesta_selecionada"]

            # ── CENÁRIO 1: CONVENIÊNCIA ──
            m_conv, total_conv, todos_totais = cenario_conveniencia(itens)
            mais_caro_m = max(todos_totais, key=todos_totais.get)

            # ── CENÁRIO 2: ECONOMIA MÁXIMA ──
            eco = cenario_economia_maxima(itens)
            total_eco = eco["total"]
            economia = total_conv - total_eco

            # ── EXIBIÇÃO DOS CARDS ──
            st.markdown("---")
            st.markdown("#### 📊 Comparativo — 3 Cenários de Compra")

            # Cenário 1
            st.markdown(f"""
            <div class="scenario-card">
              <div class="scenario-title">🏪 Cenário 1 — Conveniência (1 único mercado)</div>
              <div>Leve <b>toda</b> a cesta para o <b>{m_conv}</b> e pague:</div>
              <div class="scenario-price">R$ {total_conv:,.2f}</div>
              <div style="color:#889aab;font-size:0.85rem;margin-top:0.3rem">
                ✅ Menos deslocamento &nbsp;|&nbsp; Simples e rápido
              </div>
            </div>
            """, unsafe_allow_html=True)

            # Cenário 2
            mercados_split = list(eco["por_mercado"].keys())
            split_label = " + ".join(mercados_split)
            st.markdown(f"""
            <div class="scenario-card best">
              <div class="scenario-title">💡 Cenário 2 — Economia Máxima ({eco['num_mercados']} mercados)</div>
              <div>Divida a compra entre: <b>{split_label}</b></div>
              <div class="scenario-price green">R$ {total_eco:,.2f}</div>
              <div class="economy-badge">💰 Economia de R$ {economia:.2f}</div>
            </div>
            """, unsafe_allow_html=True)

            # Cenário 3: resumo
            pct = (economia / total_conv * 100) if total_conv > 0 else 0
            st.markdown(f"""
            <div class="scenario-card" style="border-left-color:#f39c12;background:linear-gradient(135deg,#fffbf0,#fff)">
              <div class="scenario-title">📋 Resumo da Comparação</div>
              <table style="width:100%;font-size:0.9rem">
                <tr><td>💵 Mais barato <b>1 mercado</b></td><td><b>{m_conv}</b> — R$ {total_conv:,.2f}</td></tr>
                <tr><td>🏆 Economia máxima</td><td><b>{eco['num_mercados']} mercados</b> — R$ {total_eco:,.2f}</td></tr>
                <tr><td>💚 Você economiza</td><td><b style="color:#2ecc71">R$ {economia:.2f} ({pct:.1f}%)</b></td></tr>
                <tr><td>🚫 Mais caro</td><td>{mais_caro_m} — R$ {todos_totais[mais_caro_m]:,.2f}</td></tr>
              </table>
            </div>
            """, unsafe_allow_html=True)

            # ── PLANO DETALHADO CENÁRIO 2 ──
            with st.expander("📋 Ver plano detalhado — Quem vendo o quê?", expanded=False):
                for mercado, info in eco["por_mercado"].items():
                    cor = CORES_MERCADO.get(mercado, "#333")
                    itens_html = "".join([
                        f"<tr><td>{r['item']}</td><td style='text-align:right;color:{cor};font-weight:600'>R$ {r['preco']:.2f}</td></tr>"
                        for r in info["itens"]
                    ])
                    st.markdown(f"""
                    <div style="margin-bottom:1rem">
                      <div style="font-family:'Sora',sans-serif;font-weight:700;color:{cor};font-size:1rem;margin-bottom:0.4rem">
                        🏬 {mercado}
                      </div>
                      <table class="split-table">
                        <thead><tr><th>Item</th><th>Preço</th></tr></thead>
                        <tbody>{itens_html}</tbody>
                        <tfoot>
                          <tr style="background:#f0f4f8">
                            <td><b>Subtotal</b></td>
                            <td style="text-align:right"><b>R$ {info['subtotal']:.2f}</b></td>
                          </tr>
                        </tfoot>
                      </table>
                    </div>
                    """, unsafe_allow_html=True)

            # ── GRÁFICO COMPARATIVO DE PREÇOS POR MERCADO ──
            st.markdown("#### 🏪 Comparação — Custo total da cesta por mercado")
            df_totais = pd.DataFrame([
                {"Mercado": m, "Total": t}
                for m, t in sorted(todos_totais.items(), key=lambda x: x[1])
            ])
            colors = [CORES_MERCADO[m] for m in df_totais["Mercado"]]

            fig_bar = go.Figure(go.Bar(
                x=df_totais["Mercado"],
                y=df_totais["Total"],
                marker_color=colors,
                text=[f"R$ {v:.2f}" for v in df_totais["Total"]],
                textposition="outside",
            ))
            fig_bar.update_layout(
                plot_bgcolor="white",
                paper_bgcolor="white",
                font=dict(family="Sora"),
                yaxis=dict(showgrid=True, gridcolor="#eef2f7", title="R$"),
                height=340,
                margin=dict(t=20, b=10),
                showlegend=False,
            )
            st.plotly_chart(fig_bar, use_container_width=True)

            # ── GRÁFICO HEATMAP DE PREÇOS POR ITEM ──
            if len(itens) > 1:
                with st.expander("🔥 Ver heatmap de preços por item e mercado"):
                    df_heat = get_df_precos(itens)
                    pivot = df_heat.pivot(index="Item", columns="Mercado", values="Preço")
                    fig_heat = px.imshow(
                        pivot,
                        color_continuous_scale=["#2ecc71", "#f39c12", "#e74c3c"],
                        aspect="auto",
                        text_auto=".2f",
                    )
                    fig_heat.update_layout(
                        height=max(300, len(itens) * 38),
                        font=dict(family="Sora", size=11),
                        margin=dict(t=10, b=10),
                        coloraxis_colorbar=dict(title="R$"),
                    )
                    st.plotly_chart(fig_heat, use_container_width=True)

    # ── SEÇÃO: FUI AO MERCADO ──
    st.markdown("---")
    st.markdown("### 🏃 Fui ao Mercado!")
    col_fui1, col_fui2 = st.columns([1, 1])

    with col_fui1:
        mercado_escolhido = st.selectbox(
            "Em qual mercado você foi (ou vai)?",
            MERCADOS,
            key="sel_mercado_visita"
        )
        if st.button("✅ Confirmar Visita ao Mercado", key="btn_fui"):
            st.session_state["trafego_total"] += 1
            if mercado_escolhido not in st.session_state["lojas_visitadas"]:
                st.session_state["lojas_visitadas"].append(mercado_escolhido)
            st.balloons()
            st.success(f"🎉 Ótimo! Visita ao **{mercado_escolhido}** confirmada! "
                       f"Você está ajudando nossa comunidade de consumidores. "
                       f"Tráfego 4SAVR acumulado: **{st.session_state['trafego_total']} visitas**")

    with col_fui2:
        st.markdown("#### 📸 Validação de Nota Fiscal")
        st.markdown("*Envie sua NF ou foto do cupom para ganhar Score de Confiança*")
        uploaded = st.file_uploader(
            "Upload NF / Foto de Cupom", type=["jpg","jpeg","png","pdf"],
            key="upload_nf", label_visibility="collapsed"
        )
        if uploaded is not None:
            pontos = random.randint(8, 25)
            st.session_state["score_confianca"] += pontos
            st.session_state["historico_validacoes"].append({
                "arquivo": uploaded.name,
                "pontos": pontos,
                "data": datetime.datetime.now().strftime("%d/%m %H:%M"),
            })
            st.success(f"✅ Arquivo **{uploaded.name}** recebido! "
                       f"+{pontos} pontos de confiança adicionados ao seu perfil.")

        score = st.session_state["score_confianca"]
        nivel = "🥉 Bronze" if score < 50 else ("🥈 Prata" if score < 150 else "🥇 Ouro")
        st.markdown(f"""
        <div style="text-align:center;margin-top:0.8rem">
          <div class="score-badge">{score}</div>
          <div style="font-family:'Sora',sans-serif;font-weight:700;margin-top:0.4rem">{nivel}</div>
          <div style="color:#889aab;font-size:0.8rem">Score de Confiança 4SAVR</div>
        </div>
        """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════
#  ABA 2: LOJISTA
# ══════════════════════════════════════════════════════════════════════
with tab_lojista:
    # KPIs rápidos no topo
    st.markdown("### 🏬 Painel do Lojista — BI em Tempo Real")
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("🚶 Tráfego 4SAVR", f"{st.session_state['trafego_total']}", "+3 hoje")
    k2.metric("🔍 Itens Buscados", f"{len(st.session_state['buscas_por_item'])}", "na sua região")
    k3.metric("⭐ Score Médio Clientes", "73 pts", "+12 esta semana")
    k4.metric("📦 Itens em Alerta", f"{(df_estoque['Dias para Vencer'] < 20).sum()}", "perto do vencimento")

    st.markdown("---")
    tab_bi, tab_marcas, tab_validade = st.tabs([
        "🧠  Inteligência de Mercado",
        "🏷️  Marcas & Giro",
        "⚠️  Prevenção de Desperdício"
    ])

    # ────────────────────────────────────────────
    # TAB B2B-1: INTELIGÊNCIA DE MERCADO
    # ────────────────────────────────────────────
    with tab_bi:
        col_a, col_b = st.columns([3, 2], gap="large")

        with col_a:
            st.markdown("#### 📈 Comparativo de Preços — Seu mercado vs. Grandes Redes")
            item_cmp = st.selectbox("Selecionar item para comparar:", TODOS_ITENS, key="sel_item_bi")

            precos_item = PRECOS_BASE[item_cmp]
            df_cmp = pd.DataFrame([
                {"Mercado": m, "Preço": p, "Tipo": "Sua Loja" if m == "Condor" else "Concorrente"}
                for m, p in sorted(precos_item.items(), key=lambda x: x[1])
            ])
            colors_cmp = [
                "#2ecc71" if t == "Sua Loja" else CORES_MERCADO[m]
                for m, t in zip(df_cmp["Mercado"], df_cmp["Tipo"])
            ]

            fig_cmp = go.Figure(go.Bar(
                x=df_cmp["Mercado"],
                y=df_cmp["Preço"],
                marker_color=colors_cmp,
                text=[f"R$ {v:.2f}" for v in df_cmp["Preço"]],
                textposition="outside",
            ))
            fig_cmp.update_layout(
                plot_bgcolor="white", paper_bgcolor="white",
                font=dict(family="Sora"),
                yaxis=dict(title="R$", showgrid=True, gridcolor="#eef2f7"),
                height=350, margin=dict(t=10, b=10), showlegend=False,
            )
            # Linha de média
            media = df_cmp["Preço"].mean()
            fig_cmp.add_hline(
                y=media, line_dash="dot", line_color="#f39c12",
                annotation_text=f"Média R$ {media:.2f}", annotation_position="top right"
            )
            st.plotly_chart(fig_cmp, use_container_width=True)

            preco_loja = precos_item["Condor"]
            preco_min  = min(precos_item.values())
            diff_min   = preco_loja - preco_min
            if diff_min > 0:
                st.warning(f"⚠️ Seu preço está **R$ {diff_min:.2f} acima** do mais barato da região. "
                           f"Considere ajustar para reter clientes 4SAVR.")
            else:
                st.success(f"✅ Parabéns! Você já tem o **menor preço** para {item_cmp} na região!")

        with col_b:
            st.markdown("#### 🎯 Radar de Procura — Bairro")
            st.markdown("*Itens mais buscados por consumidores 4SAVR na sua região agora*")

            buscas = radar_buscas()
            top_buscas = sorted(buscas.items(), key=lambda x: x[1], reverse=True)[:10]
            df_radar = pd.DataFrame(top_buscas, columns=["Item", "Buscas"])
            df_radar["Item_curto"] = df_radar["Item"].str.replace(r"\s\d.*", "", regex=True)

            fig_radar = go.Figure(go.Bar(
                x=df_radar["Buscas"],
                y=df_radar["Item_curto"],
                orientation="h",
                marker=dict(
                    color=df_radar["Buscas"],
                    colorscale=[[0, "#a8c8e8"], [1, "#001f3f"]],
                ),
                text=df_radar["Buscas"],
                textposition="outside",
            ))
            fig_radar.update_layout(
                plot_bgcolor="white", paper_bgcolor="white",
                font=dict(family="Sora"),
                xaxis=dict(showgrid=False),
                yaxis=dict(autorange="reversed"),
                height=380, margin=dict(t=10, b=10),
            )
            st.plotly_chart(fig_radar, use_container_width=True)

        # Tráfego 4SAVR timeline simulada
        st.markdown("#### 🚶 Histórico de Tráfego 4SAVR — Últimos 30 dias")
        dias = pd.date_range(end=datetime.date.today(), periods=30)
        trafego_hist = np.random.poisson(lam=4, size=30)
        trafego_hist[-1] += st.session_state["trafego_total"] - 47
        trafego_hist = np.clip(trafego_hist, 0, None)

        fig_traf = go.Figure()
        fig_traf.add_trace(go.Scatter(
            x=dias, y=trafego_hist.cumsum(),
            fill="tozeroy", fillcolor="rgba(46,204,113,0.15)",
            line=dict(color="#2ecc71", width=2.5),
            name="Tráfego acumulado",
        ))
        fig_traf.add_trace(go.Bar(
            x=dias, y=trafego_hist,
            marker_color="#001f3f", opacity=0.5,
            name="Visitas/dia",
        ))
        fig_traf.update_layout(
            plot_bgcolor="white", paper_bgcolor="white",
            font=dict(family="Sora"), height=280,
            legend=dict(orientation="h", yanchor="bottom", y=1),
            margin=dict(t=30, b=10),
        )
        st.plotly_chart(fig_traf, use_container_width=True)

    # ────────────────────────────────────────────
    # TAB B2B-2: MARCAS & GIRO
    # ────────────────────────────────────────────
    with tab_marcas:
        col_m1, col_m2 = st.columns([3, 2], gap="large")

        with col_m1:
            st.markdown("#### 🏷️ Análise de Performance por Marca")
            categoria_sel = st.selectbox("Categoria:", list(MARCAS.keys()), key="sel_cat_marca")
            marcas_lista  = MARCAS[categoria_sel]

            # Giro simulado por marca
            np.random.seed(hash(categoria_sel) % 100)
            giro      = np.random.randint(20, 200, len(marcas_lista))
            interesse = np.random.randint(10, 100, len(marcas_lista))
            margem    = np.random.uniform(0.08, 0.28, len(marcas_lista))

            df_marcas = pd.DataFrame({
                "Marca":    marcas_lista,
                "Giro (un/sem)": giro,
                "Interesse (cliques)": interesse,
                "Margem (%)": (margem * 100).round(1),
            })

            fig_marcas = go.Figure()
            fig_marcas.add_trace(go.Bar(
                name="Giro (un/sem)", x=df_marcas["Marca"], y=df_marcas["Giro (un/sem)"],
                marker_color="#001f3f",
            ))
            fig_marcas.add_trace(go.Bar(
                name="Interesse (cliques)", x=df_marcas["Marca"], y=df_marcas["Interesse (cliques)"],
                marker_color="#2ecc71",
            ))
            fig_marcas.update_layout(
                barmode="group", plot_bgcolor="white", paper_bgcolor="white",
                font=dict(family="Sora"), height=340, margin=dict(t=10, b=10),
            )
            st.plotly_chart(fig_marcas, use_container_width=True)

            # Scatter: margem vs giro
            fig_sc = px.scatter(
                df_marcas, x="Giro (un/sem)", y="Margem (%)",
                text="Marca", size="Interesse (cliques)",
                color="Marca",
                color_discrete_sequence=["#001f3f","#2ecc71","#f39c12","#e74c3c"],
            )
            fig_sc.update_traces(textposition="top center")
            fig_sc.update_layout(
                plot_bgcolor="white", paper_bgcolor="white",
                font=dict(family="Sora"), height=300,
                showlegend=False, margin=dict(t=10),
            )
            st.plotly_chart(fig_sc, use_container_width=True)

        with col_m2:
            st.markdown("#### 📦 Sugestão de Pedido ao Distribuidor")
            st.markdown("*Baseado no giro médio e estoque atual*")

            for _, row in df_marcas.iterrows():
                semanas_ideal  = 3
                qtd_ideal      = row["Giro (un/sem)"] * semanas_ideal
                estoque_atual  = random.randint(10, 80)
                pedido_sugere  = max(0, qtd_ideal - estoque_atual)

                cor_card = "#f0fff6" if pedido_sugere < 30 else "#fff8e1" if pedido_sugere < 80 else "#fff3f3"
                icon = "🟢" if pedido_sugere < 30 else ("🟡" if pedido_sugere < 80 else "🔴")
                st.markdown(f"""
                <div style="background:{cor_card};border-radius:10px;padding:0.8rem 1rem;margin-bottom:0.7rem;border:1px solid #e0e8f0">
                  <div style="font-family:'Sora',sans-serif;font-weight:700;font-size:0.95rem">{icon} {row['Marca']}</div>
                  <div style="font-size:0.82rem;color:#556;margin-top:0.2rem">
                    Estoque atual: <b>{estoque_atual} un</b> &nbsp;|&nbsp; Giro: <b>{row['Giro (un/sem)']} un/sem</b>
                  </div>
                  <div style="font-size:0.95rem;font-weight:700;color:#001f3f;margin-top:0.3rem">
                    📋 Pedido sugerido: <span style="color:#2ecc71">{pedido_sugeres:.0f} un</span>
                  </div>
                </div>
                """.replace("pedido_sugeres", str(int(pedido_sugere))), unsafe_allow_html=True)

            st.markdown("---")
            st.caption("💡 *Quantidade ideal = 3 semanas de estoque. Ajuste conforme sazonalidade.*")

    # ────────────────────────────────────────────
    # TAB B2B-3: PREVENÇÃO DE DESPERDÍCIO
    # ────────────────────────────────────────────
    with tab_validade:
        st.markdown("#### ⚠️ Radar de Validade & Prevenção de Desperdício")

        # Filtro
        filtro_dias = st.slider("Mostrar itens com vencimento em até (dias):", 7, 90, 30, key="sl_dias")
        df_alerta = df_estoque[df_estoque["Dias para Vencer"] <= filtro_dias].sort_values("Dias para Vencer")

        col_v1, col_v2 = st.columns([3, 2], gap="large")

        with col_v1:
            if df_alerta.empty:
                st.success("✅ Nenhum item com vencimento nos próximos dias. Ótima gestão!")
            else:
                for _, row in df_alerta.iterrows():
                    critico = row["Dias para Vencer"] <= 10
                    classe  = "alert-card danger" if critico else "alert-card"
                    icon    = "🚨" if critico else "⚠️"
                    badge   = f"<b style='color:#e74c3c'>CRÍTICO</b>" if critico else "<b style='color:#f39c12'>Atenção</b>"

                    # Verificar se já tem promoção ativa
                    tem_promo = row["Item"] in st.session_state["promo_relampago"]
                    promo_html = "<span style='background:#2ecc71;color:white;border-radius:10px;padding:2px 10px;font-size:0.78rem'>🏷️ PROMOÇÃO ATIVA</span>" if tem_promo else ""

                    st.markdown(f"""
                    <div class="{classe}">
                      <div style="font-family:'Sora',sans-serif;font-weight:700;font-size:0.95rem">
                        {icon} {row['Item']} {promo_html}
                      </div>
                      <div style="font-size:0.82rem;margin-top:0.3rem;color:#556">
                        Vence em: <b>{row['Dias para Vencer']} dias</b> ({row['Validade'].strftime('%d/%m/%Y')})
                        &nbsp;|&nbsp; Estoque: <b>{row['Estoque (un)']} un</b>
                        &nbsp;|&nbsp; Giro: <b>{row['Giro Semanal']} un/sem</b>
                        &nbsp;|&nbsp; {badge}
                      </div>
                    </div>
                    """, unsafe_allow_html=True)

                    if not tem_promo:
                        if st.button(
                            f"📣 Criar Promoção Relâmpago — {row['Item']}",
                            key=f"promo_{row['Item']}"
                        ):
                            st.session_state["promo_relampago"].append(row["Item"])
                            st.success(f"🎉 Promoção Relâmpago criada para **{row['Item']}**! "
                                       f"Notificação enviada para **{random.randint(80, 340)} consumidores** "
                                       f"da sua região via app 4SAVR.")
                            st.rerun()

        with col_v2:
            # Gráfico donut: distribuição de urgência
            d_ok      = (df_estoque["Dias para Vencer"] > 30).sum()
            d_atencao = ((df_estoque["Dias para Vencer"] > 10) & (df_estoque["Dias para Vencer"] <= 30)).sum()
            d_critico = (df_estoque["Dias para Vencer"] <= 10).sum()

            fig_donut = go.Figure(go.Pie(
                values=[d_ok, d_atencao, d_critico],
                labels=["OK (>30d)", "Atenção (11-30d)", "Crítico (≤10d)"],
                hole=0.55,
                marker=dict(colors=["#2ecc71", "#f39c12", "#e74c3c"]),
                textinfo="label+percent",
                textfont=dict(family="Sora", size=11),
            ))
            fig_donut.update_layout(
                font=dict(family="Sora"),
                paper_bgcolor="white",
                height=300,
                margin=dict(t=10, b=10),
                annotations=[dict(
                    text=f"<b>{len(df_estoque)}</b><br>itens",
                    x=0.5, y=0.5, font_size=16, showarrow=False,
                    font=dict(family="Sora", color="#001f3f"),
                )],
            )
            st.plotly_chart(fig_donut, use_container_width=True)

            # Scatter: estoque vs dias para vencer
            fig_est = px.scatter(
                df_estoque,
                x="Dias para Vencer", y="Estoque (un)",
                size="Giro Semanal", color="Dias para Vencer",
                color_continuous_scale=["#e74c3c","#f39c12","#2ecc71"],
                hover_name="Item",
                labels={"Dias para Vencer": "Dias p/ Vencer", "Estoque (un)": "Estoque"},
            )
            fig_est.update_layout(
                plot_bgcolor="white", paper_bgcolor="white",
                font=dict(family="Sora"), height=280,
                margin=dict(t=10, b=10),
                coloraxis_showscale=False,
            )
            fig_est.add_vline(x=10, line_dash="dot", line_color="#e74c3c", annotation_text="Crítico")
            fig_est.add_vline(x=30, line_dash="dot", line_color="#f39c12", annotation_text="Atenção")
            st.plotly_chart(fig_est, use_container_width=True)

        # Promoções ativas
        if st.session_state["promo_relampago"]:
            st.markdown("---")
            st.markdown("#### 🏷️ Promoções Relâmpago Ativas")
            promo_cols = st.columns(min(3, len(st.session_state["promo_relampago"])))
            for i, item_promo in enumerate(st.session_state["promo_relampago"]):
                with promo_cols[i % 3]:
                    desc = random.randint(10, 30)
                    preco_orig = PRECOS_BASE.get(item_promo, {}).get("Condor", 10.0)
                    preco_promo = preco_orig * (1 - desc / 100)
                    st.markdown(f"""
                    <div style="background:linear-gradient(135deg,#001f3f,#003366);border-radius:12px;
                                padding:1rem;color:white;text-align:center">
                      <div style="font-size:0.8rem;color:#a8c8e8">PROMOÇÃO RELÂMPAGO</div>
                      <div style="font-family:'Sora',sans-serif;font-weight:700;font-size:0.95rem;
                                  margin:0.4rem 0">{item_promo}</div>
                      <div style="text-decoration:line-through;color:#a8c8e8;font-size:0.85rem">
                        R$ {preco_orig:.2f}</div>
                      <div style="font-size:1.6rem;font-weight:800;color:#2ecc71">
                        R$ {preco_promo:.2f}</div>
                      <div style="background:#2ecc71;border-radius:10px;padding:2px 8px;
                                  font-size:0.8rem;font-weight:700;display:inline-block;margin-top:0.3rem">
                        -{desc}% OFF</div>
                    </div>
                    """, unsafe_allow_html=True)

# ── FOOTER ──
st.markdown("""
<div class="footer-note">
  4SAVR MVP v4.0 &nbsp;|&nbsp; Dados simulados para demonstração &nbsp;|&nbsp;
  Desenvolvido com ❤️ para o comércio local de Curitiba &nbsp;|&nbsp; 🛒
</div>
""", unsafe_allow_html=True)
