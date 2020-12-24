# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/blacklight/git_tree/runbullet/runbullet/plugins/__init__.py
# Compiled at: 2017-11-03 13:31:08
# Size of source mod 2**32: 402 bytes
import os, sys

class Plugin(object):

    def __init__(self, config):
        self.config = config
        for cls in reversed(self.__class__.mro()):
            if cls is not object:
                try:
                    cls._init(self)
                except AttributeError as e:
                    pass

    def run(self, args):
        raise NotImplementedError()