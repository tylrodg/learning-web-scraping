#! python3
from bs4 import BeautifulSoup
import requests

url = 'http://www.showmeboone.com/sheriff/JailResidents/JailResidents.asp'
response = requests.get(url)
html = response.content

soup = BeautifulSoup(html, "html.parser")
table = soup.find('tbody', attrs={'id': 'mrc_main_table'})

for row in table.findAll('tr')[:-1]:
    list_of_cells=[]
    for cell in row.findAll('td')[:-1]:
        text = cell.text.replace('&nbsp;', '')
        list_of_cells.append(text)
    print(list_of_cells)
