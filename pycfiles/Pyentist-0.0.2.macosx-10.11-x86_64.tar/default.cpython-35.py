# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/mpcabd/Projects/pyentist/env/lib/python3.5/site-packages/pyentist/default.py
# Compiled at: 2016-02-23 16:52:28
# Size of source mod 2**32: 222 bytes
from .experiment import Experiment

class DefaultExperiment(Experiment):

    def __init__(self, name):
        self.name = name

    def is_enabled(self):
        return True

    def publish(self, result):
        pass