import streamlit as st
import pandas as pd


st.title("FII")
st.write("Bem-vindo ao FII")


df = pd.read_csv("merge.csv")

liquidez_minima = st.sidebar.number_input("Liquidez mínima", value=2_000_000)
min_pvp = df["P/VP"].min()
max_pvp = df["P/VP"].max()
pvp = st.sidebar.slider("PVP", min_value=min_pvp, max_value=max_pvp,value=(min_pvp, max_pvp), step=0.01)
tipo_fundo = st.sidebar.selectbox("Tipo de fundo", ["Fundo de papel", "Outro", "Fundo misto"])

#segmentos_permitidos = ["Logística", "Shoppings", "Híbrido", "Lajes Corporativas"]
df = df[df["Liquidez"] >= liquidez_minima]
df = df[df["P/VP"] >= pvp[0]]
df = df[df["P/VP"] <= pvp[1]]
df = df[df["TIPO DE FUNDO"].isin([tipo_fundo])]
df = df.sort_values(by="Dividend Yield", ascending=False)


st.write("Esse é um projeto para auxiliar na busca de FII")

st.write("Filtrados")
st.dataframe(df)



