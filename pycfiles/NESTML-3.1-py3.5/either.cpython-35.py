# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pynestml/utils/either.py
# Compiled at: 2020-03-05 05:49:41
# Size of source mod 2**32: 2958 bytes


class Either(object):
    __doc__ = '\n    Objects of these class are either values or error messages.\n    Attributes:\n        __value (object): The value.\n        __error (str): An error message.\n    '

    def __init__(self, value=None, error=None):
        """
        Constructor for Either. Do not call directly! Use Either.value() or Either.error instead!
        :param value: a value
        :type value: object
        :param error: an error
        :type error: object
        """
        self._Either__value = value
        self._Either__error = error

    @classmethod
    def value(cls, value):
        """
        Construct an Either holding a valid value
        :param value: the value to hold
        :type: _value: anything
        :return: an Either object holding a valid value
        :rtype: Either
        """
        return Either(value, None)

    @classmethod
    def error(cls, error):
        """
        Construct an Either holding an error message
        :param error: an error message
        :type error: str
        :return: an Either object holding an error message
        :rtype: Either
        """
        return Either(None, error)

    def get_value(self):
        """
        Get the valid value saved in the Either object
        :return: valid value
        :rtype: any type of valid values
        """
        return self._Either__value

    def get_error(self):
        """
        Get the error message saved in the Either object
        :return: an error message
        :rtype: str
        """
        return self._Either__error

    def is_value(self):
        """
        Return whether the object holds a valid value
        :return: true iff object holds a valid value
        :rtype: bool
        """
        return self._Either__value is not None

    def is_error(self):
        """
        Return whether the object holds an error message
        :return: true iff the object holds an error message
        :rtype: bool
        """
        return self._Either__error is not None

    def __str__(self):
        """
        Constructs string representation of the Either object
        :return: string representation of the object
        :rtype: str
        """
        return '(' + str(self._Either__value) + ', ' + str(self._Either__error) + ')'