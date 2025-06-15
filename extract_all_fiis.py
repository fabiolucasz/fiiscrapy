import requests
import pandas as pd
from bs4 import BeautifulSoup

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}



def fundamentus_craw():
    url = "https://www.fundamentus.com.br/fii_resultado.php"
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find('table')
    df = pd.read_html(str(table))[0]
    return df



fundamentus_craw().to_csv("fiis.csv", index=False)





