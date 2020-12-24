# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bibliopixel/util/image/directory.py
# Compiled at: 2019-08-11 12:22:47
# Size of source mod 2**32: 205 bytes
from . import gif

class Writer(gif.Writer):

    def __init__(self, writer):
        writer.gif_dir = writer.gif_dir or writer.basename
        super().__init__(writer)

    def write(self):
        pass