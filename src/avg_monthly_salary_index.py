from bs4 import BeautifulSoup
import csv
import requests
import re

cap_csv = ['Country' , 'EUR Average Monthly Salary', 'USD Average Monthly Salary']
countries = []
avgmsalary_eur = []
avgmsalary_usd = []

# Modifiquem l'User-Agent per a que al moment d'executar el codi la pàgina ens identifiqui com un usuari 
headers = {
    "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"
}

paginaEUR = requests.get("https://www.numbeo.com/cost-of-living/prices_by_country.jsp?displayCurrency=EUR&itemId=105", headers=headers)
paginaUSD = requests.get("https://www.numbeo.com/cost-of-living/prices_by_country.jsp?itemId=105&displayCurrency=USD", headers=headers)

soupEUR = BeautifulSoup(paginaEUR.content, 'html.parser')
soupUSD = BeautifulSoup(paginaUSD.content, 'html.parser')

soup_tdEUR = soupEUR.find_all('td')
soup_tdUSD = soupUSD.find_all('td')



for item in soup_tdEUR:
   for country in item.find_all('a'):
    countries.append(country.text)

for item in soup_tdEUR:
  for monthsalary in item.find_all(text=re.compile(r'\b\d+\b')):
       avgmsalary_eur.append(monthsalary.text)

for item in soup_tdUSD:
  for monthsalary in item.find_all(text=re.compile(r'\b\d+\b')):
      avgmsalary_usd.append(monthsalary.text)


with open('average_monthly_salary_index.csv', 'w', encoding='UTF8', newline='') as csvfile:
    write = csv.writer(csvfile)
    write.writerow(cap_csv)
    for i in range(len(countries)):
        write.writerow([countries[i], avgmsalary_eur[i], avgmsalary_usd[i]])
