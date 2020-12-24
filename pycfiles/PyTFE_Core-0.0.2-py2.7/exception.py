# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/tfe/core/exception.py
# Compiled at: 2018-10-14 15:12:44


class TFEException(Exception):
    pass


class TFESessionException(Exception):
    pass


class TFEValidationError(Exception):
    pass


class TFEAttributeError(Exception):
    pass


def exc(original_function):

    def new_function(*args, **kwargs):
        try:
            x = original_function(*args, **kwargs)
            return x
        except Exception as e:
            exception_name = e.__class__.__name__
            raise type(('TFE{0}').format(exception_name), (TFEException, e.__class__), dict())(str(e))

    return new_function


def RaisesTFEException(Cls):

    class NewCls(object):

        def __init__(self, *args, **kwargs):
            self.oInstance = Cls(*args, **kwargs)

        def __getattribute__(self, s):
            try:
                x = super(NewCls, self).__getattribute__(s)
            except AttributeError:
                pass
            else:
                return x

            try:
                x = self.oInstance.__getattribute__(s)
            except AttributeError as e:
                raise type('TFEAttributeError', (TFEException, AttributeError), dict())(str(e))

            if type(x) == type(self.__init__):
                return exc(x)
            else:
                return x

    return NewCls