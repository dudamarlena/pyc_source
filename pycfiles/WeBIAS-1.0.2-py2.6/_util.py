# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/webias/gnosis/xml/pickle/util/_util.py
# Compiled at: 2015-04-13 16:10:48
import gnosis.xml.pickle
from types import *
import sys
CLASS_STORE = {}

class _EmptyClass:
    pass


dynamic_module = _EmptyClass().__class__.__module__

def dbg(s):
    pass


def get_function_info(func):
    fname = func.__name__
    for (name, module) in sys.modules.items():
        if name != '__main__' and hasattr(module, fname) and getattr(module, fname) is func:
            break
    else:
        name = '__main__'

    return (name, func.__name__)


def unpickle_function(module, name, paranoia):
    """Load a function, given module.name as returned by get_function_info()"""
    if paranoia > 0:
        return
    else:
        if paranoia < 0:
            __import__(module)
        mod = sys.modules.get(module, None)
        if mod is None:
            return
        if hasattr(mod, name):
            return getattr(mod, name)
        return


def _get_class_from_locals(dict, modname, classname):
    for name in dict.keys():
        if name == modname and type(dict[name]) is ModuleType:
            mod = dict[name]
            if hasattr(mod, classname):
                return getattr(mod, classname)
        if name == classname and dict[name].__module__ == modname:
            return dict[name]

    return


def get_class_from_sysmodules(modname, classname):
    """Get a class by looking in sys.modules"""
    try:
        return getattr(sys.modules[modname], classname)
    except (KeyError, AttributeError):
        return

    return


def get_class_from_stack(modname, classname):
    """Get a class ONLY IF already been imported or created by caller"""
    stk = _mini_getstack()
    for frame in stk:
        k = _get_class_from_locals(frame.f_locals, modname, classname)
        if k:
            return k


def get_class_full_search(modname, classname):
    """Get a class, importing if necessary"""
    __import__(modname)
    mod = sys.modules[modname]
    if hasattr(mod, classname):
        return getattr(mod, classname)
    else:
        return


def get_class_from_store(classname):
    """Get the class from the store, if possible"""
    return CLASS_STORE.get(classname, None) or gnosis.xml.pickle.__dict__.get(classname, None)


def add_class_to_store(classname='', klass=None):
    """Put the class in the store (as 'classname'), return CLASS_STORE"""
    if classname and klass:
        CLASS_STORE[classname] = klass
    return CLASS_STORE


def remove_class_from_store(classname):
    """Remove the classname from the store, return CLASS_STORE"""
    try:
        del CLASS_STORE[classname]
    except:
        pass

    return CLASS_STORE


def get_class_from_vapor(classname):
    """ Create new class from nothing"""
    exec 'class %s: pass' % classname
    k = locals()[classname]
    return k


from gnosis.util.introspect import instance_noinit

def obj_from_classtype(klass):
    """Create an object of ClassType klass. We aren't
    allowed (by the pickle protocol) to call __init__() on
    the new object, so we have to be careful."""
    return instance_noinit(klass)


def get_class_from_name(classname, modname=None, paranoia=1):
    """Given a classname, optional module name, return a ClassType,
    of type module.classname, obeying the PARANOIA rules."""
    if paranoia <= 2:
        klass = get_class_from_store(classname)
        if klass:
            dbg('**GOT CLASS FROM STORE**')
            return klass
    if paranoia <= 0 and modname:
        klass = get_class_from_sysmodules(modname, classname)
        if klass:
            dbg('**GOT CLASS FROM sys.modules**')
            return klass
    if paranoia <= 0 and modname:
        klass = get_class_from_stack(modname, classname)
        if klass:
            dbg('**GOT CLASS FROM STACK**')
            return klass
    if paranoia <= -1 and modname:
        klass = get_class_full_search(modname, classname)
        if klass:
            dbg('**GOT CLASS FROM CALLER**')
            return klass
    if paranoia <= 1:
        klass = get_class_from_vapor(classname)
        dbg('**GOT CLASS FROM VAPOR**')
        return klass
    dbg("**ERROR - couldn't get class - paranoia = %s" % str(paranoia))
    raise XMLUnpicklingError, 'Cannot create class under current PARANOIA setting!'


def obj_from_name(classname, modname=None, paranoia=1):
    """Given a classname, optional module name, return an object
    of type module.classname, obeying the PARANOIA rules.
    Does NOT call __init__ on the new object, since the caller
    may need to do some other preparation first."""
    dbg('OBJ FROM NAME %s.%s' % (str(modname), str(classname)))
    klass = get_class_from_name(classname, modname, paranoia)
    dbg('KLASS %s' % str(klass))
    return obj_from_classtype(klass)


def _klass(thing):
    return thing.__class__.__name__


def _module(thing):
    """If thing's class is located in CLASS_STORE, was created
    from "thin-air", or lives in the "xml_pickle" namespace,
    don't write the module name to the XML stream (without these
    checks, the XML is functional, but ugly -- module names like
    "gnosis.xml.pickle.util._util")
    """
    klass = thing.__class__
    if klass.__module__ == dynamic_module:
        return None
    else:
        if klass in CLASS_STORE.values():
            return None
        if klass in gnosis.xml.pickle.__dict__.values():
            return None
        return thing.__class__.__module__


def safe_eval(s):
    return eval(s)


def safe_string(s):
    if isinstance(s, UnicodeType):
        raise TypeError, 'Unicode strings may not be stored in XML attributes'
    s = s.replace('&', '&amp;')
    s = s.replace('<', '&lt;')
    s = s.replace('>', '&gt;')
    s = s.replace('"', '&quot;')
    s = s.replace("'", '&apos;')
    s = repr(s)
    return s[1:-1]


def unsafe_string(s):
    s = s.replace("'", '\\047')
    exec "s='" + s + "'"
    return s


def safe_content(s):
    """Markup XML entities and strings so they're XML & unicode-safe"""
    s = s.replace('&', '&amp;')
    s = s.replace('<', '&lt;')
    s = s.replace('>', '&gt;')
    if isinstance(s, StringType):
        s = '»»%s««' % s
    return s.encode('utf-8')


def unsafe_content(s):
    """Take the string returned by safe_content() and recreate the
    original string."""
    if s[:2] == unichr(187) * 2 and s[-2:] == unichr(171) * 2:
        s = s[2:-2].encode('us-ascii')
    return s


def subnodes(node):
    return filter(lambda n: hasattr(n, '_attrs') and n.nodeName != '#text', node.childNodes)


def _mini_getstack():
    frame = _mini_currentframe().f_back
    framelist = []
    while frame:
        framelist.append(frame)
        frame = frame.f_back

    return framelist


def _mini_currentframe():
    try:
        raise 'catch me'
    except:
        return sys.exc_traceback.tb_frame.f_back