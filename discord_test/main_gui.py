import multiprocessing as mp
import tkinter as tk
from tkinter import  ttk
import time
import datetime as dt
import easyocr
import cv2
import pywinauto
import pygetwindow as gw
import win32gui
import pyautogui
import requests
import numpy as np
import json 

import request_to_discord as rd
import tft_ocr as docr

def get_time():
    t = time.localtime()
    return time.strftime("%H:%M:%S", t)

def time_to_int(t):
    date_string = dt.datetime.strptime(t.rsplit('+')[0], '%Y-%m-%dT%H:%M:%S.%f')
    date_int = int(dt.datetime.strftime(date_string, '%Y%m%d%H%M%S%f'))
    return date_int

def log(q):
    while True:
        print(q[3].get())

def get_discord_messages(q,id,channel_index):
    while True:
        q[4+channel_index].put(rd.retrieve_messages(id))
        #q[3].put(f'Http request sent to channel {id}')
        time.sleep(1)

def renew_message_list(q,channel_index):
    save_message = None
    new_message = []
    threshold_time = 0

    while True:
        raw_message = q[4+channel_index].get()
        date_int = time_to_int(raw_message[0]['timestamp'])
        
        #save the raw message if there is no existing saved message
        if save_message is None:
            save_message = raw_message
            new_message = raw_message
        else:
            threshold_time = time_to_int(save_message[0]['timestamp'])
            index = 0
            #find the part of raw message that is new
            while time_to_int(raw_message[index]['timestamp']) > threshold_time:
                index = index + 1
                if index >= len(raw_message):
                    break
                
            new_message = raw_message[0:index]
            #if there is new message, save that new message and send to ui que
            if new_message:
                save_message = new_message
        for m in reversed(new_message):
            q[0].put(m)

def parse_message(q):
    reader = easyocr.Reader(['en'])
    f = open('currency.json')
    data = json.load(f)
    while not q[0].empty():
        channel = ''
        discordname = ''
        ign = ''
        asking_price = ''
        url = ''
        m = q[0].get()
        q[3].put('Parsing started')
        print(m)
        if m['attachments']:
            if '\nIGN' in m['content']:
                found_text = m['content'][m['content'].find('\nIGN'):]
                start_index = found_text.find('`')
                end_index = found_text[start_index+1:].find('`')
                ign = found_text[start_index+1:start_index+end_index+1]

            if '\nAsking price' in m['content']:
                found_text = m['content'][m['content'].find('\nAsking price'):]
                start_index = found_text.find('`')
                end_index = found_text[start_index+1:].find('`')
                asking_price = found_text[start_index+1:start_index+end_index+1]
            
            if m['channel_id'] == '874662778592460851':
                channel = 'Essence'
                name_list=list(data['essence'].keys())
            elif m['channel_id'] == '874663081400209499':
                channel = 'Fossil'
                name_list=list(data['fossil'].keys())
            q[3].put('Parsing finished. Reading image started')
            username = m['author']['username']
            discriminator = m['author']['discriminator']
            discordname = f'{username}#{discriminator}'
            url = m['attachments'][0]['url']
            image_nparray = np.asarray(bytearray(requests.get(url).content), dtype=np.uint8)
            image = cv2.imdecode(image_nparray, cv2.IMREAD_COLOR)
            item, num = docr.img_to_text(image, reader, name_list)
            ninja_price = 0
            bulk_price = 0
            for index in range(len(item)):
                i = int(num[index])
                chaos_price = i*data[channel.lower()][item[index]]['chaos']
                ninja_price = ninja_price + chaos_price
                exalted_price = i*data[channel.lower()][item[index]]['exalted']
                bulk_price = bulk_price + exalted_price
                print(f'item: {item[index]} amount: {i} chaos: {chaos_price} exalted: {exalted_price}')
            q[1].put((channel,discordname,ign, asking_price, ninja_price, bulk_price))
            q[3].put('Reading image finished.')
            time.sleep(1)

def send_discord(id, message):
    discord = gw.getWindowsWithTitle('Discord')
    if discord:
        win = gw.getWindowsWithTitle('Discord')[0]
     # 윈도우 타이틀에 Chrome 이 포함된 모든 윈도우 수집, 리스트로 리턴
        if win.isActive == False:
            pywinauto.application.Application().connect(handle=win._hWnd).top_window().set_focus()
        win.activate() #윈도우 활성화p
        coord = win32gui.GetWindowRect(win._hWnd)
        center = ((coord[0]+coord[2])/2,(coord[1]+coord[3])/2)
        pyautogui.press('esc')
        pyautogui.press('esc')
        pyautogui.hotkey('ctrl', 'k')
        time.sleep(0.2)
        pyautogui.click(x=center[0], y = center[1]-127)
        pyautogui.click(x=center[0], y = center[1]-127)
        time.sleep(0.2)
        pyautogui.write(id)
        time.sleep(0.2)
        pyautogui.press('enter')
        time.sleep(0.1)
        pyautogui.press('enter')
        time.sleep(0.2)
        pyautogui.write(message)
        pyautogui.press('enter')

def send_poe(ign, message):
    pass

def poe_invite(ign, message):
    pass

def pop_window(event_0):
    def discord_ask():
        send_discord(pandagirl,ask)
    def discord_buyout():
        send_discord(pandagirl,buyout)
    def discord_offer():
        res = myEntry.get()
        offer = f'I would like to offer you {res}ex total. Let me know if you are interested.'
        send_discord(pandagirl,offer)

    top = tk.Toplevel(root)
    top.title('Send Message')
    selected = tree.focus()
    temp = tree.item(selected, 'values')
    pandagirl = 'pandagirl#5117'
    ask = f'Hi, would you be interested if I make an offer for your bulk {temp[0].lower()} sale on TFT?'
    buyout = f'Hi, I would like to buy your bulk {temp[0].lower()} sale on TFT.'
    tk.Label(top, text=f'Discord Name: {temp[1]}').grid(row=0, column=0, sticky='W')
    tk.Label(top, text=f'IGN: {temp[2]}').grid(row=0, column=4, sticky='E')
    tk.Label(top, text='Discord').grid(row=1, column=0, columnspan=3, sticky='E')
    tk.Label(top, text=ask).grid(row=2, column=0, columnspan=3, sticky='E')
    tk.Label(top, text=buyout).grid(row=3, column=0, columnspan=3, sticky='E')
    tk.Label(top, text='I would like to offer you ').grid(row=4, column=0)
    myEntry = tk.Entry(top, width = 5)
    myEntry.grid(row=4, column=1)
    tk.Label(top, text='ex total. Let me know if you are interested.').grid(row=4, column=2)
    tk.Button(top, width=10, text = 'Ask', command=discord_ask).grid(row=2, column=3)
    tk.Button(top, width=10, text = 'Buyout', command=discord_buyout).grid(row=3, column=3)
    tk.Button(top, width=10, text = 'Offer', command=discord_offer).grid(row=4, column=3)

    

#read from que and update ui    
def update():
    currentTime = dt.datetime.now()
    label['text'] = currentTime
    root.after(200, update)
    while not q[1].empty():
        t = q[1].get()
        q[3].put('Updating UI')
        tree.insert('', 0, values=t,text = 'abcde')
        

if __name__ == '__main__':
    #set up variables

    channel_id = ['874662778592460851']
    #initiate ques for communication

    message_que = mp.Queue()                #que to pass on messages retrieved from discord server
    parse_que = mp.Queue()
    ui_que = mp.Queue()
    log_que = mp.Queue()
    q = [parse_que, ui_que, message_que, log_que]
    
    root = tk.Tk()
    root.title('Main Application')
    # define columns
    columns = ('currency', 'discord name', 'ign', 'asking price', 'ninja price', 'bulk price', 'minimum profit', 'maximum profit')
    tree=ttk.Treeview(root, columns=columns, show='headings')

    # define headings
    for i in range(len(columns)):
        tree.heading(columns[i], text=columns[i].title())
        
    tree.grid(row=0, column=0, sticky='nsew')
    tree.bind("<Double-Button-1>", pop_window)

    scrollbar = ttk.Scrollbar(root, orient=tk.VERTICAL, command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.grid(row=0, column=1, sticky='ns')

    label = tk.Label(root, text="placeholder")
    label.grid(row=1)
    update()
        
    #initiate multiprocess
    p = []
    for id in channel_id:
        q.append(mp.Queue())
    for index, id in enumerate(channel_id, start=0):
        p.append(mp.Process(target=get_discord_messages, args=(q,id, index)))
        p.append(mp.Process(target=renew_message_list, args=(q,index)))
    p.append(mp.Process(target=parse_message, args=(q,)))
    p.append(mp.Process(target=log, args=(q,)))
    
    for process in p:
        process.start()
    root.mainloop()
    for process in p:
        process.join()
