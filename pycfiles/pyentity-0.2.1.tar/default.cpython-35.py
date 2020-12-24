# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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