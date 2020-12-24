# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/magland/src/ccm_widgets/generated/ccm_widgets/ccm_widgets/widgets/create_sync.py
# Compiled at: 2019-09-05 16:21:02
# Size of source mod 2**32: 617 bytes
import uuid

def create_sync(*state_keys):
    return SyncObject(state_keys)


class SyncObject:

    def __init__(self, state_keys):
        self._id = uuid.uuid4().hex.upper()
        self._state_keys = state_keys

    def map(self, **kwargs):
        for key in kwargs:
            if key not in self._state_keys:
                raise Exception('Key not found in sync state keys: {}'.format(key))

        return dict(id=(self._id),
          syncState=kwargs)

    def map_all(self):
        a = dict()
        for key in self._state_keys:
            a[key] = key

        return (self.map)(**a)