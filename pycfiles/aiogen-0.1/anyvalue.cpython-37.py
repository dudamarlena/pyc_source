# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/aiogcd/orm/properties/anyvalue.py
# Compiled at: 2019-09-11 07:21:09
# Size of source mod 2**32: 998 bytes
__doc__ = 'anyvalue.py\n\nCreated on: May 19, 2017\n    Author: Jeroen van der Heijden <jeroen@transceptor.technology>\n'
from .value import Value

class AnyValue(Value):

    def __init__(self, default=None, required=True, accept=None):
        """Initialize a mapped property.

        When 'accept' is None any type is accepted. A tuple can be
        used to force one of the specified types.

        :param default: default value, all types allowed
        :param required: boolean
        :param accept: None or tuple
        """
        self._accept = accept
        super().__init__(default=default, required=required)

    def check_value(self, value):
        if self._accept:
            if not isinstance(value, self._accept):
                raise TypeError('Received value for property {!r} is of invalid type: {!r}'.format(self.name, value.__class__.__name__))

    def set_value(self, model, value):
        self.check_value(value)
        super().set_value(model, value)