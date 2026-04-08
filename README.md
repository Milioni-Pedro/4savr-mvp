# 🛒 4SAVR MVP v4.0 — Deploy Guide

## O que é o 4SAVR?
Plataforma de comparação de preços para a Cesta Básica em Curitiba-PR, com painel B2C (consumidor) e B2B (lojista), otimização de compra em múltiplos mercados e alertas de validade/desperdício.

---

## 📁 Estrutura de Arquivos

```
4savr/
├── app.py            ← Código principal do MVP
├── requirements.txt  ← Dependências Python
└── README.md         ← Este arquivo
```

---

## 🚀 Deploy Gratuito — Passo a Passo

### PASSO 1 — Criar conta no GitHub (se não tiver)
1. Acesse https://github.com/signup
2. Crie sua conta gratuitamente

### PASSO 2 — Criar repositório no GitHub
1. Clique em **"New repository"**
2. Nome: `4savr-mvp` (ou qualquer nome)
3. Marque como **Public**
4. Clique em **"Create repository"**

### PASSO 3 — Fazer upload dos arquivos
**Opção A — Pelo navegador (mais fácil):**
1. Na página do repositório, clique em **"Add file > Upload files"**
2. Arraste os arquivos `app.py` e `requirements.txt`
3. Clique em **"Commit changes"**

**Opção B — Via Git (terminal):**
```bash
git init
git add app.py requirements.txt
git commit -m "4SAVR MVP v4.0"
git branch -M main
git remote add origin https://github.com/SEU_USUARIO/4savr-mvp.git
git push -u origin main
```

### PASSO 4 — Criar conta no Streamlit Cloud
1. Acesse https://streamlit.io/cloud
2. Clique em **"Sign up for free"**
3. Faça login com sua conta do GitHub (**recomendado** — facilita o acesso ao repositório)

### PASSO 5 — Deploy do App
1. No Streamlit Cloud, clique em **"New app"**
2. Selecione:
   - **Repository:** `SEU_USUARIO/4savr-mvp`
   - **Branch:** `main`
   - **Main file path:** `app.py`
3. Clique em **"Deploy!"**
4. Aguarde ~2 minutos e seu app estará online! 🎉

### URL do seu app
Será algo como:
```
https://seu-usuario-4savr-mvp-app-XXXXXX.streamlit.app
```

---

## 🔄 Como atualizar o app
Sempre que você fizer um novo commit/push para o repositório GitHub,
o Streamlit Cloud vai **redeploy automaticamente** em ~30 segundos.

---

## 🛠️ Rodar localmente (desenvolvimento)

### Requisitos
- Python 3.9 ou superior
- pip

### Comandos
```bash
# 1. Instalar dependências
pip install -r requirements.txt

# 2. Rodar o app
streamlit run app.py

# O app abre automaticamente em: http://localhost:8501
```

---

## 📦 Dependências (todas gratuitas)

| Pacote      | Versão mínima | Uso                        |
|-------------|--------------|----------------------------|
| streamlit   | 1.32.0       | Framework de interface     |
| pandas      | 2.0.0        | Manipulação de dados       |
| numpy       | 1.26.0       | Cálculos numéricos         |
| plotly      | 5.20.0       | Gráficos interativos       |

---

## 🗺️ Funcionalidades do MVP

### 🛍️ Aba Consumidor
- ✅ Configurador de cesta com 15 itens agrupados por categoria
- ✅ Cenário 1: Conveniência (1 mercado mais barato)
- ✅ Cenário 2: Economia Máxima (melhor preço item a item)
- ✅ Cenário 3: Resumo com R$ economizados e % de desconto
- ✅ Heatmap de preços por item e mercado
- ✅ Gráfico de barras comparativo entre os 6 mercados
- ✅ Botão "Fui ao Mercado" com gamificação e balões
- ✅ Upload simulado de NF para Score de Confiança

### 📊 Aba Lojista
- ✅ KPIs: tráfego, buscas, score, alertas
- ✅ Comparativo de preços item a item vs concorrentes
- ✅ Radar de Procura (itens mais buscados no bairro)
- ✅ Histórico de tráfego 4SAVR (30 dias)
- ✅ Análise de marcas por giro e interesse
- ✅ Sugestão de pedido ao distribuidor
- ✅ Alertas de validade com semáforo (verde/amarelo/vermelho)
- ✅ Botão "Promoção Relâmpago" com notificação simulada
- ✅ Cards de promoção com % desconto calculado

---

## 🔮 Próximos Passos (Roadmap)

1. **Integração real de preços** via scraping ou API de supermercados
2. **Autenticação** de consumidores e lojistas (st.secrets + supabase)
3. **Banco de dados** persistente (Supabase PostgreSQL — free tier)
4. **Geolocalização** para identificar mercados próximos
5. **Push notifications** para promoções relâmpago
6. **App mobile** com React Native (exportar lógica do backend)

---

## 💡 Dicas de Customização

### Alterar os mercados ou preços
Edite o dicionário `PRECOS_BASE` no início do `app.py`.

### Adicionar mais itens à cesta
Adicione ao dicionário `PRECOS_BASE` e aos grupos em `grupos` na Aba Consumidor.

### Mudar "Condor" pelo nome do lojista
Procure por `"Condor"` no código e substitua pelo nome desejado.

---

*4SAVR MVP v4.0 — Economize na Cesta Básica, Curitiba-PR*
