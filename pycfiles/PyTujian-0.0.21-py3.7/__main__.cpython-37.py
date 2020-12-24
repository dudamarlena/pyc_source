# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/PyTujian/__main__.py
# Compiled at: 2020-05-03 11:23:59
# Size of source mod 2**32: 1368 bytes
import sys, os, signal
from getopt import getopt
from .helper import TujianHelper
from .tools import printSort, getToday, getArchive, getAll, printByPID, getByPID
from .upload import upoladPics
from . import print2
pars = sys.argv[1:]
try:
    opt, par = getopt(pars, 'hp:', ['help', 'path='])
except:
    TujianHelper(pars)

dir = './Tujian/'
path = os.path.abspath(dir)

def exitTujian(signum, frame):
    raise KeyboardInterrupt('操作被用户终止')


signal.signal(signal.SIGINT, exitTujian)
signal.signal(signal.SIGTERM, exitTujian)
for o, a in opt:
    if o in ('-h', '--help'):
        par2 = [
         'help'] + par
        TujianHelper(par2)
        sys.exit()

if not os.path.isdir(path):
    os.makedirs(path)
else:
    try:
        key = par[0]
    except IndexError:
        TujianHelper(par)
        sys.exit()

    if key == 'help':
        TujianHelper(par)
    else:
        if key == 'path':
            print(path)
        else:
            if key == 'today':
                getToday(path)
            else:
                if key == 'archive':
                    getArchive(par, path)
                else:
                    if key == 'sort':
                        printSort()
                    else:
                        if key == 'all':
                            getAll(path)
                        else:
                            if key == 'info':
                                printByPID(par)
                            else:
                                if key == 'upload':
                                    upoladPics(par)
                                else:
                                    if key == 'get':
                                        getByPID(par, path)
                                    else:
                                        print2.error('找不到这个命令')
                                        print('使用 help 查看帮助')
                                        sys.exit(1)
sys.exit()