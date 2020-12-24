# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pysentosa/tradeinfo.py
# Compiled at: 2016-03-13 09:01:11
__author__ = 'Wu Fuheng(henry.woo@outlook.com)'
__version__ = '0.1.32'
import os, json
POSITION_STATUS = [
 'NOPOS',
 'OTL',
 'OTS',
 'DELIMITER',
 'LWaitC',
 'LWaitC2',
 'SWaitC',
 'SWaitC2',
 'NWaitL',
 'NWaitL2',
 'NWaitS',
 'NWaitS2']

def getTI0(mypath):
    if not os.path.exists(mypath):
        return (None, None)
    else:
        onlyfiles = [ os.path.join(mypath, f) for f in os.listdir(mypath) if os.path.isfile(os.path.join(mypath, f)) and f.endswith('json')
                    ]
        ti = None
        dt = None
        tmp = None
        pat = None
        for f in onlyfiles:
            dt = f.split(os.sep)[(-1)].split('.')[0]
            if f.endswith('vola.json'):
                pass
            elif tmp is None or tmp < dt:
                tmp = dt
                pat = f

        if os.path.exists(pat):
            j = json.load(open(pat))
            ti = j['_tinfo']
        return (ti, tmp)


def getTI(sym):
    from config import TRADEINFODIR
    mypath = TRADEINFODIR + os.sep + sym
    return getTI0(mypath)


def getTI2(sym, dt):
    from config import TRADEINFODIR
    mypath = TRADEINFODIR + os.sep + sym + os.sep + dt + '.json'
    j = json.load(open(mypath))
    ti = j['_tinfo']
    return (
     ti, dt)


if __name__ == '__main__':
    from pprint import pprint
    ti, dt = getTI('TAOM')
    pprint(ti)