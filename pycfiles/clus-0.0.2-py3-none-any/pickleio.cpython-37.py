# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/Clumsy/io/pickleio.py
# Compiled at: 2018-11-20 16:29:41
# Size of source mod 2**32: 3043 bytes
from __future__ import print_function
from itertools import chain
from collections import deque
import pickle
from six.moves import cPickle
import sys
try:
    from reprlib import repr
except ImportError:
    print('Could not find rprlib cannot import repr')

__all__ = [
 'Save_Data', 'Load_Data', 'get_total_size']

def Save_Data(Object, path):
    """Saves arbitrary objects using pickling to desired path

    Parameters
    ----------
    Object: object, an arbitrary thing to save
    path: str, file path to Object to
    """
    with open(path, 'wb') as (handle):
        pickle.dump(Object, handle, protocol=(pickle.HIGHEST_PROTOCOL))
    print('saved successfully, file save as:\n' + path)


def Load_Data(path):
    """Loads objects using pickling

    Parameters
    ----------
    path: str, file path to load from

    Returns
    -------
    loaded_data: object, returned object
    """
    with open(path, 'rb') as (handle):
        loaded_data = pickle.load(handle)
        return loaded_data


def sizecheck(object):
    """Check size of object"""
    mydict = {'object': object}
    mydict_as_string = cPickle.dumps(mydict)
    print(sys.getsizeof(mydict_as_string))


def get_total_size(o, handlers={}, verbose=False):
    """ Returns the approximate memory footprint an object and all of its contents.
    Automatically finds the contents of the following builtin containers and
    their subclasses:  tuple, list, deque, dict, set and frozenset.
    To search other containers, add handlers to iterate over their contents:
        handlers = {SomeContainerClass: iter,
                    OtherContainerClass: OtherContainerClass.get_elements}

    Parameters
    ----------
    o: Object
    handlers:
    verbose: bool, whether to print out statements.

    Returns
    -------
    size

    ##### Example call #####

    #if __name__ == '__main__':
        #d = dict(a=power_ts)  # a=1, b=2, c=3, d=[4,5,6,7], e='a string of chars')
        #x = (total_size(d, verbose=True))
        #print(x)  # *1e-9)

    """
    dict_handler = lambda d: chain.from_iterable(d.items())
    all_handlers = {tuple: iter, 
     list: iter, 
     deque: iter, 
     dict: dict_handler, 
     set: iter, 
     frozenset: iter}
    all_handlers.update(handlers)
    seen = set()
    default_size = sys.getsizeof(0)

    def sizeof(o):
        if id(o) in seen:
            return 0
        seen.add(id(o))
        s = sys.getsizeof(o, default_size)
        if verbose:
            print(s, (type(o)), (repr(o)), file=(sys.stderr))
        for typ, handler in all_handlers.items():
            if isinstance(o, typ):
                s += sum(map(sizeof, handler(o)))
                break

        return s

    return sizeof(o)