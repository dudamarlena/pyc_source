# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/quintagroup/catalogupdater/exportimport/catalogupdater.py
# Compiled at: 2010-07-14 11:48:20
"""Catalog tool columns updater setup handlers.
"""
from zope.component import adapts
from zope.component import queryUtility
from Products.ZCatalog.interfaces import IZCatalog
from Products.GenericSetup.interfaces import ISetupEnviron
from Products.GenericSetup.ZCatalog.exportimport import ZCatalogXMLAdapter
from quintagroup.catalogupdater.interfaces import ICatalogUpdater

class CatalogUpdaterXMLAdapter(ZCatalogXMLAdapter):
    """XML im- and exporter for ZCatalog with
       support of columns updates
    """
    __module__ = __name__
    adapts(IZCatalog, ISetupEnviron)

    def _initColumns(self, node):
        super(CatalogUpdaterXMLAdapter, self)._initColumns(node)
        updatecols = []
        for child in node.childNodes:
            if child.nodeName != 'column':
                continue
            col = str(child.getAttribute('value'))
            if child.hasAttribute('update'):
                if col in self.context.schema()[:]:
                    updatecols.append(col)
                continue

        if len(updatecols) > 0:
            catalog = self.context
            self._logger.info('Updating %s columns for %s Catalog.' % (updatecols, ('/').join(catalog.getPhysicalPath())))
            cu = queryUtility(ICatalogUpdater, name='catalog_updater')
            cu.updateMetadata4All(catalog, updatecols)