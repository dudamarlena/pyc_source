# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/picharsso/configer.py
# Compiled at: 2019-11-08 16:27:15
# Size of source mod 2**32: 467 bytes
from json import load, dump
from types import SimpleNamespace
from os.path import join, dirname

class Configer:
    __doc__ = 'A wrapper to load configuration\n    '

    def __init__(self):
        self.config_file = join(dirname(__file__), 'config.json')
        self.load_config()

    def load_config(self):
        with open(self.config_file, 'r') as (f):
            self.configuration = SimpleNamespace(**load(f))

    def config(self):
        print(self.config_file)