# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: c:\dev\pylib\visvis\utils\ssdf\ssdf_base.py
# Compiled at: 2017-05-31 20:05:28
# Size of source mod 2**32: 14240 bytes
""" ssdf.ssdf_base.py

Implements the base functionality for ssdf:
    * The Struct class
    * Some constants and small functions
    * The VirtualArray class
    * The base classes for SSDFReader, SSDFWriter anf Block
"""
import sys
from . import ClassManager
try:
    import numpy as np
except ImportError:
    np = None

PY3 = sys.version_info[0] == 3
if PY3:
    string_types = (
     str,)
    integer_types = (int,)
    text_type = str
    binary_type = bytes
    ascii_type = str
    from functools import reduce
else:
    string_types = (
     basestring,)
    integer_types = (int, long)
    text_type = unicode
    binary_type = str
    ascii_type = str
    reduce = reduce
_CLASS_NAME = '_CLASS_NAME_'
_TYPE_DICT = ord('D')
_FLOAT_TYPES = set([float])
_INT_TYPES = set(integer_types)
if np:
    _FLOAT_TYPES.update([np.float32, np.float64])
    _INT_TYPES.update([np.int8, np.int16, np.int32, np.int64,
     np.uint8, np.uint16, np.uint32, np.uint64])
_FLOAT_TYPES = tuple(_FLOAT_TYPES)
_INT_TYPES = tuple(_INT_TYPES)

def isstruct(ob):
    """ isstruct(ob)
    
    Returns whether the given object is an SSDF struct.
    
    """
    if hasattr(ob, '__is_ssdf_struct__'):
        return bool(ob.__is_ssdf_struct__)
    else:
        return False


def _not_equal(ob1, ob2):
    """ _not_equal(ob1, ob2)
    
    Returns None if the objects are equal. Otherwise returns a string
    indicating how the objects are inequal.
    
    """
    if isstruct(ob1) or isinstance(ob1, dict):
        if not (isstruct(ob2) or isinstance(ob2, dict)):
            return '<type does not match>'
        keys1 = [key for key in ob1]
        keys2 = [key for key in ob2]
        if len(keys1) != len(keys2):
            return '<lengths do not match>'
        for key in keys1:
            if key not in keys2:
                return '<key not present in other struct/dict>'
            not_equal = _not_equal(ob1[key], ob2[key])
            if not_equal:
                return '.' + key + not_equal

    else:
        if isinstance(ob1, (tuple, list)):
            if not isinstance(ob2, (tuple, list)):
                return '<type does not match>'
            if len(ob1) != len(ob2):
                return '<lengths do not match>'
            for i in range(len(ob1)):
                not_equal = _not_equal(ob1[i], ob2[i])
                if not_equal:
                    return '[%i]' % i + not_equal

        else:
            if isinstance(ob1, VirtualArray):
                if not isinstance(ob2, VirtualArray):
                    return '<type does not match>'
                if not (ob1.shape == ob2.shape and ob1.dtype == ob2.dtype and ob1.data == ob2.data):
                    return '<array does not match>'
            elif np:
                if isinstance(ob1, np.ndarray):
                    if not isinstance(ob2, np.ndarray):
                        return '<type does not match>'
                else:
                    return ob1.shape == ob2.shape and ob1.dtype == ob2.dtype and (ob1 == ob2).sum() == ob1.size or '<array does not match>'
            elif not ob1 == ob2:
                return '<objects not equal>'


def _isvalidname(name):
    """ _isvalidname(name)
    
    Returns attribute name, or None, if not valid
    
    """
    if not (name and isinstance(name, string_types)):
        return
    else:
        namechars = str('abcdefghijklmnopqrstuvwxyz_0123456789')
        name2 = name.lower()
        if name2[0] not in namechars[0:-10]:
            return
        tmp = list(map(lambda x: x not in namechars, name2[2:]))
        if sum(tmp) == 0:
            return name


def _shapeString(ob):
    """ _shapeString(ob)
    
    Returns a string that represents the shape of the given array.
    
    """
    ss = str()
    for n in ob.shape:
        ss += '%ix' % n

    return ss[:-1]


class Struct(object):
    __doc__ = " Struct(dictionary=None)\n    \n    Object to holds named data (syntactic sugar for a dictionary).\n    \n    Attributes can be any of the seven SSDF supported types:\n    struct/dict, tuple/list, numpy array, (Unicode) string, int, float, None.\n    \n    Elements can be added in two ways:\n        * s.foo = 'bar'       # the object way\n        * s['foo'] = 'bar'    # the dictionary way\n    \n    Supported features\n    ------------------\n    * Iteration - yields the keys/names in the struct\n    * len() - returns the number of elements in the struct\n    * del statement can be used to remove elements\n    * two structs can be added, yielding a new struct with combined elements\n    * testing for equality with other structs\n    \n    Notes\n    -----\n      * The keys in the given dict should be valid names (invalid\n        keys are ignoired).\n      * On saving, names starting with two underscores are ignored.\n      * This class does not inherit from dict to keep its namespace clean,\n        avoid nameclashes, and to enable autocompletion of its items in\n        most IDE's.\n      * To get the underlying dict, simply use s.__dict__.\n    \n    "
    __is_ssdf_struct__ = True

    def __init__(self, a_dict=None):
        if a_dict is None:
            return
        elif not isinstance(a_dict, dict) and not isstruct(a_dict):
            tmp = 'Struct can only be initialized with a Struct or a dict.'
            raise ValueError(tmp)
        else:

            def _getValue(val):
                if isinstance(val, (string_types,) + _FLOAT_TYPES + _INT_TYPES):
                    return val
                else:
                    if np:
                        if isinstance(val, np.ndarray):
                            return val
                    if isinstance(val, (tuple, list)):
                        L = list()
                        for element in val:
                            L.append(_getValue(element))

                        return L
                    if isinstance(val, dict):
                        return Struct(val)

            for key in a_dict:
                if not _isvalidname(key):
                    print("Ignoring invalid key-name '%s'." % key)
                else:
                    val = a_dict[key]
                    self[key] = _getValue(val)

    def __getitem__(self, key):
        key2 = _isvalidname(key)
        if not key2:
            raise KeyError("Trying to get invalid name '%s'." % key)
        if key not in self.__dict__:
            raise KeyError(str(key))
        return self.__dict__[key]

    def __setitem__(self, key, value):
        key2 = _isvalidname(key)
        if not key2:
            raise KeyError("Trying to set invalid name '%s'." % key)
        self.__dict__[key] = value

    def __iter__(self):
        """ Returns iterator over keys. """
        return self.__dict__.__iter__()

    def __delitem__(self, key):
        return self.__dict__.__delitem__(key)

    def __len__(self):
        """ Return amount of fields in the Struct object. """
        return len(self.__dict__)

    def __add__(self, other):
        """ Enable adding two structs by combining their elemens. """
        s = Struct()
        s.__dict__.update(self.__dict__)
        s.__dict__.update(other.__dict__)
        return s

    def __eq__(self, other):
        return not _not_equal(self, other)

    def __repr__(self):
        """ Short string representation. """
        return '<SSDF struct instance with %i elements>' % len(self)

    def __str__(self):
        """ Long string representation. """
        c = 0
        for key in self:
            c = max(c, len(key))

        charsLeft = 79 - (c + 4)
        s = 'Elements in SSDF struct:\n'
        for key in self:
            if key.startswith('__'):
                pass
            else:
                tmp = '%s' % key
                value = self[key]
                valuestr = repr(value)
                if len(valuestr) > charsLeft or '\n' in valuestr:
                    typestr = str(type(value))[7:-2]
                    if np:
                        if isinstance(value, np.ndarray):
                            shapestr = _shapeString(value)
                            valuestr = '<array %s %s>' % (shapestr, str(value.dtype))
                    if isinstance(value, string_types):
                        valuestr = valuestr[:charsLeft - 3] + '...'
                    else:
                        valuestr = '<%s with length %i>' % (typestr, len(value))
                s += tmp.rjust(c + 2) + ': %s\n' % valuestr

        return s


class VirtualArray(object):
    __doc__ = ' VirtualArray\n    \n    A VirtualArray represents an array when numpy is not available.\n    This enables preserving the array when saving back a loaded dataset.\n    \n    '

    def __init__(self, shape, dtype, data):
        self.shape = tuple(shape)
        self.dtype = dtype
        self.data = data

    def tostring(self):
        return self.data

    @property
    def size(self):
        if self.shape:
            return reduce(lambda a, b: a * b, self.shape)
        else:
            return 1


class SSDFReader:

    def build_tree(self, root, blocks):
        """ build_tree(root, blocks)
        
        Build up the tree using the indentation information in the blocks.
        The tree is build up from the given root.
        
        """
        tree = [
         root]
        for block in blocks:
            while block._indent <= tree[(-1)]._indent:
                tree.pop()

            tree[(-1)]._children.append(block)
            tree.append(block)

    def serialize_struct(self, object, f=None):
        raise NotImplementedError()

    def read(self, file_or_string):
        raise NotImplementedError()


class SSDFWriter:

    def flatten_tree(self, block, sort=False):
        """ flatten_tree(block, sort=False)
        
        Returns a flat list containing the given block and
        all its children.
        
        If sort is True, packs blocks such that the data
        structures consisting of less blocks appear first.
        
        """
        listOfLists = []
        for child in block._children:
            childList = self.flatten_tree(child, sort)
            listOfLists.append(childList)

        if sort:
            if listOfLists:
                if block._type == _TYPE_DICT:
                    listOfLists.sort(key=len)
        flatList = [
         block]
        for childList in listOfLists:
            flatList.extend(childList)

        return flatList

    def write(self, object, f=None):
        raise NotImplementedError()


class Block:
    __doc__ = " Block\n    \n    A block represents a data element. This is where the conversion from\n    Python objects to text/bytes and vice versa occurs.\n    \n    A block is a line in a text file or a piece of data in a binary file.\n    A block contains all information about indentation, name, and value\n    of the data element that it represents. The raw representation of its\n    value is refered to as 'data'.\n    \n    "

    def __init__(self, indent, blocknr, name=None, type=None, data=None):
        self._indent = indent
        self._blocknr = blocknr
        self._name = name
        self._type = type
        self._data = data
        self._children = []

    @classmethod
    def from_object(cls, indent, name, value):
        self = cls(indent, -1, name)
        if value is None:
            self._from_none()
        else:
            if ClassManager.is_registered_class(value.__class__):
                s = value.__to_ssdf__()
                s[_CLASS_NAME] = value.__class__.__name__
                self._from_dict(s)
            else:
                if isinstance(value, _INT_TYPES):
                    self._from_int(value)
                else:
                    if isinstance(value, _FLOAT_TYPES):
                        self._from_float(value)
                    else:
                        if isinstance(value, bool):
                            self._from_int(int(value))
                        else:
                            if isinstance(value, string_types):
                                self._from_unicode(value)
                            elif np and isinstance(value, np.ndarray):
                                self._from_array(value)
                            else:
                                if isinstance(value, VirtualArray):
                                    self._from_array(value)
                                else:
                                    if isinstance(value, dict) or isstruct(value):
                                        self._from_dict(value)
                                    else:
                                        if isinstance(value, (list, tuple)):
                                            self._from_list(value)
                                        else:
                                            self._from_none()
                                            tmp = repr(value)
                                            if len(tmp) > 64:
                                                tmp = tmp[:64] + '...'
                                            if name is not None:
                                                print('SSDF: %s is unknown object: %s %s' % (
                                                 name, tmp, repr(type(value))))
                                            else:
                                                print('SSDF: unknown object: %s %s' % (
                                                 tmp, repr(type(value))))
        return self