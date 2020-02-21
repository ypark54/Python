from bs4 import BeautifulSoup
import requests
import chardet
import io

headers = requests.utils.default_headers()
headers.update({
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.106 Safari/537.36',
})

urlBase = 'http://shop.danawa.com/virtualestimate/?controller=estimateMain&methods=product&orderbyList=GOODSINFO_CASH_PRICE_DESC&page='
source = requests.get(urlBase+'1', headers=headers)


#print(source.apparent_encoding)
#print(source.encoding)
source.encoding = "EUC-KR"
#print(source.encoding)
#print(chardet.detect(source.content))
text = source.text
soup = BeautifulSoup(text, 'lxml')

#print(soup.get_text())
#print(type(soup))

#print(type("sdf"))
#f.write(str(soup))

#print(soup.prettify)
body = soup.find('div', class_='scroll_box search_scroll_box')
#number = soup.find('div', class_='total_srch_area')
#print(number)
#print(body.prettify)
containers = body.find_all('td', class_='title_price')
#prices = body.find_all('span', class_='prod_price')
prices = body.find_all('p', class_='low_price')
#print(type(container))
#print(containers)
#f = open('guru99.txt', "w", encoding="utf-8")


for container, price in zip(containers, prices):
    if container.find('span', class_='icon_style md_recom')!= None:
        continue
    s1 = container.find('a').text
    
    print(s1)
    s3 = container.find('div', class_='spec_bg').find('a').text
    print(s3)
    s2 = price.text
    print(s2)
    
    
    #f.write(str(s1)+'\n'+str(s2)+'\n')

#name = soup.find('a', class_='item-title')
print(len(containers))
#print(name)