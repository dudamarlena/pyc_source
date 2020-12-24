# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mittepro/mitte_exceptions.py
# Compiled at: 2019-11-04 13:57:47
# Size of source mod 2**32: 2164 bytes
import six

class BaseError(Exception):

    def __init__(self, message=None, codigo=None, message_values=()):
        self.message_values = message_values
        self.codigo = codigo
        if six.PY2:
            super(Exception, self).__init__(message)
        else:
            super().__init__(message)


class InvalidParam(BaseError):

    def __init__(self, message='MitteProError - Parâmetro {0} é inválido. Razão: {1}', codigo=None, message_values=()):
        self.message_values = message_values
        self.codigo = codigo
        if message_values:
            message = message.format(*message_values)
        if six.PY2:
            super(InvalidParam, self).__init__(message)
        else:
            super().__init__(message)


class APIError(BaseError):

    def __init__(self, message='MitteProError. Razão: {0}', codigo=None, message_values=()):
        self.message_values = message_values
        self.codigo = codigo
        if message_values:
            message = message.format(*message_values)
        if six.PY2:
            super(APIError, self).__init__(message)
        else:
            super().__init__(message)


class TimeoutError(BaseError):

    def __init__(self, message='MitteProError. Razão: O servidor não respondeu dentro do tempo que você estipulou. O tempo foi de {0} segundo(s)', codigo=None, message_values=()):
        self.message_values = message_values
        self.codigo = codigo
        if message_values:
            message = message.format(*message_values)
        if six.PY2:
            super(TimeoutError, self).__init__(message)
        else:
            super().__init__(message)


class ImproperlyConfigured(BaseError):

    def __init__(self, message='MitteProError. Configuração inapropriada. Razão: {0}', codigo=None, message_values=()):
        self.message_values = message_values
        self.codigo = codigo
        if message_values:
            message = message.format(*message_values)
        if six.PY2:
            super(ImproperlyConfigured, self).__init__(message)
        else:
            super().__init__(message)