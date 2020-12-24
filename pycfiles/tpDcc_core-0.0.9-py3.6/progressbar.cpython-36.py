# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tpDcc/abstract/progressbar.py
# Compiled at: 2020-04-15 14:06:48
# Size of source mod 2**32: 910 bytes
"""
Module that contains abstract definition of basic DCC progress bar
"""
from tpDcc import register
from tpDcc.libs.python import decorators

class AbstractProgressBar(object):
    inc_value = 0

    def __init__(self, *args, **kwargs):
        self.progress_ui = None

    @decorators.abstractmethod
    def set_count(self, count_number):
        pass

    @decorators.abstractmethod
    def get_count(self):
        return 0

    @decorators.abstractmethod
    def status(self, status_str):
        pass

    @decorators.abstractmethod
    def end(self):
        pass

    @decorators.abstractmethod
    def break_signaled(self):
        pass

    @decorators.abstractmethod
    def set_progress(self, value):
        pass

    def inc(self, inc=1):
        self.__class__.inc_value += inc


register.register_class('DccProgressBar', AbstractProgressBar)