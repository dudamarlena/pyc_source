# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/xooof/xmldispatcher/servers/tools/metaclass.py
# Compiled at: 2008-10-01 10:39:52
_impl_pfx = '_'

def _basecheck(base, mname):
    if base.__dict__.has_key(mname):
        return 1
    for basebase in base.__bases__:
        if _basecheck(basebase, mname):
            return 1

    return 0


def _check(clsdict, clsname, bases, mname):
    """Helper to check that the implementation method is present in the user class"""
    if clsdict.has_key(_impl_pfx + mname):
        return
    for base in bases:
        if _basecheck(base, _impl_pfx + mname):
            return

    raise RuntimeError('Xooof method implementation %s is missing in class %s and its base classes' % (_impl_pfx + mname, clsname))


def _add(clsdict, clsname, mname, mvalue):
    """Helper to add a xooof method to the user class"""
    if clsdict.has_key(mname):
        raise RuntimeError('Xooof method %s would hide user-provided attribute or method in class %s' % (mname, clsname))
    clsdict[mname] = mvalue


def _getXooofClass(clsdict, clsname):
    if clsdict.has_key('__xooofpackage__'):
        package = clsdict['__xooofpackage__']
        module = __import__(package.__name__ + '.' + clsname, globals(), locals(), [clsname])
        return getattr(module, clsname)
    elif clsdict.has_key('__xooofclass__'):
        return clsdict['__xooofclass__']
    else:
        raise RuntimeError('XooofMetaClass requires a __xooofpackage__ or __xooofclass__ class attribute to be defined')


class XooofMetaClass(type):
    """Metaclass to add xooof-specified behaviour to a user class

    The user class must have a __xooofclass__ attribute
    that specifies the xooof-generated class containing the
    specified behaviour (state machine, validation of request
    and replies). Alternatively, it can have a __xooofpackage__
    attribute referencing the package containing all the
    xooof-generated classes.

    This metaclass adds the xooof-generated behaviour and
    hides the user-provided implementations, to which the
    xooof-generated behaviour will delegate.
    """
    __module__ = __name__

    def __new__(cls, clsname, bases, clsdict):
        xooofClass = _getXooofClass(clsdict, clsname)
        xooofClassDict = xooofClass.__dict__
        try:
            fsm = xooofClass._fsm
        except AttributeError:
            fsm = None
        else:
            _add(clsdict, clsname, '_fsm', fsm)

        _add(clsdict, clsname, '_public_class_methods', xooofClassDict['_public_class_methods'])
        _add(clsdict, clsname, '_public_constructors', xooofClassDict['_public_constructors'])
        _add(clsdict, clsname, '_public_instance_methods', xooofClassDict['_public_instance_methods'])
        _add(clsdict, clsname, 'getClassInfo', xooofClassDict['getClassInfo'])
        ci = xooofClass.getClassInfo()
        for cm in ci.classmethods:
            if cm.name != 'getClassInfo':
                _check(clsdict, clsname, bases, cm.name)
            _add(clsdict, clsname, cm.name, xooofClassDict[cm.name])

        for im in ci.instancemethods:
            if im.special == 'constructor':
                _check(clsdict, clsname, bases, im.name)
            if fsm:
                for action in fsm.getActionsForEvent(im.name):
                    assert action.startswith(_impl_pfx)
                    _check(clsdict, clsname, bases, action[len(_impl_pfx):])

            elif im.special == 'constructor':
                _check(clsdict, clsname, bases, 'post' + im.name[0].upper() + im.name[1:])
            else:
                _check(clsdict, clsname, bases, im.name)
            _add(clsdict, clsname, im.name, xooofClassDict[im.name])

        return type.__new__(cls, clsname, bases, clsdict)