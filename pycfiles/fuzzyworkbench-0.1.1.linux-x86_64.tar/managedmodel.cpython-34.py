# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.4/dist-packages/fuzzyworkbench/managedmodel.py
# Compiled at: 2015-10-01 12:54:48
# Size of source mod 2**32: 419 bytes


class ManagedModel:
    __doc__ = 'A model in which changes are monitored'

    def __init__(self, editor):
        self._editor = editor
        self._changed = False

    def _do_changed(self, *args):
        self._changed = True
        if self._editor:
            self._editor.notify(self)

    def hasChanged(self):
        return self._changed

    def save(self):
        self._changed = False