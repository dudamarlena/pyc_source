# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/webias/gnosis/xml/pickle/ext/_mutate.py
# Compiled at: 2015-04-13 16:10:46
from types import *
from gnosis.util.introspect import isInstanceLike, hasCoreData
import gnosis.pyconfig
XMLPicklingError = 'gnosis.xml.pickle.XMLPicklingError'
XMLUnpicklingError = 'gnosis.xml.pickle.XMLUnpicklingError'
_mutators_by_classtype = {}
_unmutators_by_tag = {}

def __disable_extensions():
    global _mutators_by_classtype
    _mutators_by_classtype = {}
    for tag in _unmutators_by_tag.keys():
        if tag != 'rawpickle':
            del _unmutators_by_tag[tag]


_has_coredata_cache = {}
if gnosis.pyconfig.Have_BoolClass() and gnosis.pyconfig.IsLegal_BaseClass('bool'):
    raise XMLPicklingError, 'Assumption broken - can now use bool as baseclass!'
Have_BoolClass = gnosis.pyconfig.Have_BoolClass()

def get_mutator(obj):
    mlist = _mutators_by_classtype.get(type(obj)) or []
    for mutator in mlist:
        if mutator.wants_obj(obj):
            return mutator

    if Have_BoolClass and type(obj) is BooleanType:
        return
    else:
        if not hasattr(obj, '__class__'):
            return
        if _has_coredata_cache.has_key(obj.__class__):
            return _has_coredata_cache[obj.__class__]
        if hasCoreData(obj):
            _has_coredata_cache[obj.__class__] = get_unmutator('__compound__', None)
            return get_unmutator('__compound__', None)
        _has_coredata_cache[obj.__class__] = None
        return


def can_mutate(obj):
    if get_mutator(obj):
        return 1
    else:
        return 0


def mutate(obj):
    mutator = get_mutator(obj)
    tobj = mutator.mutate(obj)
    if not isinstance(tobj, XMLP_Mutated):
        raise XMLPicklingError, 'Bad type returned from mutator %s' % mutator
    return (mutator.tag, tobj.obj, mutator.in_body, tobj.extra)


def try_mutate(obj, alt_tag, alt_in_body, alt_extra):
    mutator = get_mutator(obj)
    if mutator is None:
        return (alt_tag, obj, alt_in_body, alt_extra)
    else:
        tobj = mutator.mutate(obj)
        if not isinstance(tobj, XMLP_Mutated):
            raise XMLPicklingError, 'Bad type returned from mutator %s' % mutator
        return (mutator.tag, tobj.obj, mutator.in_body, tobj.extra)


def get_unmutator(tag, obj):
    list = _unmutators_by_tag.get(tag) or []
    for unmutator in list:
        if unmutator.wants_mutated(obj):
            return unmutator

    return


def can_unmutate(tag, obj):
    if get_unmutator(tag, obj):
        return 1
    else:
        return 0


def unmutate(tag, obj, paranoia, mextra):
    unmutator = get_unmutator(tag, obj)
    return unmutator.unmutate(XMLP_Mutated(obj, mextra))


def add_mutator(xmlp_mutator):
    """Register an XMLP_Mutator object"""
    if xmlp_mutator.class_type:
        try:
            _mutators_by_classtype[xmlp_mutator.class_type].insert(0, xmlp_mutator)
        except:
            _mutators_by_classtype[xmlp_mutator.class_type] = [
             xmlp_mutator]

    try:
        _unmutators_by_tag[xmlp_mutator.tag].insert(0, xmlp_mutator)
    except:
        _unmutators_by_tag[xmlp_mutator.tag] = [
         xmlp_mutator]


def remove_mutator(xmlp_mutator):
    """De-register an XMLP_Mutator object"""
    list = _unmutators_by_tag[xmlp_mutator.tag]
    list.remove(xmlp_mutator)
    list = _mutators_by_classtype[xmlp_mutator.class_type]
    list.remove(xmlp_mutator)


class XMLP_Mutated:
    """This is the type that XMLP_Mutator.mutate() returns.
    Having this as a distinct type will make it easy to add flags,
    etc., in the future without breaking existing mutators.
    In most cases, you just wrap your mutated obj like this:
        return XMLP_Mutated( obj )"""

    def __init__(self, obj, extra=None):
        self.obj = obj
        self.extra = extra


class XMLP_Mutator:
    """Parent class for XMLP Mutators"""

    def __init__(self, class_type, tag, paranoia=1, in_body=0):
        """
        class_type = type() that this mutator handles
        tag = Symbolic tag for what this mutator produces
        paranoia = Maximum PARANOIA level at which to enable this
                   mutator (note that PARANOIA for mutators is a
                   static concept - it doesn't matter which
                   namespace we're in, etc. Each mutator is instead
                   judged to be "safe" at a given level based on
                   what the datatype can do).
        in_body = (Applicable only for types that mutate to a string or
                   numeric type.)
                  If in_body == 0, pickled text is placed in the value= attr.
                  If in_body == 1, pickled text is placed in the element body.
        """
        self.class_type = class_type
        self.tag = tag
        self.paranoia = paranoia
        self.in_body = in_body

    def wants_obj(self, obj):
        return 1

    def wants_mutated(self, mobj):
        """obj is of type XMLP_Mutated"""
        return 1

    def mutate(self, obj):
        """given obj, return an XMLP_Mutated object, where the
        XMLP_Mutated.obj member is a basic type (string,numeric,
        assoc,seq,or PyObject)"""
        raise NotImplementedError

    def unmutate(self, mobj):
        """take an XMLP_Mutated obj and recreate the original object"""
        raise NotImplementedError