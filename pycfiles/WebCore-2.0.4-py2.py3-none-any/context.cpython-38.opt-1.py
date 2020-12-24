# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /web/core/context.py
# Compiled at: 2020-05-11 19:05:16
# Size of source mod 2**32: 4200 bytes
"""A `MutableMapping` subclass for use as a request-local context object."""
from __future__ import unicode_literals
from collections import MutableMapping

class Context(MutableMapping):
    __doc__ = 'An attribute access dictionary, of a kind.\n\t\n\tThis utility class is used to cooperatively construct the ApplicationContext (and subsequent RequestContext)\n\tfrom the contributions of multiple extensions. The concept of "promotion to a class" is needed in order to enable\n\tthe use of descriptor protocol attributes; without promotion the protocol would not be utilized.\n\t'

    def _promote(self, name, instantiate=True):
        """Create a new subclass of Context which incorporates instance attributes and new descriptors.
                
                This promotes an instance and its instance attributes up to being a class with class attributes, then
                returns an instance of that class.
                """
        metaclass = type(self.__class__)
        contents = self.__dict__.copy()
        cls = metaclass(str(name), (self.__class__,), contents)
        if instantiate:
            return cls()
        return cls

    def __init__(self, **kw):
        self.__dict__.update(kw)
        super(Context, self).__init__()

    def __len__(self):
        """Get a list of the public data attributes."""
        return len([i for i in set(dir(self)) - self._STANDARD_ATTRS if i[0] != '_'])

    def __iter__(self):
        """Iterate all valid (public) attributes/keys."""
        return (i for i in set(dir(self)) - self._STANDARD_ATTRS if i[0] != '_')

    def __getitem__--- This code section failed: ---

 L.  57         0  SETUP_FINALLY        14  'to 14'

 L.  58         2  LOAD_GLOBAL              getattr
                4  LOAD_FAST                'self'
                6  LOAD_FAST                'name'
                8  CALL_FUNCTION_2       2  ''
               10  POP_BLOCK        
               12  RETURN_VALUE     
             14_0  COME_FROM_FINALLY     0  '0'

 L.  59        14  DUP_TOP          
               16  LOAD_GLOBAL              AttributeError
               18  COMPARE_OP               exception-match
               20  POP_JUMP_IF_FALSE    32  'to 32'
               22  POP_TOP          
               24  POP_TOP          
               26  POP_TOP          

 L.  60        28  POP_EXCEPT       
               30  JUMP_FORWARD         34  'to 34'
             32_0  COME_FROM            20  '20'
               32  END_FINALLY      
             34_0  COME_FROM            30  '30'

 L.  63        34  LOAD_GLOBAL              KeyError
               36  LOAD_FAST                'name'
               38  CALL_FUNCTION_1       1  ''
               40  RAISE_VARARGS_1       1  'exception instance'

Parse error at or near `POP_TOP' instruction at offset 24

    def __setitem__(self, name, value):
        """Assign an attribute through dictionary access."""
        setattr(self, name, value)

    def __delitem__--- This code section failed: ---

 L.  71         0  SETUP_FINALLY        14  'to 14'

 L.  72         2  LOAD_GLOBAL              delattr
                4  LOAD_FAST                'self'
                6  LOAD_FAST                'name'
                8  CALL_FUNCTION_2       2  ''
               10  POP_BLOCK        
               12  RETURN_VALUE     
             14_0  COME_FROM_FINALLY     0  '0'

 L.  73        14  DUP_TOP          
               16  LOAD_GLOBAL              AttributeError
               18  COMPARE_OP               exception-match
               20  POP_JUMP_IF_FALSE    32  'to 32'
               22  POP_TOP          
               24  POP_TOP          
               26  POP_TOP          

 L.  74        28  POP_EXCEPT       
               30  JUMP_FORWARD         34  'to 34'
             32_0  COME_FROM            20  '20'
               32  END_FINALLY      
             34_0  COME_FROM            30  '30'

 L.  77        34  LOAD_GLOBAL              KeyError
               36  LOAD_FAST                'name'
               38  CALL_FUNCTION_1       1  ''
               40  RAISE_VARARGS_1       1  'exception instance'

Parse error at or near `POP_TOP' instruction at offset 24


Context._STANDARD_ATTRS = set(dir(Context()))

class ContextGroup(Context):
    __doc__ = 'A managed group of related context additions.\n\t\n\tThis proxies most attribute access through to the "default" group member.\n\t\n\tBecause of the possibility of conflicts, all attributes are accessible through dict-like subscripting.\n\t\n\tRegister new group members through dict-like subscript assignment as attribute assignment is passed through to the\n\tdefault handler if assigned.\n\t'
    default = None

    def __init__(self, default=None, **kw):
        if default is not None:
            self.default = default
            default.__name__ = 'default'
        for name in kw:
            kw[name].__name__ = name
            self.__dict__[name] = kw[name]

    def __repr__(self):
        return '{0.__class__.__name__}({1})'.format(self, ', '.join(sorted(self)))

    def __len__(self):
        return len(self.__dict__)

    def __iter__(self):
        return iter(set(dir(self)) - self._STANDARD_ATTRS)

    def __getitem__--- This code section failed: ---

 L. 117         0  SETUP_FINALLY        14  'to 14'

 L. 118         2  LOAD_GLOBAL              getattr
                4  LOAD_FAST                'self'
                6  LOAD_FAST                'name'
                8  CALL_FUNCTION_2       2  ''
               10  POP_BLOCK        
               12  RETURN_VALUE     
             14_0  COME_FROM_FINALLY     0  '0'

 L. 119        14  DUP_TOP          
               16  LOAD_GLOBAL              AttributeError
               18  COMPARE_OP               exception-match
               20  POP_JUMP_IF_FALSE    32  'to 32'
               22  POP_TOP          
               24  POP_TOP          
               26  POP_TOP          

 L. 120        28  POP_EXCEPT       
               30  JUMP_FORWARD         34  'to 34'
             32_0  COME_FROM            20  '20'
               32  END_FINALLY      
             34_0  COME_FROM            30  '30'

 L. 122        34  LOAD_GLOBAL              KeyError
               36  CALL_FUNCTION_0       0  ''
               38  RAISE_VARARGS_1       1  'exception instance'

Parse error at or near `POP_TOP' instruction at offset 24

    def __setitem__(self, name, value):
        self.__dict__[name] = value

    def __delitem__(self, name):
        del self.__dict__[name]

    def __getattr__(self, name):
        if self.default is None:
            raise AttributeError()
        return getattr(self.default, name)

    def __setattr__(self, name, value):
        if self.default is not None:
            return setattr(self.default, name, value)
        self.__dict__[name] = value

    def __delattr__(self, name):
        if self.default is not None:
            return delattr(self.default, name)
        self.__dict__[name] = None
        del self.__dict__[name]


ContextGroup._STANDARD_ATTRS = set(dir(ContextGroup()))