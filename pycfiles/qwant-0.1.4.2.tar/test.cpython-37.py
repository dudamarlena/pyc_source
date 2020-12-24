# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/shinsheel/Документы/libs/anarcute/test.hy
# Compiled at: 2019-07-22 05:47:45
# Size of source mod 2**32: 483 bytes
import hy.macros
from hy.core.language import first, last
from anarcute.lib import *
hy.macros.require('anarcute.lib', None, assignments='ALL', prefix='')
import sys, os

def cowsay(s):
    return print('COWSAID', s)


def enroute(*args):
    compiler = 'hy' if first(sys.argv).endswith('.hy') else 'python3'
    cmd = '{} {} {} routed'.format(compiler, first(sys.argv), ' '.join(list(map(lambda x: json.dumps(x), args))))
    return os.popen(cmd)


route({'cs': cowsay})
enroute('cs', 'lolo') if (__name__ == '__main__' and 'routed' != last(sys.argv)) else None