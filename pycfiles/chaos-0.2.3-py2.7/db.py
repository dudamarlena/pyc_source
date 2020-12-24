# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/chaos/db.py
# Compiled at: 2014-10-31 10:19:18
import gdbm, json, collections

def dump_simple_db(path):
    """
        Dumps a SimpleDb as string in the following format:
        <key>: <json-encoded string>
        """
    output = []
    simpledb = SimpleDb(path, mode='r', sync=False)
    with simpledb as (db):
        for key in db:
            output.append(('{0}: {1}').format(key, db.dumpvalue(key)))

    return ('\n').join(output)


class SimpleDb(collections.MutableMapping):
    """
        Implements a simple key/value store based on GDBM. Values are stored as JSON strings,
        to allow for more complex values than GDBM itself can provide.

        This class implements the full MutableMapping ABC, which means that after using open(),
        or using with, this class behaves as a dict. All changes will be saved to disk after
        using close() or ending the with statement.
        """

    def __init__(self, path, mode='c', sync=True):
        """
                Store the given parameters internally and prepare for opening the database later.

                Arguments
                ---------
                path: string
                        Path where to create or open the database
                mode: string
                        What mode to use when opening the database:
                        - "r" (read-only)
                        - "w" (read-write)
                        - "c" (read-write, create when not exists)
                        - "n" (read-write, always create new file)
                sync: boolean
                        If set to True, data will be flushed to disk after every change.
                """
        self.path = path
        self.mode = mode + ('s' if sync else '')
        self.db = None
        return

    def _checkopen(self):
        if self.db == None:
            raise RuntimeError('SimpleDb was not opened')
        return

    def open(self):
        """
                Open the GDBM database internally.
                """
        return self.__enter__()

    def close(self):
        """
                Close the internal GDBM database.
                """
        self.__exit__(None, None, None)
        return

    def dumpvalue(self, key):
        """
                Retrieves the given key, and returns the raw JSON encoded string.
                """
        self._checkopen()
        return self.db[key]

    def __enter__(self):
        self.db = gdbm.open(self.path, self.mode)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self._checkopen()
        self.db.sync()
        self.db.close()
        self.db = None
        return

    def __getitem__(self, key):
        self._checkopen()
        return json.loads(self.db[key])

    def __setitem__(self, key, value):
        self._checkopen()
        self.db[key] = json.dumps(value)

    def __delitem__(self, key):
        self._checkopen()
        del self.db[key]

    def __iter__(self):
        self._checkopen()
        key = self.db.firstkey()
        while key != None:
            yield key
            key = self.db.nextkey(key)

        if key == None:
            raise StopIteration()
        return

    def __len__(self):
        self._checkopen()
        return len(self.db)