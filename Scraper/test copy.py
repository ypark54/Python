from bs4 import BeautifulSoup
import requests
import chardet
import io

headers = requests.utils.default_headers()
headers.update({
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.106 Safari/537.36',
})

urlBase = 'https://newtoki51.com/'
source = requests.get(urlBase, headers=headers)


#print(source.apparent_encoding)
#print(source.encoding)
text = source.text
soup = BeautifulSoup(text, 'lxml')

#print(soup.get_text())
#print(type(soup))

#print(type("sdf"))
#f.write(str(soup))

print(soup.prettify)