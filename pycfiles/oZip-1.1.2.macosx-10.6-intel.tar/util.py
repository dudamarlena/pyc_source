# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/site-packages/oZip/core/util.py
# Compiled at: 2014-09-02 10:10:57


def str2bin(data):
    """ Convert a string into a binary format """
    temp = None
    if len(data) % 8 != 0:
        temp = data[-(len(data) % 8):]
    data = [ data[8 * i:8 * (i + 1)] for i in range(len(data) / 8) ]
    if temp:
        data.append(temp)
    data = [ int(i, 2) for i in data ]
    data = ('').join(chr(i) for i in data)
    return data


def bin2str(data):
    """ Read a binary string into decompressable format """
    data = [ ord(i) for i in data ]
    data = [ ('{:08b}').format(int(bin(i), 2)) for i in data ]
    temp = data[(-1)]
    while temp[0] == '0':
        temp = temp[1:]

    data[-1] = temp
    return ('').join(data)