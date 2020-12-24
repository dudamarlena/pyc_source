# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/event/transferable.py
# Compiled at: 2013-04-04 15:36:37
"""Wraps the data that is to be imported into another component."""

class ITransferable(object):
    """ITransferable wraps the data that is to be imported into another
    component. Currently ITransferable is only used for drag and drop.
    """

    def getData(self, dataFlavor):
        """Returns the data from ITransferable by its data flavor (aka data
        type). Data types can be any string keys, but MIME types like
        "text/plain" are commonly used.

        Note, implementations of L{ITransferable} often provide a better
        typed API for accessing data.

        @param dataFlavor:
                   the data flavor to be returned from ITransferable
        @return: the data stored in the ITransferable or null if ITransferable
                contains no data for given data flavour
        """
        raise NotImplementedError

    def setData(self, dataFlavor, value):
        """Stores data of given data flavor to ITransferable. Possibly existing
        value of the same data flavor will be replaced.

        @param dataFlavor:
                   the data flavor
        @param value:
                   the new value of the data flavor
        """
        raise NotImplementedError

    def getDataFlavors(self):
        """@return: a collection of data flavors ( data types ) available in
                this ITransferable
        """
        raise NotImplementedError

    def getSourceComponent(self):
        """@return: the component that created the ITransferable or null if
                the source component is unknown
        """
        raise NotImplementedError