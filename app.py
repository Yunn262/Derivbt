import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from deriv_client import DerivClient
from strategy import analyze_ticks, SYMBOLS

st.set_page_config(page_title="Deriv Signal Desk", page_icon="📈", layout="wide")
st.markdown("""
<style>
.stApp {background:#0b1220;color:#e8edf5}
[data-testid="stMetric"] {background:#121d30;border:1px solid #24334a;padding:14px;border-radius:12px}
.signal {padding:16px;border-radius:14px;background:#121d30;border:1px solid #24334a}
</style>
""", unsafe_allow_html=True)
st.title("📈 Deriv Signal Desk")
st.caption("Sinais técnicos Rise/Fall • Somente análise — não executa contratos")

with st.sidebar:
    st.header("Configuração")
    app_id = st.text_input("Deriv App ID", value="")
    token = st.text_input("Token API (opcional)", type="password", help="Para leitura pública, não é necessário. Não conceda permissões de negociação.")
    symbols = st.multiselect("Índices Volatility", options=list(SYMBOLS), default=["R_25","R_10","R_50","R_75","R_100"])
    duration = st.selectbox("Duração do sinal", [10], index=0, format_func=lambda x: f"{x} ticks")
    refresh = st.selectbox("Atualização automática", [5,10,15,30], index=1, format_func=lambda x:f"A cada {x} segundos")
    st.warning("Modo real significa observar mercado real. Este app não faz entradas nem promete resultados.")
    start = st.button("Conectar e analisar", type="primary", use_container_width=True)

if "results" not in st.session_state: st.session_state.results = []
if start:
    if not app_id.strip():
        st.error("Insira o App ID da Deriv. Crie um aplicativo no painel de desenvolvedor da Deriv.")
    elif not symbols:
        st.error("Escolha pelo menos um índice.")
    else:
        try:
            client=DerivClient(app_id.strip())
            with st.spinner("A ligar à Deriv e a recolher ticks…"):
                rows=[]
                for symbol in symbols:
                    ticks=client.get_ticks(symbol, count=300)
                    result=analyze_ticks(symbol, ticks)
                    rows.append(result)
            st.session_state.results=rows
            st.success("Dados recebidos. Avalie os sinais; são estimativas técnicas.")
        except Exception as e:
            st.error(f"Falha na conexão/dados: {e}")

if st.session_state.results:
    df=pd.DataFrame(st.session_state.results)
    cols=st.columns(3)
    cols[0].metric("Mercados analisados",len(df))
    cols[1].metric("Sinais",int(df["signal"].isin(["RISE","FALL"]).sum()))
    cols[2].metric("Aguardar",int((df["signal"]=="WAIT").sum()))
    for row in st.session_state.results:
        with st.container(border=True):
            a,b,c=st.columns([2,1,1])
            a.subheader(f"{row['name']} ({row['symbol']})")
            color="#1bbf83" if row["signal"]=="RISE" else "#f45b69" if row["signal"]=="FALL" else "#9aa8bd"
            a.markdown(f"<div class='signal'><h2 style='color:{color};margin:0'>{row['signal']}</h2><p>Entrada sugerida: {row['entry']}</p><p>Confiança heurística: {row['confidence']}%</p></div>",unsafe_allow_html=True)
            b.metric("RSI",f"{row['rsi']:.1f}")
            c.metric("Momentum",row["momentum"])
            st.caption(row["reason"])
            fig=go.Figure()
            fig.add_trace(go.Scatter(y=row["prices"],mode="lines",name="Ticks"))
            fig.update_layout(height=220,margin=dict(l=10,r=10,t=10,b=10),paper_bgcolor="#121d30",plot_bgcolor="#121d30",font_color="#e8edf5")
            st.plotly_chart(fig,use_container_width=True)
    st.dataframe(df.drop(columns=["prices"]),use_container_width=True,hide_index=True)

st.caption("O sinal não é garantia. Faça backtest/demo e nunca arrisque dinheiro que não pode perder.")
