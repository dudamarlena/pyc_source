# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sanhehu/Documents/GitHub/pytq-project/pytq/pkg/sqlitedict.py
# Compiled at: 2017-11-23 13:02:06
"""
A lightweight wrapper around Python's sqlite3 database, with a dict-like interface
and multi-thread access support::

>>> mydict = SqliteDict('some.db', autocommit=True) # the mapping will be persisted to file `some.db`
>>> mydict['some_key'] = any_picklable_object
>>> print mydict['some_key']
>>> print len(mydict) # etc... all dict functions work

Pickle is used internally to serialize the values. Keys are strings.

If you don't use autocommit (default is no autocommit for performance), then
don't forget to call `mydict.commit()` when done with a transaction.

"""
import sqlite3, os, sys, tempfile, random, logging, traceback
from threading import Thread
try:
    __version__ = __import__('pkg_resources').get_distribution('sqlitedict').version
except:
    __version__ = '?'

major_version = sys.version_info[0]
if major_version < 3:
    if sys.version_info[1] < 5:
        raise ImportError('sqlitedict requires python 2.5 or higher (python 3.3 or higher supported)')

    def exec_(_code_, _globs_=None, _locs_=None):
        """Execute code in a namespace."""
        if _globs_ is None:
            frame = sys._getframe(1)
            _globs_ = frame.f_globals
            if _locs_ is None:
                _locs_ = frame.f_locals
            del frame
        elif _locs_ is None:
            _locs_ = _globs_
        exec 'exec _code_ in _globs_, _locs_'
        return


    exec_('def reraise(tp, value, tb=None):\n    raise tp, value, tb\n')
else:

    def reraise(tp, value, tb=None):
        if value is None:
            value = tp()
        if value.__traceback__ is not tb:
            raise value.with_traceback(tb)
        raise value
        return


try:
    from cPickle import dumps, loads, HIGHEST_PROTOCOL as PICKLE_PROTOCOL
except ImportError:
    from pickle import dumps, loads, HIGHEST_PROTOCOL as PICKLE_PROTOCOL

try:
    from collections import UserDict as DictClass
except ImportError:
    from UserDict import DictMixin as DictClass

try:
    from queue import Queue
except ImportError:
    from Queue import Queue

logger = logging.getLogger(__name__)

def open(*args, **kwargs):
    """See documentation of the SqliteDict class."""
    return SqliteDict(*args, **kwargs)


def encode(obj):
    """Serialize an object using pickle to a binary format accepted by SQLite."""
    return sqlite3.Binary(dumps(obj, protocol=PICKLE_PROTOCOL))


def decode(obj):
    """Deserialize objects retrieved from SQLite."""
    return loads(bytes(obj))


class SqliteDict(DictClass):
    VALID_FLAGS = [
     'c', 'r', 'w', 'n']

    def __init__(self, filename=None, tablename='unnamed', flag='c', autocommit=False, journal_mode='DELETE', encode=encode, decode=decode):
        """
        Initialize a thread-safe sqlite-backed dictionary. The dictionary will
        be a table `tablename` in database file `filename`. A single file (=database)
        may contain multiple tables.

        If no `filename` is given, a random file in temp will be used (and deleted
        from temp once the dict is closed/deleted).

        If you enable `autocommit`, changes will be committed after each operation
        (more inefficient but safer). Otherwise, changes are committed on `self.commit()`,
        `self.clear()` and `self.close()`.

        Set `journal_mode` to 'OFF' if you're experiencing sqlite I/O problems
        or if you need performance and don't care about crash-consistency.

        The `flag` parameter. Exactly one of:
          'c': default mode, open for read/write, creating the db/table if necessary.
          'w': open for r/w, but drop `tablename` contents first (start with empty table)
          'r': open as read-only
          'n': create a new database (erasing any existing tables, not just `tablename`!).

        The `encode` and `decode` parameters are used to customize how the values
        are serialized and deserialized.
        The `encode` parameter must be a function that takes a single Python
        object and returns a serialized representation.
        The `decode` function must be a function that takes the serialized
        representation produced by `encode` and returns a deserialized Python
        object.
        The default is to use pickle.

        """
        self.in_temp = filename is None
        if self.in_temp:
            randpart = hex(random.randint(0, 16777215))[2:]
            filename = os.path.join(tempfile.gettempdir(), 'sqldict' + randpart)
        if flag not in SqliteDict.VALID_FLAGS:
            raise RuntimeError('Unrecognized flag: %s' % flag)
        self.flag = flag
        if flag == 'n':
            if os.path.exists(filename):
                os.remove(filename)
        dirname = os.path.dirname(filename)
        if dirname:
            if not os.path.exists(dirname):
                raise RuntimeError('Error! The directory does not exist, %s' % dirname)
        self.filename = filename
        if '"' in tablename:
            raise ValueError('Invalid tablename %r' % tablename)
        self.tablename = tablename
        self.autocommit = autocommit
        self.journal_mode = journal_mode
        self.encode = encode
        self.decode = decode
        logger.info('opening Sqlite table %r in %s' % (tablename, filename))
        MAKE_TABLE = 'CREATE TABLE IF NOT EXISTS "%s" (key TEXT PRIMARY KEY, value BLOB)' % self.tablename
        self.conn = self._new_conn()
        self.conn.execute(MAKE_TABLE)
        self.conn.commit()
        if flag == 'w':
            self.clear()
        return

    def _new_conn(self):
        return SqliteMultithread(self.filename, autocommit=self.autocommit, journal_mode=self.journal_mode)

    def __enter__(self):
        if not hasattr(self, 'conn') or self.conn is None:
            self.conn = self._new_conn()
        return self

    def __exit__(self, *exc_info):
        self.close()

    def __str__(self):
        return 'SqliteDict(%s)' % self.filename

    def __repr__(self):
        return str(self)

    def __len__(self):
        GET_LEN = 'SELECT COUNT(*) FROM "%s"' % self.tablename
        rows = self.conn.select_one(GET_LEN)[0]
        if rows is not None:
            return rows
        else:
            return 0

    def __bool__(self):
        GET_MAX = 'SELECT MAX(ROWID) FROM "%s"' % self.tablename
        m = self.conn.select_one(GET_MAX)[0]
        if m is not None:
            return True
        else:
            return False

    def iterkeys(self):
        GET_KEYS = 'SELECT key FROM "%s" ORDER BY rowid' % self.tablename
        for key in self.conn.select(GET_KEYS):
            yield key[0]

    def itervalues(self):
        GET_VALUES = 'SELECT value FROM "%s" ORDER BY rowid' % self.tablename
        for value in self.conn.select(GET_VALUES):
            yield self.decode(value[0])

    def iteritems(self):
        GET_ITEMS = 'SELECT key, value FROM "%s" ORDER BY rowid' % self.tablename
        for key, value in self.conn.select(GET_ITEMS):
            yield (
             key, self.decode(value))

    def keys(self):
        if major_version > 2:
            return self.iterkeys()
        return list(self.iterkeys())

    def values(self):
        if major_version > 2:
            return self.itervalues()
        return list(self.itervalues())

    def items(self):
        if major_version > 2:
            return self.iteritems()
        return list(self.iteritems())

    def __contains__(self, key):
        HAS_ITEM = 'SELECT 1 FROM "%s" WHERE key = ?' % self.tablename
        return self.conn.select_one(HAS_ITEM, (key,)) is not None

    def __getitem__(self, key):
        GET_ITEM = 'SELECT value FROM "%s" WHERE key = ?' % self.tablename
        item = self.conn.select_one(GET_ITEM, (key,))
        if item is None:
            raise KeyError(key)
        return self.decode(item[0])

    def __setitem__(self, key, value):
        if self.flag == 'r':
            raise RuntimeError('Refusing to write to read-only SqliteDict')
        ADD_ITEM = 'REPLACE INTO "%s" (key, value) VALUES (?,?)' % self.tablename
        self.conn.execute(ADD_ITEM, (key, self.encode(value)))

    def __delitem__(self, key):
        if self.flag == 'r':
            raise RuntimeError('Refusing to delete from read-only SqliteDict')
        if key not in self:
            raise KeyError(key)
        DEL_ITEM = 'DELETE FROM "%s" WHERE key = ?' % self.tablename
        self.conn.execute(DEL_ITEM, (key,))

    def update(self, items=(), **kwds):
        if self.flag == 'r':
            raise RuntimeError('Refusing to update read-only SqliteDict')
        try:
            items = items.items()
        except AttributeError:
            pass

        items = [ (k, self.encode(v)) for k, v in items ]
        UPDATE_ITEMS = 'REPLACE INTO "%s" (key, value) VALUES (?, ?)' % self.tablename
        self.conn.executemany(UPDATE_ITEMS, items)
        if kwds:
            self.update(kwds)

    def __iter__(self):
        return self.iterkeys()

    def clear(self):
        if self.flag == 'r':
            raise RuntimeError('Refusing to clear read-only SqliteDict')
        CLEAR_ALL = 'DELETE FROM "%s";' % self.tablename
        self.conn.commit()
        self.conn.execute(CLEAR_ALL)
        self.conn.commit()

    def commit(self, blocking=True):
        """
        Persist all data to disk.

        When `blocking` is False, the commit command is queued, but the data is
        not guaranteed persisted (default implication when autocommit=True).
        """
        if self.conn is not None:
            self.conn.commit(blocking)
        return

    sync = commit

    def close(self, do_log=True, force=False):
        if do_log:
            logger.debug('closing %s' % self)
        if hasattr(self, 'conn') and self.conn is not None:
            if self.conn.autocommit and not force:
                self.conn.commit(blocking=True)
            self.conn.close(force=force)
            self.conn = None
        if self.in_temp:
            try:
                os.remove(self.filename)
            except:
                pass

        return

    def terminate(self):
        """Delete the underlying database file. Use with care."""
        if self.flag == 'r':
            raise RuntimeError('Refusing to terminate read-only SqliteDict')
        self.close()
        if self.filename == ':memory:':
            return
        logger.info('deleting %s' % self.filename)
        try:
            if os.path.isfile(self.filename):
                os.remove(self.filename)
        except (OSError, IOError):
            logger.exception('failed to delete %s' % self.filename)

    def __del__(self):
        try:
            self.close(do_log=False, force=True)
        except Exception:
            pass


if major_version == 2:
    SqliteDict.__nonzero__ = SqliteDict.__bool__
    del SqliteDict.__bool__

class SqliteMultithread(Thread):
    """
    Wrap sqlite connection in a way that allows concurrent requests from multiple threads.

    This is done by internally queueing the requests and processing them sequentially
    in a separate thread (in the same order they arrived).

    """

    def __init__(self, filename, autocommit, journal_mode):
        super(SqliteMultithread, self).__init__()
        self.filename = filename
        self.autocommit = autocommit
        self.journal_mode = journal_mode
        self.reqs = Queue()
        self.setDaemon(True)
        self.exception = None
        self.log = logging.getLogger('sqlitedict.SqliteMultithread')
        self.start()
        return

    def run(self):
        if self.autocommit:
            conn = sqlite3.connect(self.filename, isolation_level=None, check_same_thread=False)
        else:
            conn = sqlite3.connect(self.filename, check_same_thread=False)
        conn.execute('PRAGMA journal_mode = %s' % self.journal_mode)
        conn.text_factory = str
        cursor = conn.cursor()
        conn.commit()
        cursor.execute('PRAGMA synchronous=OFF')
        res = None
        while True:
            req, arg, res, outer_stack = self.reqs.get()
            if req == '--close--':
                assert res, ('--close-- without return queue', res)
                break
            elif req == '--commit--':
                conn.commit()
                if res:
                    res.put('--no more--')
            else:
                try:
                    cursor.execute(req, arg)
                except Exception as err:
                    self.exception = e_type, e_value, e_tb = sys.exc_info()
                    inner_stack = traceback.extract_stack()
                    self.log.error('Inner exception:')
                    for item in traceback.format_list(inner_stack):
                        self.log.error(item)

                    self.log.error('')
                    for item in traceback.format_exception_only(e_type, e_value):
                        self.log.error(item)

                    self.log.error('')
                    self.log.error('Outer stack:')
                    for item in traceback.format_list(outer_stack):
                        self.log.error(item)

                    self.log.error('Exception will be re-raised at next call.')

                if res:
                    for rec in cursor:
                        res.put(rec)

                    res.put('--no more--')
                if self.autocommit:
                    conn.commit()

        self.log.debug('received: %s, send: --no more--', req)
        conn.close()
        res.put('--no more--')
        return

    def check_raise_error(self):
        """
        Check for and raise exception for any previous sqlite query.

        For the `execute*` family of method calls, such calls are non-blocking and any
        exception raised in the thread cannot be handled by the calling Thread (usually
        MainThread).  This method is called on `close`, and prior to any subsequent
        calls to the `execute*` methods to check for and raise an exception in a
        previous call to the MainThread.
        """
        if self.exception:
            e_type, e_value, e_tb = self.exception
            self.exception = None
            self.log.error('An exception occurred from a previous statement, view the logging namespace "sqlitedict" for outer stack.')
            reraise(e_type, e_value, e_tb)
        return

    def execute(self, req, arg=None, res=None):
        """
        `execute` calls are non-blocking: just queue up the request and return immediately.
        """
        self.check_raise_error()
        stack = traceback.extract_stack()[:-1]
        self.reqs.put((req, arg or tuple(), res, stack))

    def executemany(self, req, items):
        for item in items:
            self.execute(req, item)

        self.check_raise_error()

    def select(self, req, arg=None):
        """
        Unlike sqlite's native select, this select doesn't handle iteration efficiently.

        The result of `select` starts filling up with values as soon as the
        request is dequeued, and although you can iterate over the result normally
        (`for res in self.select(): ...`), the entire result will be in memory.
        """
        res = Queue()
        self.execute(req, arg, res)
        while True:
            rec = res.get()
            self.check_raise_error()
            if rec == '--no more--':
                break
            yield rec

    def select_one(self, req, arg=None):
        """Return only the first row of the SELECT, or None if there are no matching rows."""
        try:
            return next(iter(self.select(req, arg)))
        except StopIteration:
            return

        return

    def commit(self, blocking=True):
        if blocking:
            self.select_one('--commit--')
        else:
            self.execute('--commit--')

    def close(self, force=False):
        if force:
            self.reqs.put(('--close--', None, Queue(), None))
        else:
            self.select_one('--close--')
            self.join()
        return