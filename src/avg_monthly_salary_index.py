from bs4 import BeautifulSoup
import csv
import requests
import re

# Definim la capçalera del .csv que crearem al final i també definim les llistes buides.
cap_csv = ['Country' , 'EUR Average Monthly Salary', 'USD Average Monthly Salary']
countries = []
avgmsalary_eur = []
avgmsalary_usd = []

# Modifiquem l'User-Agent per a que al moment d'executar el codi la pàgina ens identifiqui com un usuari comú.
headers = {
    "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"
}

# Fem un "request" per cada pàgina diferent que anem a "scrapejar."
paginaEUR = requests.get("https://www.numbeo.com/cost-of-living/prices_by_country.jsp?displayCurrency=EUR&itemId=105", headers=headers)
paginaUSD = requests.get("https://www.numbeo.com/cost-of-living/prices_by_country.jsp?itemId=105&displayCurrency=USD", headers=headers)

# Analitzem les pàgines html.
soupEUR = BeautifulSoup(paginaEUR.content, 'html.parser')
soupUSD = BeautifulSoup(paginaUSD.content, 'html.parser')

# Fem una primera cerca per el tag "td".
soup_tdEUR = soupEUR.find_all('td')
soup_tdUSD = soupUSD.find_all('td')


# Agafem tots els països del llistat en format text.
for item in soup_tdEUR:
   for country in item.find_all('a'):
    countries.append(country.text)

# Agafem tots els salaris en format EUR amb una regular expression.
for item in soup_tdEUR:
  for monthsalary in item.find_all(text=re.compile(r'\b\d+\b')):
       avgmsalary_eur.append(monthsalary.text)

# Agafem tots els salaris en format USD amb una regular expression.
for item in soup_tdUSD:
  for monthsalary in item.find_all(text=re.compile(r'\b\d+\b')):
      avgmsalary_usd.append(monthsalary.text)

# Finalment creem el nostre .csv, en aquest cas volem crear una fila per cada ítem, utilitzem un for loop
with open('average_monthly_salary_index.csv', 'w', encoding='UTF8', newline='') as csvfile:
    write = csv.writer(csvfile)
    write.writerow(cap_csv)
    for i in range(len(countries)):
        write.writerow([countries[i], avgmsalary_eur[i], avgmsalary_usd[i]])
