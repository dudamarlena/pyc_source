# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\pydrizzle\traits102\trait_base.py
# Compiled at: 2014-04-16 13:17:36
from __future__ import division
from types import ListType, TupleType, StringType, UnicodeType, IntType, LongType, FloatType, ComplexType, BooleanType
import sys
SequenceTypes = (
 ListType, TupleType)
TraitNotifier = '__trait_notifier__'

class UndefinedObject:

    def __repr__(self):
        return '<undefined>'


class SelfObject:

    def __repr__(self):
        return '<self>'


Undefined = UndefinedObject()
Self = SelfObject()

def strx(arg):
    if type(arg) in StringTypes:
        return str(arg)
    raise TypeError


def unicodex(arg):
    if type(arg) in StringTypes:
        return unicode(arg)
    raise TypeError


def intx(arg):
    try:
        return int(arg)
    except:
        try:
            return int(float(arg))
        except:
            return int(long(arg))


def longx(arg):
    try:
        return long(arg)
    except:
        return long(float(arg))


def floatx(arg):
    try:
        return float(arg)
    except:
        return float(long(arg))


def complexx(arg):
    try:
        return complex(arg)
    except:
        return complex(long(arg))


def booleanx(arg):
    if arg:
        return True
    return False


NumericFuncs = {IntType: (intx, 'an integer'), LongType: (
            longx, 'a long integer'), 
   FloatType: (
             floatx, 'a floating point number')}
StringTypes = (
 StringType, UnicodeType, IntType, LongType, FloatType,
 ComplexType)
CoercableFuncs = {IntType: intx, LongType: longx, 
   FloatType: floatx, 
   ComplexType: complexx, 
   StringType: strx, 
   UnicodeType: unicodex, 
   BooleanType: booleanx}
trait_editors_module = None
trait_editors_module_name = None

def trait_editors(module_name=None):
    global trait_editors_module
    global trait_editors_module_name
    if module_name is not None:
        if module_name != trait_editors_module_name:
            trait_editors_module_name = module_name
            trait_editors_module = None
        return
    traits_prefix = 'enthought.traits'
    for key in sys.modules.keys():
        if key.find('.traits') > -1:
            traits_prefix = key

    if trait_editors_module is None:
        if trait_editors_module_name is None:
            try:
                __import__('wxPython')
                trait_editors_module_name = traits_prefix[:-6] + 'wxtrait_sheet'
            except ImportError:
                try:
                    __import__('Tkinter')
                    trait_editors_module_name = traits_prefix[:-6] + 'tktrait_sheet'
                except ImportError:
                    return

        try:
            trait_editors_module = sys.modules[trait_editors_module_name]
        except:
            try:
                trait_editors_module = __import__(trait_editors_module_name)
                for item in trait_editors_module_name.split('.')[1:]:
                    trait_editors_module = getattr(trait_editors_module, item)

            except ImportError:
                trait_editors_module = None

    return trait_editors_module


def class_of(object):
    if type(object) is StringType:
        name = object
    else:
        name = object.__class__.__name__
    if name[:1].lower() in 'aeiou':
        return 'an ' + name
    return 'a ' + name