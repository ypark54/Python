import requests
import json
import os
import numpy as np
import cv2
import time


def retrieve_messages(channelid):
    h  = {
        #losba/foxa#1501 : MjI4NDczNjc1NjE0MTI2MDgw.YmBcxg.BVG2IGl9HYeji8H4Yb9bI415wc4
        'accept': '*/*',
        'accept-encoding': 'gzip, deflate',
        'accept-language': '"en-US,en";"q=0.9"',
        'authorization': 'MjI4NDczNjc1NjE0MTI2MDgw.YmBcxg.BVG2IGl9HYeji8H4Yb9bI415wc4',
        'referer':'https://discord.com/channels/@me',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="100", "Google Chrome";v="100"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36',
        'x-debug-options': 'bugReporterEnabled',
        'x-discord-locale': 'en-US',
        'x-super-properties': 'eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiQ2hyb21lIiwiZGV2aWNlIjoiIiwic3lzdGVtX2xvY2FsZSI6ImVuLVVTIiwiYnJvd3Nlcl91c2VyX2FnZW50IjoiTW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV2luNjQ7IHg2NCkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzEwMC4wLjQ4OTYuMTI3IFNhZmFyaS81MzcuMzYiLCJicm93c2VyX3ZlcnNpb24iOiIxMDAuMC40ODk2LjEyNyIsIm9zX3ZlcnNpb24iOiIxMCIsInJlZmVycmVyIjoiIiwicmVmZXJyaW5nX2RvbWFpbiI6IiIsInJlZmVycmVyX2N1cnJlbnQiOiIiLCJyZWZlcnJpbmdfZG9tYWluX2N1cnJlbnQiOiIiLCJyZWxlYXNlX2NoYW5uZWwiOiJzdGFibGUiLCJjbGllbnRfYnVpbGRfbnVtYmVyIjoxMjU3MjEsImNsaWVudF9ldmVudF9zb3VyY2UiOm51bGx9',
        
    }
    #retrieve messages from channel in json format
    r = requests.get(f'https://discord.com/api/v9/channels/{channelid}/messages?limit=4', headers = h)
        

    messages = json.loads(r.text)
    #print(messages)
    return messages

def send_message():
    url = "https://discord.com/api/v9/channels/558415015976108034/messages"

    payload = json.dumps({
        "content": "aasdfasdfsdf",
        "tts": False
    })
    headers = {
        'authorization': 'MjI4NDczNjc1NjE0MTI2MDgw.YmBbnw.38huVYPcgE636HXIYEwFUAxbjZQ',
        'content-type': 'application/json',
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)

if __name__ == '__main__':
    #TFT Bulk Essence: 874662778592460851
    retrieve_messages('874662778592460851')