import multiprocessing as mp
import asyncio
import time
import random

import request_to_discord as rd

def sync(n):
    print(f'lock has been retrieved by process {n}')

def get_time():
    t = time.localtime()
    return time.strftime("%H:%M:%S", t)

async def task1(q):
    while True:
        if q.empty():
            #print('process 1 did not detect lock in que')
            pass
            
        else:
            q.get()
            sync(1)
            print(f'task1 started at {get_time()}')
            print(len(rd.retrieve_messages('874662778592460851')))
            await asyncio.sleep(random.random()*3)
            print(f'task1 finished at {get_time()}')
        await asyncio.sleep(random.random())

async def task2(q):
    while True:
        if q.empty():
            #print('process 2 did not detect lock in que')
            pass
            
        else:
            q.get()
            sync(2)
            print(f'task2 started at {get_time()}')
            await asyncio.sleep(random.random()*3)
            print(f'task2 finished at {get_time()}')
        await asyncio.sleep(random.random())
        
async def time_lock(q):
    rate_limit = 2
    while True:
        if q.empty():
            t = get_time()
            #print(f'there is no lock in que. timer started at{t}')
            await asyncio.sleep(1/rate_limit)
            q.put('lock')
            t = get_time()
            #print(f'lock has been put in que at {t}')
        else:
            await asyncio.sleep(0.001)




async def start_task(q,func):
    task = asyncio.create_task(func(q))
    await task

def create_process(q, func):
    asyncio.run(start_task(q,func))

if __name__ == '__main__':
    q = mp.Queue()
    q.put('lock_init')
    p1 = mp.Process(target=create_process, args=(q,task1))
    p3 = mp.Process(target=create_process, args=(q,time_lock))

    p1.start()
    p3.start()
    p1.join()
    p3.join()

    print('finished')
    