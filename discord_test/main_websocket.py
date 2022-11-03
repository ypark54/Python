import websocket
import json
import os
import threading
import time


def send_request(ws, rq):
    ws.send(json.dumps(rq))

def recv_response(ws):
    response = ws.recv()
    if response:
        return json.loads(response)

def heartbeat(interval, ws):
    print('Heartbeat Begins')
    while True:
        time.sleep(interval)
        print(interval)
        heartbeatJson = {
            'op': 1,
            'd': 'null'
        }
        send_request(ws, heartbeatJson)
        print('Heartbeat Sent')


if __name__ == '__main__':
    ws = websocket.WebSocket()
    ws.connect('wss://gateway.discord.gg/?v=9&encoding=json')

    #heartbeat_interval = event['d']['heartbeat_interval'] / 1000
    #threading._start_new_thread(heartbeat, (heartbeat_interval, ws))

    payload = {
        'op': 2,
        'd': {
            'token': 'MjI4NDczNjc1NjE0MTI2MDgw.YmBcxg.BVG2IGl9HYeji8H4Yb9bI415wc4',
            'properties': {
                '$os': 'windows',
                '$browser': 'chrome',
                'device' : 'pc'
            }
        }
    }
    send_request(ws,payload)

    while True:
        event = recv_response(ws)
        print(event)
        