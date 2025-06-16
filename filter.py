import pandas as pd
liquidez_minima = 1_500_000
pvp = 0.85

def filtrar_fiis(liquidez_minima, pvp):
    df = pd.read_csv("df1_tratado.csv", quotechar='"', sep=',', decimal='.', encoding='utf-8', skipinitialspace=True)
    segmentos_permitidos = ["Logística", "Shoppings", "Híbrido", "Lajes Corporativas"]
    df = df[df["Liquidez"] >= liquidez_minima]
    df = df[df["P/VP"] >= pvp]
    df = df[df["Segmento"].isin(segmentos_permitidos)]
    df = df.sort_values(by="Dividend Yield", ascending=False)

    print("\n Original")
    print(df)

    
    df.to_csv("df1_filtro.csv", index=False)
    return df

filtrar_fiis(liquidez_minima, pvp)



#print("\n Logística")
#df_logistica = df_filtrado[df_filtrado["Segmento"] == "Logística"]
#df_logistica = df_logistica.sort_values(by="Dividend Yield", ascending=False)
#print(df_logistica)

#print("\n Shoppings")
#df_shoppings = df_filtrado[df_filtrado["Segmento"] == "Shoppings"]
#df_shoppings = df_shoppings.sort_values(by="Dividend Yield", ascending=False)
#print(df_shoppings)

#print("\n Híbrido")
#df_hibrido = df_filtrado[df_filtrado["Segmento"] == "Híbrido"]
#df_hibrido = df_hibrido.sort_values(by="Dividend Yield", ascending=False)
#print(df_hibrido)

#print("\n Lajes Corporativas")
#df_lajes_corporativas = df_filtrado[df_filtrado["Segmento"] == "Lajes Corporativas"]
#df_lajes_corporativas = df_lajes_corporativas.sort_values(by="Dividend Yield", ascending=False)
#print(df_lajes_corporativas)

# (Opcional) salvar em novo CSV
#df_filtrado.to_csv("fiis_filtrados.csv", index=False)
