import requests
from bs4 import BeautifulSoup

res = requests.get('https://free-proxy-list.net')
content = BeautifulSoup(res.text, 'lxml')
table = content.find('table')
rows = table.find_all('tr')
cols = [[col.text for col in row.find_all('td')] for row in rows]

proxies = []
proxy_index = 0

for col in cols:
    try:
        if col[4] == 'elite proxy' and col[6] == 'yes':
            proxies.append('https://' + col[0] + ':' + col[1])
    except:
        pass
    
def fetch(url, params):
    global proxy_index
    
    while proxy_index < len(proxies):
        try:
            print('Trying proxy:', proxies[proxy_index])
            res = requests.get(url, proxies={'https': proxies[proxy_index]}, params=params, timeout=5).text
            return res
            
        except:
            print('Bad proxy...')
            proxy_index += 1

for page in range(0, 4):
    params = {'page': page}
    res = fetch('https://www.newegg.com/p/pl?N=100007671%204814%2050001028%2050001157', params=params)
    proxy_index += 1
    soup = BeautifulSoup(res, 'lxml')
    print(soup.find('dt', id = 'checkbox_Series'))
    break