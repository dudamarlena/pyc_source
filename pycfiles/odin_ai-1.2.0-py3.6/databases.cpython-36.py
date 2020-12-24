# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/odin/fuel/databases.py
# Compiled at: 2019-07-19 10:36:05
# Size of source mod 2**32: 25795 bytes
from __future__ import print_function, division, absolute_import
import os, io, mmap, marshal, sqlite3
from itertools import chain
from six import add_metaclass
from six.moves import cPickle
from contextlib import contextmanager
from abc import ABCMeta, abstractmethod, abstractproperty
from collections import OrderedDict, Iterator, defaultdict, MutableMapping, Mapping
import numpy as np
from odin.utils import async, is_string, ctext
__all__ = [
 'NoSQL',
 'MmapDict',
 'TableDict',
 'SQLiteDict']

def _dump(x):
    if isinstance(x, np.str_):
        x = str(x)
    return marshal.dumps(x)


@add_metaclass(ABCMeta)
class NoSQL(MutableMapping):
    __doc__ = ' The idea of this is transform everything (even SQL) into\n  (key, value) kind-of database.\n  '
    _INSTANCES = defaultdict(dict)

    def __new__(subclass, path, read_only=False, cache_size=250, *args, **kwargs):
        if not is_string(path):
            raise ValueError('`path` for MmapDict must be string, but given object with type: %s' % type(path))
        path = os.path.abspath(path)
        read_only = bool(read_only)
        cache_size = int(cache_size)
        all_instances = NoSQL._INSTANCES[subclass.__name__]
        if path in all_instances:
            return all_instances[path]
        else:
            new_instance = super(NoSQL, subclass).__new__(subclass)
            all_instances[path] = new_instance
            new_instance._cache_size = cache_size
            new_instance._read_only = read_only
            new_instance._new_args_called = False
            new_instance._path = path
            new_instance._is_closed = False
            return new_instance

    def __init__(self, path, read_only=False, cache_size=250, override=False):
        super(NoSQL, self).__init__()
        if override:
            if os.path.exists(path):
                if os.path.isfile(path):
                    os.remove(path)
        try:
            self._restore_dict(self.path, self.read_only, self.cache_size)
        except Exception as e:
            del NoSQL._INSTANCES[self.__class__.__name__][self.path]
            import traceback
            traceback.print_exc()
            raise e

    @abstractmethod
    def _restore_dict(self, path, read_only, cache_size):
        raise NotImplementedError

    @abstractmethod
    def _close(self):
        raise NotImplementedError

    @abstractmethod
    def _flush(self, save_all):
        raise NotImplementedError

    def __getstate__(self):
        if not self._new_args_called:
            raise RuntimeError('You must use argument `protocol=cPickle.HIGHEST_PROTOCOL` when using `pickle` or `cPickle` to be able pickling NoSQL.')
        self._new_args_called = False
        return (self.path, self.read_only, self.cache_size)

    def __setstate__(self, states):
        path, read_only, cache_size = states
        if not os.path.exists(path):
            raise ValueError('Cannot find store NoSQL database at path: %s.If you have moved the database, the dumps from cannot restore the previous intance.' % path)
        self._restore_dict(path, read_only, cache_size)
        self._path = path
        self._read_only = read_only
        self._cache_size = cache_size

    def __getnewargs__(self):
        self._new_args_called = True
        return (self.path,)

    @property
    def cache_size(self):
        return self._cache_size

    @property
    def read_only(self):
        return self._read_only

    @property
    def path(self):
        return self._path

    @property
    def is_closed(self):
        return self._is_closed

    def close(self):
        if self._is_closed:
            return
        else:
            self._is_closed = True
            if not self.read_only:
                self.flush(save_all=True)
            del NoSQL._INSTANCES[self.__class__.__name__][self.path]
            try:
                self._close()
            except AttributeError as e:
                pass

    def flush(self, save_all=True):
        if self.read_only or self.is_closed:
            return
        else:
            self._flush(save_all=(bool(save_all)))
            return self

    def __call__(self, key):
        return self.__getitem__(key)

    def set(self, key, value):
        self.__setitem__(key, value)
        return self

    @abstractmethod
    def __setitem__(self, key, value):
        raise NotImplementedError

    @abstractmethod
    def __getitem__(self, key):
        raise NotImplementedError

    @abstractmethod
    def __delitem__(self, key):
        raise NotImplementedError

    @abstractmethod
    def __len__(self):
        raise NotImplementedError

    def __iter__(self):
        return self.items()

    @abstractmethod
    def keys(self):
        raise NotImplementedError

    @abstractmethod
    def values(self):
        raise NotImplementedError

    @abstractmethod
    def items(self):
        raise NotImplementedError

    def __del__(self):
        self.close()

    def __repr__(self):
        return str(self)

    def update(*args, **kwargs):
        self = args[0]
        if self.read_only:
            return self
        else:
            return (super(NoSQL, self).update)(*args, **kwargs)

    def clear(self):
        if self.read_only:
            return self
        else:
            return super(NoSQL, self).clear()

    def __cmp__(self, d):
        if isinstance(d, NoSQL):
            return self.path == d.path
        raise ValueError('Cannot compare NoSQL to other type (i.e. %s)' % d.__class__.__name__)


def _safe_loading_indices(file_obj, class_name, path):
    try:
        return cPickle.loads(file_obj)
    except Exception as e:
        del NoSQL._INSTANCES[class_name][path]
        import traceback
        traceback.print_exc()
        raise e


class MmapDict(NoSQL):
    __doc__ = " MmapDict\n  Handle enormous dictionary (up to thousand terabytes of data) in\n  memory mapped dictionary, extremely fast to load, and for randomly access.\n  The alignment of saved files:\n\n  ==> |'mmapdict'|48-bytes(max_pos)|48-bytes(dict_size)|MmapData|indices-dict|\n\n  * The first 48-bytes number: is ending position of the Mmmap, start from\n  the (8 + 48 + 48) bytes.\n\n  * The next 48-bytes number: is length of pickled indices (i.e. the\n  indices start from max_pos to max_pos + dict_size)\n\n  Note\n  ----\n  Only support (key, value) types = (str, primitive_type)\n  MmapDict read speed is double faster than SQLiteDict.\n  MmapDict also support multiprocessing\n  "
    HEADER = b'mmapdict'
    SIZE_BYTES = 48
    MAX_INDICES_SIZE = 25

    def _restore_dict(self, path, read_only, cache_size):
        if os.path.exists(path):
            if os.path.getsize(path) == 0:
                if read_only:
                    raise Exception('File at path:"%s" has zero size, no data found in (read-only mode).' % path)
            file = open((str(path)), mode='rb+')
            if file.read(len(MmapDict.HEADER)) != MmapDict.HEADER:
                file.close()
                raise Exception('Given file is not in the right format for MmapDict.')
            max_position = int(file.read(MmapDict.SIZE_BYTES))
            dict_size = int(file.read(MmapDict.SIZE_BYTES))
            file.seek(max_position)
            pickled_indices = file.read(dict_size)
            self._indices_dict = async(_safe_loading_indices)(pickled_indices, self.__class__.__name__, path)
        else:
            file = open((str(path)), mode='wb+')
            file.write(MmapDict.HEADER)
            header = ('%' + str(MmapDict.SIZE_BYTES) + 'd') % (len(MmapDict.HEADER) + MmapDict.SIZE_BYTES * 2)
            file.write(header.encode())
            data_size = ('%' + str(MmapDict.SIZE_BYTES) + 'd') % 0
            file.write(data_size.encode())
            file.flush()
            self._indices_dict = {}
        self._file = file
        self._mmap = mmap.mmap((file.fileno()), length=0, offset=0, flags=(mmap.MAP_SHARED))
        self._increased_indices_size = 0.0
        self._cache_dict = {}

    def _close(self):
        self._mmap.close()
        self._file.close()
        del self._indices_dict
        del self._cache_dict

    def _flush(self, save_all=False):
        """
    Parameters
    ----------
    save_all: bool
        force the indices dictionary to be saved, even though,
        its increased hasn't reach the maximum.
    """
        if self.is_closed or self.read_only:
            return
        else:
            file = self._file
            file.seek(len(MmapDict.HEADER))
            max_position = int(file.read(MmapDict.SIZE_BYTES))
            file.seek(max_position)
            for key, value in self._cache_dict.items():
                try:
                    value = _dump(value)
                except ValueError:
                    raise RuntimeError('Cannot marshal.dump %s' % str(value))

                self.indices[key] = (
                 max_position, len(value))
                max_position += len(value)
                file.write(value)
                self._increased_indices_size += (16 + len(key)) / 1024.0 / 1024.0

            indices_length = 0
            if save_all or self._increased_indices_size > MmapDict.MAX_INDICES_SIZE:
                indices_dump = cPickle.dumps((self.indices), protocol=(cPickle.HIGHEST_PROTOCOL))
                indices_length = len(indices_dump)
                file.write(indices_dump)
                self._increased_indices_size = 0.0
            file.seek(len(MmapDict.HEADER))
            max_position = ('%' + str(MmapDict.SIZE_BYTES) + 'd') % max_position
            file.write(max_position.encode())
            if indices_length > 0:
                indices_length = ('%' + str(MmapDict.SIZE_BYTES) + 'd') % indices_length
                file.write(indices_length.encode())
        file.flush()
        self._mmap.close()
        del self._mmap
        self._mmap = mmap.mmap((file.fileno()), length=0, offset=0, flags=(mmap.MAP_SHARED))
        del self._cache_dict
        self._cache_dict = {}

    @property
    def indices(self):
        if not isinstance(self._indices_dict, Mapping):
            self._indices_dict = self._indices_dict.get()
        return self._indices_dict

    @property
    def is_loaded(self):
        if self.is_closed:
            return False
        else:
            if not isinstance(self._indices_dict, Mapping):
                return self._indices_dict.finished
            return True

    def __str__(self):
        length = None if self.is_closed else str(len(self.indices) + len(self._cache_dict))
        cache_length = 'None' if self.is_closed else str(len(self._cache_dict))
        fmt = '<MmapDict path:"%s", length:%s/%s, loaded:%s, closed:%s, read_only:%s>'
        return fmt % (self.path, length, cache_length,
         self.is_loaded, self.is_closed, self.read_only)

    def __setitem__(self, key, value):
        if self.read_only:
            return
        key = str(key)
        self._cache_dict[key] = value
        if len(self._cache_dict) > self.cache_size:
            self.flush(save_all=False)

    def __getitem__(self, key):
        if key in self._cache_dict:
            return self._cache_dict[key]
        else:
            start, size = self.indices[key]
            self._mmap.seek(start)
            return marshal.loads(self._mmap.read(size))

    def __contains__(self, key):
        return key in self.indices or key in self._cache_dict

    def __len__(self):
        return len(self.indices) + len(self._cache_dict)

    def __delitem__(self, key):
        if self.read_only:
            return
        else:
            if key in self._cache_dict:
                del self._cache_dict
            else:
                del self.indices[key]

    def keys(self):
        return chain(self.indices.keys(), self._cache_dict.keys())

    def values(self):
        for name, (start, size) in self.indices.items():
            self._mmap.seek(start)
            yield marshal.loads(self._mmap.read(size))

        for val in self._cache_dict.values():
            yield val

    def items(self):
        for name, (start, size) in self.indices.items():
            self._mmap.seek(start)
            yield (name, marshal.loads(self._mmap.read(size)))

        for key, val in self._cache_dict.values():
            yield (
             key, val)


def _adapt_array(arr):
    """ Converts np.array to TEXT when inserting
  http://stackoverflow.com/a/31312102/190597 (SoulNibbler)
  """
    out = io.BytesIO()
    np.save(out, arr)
    out.seek(0)
    return sqlite3.Binary(out.read())


def _convert_array(text):
    """ Converts TEXT to np.array when selecting """
    out = io.BytesIO(text)
    out.seek(0)
    return np.load(out)


class TableDict(MutableMapping):

    def __init__(self, sqlite, table_name):
        if not isinstance(sqlite, SQLiteDict):
            raise ValueError('`sqlite` must be instance of SQLiteDict')
        self._sqlite = sqlite
        self._name = str(table_name)

    @contextmanager
    def table_context(self):
        """Return temporary context that switch the SQLite to given table"""
        curr_tab = self._sqlite.current_table
        self._sqlite.set_table(self._table_name)
        yield
        self._sqlite.set_table(curr_tab)

    @property
    def sqlite(self):
        return self._sqlite

    @property
    def name(self):
        return self._name

    def flush(self):
        with self.table_context():
            self._sqlite.flush()

    @property
    def connection(self):
        return self._sqlite.connection

    @property
    def cursor(self):
        return self._sqlite.cursor

    @property
    def path(self):
        return self._sqlite.path

    @property
    def is_closed(self):
        return self._sqlite.is_closed

    def __setstate__(self, states):
        self._sqlite, self._name = states

    def __getstate__(self):
        return (
         self.sqlite, self.name)

    def __str__(self):
        pass

    def __repr__(self):
        return str(self)

    def set(self, key, value):
        self.__setitem__(key, value)
        return self

    def __setitem__(self, key, value):
        with self.table_context():
            return self._sqlite.__setitem__(key, value)

    def __getitem__(self, key):
        with self.table_context():
            return self._sqlite.__getitem__(key)

    def update(self, items):
        with self.table_context():
            self._sqlite.update(items)
        return self

    def __iter__(self):
        with self.table_context():
            return self._sqlite.__iter__()

    def __contains__(self, key):
        with self.table_context():
            return self._sqlite.__contains__(key)

    def __len__(self):
        with self.table_context():
            return self._sqlite.__len__()

    def __delitem__(self, key):
        with self.table_context():
            return self._sqlite.__delitem__(key)

    def __cmp__(self, dict):
        if isinstance(dict, TableDict):
            return self._sqlite is dict._sqlite and self._table_name == dict._table_name
        else:
            return False

    def keys(self):
        with self.table_context():
            return self._sqlite.keys()

    def values(self):
        with self.table_context():
            return self._sqlite.values()

    def items(self):
        with self.table_context():
            return self._sqlite.items()

    def clear(self):
        with self.table_context():
            self._sqlite.clear()
        return self


class SQLiteDict(NoSQL):
    __doc__ = ' Using SQLite in key-value pair manner\n\n  Example\n  -------\n  >>> path = \'/tmp/tmp.db\'\n  >>> db = SQLiteDict(path)\n  >>> db1 = SQLiteDict(path)\n  >>> print(id(db) == id(db1)) # True\n  >>> def sett(i):\n  ...     db = SQLiteDict(path)\n  ...     db[i] = \'Process%d\' % i\n  ...     db.close()\n  >>> def get(i):\n  ...     db = SQLiteDict(path)\n  ...     print("Get", db[i])\n  >>> pros = [Process(target=sett, args=(i,))\n  ...         for i in range(10)]\n  >>> [p.start() for p in pros]\n  >>> [p.join() for p in pros]\n  ...\n  >>> db = SQLiteDict(path)\n  >>> print(db.items())\n  >>> print(db[0])\n  ...\n  >>> pros = [Process(target=get, args=(i,))\n  ...         for i in range(10)]\n  >>> [p.start() for p in pros]\n  >>> [p.join() for p in pros]\n\n  Note\n  ----\n  numpy.ndarray will be converted to list before dumped to the database,\n  hence, the speed of serialize and deserialize ndarray is extremely slow.\n  This dict is purely performing in multiprocessing\n  '
    _DEFAULT_TABLE = '_default_'

    def _restore_dict(self, path, read_only, cache_size):
        self._cache = defaultdict(dict)
        self._conn = sqlite3.connect(path, detect_types=(sqlite3.PARSE_DECLTYPES))
        self._conn.text_factory = str
        self._cursor = self._conn.cursor()
        self.connection.execute('PRAGMA main.locking_mode = EXCLUSIVE;')
        self.connection.execute('PRAGMA main.synchronous = 0;')
        self.connection.execute('PRAGMA journal_mode = MEMORY;')
        self.connection.commit()
        self._current_table = SQLiteDict._DEFAULT_TABLE
        self.set_table(SQLiteDict._DEFAULT_TABLE)

    def _flush(self, save_all=False):
        curr_tab = self.current_table
        tables = self.get_all_tables() if save_all else [curr_tab]
        for tab in tables:
            self.set_table(tab)
            if len(self.current_cache) > 0:
                self.cursor.executemany('INSERT INTO {tb} VALUES (?, ?)'.format(tb=tab), [(str(k), _dump(v.tolist()) if isinstance(v, np.ndarray) else _dump(v)) for k, v in self.current_cache.items()])
                self.connection.commit()
                self.current_cache.clear()

        return self.set_table(curr_tab)

    def _close(self):
        self._conn.close()

    def as_table(self, table_name):
        return TableDict(self, table_name)

    def set_table(self, table_name):
        if table_name is None:
            table_name = SQLiteDict._DEFAULT_TABLE
        table_name = str(table_name)
        if not self.is_table_exist(table_name):
            query = 'CREATE TABLE {tb} (\n                            key text NOT NULL,\n                            value text NOT NULL,\n                            PRIMARY KEY (key)\n                        );'
            self.cursor.execute(query.format(tb=table_name))
            self.connection.commit()
        self._current_table = table_name
        return self

    @property
    def current_table(self):
        return self._current_table

    @property
    def current_cache(self):
        return self._cache[self.current_table]

    def get_all_tables(self):
        query = "SELECT name FROM sqlite_master where type='table';"
        self.cursor.execute(query)
        return [table[0] for table in self.cursor.fetchall()]

    def drop_table(self, table_name=None):
        if self.read_only:
            return
        else:
            if table_name is None:
                table_name = self._current_table
                self._current_table = SQLiteDict._DEFAULT_TABLE
            else:
                table_name = str(table_name)
            if table_name == SQLiteDict._DEFAULT_TABLE:
                raise ValueError('Cannot drop default table.')
            self.cursor.execute('DROP TABLE {tb};'.format(tb=table_name))
            return self

    def is_table_exist(self, table_name):
        try:
            self.cursor.execute('SELECT 1 FROM %s LIMIT 1;' % table_name)
            self.cursor.fetchone()
        except sqlite3.OperationalError as e:
            if 'no such table' in str(e):
                return False
            raise e

        return True

    def __str__(self):
        curr_tab = self.current_table
        s = '<' + ctext('SQLiteDB:', 'red') + '%s>\n' % self.path
        all_tables = self.get_all_tables()
        name_fmt = '%' + str(max(len(i) for i in all_tables)) + 's'
        for tab in all_tables:
            self.set_table(tab)
            s += ' ' + ctext(name_fmt % tab, 'yellow') + ': db=%d cache=%d\n' % (
             len(self), len(self.current_cache))

        self.set_table(curr_tab)
        return s[:-1]

    @property
    def connection(self):
        return self._conn

    @property
    def cursor(self):
        return self._cursor

    def __setitem__(self, key, value):
        if self.read_only:
            raise RuntimeError('Cannot __setitem__ for this Dict in read_only mode.')
        key = str(key)
        self.current_cache[key] = value
        if len(self.current_cache) >= self._cache_size:
            self.flush()
            self.current_cache.clear()

    def __getitem__(self, key):
        if isinstance(key, (tuple, list, np.ndarray)):
            query = 'SELECT value FROM {tb}\n                       WHERE key IN {keyval};'
            keyval = '(' + ', '.join(['"%s"' % str(k) for k in key]) + ')'
            self.cursor.execute(query.format(tb=(self._current_table), keyval=keyval))
            results = self.cursor.fetchall()
            if len(results) != len(key):
                raise KeyError("Cannot find all `key`='%s' in the dictionary." % keyval)
            results = [marshal.loads(r[0]) for r in results]
        else:
            key = str(key)
            if key in self.current_cache:
                return self.current_cache[key]
            query = 'SELECT value FROM {tb} WHERE key="{keyval}" LIMIT 1;'
            results = self.connection.execute(query.format(tb=(self._current_table), keyval=key)).fetchone()
            if results is None:
                raise KeyError("Cannot find `key`='%s' in the dictionary." % key)
            results = marshal.loads(results[0])
        return results

    def __contains__(self, key):
        key = str(key)
        if key in self.current_cache:
            return True
        else:
            query = 'SELECT 1 FROM {tb} WHERE key="{keyval}" LIMIT 1;'
            self.cursor.execute(query.format(tb=(self._current_table), keyval=key))
            if self.cursor.fetchone() is None:
                return False
            return True

    def __len__(self):
        query = 'SELECT COUNT(1) FROM {tb}'.format(tb=(self._current_table))
        self.cursor.execute(query)
        n = self.cursor.fetchone()[0]
        return n + len(self.current_cache)

    def __delitem__(self, key):
        if self.read_only:
            return
        else:
            query = 'DELETE FROM {tb} WHERE {cond};'
            if isinstance(key, (tuple, list, Iterator, np.ndarray)):
                key = [str(k) for k in key]
            else:
                key = [
                 str(key)]
        db_key = []
        for k in key:
            if k in self.current_cache:
                del self.current_cache[k]
            else:
                db_key.append(k)

        self.cursor.execute(query.format(tb=(self._current_table), cond=('key IN ("%s")' % ', '.join(db_key))))
        self.connection.commit()

    def keys(self):
        for k in self.cursor.execute('SELECT key from {tb};'.format(tb=(self._current_table))):
            yield k[0]

        for k in self.current_cache.keys():
            yield k

    def values(self):
        for val in self.cursor.execute('SELECT value from {tb};'.format(tb=(self._current_table))):
            yield marshal.loads(val[0])

        for v in self.current_cache.values():
            yield v

    def items(self):
        for item in self.cursor.execute('SELECT key, value from {tb};'.format(tb=(self._current_table))):
            yield (
             item[0], marshal.loads(item[1]))

        for k, v in self.current_cache.items():
            yield (
             k, v)

    def update(self, items):
        if self.read_only:
            return
        else:
            query = 'UPDATE {tb} SET value=(?) WHERE key=("?");'
            if isinstance(items, Mapping):
                items = items.items()
            db_update = []
            for key, value in items:
                key = str(key)
                if key in self.current_cache:
                    self.current_cache[key] = value
                else:
                    db_update.append((_dump(value), key))

            self.cursor.executemany(query.format(tb=(self._current_table)), db_update)
            self.connection.commit()
            return self

    def clear(self):
        if self.read_only:
            return
        else:
            self.cursor.execute('TRUNCATE TABLE {tb};'.format(tb=(self._current_table)))
            self.connection.commit()
            self.current_cache.clear()
            return self