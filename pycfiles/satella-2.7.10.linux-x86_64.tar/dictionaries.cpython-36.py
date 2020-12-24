# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/virtualenv/python3.6.7/lib/python3.6/site-packages/satella/coding/structures/dictionaries.py
# Compiled at: 2020-04-14 13:42:23
# Size of source mod 2**32: 12548 bytes
import collections.abc, copy, typing as tp
from satella.coding.recast_exceptions import rethrow_as
from satella.configuration.schema import Descriptor, descriptor_from_dict
from satella.exceptions import ConfigurationValidationError
__all__ = [
 'DictObject', 'apply_dict_object', 'DictionaryView', 'TwoWayDictionary', 'DirtyDict',
 'KeyAwareDefaultDict']
K, V, T = tp.TypeVar('K'), tp.TypeVar('V'), tp.TypeVar('T')

class DictObject(tp.MutableMapping[(str, T)]):
    __doc__ = "\n    A dictionary wrapper that can be accessed by attributes.\n\n    You can use keys different than strings, but they will be inaccessible as attributes, and\n    you will have to do subscription to get them.\n\n    Eg:\n\n    >>> a = DictObject({'test': 5})\n    >>> self.assertEqual(a.test, 5)\n    "

    def __init__(self, *args, **kwargs):
        self._DictObject__data = dict(*args, **kwargs)

    def __delitem__(self, k: str) -> None:
        del self._DictObject__data[k]

    def __setitem__(self, k: str, v: T) -> None:
        self._DictObject__data[k] = v

    def __getitem__(self, item: str) -> T:
        return self._DictObject__data[item]

    def __iter__(self) -> tp.Iterator[str]:
        return iter(self._DictObject__data)

    def __len__(self) -> int:
        return len(self._DictObject__data)

    def __copy__(self) -> 'DictObject':
        return DictObject(self._DictObject__data.copy())

    def __eq__(self, other: dict):
        if isinstance(other, DictObject):
            return self._DictObject__data == other._DictObject__data
        else:
            return self._DictObject__data == other

    def copy(self) -> 'DictObject':
        return DictObject(self._DictObject__data.copy())

    def __deepcopy__(self, memo) -> 'DictObject':
        return DictObject(copy.deepcopy(self._DictObject__data, memo))

    @rethrow_as(KeyError, AttributeError)
    def __getattr__(self, item: str) -> T:
        return self[item]

    def __setattr__(self, key, value):
        if key == '_DictObject__data':
            return super().__setattr__(key, value)
        self[key] = value

    @rethrow_as(KeyError, AttributeError)
    def __delattr__(self, key: str) -> None:
        del self[key]

    def is_valid_schema(self, schema: tp.Optional[tp.Union[(Descriptor, tp.Dict)]]=None, **kwarg_schema) -> bool:
        """
        Check if this dictionary conforms to particular schema.

        Schema is either a Descriptor, or a JSON-based schema. See satella.configuration.schema for details.
        Schema can be passed as well using kwargs. It will be preferred to the one passed as schema.

        :param schema: schema to verify against
        :return: whether is conformant
        """
        if kwarg_schema:
            schema = kwarg_schema
        else:
            if isinstance(schema, Descriptor):
                descriptor = schema
            else:
                descriptor = descriptor_from_dict(schema)
        try:
            descriptor(self._DictObject__data)
        except ConfigurationValidationError:
            return False
        else:
            return True


def apply_dict_object(v: tp.Union[(tp.Any, tp.Dict[(str, T)])]) -> tp.Union[(DictObject, tp.Any)]:
    """
    Apply DictObject() to every dict inside v.

    This assumes that the only things that will be touched will be nested dicts and lists.

    If you pass a non-dict and a non-list, they will be returned as is.
    """
    if isinstance(v, list):
        return [apply_dict_object(x) for x in v]
    else:
        if isinstance(v, dict):
            return DictObject({k:apply_dict_object(val) for k, val in v.items()})
        return v


class DictionaryView(collections.abc.MutableMapping, tp.Generic[(K, V)]):
    __doc__ = "\n    A view on a multiple dictionaries. If key isn't found in the first dictionary, it is looked up\n    in another. Use like:\n\n    >>> dv = DictionaryView({1:2, 3:4}, {4: 5, 6: 7})\n    >>> assert dv[4] == 5\n    >>> del dv[1]\n    >>> assertRaises(KeyError, lambda: dv.__delitem__(1))\n\n    :param master_dict: First dictionary to look up. Entries made via __setitem__ will be put here.\n    :param rest_of_dicts: Remaining dictionaries\n    :param propagate_deletes: Whether to delete given key from the first dictionary that it is\n        found. Otherwise it will be only deleted from the master_dict. Also, if this is set to\n        False, on deletion, if the key isn't found in master dictionary, deletion will KeyError.\n    :param assign_to_same_dict: whether updates done by __setitem__ should be written to the\n        dictionary that contains that key. If not, all updates will be stored in master_dict. If\n        this is True, updates made to keys that are not in this dictionary will go to master_dict.\n    "
    __slots__ = ('assign_to_same_dict', 'master_dict', 'dictionaries', 'propagate_deletes')

    def __copy__(self):
        return DictionaryView(*copy.copy(self.dictionaries))

    def __deepcopy__(self, memo):
        return DictionaryView(*copy.deepcopy(self.dictionaries, memo))

    def __init__(self, master_dict: tp.Dict[(K, V)], *rest_of_dicts: tp.Dict[(K, V)], propagate_deletes: bool=True, assign_to_same_dict: bool=True):
        self.assign_to_same_dict = assign_to_same_dict
        self.master_dict = master_dict
        self.dictionaries = [master_dict, *rest_of_dicts]
        self.propagate_deletes = propagate_deletes

    def __contains__(self, item: K) -> bool:
        for dictionary in self.dictionaries:
            if item in dictionary:
                return True

        return False

    def __iter__(self) -> tp.Iterator[K]:
        seen_already = set()
        for dictionary in self.dictionaries:
            for key in dictionary:
                if key not in seen_already:
                    yield key
                    seen_already.add(key)

    def __len__(self) -> int:
        seen_already = set()
        i = 0
        for dictionary in self.dictionaries:
            for key in dictionary:
                if key not in seen_already:
                    i += 1
                    seen_already.add(key)

        return i

    def __getitem__(self, item: K) -> V:
        for dictionary in self.dictionaries:
            if item in dictionary:
                return dictionary[item]

        raise KeyError('Key not found')

    def __setitem__(self, key: K, value: V):
        if self.assign_to_same_dict:
            for dictionary in self.dictionaries:
                if key in dictionary:
                    dictionary[key] = value
                    return

        self.master_dict[key] = value

    def __delitem__(self, key: K) -> V:
        if self.propagate_deletes:
            for dictionary in self.dictionaries:
                if key in dictionary:
                    del dictionary[key]
                    return

            raise KeyError('Key not found')
        else:
            del self.master_dict[key]


class TwoWayDictionary(collections.abc.MutableMapping, tp.Generic[(K, V)]):
    __doc__ = "\n    A dictionary that keeps also a reverse_data mapping, allowing to look up keys by values.\n\n    Not thread-safe.\n\n    Example usage:\n\n    >>> twd = TwoWayDictionary()\n    >>> twd[2] = 3\n    >>> self.assertEqual(twd.reverse[3], 2)\n\n    When you're done using a given TwoWayDictionary, please call .done(). This will make it easier for the GC to collect\n    the dictionaries.\n\n    You can also use the context manager to make the TwoWayDictionary clean up itself, eg.\n\n    >>> with TwoWayDictionary() as twd:\n    >>>     ...\n    >>> # at this point twd is .done()\n\n    :param data: data to generate the dict from\n    :raises ValueError: on being given data from which it is impossible to construct a reverse\n        mapping (ie. same value appears at least twice)\n    "
    __slots__ = ('data', 'reverse_data', '_reverse')

    def done(self):
        """
        Called when the user is done using given TwoWayDictionary.

        Internally this will break the reference cycle, and enable Python GC to collect the objects.
        """
        self.reverse.reverse = None
        self.reverse = None

    def __init__(self, data=None, _is_reverse: bool=False):
        if not _is_reverse:
            self.data = dict(data or [])
            self.reverse_data = {v:k for k, v in self.data.items()}
            if len(self.reverse_data) != len(self.data):
                raise ValueError('Value repeats itself, invalid data!')
            self._reverse = TwoWayDictionary(_is_reverse=True)
            self._reverse.data = self.reverse_data
            self._reverse.reverse_data = self.data
            self._reverse._reverse = self

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.done()
        return False

    def __getitem__(self, item: K) -> V:
        return self.data[item]

    def items(self) -> tp.Iterator[tp.Tuple[(K, V)]]:
        return self.data.items()

    def keys(self) -> tp.AbstractSet[K]:
        return self.data.keys()

    def values(self) -> tp.AbstractSet[V]:
        return self.data.values()

    def __len__(self) -> int:
        return len(self.data)

    def __setitem__(self, key: K, value: V):
        if value in self.reverse_data:
            raise ValueError('This value is already mapped to something!')
        try:
            prev_val = self.data[key]
        except KeyError:
            pass
        else:
            del self.reverse_data[prev_val]
        self.data[key] = value
        self.reverse_data[value] = key

    def __delitem__(self, key: K) -> None:
        value = self.data[key]
        del self.data[key]
        del self.reverse_data[value]

    def __iter__(self) -> tp.Iterator[K]:
        return iter(self.data)

    @property
    def reverse(self) -> tp.MutableMapping[(V, K)]:
        """
        Return a reverse mapping. Reverse mapping is updated as soon as an operation is done.
        """
        return self._reverse


class DirtyDict(collections.UserDict, tp.Generic[(K, V)]):
    __doc__ = "\n    A dictionary that has also a flag called .dirty that sets to True if the dictionary has been\n    changed since that flag was last cleared.\n\n    Setting the dict with the value that it already has doesn't count as dirtying it.\n    Note that such changes will not be registered in the dict!\n    "

    def __init__(self, *args, **kwargs):
        (super().__init__)(*args, **kwargs)
        self.dirty = False

    def __copy__(self) -> 'DirtyDict':
        dd = DirtyDict(self.data.copy())
        dd.dirty = self.dirty
        return dd

    def __setitem__(self, key, value):
        if key in self:
            if self[key] == value:
                return
        super().__setitem__(key, value)
        self.dirty = True

    def __delitem__(self, key):
        super().__delitem__(key)
        self.dirty = True

    def clear_dirty(self) -> None:
        """Clears the dirty flag"""
        self.dirty = False

    def __bool__(self) -> bool:
        return bool(self.data)

    def swap_and_clear_dirty(self) -> tp.Dict[(K, V)]:
        """
        Returns this data, clears self and sets dirty to False

        After this is called, this dict will be considered empty.

        :return: a plain, normal Python dictionary is returned
        """
        a = self.data
        self.data = {}
        self.dirty = False
        return a

    def copy_and_clear_dirty(self) -> tp.Dict[(K, V)]:
        """
        Returns a copy of this data and sets dirty to False

        :return: a plain, normal Python dictionary is returned
        """
        a = self.data.copy()
        self.dirty = False
        return a


class KeyAwareDefaultDict(collections.abc.MutableMapping):
    __doc__ = '\n    A defaultdict whose factory function accepts the key to provide a default value for the key\n\n    :param factory_function: a callable that accepts a single argument, a key, for which it is to provide\n        a default value\n    '

    def __len__(self) -> int:
        return len(self.dict)

    def __iter__(self):
        return iter(self.dict)

    def __init__(self, factory_function: tp.Callable[([K], V)], *args, **kwargs):
        self.dict = dict(*args, **kwargs)
        self.factory_function = factory_function

    def __getitem__(self, item):
        if item in self.dict:
            return self.dict[item]
        else:
            self.dict[item] = self.factory_function(item)
            return self.dict[item]

    def __setitem__(self, key, value):
        self.dict[key] = value

    def __delitem__(self, key):
        del self.dict[key]