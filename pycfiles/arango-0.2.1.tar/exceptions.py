# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/maxk/Projects/OpenSource/arango-python/arango/exceptions.py
# Compiled at: 2013-11-10 14:30:06
__all__ = ('InvalidCollectionId', 'CollectionIdAlreadyExist', 'InvalidCollection',
           'DocumentAlreadyCreated', 'DocumentIncompatibleDataType', 'WrongIndexType',
           'EmptyFields', 'EdgeAlreadyCreated', 'DocumentNotFound', 'EdgeNotYetCreated',
           'EdgeIncompatibleDataType', 'EdgeNotFound', 'DocuemntUpdateError', 'AqlQueryError',
           'DatabaseAlreadyExist', 'DatabaseSystemError')

class DatabaseSystemError(Exception):
    """Raises in case something went completely wrong"""
    pass


class InvalidCollection(Exception):
    """Collection should exist and be subclass of Collection object"""
    pass


class InvalidCollectionId(Exception):
    """Invalid name of the collection provided"""
    pass


class CollectionIdAlreadyExist(Exception):
    """Raise in case you try to rename collection and new name already
    available"""
    pass


class DocumentAlreadyCreated(Exception):
    """Raise in case document already exist and you try to
    call `create` method"""
    pass


class DocumentIncompatibleDataType(Exception):
    """Raises in case you trying to update document
    with non-dict or non-list data"""
    pass


class DocumentNotFound(Exception):
    """Raises in case Document not exist in database"""
    pass


class DocuemntUpdateError(Exception):
    """In case can't save document"""
    pass


class WrongIndexType(Exception):
    """Raises in case index type is undefined"""
    pass


class EmptyFields(Exception):
    """Raises in case no fields for index provied"""
    pass


class EdgeAlreadyCreated(Exception):
    """Raises in case Edge have identifier and already created"""
    pass


class EdgeNotYetCreated(Exception):
    """Raises in case you try to update Edge which is not created"""
    pass


class EdgeIncompatibleDataType(Exception):
    """Raises when you provide new body not None or not dict"""
    pass


class EdgeNotFound(Exception):
    """Raised in case Edge not found"""
    pass


class AqlQueryError(Exception):
    """In case AQL query cannot be executed"""

    def __init__(self, message, num=0, code=0):
        self.num = num
        self.code = code
        self.message = message
        super(AqlQueryError, self).__init__(message)


class DatabaseAlreadyExist(Exception):
    """Raises in case database already exists"""
    pass