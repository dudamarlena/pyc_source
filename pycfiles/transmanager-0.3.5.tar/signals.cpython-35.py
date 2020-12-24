# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /var/www/transmanager/transmanager/signals.py
# Compiled at: 2017-07-27 04:21:44
# Size of source mod 2**32: 704 bytes
import logging
from .settings import TM_DISABLED
logger = logging.getLogger(__name__)

def object_on_pre_save(sender, instance, **kwargs):
    if TM_DISABLED:
        return
    from .manager import Manager
    man = Manager()
    man.start(sender, instance, **kwargs)


class SignalBlocker(object):
    __doc__ = '\n    Class used to block the models signals in certains cases\n    '

    def __init__(self, signal):
        self.signal = signal
        self.receivers = signal.receivers

    def __enter__(self, *args, **kwargs):
        self.signal.receivers = []

    def __exit__(self, *args, **kwargs):
        self.signal.receivers = self.receivers