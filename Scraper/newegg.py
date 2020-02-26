from bs4 import BeautifulSoup
import requests

headers = requests.utils.default_headers()
print(headers)
proxies = {
  "http": "http://38.89.138.170:3128",
  "https": "http://38.89.138.170:3128",
}
headers.update({
    'User-Agent': 'Mozilla/5.0 (Linux; Android 8.0.0; SM-G960F Build/R16NW) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.84 Mobile Safari/537.36',
})
for i in range(0, 1):
    source = requests.get('https://www.newegg.com/p/pl?N=100007671%204814%2050001028%2050001157%20601350557',headers = headers).text
    soup = BeautifulSoup(source, 'lxml')


    #print(soup.prettify())
 
    #container = soup.find_all('div', class_='item-container')

    #print(container)
    #print(len(container))
    name = soup.find('dt', id = 'checkbox_Series')
    print(source)