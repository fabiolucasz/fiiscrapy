import streamlit as st
import pandas as pd

df = pd.read_csv("merge.csv")

st.title("FII")
st.write("Bem-vindo ao FII")
st.write("Esse é um projeto para auxiliar na busca de FII")

st.write("Filtrados")
st.dataframe(df)


