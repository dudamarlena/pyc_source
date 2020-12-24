# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/mengliu/Dropbox/Research/graph_lib/graph_lib/wrappers/python/read_seed.py
# Compiled at: 2017-09-07 23:15:41


def read_seed(filename):
    f = open(filename)
    data = f.read()
    data = data.split()
    nseedids = int(data[0])
    seedids = []
    for i in range(nseedids):
        seedids += [data[(i + 1)]]

    f.close()
    return (seedids, nseedids)