# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\dragonfly\engines\recobs_base.py
# Compiled at: 2009-04-06 11:18:28
"""
Recognition observer base class
============================================================================

"""
from ..log import get_log

class RecObsManagerBase(object):
    _log = get_log('engine')

    def __init__(self, engine):
        self._engine = engine
        self._enabled = True
        self._observers = []
        self._observer_ids = set()

    def enable(self):
        if not self._enabled:
            self._enabled = True
            self._activate()

    def disable(self):
        if self._enabled:
            self._enabled = False
            self._deactivate()

    def register(self, observer):
        if id(observer) in self._observer_ids:
            return
        elif not self._observers:
            self._activate()
        self._observers.append(observer)
        self._observer_ids.add(id(observer))

    def unregister(self, observer):
        try:
            self._observers.remove(observer)
            self._observer_ids.remove(id(observer))
        except ValueError:
            pass
        else:
            if not self._observers:
                self._deactivate()

    def notify_begin(self):
        for observer in self._observers:
            if hasattr(observer, 'on_begin'):
                observer.on_begin()

    def notify_recognition(self, result, words):
        for observer in self._observers:
            if hasattr(observer, 'on_recognition'):
                observer.on_recognition(result, words)

    def notify_failure(self, result):
        for observer in self._observers:
            if hasattr(observer, 'on_failure'):
                observer.on_failure(result)

    def _activate(self):
        raise NotImplementedError(str(self))

    def _deactivate(self):
        raise NotImplementedError(str(self))