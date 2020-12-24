# uncompyle6 version 3.6.7
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/maxk/Projects/OpenSource/arango-python/arango/exceptions.py
# Compiled at: 2013-11-10 14:30:06
# Size of source mod 2**32: 2231 bytes
__all__ = ('InvalidCollectionId', 'CollectionIdAlreadyExist', 'InvalidCollection',
           'DocumentAlreadyCreated', 'DocumentIncompatibleDataType', 'WrongIndexType',
           'EmptyFields', 'EdgeAlreadyCreated', 'DocumentNotFound', 'EdgeNotYetCreated',
           'EdgeIncompatibleDataType', 'EdgeNotFound', 'DocuemntUpdateError', 'AqlQueryError',
           'DatabaseAlreadyExist', 'DatabaseSystemError')

class DatabaseSystemError(Exception):
    """DatabaseSystemError"""
    pass


class InvalidCollection(Exception):
    """InvalidCollection"""
    pass


class InvalidCollectionId(Exception):
    """InvalidCollectionId"""
    pass


class CollectionIdAlreadyExist(Exception):
    """CollectionIdAlreadyExist"""
    pass


class DocumentAlreadyCreated(Exception):
    """DocumentAlreadyCreated"""
    pass


class DocumentIncompatibleDataType(Exception):
    """DocumentIncompatibleDataType"""
    pass


class DocumentNotFound(Exception):
    """DocumentNotFound"""
    pass


class DocuemntUpdateError(Exception):
    """DocuemntUpdateError"""
    pass


class WrongIndexType(Exception):
    """WrongIndexType"""
    pass


class EmptyFields(Exception):
    """EmptyFields"""
    pass


class EdgeAlreadyCreated(Exception):
    """EdgeAlreadyCreated"""
    pass


class EdgeNotYetCreated(Exception):
    """EdgeNotYetCreated"""
    pass


class EdgeIncompatibleDataType(Exception):
    """EdgeIncompatibleDataType"""
    pass


class EdgeNotFound(Exception):
    """EdgeNotFound"""
    pass


class AqlQueryError(Exception):
    """AqlQueryError"""

    def __init__(self, message, num=0, code=0):
        self.num = num
        self.code = code
        self.message = message
        super(AqlQueryError, self).__init__(message)


class DatabaseAlreadyExist(Exception):
    """DatabaseAlreadyExist"""
    pass