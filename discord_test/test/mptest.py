import multiprocessing as mp


def f(d, l):
    d[1] = '1'
    d['asd'] = 2
    d[0.25] = None
    d['qwqwe'] = False
    l.reverse()

if __name__ == '__main__':
    manager = mp.Manager()
    d = manager.dict()
    l = manager.list(range(10))
    d['qwqwe'] = True

    p = mp.Process(target=f, args=(d, l))
    p.start()
    p.join()

    print(d)
    print(l)