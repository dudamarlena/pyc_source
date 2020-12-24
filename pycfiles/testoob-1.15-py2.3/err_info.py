# uncompyle6 version 3.7.4
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/testoob/reporting/err_info.py
# Compiled at: 2009-10-07 18:08:46
"""getting information about errors"""

def create_err_info(test, err):
    """
    Factory method for creating ErrInfo instances.
    """
    if isinstance(err, ErrInfo):
        return err
    return ErrInfo(test, err)


def _should_skip(exception_type):
    import testoob
    try:
        return issubclass(exception_type, testoob.SkipTestException)
    except TypeError:
        return False


class ErrInfo:
    """
    An interface for getting information about test errors.
    Reporters receive instances of this class.
    """
    __module__ = __name__

    def __init__(self, test, exc_info):
        self.test = test
        self.exc_info = exc_info

    def __str__(self):
        from common import exc_info_to_string
        from test_info import TestInfo
        return exc_info_to_string(self.exc_info, TestInfo(self.test))

    def is_skip(self):
        """
        Does the error signify a skip?

        Normally done by checking that exception_type derives from
        SkipTestException, but that can't be done after fields pickling.
        """
        return _should_skip(self.exc_info[0])

    def exception_type(self):
        t = self.exc_info[0]
        try:
            return t.__module__ + '.' + t.__name__
        except AttributeError:
            return str(t)

    def exception_value(self):
        return str(self.exc_info[1])

    def traceback(self):
        return self.exc_info[2]


from testoob.utils import add_fields_pickling
add_fields_pickling(ErrInfo)