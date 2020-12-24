# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/dicom_tools/pyqtgraph/pgcollections.py
# Compiled at: 2018-05-21 04:28:19
# Size of source mod 2**32: 15608 bytes
__doc__ = '\nadvancedTypes.py - Basic data structures not included with python \nCopyright 2010  Luke Campagnola\nDistributed under MIT/X11 license. See license.txt for more infomation.\n\nIncludes:\n  - OrderedDict - Dictionary which preserves the order of its elements\n  - BiDict, ReverseDict - Bi-directional dictionaries\n  - ThreadsafeDict, ThreadsafeList - Self-mutexed data structures\n'
import threading, sys, copy, collections
try:
    from collections import OrderedDict
except ImportError:
    from ordereddict import OrderedDict

class ReverseDict(dict):
    """ReverseDict"""

    def __init__(self, data=None):
        if data is None:
            data = {}
        self.reverse = {}
        for k in data:
            self.reverse[data[k]] = k

        dict.__init__(self, data)

    def __getitem__(self, item):
        if type(item) is list:
            return self.reverse[item[0]]
        return dict.__getitem__(self, item)

    def __setitem__(self, item, value):
        self.reverse[value] = item
        dict.__setitem__(self, item, value)

    def __deepcopy__(self, memo):
        raise Exception('deepcopy not implemented')


class BiDict(dict):
    """BiDict"""

    def __init__(self, data=None):
        if data is None:
            data = {}
        dict.__init__(self)
        for k in data:
            self[data[k]] = k

    def __setitem__(self, item, value):
        dict.__setitem__(self, item, value)
        dict.__setitem__(self, value, item)

    def __deepcopy__(self, memo):
        raise Exception('deepcopy not implemented')


class ThreadsafeDict(dict):
    """ThreadsafeDict"""

    def __init__(self, *args, **kwargs):
        self.mutex = threading.RLock()
        (dict.__init__)(self, *args, **kwargs)
        for k in self:
            if type(self[k]) is dict:
                self[k] = ThreadsafeDict(self[k])

    def __getitem__(self, attr):
        self.lock()
        try:
            val = dict.__getitem__(self, attr)
        finally:
            self.unlock()

        return val

    def __setitem__(self, attr, val):
        if type(val) is dict:
            val = ThreadsafeDict(val)
        self.lock()
        try:
            dict.__setitem__(self, attr, val)
        finally:
            self.unlock()

    def __contains__(self, attr):
        self.lock()
        try:
            val = dict.__contains__(self, attr)
        finally:
            self.unlock()

        return val

    def __len__(self):
        self.lock()
        try:
            val = dict.__len__(self)
        finally:
            self.unlock()

        return val

    def clear(self):
        self.lock()
        try:
            dict.clear(self)
        finally:
            self.unlock()

    def lock(self):
        self.mutex.acquire()

    def unlock(self):
        self.mutex.release()

    def __deepcopy__(self, memo):
        raise Exception('deepcopy not implemented')


class ThreadsafeList(list):
    """ThreadsafeList"""

    def __init__(self, *args, **kwargs):
        self.mutex = threading.RLock()
        (list.__init__)(self, *args, **kwargs)
        for k in self:
            self[k] = mkThreadsafe(self[k])

    def __getitem__(self, attr):
        self.lock()
        try:
            val = list.__getitem__(self, attr)
        finally:
            self.unlock()

        return val

    def __setitem__(self, attr, val):
        val = makeThreadsafe(val)
        self.lock()
        try:
            list.__setitem__(self, attr, val)
        finally:
            self.unlock()

    def __contains__(self, attr):
        self.lock()
        try:
            val = list.__contains__(self, attr)
        finally:
            self.unlock()

        return val

    def __len__(self):
        self.lock()
        try:
            val = list.__len__(self)
        finally:
            self.unlock()

        return val

    def lock(self):
        self.mutex.acquire()

    def unlock(self):
        self.mutex.release()

    def __deepcopy__(self, memo):
        raise Exception('deepcopy not implemented')


def makeThreadsafe(obj):
    if type(obj) is dict:
        return ThreadsafeDict(obj)
    if type(obj) is list:
        return ThreadsafeList(obj)
    if type(obj) in [str, int, float, bool, tuple]:
        return obj
    raise Exception('Not sure how to make object of type %s thread-safe' % str(type(obj)))


class Locker(object):

    def __init__(self, lock):
        self.lock = lock
        self.lock.acquire()

    def __del__(self):
        try:
            self.lock.release()
        except:
            pass


class CaselessDict(OrderedDict):
    """CaselessDict"""

    def __init__(self, *args):
        OrderedDict.__init__(self, {})
        self.keyMap = OrderedDict([(k.lower(), k) for k in OrderedDict.keys(self)])
        if len(args) == 0:
            return
            if len(args) == 1 and isinstance(args[0], dict):
                for k in args[0]:
                    self[k] = args[0][k]

        else:
            raise Exception('CaselessDict may only be instantiated with a single dict.')

    def __setitem__(self, key, val):
        kl = key.lower()
        if kl in self.keyMap:
            OrderedDict.__setitem__(self, self.keyMap[kl], val)
        else:
            OrderedDict.__setitem__(self, key, val)
            self.keyMap[kl] = key

    def __getitem__(self, key):
        kl = key.lower()
        if kl not in self.keyMap:
            raise KeyError(key)
        return OrderedDict.__getitem__(self, self.keyMap[kl])

    def __contains__(self, key):
        return key.lower() in self.keyMap

    def update(self, d):
        for k, v in d.iteritems():
            self[k] = v

    def copy(self):
        return CaselessDict(OrderedDict.copy(self))

    def __delitem__(self, key):
        kl = key.lower()
        if kl not in self.keyMap:
            raise KeyError(key)
        OrderedDict.__delitem__(self, self.keyMap[kl])
        del self.keyMap[kl]

    def __deepcopy__(self, memo):
        raise Exception('deepcopy not implemented')

    def clear(self):
        OrderedDict.clear(self)
        self.keyMap.clear()


class ProtectedDict(dict):
    """ProtectedDict"""

    def __init__(self, data):
        self._data_ = data

    wrapMethods = [
     '_cmp_', '__contains__', '__eq__', '__format__', '__ge__', '__gt__', '__le__', '__len__', '__lt__', '__ne__', '__reduce__', '__reduce_ex__', '__repr__', '__str__', 'count', 'has_key', 'iterkeys', 'keys']
    protectMethods = [
     '__getitem__', '__iter__', 'get', 'items', 'values']
    disableMethods = [
     '__delitem__', '__setitem__', 'clear', 'pop', 'popitem', 'setdefault', 'update']

    def wrapMethod(methodName):
        return lambda self, *a, **k: (getattr(self._data_, methodName))(*a, **k)

    def protectMethod(methodName):
        return lambda self, *a, **k: protect((getattr(self._data_, methodName))(*a, **k))

    def error(self, *args, **kargs):
        raise Exception('Can not modify read-only list.')

    for methodName in wrapMethods:
        locals()[methodName] = wrapMethod(methodName)

    for methodName in protectMethods:
        locals()[methodName] = protectMethod(methodName)

    for methodName in disableMethods:
        locals()[methodName] = error

    def copy(self):
        raise Exception('It is not safe to copy protected dicts! (instead try deepcopy, but be careful.)')

    def itervalues(self):
        for v in self._data_.itervalues():
            yield protect(v)

    def iteritems(self):
        for k, v in self._data_.iteritems():
            yield (
             k, protect(v))

    def deepcopy(self):
        return copy.deepcopy(self._data_)

    def __deepcopy__(self, memo):
        return copy.deepcopy(self._data_, memo)


class ProtectedList(collections.Sequence):
    """ProtectedList"""

    def __init__(self, data):
        self._data_ = data

    wrapMethods = [
     '__contains__', '__eq__', '__format__', '__ge__', '__gt__', '__le__', '__len__', '__lt__', '__ne__', '__reduce__', '__reduce_ex__', '__repr__', '__str__', 'count', 'index']
    protectMethods = [
     '__getitem__', '__getslice__', '__mul__', '__reversed__', '__rmul__']
    disableMethods = [
     '__delitem__', '__delslice__', '__iadd__', '__imul__', '__setitem__', '__setslice__', 'append', 'extend', 'insert', 'pop', 'remove', 'reverse', 'sort']

    def wrapMethod(methodName):
        return lambda self, *a, **k: (getattr(self._data_, methodName))(*a, **k)

    def protectMethod(methodName):
        return lambda self, *a, **k: protect((getattr(self._data_, methodName))(*a, **k))

    def error(self, *args, **kargs):
        raise Exception('Can not modify read-only list.')

    for methodName in wrapMethods:
        locals()[methodName] = wrapMethod(methodName)

    for methodName in protectMethods:
        locals()[methodName] = protectMethod(methodName)

    for methodName in disableMethods:
        locals()[methodName] = error

    def __iter__(self):
        for item in self._data_:
            yield protect(item)

    def __add__(self, op):
        if isinstance(op, ProtectedList):
            return protect(self._data_.__add__(op._data_))
        if isinstance(op, list):
            return protect(self._data_.__add__(op))
        raise TypeError('Argument must be a list.')

    def __radd__(self, op):
        if isinstance(op, ProtectedList):
            return protect(op._data_.__add__(self._data_))
        if isinstance(op, list):
            return protect(op.__add__(self._data_))
        raise TypeError('Argument must be a list.')

    def deepcopy(self):
        return copy.deepcopy(self._data_)

    def __deepcopy__(self, memo):
        return copy.deepcopy(self._data_, memo)

    def poop(self):
        raise Exception('This is a list. It does not poop.')


class ProtectedTuple(collections.Sequence):
    """ProtectedTuple"""

    def __init__(self, data):
        self._data_ = data

    wrapMethods = [
     '__contains__', '__eq__', '__format__', '__ge__', '__getnewargs__', '__gt__', '__hash__', '__le__', '__len__', '__lt__', '__ne__', '__reduce__', '__reduce_ex__', '__repr__', '__str__', 'count', 'index']
    protectMethods = [
     '__getitem__', '__getslice__', '__iter__', '__add__', '__mul__', '__reversed__', '__rmul__']

    def wrapMethod(methodName):
        return lambda self, *a, **k: (getattr(self._data_, methodName))(*a, **k)

    def protectMethod(methodName):
        return lambda self, *a, **k: protect((getattr(self._data_, methodName))(*a, **k))

    for methodName in wrapMethods:
        locals()[methodName] = wrapMethod(methodName)

    for methodName in protectMethods:
        locals()[methodName] = protectMethod(methodName)

    def deepcopy(self):
        return copy.deepcopy(self._data_)

    def __deepcopy__(self, memo):
        return copy.deepcopy(self._data_, memo)


def protect(obj):
    if isinstance(obj, dict):
        return ProtectedDict(obj)
    if isinstance(obj, list):
        return ProtectedList(obj)
    if isinstance(obj, tuple):
        return ProtectedTuple(obj)
    return obj


if __name__ == '__main__':
    d = {'x':1, 
     'y':[1, 2],  'z':({'a':2,  'b':[3, 4],  'c':(5, 6)}, 1, 2)}
    dp = protect(d)
    l = [
     1, 'x', ['a', 'b'], ('c', 'd'), {'x':1,  'y':2}]
    lp = protect(l)
    t = (
     1, 'x', ['a', 'b'], ('c', 'd'), {'x':1,  'y':2})
    tp = protect(t)