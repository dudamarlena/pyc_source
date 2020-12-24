# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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