# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/ssh_keydb/ssh_keydb.py
# Compiled at: 2013-02-18 13:07:40
from plugins.model import *
from plugins import *
from skeletool.options import *
from skeletool import *
VERSION = '0.2'

def run():
    MainApp('ssh_keydb', VERSION, dbinit).run()


if __name__ == '__main__':
    run()