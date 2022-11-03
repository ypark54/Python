
import requests
import json
import time

#renew json file and return list of keys for official trade
def renew_by_tag(tag, currency, price):
    f = open('currency.json')
    data = json.load(f)
    split_tag = tag.split('-')
    if split_tag[0] == 'deafening':
        key = ''.join(['deafening ',split_tag[3]])
        data['essence'][key][currency] = price
        key = ''.join(['shrieking ',split_tag[3]])
        data['essence'][key][currency] = price/3
        key = ''.join(['screaming ',split_tag[3]])
        data['essence'][key][currency] = price/9
        if split_tag[3] not in ['scorn','envy','misery','dread']:
            key = ''.join(['wailing ',split_tag[3]])
            data['essence'][key][currency] = price/27
            if split_tag[3] not in ['loathing', 'zeal', 'anguish', 'spite']:
                key = ''.join(['weeping ',split_tag[3]])
                data['essence'][key][currency] = price/81
                if split_tag[3] not in ['rage', 'suffering', 'wrath', 'doubt']:
                    key = ''.join(['muttering ',split_tag[3]])
                    data['essence'][key][currency] = price/243
                    if split_tag[3] not in ['fear', 'anger', 'sorrow', 'torment']:
                        key = ''.join(['whispering ',split_tag[3]])
                        data['essence'][key][currency] = price/729

    elif split_tag[0] == 'essence':
        key = split_tag[2]
        data['essence'][key][currency] = price
    elif split_tag[0] == 'remnant':
        key = 'remnant'
        data['essence'][key][currency] = price
    else:
        pass
    with open('currency.json', 'w') as json_file:
        json.dump(data, json_file, indent=4)

def ninja_renew():
    url = 'https://poe.ninja/api/data/ItemOverview?league=Archnemesis&type=Essence'

    payload={}
    headers={}

    response = requests.request("GET", url, headers=headers, data=payload)
    r = json.loads(response.text)


    search = []
    for line in r['lines']:
        tag = line['detailsId']
        
        chaos = line['chaosValue']
        #print(f'tag: {tag} chaos: {chaos}')
        split_tag = tag.split('-')
        if split_tag[0] == 'deafening':
            key = ''.join(['deafening ',split_tag[3]])
            search.append(key)
            print(tag)
        elif split_tag[0] == 'essence':
            key = split_tag[2]
            search.append(key)
        elif split_tag[0] == 'remnant':
            key = 'remnant'
            search.append(key)
        else:
            pass
    
    for line in r['lines']:
        tag = line['detailsId']
        chaos = line['chaosValue']
        #print(f'tag: {tag} chaos: {chaos}')
        renew_by_tag(tag, 'chaos', chaos)


    print(search)
    return search

def trade_renew(search):
    f = open('currency.json')
    data = json.load(f)
    f.close()
    start_time = time.time()
    for key in search:
        tag = data['essence'][key]['tag']
        print(tag)
        body = {
            'exchange': {
                'status': {
                'option': 'online'
                },
                'have': [
                'exa'
                ],
                'want': [
                tag
                ]
            }
        }
        headers = {
            'Content-Type': 'application/json',
            'Cookie': 'POESESSID=24a9f25c705f48091a25beb9cd2497f4',
            'User-Agent': 'poetrade/1.0.0'
        }
        payload = json.dumps(body)
        url = 'https://www.pathofexile.com/api/trade/exchange/archnemesis'
        r = {'error':'error'}
        while 'error' in r:
            response = requests.request('POST', url, headers=headers, data=payload)
            r = json.loads(response.text)
            rules = response.headers['X-Rate-Limit-Ip'].split(',')
            states = response.headers['X-Rate-Limit-Ip-State'].split(',')
            limit = []
            state = []
            interval = []
            timeout = []
            for index, rule in enumerate(rules):
                limit.append(int(rule.split(':')[0]))
                interval.append(int(rule.split(':')[1]))
                state.append(int(states[index].split(':')[0]))
                timeout.append(int(states[index].split(':')[2]))
            '''
            print(f'limit: {limit}')
            print(f'interval: {interval}')
            print(f'timeout: {timeout}')
            print(f'state: {state}')
            '''

            if max(timeout)>0:
                #print(f'Timeout occurred. Sleeping for {max(timeout)}seconds.')            
                time.sleep(max(timeout))
            
            for index in range(len(limit)):
                if state[index]+1 >= limit[index]:
                    while time.time()-start_time < interval[index]:
                        #print(f'waiting for cooldown. {interval[index]-time.time()+start_time}s left.')
                        time.sleep(1)
                start_time = time.time()    
            
                
            

        #print(r['result'])
        seg = ','.join(r['result'])
        id = r['id']
        url = f'https://www.pathofexile.com/api/trade/fetch/{seg}?query={id}&exchange'
        response = requests.request('GET', url, headers=headers, data={})
        r = json.loads(response.text)

            
        #print(response.headers)
        h = response.headers['X-Rate-Limit-Ip-State']
        #print(h)
        price = []
        for rr in r['result']:
            #print(rr)
            exa = rr['listing']['price']['exchange']['amount']
            item = rr['listing']['price']['item']['amount']
            #print(f'{exa/item}ex')
            price.append(exa/item)
        renew_by_tag(tag, 'exalted', price[0])
        



if __name__ == '__main__':
    search = ninja_renew()
    trade_renew(search)
    