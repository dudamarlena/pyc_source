# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ZSI/generate/pyclass.py
# Compiled at: 2006-10-25 20:33:26
import pydoc, sys, warnings
from ZSI import TC

def _x():
    pass


try:
    _x.func_name = '_y'
except:
    raise RuntimeError, 'use python-2.4 or later, cannot set function names in python "%s"' % sys.version

del _x

class pyclass_type(type):
    """Stability: Unstable

    type for pyclasses used with typecodes.  expects the typecode to
    be available in the classdict.  creates python properties for accessing
    and setting the elements specified in the ofwhat list, and factory methods
    for constructing the elements.
    
    Known Limitations:
        1)Uses XML Schema element names directly to create method names, 
           using characters in this set will cause Syntax Errors:
        
              (NCNAME)-(letter U digit U "_")
    
    """

    def __new__(cls, classname, bases, classdict):
        """
        """
        typecode = classdict.get('typecode')
        assert typecode is not None, 'MUST HAVE A TYPECODE.'
        if len(bases) > 0:
            pass
        else:
            assert hasattr(typecode, 'ofwhat'), 'typecode has no ofwhat list??'
            assert hasattr(typecode, 'attribute_typecode_dict'), 'typecode has no attribute_typecode_dict??'
            if typecode.mixed:
                get, set = cls.__create_text_functions_from_what(typecode)
                if classdict.has_key(get.__name__):
                    raise AttributeError, 'attribute %s previously defined.' % get.__name__
                if classdict.has_key(set.__name__):
                    raise AttributeError, 'attribute %s previously defined.' % set.__name__
                classdict[get.__name__] = get
                classdict[set.__name__] = set
            for what in typecode.ofwhat:
                get, set, new_func = cls.__create_functions_from_what(what)
                if classdict.has_key(get.__name__):
                    raise AttributeError, 'attribute %s previously defined.' % get.__name__
                classdict[get.__name__] = get
                if classdict.has_key(set.__name__):
                    raise AttributeError, 'attribute %s previously defined.' % set.__name__
                classdict[set.__name__] = set
                if new_func is not None:
                    if classdict.has_key(new_func.__name__):
                        raise AttributeError, 'attribute %s previously defined.' % new_func.__name__
                    classdict[new_func.__name__] = new_func
                assert not classdict.has_key(what.pname), 'collision with pname="%s", bail..' % what.pname
                pname = what.pname
                if pname is None and isinstance(what, TC.AnyElement):
                    pname = 'any'
                assert pname is not None, 'Element with no name: %s' % what
                pname = pname[0].upper() + pname[1:]
                assert not pydoc.Helper.keywords.has_key(pname), 'unexpected keyword: %s' % pname
                classdict[pname] = property(get, set, None, 'property for element (%s,%s), minOccurs="%s" maxOccurs="%s" nillable="%s"' % (
                 what.nspname, what.pname, what.minOccurs, what.maxOccurs, what.nillable))

        if hasattr(typecode, 'attribute_typecode_dict'):
            attribute_typecode_dict = typecode.attribute_typecode_dict or {}
            for key, what in attribute_typecode_dict.items():
                get, set = cls.__create_attr_functions_from_what(key, what)
                if classdict.has_key(get.__name__):
                    raise AttributeError, 'attribute %s previously defined.' % get.__name__
                if classdict.has_key(set.__name__):
                    raise AttributeError, 'attribute %s previously defined.' % set.__name__
                classdict[get.__name__] = get
                classdict[set.__name__] = set

        return type.__new__(cls, classname, bases, classdict)

    def __create_functions_from_what(what):
        if not callable(what):

            def get(self):
                return getattr(self, what.aname)

            if what.maxOccurs > 1:

                def set(self, value):
                    if not (value is None or hasattr(value, '__iter__')):
                        raise TypeError, 'expecting an iterable instance'
                    setattr(self, what.aname, value)
                    return

            else:

                def set(self, value):
                    setattr(self, what.aname, value)

        else:

            def get(self):
                return getattr(self, what().aname)

            if what.maxOccurs > 1:

                def set(self, value):
                    if not (value is None or hasattr(value, '__iter__')):
                        raise TypeError, 'expecting an iterable instance'
                    setattr(self, what().aname, value)
                    return

            else:

                def set(self, value):
                    setattr(self, what().aname, value)

        if not callable(what) and getattr(what, 'pyclass', None) is None:
            new_func = None
        elif isinstance(what, TC.ComplexType) or isinstance(what, TC.Array):

            def new_func(self):
                """returns a mutable type
                """
                return what.pyclass()

        elif not callable(what):

            def new_func(self, value):
                """value -- initialize value
                returns an immutable type
                """
                return what.pyclass(value)

        elif issubclass(what.klass, TC.ComplexType) or issubclass(what.klass, TC.Array):

            def new_func(self):
                """returns a mutable type or None (if no pyclass).
                """
                p = what().pyclass
                if p is None:
                    return
                else:
                    return p()

        else:

            def new_func(self, value=None):
                """if simpleType provide initialization value, else
                if complexType value should be left as None.
                Parameters:
                    value -- initialize value or None
                    
                returns a mutable instance (value is None) 
                    or an immutable instance or None (if no pyclass)
                """
                p = what().pyclass
                if p is None:
                    return
                else:
                    if value is None:
                        return p()
                    return p(value)

        if new_func is not None:
            new_func.__name__ = 'new_%s' % what.pname
        get.func_name = 'get_element_%s' % what.pname
        set.func_name = 'set_element_%s' % what.pname
        return (get, set, new_func)

    __create_functions_from_what = staticmethod(__create_functions_from_what)

    def __create_attr_functions_from_what(key, what):

        def get(self):
            'returns attribute value for attribute %s, else None.\n            ' % str(key)
            return getattr(self, what.attrs_aname, {}).get(key, None)

        def set(self, value):
            'set value for attribute %s.\n            value -- initialize value, immutable type\n            ' % str(key)
            if not hasattr(self, what.attrs_aname):
                setattr(self, what.attrs_aname, {})
            getattr(self, what.attrs_aname)[key] = value

        if type(key) in (tuple, list):
            get.__name__ = 'get_attribute_%s' % key[1]
            set.__name__ = 'set_attribute_%s' % key[1]
        else:
            get.__name__ = 'get_attribute_%s' % key
            set.__name__ = 'set_attribute_%s' % key
        return (get, set)

    __create_attr_functions_from_what = staticmethod(__create_attr_functions_from_what)

    def __create_text_functions_from_what(what):

        def get(self):
            """returns text content, else None.
            """
            return getattr(self, what.mixed_aname, None)

        get.im_func = 'get_text'

        def set(self, value):
            """set text content.
            value -- initialize value, immutable type
            """
            setattr(self, what.mixed_aname, value)

        get.im_func = 'set_text'
        return (
         get, set)

    __create_text_functions_from_what = staticmethod(__create_text_functions_from_what)