import pandas as pd

df = pd.read_csv("fiis.csv", quotechar='"', sep=',', decimal='.', encoding='utf-8', skipinitialspace=True)
lista_colunas = ["Papel", "Segmento", "Cotação", "FFO Yield", "Dividend Yield", "P/VP", "Valor de Mercado", "Liquidez", "Qtd de imóveis", "Preço do m2", "Aluguel por m2", "Cap Rate", "Vacância Média"]


colunas_percentuais = ["FFO Yield", "Dividend Yield", "Cap Rate", "Vacância Média"]
colunas_valores = ["Valor de Mercado", "Liquidez"]
colunas_inteiras = ["Qtd de imóveis"]
colunas_cotacao = ["Cotação"]
colunas_pvp = ["P/VP"]

#tratar as duas colunas depois
colunas_preco_m2 = ["Preço do m2"]
colunas_aluguel_m2 = ["Aluguel por m2"]


for col in colunas_percentuais:
    df[col] = df[col].astype(str).str.replace("%", "", regex=False).str.replace(",", ".")
    df[col] = pd.to_numeric(df[col], errors="coerce")

for col in colunas_valores:
    df[col] = df[col].astype(str).str.replace(".", "", regex=False).str.replace(",", ".", regex=False)
    df[col] = pd.to_numeric(df[col], errors="coerce")


for col in colunas_inteiras:
    df[col] = pd.to_numeric(df[col], errors="coerce", downcast="integer")

for col in colunas_cotacao:
    df[col] = df[col].astype(str).str.replace(r"\D", "", regex=True)  
    df[col] = df[col].apply(
        lambda x: float(x.zfill(3)[:-2] + "." + x.zfill(3)[-2:]) if x else None
    )

def pvp(x):
    x = x.strip()
    if not x.isdigit():
        return None
    if len(x) > 2:
        return float(x[:-2] + "." + x[-2:])
    else:
        return float("0." + x)


for col in colunas_pvp:
    df[col] = df[col].astype(str).str.replace(r"\D", "", regex=True)
    df[col] = df[col].apply(pvp)



# ✅ Ver resultado
#print(df.dtypes)
#print(df.head())


#print(df)

liquidez_minima = 1_500_000
pvp = 0.01
#Pesquisar depois empresas classificadas como Papel na bolsa
segmentos_permitidos = ["Logística", "Shoppings", "Híbrido", "Lajes Corporativas"]
df_filtrado = df[df["Liquidez"] >= liquidez_minima]
df_filtrado = df_filtrado[df_filtrado["P/VP"] >= pvp]
df_filtrado = df_filtrado[df_filtrado["Segmento"].isin(segmentos_permitidos)]
df_filtrado = df_filtrado.sort_values(by="Dividend Yield", ascending=False)

print("\n Original")
print(df_filtrado)

print("\n Logística")
df_logistica = df_filtrado[df_filtrado["Segmento"] == "Logística"]
df_logistica = df_logistica.sort_values(by="Dividend Yield", ascending=False)
print(df_logistica)

print("\n Shoppings")
df_shoppings = df_filtrado[df_filtrado["Segmento"] == "Shoppings"]
df_shoppings = df_shoppings.sort_values(by="Dividend Yield", ascending=False)
print(df_shoppings)

print("\n Híbrido")
df_hibrido = df_filtrado[df_filtrado["Segmento"] == "Híbrido"]
df_hibrido = df_hibrido.sort_values(by="Dividend Yield", ascending=False)
print(df_hibrido)

print("\n Lajes Corporativas")
df_lajes_corporativas = df_filtrado[df_filtrado["Segmento"] == "Lajes Corporativas"]
df_lajes_corporativas = df_lajes_corporativas.sort_values(by="Dividend Yield", ascending=False)
print(df_lajes_corporativas)

# (Opcional) salvar em novo CSV
df_filtrado.to_csv("fiis_filtrados.csv", index=False)
