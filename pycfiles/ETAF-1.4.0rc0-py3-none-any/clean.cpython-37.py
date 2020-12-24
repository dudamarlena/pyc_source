# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sage/fatedoc/FATE/arch/api/base/utils/clean.py
# Compiled at: 2020-04-28 09:19:05
# Size of source mod 2**32: 3368 bytes
from collections import deque
from arch.api.utils.log_utils import getLogger
LOGGER = getLogger()

class Rubbish(object):
    __doc__ = '\n    a collection collects all tables / objects in federation tagged by `tag`.\n    '

    def __init__(self, name, tag):
        self._name = name
        self._tag = tag
        self._tables = []
        self._kv = {}

    @property
    def tag(self):
        return self._tag

    def add_table(self, table):
        self._tables.append(table)

    def add_obj(self, table, key):
        if (
         table._name, table._namespace) not in self._kv:
            self._kv[(table._name, table._namespace)] = (
             table, [key])
        else:
            self._kv[(table._name, table._namespace)][1].append(key)

    def merge(self, rubbish: 'Rubbish'):
        self._tables.extend(rubbish._tables)
        for tk, (t, k) in rubbish._kv.items():
            if tk in self._kv:
                self._kv[tk][1].extend(k)
            else:
                self._kv[tk] = (
                 t, k)

        return self

    def empty(self):
        self._tables = []
        self._kv = {}

    def clean(self):
        if self._tables or self._kv:
            LOGGER.debug(f"[CLEAN] {self._name} cleaning rubbishes tagged by {self._tag}")
        for table in self._tables:
            try:
                LOGGER.debug(f"[CLEAN] try destroy table {table}")
                table.destroy()
            except:
                pass

        for _, (table, keys) in self._kv.items():
            for key in keys:
                try:
                    LOGGER.debug(f"[CLEAN] try delete object with key={key} from table={table}")
                    table.delete(key)
                except:
                    pass


class Cleaner(object):

    def __init__(self):
        self._ashcan = deque()

    def push(self, rubbish):
        """
        append `rubbish`
        :param rubbish: a rubbish instance
        :return:
        """
        if self.is_latest_tag(rubbish.tag):
            self._ashcan[(-1)].merge(rubbish)
        else:
            self._ashcan.append(rubbish)
        return self

    def is_latest_tag(self, tag):
        return len(self._ashcan) > 0 and self._ashcan[(-1)].tag == tag

    def keep_latest_n(self, n):
        while len(self._ashcan) > n:
            self._ashcan.popleft().clean()

    def clean_all(self):
        while len(self._ashcan) > 0:
            self._ashcan.popleft().clean()