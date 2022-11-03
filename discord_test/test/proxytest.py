import requests
import json
from random_word import RandomWords
from random import randint
from collections import deque

'''
header = {"Authorization": "43dac75fdfdfcad6ede6df341b5007ebad9eb10d"}
response = requests.get("https://proxy.webshare.io/api/proxy/replacement/info/", headers=header)
print(response.text)
'''

rand = RandomWords()

proxy_json = open('C:/Python/discord_test/proxy.json')
proxy_list = json.load(proxy_json)
proxy_json.close()

currency_json = open('C:/Python/discord_test/currency_db.json')
currency_dict = json.load(currency_json)
currency_json.close()

currency_list = list(currency_dict)
league = 'standard'
ratio = 130
while True:
    tag = currency_list[0]
    stock = currency_dict[tag]['stock']
    mode = currency_dict[tag]['mode']
    if tag == 'chaos' or tag == 'exalted':
        currency_list = deque(currency_list)
        currency_list.rotate(-1)
        currency_list = list(currency_list)
        continue
    
    body_list = []
    if 's' in mode:
        body_list.append({'exchange': {'status': {'option': 'online'},'have': [tag],'want': ['chaos']}})
    if 'b' in mode:
        body_list.append({'exchange': {'status': {'option': 'online'},'have': ['chaos'],'want': [tag]}})
        body_list.append({'exchange': {'status': {'option': 'online'},'have': ['exalted'],'want': [tag]}})
    

    price_list = []
    note_list = []
    for index, body in enumerate(body_list):
        while True:
            try:
                user_agent = f'{rand.get_random_word()}/1.{randint(0,9)}.{randint(0,9)}'
                url = f'https://www.pathofexile.com/api/trade/exchange/Sentinel'
                headers = {
                    'Content-Type': 'application/json',
                    #'Cookie': 'POESESSID=24a9f25c705f48091a25beb9cd2497f4',
                    'User-Agent': user_agent
                }
                
                body = {"query":{"status":{"option":"online"},"have":["alt"],"want":["chaos"]},"sort":{"have":"asc"},"engine":"new"}
                payload = json.dumps(body)
                response = requests.request('POST', url, headers=headers, data=payload, proxies=proxy_list[0])
                r = json.loads(response.text)
                seg = ','.join(r['result'])
                id = r['id']
                url = f'https://www.pathofexile.com/api/trade/fetch/{seg}?query={id}&exchange'
                response = requests.request('GET', url, headers=headers, data={})
                r = json.loads(response.text)
                print(r)
                price = 0
                exchange = 0
                item = 0
                note = ''
                if r.get('result'):
                    for entry in r['result']:
                        exchange = entry['listing']['price']['exchange']['amount']
                        item = entry['listing']['price']['item']['amount']
                        new_price = int(exchange)/int(item)
                        if len(r['result']) <= 5:
                            price = new_price
                            break
                        if new_price < 1.1*price:
                            price = new_price
                            break
                        price = new_price
                    if index == 2:
                        note = f'~price {exchange}/{item} exalted'
                        price = price*ratio
                    elif index == 1:
                        note = f'~price {exchange}/{item} chaos'
                    else:
                        note = f'~price {exchange}/{item} {tag}'
                        price = 1/price
                price_list.append(price)
                note_list.append(note)
                break
            except KeyboardInterrupt:
                break
            except:
                print('error')
                proxy_list = deque(proxy_list)
                proxy_list.rotate(-1)
                proxy_list = list(proxy_list)
    
    print(price_list)
    print(note_list)

    if mode == 'bs':
        ex = note_list[2].split(' ')[1].split('/')[1]
        sell_c = price_list[0] < price_list[1]
        sell_ex = price_list[0] < price_list[2]
        ex_avail = stock < int(ex)

        if sell_c and sell_ex:
            if ex_avail:
                print(note_list[0], note_list[2])
            else:
                print(note_list[0], note_list[1])
        elif sell_c and (not sell_ex):
            print(note_list[0], note_list[1])
        elif (not sell_c) and sell_ex:
            print(note_list[0], note_list[2])
        elif (not sell_c) and (not sell_ex):
            print('not profitable')
    elif mode == 's':
        if price_list[0] < price_list[1]:
            print(note_list[1])
        elif price_list[0] > price_list[1]:
            print(note_list[0])
    elif mode == 'b':
        print(note_list[0])

    currency_list = deque(currency_list)
    currency_list.rotate(-1)
    currency_list = list(currency_list)

    proxy_list = deque(proxy_list)
    proxy_list.rotate(-1)
    proxy_list = list(proxy_list)
    