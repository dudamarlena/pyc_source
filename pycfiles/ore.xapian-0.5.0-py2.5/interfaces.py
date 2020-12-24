# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/ore/xapian/interfaces.py
# Compiled at: 2008-10-14 23:52:26
"""
$Id: $
"""
from zope import interface, schema
OP_ADDED = 'added'
OP_DELETED = 'deleted'
OP_MODIFED = 'modified'
OP_REQUEUE = object()
DEBUG_SYNC = False
DEBUG_SYNC_IDX = None
DEBUG_LOG = True

class IIndexable(interface.Interface):
    """
    marker interface for content to be indexed
    """
    pass


class IIndexer(interface.Interface):
    """
    indexes an object into the index
    """

    def index(connection):
        """
        index an object into the connection
        """
        pass


class IIndexOperation(interface.Interface):
    oid = schema.ASCIILine(description='The identifier for the content')
    resolver_id = schema.ASCIILine(description='The resolver used to find the content')

    def process(connection):
        """
        process an index operation
        """
        pass


class IDeleteOperation(IIndexOperation):
    pass


class IModifyOperation(IIndexOperation):
    pass


class IAddOperation(IIndexOperation):
    pass


class IOperationFactory(interface.Interface):
    """
    creates operations, customizable by context, useful for creating classes
    of indexers across an entire class of objects (rdb, svn, fs, etc).
    """

    def add():
        """
        create an add operation
        """
        pass

    def modify():
        """
        create a modify operation
        """
        pass

    def delete():
        """
        create a delete operation
        """
        pass


class IResolver(interface.Interface):
    """
    provides for getting an object identity and resolving an object by
    that identity. these identities are resolver specific, in order
    to resolve them from a document, we need to store the resolver name
    with the document in order to retrieve the appropriate resolver.
    """
    scheme = schema.TextLine(title='Resolver Scheme', description='Name of Resolver Utility')

    def id(object):
        """
        return the document id represented by the object
        """
        pass

    def resolve(document_id):
        """
        return the object represented by a document id
        """
        pass


class IIndexConnection(interface.Interface):
    """
    a xapian index connection
    """
    pass


class ISearchConnection(interface.Interface):
    """
    a xapian search connection
    """
    pass


class IIndexSearch(interface.Interface):
    """
    an access mediator to search connections, to allow for better reuse
    of search connections, avoid the need to carry constructor parameters
    when getting a search connection, and for the framework to provide
    for automatic reopening of connections when the index is modified.
    """

    def __call__():
        """
        return a search connection
        """
        pass