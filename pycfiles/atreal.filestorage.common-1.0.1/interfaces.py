# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/romain/dev/buildouts/xnet4.1/src/atreal.filestorage.common/atreal/filestorage/common/interfaces.py
# Compiled at: 2011-10-27 09:41:01
from zope.interface import Interface

class IAnnotFileStore(Interface):
    """
    """
    pass


class IOfsFile(Interface):
    """
    """
    pass


class IOmniFile(Interface):
    """
    """

    def setContenType(value):
        """
        """
        pass

    def getContentType():
        """
        """
        pass

    def open():
        """
        """
        pass


class IArFileData(Interface):

    def read(size):
        """
        """
        pass

    def write(buffer):
        """
        """
        pass

    def seek(pos, rel):
        """
        """
        pass

    def tell():
        """
        """
        pass