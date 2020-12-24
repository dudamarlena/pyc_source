# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dj/workspace/dyson-py/lib/dyson/utils/module.py
# Compiled at: 2016-11-07 22:16:35
# Size of source mod 2**32: 476 bytes
import os
from dyson import constants
from abc import abstractmethod
import sys
from dyson.constants import to_boolean

class DysonModule:

    def __init__(self):
        pass

    @abstractmethod
    def run(self, webdriver, params):
        pass

    def fail(self, msg):
        print(msg, file=sys.stderr)
        if not to_boolean(constants.DEFAULT_SELENIUM_PERSIST):
            exit(2)


def get_module_path():
    return os.path.dirname(os.path.realpath(__file__))