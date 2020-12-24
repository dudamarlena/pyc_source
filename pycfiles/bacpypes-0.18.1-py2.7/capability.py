# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bacpypes/capability.py
# Compiled at: 2017-05-01 00:38:10
"""
Capability
"""
from .debugging import bacpypes_debugging, ModuleLogger
_debug = 0
_log = ModuleLogger(globals())

@bacpypes_debugging
class Capability(object):
    _zindex = 99

    def __init__(self):
        if _debug:
            Capability._debug('__init__')


@bacpypes_debugging
class Collector(object):

    def __init__(self):
        if _debug:
            Collector._debug('__init__ (%r %r)', self.__class__, self.__class__.__bases__)
        self.capabilities = self._search_capability(self.__class__)
        for cls in self.capabilities:
            if hasattr(cls, '__init__') and cls is not Collector:
                if _debug:
                    Collector._debug('    - calling %r.__init__', cls)
                cls.__init__(self)

    def _search_capability(self, base):
        """Given a class, return a list of all of the derived classes that
        are themselves derived from Capability."""
        if _debug:
            Collector._debug('_search_capability %r', base)
        rslt = []
        for cls in base.__bases__:
            if issubclass(cls, Collector):
                map(rslt.append, self._search_capability(cls))
            elif issubclass(cls, Capability):
                rslt.append(cls)

        if _debug:
            Collector._debug('    - rslt: %r', rslt)
        return rslt

    def capability_functions(self, fn):
        """This generator yields functions that match the
        requested capability sorted by z-index."""
        if _debug:
            Collector._debug('capability_functions %r', fn)
        fns = []
        for cls in self.capabilities:
            xfn = getattr(cls, fn, None)
            if _debug:
                Collector._debug('    - cls, xfn: %r, %r', cls, xfn)
            if xfn:
                fns.append((getattr(cls, '_zindex', None), xfn))

        fns.sort(key=lambda v: v[0])
        if _debug:
            Collector._debug('    - fns: %r', fns)
        for xindx, xfn in fns:
            if _debug:
                Collector._debug('    - yield xfn: %r', xfn)
            yield xfn

        return

    def add_capability(self, cls):
        """Add a capability to this object."""
        if _debug:
            Collector._debug('add_capability %r', cls)
        bases = (
         self.__class__, cls)
        if _debug:
            Collector._debug('    - bases: %r', bases)
        self.capabilities.append(cls)
        newtype = type(self.__class__.__name__ + '+' + cls.__name__, bases, {})
        self.__class__ = newtype
        if hasattr(cls, '__init__'):
            if _debug:
                Collector._debug('    - calling %r.__init__', cls)
            cls.__init__(self)


@bacpypes_debugging
def compose_capability(base, *classes):
    """Create a new class starting with the base and adding capabilities."""
    if _debug:
        compose_capability._debug('compose_capability %r %r', base, classes)
    if not issubclass(base, Collector):
        raise TypeError('base must be a subclass of Collector')
    for cls in classes:
        if not issubclass(cls, Capability):
            raise TypeError('%s is not a Capability subclass' % (cls,))

    bases = (base,) + classes
    name = base.__name__
    for cls in classes:
        name += '+' + cls.__name__

    return type(name, bases, {})


@bacpypes_debugging
def add_capability(base, *classes):
    """Add capabilites to an existing base, all objects get the additional
    functionality, but don't get inited.  Use with great care!"""
    if _debug:
        add_capability._debug('add_capability %r %r', base, classes)
    if not issubclass(base, Collector):
        raise TypeError('base must be a subclass of Collector')
    for cls in classes:
        if not issubclass(cls, Capability):
            raise TypeError('%s is not a Capability subclass' % (cls,))

    base.__bases__ += classes
    for cls in classes:
        base.__name__ += '+' + cls.__name__