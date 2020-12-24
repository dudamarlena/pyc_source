# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dbETL/pyAPI.py
# Compiled at: 2018-02-25 15:31:20
import os, sys, shutil
from time import time, ctime
import requests, imp
try:
    secret = imp.load_source('key', 'secret.py')
except:
    print 'plase create secret.py with key="apikey=yourapi"'
    exit(0)

key = secret.key
print key
SS = 'https://storage.scrapinghub.com/items/276632/'
cell = 'format=csv&fields=post_ID,comments,favor,views&include_headers=1'
try:
    os.mkdir('data')
    os.mkdir('archive')
    os.mkdir('archive/trash')
except:
    pass

def api(ID, start, end):
    ID, start, end = int(ID), int(start), int(end)
    have = [ int(i.split('.csv')[0].split('_')[(-1)]) for i in os.listdir('data') if i.endswith('.csv') and int(i.split('diary_')[(-1)].split('_')[0]) == ID
           ]
    point = time()
    for i in range(start, end + 1):
        if i in have:
            print ID, i, 'have downloaded already'
            continue
        string = SS + str(ID) + '/' + str(i) + '?' + key + '&' + cell
        print ID, i, ctime()
        try:
            response = requests.get(string, timeout=20)
        except:
            print 'time out'
            continue

        name = 'diary_' + str(ID) + '_' + str(i) + '.csv'
        with open(name, 'w') as (fh):
            fh.write(response.text)
        print name, ('used: {:.2f} s').format(time() - point)
        point = time()

    CSVs = [ i for i in os.listdir('.') if i.startswith('diary_' + str(ID)) ]
    for j in CSVs:
        st = os.stat(j)
        if st.st_size < 819200:
            shutil.move(j, 'archive/trash/' + j)
        else:
            shutil.move(j, 'data/' + j)


if __name__ == '__main__':
    ID, start, end = sys.argv[1:]
    print ID, start, end
    api(ID, start, end)