# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\mad\validation\issues.py
# Compiled at: 2016-04-12 03:24:05
# Size of source mod 2**32: 3313 bytes


class SemanticIssue:
    __doc__ = '\n    Commonalities between all semantic errors\n    '
    ERROR = 0
    WARNING = 1

    def __init__(self, level):
        self.level = level

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self.__eq__(other)

    def is_error(self):
        return self.level == self.ERROR

    def is_warning(self):
        return self.level == self.WARNING

    def accept(self, visitor):
        raise NotImplementedError('SemanticIssue::accept is abstract')


class ServiceIssue(SemanticIssue):

    def __init__(self, level, service):
        super().__init__(level)
        self.service = service

    def accept(self, visitor):
        raise NotImplementedError('ServiceIssue::accept is abstract')


class EmptyService(ServiceIssue):

    def __init__(self, service):
        super().__init__(self.ERROR, service)

    def accept(self, visitor):
        visitor.empty_service(self)


class UnknownService(ServiceIssue):

    def __init__(self, missing_service):
        super().__init__(self.ERROR, missing_service)

    def accept(self, visitor):
        visitor.unknown_service(self)


class DuplicateIdentifier(SemanticIssue):

    def __init__(self, identifier):
        super().__init__(self.ERROR)
        self.identifier = identifier

    def accept(self, visitor):
        visitor.duplicate_identifier(self)


class OperationIssue(ServiceIssue):

    def __init__(self, level, service, operation):
        super().__init__(level, service)
        self.operation = operation

    def accept(self, visitor):
        raise NotImplementedError('OperationIssue::accept is abstract')


class UnknownOperation(OperationIssue):

    def __init__(self, service, missing_operation):
        super().__init__(self.ERROR, service, missing_operation)

    def accept(self, visitor):
        visitor.unknown_operation(self)


class NeverInvokedOperation(OperationIssue):

    def __init__(self, service, operation):
        super().__init__(self.WARNING, service, operation)

    def accept(self, visitor):
        visitor.never_invoked_operation(self)


class DuplicateOperation(OperationIssue):

    def __init__(self, service, operation):
        super().__init__(self.ERROR, service, operation)

    def accept(self, visitor):
        visitor.duplicate_operation(self)

    def __repr__(self):
        return 'Duplicate operation {0.service}::{0.operation}'.format(self)