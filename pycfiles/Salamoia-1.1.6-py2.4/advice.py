# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/salamoia/nacl/advice.py
# Compiled at: 2007-12-02 16:26:59
"""Class advice.

This module was adapted from 'protocols.advice', part of the Python
Enterprise Application Kit (PEAK).  Please notify the PEAK authors
(pje@telecommunity.com and tsarna@sarna.org) if bugs are found or
Zope-specific changes are required, so that the PEAK version of this module
can be kept in sync.

PEAK is a Python application framework that interoperates with (but does
not require) Zope 3 and Twisted.  It provides tools for manipulating UML
models, object-relational persistence, aspect-oriented programming, and more.
Visit the PEAK home page at http://peak.telecommunity.com for more information.

$Id: advice.py 25177 2004-06-02 13:17:31Z jim $
"""
from types import ClassType, FunctionType
import sys

def getFrameInfo(frame):
    """Return (kind,module,locals,globals) for a frame

    'kind' is one of "exec", "module", "class", "function call", or "unknown".
    """
    f_locals = frame.f_locals
    f_globals = frame.f_globals
    sameNamespace = f_locals is f_globals
    hasModule = '__module__' in f_locals
    hasName = '__name__' in f_globals
    sameName = hasModule and hasName
    sameName = sameName and f_globals['__name__'] == f_locals['__module__']
    module = hasName and sys.modules.get(f_globals['__name__']) or None
    namespaceIsModule = module and module.__dict__ is f_globals
    if not namespaceIsModule:
        kind = 'exec'
    elif sameNamespace and not hasModule:
        kind = 'module'
    elif sameName and not sameNamespace:
        kind = 'class'
    elif not sameNamespace:
        kind = 'function call'
    else:
        kind = 'unknown'
    return (
     kind, module, f_locals, f_globals)


def addClassAdvisor(callback, depth=2):
    """Set up 'callback' to be passed the containing class upon creation

    This function is designed to be called by an "advising" function executed
    in a class suite.  The "advising" function supplies a callback that it
    wishes to have executed when the containing class is created.  The
    callback will be given one argument: the newly created containing class.
    The return value of the callback will be used in place of the class, so
    the callback should return the input if it does not wish to replace the
    class.

    The optional 'depth' argument to this function determines the number of
    frames between this function and the targeted class suite.  'depth'
    defaults to 2, since this skips this function's frame and one calling
    function frame.  If you use this function from a function called directly
    in the class suite, the default will be correct, otherwise you will need
    to determine the correct depth yourself.

    This function works by installing a special class factory function in
    place of the '__metaclass__' of the containing class.  Therefore, only
    callbacks *after* the last '__metaclass__' assignment in the containing
    class will be executed.  Be sure that classes using "advising" functions
    declare any '__metaclass__' *first*, to ensure all callbacks are run."""
    frame = sys._getframe(depth)
    (kind, module, caller_locals, caller_globals) = getFrameInfo(frame)
    previousMetaclass = caller_locals.get('__metaclass__')
    defaultMetaclass = caller_globals.get('__metaclass__', ClassType)

    def advise(name, bases, cdict):
        if '__metaclass__' in cdict:
            del cdict['__metaclass__']
        if previousMetaclass is None:
            if bases:
                meta = determineMetaclass(bases)
            else:
                meta = defaultMetaclass
        elif isClassAdvisor(previousMetaclass):
            meta = previousMetaclass
        else:
            meta = determineMetaclass(bases, previousMetaclass)
        newClass = meta(name, bases, cdict)
        return callback(newClass)

    advise.previousMetaclass = previousMetaclass
    advise.callback = callback
    caller_locals['__metaclass__'] = advise


def isClassAdvisor(ob):
    """True if 'ob' is a class advisor function"""
    return isinstance(ob, FunctionType) and hasattr(ob, 'previousMetaclass')


def determineMetaclass(bases, explicit_mc=None):
    """Determine metaclass from 1+ bases and optional explicit __metaclass__"""
    meta = [ getattr(b, '__class__', type(b)) for b in bases ]
    if explicit_mc is not None:
        meta.append(explicit_mc)
    if len(meta) == 1:
        return meta[0]
    candidates = minimalBases(meta)
    if not candidates:
        return ClassType
    elif len(candidates) > 1:
        raise TypeError('Incompatible metatypes', bases)
    return candidates[0]


def minimalBases(classes):
    """Reduce a list of base classes to its ordered minimum equivalent"""
    classes = [ c for c in classes if c is not ClassType ]
    candidates = []
    for m in classes:
        for n in classes:
            if issubclass(n, m) and m is not n:
                break
        else:
            if m in candidates:
                candidates.remove(m)
            candidates.append(m)

    return candidates


from salamoia.tests import *
runDocTests()