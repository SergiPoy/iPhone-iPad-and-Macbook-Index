
# Importem les llibreries necessàries
import csv
import json
import bs4
import pandas as pd
import requests

# Modifiquem a la capçalera HTTP de les dades que user-agent que enviarem al fer el request
headers = {
    "User-Agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15"
}

# Recuperem els links, per a cada producte, de tots els països als que es comecialitzen
def recuperarLink(url):
    site_content = requests.get(url, headers=headers)
    htmlContent = site_content.content
    soup = bs4.BeautifulSoup(htmlContent, 'html.parser')
    links = []
    for data in soup.findAll('link', {'rel': 'alternate'}):
        links.append(data.get('href'))
    return links

# Recuperem els preus, producte i pais de cadascun dels links que s'introdueixen. Tornem el resultat en un DataFrame
def recuperarPrecios(url):
    site_content = requests.get(url, headers=headers)
    htmlContent = site_content.content
    soup = bs4.BeautifulSoup(htmlContent, 'html.parser')
    res = soup.find('script', {'id': 'metrics'})
    # Inicialitzem el DataFrame
    datos = pd.DataFrame()

    try:  # Com que tenim països als que no es poden comprar, gestionem les excepcions que apareixen
        # Ho fem a partir d'un JSON al que es llisten tots els preus que van sorgint al llarg dels links del website
        json_object = json.loads(res.contents[0])
        json_object_df = pd.DataFrame.from_dict(json_object)
        datos = pd.DataFrame(json_object_df['data']['products'])
        datos['currency'] = json_object_df['data']['currency']
        datos['country'] = url[22:24]
        datos['store'] = json_object_df['data']['properties'].get('computedCustomStoreName')
    except KeyError:
        datos = pd.DataFrame()
    finally:
        return datos

    return datos

#Definim els productes dels que anem a extraure els preus per a tots els països als que es comercialitzen
productes = ['https://www.apple.com/shop/buy-mac/macbook-air/m1-chip',
            'https://www.apple.com/shop/buy-mac/macbook-air/m2-chip',
            'https://www.apple.com/shop/buy-mac/macbook-pro/13-inch',
            'https://www.apple.com/shop/buy-mac/macbook-pro/14-inch',
            'https://www.apple.com/shop/buy-mac/macbook-pro/16-inch',
            'https://www.apple.com/shop/buy-mac/imac',
            'https://www.apple.com/shop/buy-ipad/ipad-pro',
            'https://www.apple.com/shop/buy-ipad/ipad-air',
            'https://www.apple.com/shop/buy-ipad/ipad',
            'https://www.apple.com/shop/buy-iphone/iphone-14-pro',
            'https://www.apple.com/shop/buy-iphone/iphone-14',
            'https://www.apple.com/iphone-se']

# Inicialitzem el DataFrame
dades_acum = pd.DataFrame()

for pagina in productes: # Anem treient els productes
    links = recuperarLink(pagina)
    for pagina_pais in links: #Anem treient els països per a cada producte
        dades = recuperarPrecios(pagina_pais)
        dades_acum = pd.concat([dades_acum, dades], axis=0)

# Ho guardem a un CSV
dades_acum.to_csv('preus_mac_ipad_iphone.csv', header=True, index=False)
