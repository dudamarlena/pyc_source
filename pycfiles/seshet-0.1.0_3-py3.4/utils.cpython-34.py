# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/seshet/utils.py
# Compiled at: 2015-07-15 10:55:27
# Size of source mod 2**32: 10679 bytes
"""Various utility classes used by the bot and command modules.

`Storage` is copied from gluon.storage, part of the web2py framework,
    Copyrighted by Massimo Di Pierro <mdipierro@cs.depaul.edu>,
    License: LGPLv3 (http://www.gnu.org/licenses/lgpl.html)
"""
import random, inspect, pickle
from pydal import Field

class Storage(dict):
    __doc__ = "A Storage object is like a dictionary except `obj.foo` can be used\n    in addition to `obj['foo']`, and setting obj.foo = None deletes item foo.\n\n    Example:\n\n        >>> o = Storage(a=1)\n        >>> print o.a\n        1\n\n        >>> o['a']\n        1\n\n        >>> o.a = 2\n        >>> print o['a']\n        2\n\n        >>> del o.a\n        >>> print o.a\n        None\n\n    "
    __slots__ = ()
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__
    __getitem__ = dict.get
    __getattr__ = dict.get
    __getnewargs__ = lambda self: getattr(dict, self).__getnewargs__(self)
    __repr__ = lambda self: '<Storage %s>' % dict.__repr__(self)
    __getstate__ = lambda self: None
    __copy__ = lambda self: Storage(self)

    def getlist(self, key):
        """Returns a Storage value as a list.

        If the value is a list it will be returned as-is.
        If object is None, an empty list will be returned.
        Otherwise, `[value]` will be returned.

        Example output for a query string of `?x=abc&y=abc&y=def`::

            >>> request = Storage()
            >>> request.vars = Storage()
            >>> request.vars.x = 'abc'
            >>> request.vars.y = ['abc', 'def']
            >>> request.vars.getlist('x')
            ['abc']
            >>> request.vars.getlist('y')
            ['abc', 'def']
            >>> request.vars.getlist('z')
            []

        """
        value = self.get(key, [])
        if value is None or isinstance(value, (list, tuple)):
            return value
        else:
            return [
             value]

    def getfirst(self, key, default=None):
        """Returns the first value of a list or the value itself when given a
        `request.vars` style key.

        If the value is a list, its first item will be returned;
        otherwise, the value will be returned as-is.

        Example output for a query string of `?x=abc&y=abc&y=def`::

            >>> request = Storage()
            >>> request.vars = Storage()
            >>> request.vars.x = 'abc'
            >>> request.vars.y = ['abc', 'def']
            >>> request.vars.getfirst('x')
            'abc'
            >>> request.vars.getfirst('y')
            'abc'
            >>> request.vars.getfirst('z')

        """
        values = self.getlist(key)
        if values:
            return values[0]
        return default

    def getlast(self, key, default=None):
        """Returns the last value of a list or value itself when given a
        `request.vars` style key.

        If the value is a list, the last item will be returned;
        otherwise, the value will be returned as-is.

        Simulated output with a query string of `?x=abc&y=abc&y=def`::

            >>> request = Storage()
            >>> request.vars = Storage()
            >>> request.vars.x = 'abc'
            >>> request.vars.y = ['abc', 'def']
            >>> request.vars.getlast('x')
            'abc'
            >>> request.vars.getlast('y')
            'def'
            >>> request.vars.getlast('z')

        """
        values = self.getlist(key)
        if values:
            return values[(-1)]
        return default


class KVStore:
    __doc__ = "Create a key/value store in the bot's database for each\n    command module to use for persistent storage. Can be accessed\n    either like a class:\n    \n        >>> store = KVStore(db)\n        >>> store.foo = 'bar'\n        >>> store.foo\n        'bar'\n        \n    Or like a dict:\n    \n        >>> store[spam] = 'eggs'\n        >>> store[spam]\n        'eggs'\n        \n    The KVStore object uses `inspect` to determine which module\n    the object is being accessed from and will automatically create\n    a database table as needed or determine which one to use if it\n    already exists, so that each module the object is used from has\n    its own namespace.\n    \n    KVStore has most of the same interfaces as an ordinary `dict`, but\n    is not a subclass of `dict` or `collections.UserDict` because\n    so many functions had to be completely rewritten to work with\n    KVStore's database model.\n    "

    def __init__(self, db):
        if 'modules' not in db:
            db.define_table('modules', Field('name'))
        for m in db().select(db.modules.ALL):
            tbl_name = 'kv_' + m.name
            if tbl_name not in db:
                db.define_table(tbl_name, Field('k', 'string', unique=True), Field('v', 'text'))
                continue

        self._db = db

    def __getattr__(self, k):
        if k.startswith('_'):
            return self.__dict__[k]
        db = self._db
        tbl = self._get_calling_module()
        tbl_name = 'kv_' + tbl if table is not None else None
        if tbl is None or tbl_name not in db:
            return
        r = db(db[tbl_name].k == k)
        if r.isempty():
            return
        r = r.select().first()
        return pickle.loads(r.v.encode(errors='ignore'))

    def __setattr__(self, k, v):
        if k.startswith('_'):
            self.__dict__[k] = v
            return
        if k in self.__dict__:
            raise AttributeError('Name already in use: %s' % k)
        db = self._db
        if v is not None:
            v = pickle.dumps(v).decode(errors='ignore')
        tbl = self._get_calling_module()
        tbl_name = 'kv_' + tbl if tbl is not None else None
        if tbl is None or tbl_name not in db:
            if v is not None:
                self._register_module(tbl)
                db[tbl_name].insert(k=k, v=repr(v))
            else:
                return
        else:
            if v is not None:
                db[tbl_name].update_or_insert(db[tbl_name].k == k, k=k, v=v)
            else:
                db(db[tbl_name].k == k).delete()
        db.commit()
        self._db = db

    def __delattr__(self, k):
        self.__setattr__(k, None)

    def __getitem__(self, k):
        return self.__getattr__(k)

    def __setitem__(self, k, v):
        self.__setattr__(k, v)

    def __delitem__(self, k):
        self.__setattr__(k, None)

    def _register_module(self, name):
        db = self._db
        tbl_name = 'kv_' + name
        if db(db.modules.name == name).isempty():
            db.modules.insert(name=name)
            db.commit()
        if tbl_name not in db:
            db.define_table(tbl_name, Field('k', 'string', unique=True), Field('v', 'text'))
        self._db = db

    def _get_calling_module(self):
        curfrm = inspect.currentframe()
        for f in inspect.getouterframes(curfrm)[1:]:
            if self.__module__.split('.')[(-1)] not in f[1]:
                calling_file = f[1]
                break

        caller_mod = inspect.getmodulename(calling_file)
        db = self._db
        mod = db(db.modules.name == caller_mod)
        if mod.isempty():
            return
        else:
            return caller_mod

    def keys(self):
        db = self._db
        tbl = self._get_calling_module()
        tbl_name = 'kv_' + tbl if tbl is not None else None
        if tbl is None or tbl_name not in db:
            return []
        all_items = db().select(db[tbl_name].ALL)
        all_keys = [r.k for r in all_items]
        return all_keys

    def values(self):
        all_keys = self.keys()
        all_vals = list()
        for k in all_keys:
            all_vals.append(self[k])

        return all_vals

    def update(self, other):
        for k, v in other.items():
            self[k] = v

    def items(self):
        return zip(self.keys(), self.values())

    def iterkeys(self):
        return iter(self.keys())

    def itervalues(self):
        return iter(self.values())

    def iteritems(self):
        return iter(self.items())

    def __iter__(self):
        return iter(self.keys())

    def __contains__(self, k):
        if self[k] is not None:
            return True
        else:
            return False

    def __copy__(self):
        """Return a dict representing the current table"""
        d = dict()
        d.update(self.items())
        return d

    def copy(self):
        """Return a dict representing the current table"""
        return self.__copy__()

    def pop(self, k):
        v = self[k]
        self[k] = None
        return v

    def popitem(self):
        """Unlike `dict.popitem()`, this is actually random"""
        all_items = self.items()
        removed_item = random.choice(all_items)
        self[removed_item[0]] = None
        return removed_item

    def setdefault(self, k, v=None):
        existing_v = self[k]
        if existing_v is None:
            self[k] = v
            return v
        return existing_v

    def has_key(self, k):
        return k in self

    def get(self, k, v=None):
        existing_v = self[k]
        if existing_v is None:
            return v
        else:
            return existing_v

    def clear(self):
        for k in self.keys():
            self[k] = None