import requests
import pandas as pd
from bs4 import BeautifulSoup

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

liquidez_minima = 2_000_000
pvp = 0.75

def get_fiis():
    url = "https://www.fundamentus.com.br/fii_resultado.php"
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find('table')
    df = pd.read_html(str(table))[0]
    df.to_csv("df1.csv", index=False)
    df = tratar_df1()
    df.to_csv("df1.csv", index=False)
    return df

def filtrar_fiis(liquidez_minima, pvp):
    df = pd.read_csv("df1.csv", quotechar='"', sep=',', decimal='.', encoding='utf-8', skipinitialspace=True)
    segmentos_permitidos = ["Logística", "Shoppings", "Híbrido", "Lajes Corporativas"]
    df = df[df["Liquidez"] >= liquidez_minima]
    df = df[df["P/VP"] >= pvp]
    #df = df[df["Segmento"].isin(segmentos_permitidos)]
    df = df.sort_values(by="Dividend Yield", ascending=False)
    return df
def tratar_df1():
    df = pd.read_csv("df1.csv", quotechar='"', sep=',', decimal='.', encoding='utf-8', skipinitialspace=True)
    df = df.drop(columns=["Preço do m2", "Aluguel por m2"], errors="ignore")

    colunas_percentuais = ["FFO Yield", "Dividend Yield", "Cap Rate", "Vacância Média"]
    colunas_valores = ["Valor de Mercado", "Liquidez"]
    colunas_inteiras = ["Qtd de imóveis"]
    colunas_cotacao = ["Cotação"]
    colunas_pvp = ["P/VP"]

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
    return df

def get_data_com():
    fiis =pd.read_csv("fiis.csv", quotechar='"', sep=',', decimal='.', encoding='utf-8', skipinitialspace=True)
    tickers = fiis["Papel"].tolist()
    todos_os_fiis = []
    for papel in tickers:
        print(f"Processando data com de: {papel}")
        url = f"https://investidor10.com.br/fiis/{papel}/"
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')

        table = soup.find_all('table', class_="table")
        df = pd.read_html(str(table))[0]

        dados_fiis = dict(zip(titulos, valores))
        dados_fiis["Papel"] = papel
        todos_os_fiis.append(dados_fiis)

    df = pd.DataFrame(todos_os_fiis)
    df.to_csv("data_com.csv", index=False)
    return df

def merge_fiis():
    df1 = filtrar_fiis(liquidez_minima, pvp)
    df2 = pd.read_csv("df2.csv")
    merge = pd.merge(df1, df2, on="Papel", how="inner")
    merge.to_csv("merge.csv", index=False)
    merge = pd.read_csv("merge.csv")
    ordem = ["Papel", "Segmento", "TIPO DE FUNDO", "VAL. PATRIMONIAL P/ COTA", "Cotação", "Dividend Yield", "P/VP", "ÚLTIMO RENDIMENTO", "FFO Yield", "Liquidez", "Valor de Mercado", "Qtd de imóveis", "Cap Rate", "Vacância Média", "VALOR PATRIMONIAL"]
    merge = merge[ordem]
    merge.to_csv("merge.csv", index=False)
    return merge

def tratar_df2():
    df = pd.read_csv("df2.csv", quotechar='"', sep=',', decimal='.', encoding='utf-8', skipinitialspace=True)
    

    df = df.drop(columns=["Razão Social", "CNPJ", "PÚBLICO-ALVO", "MANDATO", "SEGMENTO", "PRAZO DE DURAÇÃO", "TIPO DE GESTÃO", "TAXA DE ADMINISTRAÇÃO", "VACÂNCIA", "COTAS EMITIDAS", "NUMERO DE COTISTAS"], errors="ignore")
    
    return df

def get_fiis_complement():
    #fiis =pd.read_csv("df1_filtro.csv", quotechar='"', sep=',', decimal='.', encoding='utf-8', skipinitialspace=True)
    fiis = filtrar_fiis(liquidez_minima, pvp)
    tickers = fiis["Papel"].tolist()
    todos_os_fiis = []
    for papel in tickers:
        print(f"Processando complemento de: {papel}")

        url = f"https://investidor10.com.br/fiis/{papel}/"
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')

        titulos = [item.text.strip() for item in soup.find_all('span', class_="name")]
        valores = [item.text.strip() for item in soup.find_all('div', class_="value")]

        dados_fiis = dict(zip(titulos, valores))
        dados_fiis["Papel"] = papel
        todos_os_fiis.append(dados_fiis)
    
    df = pd.DataFrame(todos_os_fiis)
    df.to_csv("df2.csv", index=False)
    df = tratar_df2()
    df.to_csv("df2.csv", index=False)
    merge_fiis()
    return df


def iniciar():
    get_fiis()
    get_fiis_complement()
    #get_data_com()

iniciar()
