# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/plover_vcs/message_generator/line_changes.py
# Compiled at: 2020-04-03 01:04:01
# Size of source mod 2**32: 578 bytes
from typing import List

class LineChanges:

    def __init__(self, added: List[str]=None, deleted: List[str]=None):
        self._LineChanges__added = [] if added is None else added
        self._LineChanges__deleted = [] if deleted is None else deleted

    @property
    def added(self) -> List[str]:
        return self._LineChanges__added

    @added.setter
    def added(self, added: List[str]):
        self._LineChanges__added = added

    @property
    def deleted(self) -> List[str]:
        return self._LineChanges__deleted

    @deleted.setter
    def deleted(self, deleted: List[str]):
        self._LineChanges__deleted = deleted