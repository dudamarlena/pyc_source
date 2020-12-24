# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\cgp\utils\argrec.py
# Compiled at: 2012-02-14 07:44:45
"""Make record array from argument list for function."""
import inspect, numpy as np

def argrec(func, *args, **kwargs):
    """
    Return a record array of the arguments ``func(*args, **kwargs)`` would receive.
    
    This function pieces together a Numpy record array that can be used to log 
    input to an arbitrary function.
    
    The optional keyword argument "ignore" can be a list specifying argument
    positions or names that should not be included in the result.
    
    For unnamed optional arguments to func, field names default to _i, where i
    is the field number.
    
    A function whose input argument a is required, b has a default, and 
    ``*args`` and ``**kwargs`` specify an arbitrary number of unnamed and 
    keyword arguments, respectively. It also prints the information we are 
    trying to obtain without having to modify or call f.
    
    >>> def f(a, b=10, *args, **kwargs):
    ...     print inspect.getargvalues(inspect.currentframe())
    
    Here's what we have to work with.
    
    >>> inspect.getargspec(f)
    ArgSpec(args=['a', 'b'], varargs='args', keywords='kwargs', defaults=(10,))
    
    Here are a number of function calls, showing the output of getargvalues(),
    and the corresponding output of argrec().
    
    >>> f(1)
    ArgInfo(args=['a', 'b'], varargs='args', keywords='kwargs',
    locals={'a': 1, 'args': (), 'b': 10, 'kwargs': {}})
    >>> argrec(f, 1) == np.rec.array([(1, 10)], dtype=[('a', int), ('b', int)])
    rec.array([ True], dtype=bool)

    >>> f(1.0, 2, "test", d=20)
    ArgInfo(args=['a', 'b'], varargs='args', keywords='kwargs',
    locals={'a': 1.0, 'args': ('test',), 'b': 2, 'kwargs': {'d': 20}})
    >>> argrec(f, 1.0, 2, "test", d=20) == np.rec.array([(1.0, 2, 'test', 20)],
    ...     dtype=[('a', float), ('b', int), ('_2', '|S4'), ('d', int)])
    rec.array([ True], dtype=bool)
    
    Checking that all required arguments are given.
    
    >>> f()
    Traceback (most recent call last):
    TypeError: f() takes at least 1 argument (0 given)
    >>> argrec(f)
    Traceback (most recent call last):
    TypeError: One or more required arguments (['a'])
    not specified, or specified by keyword.
    Unfortunately, argrec() currently does not understand
    required arguments specified by keyword.

    >>> argrec(f, ignore="a") == np.rec.array([(10,)], dtype=[('b', int)])
    rec.array([ True], dtype=bool)
    
    Ignoring an argument by position.
    
    #>>> argrec(f, 1, ignore=0) # DOES NOT WORK YET
    rec.array([(1,)], dtype=[('b', '<i4')])

    An argument that is given, but should be ignored.
    
    #>>> argrec(f, 1, ignore="a") # DOES NOT WORK YET
    rec.array([(10,)], dtype=[('b', '<i4')])
            
    This one isn't handled correctly: it is illegal to specify an argument both
    by position and by name, but argrec() doesn't catch this.
    
    >>> f(1.0, 2, "test", d=20, b="abc")
    Traceback (most recent call last):
    TypeError: f() got multiple values for keyword argument 'b'
    >>> argrec(f, 1.0, 2, "test", d=20, b="abc") == np.rec.array(
    ...     [(1.0, 2, 'test', 20)], 
    ...     dtype=[('a', float), ('b', int), ('_2', '|S4'), ('d', int)])
    rec.array([ True], dtype=bool)
    
    Another data type: bool.
    
    >>> argrec(f, 1, c=True) == np.rec.array([(1, 10, True)],
    ...     dtype=[('a', int), ('b', int), ('c', '|b1')])
    rec.array([ True], dtype=bool)
    
    Todo: A structured array as argument.
    
    >>> def h(r): pass
    >>> r = np.array((2, 3), dtype=[("a", "<i4"), ("b", "<i4")])
    
    #>>> argrec(h, r) # DOES NOT WORK YET
    array(((2,3),), dtype=[("r", [("a", "<i4"), ("b", "<i4")])])
    
    Todo: Multiple record arrays as argument.
    
    #>>> def i(r, s): pass
    #>>> argrec(i, r, r) # DOES NOT WORK YET
    #array(((2,3), (2,3)), dtype=[("r", [("a", "<i4"), ("b", "<i4")]), 
    #                             ("s", [("a", "<i4"), ("b", "<i4")])])
    
    Verify bugfix when there are no defaults. Slicing by [:-ndef] or [-ndef:] 
    breaks down when ndef is zero, because 
    [:-0] means [:0], i.e. no elements (intended: all except zero = all)
    [-0:] means [0:], i.e. all elements (intended: last except zero = none).
    
    >>> def g(a, b): pass
    >>> argrec(g, "This is a", "This is b")
    rec.array([('This is a', 'This is b')], dtype=[('a', '|S9'), ('b', '|S9')])
    
    ..  Tests not working yet::
        #>>> argrec(g, "This is a", "This is b", ignore=0) # DOES NOT WORK YET
        rec.array([('This is b')], dtype=[('b', '|S9')])
        #>>> argrec(g, "This is a", "This is b", ignore="a") # DOES NOT WORK YET
        rec.array([('This is b')], dtype=[('b', '|S9')])
        #>>> argrec(g, "This is a", "This is b", ignore=1) # DOES NOT WORK YET
        rec.array([('This is a',)], dtype=[('a', '|S9')])
        #>>> argrec(g, "This is a", "This is b", ignore=["b"]) # DOES NOT WORK YET
    """
    ignore = kwargs.pop('ignore', ())
    try:
        len(ignore)
    except TypeError:
        ignore = [
         ignore]

    if isinstance(ignore, basestring):
        ignore = [
         ignore]
    spec = inspect.getargspec(func)
    defaults = spec.defaults if spec.defaults else ()
    ndef = len(defaults)
    reqnames = spec.args[:-ndef] if ndef else spec.args
    for i in ignore:
        reqnames.remove(i)

    defnames = spec.args[-ndef:] if ndef else []
    nreq = len(reqnames)
    reqvals = args[:nreq]
    defvals = [ kwargs.pop(k, d) for k, d in zip(defnames, defaults) ]
    for i, v in enumerate(args[nreq:][:ndef]):
        defvals[i] = v

    varargs = args[nreq + ndef:]
    varargnames = [ '_%s' % (i + nreq + ndef) for i in range(len(varargs)) ]
    names = reqnames + defnames + varargnames + kwargs.keys()
    values = list(reqvals) + defvals + list(varargs) + kwargs.values()
    if len(names) != len(values):
        msg = 'One or more required arguments (%s)\n' % reqnames
        msg += 'not specified, or specified by keyword.\n'
        msg += 'Unfortunately, argrec() currently does not understand \n'
        msg += 'required arguments specified by keyword.'
        raise TypeError(msg)
    for i, (k, v) in enumerate(zip(names, values)):
        if k in ignore or i in ignore:
            del names[i]
            del values[i]

    return np.rec.fromarrays([ [i] for i in values ], names=names)


def autoname(x):
    """
    Record array of x, with automatic names if needed, and ndim >= 1.
    
    A view is returned if possible, otherwise a copy is made.
    
    >>> autoname([1, 2]) == np.rec.array([(1, 2)], 
    ...     dtype=[('_0', int), ('_1', int)])
    rec.array([ True], dtype=bool)
    >>> bool(autoname(np.rec.fromarrays([[1], ["test"]], names=["i", "s"])) == 
    ...     np.rec.array([(1, 'test')], dtype=[('i', int), ('s', '|S4')]))
    True
    >>> autoname(0) == np.rec.array([(0,)], dtype=[('_0', int)])
    rec.array([ True], dtype=bool)
    
    Changes to the recarray will affect the original array only if the data is 
    contiguous, otherwise a copy is made.
    
    >>> a = np.arange(4, dtype=np.byte).reshape(2, 2)
    >>> b = autoname(a[0])
    
    Below, creating the "c" array requires a copy, so the subsequent 
    assignment to c cannot update the original array.
    
    >>> c = autoname(a.T[0])
    >>> b._0 = 10
    >>> c._0 = 20
    >>> a
    array([[10,  1], [ 2,  3]], dtype=int8)
    """
    x = np.ascontiguousarray(x)
    if not x.shape:
        x.shape = (1, )
    if not x.dtype.names:
        dtype = [ ('_%s' % i, x.dtype) for i in range(len(x)) ]
        return x.view(dtype, np.recarray)
    else:
        return x.view(np.recarray)


if __name__ == '__main__':
    import doctest
    doctest.testmod(optionflags=doctest.NORMALIZE_WHITESPACE)