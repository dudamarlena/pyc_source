# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib64/python3.6/site-packages/ioflo/base/storing.py
# Compiled at: 2017-12-17 08:35:26
# Size of source mod 2**32: 38088 bytes
"""storing.py datashare module

"""
import time, struct, re, copy
from collections import deque
import datetime
from ..aid.sixing import *
from .globaling import INDENT_ADD, REO_IdentPub
from ..aid.odicting import odict
from . import excepting
from . import registering
from ..aid.aiding import nameToPath
from ..aid.consoling import getConsole
console = getConsole()

class Node(odict):
    __doc__ = '\n    Special odict with name property to hold the pathname to the node\n    '
    __slots__ = ('_name', )

    def __init__(self, *pa, **kwa):
        (super(Node, self).__init__)(*pa, **kwa)
        self._name = ''

    @property
    def name(self):
        """Get name property. Pathname to node."""
        return self._name

    @name.setter
    def name(self, name):
        """Set name property """
        self._name = name

    def byName(self, name):
        """ Sets name and returns self.
            Enables setting name as part of method chaining.
        """
        self.name = name
        return self


class Store(registering.Registrar):
    __doc__ = '\n    global data store to be shared amoungst all taskers.\n\n    Each object has the concept of ownership in the datashare.\n\n    inherited instance attributes:\n        .name  = unique data store name\n\n    instance attributes:\n        .stamp = global time stamp for store\n        .house = reference to house owning this store\n        .shares = dictionary of shared data store items\n        .metaShr = share for meta data\n        .realTimeShr = share whose value is realtime time when .stamp is updated\n        .timeShr = share whose value is copy of stamp when .stamp is updated\n\n    '
    Counter = 0
    Names = {}

    def __init__(self, stamp=None, house=None, **kwa):
        """Initialize instance

           *pa and **kwa allow multiple inheritance

        """
        (super(Store, self).__init__)(**kwa)
        try:
            stamp = float(stamp)
        except TypeError:
            stamp = None

        self.stamp = stamp
        self.house = house
        self.shares = Node().byName('')
        self.metaShr = self.createNode('.meta')
        self.timeShr = self.create('.time').update(value=(self.stamp or 0.0))
        rt = time.time()
        self.realTimeShr = self.create('.realtime').update(value=rt)
        dt = datetime.datetime.fromtimestamp(rt)
        self.dateTimeShr = self.create('.datetime').update([('iso', dt.isoformat()),
         (
          'dt', dt),
         (
          'year', dt.year),
         (
          'month', dt.month),
         (
          'day', dt.day),
         (
          'hour', dt.hour),
         (
          'minute', dt.minute),
         (
          'second', dt.second),
         (
          'micro', dt.microsecond)])

    def changeStamp(self, stamp):
        """change time stamp for this store """
        try:
            self.stamp = float(stamp)
            self.timeShr.update(value=(self.stamp))
            rt = time.time()
            self.realTimeShr.update(value=rt)
            dt = datetime.datetime.fromtimestamp(rt)
            self.dateTimeShr.update([('iso', dt.isoformat()),
             (
              'dt', dt),
             (
              'year', dt.year),
             (
              'month', dt.month),
             (
              'day', dt.day),
             (
              'hour', dt.hour),
             (
              'minute', dt.minute),
             (
              'second', dt.second),
             (
              'micro', dt.microsecond)])
        except TypeError:
            self.stamp = None
            console.verbose("Error: Store {0}, Invalid stamp '{1}'\n".format(self.name, self.stamp))
            raise

    def advanceStamp(self, delta):
        """change time stamp for this store """
        try:
            self.stamp += delta
            self.timeShr.update(value=(self.stamp))
            rt = time.time()
            self.realTimeShr.update(value=rt)
            dt = datetime.datetime.fromtimestamp(rt)
            self.dateTimeShr.update([('iso', dt.isoformat()),
             (
              'dt', dt),
             (
              'year', dt.year),
             (
              'month', dt.month),
             (
              'day', dt.day),
             (
              'hour', dt.hour),
             (
              'minute', dt.minute),
             (
              'second', dt.second),
             (
              'micro', dt.microsecond)])
        except TypeError:
            console.verbose("Error: Store {0}, Can't advance stamp={1} by delta={2}\n".format(self.name, self.stamp, delta))
            raise

    def fetch(self, name):
        """Retrieve from .shares a  node (or special case share)  by its name
           where name is path through hierarchy (may be partial)
           return node or share or if not exist return None

           User of this method needs to test result to determine if node or share

           isinstance(nos, Share)

           since .shares is hierachical dictionary of dictionaries
           need to traverse the hirearchy
        """
        try:
            levels = name.strip('.').split('.')
            nos = self.shares
            for level in levels:
                nos = nos[level]

        except KeyError:
            return
        else:
            return nos

    def fetchShare(self, name):
        """Retrieve from .shares a  share by its name
           return share or if not exist or if not a share (node by same name then
              return None

           since .shares is hierachical dictionary of dictionaries
           need to traverse the hirearchy
        """
        try:
            levels = name.strip('.').split('.')
            nos = self.shares
            for level in levels:
                nos = nos[level]

        except KeyError:
            return
        else:
            if not isinstance(nos, Share):
                return
            else:
                return nos

    def fetchNode(self, name):
        """Retrieve from .shares a  node by its name from .shares
           return node or if not exist or if not a node (share by same name then
              return None

           since .shares is hierachical dictionary of dictionaries
           need to traverse the hirearchy
        """
        try:
            levels = name.strip('.').split('.')
            nos = self.shares
            for level in levels:
                nos = nos[level]

        except KeyError:
            return
        else:
            if isinstance(nos, Share):
                return
            else:
                return nos

    def add(self, share):
        """Add share to store and change shares .store to self
           Creates node hierarchy from name as needed
           If share already exists with same name then raises exception.
           Should use .change instead is want to change path of existing share
           This is to prevent inadvertant adding of shares that clobber node hierarchy

           for a single item list
              the slice [0:-1] is empty
              the slice [-1] = [0] is the single item
        """
        if not isinstance(share, Share):
            raise ValueError('Not Share %s' % share)
        else:
            if not share.name:
                raise ValueError('Empty Share Name %s' % share.name)
            levels = share.name.strip('.').split('.')
            node = self.shares
            depth = 0
            for level in levels[0:-1]:
                if not level:
                    raise ValueError("Empty level in '%s'" % share.name)
                depth += 1
                node = node.setdefault(level, Node().byName('.'.join(levels[:depth])))
                if isinstance(node, Share):
                    raise ValueError("Level  '%s' in '%s' is preexisting share" % (level, share.name))

            tail = levels[(-1)]
            if tail in node:
                raise ValueError("Tail '%s' of '%s' is preexisting level" % (tail, share.name))
        node[tail] = share
        share.changeStore(self)
        console.profuse('{0}Added share {1} to store {2}\n'.format(INDENT_ADD, share.name, self.name))
        return share

    def addNode(self, name):
        """Add node with pathname name to store
           Creates node hierarchy from name as needed
           If node already exists with same name then raises exception.
           This is to prevent inadvertant adding of node that clobber node/share hierarchy

           for a single item list
              the slice [0:-1] is empty
              the slice [-1] = [0] is the single item
        """
        levels = name.strip('.').split('.')
        node = self.shares
        depth = 0
        for level in levels:
            if not level:
                raise ValueError("Empty level in '%s'" % name)
            depth += 1
            node = node.setdefault(level, Node().byName('.'.join(levels[:depth])))
            if isinstance(node, Share):
                raise ValueError("Level  '%s' in '%s' is preexisting share" % (level, node.name))

        console.profuse('{0}Added node {1} to {2}\n'.format(INDENT_ADD, name, self.name))
        return node

    def change(self, share):
        """change existing share with same name in store to share and change share's .store to self
           if share and node hierachy do not exist then raises exception
           this is to make it harder to inadvertantly mess up node hierarchy
        """
        if not isinstance(share, Share):
            raise ValueError('Not share %s' % share)
        levels = share.name.strip('.').split('.')
        node = self.shares
        for level in levels[0:-1]:
            if not level:
                raise ValueError("Empty level in '%s'" % share.name)
            else:
                if level in node:
                    node = node[level]
                    if isinstance(node, Share):
                        raise ValueError("Level  '%s' in '%s' is preexisting share" % (level, share.name))
                else:
                    raise ValueError("No share with name '%s'" % share.name)

        tail = levels[(-1)]
        if tail not in node or not isinstance(node[tail], Share):
            raise ValueError("No share with name '%s'" % share.name)
        node[tail] = share
        share.changeStore(self)
        return share

    def create(self, name):
        """Retrieve share with name if it exits
           otherwise create a share with  name
              and add to store
        """
        share = self.fetchShare(name)
        if share is not None:
            return share
        else:
            return self.add(Share(name=(name.strip('.'))))

    def createNode(self, name):
        """Retrieve node with name if it exits
           otherwise create a node with  name and add to store
        """
        node = self.fetchNode(name)
        if node is not None:
            return node
        else:
            return self.addNode(name=name)

    def expose(self, valued=False):
        """
        If valued then display values for leaf share items
        """
        console.terse('Store name= {0}, stamp= {1}\n'.format(self.name, self.stamp))
        console.terse('Nodes & Shares:\n')
        Store.ShowNode((self.shares), indent=0, valued=valued)

    @staticmethod
    def ShowNode(node, indent=0, valued=False):
        """
        node is node to display
        indent is number of spaces to indent
        If valued then display values for leaf share items
        """
        if isinstance(node, dict):
            for key, value in node.items():
                msg = ''
                for i in range(indent):
                    msg += '  '

                msg += '.{0} '.format(key)
                console.terse('{0}\n'.format(msg))
                Store.ShowNode(value, indent=(indent + 1), valued=valued)

        else:
            msg = ''
            offset = ''
            for i in range(indent):
                offset += '  '

            msg += offset
        if valued:
            for key, val in node.items():
                msg += '{0}={1} '.format(key, val)

            if node.deck:
                msg += '\n{0}deck={1}'.format(offset, list(node.deck))
            console.terse('{0}\n'.format(msg))
        else:
            for key in node.keys():
                msg += '{0} '.format(key)

            if node.deck:
                msg += '\n{0}deck'.format(offset)
            console.terse('{0}\n'.format(msg))


class Mark(object):
    __doc__ = ' Supports the NeedUpdate, NeedChange and Marker Actor\n        NeedUpdate checks if associated share is update while in associated frame\n        NeedChange checks if associated share data is changed while in associated frame\n\n\n        stamp = last stamp of associated share\n        data = copy of data of associated share\n\n    '
    __slots__ = ('stamp', 'data', 'used')

    def __init__(self, *pa, **kwa):
        (super(Mark, self).__init__)(*pa, **kwa)
        self.stamp = None
        self.data = None
        self.used = None


class Share(object):
    __doc__ = "\n    Shared item in data store\n\n    so it functions somewhat like a dictionary defines:\n    __setitem__\n    __getitem__\n    __delitem__\n    __contains__\n    __iter__\n    __len__\n    clear()\n    items()\n    iteritems()\n    iterkeys()\n    itervalues()\n    keys()\n    values()\n\n    instance attributes:\n        .name = holds unique store path entry name of share '.' notation\n        .store = data store holding share\n        .stamp = time stamp of this share\n        .deck = Deck instance for this share\n\n        ._owner used by owner property\n        ._data used by data property and also by private accessor methods\n        ._truth used by truth property\n        ._unit used by unit property\n\n\n    properties are used so that time stamps etc are updated properly for logging\n\n    properties (properites are stored in class):\n        .owner property holds a reference to owner of share (writer)\n        .data property holds data record\n            one time stamp applies to the whole data structure\n        .value property manages default single field value in data\n        .truth property holds the confidence of the value/data. may be None, True, False, [0.0, 1.0]\n            truth should not be updated unless value/data is, they are coupled\n            thus log if changed on truth also uses last value\n        .unit property hold units for fields\n\n    "

    def __init__(self, name='', store=None, value=None, data=None, truth=None, stamp=None, unit=None, owner=None, deck=None):
        """
        Initialize instance

        Parameters:
           name = path name of share in store if created by store
           store = shared data store
           value = value of data field 'value' if any
           data = dictionary (preferable ordered) of data fields and values
           truth = truth for this share
           stamp = time stamp for this share
           unit = measurement units for this share dict (preferably ordered) of fields and values
           owner = owner framework for this share
        """
        self._data = Data()
        self._truth = None
        self._unit = None
        self._owner = None
        self.stamp = None
        self.deck = Deck()
        if not isinstance(name, str):
            name = ''
        self.name = name
        self.changeStore(store=store)
        if value is not None:
            self.value = value
        if data is not None:
            (self.change)(**data)
        if truth is not None:
            self.truth = truth
        if stamp is not None:
            try:
                stamp = float(stamp)
                self.stamp = stamp
            except TypeError:
                console.terse('Error: Share {0} bad initializer stamp= {1}\n'.format(self.name, stamp))

        if unit is not None:
            (self.changUnit)(**unit)
        if owner is not None:
            self.owner = owner
        if deck is not None:
            self.deck.extend(deck)
        self.marks = odict()

    def __contains__(self, key):
        """       """
        return hasattr(self._data, key)

    def __delitem__(self, key):
        """       """
        try:
            delattr(self._data, key)
        except AttributeError:
            raise KeyError("%s object has no key '%s'" % (self.__class__.__name__, key))

    def __getitem__(self, key):
        """    """
        try:
            return getattr(self._data, key)
        except AttributeError:
            raise KeyError("%s object has no key '%s'" % (self.__class__.__name__, key))

    def __setitem__(self, key, value):
        """          """
        try:
            setattr(self._data, key, value)
        except AttributeError:
            raise KeyError("%s invalid key '%s'" % (self.__class__.__name__, key))

    def __iter__(self):
        """      """
        for key in self.keys():
            yield key

    def __len__(self):
        """    """
        return len(self._data.__dict__)

    def __repr__(self):
        """    """
        itemreprs = repr(self._data)
        deckreprs = repr(self.deck)
        return 'Share(name={0}, data={1}, deck={2})'.format(self.name, itemreprs, deckreprs)

    def clear(self):
        """   """
        self._data.__dict__.clear()

    def copy(self):
        """
        Make a shallow copy of ._data.__dict__
        """
        return self._data.__dict__.copy()

    def get(self, key, default=None):
        """D.get(k,d)"""
        if key in self:
            return self[key]
        else:
            return default

    def has_key(self, key):
        """  """
        return key in self

    def insert(self, index, key, item):
        """Insert key:item at index."""
        self._data.__dict__.insert(index, key, item)

    def items(self):
        """   """
        return self._data.__dict__.items()

    def iterkeys(self):
        """   """
        return iter(self)

    def iteritems(self):
        """   """
        return ((key, self[key]) for key in self.keys())

    def itervalues(self):
        """    """
        return (self[key] for key in self.keys())

    def keys(self):
        """   """
        return self._data.__dict__.keys()

    def values(self):
        """  """
        return [self[key] for key in self.keys()]

    def pop(self, key, *default):
        """
        Remove key and the associated item and return the associated value
        If key not found return default if given otherwise raise KeyError
        """
        value = (self._data.__dict__.pop)(key, *default)
        return value

    def popitem(self):
        """
        Remove and return last item (key, value) duple from ._data
        If ._data is empty raise KeyError
        """
        return self._data.__dict__.popitem()

    def setdefault(self, key, default=None):
        """
        If key in ._data, return value at key
        Otherwise set value at key to default and return default
        """
        value = self._data.__dict__.setdefault(key, default)
        return value

    def sift(self, fields=None):
        """
        Return odict of items keyed by field name strings provided in optional
        fields sequence in that order with each value given by the associated
        item in ._data
        If fields is not provided then return odict copy of ._data with all
        the fields
        Raises AttributeError if no entry in ._data for a given field name
        """
        return self._data._sift(fields=fields)

    def reorder(self, other):
        """
        Reorder values in ._dict based on the other odict.
        Raise ValueError if other is not an odict
        """
        if not isinstance(other, odict):
            raise ValueError('other must be an odict')
        if other is self:
            pass
        dict.update(self, other)
        keys = self._keys
        for key in other:
            if key in keys:
                keys.remove(key)
            keys.append(key)

    def changeStore(self, store=None):
        """Replace .store """
        if store is not None:
            if not isinstance(store, Store):
                raise ValueError('Not store %s' % store)
        self.store = store

    def push(self, elem):
        """
        Convenience method to push to .deck
        """
        self.deck.push(elem)

    def pull(self):
        """
        Convenience method to pull from .deck
        """
        return self.deck.pull()

    @property
    def owner(self):
        """Get owner property"""
        return self._owner

    @owner.setter
    def owner(self, owner):
        """Set owner property """
        self._owner = owner

    @property
    def truth(self):
        """Get truth property """
        return self._truth

    @truth.setter
    def truth(self, truth):
        """Set truth property """
        self._truth = truth

    @property
    def unit(self):
        """Get unit property """
        return self._unit

    @unit.setter
    def unit(self, unit):
        """Set unit property """
        if not isinstance(unit, Data):
            raise ValueError('Not Data object %s' % unit)
        self._unit = unit

    @property
    def value(self):
        """Get value property
           returns none if no field in data of name 'value'
        """
        try:
            return getattr(self._data, 'value')
        except AttributeError:
            return

    @value.setter
    def value(self, value):
        """Set value property """
        setattr(self._data, 'value', value)
        try:
            self.stamp = self.store.stamp
        except AttributeError as ex:
            self.stamp = None

    @property
    def data(self):
        """Get data property """
        return self._data

    @data.setter
    def data(self, data):
        """Set data property """
        if not isinstance(data, Data):
            raise ValueError('Not Data object %s' % data)
        self._data = data
        try:
            self.stamp = self.store.stamp
        except AttributeError as ex:
            self.stamp = None

    def stampNow(self):
        """Force time stamp of this share to store.stamp if exists
           This is useful when share data is changed in a way that does not
           update the stamp.
           so stampNow force updates the stamp.
        """
        try:
            self.stamp = self.store.stamp
        except AttributeError as ex:
            self.stamp = None

        return self.stamp

    def change(self, *pa, **kwa):
        """Change data fields without affecting stamp.
           Create if not already exist.
        """
        for a in pa:
            if isinstance(a, dict) or hasattr(a, 'get') and hasattr(a, 'items'):
                for k, v in a.items():
                    setattr(self._data, k, v)

            else:
                for k, v in a:
                    setattr(self._data, k, v)

        for k, v in kwa.items():
            setattr(self._data, k, v)

        return self

    def update(self, *pa, **kwa):
        """Update data fields of this share.
           create field if not already exist
           set stamp to store.stamp if store
        """
        (self.change)(*pa, **kwa)
        try:
            self.stamp = self.store.stamp
        except AttributeError as ex:
            self.stamp = None

        return self

    def create(self, *pa, **kwa):
        """Create and update fields if they do not already exist otherwise do nothing
           This allows setting defaults only if they have not already been set
        """
        update = False
        for a in pa:
            if isinstance(a, dict) or hasattr(a, 'get') and hasattr(a, 'items'):
                for k, v in a.items():
                    if not hasattr(self._data, k):
                        setattr(self._data, k, v)
                        update = True

            else:
                for k, v in a:
                    if not hasattr(self._data, k):
                        setattr(self._data, k, v)
                        update = True

        for k, v in kwa.items():
            if not hasattr(self._data, k):
                setattr(self._data, k, v)
                update = True

        if update:
            try:
                self.stamp = self.store.stamp
            except AttributeError as ex:
                self.stamp = None

        return self

    def fetch(self, field, default=None):
        """Retrieve from .data the the value of attribute field or
           None if it does not exist
        """
        return self.get(field, default)

    def copyDataDict(self):
        """returns a copy of the data odict dictionary
        """
        return self._data.__dict__.copy()

    def changeUnit(self, *pa, **kwa):
        """update unit from kw """
        if self.unit is None:
            self.unit = Data()
        for a in pa:
            if isinstance(a, dict):
                for k, v in a.items():
                    setattr(self.unit, k, v)

            else:
                for k, v in a:
                    setattr(self.unit, k, v)

        for k, v in kwa.items():
            setattr(self.unit, k, v)

        return self

    def createUnit(self, *pa, **kwa):
        """create unit from kw  """
        if self.unit is None:
            self.unit = Data()
        for a in pa:
            if isinstance(a, dict):
                for k, v in a.items():
                    if not hasattr(self._unit, k):
                        setattr(self._unit, k, v)

            else:
                for k, v in a:
                    if not hasattr(self._unit, k):
                        setattr(self._unit, k, v)

        for k, v in kwa.items():
            if not hasattr(self._unit, k):
                setattr(self._unit, k, v)

        return self

    def fetchUnit(self, field, default=None):
        """Retrieve from .unit the value of attribute field or None if it does not exist """
        if self.unit:
            if hasattr(self._unit, field):
                return getattr(self._unit, field)
        return default

    def expose(self):
        """print out important attributes for debugging """
        print('Name %s Store %s Stamp %s Value %s  Dict %s\nTruth %s Unit %s Owner %s ' % (
         self.name, self.store, self.stamp, self.value, self.data, self.truth,
         self.unit, self.owner))

    def show(self):
        """print name and data files"""
        result = 'Name {0} Value {1}\n'.format(self.name, self.value)
        entries = []
        for key, value in self.data.__dict__.items():
            entries.append('{0} = {1}'.format(key, value))

        result = '{0}{1}\n'.format(result, ' '.join(entries))
        return result


class Data(object):
    __doc__ = '\n    Data class\n    Attributes may be any python public identifier, that is,\n    a string that starts with letter but not underscore\n\n    Attempting to set an attribute that is not a python public identifier raises\n    AttributeError\n    '

    def __new__(cls, *pa, **kwa):
        """Set up at instance creation """
        self = object.__new__(cls)
        self.__dict__ = odict()
        return self

    def __init__(self, *pa, **kwa):
        """
        Data() -> new empty Data record.

        Data(pa1, pa2, ...) where pa = tuple of positional args, (pa1, pa2, ...)
              each paX may be  a sequence of duples (k,v) or a dict

        Data(k1 = v1, k2 = v2, ...) where kwa = dictionary of keyword args, {k1: v1, k2 : v2, ...}
        """
        for a in pa:
            if isinstance(a, dict):
                for k, v in a.items():
                    setattr(self, k, v)

            else:
                for k, v in a:
                    setattr(self, k, v)

        for k, v in kwa.items():
            setattr(self, k, v)

    def __setattr__(self, key, value):
        try:
            super(Data, self).__getattribute__(key)
        except AttributeError:
            if key in self.__dict__ or REO_IdentPub.match(key):
                self.__dict__.__setitem__(key, value)
            else:
                raise AttributeError("Invalid attribute name '%s'" % key)
        else:
            super(Data, self).__setattr__(key, value)

    def __repr__(self):
        """
        Representation
        """
        return '{0}({1})'.format(self.__class__.__name__, repr(self.__dict__.items()))

    def _change(self, *pa, **kwa):
        """
        Change attributes

        ._change(pa1, pa2, ...) where pa = tuple of positional args, (pa1, pa2, ...)
            each paX may be  a sequence of duples (k,v) or a dict

        ._change(k1 = v1, k2 = v2, ...) where kwa = dictionary of keyword args,
            {k1: v1, k2 : v2, ...}

        Returns self so can chain
        """
        for a in pa:
            if isinstance(a, dict):
                for k, v in a.items():
                    setattr(self, k, v)

            else:
                for k, v in a:
                    setattr(self, k, v)

        for k, v in kwa.items():
            setattr(self, k, v)

        return self

    def _sift(self, fields=None):
        """
        Return odict of items keyed by field name strings provided in  optional
        fields sequence in that order with each value given by the associated
        item in .__dict__
        If fields is not provided then return odict copy of .__dict__ with all
        the fields
        Raises AttributeError if no entry in .__dict__ for a given field name
        """
        if fields is None:
            return odict(self.__dict__)
        else:
            stuff = odict()
            for key in fields:
                if key not in self.__dict__:
                    raise AttributeError("'{0}' object has no attribute '{1}'".format(self.__class__.__name__, key))
                stuff[key] = self.__dict__[key]

            return stuff

    def _show(self):
        """
        Returns descriptive string for display purposes
        """
        infix = []
        for key in self.__dict__:
            val = getattr(self, key)
            infix.append('{0}={1}'.format(key, val))

        result = '{0}: {1}\n'.format(self.__class__.__name__, ' '.join(infix))
        return result


class Deck(deque):
    __doc__ = '\n    Extends deque to support deque access convenience methods .push and .pull\n    to remove confusion  about which side of the deque to use (left or right).\n\n    Extends deque to support deque access convenience methods .gulp and .spew\n    to enable a different pattern for access. .gulp does not allow  a value\n    of None to be added to the Deck so retrieval with .spew can be done without\n    checking for empty. .spew returns None when empty\n\n    To determine if deck or deque is empty use\n       if d:\n\n\n    Inherited methods from deque:\n    .append(x)             = add x to right side of deque\n    .appendleft(x)         = add x to left side of deque\n    .clear()               = clear all items from deque leaving it a length 0\n    .count(x)              = count the number of deque elements equal to x.\n    .extend(iterable)      = append elements of iterable to right side\n    .extendleft(iterable)  = append elemets of iterable to left side\n                             (this reverses iterable)\n    .pop()                 = remove and return element from right side\n                              if empty then raise IndexError\n    .popleft()             = remove and return element from left side\n                              if empty then raise IndexError\n    .remove(x)             = remove first occurence of x left to right\n                              if not found raise ValueError\n    .rotate(n)             = rotate n steps to right if neg rotate to left\n\n    Built in methods supported:\n    len(d)\n    reversed(d)\n    copy.copy(d)\n    copy.deepcopy(d)\n    subscripts d[0] d[-1]\n\n    Attributes:\n    .maxlen  = maximum size of Deck or None if unbounded\n\n    Local methods:\n    .push(x)   = add x to the right side of deque (alias of append)\n    .pull(x)   = remove and return element from left side of deque (alias of popleft)\n\n    .gulp(x)    = If not None, add x to right side of deque, Otherwise ignore\n    .spew()     = remove and return element from left side of deque,\n                 If empty return None\n\n\n    '
    push = deque.append
    pull = deque.popleft

    def __repr__(self):
        """    """
        itemreprs = repr(list(self))
        return 'Deck({0})'.format(itemreprs)

    def gulp(self, elem):
        """
        If not None, add elem to right side of deque, Otherwise ignore
        """
        if elem is not None:
            self.append(elem)

    def spew(self):
        """
        Remove and return elem from left side of deque,
        If empty return None
        """
        try:
            elem = self.popleft()
        except IndexError:
            elem = None

        return elem