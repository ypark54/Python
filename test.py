from bs4 import BeautifulSoup
import requests
import chardet
import io

headers = requests.utils.default_headers()
headers.update({
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
})

urlBase = 'http://shop.danawa.com/virtualestimate/?controller=estimateMain&methods=product&categorySeq=873&categoryDepth=2&marketPlaceSeq=16&pseq=2&orderbyList=GOODSINFO_CASH_PRICE_DESC&page='
source = requests.get(urlBase+'18', headers=headers)


print(source.apparent_encoding)
print(source.encoding)
source.encoding = "EUC-KR"
print(source.encoding)
print(chardet.detect(source.content))
text = source.text
soup = BeautifulSoup(text, 'lxml')

#print(soup.get_text())
print(type(soup))

#print(type("sdf"))
#f.write(str(soup))

#print(soup.prettify)

container = soup.find_all('td', class_='title_price')
price = soup.find_all('span', class_='prod_price')
print(type(container))
#print(container)
f = open('guru99.txt', "w", encoding="utf-8")
for n,x in enumerate(container):
    s1 = x.find('a').text
    print(s1)
    s2 = price[n].text
    print(s2)
    
    f.write(str(s1)+'\n'+str(s2)+'\n')

#print(len(container))
#name = soup.find('a', class_='item-title')

#print(name)