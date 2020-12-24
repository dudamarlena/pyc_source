# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/karas/training/extensions/lr_scheduler.py
# Compiled at: 2019-01-07 03:50:47
# Size of source mod 2**32: 215 bytes
from karas.training import extension

class LrScheduler(extension.Extension):

    def __init__(self, scheduler):
        self._scheduler = scheduler

    def __call__(self, trainer):
        self._scheduler.step()