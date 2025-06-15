import requests
import pandas as pd
from bs4 import BeautifulSoup

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}



def get_fiis():
    url = "https://www.fundamentus.com.br/fii_resultado.php"
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find('table')
    df = pd.read_html(str(table))[0]
    return df

def get_data_com(papel: str):
    url = f"https://investidor10.com.br/fiis/{papel.lower()}/"
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find_all('table', class_="table")
    #tabela datacom
    #table = soup.find_all('table', class_="table-balance")
    df = pd.read_html(str(table))[0]
    return df


def get_fiis_complement(papel: str):
    url = f"https://investidor10.com.br/fiis/{papel.lower()}/"
    response = requests.get(url, headers=headers)

    soup = BeautifulSoup(response.text, 'html.parser')

    titulos = [item.text.strip() for item in soup.find_all('span', class_="name")]
    valores = [item.text.strip() for item in soup.find_all('div', class_="value")]
    
    dados = dict(zip(titulos, valores))
    dados["Papel"] = papel

    return dados

fiis =pd.read_csv("fiis.csv", quotechar='"', sep=',', decimal='.', encoding='utf-8', skipinitialspace=True)
#tickers = fiis["Papel"].tolist()


#dados_fiis = []
#for ticker in tickers:
#    dados = get_fiis_complement(ticker)
#    if dados:
#        dados_fiis.append(dados)

# Converte para DataFrame e salva
#df = pd.DataFrame(dados_fiis)
#df.to_csv("dados_investidor10.csv", index=False)

df2 = pd.read_csv("dados_investidor10.csv")

#concat = pd.concat([fiis, df2], ignore_index=True)
#concat.to_csv("concat.csv", index=False)

merge = pd.merge(fiis, df2, on="Papel", how="inner")
merge.to_csv("merge.csv", index=False)