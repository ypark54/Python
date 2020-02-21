from bs4 import BeautifulSoup
import requests

headers = requests.utils.default_headers()
headers.update({
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.106 Safari/537.36',
})
for i in range(1, 10):
    source = requests.get('https://www.newegg.com/p/pl?N=100007671%204814&Page='+str(i)+'&order=PRICED', headers=headers).text
    soup = BeautifulSoup(source, 'lxml')


    #print(soup.prettify())
 
    #container = soup.find_all('div', class_='item-container')

    #print(container)
    #print(len(container))
    name = soup.find_all('a', class_='item-title')

    for n in name:
        print(n.text)