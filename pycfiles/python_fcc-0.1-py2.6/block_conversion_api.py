# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/python-fcc/block_conversion_api.py
# Compiled at: 2011-04-16 22:45:28
from generic_api import *

class BlockConversionAPI(GenericAPI):

    def __init__(self):
        GenericAPI.__init__(self, [('get_block', 'http://data.fcc.gov/api/block/find')])


if __name__ == '__main__':
    bc = BlockConversionAPI()
    print bc.get_block(lat=41, long=-87)