# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/recur7down/products.py
# Compiled at: 2018-01-08 23:32:04
from recur7down import Collect
import sys
from time import time, ctime, strftime, localtime
from multiprocessing import cpu_count
from multiprocessing.dummy import Pool as ThreadPool
import pandas as pd, os

def helper((link, place, cat)):
    instance = Collect(link, place, cat)
    instance.main()
    instance.save()


def product_main():
    try:
        sys.path.append(os.getcwd())
        from info import link, cat, large, small
        print 'imported data from info'
        sys.path.remove(os.getcwd())
    except:
        print 'lack of info.py'
        exit(0)

    cpu = int(raw_input('(multi-processing) how many process to run ? '))
    try:
        from info import link, cat, large, small
        print 'imported data from info'
    except:
        print 'lack of info.py'
        exit(0)

    swim = []
    for i in small:
        swim.append((link, i, 0))

    for p in large:
        for c in cat:
            swim.append((link, p, c))

    print 'combinations: ' + str(len(swim))
    start = time()
    pool = ThreadPool(cpu)
    results = pool.map(helper, swim)
    pool.close()
    pool.join()
    end = time()
    elapse = end - start
    print ('used {:.2f} s, {:.2f} mins').format(elapse, elapse / 60)
    print 'start concating data'
    ct = ctime().split()
    path = ct[2] + ct[1] + ct[(-1)] + '_product/'
    files = os.listdir(path)
    len(files)
    df = pd.concat([ pd.read_excel(path + i) for i in files ])
    print df.shape
    print 'removing duplicates'
    col = list(df.columns)
    col = [col.pop(col.index('pid')), col.pop(col.index('title'))] + col
    df = df[col]
    df = df.reset_index(drop=True)
    df = df.loc[df['pid'].drop_duplicates().index, :]
    print df.shape
    print 'saving to products.xlsx'
    df.to_excel(strftime('%Y-%m-%d-%H-%M', localtime()) + ' Products.xlsx', encoding='utf-8', index=False)
    print 'done!', ctime()