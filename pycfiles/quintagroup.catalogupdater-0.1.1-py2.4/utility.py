# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/quintagroup/catalogupdater/utility.py
# Compiled at: 2010-07-14 11:48:20
import logging, types, transaction
from zope.interface import implements
from zope.component import getMultiAdapter
from zope.component import queryMultiAdapter
from Missing import MV
from Acquisition import aq_inner
from Acquisition import aq_parent
from Products.CMFCore.utils import getToolByName
from Products.ZCatalog.Catalog import safe_callable
try:
    from plone.indexer.interfaces import IIndexableObject
except ImportError:
    from plone.app.content.interfaces import IIndexableObjectWrapper as _old_IIndexableObjectWrapper
    IS_NEW = False
else:
    IS_NEW = True

from quintagroup.catalogupdater.interfaces import ICatalogUpdater
LOG = logging.getLogger('quintagroup.catalogupdater')

class CatalogUpdaterUtility(object):
    __module__ = __name__
    implements(ICatalogUpdater)

    def validate(self, cat, cols):
        AVAIL_COLTYPES = list(types.StringTypes) + [types.ListType, types.TupleType]
        _cat = getattr(cat, '_catalog', None)
        if _cat is None:
            raise AttributeError('%s - is not ZCatalog based catalog' % cat)
        if type(cols) not in AVAIL_COLTYPES:
            raise TypeError("'columns' parameter must be one of the following types: %s" % AVAIL_COLTYPES)
        if type(cols) in types.StringTypes:
            cols = [
             cols]
        for col in cols:
            if not _cat.schema.has_key(col):
                raise AttributeError("'%s' - not presented column in %s catalog " % (col, cat))

        return (
         _cat, cols)

    def getWrappedObjectNew(self, obj, portal, catalog):
        wrapper = None
        if not IIndexableObject.providedBy(obj):
            wrapper = queryMultiAdapter((obj, catalog), IIndexableObject)
        return wrapper and wrapper or obj

    def getWrappedObjectOld(self, obj, portal, catalog):
        wf = getattr(self, 'portal_workflow', None)
        if wf is not None:
            vars = wf.getCatalogVariablesFor(obj)
        else:
            vars = {}
        w = getMultiAdapter((obj, portal), _old_IIndexableObjectWrapper)
        w.update(vars)
        return w

    def updateMetadata4All(self, catalog, columns):
        """ Look into appropriate method of ICatalogUpdate interface
        """
        (_catalog, columns) = self.validate(catalog, columns)
        portal = getToolByName(catalog, 'portal_url').getPortalObject()
        root = aq_parent(portal)
        data = _catalog.data
        schema = _catalog.schema
        paths = _catalog.paths
        getWrappedObject = IS_NEW and self.getWrappedObjectNew or self.getWrappedObjectOld
        threshold = getattr(catalog, 'threshold', 10000)
        _v_total = 0
        _v_transaction = None
        for (rid, md) in data.items():
            obj_uid = paths[rid]
            try:
                obj = root.unrestrictedTraverse(obj_uid)
                obj = getWrappedObject(obj, portal, catalog)
            except:
                LOG.error('updateMetadata4All could not resolve an object from the uid %r.' % obj_uid)
                continue

            mdlist = list(md)
            for column in columns:
                attr = getattr(obj, column, MV)
                if attr is not MV and safe_callable(attr):
                    attr = attr()
                indx = schema[column]
                mdlist[indx] = attr

            data[rid] = tuple(mdlist)
            if threshold is not None:
                t = id(transaction.get())
                if t != _v_transaction:
                    _v_total = 0
                _v_transaction = t
                _v_total = _v_total + 1
                if _v_total > threshold:
                    transaction.savepoint(optimistic=True)
                    catalog._p_jar.cacheGC()
                    _v_total = 0
                    LOG.info('commiting subtransaction')

        return