# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/gf/base.py
# Compiled at: 2013-12-18 06:09:17
"""Generic functions and multi methods.

This module was snarfed from:
<http://svn.python.org/view/*checkout*/sandbox/trunk/overload/overloading.py?content-type=text%2Fplain&rev=43727>

The original doc string follows:

Dynamically overloaded functions.

This is an implementation of (dynamically, or run-time) overloaded
functions; also known as generic functions or multi-methods.

The dispatch algorithm uses the types of all argument for dispatch,
similar to (compile-time) overloaded functions or methods in C++ and
Java.

Most of the complexity in the algorithm comes from the need to support
subclasses in call signatures.  For example, if an function is
registered for a signature (T1, T2), then a call with a signature (S1,
S2) is acceptable, assuming that S1 is a subclass of T1, S2 a subclass
of T2, and there are no other more specific matches (see below).

If there are multiple matches and one of those doesn't *dominate* all
others, the match is deemed ambiguous and an exception is raised.  A
subtlety here: if, after removing the dominated matches, there are
still multiple matches left, but they all map to the same function,
then the match is not deemed ambiguous and that function is used.
Read the method find_func() below for details.

Python 2.5 is required due to the use of predicates any() and all().
"""
from itertools import izip as zip
from types import FunctionType
from inspect import getargspec

class GenericFunction(object):
    """An implementation of generic functions.
    """

    def __init__(self, default_func=None, name=None):
        self.registry = {}
        self.variadics = {}
        self.generated_variadic_signatures = {}
        self.arities = set()
        self.cache = {}
        self.name = name
        self.default_func = default_func

    def method(self, *types):
        """Decorator to register a method for a specific set of types.
        """

        def helper(function):
            self.register_func(types, function, False)
            return self.substitute

        return helper

    def variadic_method(self, *types):
        """Decorator to register a method for a specific set of types.
        
        The method has a variable argument count.
        """

        def helper(function):
            self.register_func(types, function, True)
            return self.substitute

        return helper

    def register_func(self, types, func, variadic):
        """Helper to register an implementation."""
        if self.name is None:
            self.name = '%s.%s' % (func.__module__, func.__name__)
            self.substitute.__name__ = func.__name__
        if self.substitute.__doc__ and func.__doc__:
            doc = '\n\n'
            if not self.registry:
                doc += 'Multi methods:\n\n'
            arg_spec = getargspec(func)
            doc += '.. function:: %s.%s(%s)' % (func.__module__, func.__name__,
             (', ').join('%s: %s' % (arg, type.__name__) for arg, type in zip(arg_spec[0], types)) + (', *%s' % arg_spec[1] if variadic else ''))
            doc += '\n\n'
            doc += ('\n').join('    ' + line for line in func.__doc__.split('\n'))
            if variadic:
                doc += '\n    *This is a variadic method.*'
            self.substitute.__doc__ += doc
        self.registry[tuple(types)] = func
        if variadic:
            self.variadics[tuple(types)] = func
            self.arities = set()
            for sig in self.generated_variadic_signatures:
                del self.registry[sig]

            self.generated_variadic_signatures = {}
        self.cache = {}
        return

    def __call__(self, *args):
        """Call the overloaded function."""
        types = tuple(map(type, args))
        func = self.cache.get(types)
        if func is None:
            self.cache[types] = func = self.find_func(types)
        return func(*args)

    def super(self, *types):
        """Answer a specific (base) method that for the types passed."""
        return self.find_func(types)

    def _fix_variadics(self, arity):
        """Fix the registry for all the variadic functions.
        
        Don't touch the cache, we never processed functions
        with this `arity`."""
        if arity not in self.arities:
            for sig, function in self.variadics.iteritems():
                sig_len = len(sig)
                if sig_len < arity:
                    new_sig = sig + (object,) * (arity - len(sig))
                    generated_arity = self.generated_variadic_signatures.get(new_sig)
                    if generated_arity is None and new_sig not in self.registry or generated_arity <= arity:
                        self.registry[new_sig] = function
                        self.generated_variadic_signatures[new_sig] = arity

            self.arities.add(arity)
        return

    def find_func(self, types):
        """Find the appropriate overloaded function; don't call it.
        
        This won't work for old-style classes or classes without __mro__.
    
        """
        func = self.registry.get(types)
        if func is not None:
            return func
        else:
            self._fix_variadics(len(types))
            mros = tuple(t.__mro__ for t in types)
            n = len(mros)
            candidates = [ sig for sig in self.registry if len(sig) == n and all(t in mro for t, mro in zip(sig, mros))
                         ]
            if not candidates:
                answer = self.default_func
                if answer is None:

                    def answer(*arguments):
                        raise NotImplementedError('Generic %r has no implementation for type(s): %s' % (
                         self.name,
                         (', ').join('%s.%s' % (parameterType.__module__, parameterType.__name__) for parameterType in types)))

                return answer
            if len(candidates) == 1:
                return self.registry[candidates[0]]

            def dominates(dom, sub, orders=tuple(dict((t, i) for i, t in enumerate(mro)) for mro in mros)):
                if dom is sub:
                    return False
                return all(order[d] <= order[s] for d, s, order in zip(dom, sub, orders))

            candidates = [ cand for cand in candidates if not any(dominates(dom, cand) for dom in candidates)
                         ]
            if len(candidates) == 1:
                return self.registry[candidates[0]]
            funcs = set(self.registry[cand] for cand in candidates)
            if len(funcs) == 1:
                return funcs.pop()
            raise TypeError('ambiguous call to generic %r; types=%r; candidates=%r' % (
             self.name, types, candidates))
            return

    def callmapped(self, mapper, *arguments):
        """Call the overloaded function, with a mapper passed explicitly."""
        types = tuple(map(type, arguments))
        function = self.cache.get(types)
        if function is None:
            self.cache[types] = function = self.find_func(types)
        return function(*(mapper(argument) for argument in arguments))


def _generic(defaultFunction=None, name=None, doc=None):
    """Answer a generic function, that is a real function object.
    """
    genericFunction = GenericFunction(defaultFunction, name)

    def substitute(*arguments):
        return genericFunction(*arguments)

    substitute.method = genericFunction.method
    substitute.variadic_method = genericFunction.variadic_method
    substitute.super = genericFunction.super
    if defaultFunction is not None:
        substitute.__name__ = defaultFunction.__name__
        substitute.__doc__ = defaultFunction.__doc__
    else:
        if name is not None:
            substitute.__name__ = name
        if doc is not None:
            substitute.__doc__ = doc
    genericFunction.substitute = substitute
    return substitute


def method(*types):
    u"""Automatically call the `method´ method of a generic function.

    This function is intended to be used as a decorator.
    """

    def helper(function):
        return find_generic(function).method(*types)(function)

    return helper


def variadic_method(*types):
    u"""Automatically call the `variadic_method´ method of a generic function.

    This function is intended to be used as a decorator.
    """

    def helper(function):
        return find_generic(function).variadic_method(*types)(function)

    return helper


@_generic
def find_generic(someObject):
    """Find the generic function for some function with the same name,
    """
    raise NotImplementedError("Can't find the generic function for %s" % type(someObject))


@find_generic.method(FunctionType)
def find_generic(function):
    try:
        name = function.__name__
        return function.func_globals[name]
    except KeyError:
        raise TypeError("Can't find a generic function for method named %s" % function.__name__)


generic = _generic(name='generic')

@method(FunctionType)
def generic(default_function):
    return _generic(default_function)


@method(type)
def generic(newstyle_class):
    return _generic(newstyle_class)


@method()
def generic():
    return _generic()


@method(basestring)
def generic(function_name):
    return _generic(name=function_name)


@method(basestring, basestring)
def generic(function_name, doc):
    return _generic(name=function_name, doc=doc)