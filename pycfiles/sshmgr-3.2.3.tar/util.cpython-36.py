# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bugnofree/DevSpace/sshmgr/src/util.py
# Compiled at: 2019-04-25 04:34:16
# Size of source mod 2**32: 625 bytes
import os
from inspect import getframeinfo, stack

def get_data_root():
    dataroot = os.path.abspath(os.path.dirname(__file__))
    return os.path.join(dataroot, 'data')


def get_proj_root():
    rootpath = os.path.abspath(os.path.dirname(__file__))
    return rootpath


def get_version():
    with open(os.path.join(get_proj_root(), '__VERSION__'), 'r') as (_):
        return _.readline().strip()


def dbgprint(msg):
    caller = getframeinfo(stack()[1][0])
    print('[DBGINFO] ==> [%s -> %s -> %d]\n\t%s' % (
     caller.filename, caller.function, caller.lineno, msg))