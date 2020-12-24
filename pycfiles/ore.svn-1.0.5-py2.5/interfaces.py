# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/ore/svn/interfaces.py
# Compiled at: 2008-05-07 15:44:29
"""
$Id: interfaces.py 2205 2008-05-07 19:44:27Z hazmat $
"""
from zope.interface import Interface

class InvalidRepositoryPath(Exception):
    pass


class RootPathViolation(Exception):
    pass


class UnsupportedNodeType(Exception):
    pass


class NoTransaction(Exception):
    pass


DEBUG = 0
CHUNK_SIZE = 16384
_marker = object()
HEAD = 0

class ISubversionNode(Interface):

    def getModificationTime():
        """
        """
        pass

    def getProperty(property_name):
        """
        """
        pass

    def getProperties():
        """
        """
        pass

    def getRevisionPathMap():
        """
        """
        pass

    def getRevisionCreated():
        """
        """
        pass

    def getMappedLogEntries():
        """
        """
        pass

    def getLog(revision=HEAD):
        """
        """
        pass


class ISubversionFile(ISubversionNode):

    def isBinary():
        """
        """
        pass

    def getMimeType():
        """
        """
        pass

    def getContents(revision=None, writer=None):
        """
        """
        pass

    def getSize():
        """
        """
        pass

    def getAnnotatedLines(revision_set=(), include_copies=True):
        """
        """
        pass

    def lock():
        """
        lock the node
        """
        pass

    def unlock():
        """
        unlock the node
        """
        pass


class ISubversionDirectory(ISubversionNode):
    """
    """
    pass


class ISubversionContext(Interface):
    pass


class IPropertySheet(Interface):
    pass


class ISubversionProperties(IPropertySheet):
    pass


class ILogEntry(Interface):
    pass


class ILogFormatter(Interface):

    def __call__(text):
        """
        return text formatted
        """
        pass