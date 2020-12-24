# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\mad\ast\definitions.py
# Compiled at: 2016-04-04 07:45:39
# Size of source mod 2**32: 2315 bytes
from mad.ast.commons import Expression

class Definition(Expression):
    __doc__ = '\n    Abstract definition that binds a name to an expression to be evaluated\n    '

    def __init__(self, name, body):
        super().__init__()
        self.name = name
        self.body = body

    def accept(self, evaluation):
        raise NotImplementedError('Definition::accept is abstract!')


class DefineService(Definition):
    __doc__ = '\n    Definition of a service and the operations it exposes\n    '

    def __init__(self, name, body):
        super().__init__(name, body)

    def accept(self, evaluation):
        return evaluation.of_service_definition(self)

    def __repr__(self):
        return 'DefineService(%s, %s)' % (self.name, self.body)


class DefineOperation(Definition):
    __doc__ = '\n    Define an operation exposed by a service.\n    '

    def __init__(self, name, body):
        super().__init__(name, body)
        self.parameters = []

    def accept(self, evaluation):
        return evaluation.of_operation_definition(self)

    def __repr__(self):
        return 'DefineOperation(%s, %s)' % (self.name, str(self.body))


class DefineClientStub(Definition):
    __doc__ = '\n    Define a client stub, that is an entity that emits requests at a given frequency\n    '

    def __init__(self, name, period, body):
        super().__init__(name, body)
        self.period = period

    def __repr__(self):
        return 'DefineClientStub(%d, %s)' % (self.period, self.body)

    def accept(self, evaluation):
        return evaluation.of_client_stub_definition(self)