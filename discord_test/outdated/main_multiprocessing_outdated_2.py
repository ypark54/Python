import multiprocessing as mp
import time
import datetime as dt

import request_to_discord as rd

def get_time():
    t = time.localtime()
    return time.strftime("%H:%M:%S", t)

def time_to_int(t):
    date_string = dt.datetime.strptime(t.rsplit('+')[0], '%Y-%m-%dT%H:%M:%S.%f')
    date_int = int(dt.datetime.strftime(date_string, '%Y%m%d%H%M%S%f'))
    return date_int

def discord_messages(q,channel_id):
    while True:
        if not q[0].empty():
            q[0].get()
            print(f'lock has been retrieved by channel {channel_id}at {get_time()}')
            q[1].put(channel_id)
            q[2].put(rd.retrieve_messages(channel_id))
            print(f'{channel_id} finished at {get_time()}')

def time_lock(q,limit_upper):
    while True:
        if q[0].empty():
            t = get_time()
            print(f'there is no lock in que. timer started at{t}')
            time.sleep(1/limit_upper)
            q[0].put('lock')
            t = get_time()
            print(f'lock has been put in que at {t}')
        else:
            pass

def min_rate(q,id,limit):
    while True:
        time.sleep(1/limit)
        id_copy = id[:]
        while not q[1].empty():
            channel_id = q[1].get()
            try:
                id_copy.remove(channel_id)
            except:
                pass
        print(f'The following channels have not been requested for the past second{id_copy}')
        for missing_id in id_copy:
            q[2].put(rd.retrieve_messages(missing_id))

def renew_message(q):
    save_message = None
    new_message = []
    threshold_time = 0

    while True:
        raw_message = q[2].get()
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
        for m in new_message:
            print(m['content'])

if __name__ == '__main__':
    #set up variables
    limit_upper = 1
    limit_lower = 0.01
    channel_id = ['966421494307639366']

    #initiate ques for communication
    lock_que = mp.Queue()           #lock que to restrict number of requests sent to discord server
    
    minimum_que = mp.Queue()        #que to track the number of requests sent by each thread to keep mininum update rate
    message_que = mp.Queue()                #que to pass on messages retrieved from discord server
    ui_que = mp.Queue()

    q = [lock_que, minimum_que, message_que, ui_que]
    
    #initiate multiprocess
    p = []
    for index, id in enumerate(channel_id, start=0):
        p.append(mp.Process(target=discord_messages, args=(q,id)))
        p.append(mp.Process(target=renew_message, args=(q,)))
    p.append(mp.Process(target=time_lock, args=(q,limit_upper)))
    p.append(mp.Process(target=min_rate, args=(q,channel_id,limit_lower)))
    
    
    for process in p:
        process.start()
    lock_que.put('lock_init')
    for process in p:
        process.join()

    