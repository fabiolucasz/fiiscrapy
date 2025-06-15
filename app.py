import streamlit as st
from filter import df_logistica, df_shoppings, df_hibrido, df_lajes_corporativas

st.title("FII")
st.write("Bem-vindo ao FII")
st.write("Esse é um projeto para auxiliar na busca de FII")

st.write("Logística")
st.dataframe(df_logistica)
st.write("Shoppings")
st.dataframe(df_shoppings)
st.write("Híbrido")
st.dataframe(df_hibrido)
st.write("Lajes Corporativas")
st.dataframe(df_lajes_corporativas)

