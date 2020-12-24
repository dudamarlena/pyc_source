# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/prototype.py
# Compiled at: 2011-05-24 15:25:18
__doc__ = '\nprototype - A tiny python library that simulates prototype inheritence in javascript\n\n# create a new type using @constructor\n>>> from prototype import *\n>>> @constructor\n... def Person(this, first, last):\n...   this.firstName = first\n...   this.lastName = last\n...\n>>> Person\n<constructor \'Person\'>\n\n# initialize an instance\n>>> bird = Person(\'Charlie\', \'Parker\')\n>>> bird.firstName\n\'Charlie\'\n>>> bird.lastName\n\'Parker\'\n\n# dynamically add attributes\n>>> bird.instrument = \'alto sax\'\n>>> bird.instrument\n\'alto sax\'\n\n# unset attributes raise an AttributeError exception\n>>> print bird.age\nTraceback (most recent call last):\n  File "<stdin>", line 1, in <module>\n  File "prototype.py", line 148, in __getattribute__\n    val = _proto_getattr(this, name)\n  File "prototype.py", line 127, in _proto_getattr\n    return _getattr(obj, name)\n  File "prototype.py", line 118, in _getattr\n    return object.__getattribute__(obj, name)\nAttributeError: \'Object\' object has no attribute \'age\'\n\n# add methods to the instance\n>>> def sing(this):\n...   print \'%s sings!!\' % this.lastName\n...\n>>> bird.sing = sing\n>>> bird.sing()\nParker sings!!\n\n# use the prototype chain to add properties and methods to the type\n>>> def getName(this):\n...   return \'%s %s\' % (this.firstName, this.lastName)\n...\n>>> Person.prototype.name = property(getName)\n>>> bird.name\n\'Charlie Parker\'\n>>> def greet(this):\n...   print \'Hello, my name is %s\' % this.name\n...\n>>> Person.prototype.greet = greet\n>>> bird.greet()\nHello, my name is Charlie Parker\n>>> monk = Person(\'Thelonious\', \'Monk\')\n>>> monk.greet()\nHello, my name is Thelonious Monk\n\n# property setter\n>>> def setName(this, name):\n...   first, last = name.split(\' \')\n...   this.firstName = first\n...   this.lastName = last\n...\n>>> Person.prototype.name = property(getName, setName)\n>>> bird.name = \'Dizzy Gillespie\'\n>>> bird.firstName\n\'Dizzy\'\n>>> bird.lastName\n\'Gillespie\'\n\n# property deleter\n>>> def deleteName(this):\n...   print \'Deleting %s.\' % this.name\n...   del this.firstName\n...   del this.lastName\n...\n>>> Person.prototype.name = property(getName, setName, deleteName)\n>>> del bird.name\nDeleting Dizzy Gillespie.\n>>> bird.name\nTraceback (most recent call last):\n  File "/usr/lib64/python2.6/doctest.py", line 1241, in __run\n    compileflags, 1) in test.globs\n  File "<doctest prototype[28]>", line 1, in <module>\n    bird.name\n  File "/backup/Projects/python-prototype/prototype.py", line 159, in __getattribute__\n    return get()\n  File "<doctest prototype[12]>", line 2, in getName\n    return \'%s %s\' % (this.firstName, this.lastName)\n  File "/backup/Projects/python-prototype/prototype.py", line 156, in __getattribute__\n    val = _proto_getattr(this, name)\n  File "/backup/Projects/python-prototype/prototype.py", line 135, in _proto_getattr\n    return _getattr(obj, name)\n  File "/backup/Projects/python-prototype/prototype.py", line 126, in _getattr\n    return object.__getattribute__(obj, name)\nAttributeError: \'Object\' object has no attribute \'firstName\'\n\n# using prototype inheritence\n>>> father = Person(\'Tom\', \'Bard\')\n>>> son = Person(\'Tommy\', \'Bard\')\n>>> son.__proto__ = father\n>>> father.eyeColor = \'blue\'\n>>> son.eyeColor\n\'blue\'\n\n# prototype chain relationships\n>>> assert son.__proto__ == father\n>>> assert son.constructor == father.constructor == Person\n>>> assert father.__proto__ == Person.prototype\n>>> assert Object.prototype.constructor == Object\n>>> assert Person.prototype.constructor == Person\n>>> assert Person.prototype.__proto__ == Object.prototype\n\n# should work with lists\n>>> father.children = [son]\n>>> len(father.children)\n1\n\n# multi-level inheritence\n>>> grandson = Person(\'Tony\', \'Bard\')\n>>> grandson.__proto__ = son\n>>> grandson.eyeColor\n\'blue\'\n'
import new, inspect

def _getattr(obj, name):
    return object.__getattribute__(obj, name)


def _setattr(obj, name, val):
    object.__setattr__(obj, name, val)


def _proto_getattr(obj, name):
    while True:
        try:
            return _getattr(obj, name)
        except AttributeError:
            obj = _getattr(obj, '__proto__')
            if obj is None:
                raise

    return


class ObjectMetaClass(type):

    def __repr__(cls):
        return "<constructor '%s'>" % cls.__name__


class Object(object):
    __metaclass__ = ObjectMetaClass
    prototype = None
    __proto__ = None
    constructor = None

    def __init__(this):
        this.__proto__ = this.prototype
        this.constructor = this.__class__

    def __getattribute__(this, name):
        val = _proto_getattr(this, name)
        if isinstance(val, property) and val.fget:
            get = new.instancemethod(val.fget, this)
            return get()
        else:
            if inspect.isfunction(val):
                func = new.instancemethod(val, this)
                return func
            return val

    def __setattr__(this, name, val):
        if not isinstance(val, property):
            try:
                _val = _proto_getattr(this, name)
            except AttributeError:
                pass
            else:
                if isinstance(_val, property) and _val.fset:
                    _val.fset(this, val)
                    return
        _setattr(this, name, val)

    def __delattr__(this, name):
        try:
            val = _proto_getattr(this, name)
        except AttributeError:
            pass
        else:
            if isinstance(val, property) and val.fdel:
                val.fdel(this)
                return

        object.__delattr__(this, name)


Object.prototype = Object()

def constructor(func):
    ret = type(func.__name__, (Object,), dict())
    ret.prototype = ret()

    def init(this, *vargs, **kwargs):
        Object.__init__(this)
        func(this, *vargs, **kwargs)

    ret.__init__ = init
    return ret