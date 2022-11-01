import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import csv

options = webdriver.ChromeOptions()
options.add_argument('headless')
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

'''with open('ul_rankings.csv', 'r') as f:
    reader = csv.reader(f)
    next(reader)
    pokemon = [line[0] for line in reader]
f.close()

url_pokemon = pokemon.copy()
for i in range(len(url_pokemon)):
    url_pokemon[i] = url_pokemon[i].replace(' ', '_').replace('(', '').replace(')', '')'''

with open('ul_iv_data.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['Rank', 'CP', 'Atk', 'Def', 'HP', 'Perfect'])

pokemon = ['Stunfisk (Galarian)', 'Swampert (Shadow)']
url_pokemon = ['Stunfisk_Galarian', 'Swampert_Shadow']

for i in range(len(url_pokemon)):
    if url_pokemon[i].endswith("_Shadow"):
        temp = url_pokemon[i].replace('_Shadow', '')
        url = f"https://pvpivs.com/?mon={temp}&r=30&cp=2500&max=50"
    else:
        url = f"https://pvpivs.com/?mon={url_pokemon[i]}&r=30&cp=2500&max=50"

    driver.get(url)
    content = driver.page_source.encode('utf-8').strip()
    soup = BeautifulSoup(content, "lxml")
    table = soup.find("table", {"id": "outTable"})

    headers = ['Rank', 'Lvl', 'CP', 'Atk', 'Def', 'HP', 'Perfect']
    data = pd.DataFrame(columns=headers)
    for j in table.find_all('tr')[1:]:
        row_data = j.find_all('td')[:7]
        row = [i.text for i in row_data]
        length = len(data)
        data.loc[length] = row
    data.drop(data.columns[[1]], inplace=True, axis=1)
    with open('ul_iv_data.csv', 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([pokemon[i]])
    data.to_csv('ul_iv_data.csv', encoding='utf-8', doublequote=False, index=False, header=False, mode="a")
f.close()
driver.quit()
