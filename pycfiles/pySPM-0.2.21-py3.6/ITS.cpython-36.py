# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\pySPM\ITS.py
# Compiled at: 2019-05-21 08:54:40
# Size of source mod 2**32: 777 bytes
from pySPM import Block, utils
import numpy as np, struct, os.path, zlib, re

class InvalidRAWdataformat(Exception):

    def __init__(self, block, msg):
        self.block = block
        self.msg = msg

    def __str__(self):
        return 'Invalid RAW dataformat seen in block ' + self.block.parent + '/' + self.block.name + ' : ' + self.msg


class ITS:

    def __init__(self, filename, debug=False):
        """
        ITS
        """
        self.filename = filename
        if not os.path.exists(filename):
            raise AssertionError
        else:
            self.f = open(self.filename, 'rb')
            self.Type = self.f.read(8)
            assert self.Type == b'ITStrF01'
        self.root = Block.Block(self.f)