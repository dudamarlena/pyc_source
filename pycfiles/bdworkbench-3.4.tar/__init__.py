# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/krishna/sources/catalogsdk/bdworkbench/baseimg/__init__.py
# Compiled at: 2018-06-04 14:09:38
from __future__ import print_function
from .. import Command
from .baseimg_init import BaseimgInit

class Baseimg(Command):
    """

    """

    def __init__(self, wb, config, inmemStore):
        Command.__init__(self, wb, config, inmemStore, 'baseimg', '')
        BaseimgInit(config, inmemStore, self)


__all__ = [
 'Baseimg']
Command.register(Baseimg)