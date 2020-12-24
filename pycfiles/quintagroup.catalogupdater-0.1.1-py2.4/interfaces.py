# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/quintagroup/catalogupdater/interfaces.py
# Compiled at: 2010-07-14 11:48:20
from zope.interface import Interface

class IUpdatableCatalog(Interface):
    """ Marker interface for separate GenericSetup
        exportimport handler
    """
    __module__ = __name__


class ICatalogUpdater(Interface):
    __module__ = __name__

    def updateMetadata4All(catalog, columns):
        """ Update metadata in the *catalog* for each column
            in the *columns* list for all records.

              * catalog - ZCatalog descendent catalog;
              * columns - list of metadata names, or
                          string with name of single
                          metadata, which must be updated.
        """
        pass