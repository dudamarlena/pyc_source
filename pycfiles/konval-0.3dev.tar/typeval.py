# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/f0/paul/Projects/Py-konval/konval/konval/typeval.py
# Compiled at: 2011-08-02 10:00:49
"""
Validators that confirm or convert types.

"""
__docformat__ = 'restructuredtext en'
from basevalidator import BaseValidator
import impl, defs
from vocabval import ToSynonym

class ToType(BaseValidator):
    """
        Convert a value to a given type.
        
        This is largely syntactic sugar: It will actually accept any callable as an
        argument, but is intended for use with class constructors. You could use
        raw types and classes, but this throws much nicer error messages. Conversion
        is done by simply passing a value to the parameter callable.
        
        """

    def __init__(self, to_type, type_name=None):
        """
                Class c'tor, accepting a type.
                
                :Parameters:
                        to_type : callable
                                A class constructor (old or new style), built-in type, or function
                                that can be called to convert a type and will throw if it fails.
                        type_name : string
                                A name for the type produced. If not supplied, it will be extracted
                                from `to_type` if possible.
                                
                For example::
                
                        >>> v = ToType(int, type_name='an integer')
                        >>> v(1)
                        1
                        >>> v(2.3)
                        2
                        >>> v('foo')
                        Traceback (most recent call last):
                        ...
                        ValueError: can't convert 'foo' to an integer
                        >>> v = ToType(float)
                        >>> v('foo')
                        Traceback (most recent call last):
                        ...
                        ValueError: can't convert 'foo' to float
                
                """
        self.to_type = to_type
        if type_name is None:
            if hasattr(to_type, '__name__'):
                type_name = getattr(to_type, '__name__')
            assert type_name not in (None, '<lambda>'), 'type validator requires type name for lambda'
        self.type_name = type_name
        return

    def make_conversion_error_msg(self, bad_val, err):
        """
                Generate an appropriate error message for type conversion problem.
                """
        return "can't convert '%s' to %s" % (bad_val, self.type_name)

    def convert_value(self, value):
        return self.to_type(value)


class ToInt(ToType):
    """
        Convert a value to an integer.
        
        While you could just use ``int``, this throws a much nicer error message.
        
                For example::
                
                        >>> v = ToInt()
                        >>> v(1)
                        1
                        >>> v(2.3)
                        2
                        >>> v('foo')
                        Traceback (most recent call last):
                        ...
                        ValueError: can't convert 'foo' to integer
                        
        """

    def __init__(self):
        ToType.__init__(self, int, type_name='integer')


class ToFloat(ToType):
    """
        Convert a value to a float.

        While you could just use ``float``, this throws a much nicer error message.
        
        For example::
        
                >>> v = ToFloat()
                >>> v(1.0)
                1.0
                >>> v(2)
                2.0
                >>> v('foo')
                Traceback (most recent call last):
                ...
                ValueError: can't convert 'foo' to float
        
        """

    def __init__(self):
        ToType.__init__(self, float)


class ToStr(ToType):
    """
        Convert a value to a string.

        While you could just use ``str``, this throws a much nicer error message.
        
        For example::
        
                >>> v = ToStr()
                >>> v(1.0)
                '1.0'
                >>> v('foo')
                'foo'
                
        """

    def __init__(self):
        ToType.__init__(self, str)


class ToList(BaseValidator):
    """
        Convert a value to a string.
        
        Makes sure that the result is a list, even if a list is passed in.
        
        For example::
        
                >>> v = ToList()
                >>> v(1.0)
                [1.0]
                >>> v([])
                []
                >>> v([1, 2, 3])
                [1, 2, 3]
                                
        """

    def convert_value(self, value):
        return impl.make_list(value)


class ToNumber(BaseValidator):
    """
        Convert a value to a the best fit numerical representation.
        
        For example::
        
                >>> v = ToNumber()
                >>> v('1')
                1
                >>> v('1.111')
                1.111
                >>> v(1.0)
                1
                >>> v(1.111)
                1.111
                
        """

    def convert_value(self, value):
        float_value = float(value)
        try:
            int_value = int(value)
        except:
            return float_value

        if float_value == int_value:
            return int_value
        return float_value


class IsInstance(BaseValidator):
    """
        Checks that values are instances of a list of classes or their subclasses.
        
        For example::
        
                >>> v = IsInstance (basestring)
                >>> v('foo')
                'foo'
                >>> v(1)
                Traceback (most recent call last):
                ...
                ValueError: '1' type is not one of basestring
                
        """

    def __init__(self, allowed_classes):
        self.allowed_classes = tuple(impl.make_list(allowed_classes))

    def validate_value(self, value):
        return isinstance(value, self.allowed_classes)

    def make_validation_error_msg(self, bad_val, err):
        return "'%s' type is not one of %s" % (bad_val,
         (', ').join([ t.__name__ for t in self.allowed_classes ]))


class IsType(BaseValidator):
    """
        Checks that values are instances of a list of classes (not their subclasses).
        
        For example::
        
                >>> v = IsType (basestring)
                >>> v('foo')
                Traceback (most recent call last):
                ...
                ValueError: 'foo' type is not an instance of basestring
                >>> v = IsType ([basestring, str])
                >>> v('foo')
                'foo'
                >>> v(1)
                Traceback (most recent call last):
                ...
                ValueError: '1' type is not an instance of basestring, str
        
        """

    def __init__(self, allowed_classes):
        self.allowed_classes = tuple(impl.make_list(allowed_classes))

    def validate_value(self, value):
        for t in self.allowed_classes:
            if type(value) is t:
                return True

        return False

    def make_validation_error_msg(self, bad_val, err):
        return "'%s' type is not an instance of %s" % (bad_val,
         (', ').join([ t.__name__ for t in self.allowed_classes ]))


class StrToBool(ToSynonym):
    """
        Converts common abbreviations for true-false to boolean values.
        
        This converts common abbreviations for true/false to actual Booleans. Case
        and flanking spaces are ignored. The allowed values are defined in `defs`.
        For example::
        
                >>> v = StrToBool()
                >>> v("True")
                True
                >>> v("f")
                False
                >>> v(" on ")
                True
                >>> v("0")
                False
                >>> v("yEs")
                True
                >>> v("maybe")
                Traceback (most recent call last):
                ...
                ValueError: can't recognise MAYBE' as true or false
                
        """

    def __init__(self):
        ToSynonym.__init__(self, defs.TRUE_FALSE_DICT)

    def convert_value(self, value):
        return ToSynonym.convert_value(self, value.strip().upper())

    def validate_value(self, value):
        return value in defs.TRUE_FALSE_DICT.keys()

    def make_validation_error_msg(self, bad_val, err):
        return "can't recognise %s' as true or false" % bad_val


if __name__ == '__main__':
    import doctest
    doctest.testmod()