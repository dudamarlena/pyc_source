# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\HDi\Google Drive\ProgramCodes\PythonCodes\gaeio\src\segpy\catalog.py
# Compiled at: 2020-04-25 14:33:32
# Size of source mod 2**32: 20281 bytes
from abc import abstractmethod, ABCMeta
from collections import Mapping, Sequence, OrderedDict
from fractions import Fraction
import reprlib, os, sys
sys.path.append(os.path.dirname(__file__)[:-6][:-4][:-6])
from gaeio.src.segpy.util import contains_duplicates, measure_stride, minmax

class CatalogBuilder(object):
    __doc__ = 'Use a catalog builder to construct optimised, immutable mappings.\n\n    A CatalogBuilder is useful when, depending on the particular keys and\n    values used, a more compact or efficient representation of the mapping\n    is possible than, say, a regular dictionary. The CatalogBuilder\n    accumulates values and then, once all values have been added, analyzes\n    the keys and values to produce a more optimized representation of the\n    mapping.\n    '

    def __init__(self, mapping=None):
        """Initialize a Catalog Builder.

        Args:
            mapping: An optional mapping (such as a dictionary) of items.
        """
        self._catalog = []
        if mapping is not None:
            for key, value in mapping.items():
                self.add(key, value)

    def add(self, index, value):
        """Add an item.

        Each index must be unique if create() is to be subsequently
        called successfully, although duplicate index values will be
        accepted by this call without complaint.

        """
        self._catalog.append((index, value))

    def create(self):
        """Create a possibly more optimized representation of the mapping.

        In this worst case, this method returns an object which is
        essentially an immutable dictionary. In the best case, the
        space savings can be vast.

        Returns:
            A mapping, if a unique mapping from indexes to values is
            possible, otherwise None.

        """
        if len(self._catalog) < 2:
            return DictionaryCatalog(self._catalog)
        else:
            self._catalog.sort(key=(lambda index_value: index_value[0]))
            if contains_duplicates(index for index, value in self._catalog):
                return
            if all(isinstance(index, Sequence) and len(index) == 2 for index, value in self._catalog):
                return self._create_catalog_2()
            return self._create_catalog_1()

    def _create_catalog_1(self):
        """Create a catalog for one-dimensional integer keys (i.e. scalars)
        """
        index_min = self._catalog[0][0]
        index_max = self._catalog[(-1)][0]
        index_stride = measure_stride(index for index, value in self._catalog)
        if index_stride is None:
            return DictionaryCatalog(self._catalog)
        else:
            self._catalog.sort(key=(lambda index_value: index_value[1]))
            value_min = self._catalog[0][1]
            value_max = self._catalog[(-1)][1]
            value_stride = measure_stride(value for index, value in self._catalog)
            if index_stride is not None:
                if value_stride == 0:
                    assert value_min == value_max
                    return RegularConstantCatalog(index_min, index_max, index_stride, value_min)
        if index_stride is None:
            assert value_stride == 0 and value_min == value_max
            return ConstantCatalog((index for index, value in self._catalog), value_min)
        else:
            if index_stride is not None and value_stride is None:
                return RegularCatalog(index_min, index_max, index_stride, (value for index, value in self._catalog))
            elif not (index_stride is not None and value_stride is not None):
                raise AssertionError
            catalog = LinearRegularCatalog(index_min, index_max, index_stride, value_min, value_max, value_stride)
            return catalog

    def _create_catalog_2(self):
        """Create a catalog for two-dimensional integer keys.

        Each key must be a two-element sequence.
        """
        i_min, i_max = minmax(i for (i, j), value in self._catalog)
        j_min, j_max = minmax(j for (i, j), value in self._catalog)
        is_rm, diff = self._is_row_major(i_min, j_min, j_max)
        if is_rm:
            return RowMajorCatalog(i_min, i_max, j_min, j_max, diff)
        else:
            return DictionaryCatalog(self._catalog)

    def _is_row_major(self, i_min, j_min, j_max):
        """Does row major ordering predict values from keys?

        In row-major order the last dimension is contiguous, and so changes
        quickest, when moving through the elements in storage order. Hence
        the number of rows is the number of distinct i values and the numbers
        of elements in each row (i.e. columns) is the number of distinct j.

        Args:
            i_min: The minimum i value.
            j_min: The minimum j value.
            j_max: The maximum j value.

        Returns:
            A 2-tuple containing, in the first element True if the values can
            be predicted from the keys by assuming a row-major ordering,
            otherwise False. If True, the second element will be a constant
            offset, otherwise it can be ignored.
        """
        diff = None
        for (i, j), actual_value in self._catalog:
            proposed_value = (i - i_min) * (j_max + 1 - j_min) + (j - j_min)
            current_diff = actual_value - proposed_value
            if diff is None:
                diff = current_diff
            if current_diff != diff:
                return (False, None)

        return (
         True, diff)


class Catalog(Mapping):
    __doc__ = 'An abstract base class for Catalogs which provides min and max keys and values.'
    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self, key_min=None, key_max=None, value_min=None, value_max=None):
        """Must be overridden and called by subclasses.

        Args:
            key_min: Optional minimum key.
            key_max: Optional maximum key.
            value_min: Optional minimum value.
            value_max: Optional maximum value.
        """
        self._min_key = key_min
        self._max_key = key_max
        self._min_value = value_min
        self._max_value = value_max

    def key_min(self):
        """Minimum key"""
        if self._min_key is None:
            self._min_key = min(self.keys())
        return self._min_key

    def key_max(self):
        """Maximum key"""
        if self._max_key is None:
            self._max_key = max(self.keys())
        return self._max_key

    def value_min(self):
        """Minimum value"""
        if self._min_value is None:
            self._min_value = min(self.values())
        return self._min_value

    def value_max(self):
        """Maximum value"""
        if self._max_value is None:
            self._max_value = max(self.values())
        return self._max_value


class RowMajorCatalog(Catalog):
    __doc__ = 'A mapping which assumes a row-major ordering of a two-dimensional matrix.\n\n    This is the ordering of items in a two-dimensional matrix where in\n    the (i, j) key tuple the j value changes fastest when iterating\n    through the items in order.\n\n    A RowMajorCatalog predicts the value v from the key (i, j) according to the\n    following formula:\n\n        v = (i - i_min) * j_max + (j - j_min) + c\n\n    for\n        i_min <= i <= i_max\n        j_min <= j <= j_max\n\n    and where c is an integer constant to allow zero- or one-based indexing.\n    '

    def __init__(self, i_min, i_max, j_min, j_max, c):
        super(RowMajorCatalog, self).__init__()
        self._i_min = i_min
        self._i_max = i_max
        self._j_min = j_min
        self._j_max = j_max
        self._c = c

    @property
    def i_min(self):
        """Minimum i value"""
        return self._i_min

    @property
    def i_max(self):
        """Maximum i value"""
        return self._i_max

    @property
    def j_min(self):
        """Minimum j value"""
        return self._j_min

    @property
    def j_max(self):
        """Maximum j value"""
        return self._j_max

    def key_min(self):
        """Minimum (i, j) key"""
        return (
         self._i_min, self._j_min)

    def key_max(self):
        """Maximum (i, j) key"""
        return (
         self._i_max, self._j_max)

    def value_min(self):
        """Minimum value at key_min"""
        return self[self.key_min()]

    def value_max(self):
        """Maximum value at key_max"""
        return self[self.key_max()]

    def __getitem__(self, key):
        i, j = key
        if not self._i_min <= i <= self._i_max:
            if self._j_min <= j <= self._j_max:
                raise KeyError('{!r} key {!r} out of range'.format(self, key))
        value = (i - self._i_min) * (self._j_max + 1 - self._j_min) + (j - self._j_min) + self._c
        return value

    def __contains__(self, key):
        i, j = key
        return self._i_min <= i <= self._i_max and self._j_min <= j <= self._j_max

    def __len__(self):
        return (self._i_max - self._i_min) * (self._j_max + 1 - self._j_min)

    def __iter__(self):
        for i in range(self._i_min, self._i_max + 1):
            for j in range(self._j_min, self._j_max + 1):
                yield (
                 i, j)

    def __repr__(self):
        return '{}({}, {}, {}, {}, {})'.format(self.__class__.__name__, self._i_min, self._i_max, self._j_min, self._j_max, self._c)


class DictionaryCatalog(Catalog):
    __doc__ = 'An immutable, ordered, dictionary mapping.\n    '

    def __init__(self, items):
        super(DictionaryCatalog, self).__init__()
        self._items = OrderedDict(items)

    def __getitem__(self, key):
        return self._items[key]

    def __iter__(self):
        return iter(self._items)

    def __len__(self):
        return len(self._items)

    def __contains__(self, item):
        return item in self._items

    def __repr__(self):
        return '{}({})'.format(self.__class__.__name__, reprlib.repr(self._items.items()))


class RegularConstantCatalog(Catalog):
    __doc__ = 'Mapping with keys ordered with regular spacing along the number line.\n\n    The values associated with the keys are constant.\n    '

    def __init__(self, key_min, key_max, key_stride, value):
        key_range = key_max - key_min
        if key_range % key_stride != 0:
            raise ValueError('RegularIndex key range {!r} is not a multiple of stride {!r}'.format(key_stride, key_range))
        super(RegularConstantCatalog, self).__init__(key_min=key_min,
          key_max=key_max,
          value_min=value,
          value_max=value)
        self._key_stride = key_stride

    def __getitem__(self, key):
        if key not in self:
            raise KeyError('{!r} does not contain key {!r}'.format(self, key))
        return self.value_min()

    def __len__(self):
        return 1 + (self.key_max() - self.key_min()) / self._key_stride

    def __contains__(self, key):
        return self.key_min() <= key <= self.key_max() and (key - self.key_min()) % self._key_stride == 0

    def __iter__(self):
        return iter(range(self.key_min(), self.key_max() + 1, self._key_stride))

    def __repr__(self):
        return '{}({}, {}, {}, {})'.format(self.__class__.__name__, self.key_min(), self.key_max(), self._key_stride, self.value_min())


class ConstantCatalog(Catalog):
    __doc__ = 'Mapping with arbitrary keys and a single constant value.\n    '

    def __init__(self, keys, value):
        super(ConstantCatalog, self).__init__(value_min=value, value_max=value)
        self._items = frozenset(keys)

    def __getitem__(self, key):
        if key not in self:
            raise KeyError('{!r} does not contain key {!r}'.format(self, key))
        return self.value_min()

    def __len__(self):
        return len(self._items)

    def __contains__(self, key):
        return key in self._items

    def __iter__(self):
        return iter(self._items)

    def __repr__(self):
        return '{}({}, {})'.format(self.__class__.__name__, reprlib.repr(self._items), self.value_min())


class RegularCatalog(Catalog):
    __doc__ = 'Mapping with keys ordered with regular spacing along the number line.\n\n    The values associated with the keys are arbitrary.\n    '

    def __init__(self, key_min, key_max, key_stride, values):
        key_range = key_max - key_min
        if key_range % key_stride != 0:
            raise ValueError('{} key range {!r} is not a multiple of stride {!r}'.format(self.__class__.__name__, key_stride, key_range))
        super(RegularCatalog, self).__init__(key_min=key_min, key_max=key_max)
        self._key_stride = key_stride
        self._values = list(values)
        num_keys = key_range // key_stride
        if num_keys != len(self._values):
            raise ValueError('{} key range and values inconsistent'.format(self.__class__.__name__))

    def __getitem__(self, key):
        if not self.key_min() <= key <= self.key_max():
            raise KeyError('{!r} key {!r} out of range'.format(self, key))
        offset = key - self.key_min()
        if offset % self._key_stride != 0:
            raise KeyError('{!r} does not contain key {!r}'.format(self, key))
        index = offset // self._key_stride
        return self._values[index]

    def __len__(self):
        return len(self._values)

    def __contains__(self, key):
        return self.key_min() <= key <= self.key_max() and (key - self.key_min()) % self._key_stride == 0

    def __iter__(self):
        return iter(range(self.key_min(), self.key_max() + 1, self._key_stride))

    def __repr__(self):
        return '{}({}, {}, {}, {})'.format(self.__class__.__name__, self.key_min(), self.key_max(), self._key_stride, reprlib.repr(self._values))


class LinearRegularCatalog(Catalog):
    __doc__ = 'A mapping which assumes a linear relationship between keys and values.\n\n    This is the ordering of items in a two-dimensional matrix where in\n    the (i, j) key tuple the j value changes fastest when iterating\n    through the items in order.\n\n    A LinearRegularCatalog predicts the value v from the key according to the\n    following formula:\n\n        v = (value_max - value_min) / (key_max - key_min) * (key - key_min) + value_min\n    '

    def __init__(self, key_min, key_max, key_stride, value_min, value_max, value_stride):
        key_range = key_max - key_min
        if key_range % key_stride != 0:
            raise ValueError('{} key range {!r} is not a multiple of key stride {!r}'.format(self.__class__.__name__, key_stride, key_range))
        self._key_stride = key_stride
        value_range = value_max - value_min
        if value_range % value_stride != 0:
            raise ValueError('{} value range {!r} is not a multiple of value stride {!r}'.format(self.__class__.__name__, value_stride, value_range))
        self._value_stride = value_stride
        super(LinearRegularCatalog, self).__init__(key_min=key_min,
          key_max=key_max,
          value_min=value_min,
          value_max=value_max)
        num_keys = (self.key_max() - self.key_min()) // self._key_stride
        num_values = (self.value_max() - self.value_min()) // self._value_stride
        if num_keys != num_values:
            raise ValueError('{} inconsistent number of keys {} and values {}'.format(self.__class__.__name__, num_keys, num_values))
        self._m = Fraction(self.value_max() - self.value_min(), self.key_max() - self.key_min())

    def __getitem__(self, key):
        if not self.key_min() <= key <= self.key_max():
            raise KeyError('{!r} key {!r} out of range'.format(self, key))
        else:
            offset = key - self.key_min()
            if offset % self._key_stride != 0:
                raise KeyError('{!r} does not contain key {!r}'.format(self, key))
            v = self._m * (key - self.key_min()) + self.value_min()
            assert v.denominator == 1
        return v.numerator

    def __len__(self):
        return 1 + (self.key_max() - self.key_min()) // self._key_stride

    def __contains__(self, key):
        return self.key_min() <= key <= self.key_max() and (key - self.key_min()) % self._key_stride == 0

    def __iter__(self):
        return iter(range(self.key_min(), self.key_max() + 1, self._key_stride))

    def __repr__(self):
        return '{}({}, {}, {}, {}, {}, {})'.format(self.__class__.__name__, self.key_min(), self.key_max(), self._key_stride, self.value_min(), self.value_max(), self._value_stride)