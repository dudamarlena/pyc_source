# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/f0/paul/Projects/Py-konval/konval/konval/sizeval.py
# Compiled at: 2011-08-02 09:53:13
"""
Validators that check value magnitude.

"""
__docformat__ = 'restructuredtext en'
from basevalidator import BaseValidator

class IsInRange(BaseValidator):
    """
        Only allow values between certain inclusive bounds.
        """

    def __init__(self, min=None, max=None):
        self.min = min
        self.max = max

    def validate_value(self, value):
        if self.min is not None:
            assert self.min <= value, '%s is lower than %s' % (value, self.min)
        if self.max is not None:
            assert value <= self.max, '%s is higher than %s' % (value, self.max)
        return True

    def make_validation_error_msg(self, bad_val, err):
        """
                Generate an meaningful error message for a range problem.
                """
        if err:
            return str(err)
        else:
            return BaseValidator.make_validation_error_msg(self, bad_val, err)


Range = IsInRange

class IsEqualOrMore(IsInRange):

    def __init__(self, min):
        IsInRange.__init__(self, min=min, max=None)
        return


MinValue = IsEqualOrMore

class IsEqualOrLess(IsInRange):

    def __init__(self, max):
        IsInRange.__init__(self, min=None, max=max)
        return


MaxValue = IsEqualOrLess

class IsBetween(IsInRange):
    """
        Only allow values between certain exclusive bounds.
        """

    def __init__(self, min=None, max=None):
        IsInRange.__init__(min=min, max=max)

    def validate_value(self, value):
        if self.min is not None:
            assert self.min < value, '%s is lower or equal to %s' % (value, self.min)
        if self.max is not None:
            assert value < self.max, '%s is higher or equal to %s' % (value, self.max)
        return True


ExclusiveRange = IsBetween

class CheckLength(BaseValidator):
    """
        Only allow values of a certain sizes.

        Length limitations are expressed as (inclusive) minimum and maximum sizes.
        This is most useful for strings, but could be used for lists.
        """

    def __init__(self, min=None, max=None):
        self.min = min
        self.max = max

    def make_validation_error_msg(self, bad_val, err):
        """
                Generate an meaningful error message for a length problem.
                """
        if err:
            return str(err)
        else:
            return BaseValidator.make_validation_error_msg(self, bad_val, err)

    def validate_value(self, value):
        if self.min is not None:
            assert self.min <= len(value), '%s is shorter than %s' % (value, self.min)
        if self.max is not None:
            assert len(value) <= self.max, '%s is longer than %s' % (value, self.max)
        return True


if __name__ == '__main__':
    import doctest
    doctest.testmod()