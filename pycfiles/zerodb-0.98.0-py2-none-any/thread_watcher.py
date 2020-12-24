# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /zerodb/util/thread_watcher.py
# Compiled at: 2015-12-09 01:37:29
from __future__ import print_function
import threading, weakref
from functools import partial

class ThreadWatcher(object):

    class Vigil(object):
        pass

    def __init__(self):
        self._refs = {}
        self._local = threading.local()

    def _on_death(self, vigil_id, callback, args, ref):
        self._refs.pop(vigil_id)
        callback(*args)

    def watch(self, callback, *args):
        if not self.is_watching():
            self._local.vigil = v = ThreadWatcher.Vigil()
            on_death = partial(self._on_death, id(v), callback, args)
            ref = weakref.ref(v, on_death)
            self._refs[id(v)] = ref

    def is_watching(self):
        """Is the current thread being watched?"""
        try:
            v = self._local.vigil
            return id(v) in self._refs
        except AttributeError:
            return False

    def unwatch(self):
        try:
            v = self._local.vigil
            del self._local.vigil
            self._refs.pop(id(v))
        except AttributeError:
            pass