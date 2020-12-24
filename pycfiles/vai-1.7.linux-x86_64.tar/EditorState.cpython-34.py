# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/sbo/lib/python3.4/site-packages/vai/models/EditorState.py
# Compiled at: 2015-05-02 14:07:56
# Size of source mod 2**32: 1678 bytes
import os, copy, json
from .. import paths

class EditorState:
    __doc__ = '\n    Class containing recoverable state that wants to survive quit/reopen of the editor.\n    The state is dumped to a file in json format.\n    '
    _instance = None

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def __init__(self):
        if self._instance is not None:
            raise Exception('Only one instance allowed')
        self._state = {}
        try:
            with open(paths.stateFile(), 'r') as (f):
                self._state = json.loads(f.read())
        except:
            self._state = {}

    def setCursorPosForPath(self, absolute_path, cursor_pos):
        if 'buffers' not in self._state:
            self._state['buffers'] = []
        buffers = self._state['buffers']
        for b in buffers:
            if b.get('absolute_path') == absolute_path:
                b['cursor_pos'] = cursor_pos
                continue
        else:
            buffers.append({'absolute_path': absolute_path,  'cursor_pos': cursor_pos})

    def cursorPosForPath(self, absolute_path):
        buffers = self._state.get('buffers', [])
        for b in buffers:
            if b.get('absolute_path') == absolute_path:
                return tuple(b.get('cursor_pos'))

    def save(self):
        """Store the contained state onto the state file"""
        with open(paths.stateFile(), 'w') as (f):
            f.write(json.dumps(self._state))