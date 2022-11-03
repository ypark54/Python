import math
import cv2
import numpy as np
import win32gui
import win32ui
import win32con
import time
import pydirectinput
import pyautogui
import os
import codecs
from multiprocessing import Process, Manager, Queue, Lock
import copy
import pyperclip
import json
import requests
import keyboard
from fractions import Fraction
from random_word import RandomWords
from random import randint
from collections import deque
import tkinter as tk                    
from tkinter import ttk
from tkinter.messagebox import showinfo

hwnd = win32gui.FindWindow(None, 'Path of Exile')
margin_x = 8
margin_y = 31
wDC = win32gui.GetWindowDC(hwnd)
dcObj = win32ui.CreateDCFromHandle(wDC)
cDC = dcObj.CreateCompatibleDC()
dataBitMap = win32ui.CreateBitmap()
dataBitMap.CreateCompatibleBitmap(dcObj, 800, 600) 

fastClickDurationAve = 0.0586967658996582*pow(10,9)
fastClickDurationSD = 0.0122891029527244*pow(10,9)
fastClickIntervalAve = 0.07695479440216971*pow(10,9)
fastClickIntervalSD = 0.018145767460531096*pow(10,9)
        
clickDurationAve = 0.06365472727482861*pow(10,9)
clickDurationSD = 0.012447467353326233*pow(10,9)
pressDurationAve = 0.06947592933579247*pow(10,9)
pressDurationSD = 0.01626015395505062*pow(10,9)

input_lock = Lock()

currency_json = open('C:/Python/discord_test/currency_db.json')
currency_dict = json.load(currency_json)
currency_json.close()


conversion_json = open('C:/Python/discord_test/currency_tag_conversion.json')
conversion_dict = json.load(conversion_json)
conversion_json.close()

rand = RandomWords()

proxy_json = open('C:/Python/discord_test/proxy.json')
proxy_list = json.load(proxy_json)
proxy_json.close()

league = 'sentinel'
ratio = 175
poesessid = 'e03ec6a925f3f62dcf3e76374074932c'

def uiConfig():
    root = tk.Tk()
    root.title("Tab Widget")
    tabControl = ttk.Notebook(root)
    
    payload={}
    headers = {
        'Cookie': f'POESESSID={poesessid}',
        'User-Agent': 'poesstan/1.0.0'
    }

    url = f'https://www.pathofexile.com/character-window/get-stash-items?accountName=calmpoe1&league={league}&tabIndex=0'
    response = requests.request("GET", url, headers=headers, data=payload)
    # need to catch error
    r = json.loads(response.text)
    numTabs = int(r['numTabs'])
    tab = []

    for index in range(numTabs):
        url = f'https://www.pathofexile.com/character-window/get-stash-items?accountName=calmpoe1&league={league}&tabIndex={index}'
        response = requests.request("GET", url, headers=headers, data=payload)
        r = json.loads(response.text)
        if r.get('items'):
            n = len(tab)
            tab.append(ttk.Frame(tabControl))
            tabControl.add(tab[n], text =f'Tab {n}')
            ttk.Label(tab[n], 
            text ="Welcome to \
            GeeksForGeeks").grid(column = 0, 
                                row = 0,
                                padx = 30,
                                pady = 30)  
        for item in r['items']:
            try:
                if r.get('currencyLayout') or r.get('delveLayout') or r.get('essenceLayout'):
                    stackSize = item['stackSize']
                    name = conversion_dict[item['typeLine'].lower()]
                    note = item.get('note')
                    currency_dict[name]['note'] = note
                    currency_dict[name]['stock'] = stackSize
                else:
                    note = item.get('note')
                    name = note.split(' ')[-1]
                    x = 9+int((item['x']+0.5)*350/12)
                    y = 71+int((item['y']+0.5)*350/12)
                    currency_dict[name]['buy_note'] = note
                    currency_dict[name]['buy_coord'] = [x,y]
            except:
                print(f'{item} keyerror')

    
    print(currency_dict)
    tabControl.pack(expand = 1, fill ="both")
    
    
    
    columns = ('first_name', 'last_name', 'email')

    tree = ttk.Treeview(tab[0], columns=columns, show='headings')

    # define headings
    tree.heading('first_name', text='First Name')
    tree.heading('last_name', text='Last Name')
    tree.heading('email', text='Email')

    # generate sample data
    contacts = []
    for n in range(1, 100):
        contacts.append((f'first {n}', f'last {n}', f'email{n}@example.com'))

    # add data to the treeview
    for contact in contacts:
        tree.insert('', tk.END, values=contact)


    def item_selected(event):
        for selected_item in tree.selection():
            item = tree.item(selected_item)
            record = item['values']
            # show a message
            showinfo(title='Information', message=','.join(record))


    tree.bind('<<TreeviewSelect>>', item_selected)

    tree.grid(row=1, column=0, sticky='nsew')

    # add a scrollbar
    scrollbar = ttk.Scrollbar(tab[0], orient=tk.VERTICAL, command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.grid(row=0, column=1, sticky='ns')

    return root

def window_capture():
    cDC.SelectObject(dataBitMap)
    cDC.BitBlt((-margin_x,-margin_y), (800+margin_x,600+margin_y), dcObj, (0,0), win32con.SRCCOPY)
    signedIntsArray = dataBitMap.GetBitmapBits(True)
    img = np.frombuffer(signedIntsArray, dtype = 'uint8')
    img.shape = (600, 800, 4)
    img = np.ascontiguousarray(img[...,:3])
    return img

def window_close():
    dcObj.DeleteDC()
    cDC.DeleteDC()
    win32gui.ReleaseDC(hwnd, wDC)
    win32gui.DeleteObject(dataBitMap.GetHandle())

def declineTrade():
    if state('trade_request'):
        rect = win32gui.GetWindowRect(hwnd)
        randClick(rect[0]+margin_x+750,rect[1]+margin_y+430)

def parseAreaMsg(msg):
    #: 호드를위하는대족장가로쉬 has joined the area.
    name = msg.split(' : ')[1].split(' ')[0]
    state = msg.split(' : ')[1].split(' has ')[1].split(' ')[0]
    return name, state

def isAfkMsg(msg):
    if "AFK mode is now ON." in msg:
        return True
    else:
        return False

def isTradeMsg(msg):
    if not isIncomingMsg(msg):
        return False
    
    if 'like to buy your' in msg:
        return True
    else:
        return False

def isIncomingMsg(msg):
    if '@From ' in msg:
        return True
    else:
        return False

def isTradeStateMsg(msg):
    if 'Trade accepted.' in msg:
        return True
    else:
        return False

def parseTradeMsg(msg):
    #@CoreyCR Hi, I would like to buy your Exalted Orb listed for 11 silver in Archnemesis (stash tab "Trade4"; position: left 49, top 1)
    #@TrueKingGarrosh Hi, I'd like to buy your 2 deft fossil for my 610 chaos in Standard.
    #@XchungeX Hi, I'd like to buy your 333 Chaos Orb for my 18 Obscured Delirium Orb, 11 Key to the Crucible in Standard.
    #@vdfbdsadasd Hi, I would like to buy your Skittering Incubator in Standard (stash tab "온퓨리"; position: left 1, top 17)
    name_temp = msg.split('@From ')[1].split(':')[0]
    if '> ' in name_temp:
        name = name_temp.split('> ')[1]
    else:
        name = name_temp

    receive_amount = []
    receive_item = []
    
    if not ' for ' in msg:                                              #trade message is asking for unlisted item
        return None
    
    if 'would' in msg:                                                  #trade message is from generic trade
        if msg.split(' buy your ')[1].split(' ')[0].isdigit():          #give item in trade message has amount specified
            give_amount = int(msg.split(' buy your ')[1].split(' listed for ')[0].split(' ',1)[0])
            give_item_raw = msg.split(' buy your ')[1].split(' listed for ')[0].split(' ',1)[1].lower()
            give_item = conversion_dict[give_item_raw]
        else:
            give_amount = 1
            give_item_raw = msg.split(' buy your ')[1].split(' listed for ')[0].lower()
            give_item = conversion_dict[give_item_raw]
        receive_amount.append( int(msg.split(' listed for ')[1].split(' in ')[0].split(' ', 1)[0]) )
        receive_item_raw = msg.split(' listed for ')[1].split(' in ')[0].split(' ', 1)[1].lower()
        receive_item.append(conversion_dict[receive_item_raw])
    else:                                                               #trade message is from bulk trade
        give_amount = int(msg.split(' buy your ')[1].split(' for my ')[0].split(' ',1)[0])
        give_item_raw = msg.split(' buy your ')[1].split(' for my ')[0].split(' ',1)[1].lower()
        give_item = conversion_dict[give_item_raw]

        rhs = msg.split(' for my ')[1]
        while ', ' in rhs:                         #message has multiple items for trade
            receive_amount.append( int(rhs.split(', ')[0].split(' ',1)[0]) )
            receive_item_raw = rhs.split(', ')[0].split(' ',1)[1].lower()
            receive_item.append(conversion_dict[receive_item_raw])
            rhs = rhs.split(', ',1)[1]
        receive_amount.append( int(rhs.split(' in ')[0].split(' ',1)[0]) )
        receive_item_raw = rhs.split(' in ')[0].split(' ',1)[1].lower()
        receive_item.append(conversion_dict[receive_item_raw])
    return name, give_item, give_amount, receive_item, receive_amount

def isAreaMsg(msg):
    #: 호드를위하는대족장가로쉬 has joined the area.
    if ' : ' in msg and 'the area' in msg:
        return True
    else:
        return False

def tradeTemplate():
    temp = {
        'name':'',
        'index': 0,
        'give item':[],
        'give amount':[],
        'receive item':[],
        'receive amount':[],
    }
    return temp

def partyTemplate():
    temp = {
        'name':'',
        'invited' : 0,
        'timeout' : 0,
        'timeout init': 0,
        'strike' : 0
    }
    return temp
    
def nanosleep(n):
    t = time.perf_counter_ns()
    expired = 0
    while expired < n:
        expired = time.perf_counter_ns()-t

def randClick(x, y, button='left'):
    pyautogui.moveTo(x,y)
    time.sleep(randClickDuration()/1000000000)
    pyautogui.mouseDown(x,y,button=button)
    time.sleep(randClickDuration()/1000000000)
    pyautogui.mouseUp(x,y,button=button)
        
def randPress(key):
    if type(key) == int:
        for k in str(key):
            pydirectinput.keyDown(k)
            pydirectinput.keyUp(k)
    else:
        pydirectinput.keyDown(key)
        time.sleep(randPressDuration()/1000000000)
        pydirectinput.keyUp(key)

def randClickDuration(fast = False, interval = False):
    return np.random.normal(clickDurationAve,clickDurationSD)
    
def randPressDuration():
    return np.random.normal(pressDurationAve,pressDurationSD)

def activate_poe():
    if hwnd != win32gui.GetForegroundWindow():
        win32gui.SetForegroundWindow(hwnd)

def state(flag):
    threshold = 0.9
    if flag != 'trade_request' and flag != 'trade':
        print(flag)
        cursorToZero()
    if flag == 'accept_enabled':
        threshold = 0.95


    if flag == 'accept_unable':
        flag_img = cv2.imread(f'C:/Python/poe_img/{flag}_flag.png', cv2.IMREAD_UNCHANGED)
        frame = window_capture()
    elif flag == 'trade_request':
        flag_img = cv2.imread(f'C:/Python/poe_img/{flag}_flag.jpg', cv2.IMREAD_UNCHANGED)
        frame = window_capture()[415:473, 576:800]
    else:
        flag_img = cv2.imread(f'C:/Python/poe_img/{flag}_flag.jpg', cv2.IMREAD_UNCHANGED)
        frame = window_capture()
    
    result = cv2.matchTemplate(frame, flag_img, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    if max_val > threshold:
        return True
    else:
        return False

def openStash():
    if not state('stash'):
        activate_poe()
        flag = cv2.imread('C:/Python/poe_img/stash.png', cv2.IMREAD_UNCHANGED)
        h, w, a= flag.shape
        frame = window_capture()
        result = cv2.matchTemplate(frame, flag, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        rect = win32gui.GetWindowRect(hwnd)
        threshold = 0.9
        if max_val> threshold:
            declineTrade()
            randClick(rect[0]+max_loc[0]+margin_x+int(w/2),rect[1]+max_loc[1]+margin_y+int(h/2))
    while (not state('stash')) or state('stash_loading'):
        pass
    return True

def openTab(tab):
    print(state(tab))
    while not state(tab):
        activate_poe()
        openStash()
        time.sleep(0.5)
        rect = win32gui.GetWindowRect(hwnd)
        flag = cv2.imread(f'C:/Python/poe_img/{tab}_tab.jpg', cv2.IMREAD_UNCHANGED)
        h, w, a= flag.shape
        frame = window_capture()
        result = cv2.matchTemplate(frame, flag, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        threshold = 0.9
        if max_val> threshold:
            randClick(rect[0]+max_loc[0]+margin_x+int(w/2),rect[1]+max_loc[1]+margin_y+int(h/2))
        while state('stash_loading'):
            pass
        time.sleep(0.5)
        if tab == 'currency_general':
            randClick(rect[0]+margin_x+138,rect[1]+margin_y+82)
        elif tab == 'currency_influence':
            randClick(rect[0]+margin_x+233,rect[1]+margin_y+82)
        time.sleep(0.5)
    
    return True

def closeStash():
    if state('stash'):
        activate_poe()
        randPress('esc')

def closeTrade():
    if state('trade'):
        activate_poe()
        randPress('esc')

def interact(command, name = 'SoulDustGarrosh'):
    activate_poe()
    pyperclip.copy(f'/{command} {name}')
    randPress('enter')
    pydirectinput.keyDown('ctrl')
    randPress('v')
    pydirectinput.keyUp('ctrl')
    randPress('enter')

def cursorToZero():
    rect = win32gui.GetWindowRect(hwnd)
    pydirectinput.moveTo(rect[0]+margin_x+30,rect[1]+margin_y+45)

def count(tag, coord):
    '''
    inventory [321:478,434:796]
    trade [108:265,33:396]
    '''
    amount = 0
    cursorToZero()
    
    if coord == 'inventory' and state('inventory'):
        frame = window_capture()[321:478,434:796]
        x_ref = 434
        y_ref = 321
    elif coord == 'trade' and state('trade'):
        frame = window_capture()[108:265,33:396]
        x_ref = 33
        y_ref = 108
    else:
        return 0

    data = currency_dict
    max_stack = data[tag]['max_stack']

    flag = cv2.imread(f'C:/Python/poe_img/{tag}/{tag}.jpg', cv2.IMREAD_UNCHANGED)
    result = cv2.matchTemplate(frame, flag, cv2.TM_SQDIFF_NORMED)

    threshold = 0.15
    locations = np.where(result <= threshold)
    locations = list(zip(*locations[::-1]))
    
    rectangles = []
    for loc in locations:
        rect = [loc[0]+x_ref,loc[1]+y_ref,27,27]
        rectangles.append(rect)
        rectangles.append(rect)
    rectangles,weights = cv2.groupRectangles(rectangles,1,0.5)
    found = []
    
    for rect in rectangles:
        point = rect[0:2]
        i = pointToSquare(point,coord)
        found.append(i)
    
    for n in range(max_stack):
        flag = cv2.imread(f'C:/Python/poe_img/{tag}/{tag}_{n+1}.jpg', cv2.IMREAD_UNCHANGED)
        result = cv2.matchTemplate(frame, flag, cv2.TM_SQDIFF_NORMED)

        threshold = 0.08
        locations = np.where(result <= threshold)
        locations = list(zip(*locations[::-1]))
        rectangles = []
        for loc in locations:
            rect = [loc[0]+x_ref,loc[1]+y_ref,27,27]
            rectangles.append(rect)
            rectangles.append(rect)
        rectangles,weights = cv2.groupRectangles(rectangles,1,0.5)
        match = 0
        for rect in rectangles:
            point = rect[0:2]
            index = pointToSquare(point,coord)
            if index in found:
                match = match + 1
        amount = amount + (n+1)*match
    return amount

def pointToSquare(point,coord):
    if coord == 'inventory':
        x = [440,469,498,528,557,586,615,645,674,703,732,762]
        y = [327,356,385,414,444]
    elif coord == 'trade':
        x = [40,69,98,127,157,186,215,244,274,303,332,361]
        y = [113,143,172,201,230]
    x.append(point[0])
    y.append(point[1])
    x.sort()
    y.sort()
    return (y.index(point[1])-1)*12+(x.index(point[0])-1)

def filledSlot(coord):
    '''
    inventory [321:478,434:796]
    trade other[108:265,33:396]
    trade me[292:449,33:396]
    '''
    if not state('inventory'):
        randPress('i')
    cursorToZero()
    time.sleep(0.1)
    if coord == 'inventory':
        declineTrade()
        frame = window_capture()[321:478,434:796]
        inventory_slot = [(441,328),(470,328),(499,328),(529,328),(558,328),(587,328),(616,328),(646,328),(675,328),(704,328),(733,328),(763,328),
                          (441,357),(470,357),(499,357),(529,357),(558,357),(587,357),(616,357),(646,357),(675,357),(704,357),(733,357),(763,357),
                          (441,386),(470,386),(499,386),(529,386),(558,386),(587,386),(616,386),(646,386),(675,386),(704,386),(733,386),(763,386),
                          (441,415),(470,415),(499,415),(529,415),(558,415),(587,415),(616,415),(646,415),(675,415),(704,415),(733,415),(763,415),
                          (441,445),(470,445),(499,445),(529,445),(558,445),(587,445),(616,445),(646,445),(675,445),(704,445),(733,445),(763,445)]
    elif coord == 'trade':
        frame = window_capture()[108:265,33:396]
        inventory_slot = [(41,114),(70,114),(99,114),(128,114),(158,114),(187,114),(216,114),(245,114),(275,114),(304,114),(333,114),(362,114),
                          (41,144),(70,144),(99,144),(128,144),(158,144),(187,144),(216,144),(245,144),(275,144),(304,144),(333,144),(362,144),
                          (41,173),(70,173),(99,173),(128,173),(158,173),(187,173),(216,173),(245,173),(275,173),(304,173),(333,173),(362,173),
                          (41,202),(70,202),(99,202),(128,202),(158,202),(187,202),(216,202),(245,202),(275,202),(304,202),(333,202),(362,202),
                          (41,231),(70,231),(99,231),(128,231),(158,231),(187,231),(216,231),(245,231),(275,231),(304,231),(333,231),(362,231)]
    else:
        pass
    
    filled_slot = copy.deepcopy(inventory_slot)
    flag = cv2.imread('C:/Python/poe_img/empty.jpg', cv2.IMREAD_UNCHANGED)
    result = cv2.matchTemplate(frame, flag, cv2.TM_SQDIFF_NORMED)
    threshold = 0.1
    locations = np.where(result <= threshold)
    locations = list(zip(*locations[::-1]))
    rectangles = []
    for loc in locations:
        if coord == 'inventory':
            rect = [loc[0]+434,loc[1]+321,27,27]
        elif coord == 'trade':
            rect = [loc[0]+33,loc[1]+108,27,27]
        else:
            pass
        rectangles.append(rect)
        rectangles.append(rect)
    rectangles,weights = cv2.groupRectangles(rectangles,1,0.5)
    for rect in rectangles:
        point = rect[0:2]
        index = pointToSquare(point,coord)
        filled_slot.remove(inventory_slot[index])
    return filled_slot

def inventoryToTrade(f):
    declineTrade()
    if f and state('trade'):
        rect = win32gui.GetWindowRect(hwnd)
        img_list = []
        activate_poe()
        recursion_list = []
        for slot in f:
            declineTrade()
            img = window_capture()[slot[1]:slot[1]+27,slot[0]:slot[0]+27]
            img_list.append(img)
        
        pydirectinput.keyDown('ctrl')
        for slot in f:
            if not state('trade'):
                pydirectinput.keyUp('ctrl')
                return
            randClick(rect[0]+margin_x+slot[0]+13,rect[1]+margin_y+slot[1]+13)
        pydirectinput.keyUp('ctrl')
        cursorToZero()
        time.sleep(0.1)
        for i, slot in enumerate(f):
            declineTrade()
            img = window_capture()[slot[1]:slot[1]+27,slot[0]:slot[0]+27]
            result = cv2.matchTemplate(img, img_list[i], cv2.TM_SQDIFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
            if min_val < 0.15:
                recursion_list.append(slot)
        inventoryToTrade(recursion_list)

def inventoryToStash(filled_slot):
    declineTrade()
    if filled_slot:
        rect = win32gui.GetWindowRect(hwnd)
        img_list = []
        activate_poe()
        recursion_list = []
        if state('stash'):
            randPress('esc')
            randPress('i')
        if not state('inventory'):
            randPress('i')
        cursorToZero()
        time.sleep(0.1)

        openStash()
        while not state('stash') or state('stash_loading'):
            pass
        
        pydirectinput.keyDown('ctrl')
        for slot in filled_slot:    
            declineTrade()
            randClick(rect[0]+margin_x+slot[0]+13,rect[1]+margin_y+slot[1]+13)
        pydirectinput.keyUp('ctrl')

        if state('stash'):
            randPress('esc')
            randPress('i')
        if not state('inventory'):
            randPress('i')
        cursorToZero()
        time.sleep(0.1)
        inventoryToStash(filledSlot('inventory'))

def retrieve(currency, amount, existing = 0):
    activate_poe()
    data = currency_dict
    openTab(data[currency]['tab'])
    while not state('stash') or state('stash_loading'):
        pass
    stash_coord = data[currency]['stash_coord']
    max_stack = data[currency]['max_stack']
    quotient = (amount-existing)//max_stack
    remainder = (amount-existing)%max_stack
    rect = win32gui.GetWindowRect(hwnd)

    pydirectinput.keyDown('ctrl')
    for i in range(quotient):
        time.sleep(0.13)
        declineTrade()
        randClick(rect[0]+margin_x+stash_coord[0],rect[1]+margin_y+stash_coord[1])
    pydirectinput.keyUp('ctrl')

    if remainder:
        flag = cv2.imread('C:/Python/poe_img/empty.jpg', cv2.IMREAD_UNCHANGED)
        frame = window_capture()[321:478,434:796]
        result = cv2.matchTemplate(frame, flag, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        
        pydirectinput.keyDown('shift')
        time.sleep(0.2)
        declineTrade()
        randClick(rect[0]+margin_x+stash_coord[0],rect[1]+margin_y+stash_coord[1])
        pydirectinput.keyUp('shift')
        randPress(remainder)
        randPress('enter')
        time.sleep(0.2)
        declineTrade()
        randClick(rect[0]+margin_x+434+max_loc[0]+13,rect[1]+margin_y+321+max_loc[1]+13)
        
    time.sleep(0.2)
    if state('stash'):
        randPress('esc')
        randPress('i')
    if not state('inventory'):
        randPress('i')
    cursorToZero()
    time.sleep(0.4)
    counted = count(currency,'inventory')
    if counted < amount:
        retrieve(currency,amount,existing = counted)
    elif counted > amount:
        inventoryToStash(filledSlot('inventory'))
        retrieve(currency,amount,existing = 0)

def logStream(input_lock, mouseQue, trade_list, hideout_list, party_list, currency_dict, target = 'INFO Client'):
    def inParty(name):
        for index, member in enumerate(party_list):
            if member['name'] == name:
                return index
        return None
    while True:
        buffer = len(target)
        original_target = target
        fh = codecs.open('C:/Program Files (x86)/Grinding Gear Games/Path of Exile/logs/Client.txt', encoding='utf8', errors='ignore')
        fh.seek(0, os.SEEK_END)
        size = fh.tell()
        #find a chunk where target string is part of
        pointer = fh.tell()-buffer
        while True:
            pointer = pointer-buffer
            if pointer < 0:
                print('cannot find target')
                break
            fh.seek(pointer)
            snip = fh.read(2*buffer)
            if target in snip:
                break
        fh.seek(pointer)
        #travel to the line where the string is part of
        while True:
            if pointer > size:
                print('cannot find target')
                break
            snip = fh.read(buffer)
            fh.seek(pointer)
                
            if snip == target:
                break
            pointer = pointer +1
        fh.seek(pointer)

        #travel to the beginning of line
        while True:
            if pointer < 0:
                print('cannot find target')
                break
            snip = fh.read(1)
            if snip == '\r':
                break
            pointer = pointer - 1
            fh.seek(pointer)

        #dump each line into message que
        fh.seek(pointer)
        msgChunk = fh.read().split('\r\n')
        fh.close()
        
        #---------------------------------------------
        for msg in msgChunk:
            if msg:
                target = msg
                if original_target not in target:
                    if isTradeMsg(msg):
                        print(msg)
                        if not ' for ' in msg:
                            continue
                        name, give_item, give_amount, receive_item, receive_amount = parseTradeMsg(msg)
                        print(give_item, give_amount, receive_item, receive_amount)
                        valid = True
                        #validity check with notes
                        for index, item in enumerate(receive_item):
                            if (give_item == 'chaos' and item == 'exalted') or (give_item == 'exalted' and item == 'chaos') or (give_item !='chaos' and give_item != 'exalted'):
                                print('case1')
                                if not currency_dict[give_item]['note']:
                                    valid = False
                                    break
                                note_ratio = currency_dict[give_item]['note'].split(' ')[-2]
                            elif (give_item == 'chaos' or give_item == 'exalted') and item != 'exalted':
                                print('case2')
                                print(currency_dict[item])
                                if not currency_dict[item]['buy_note']:
                                    valid = False
                                    break
                                note_ratio = currency_dict[item]['buy_note'].split(' ')[-2]
                            if not math.isclose(float(Fraction(note_ratio)), receive_amount[index]/give_amount, rel_tol=0.01):
                                valid = False
                                break
                        if not valid:
                            print('invalid')
                            
                        print('valid')

                        #stock check
                        temp = copy.deepcopy(currency_dict)
                        for trade in trade_list:
                            for item, amount in zip(trade['give item'], trade['give amount']):
                                temp[item]['stock'] = temp[item]['stock'] - amount
                        if give_amount > temp[give_item]['stock']:
                            print('not enough stock')
                            continue
                        print('enough stock')

                        if len(receive_amount) == 1:
                            #if give_amount > 60*currency_dict[give_item]['max_stack'] or receive_amount[0] > 60*currency_dict[receive_item[0]]['max_stack']:
                            if (give_item == 'chaos' and receive_item[0] == 'exalted') or (give_item == 'exalted' and receive_item[0] == 'chaos') or (give_item !='chaos' and give_item != 'exalted'):
                                note_ratio = currency_dict[give_item]['note'].split(' ')[-2]
                            elif (give_item == 'chaos' or give_item == 'exalted') and item != 'exalted' and item != 'chaos':
                                note_ratio = currency_dict[receive_item[0]]['buy_note'].split(' ')[-2]

                            give_unit = int(note_ratio.split('/')[1])
                            receive_unit = int(note_ratio.split('/')[0])
                            if receive_unit > give_unit:
                                quotient = 60*currency_dict[receive_item[0]]['max_stack']//receive_unit
                            elif give_unit >= receive_unit:
                                quotient = 60*currency_dict[give_item]['max_stack']//give_unit

                            index = 0
                            while give_amount > 0:
                                temp = tradeTemplate()
                                temp['name'] = name
                                temp['index'] = index
                                index = index + 1
                                temp['give item'].append(give_item)
                                temp['receive item'].append(receive_item[0])
                                if give_amount > give_unit * quotient:
                                    temp['give amount'].append(give_unit * quotient)
                                    temp['receive amount'].append(receive_unit * quotient)
                                    give_amount = give_amount - give_unit * quotient
                                    receive_amount[0] = receive_amount[0] - receive_unit * quotient
                                else:
                                    temp['give amount'].append(give_amount)
                                    temp['receive amount'].append(receive_amount[0])
                                    give_amount = 0
                                    receive_amount[0] = 0
                                trade_list.append(temp)
                            if len(temp['give amount'])>1:
                                s = []
                                for give_amount, receive_amount in zip(temp['give amount'], temp['receive amount']):
                                    s.append(f'{str(give_amount)}/{str(receive_amount)}')
                                input_lock.acquire()
                                pyperclip.copy(f'@{name} '+'+'.join(s))
                                randPress('enter')
                                pydirectinput.keyDown('ctrl')
                                randPress('v')
                                pydirectinput.keyUp('ctrl')
                                randPress('enter')
                                input_lock.release()
                            
                            if inParty(name) == None:
                                temp = partyTemplate()
                                temp['name'] = name
                                temp['invited'] = time.time()
                                party_list.append(temp)
                            input_lock.acquire()
                            interact('invite', name)
                            input_lock.release()

                    elif isAreaMsg(msg):
                        print(msg)
                        name, hideout_state = parseAreaMsg(msg)
                        if hideout_state == 'joined':
                            hideout_list.append(name)
                            print('joined')
                        elif hideout_state == 'left':
                            try:
                                hideout_list.remove(name)
                            except:
                                pass
                    elif isTradeStateMsg(msg):
                        print(msg)
                        mouseQue.put('accepted')
                    elif isAfkMsg(msg):
                        print(msg)
                        input_lock.acquire()
                        closeStash()
                        time.sleep(0.3)
                        openStash()
                        input_lock.release()
                    else:
                        pass
        #-------------------------------------------
        time.sleep(0.2)
        if state('trade_request'):
            rect = win32gui.GetWindowRect(hwnd)
            input_lock.acquire()
            randClick(rect[0]+margin_x+750,rect[1]+margin_y+430)
            input_lock.release()

def mouseStream(input_lock, mouseQue, noteQue, trade_list, hideout_list, party_list, currency_dict):
    def inParty(name):
        for index, member in enumerate(party_list):
            if member['name'] == name:
                return index
        return None

    def timeout(name,duration):
        index = inParty(name)
        temp = party_list[index]
        temp['timeout'] = duration
        temp['timeout init'] = time.time()
        temp['strike'] = temp['strike'] + 1
        party_list.pop(index)
        party_list.append(temp)
        return inParty(name)

    def priceItem(tag, mode, note):
        data = currency_dict
        rect = win32gui.GetWindowRect(hwnd)
        # if item is chaos or exalted, it is only sold on the currency tab
        '''if tag == 'chaos' or tag == 'exalted':
            if stock == 0:
                return
            tab = data[tag]['tab']
            stash_coord = data[tag]['stash_coord']
        else:'''
        stock = data[tag]['stock']
        if mode == 'sell':
            if stock == 0:
                return
            tab = data[tag]['tab']
            stash_coord = data[tag]['stash_coord']
            print(note)
            print(data[tag]['note'])
            print(stash_coord)
            if note != data[tag]['note']:
                time.sleep(1)
                openTab(tab)
                randClick(rect[0]+margin_x+stash_coord[0],rect[1]+margin_y+stash_coord[1], button='right')
                time.sleep(1)
                print('flag 1')
                flag = cv2.imread('C:/Python/poe_img/note_flag.jpg', cv2.IMREAD_UNCHANGED)
                frame = window_capture()
                result = cv2.matchTemplate(frame, flag, cv2.TM_CCOEFF_NORMED)
                min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
                
                print(max_loc)
                time.sleep(1)
                print('flag 2')
                randClick(rect[0]+margin_x+max_loc[0]+8,rect[1]+margin_y+max_loc[1]+32)
                time.sleep(1)
                print('flag 3')
                randClick(rect[0]+margin_x+max_loc[0]+8,rect[1]+margin_y+max_loc[1]+52)
                time.sleep(1)
                pyperclip.copy(note)
                randClick(rect[0]+margin_x+max_loc[0]+38,rect[1]+margin_y+max_loc[1]+32)
                time.sleep(1)
                pydirectinput.keyDown('ctrl')
                randPress('a')
                randPress('v')
                pydirectinput.keyUp('ctrl')
                randPress('enter')
            time.sleep(1)
        elif mode == 'buy':
            tab = 'misc'
            stash_coord = data[tag]['buy_coord']
            print(stash_coord)
            if note != data[tag]['note'] or note != data[tag]['buy_note']:
                pass

    while True:
        rect = win32gui.GetWindowRect(hwnd)
        ready = False
        # release all information 300s after invitation or timeout 3 times
        for party in copy.deepcopy(party_list):
            if time.time()-party['invited'] > 300 or time.time()-party['invited'] < 0 or party['strike'] >= 3:
                name = party['name']
                for trade in copy.deepcopy(trade_list):
                    if trade['name'] == name:
                        trade_list.remove(trade)
                party_list.remove(party)
                input_lock.acquire()
                inventoryToStash(filledSlot('inventory'))
                interact('kick', name)
                input_lock.release()
                print(f'{name} has been purged')
            if party['strike'] >= 3:
                pyperclip.copy(f'@{name} sorry you\'re annoying')
                randPress('enter')
                pydirectinput.keyDown('ctrl')
                randPress('v')
                pydirectinput.keyUp('ctrl')
                randPress('enter')

        # clear timeout
        for party in copy.deepcopy(party_list):
            if (time.time()-party['timeout init'] > party['timeout']) and party['timeout']:
                name = party['name']
                temp = copy.deepcopy(party)
                temp['timeout'] = 0
                temp['timeout init'] = 0
                party_list.remove(party)
                party_list.append(temp)
                print(f'{name} timeout cleared')

        for trade in copy.deepcopy(trade_list):
            name = trade['name']
            party_index = inParty(name)
            if name in hideout_list and party_list[party_index]['timeout'] == 0:
                ready = True
        
        #iterate through trade list
        for trade in copy.deepcopy(trade_list):
            name = trade['name']
            party_index = inParty(name)
            if name in hideout_list and party_list[party_index]['timeout'] == 0:
                # retrieve item from stash and request trade
                input_lock.acquire()
                for item, amount in zip(trade['give item'], trade['give amount']):
                    retrieve(item, amount)
                interact('tradewith',name)
                
                # timeout condition for cancelled trade request
                trade_timer = time.time()
                while not state('trade'):
                    while state('waiting_trade'):
                        trade_timer = time.time()
                    if time.time()-trade_timer > 3:
                        print(f'{name} timeout 1')
                        party_index = timeout(name, 15)
                        break
                input_lock.release()
                
                if party_list[party_index]['timeout']:
                    input_lock.acquire()
                    inventoryToStash(filledSlot('inventory'))
                    input_lock.release()
                    continue

                # put items in trade window if trade is open
                input_lock.acquire()
                inventoryToTrade(filledSlot('inventory'))
                input_lock.release()

                # timeout if trade is cancelled
                if not state('trade'):
                    print(f'{name} timeout 2')
                    party_index = timeout(name, 15)
                    input_lock.acquire()
                    inventoryToStash(filledSlot('inventory'))
                    input_lock.release()
                    continue

                while state('trade'):
                    trade_timer = time.time()
                    while True:
                        # timeout if trade takes too long(60s)
                        if time.time()-trade_timer >60:
                            input_lock.acquire()
                            closeTrade()
                            input_lock.release()
                            print(f'{name} timeout 3')
                            party_index = timeout(name, 15)
                            break
                        # timeout if trade is cancelled
                        elif not state('trade'):
                            print(f'{name} timeout 4')
                            party_index = timeout(name, 15)
                            break
                            
                        # if accept is enabled, break if amount is confirmed
                        if state('accept_enabled'):
                            input_lock.acquire()
                            accept = False
                            for item, amount in zip(trade['receive item'], trade['receive amount']):
                                if count(item, 'trade') >= amount:
                                    accept = True
                                else:
                                    accept = False
                            input_lock.release()    
                            if accept:
                                break

                        # if accept is not enabled, swipe trade window for grayed items
                        else:
                            input_lock.acquire()
                            f = filledSlot('trade')
                            for slot in f:
                                pydirectinput.moveTo(rect[0]+margin_x+slot[0]+13,rect[1]+margin_y+slot[1]+13)
                            input_lock.release()

                    # if for some reason timeout has occurred, break
                    if party_list[party_index]['timeout']:
                        break
                    
                    # click accept
                    input_lock.acquire()
                    randClick(rect[0]+margin_x+77,rect[1]+margin_y+463)
                    input_lock.release()

                    trade_timer = time.time()
                    while state('trade'):
                        # timeout if trade takes too long
                        if time.time()-trade_timer >20:
                            input_lock.acquire()
                            closeTrade()
                            input_lock.release()
                            print(f'{name} timeout 5')
                            party_index = timeout(name, 15)
                        elif state('trade_changed'):
                            break
                        elif state('accept_unable'):
                            break
                
                if party_list[party_index]['timeout']:
                    input_lock.acquire()
                    inventoryToStash(filledSlot('inventory'))
                    input_lock.release()
                    continue
                
                trade_timer = time.time()
                # if trade accepted flag does not arrive in 2 seconds, timeout
                while time.time()-trade_timer<2:
                    if not mouseQue.empty():
                        mouseQue.get()
                        input_lock.acquire()
                        inventoryToStash(filledSlot('inventory'))
                        trade_list.remove(trade)
                        # adjust stock
                        for give_item, give_amount, receive_item, receive_amount in zip(trade['give item'], trade['give amount'], trade['receive item'], trade['receive amount']):
                            give_temp = copy.deepcopy(currency_dict[give_item])
                            receive_temp = copy.deepcopy(currency_dict[receive_item])
                            give_temp['stock'] = give_temp['stock'] - give_amount
                            receive_temp['stock'] = receive_temp['stock'] + receive_amount
                            currency_dict[give_item] = give_temp
                            currency_dict[receive_item] = receive_temp

                        remaining = False
                        for remaining_trade in trade_list:
                            if remaining_trade['name'] == name:
                                remaining = True
                        if not remaining:
                            party_list.pop(party_index)
                            interact('kick',name)
                        input_lock.release()
                        time.sleep(0.5)
                        break
                if trade in trade_list:
                    print(f'{name} timeout 6')
                    party_index = timeout(name, 15)
                    input_lock.acquire()
                    inventoryToStash(filledSlot('inventory'))
                    input_lock.release()
            
        time.sleep(1)

def update():
    print('asdf')
    root.after(1000, update)

if __name__ == '__main__':
    pydirectinput.PAUSE = 0
    pyautogui.PAUSE = 0

    root = uiConfig()
    root.after(1000, update)
    root.mainloop()  
    
    '''keyboardQue = Queue()
    mouseQue = Queue()
    priorityQue = Queue()
    noteQue = Queue()

    manager = Manager()
    trade_list = manager.list([])
    hideout_list = manager.list([])
    party_list = manager.list([])
    currency_list = list(currency_dict)
    currency_dict = manager.dict(currency_dict)

    logStreamProcess = Process(target=logStream, args=(input_lock, mouseQue, trade_list, hideout_list, party_list, currency_dict))
    mouseStreamProcess = Process(target=mouseStream, args=(input_lock, mouseQue, noteQue, trade_list, hideout_list, party_list, currency_dict))

    logStreamProcess.start()
    mouseStreamProcess.start()
    
    logStreamProcess.join()
    mouseStreamProcess.join()'''



    #[337:355,763:790]
    #[357:370,733:746]
    
    #print(currency_dict['fusing'])
    #print('ready')
    #retrieve('chaos', 200)
    #inventoryToStash(filledSlot('inventory'))
    #cv2.imwrite('C:/Python/poe_img/asddfdffasdf.jpg', window_capture())
    #retrieve('lesser-eldritch-ichor', 10, existing = 0)
    #print(count('exalted','inventory'))
    
    window_close()