# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib64/python3.6/site-packages/ioflo/base/registering.py
# Compiled at: 2017-12-17 08:35:26
# Size of source mod 2**32: 4923 bytes
"""registering.py support functions and classes

"""
import random
from ..aid.sixing import *
from ..aid.odicting import odict
from . import excepting
from ..aid.aiding import reverseCamel
from ..aid.consoling import getConsole
console = getConsole()

class RegisterType(type):
    __doc__ = ' Metaclass that registers all subclasses '

    def __init__(cls, name, bases, attrs):
        super(RegisterType, cls).__init__(name, bases, attrs)
        if not hasattr(cls, 'Registry'):
            cls.Registry = odict()
        cls.__register__(name, inits=(getattr(cls, 'Inits', None)),
          ioinits=(getattr(cls, 'Ioinits', None)),
          parms=(getattr(cls, 'Parms', None)))

    def __register__(cls, name, inits=None, ioinits=None, parms=None):
        """ Register class cls under name with ioinits and inits

            Usage:  A.__register__(name, ioinits, inits, parms)
        """
        if name in cls.Registry:
            msg = "Entry '{0}' already exists in registry of {1}".format(name, cls)
            raise excepting.RegisterError(msg)
        cls.Registry[name] = (
         cls, inits, ioinits, parms)
        console.profuse("Registered: '{0}'\n".format(name))
        return cls

    def __fetch__(cls, name):
        """ Return tuple derived from .Registry entry at rname if present
            Otherwise raise exception
            Makes copies of inits and ioinits so safe for downstream use
        """
        if name not in cls.Registry:
            msg = "Entry '{0}' not found in Registry of '{1}'".format(name, cls.__name__)
            raise excepting.RegisterError(msg)
        actor, inits, ioinits, parms = cls.Registry[name]
        return (actor,
         odict(inits or odict()),
         odict(ioinits or odict()),
         odict(parms or odict()))


class Registrar(object):
    __doc__ = 'Class that ensures every instance has a unique name\n       uses class variable Counter and  Names dictionary\n    '
    __slots__ = ('name', )
    Counter = 0
    Names = {}

    def __init__(self, name='', preface='', **kw):
        """Initializer method for instance.

           instance attributes
           .name = unique name for instance

        """
        self.__class__.Counter += 1
        if not preface:
            preface = self.__class__.__name__
        if not isinstance(name, str):
            raise excepting.ParameterError('Expected str instance', 'name', name)
        if not name:
            name = str(preface) + str(self.__class__.Counter)
            while name in self.__class__.Names:
                name += chr(ord('a') + random.randint(0, 25))

        else:
            if name in self.__class__.Names:
                raise excepting.ParameterError('Instance name attribute not unique', 'name', name)
        self.name = name
        self.__class__.Names[self.name] = self

    @classmethod
    def Clear(cls):
        """clears (empties) registry of Names and resets Counter to 0

        """
        cls.Names = {}
        cls.Counter = 0

    @classmethod
    def VerifyName(cls, name=''):
        """verifies that name would be unique non empty string for instance name

           return False if empty or if already in Names , True otherwise
        """
        if not isinstance(name, str):
            return False
        else:
            if not name or name in cls.Names:
                return False
            return True

    @classmethod
    def Retrieve(cls, name=''):
        """Retrieves object in registry with name

           return object with name or  False if no object by name
        """
        return cls.Names.get(name, None)


class StoriedRegistrar(Registrar):
    __doc__ = 'Adds store attribute to Registry instances\n    '
    __slots__ = ('store', )

    def __init__(self, store=None, **kw):
        """Initializer method for instance.
           Inherited instance attributes:
           .name

           New instance attributes
           .store = reference to shared data store

        """
        (super(StoriedRegistrar, self).__init__)(**kw)
        self.changeStore(store=store)

    def changeStore(self, store=None):
        """Replace .store """
        from . import storing
        if store is not None:
            if not isinstance(store, storing.Store):
                raise ValueError('Not store %s' % store)
        self.store = store