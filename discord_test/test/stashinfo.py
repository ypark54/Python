
import requests
import json

currency_json = open('C:/Python/discord_test/currency_db.json')
currency_dict = json.load(currency_json)
currency_json.close()

conversion_json = open('C:/Python/discord_test/currency_tag_conversion.json')
conversion_dict = json.load(conversion_json)
conversion_json.close()

payload={}
headers = {
    'Cookie': 'POESESSID=e03ec6a925f3f62dcf3e76374074932c',
    'User-Agent': 'poetrade/1.0.0'
}

for index in range(3):
    url = f'https://www.pathofexile.com/character-window/get-stash-items?accountName=calmpoe1&league=standard&tabIndex={index}'
    response = requests.request("GET", url, headers=headers, data=payload)
    r = json.loads(response.text)

    for item in r['items']:
        stackSize = item['stackSize']
        
        name = conversion_dict[item['typeLine'].lower()]
        note = item.get('note')
        currency_dict['note'] = note
        print(f'{name} {stackSize} {note}')
