from bs4 import BeautifulSoup
import csv
import requests
import re

# Definim la capçalera del .csv que crearem al final i també definim les llistes buides.
cap_csv = ['Currency' , '1 EUR in Currency', '1 USD in Currency']
currency_name = [] 
twocurrency = []
currency_eur = []
currency_usd = []

# Modifiquem l'User-Agent per a que al moment d'executar el codi la pàgina ens identifiqui com un usuari comú.
headers = {
    "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"
}

# Fem una petició HTTP per a que ens retorni el contingut de la pàgina web a scrapejar.
pagina = requests.get("https://www.numbeo.com/common/currency_settings.jsp", headers=headers)

# Analitzem les pàgines html.
soup = BeautifulSoup(pagina.content, 'html.parser')

# Fem una primera cerca per el tag "td".
soup_td = soup.find_all('td')

# Agafem tots els noms de les divises amb una expressió regular que busqui el text ja que no tenim suficients 
# tags per a poder-ho filtrar d'altra forma.
for item in soup_td:
   for curr in item.find_all(text=re.compile(r'^[a-zA-Z]')):
    currency_name.append(curr.text)

# Agafem tots els tipus de canvi de les divises, com que no tenim suficients tags
# guardem els resultats en una llista que posteriorment dividirem.
for item in soup_td:
 for curnum in item.find_all(text=re.compile(r'\b\d+\b')):
     twocurrency.append(curnum.text)


# Fem un "list slicing" per a obtenir els valors que es corresponen a les divises EUR i USD respectivament
currency_eur = twocurrency[1::2]
currency_usd = twocurrency[2::2]

# Finalment creem el nostre .csv, en aquest cas volem crear una fila per cada ítem, utilitzem un for loop
with open('world_currencies.csv', 'w', encoding='UTF8', newline='') as csvfile:
    write = csv.writer(csvfile)
    write.writerow(cap_csv)
    for i in range(len(currency_name)):
        write.writerow([currency_name[i], currency_eur[i], currency_usd[i]])
