# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/webias/gnosis/xml/pickle/ext/_mutators.py
# Compiled at: 2015-04-13 16:10:46
from _mutate import XMLP_Mutator, XMLP_Mutated
import _mutate, sys, string
from types import *
from gnosis.util.introspect import isInstanceLike, attr_update, data2attr, attr2data, getCoreData, setCoreData, isinstance_any
from gnosis.xml.pickle.util import _klass, _module, obj_from_name
from gnosis.util.XtoY import aton
import gnosis.pyconfig

class _EmptyClass:
    pass


class mutate_builtin_wrapper(XMLP_Mutator):

    def __init__(self):
        XMLP_Mutator.__init__(self, None, 'builtin_wrapper')
        return

    def mutate(self, obj):
        wrap = _EmptyClass()
        wrap.__toplevel__ = obj
        return XMLP_Mutated(wrap)

    def unmutate(self, mobj):
        return mobj.obj.__toplevel__


_mutate.add_mutator(mutate_builtin_wrapper())
import array

class mutate_array(XMLP_Mutator):

    def __init__(self):
        XMLP_Mutator.__init__(self, array.ArrayType, 'array', 0)

    def mutate(self, obj):
        list = []
        for item in obj:
            list.append(item)

        return XMLP_Mutated(list)

    def unmutate(self, mobj):
        obj = mobj.obj
        as_int = 1
        for item in obj:
            if type(item) == type(1.0):
                as_int = 0

        if as_int:
            return array.array('b', obj)
        else:
            return array.array('d', obj)


_mutate.add_mutator(mutate_array())
try:
    import Numeric
    HAS_NUMERIC = 1
except:
    HAS_NUMERIC = 0

class mutate_numpy(XMLP_Mutator):

    def __init__(self):
        XMLP_Mutator.__init__(self, Numeric.ArrayType, 'NumPy_array', 0)

    def mutate(self, obj):
        list = []
        for item in obj:
            list.append(item)

        return XMLP_Mutated(list)

    def unmutate(self, mobj):
        return Numeric.array(mobj.obj)


if HAS_NUMERIC:
    _mutate.add_mutator(mutate_numpy())
import re
SRE_Pattern_type = type(re.compile(''))

class mutate_sre(XMLP_Mutator):

    def __init__(self):
        XMLP_Mutator.__init__(self, SRE_Pattern_type, 'SRE', paranoia=0, in_body=1)

    def mutate(self, obj):
        return XMLP_Mutated(obj.pattern)

    def unmutate(self, mobj):
        return re.compile(mobj.obj)


_mutate.add_mutator(mutate_sre())
try:
    import cPickle as pickle
except:
    import pickle

class mutate_rawpickle(XMLP_Mutator):

    def __init__(self):
        XMLP_Mutator.__init__(self, None, 'rawpickle', 0)
        return

    def mutate(self, obj):
        return XMLP_Mutated(pickle.dumps(obj))

    def unmutate(self, mobj):
        return pickle.loads(str(mobj.obj))


_mutate.add_mutator(mutate_rawpickle())
try:
    import mx.DateTime
    mxDateTime_type = type(mx.DateTime.localtime())
except:
    mxDateTime_type = None

class mutate_mxdatetime(XMLP_Mutator):

    def __init__(self):
        XMLP_Mutator.__init__(self, mxDateTime_type, 'mxDateTime', paranoia=0, in_body=1)

    def mutate(self, obj):
        s = 'YMD = %d/%d/%d, HMS = %d:%d:%.17g' % (
         obj.year, obj.month, obj.day,
         obj.hour, obj.minute, obj.second)
        return XMLP_Mutated(s)

    def unmutate(self, mobj):
        obj = mobj.obj
        fmt = 'YMD\\s*=\\s*([0-9]+)\\s*/\\s*([0-9]+)\\s*/\\s*([0-9]+)\\s*,\\s*'
        fmt += 'HMS\\s*=\\s*([0-9]+)\\s*:\\s*([0-9]+)\\s*:\\s*([0-9\\.]+)'
        m = re.match(fmt, obj)
        args = map(int, m.groups()[:5]) + [float(m.group(6))]
        return apply(mx.DateTime.DateTime, args)


if mxDateTime_type is not None:
    _mutate.add_mutator(mutate_mxdatetime())

def newdata_to_olddata(o):
    """Given o, an object subclassed from a builtin type with no attributes,
    return a tuple containing the raw data and a string containing
    a tag to save in the extra= field"""
    return (
     getCoreData(o), '%s %s' % (_module(o), _klass(o)))


def olddata_to_newdata(data, extra, paranoia):
    """Given raw data, the extra= tag, and paranoia setting,
    recreate the object that was passed to newdata_to_olddata."""
    (module, klass) = extra.split()
    o = obj_from_name(klass, module, paranoia)
    if isinstance_any(o, (IntType, FloatType, ComplexType, LongType)) and type(data) in [StringType, UnicodeType]:
        data = aton(data)
    o = setCoreData(o, data)
    return o


newinst_to_oldinst = data2attr
oldinst_to_newinst = attr2data

def hasPickleFuncs(obj):
    """Does obj define the special pickling functions?"""
    return hasattr(obj, '__getstate__') or hasattr(obj, '__setstate__') or hasattr(obj, '__getinitargs__')


class mutate_bltin_instances(XMLP_Mutator):

    def __init__(self):
        XMLP_Mutator.__init__(self, None, '__compound__', 0)
        return

    def mutate(self, obj):
        if isinstance(obj, UnicodeType):
            self.in_body = 1
        else:
            self.in_body = 0
        if isInstanceLike(obj) or hasPickleFuncs(obj):
            return XMLP_Mutated(newinst_to_oldinst(obj))
        else:
            (o, t) = newdata_to_olddata(obj)
            return XMLP_Mutated(o, t)

    def unmutate(self, mobj):
        obj = mobj.obj
        if not mobj.extra:
            return oldinst_to_newinst(obj)
        else:
            return olddata_to_newdata(obj, mobj.extra, self.paranoia)


if gnosis.pyconfig.Have_ObjectClass():
    _mutate.add_mutator(mutate_bltin_instances())