# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pylinkirc/structures.py
# Compiled at: 2020-04-11 03:31:40
# Size of source mod 2**32: 9762 bytes
"""
structures.py - PyLink data structures module.

This module contains custom data structures that may be useful in various situations.
"""
import collections, collections.abc, json, os, pickle, string, threading
from copy import copy, deepcopy
from . import conf
from .log import log
_BLACKLISTED_COPY_TYPES = []

class KeyedDefaultdict(collections.defaultdict):
    __doc__ = '\n    Subclass of defaultdict allowing the key to be passed to the default factory.\n    '

    def __missing__(self, key):
        if self.default_factory is None:
            super().__missing__(self, key)
        else:
            value = self[key] = self.default_factory(key)
            return value


class CopyWrapper:
    __doc__ = '\n    Base container class implementing copy methods.\n    '

    def copy(self):
        """Returns a shallow copy of this object instance."""
        return copy(self)

    def __deepcopy__(self, memo):
        """Returns a deep copy of the channel object."""
        newobj = copy(self)
        for attr, val in self.__dict__.items():
            if not isinstance(val, tuple(_BLACKLISTED_COPY_TYPES)):
                setattr(newobj, attr, deepcopy(val))

        memo[id(self)] = newobj
        return newobj

    def deepcopy(self):
        """Returns a deep copy of this object instance."""
        return deepcopy(self)


class CaseInsensitiveFixedSet(collections.abc.Set, CopyWrapper):
    __doc__ = '\n    Implements a fixed set storing items case-insensitively.\n    '

    def __init__(self, *, data=None):
        if data is not None:
            self._data = data
        else:
            self._data = set()

    @staticmethod
    def _keymangle(key):
        """Converts the given key to lowercase."""
        if isinstance(key, str):
            return key.lower()
        else:
            return key

    @classmethod
    def _from_iterable(cls, it):
        """Returns a new iterable instance given the data in 'it'."""
        return cls(data=it)

    def __repr__(self):
        return '%s(%s)' % (self.__class__.__name__, self._data)

    def __iter__(self):
        return iter(self._data)

    def __len__(self):
        return len(self._data)

    def __contains__(self, key):
        return self._data.__contains__(self._keymangle(key))

    def __copy__(self):
        return self.__class__(data=(self._data.copy()))


class CaseInsensitiveDict(collections.abc.MutableMapping, CaseInsensitiveFixedSet):
    __doc__ = '\n    A dictionary storing items case insensitively.\n    '

    def __init__(self, *, data=None):
        if data is not None:
            self._data = data
        else:
            self._data = {}

    def __getitem__(self, key):
        key = self._keymangle(key)
        return self._data[key]

    def __setitem__(self, key, value):
        self._data[self._keymangle(key)] = value

    def __delitem__(self, key):
        del self._data[self._keymangle(key)]


class IRCCaseInsensitiveDict(CaseInsensitiveDict):
    __doc__ = '\n    A dictionary storing items case insensitively, using IRC case mappings.\n    '

    def __init__(self, irc, *, data=None):
        super().__init__(data=data)
        self._irc = irc

    def _keymangle(self, key):
        """Converts the given key to lowercase."""
        if isinstance(key, str):
            return self._irc.to_lower(key)
        else:
            return key

    def _from_iterable(self, it):
        """Returns a new iterable instance given the data in 'it'."""
        return self.__class__((self._irc), data=it)

    def __copy__(self):
        return self.__class__((self._irc), data=(self._data.copy()))


class CaseInsensitiveSet(collections.abc.MutableSet, CaseInsensitiveFixedSet):
    __doc__ = '\n    A mutable set storing items case insensitively.\n    '

    def add(self, key):
        self._data.add(self._keymangle(key))

    def discard(self, key):
        self._data.discard(self._keymangle(key))


class IRCCaseInsensitiveSet(CaseInsensitiveSet):
    __doc__ = '\n    A set storing items case insensitively, using IRC case mappings.\n    '

    def __init__(self, irc, *, data=None):
        super().__init__(data=data)
        self._irc = irc

    def _keymangle(self, key):
        """Converts the given key to lowercase."""
        if isinstance(key, str):
            return self._irc.to_lower(key)
        else:
            return key

    def _from_iterable(self, it):
        """Returns a new iterable instance given the data in 'it'."""
        return self.__class__((self._irc), data=it)

    def __copy__(self):
        return self.__class__((self._irc), data=(self._data.copy()))


class CamelCaseToSnakeCase:
    __doc__ = '\n    Class which automatically converts missing attributes from camel case to snake case.\n    '

    def __getattr__(self, attr):
        """
        Attribute fetching fallback function which normalizes camel case attributes to snake case.
        """
        assert isinstance(attr, str), 'Requested attribute %r is not a string!' % attr
        normalized_attr = ''
        for char in attr:
            if char in string.ascii_uppercase:
                char = '_' + char.lower()
            normalized_attr += char

        classname = self.__class__.__name__
        if normalized_attr == attr:
            raise AttributeError('%s object has no attribute with normalized name %r' % (classname, attr))
        target = getattr(self, normalized_attr)
        log.warning('%s.%s is deprecated, considering migrating to %s.%s!', classname, attr, classname, normalized_attr)
        return target


class DataStore:
    __doc__ = '\n    Generic database class. Plugins should use a subclass of this such as JSONDataStore or\n    PickleDataStore.\n    '

    def __init__(self, name, filename, save_frequency=None, default_db=None):
        self.name = name
        self.filename = filename
        self.tmp_filename = filename + '.tmp'
        log.debug('(DataStore:%s) using implementation %s', self.name, self.__class__.__name__)
        log.debug('(DataStore:%s) database path set to %s', self.name, self.filename)
        self.save_frequency = save_frequency or conf.conf['pylink'].get('save_delay', 300)
        log.debug('(DataStore:%s) saving every %s seconds', self.name, self.save_frequency)
        if default_db is not None:
            self.store = default_db
        else:
            self.store = {}
        self.store_lock = threading.Lock()
        self.exportdb_timer = None
        self.load()
        if self.save_frequency > 0:
            self.save_callback(starting=True)

    def load(self):
        """
        DataStore load stub. Database implementations should subclass DataStore
        and implement this.
        """
        raise NotImplementedError

    def save_callback(self, starting=False):
        """Start the DB save loop."""
        if not starting:
            self.save()
        self.exportdb_timer = threading.Timer(self.save_frequency, self.save_callback)
        self.exportdb_timer.name = 'DataStore {} save_callback loop'.format(self.name)
        self.exportdb_timer.start()

    def save(self):
        """
        DataStore save stub. Database implementations should subclass DataStore
        and implement this.
        """
        raise NotImplementedError

    def die(self):
        """
        Saves the database and stops any save loops.
        """
        if self.exportdb_timer:
            self.exportdb_timer.cancel()
        self.save()


class JSONDataStore(DataStore):

    def load(self):
        """Loads the database given via JSON."""
        with self.store_lock:
            try:
                with open(self.filename, 'r') as (f):
                    self.store.clear()
                    self.store.update(json.load(f))
            except (ValueError, IOError, OSError):
                log.info('(DataStore:%s) failed to load database %s; creating a new one in memory', self.name, self.filename)

    def save(self):
        """Saves the database given via JSON."""
        with self.store_lock:
            with open(self.tmp_filename, 'w') as (f):
                json.dump((self.store), f, indent=4)
                os.rename(self.tmp_filename, self.filename)


class PickleDataStore(DataStore):

    def load(self):
        """Loads the database given via pickle."""
        with self.store_lock:
            try:
                with open(self.filename, 'rb') as (f):
                    self.store.clear()
                    self.store.update(pickle.load(f))
            except (ValueError, IOError, OSError):
                log.info('(DataStore:%s) failed to load database %s; creating a new one in memory', self.name, self.filename)

    def save(self):
        """Saves the database given via pickle."""
        with self.store_lock:
            with open(self.tmp_filename, 'wb') as (f):
                pickle.dump((self.store), f, protocol=4)
                os.rename(self.tmp_filename, self.filename)