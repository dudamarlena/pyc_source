# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/vmcontroller/common/support.py
# Compiled at: 2011-03-04 15:52:41
"""
Support
"""
try:
    import json
except ImportError:
    import simplejson as json

try:
    import pdb, inspect
except ImportError, e:
    print 'Import error in %s : %s' % (__name__, e)
    import sys
    sys.exit()

def serialize(data):
    """ 
    Serialize the information given in C{data}. 

    @param data: the data to serialize.
    @rtype str
    @return a string containing the serialized version of data.
    """
    return json.dumps(data)


def deserialize(data):
    """ 
    Deserialize the information given in C{data}, back to its original pythonic form.

    @param data: the data to deserialize.
    @return the python object contained in the serialized data.
    """
    return json.loads(data)


def discoverCaller():
    """
    Returns the name of the innermost frame when invoked.

    For instance, invoked from within a function g(), it'd return 
    'g'. Also works for classes:

    >>> class C:
    ...   name = discoverCaller()
    >>> print C.name
    C
    """
    caller = inspect.getouterframes(inspect.currentframe())[1][3]
    return caller


try:
    import ast
except ImportError:
    _eval_func = eval
else:
    _eval_func = ast.literal_eval

def safe_eval(expr):
    """ 
    Safely evaluates the given expression, if possible. 
    If the necessary modules aren't available (Python <= 2.5), falls
    back to an insecure evaluation.
    What it means to be safe in this context is that:
    "The string or node provided may only consist of the following
    Python literal structures: strings, numbers, tuples, lists, dicts, booleans,
    and None."
    """
    return _eval_func(expr)


def reverseDict(d):
    """
    Reverses a dictionary.
    If a key isn't unique (replicated value in the original dict), only 
    the "last" (iteration order dependent) is kept as a key in the
    result

    @type d: dictionary
    @param d: the dictionary to reverse
    """
    return dict((v, k) for (k, v) in d.iteritems())


class UninitializedPlaceholder(object):
    """
    Raises L{NotImplementedError} upon any access attempt.
    Meant to be used as a placeholder for uninitialized objects.
    """

    def __init__(self, msg=None):
        """
        @param msg: An optional message to pass to the exception raised
        """
        if not msg:
            msg = 'This is just an uninitialized placeholder!'
        self._msg = msg

    def __getattr__(self, attr):
        raise NotImplementedError(self._msg)