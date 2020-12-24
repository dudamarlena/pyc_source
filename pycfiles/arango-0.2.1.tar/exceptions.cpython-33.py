# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/maxk/Projects/OpenSource/arango-python/arango/exceptions.py
# Compiled at: 2013-11-10 14:30:06
# Size of source mod 2**32: 2231 bytes
__all__ = ('InvalidCollectionId', 'CollectionIdAlreadyExist', 'InvalidCollection',
           'DocumentAlreadyCreated', 'DocumentIncompatibleDataType', 'WrongIndexType',
           'EmptyFields', 'EdgeAlreadyCreated', 'DocumentNotFound', 'EdgeNotYetCreated',
           'EdgeIncompatibleDataType', 'EdgeNotFound', 'DocuemntUpdateError', 'AqlQueryError',
           'DatabaseAlreadyExist', 'DatabaseSystemError')

class DatabaseSystemError(Exception):
    __doc__ = 'Raises in case something went completely wrong'


class InvalidCollection(Exception):
    __doc__ = 'Collection should exist and be subclass of Collection object'


class InvalidCollectionId(Exception):
    __doc__ = 'Invalid name of the collection provided'


class CollectionIdAlreadyExist(Exception):
    __doc__ = 'Raise in case you try to rename collection and new name already\n    available'


class DocumentAlreadyCreated(Exception):
    __doc__ = 'Raise in case document already exist and you try to\n    call `create` method'


class DocumentIncompatibleDataType(Exception):
    __doc__ = 'Raises in case you trying to update document\n    with non-dict or non-list data'


class DocumentNotFound(Exception):
    __doc__ = 'Raises in case Document not exist in database'


class DocuemntUpdateError(Exception):
    __doc__ = "In case can't save document"


class WrongIndexType(Exception):
    __doc__ = 'Raises in case index type is undefined'


class EmptyFields(Exception):
    __doc__ = 'Raises in case no fields for index provied'


class EdgeAlreadyCreated(Exception):
    __doc__ = 'Raises in case Edge have identifier and already created'


class EdgeNotYetCreated(Exception):
    __doc__ = 'Raises in case you try to update Edge which is not created'


class EdgeIncompatibleDataType(Exception):
    __doc__ = 'Raises when you provide new body not None or not dict'


class EdgeNotFound(Exception):
    __doc__ = 'Raised in case Edge not found'


class AqlQueryError(Exception):
    __doc__ = 'In case AQL query cannot be executed'

    def __init__(self, message, num=0, code=0):
        self.num = num
        self.code = code
        self.message = message
        super(AqlQueryError, self).__init__(message)


class DatabaseAlreadyExist(Exception):
    __doc__ = 'Raises in case database already exists'