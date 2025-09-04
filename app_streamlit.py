import time
import random
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Demo Streamlit en Raspberry Pi", layout="centered")

st.title("Demo de Streamlit en Raspberry Pi 3")
st.caption("Serie de temperatura simulada con KPIs simples")

if "serie" not in st.session_state:
    base = 24.0
    st.session_state.serie = [round(base + random.uniform(-0.3, 0.3), 2) for _ in range(24)]

def nueva_muestra(valor):
    paso = random.uniform(-0.35, 0.6)
    nuevo = max(min(valor + paso, 30.0), 18.0)
    return round(nuevo, 2)

last = st.session_state.serie[-1]
st.session_state.serie.append(nueva_muestra(last))
if len(st.session_state.serie) > 120:
    st.session_state.serie = st.session_state.serie[-120:]

df = pd.DataFrame({"muestra": range(len(st.session_state.serie)),
                   "temperatura_c": st.session_state.serie})

fig = px.line(df, x="muestra", y="temperatura_c", title="Temperatura simulada")
fig.update_traces(mode="lines+markers")

c1, c2, c3 = st.columns(3)
c1.metric("Última", f"{df['temperatura_c'].iloc[-1]:.2f} °C")
c2.metric("Promedio", f"{df['temperatura_c'].mean():.2f} °C")
c3.metric("Rango", f"{df['temperatura_c'].min():.2f} °C — {df['temperatura_c'].max():.2f} °C")

st.plotly_chart(fig, use_container_width=True)

st.info("Ejecuta con:  streamlit run app_streamlit.py --server.address 0.0.0.0 --server.port 8501")
