# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/redomino/autodelete/annotations.py
# Compiled at: 2008-09-16 04:37:15
__author__ = 'Davide Moro <davide.moro@redomino.com>'
__docformat__ = 'plaintext'
import datetime
from zope.interface import implements
from zope.annotation.interfaces import IAnnotations
from persistent.dict import PersistentDict
from Products.CMFPlone.CatalogTool import registerIndexableAttribute
from redomino.autodelete.interfaces import IExpirable
from redomino.autodelete.interfaces import IExpires

class ExpiresAnnotation(object):
    """ Adapter for the metadata annotations """
    __module__ = __name__
    implements(IExpirable)
    _KEY = 'redomino.autodelete'
    _IDXS = ['absolote_date', 'to_be_deleted']

    def __init__(self, context):
        self.context = context
        annotations = IAnnotations(context)
        self.metadata = annotations.get(self._KEY, None)
        if self.metadata is None:
            annotations[self._KEY] = PersistentDict()
            self.metadata = annotations[self._KEY]
        return

    def _get_delete_date(self):
        """ Get the delete expiration date (datetime format)"""
        return self.metadata.get('delete_date', None)

    def _set_delete_date(self, date):
        """ Set the delete expiration date (datetime format)"""
        self.metadata['delete_date'] = date
        self._reindex()

    delete_date = property(_get_delete_date, _set_delete_date)

    def to_be_deleted(self):
        """ Returns True if the element is expired """
        delete_date = self.delete_date
        if not delete_date:
            return False
        return IExpirable.providedBy(self.context) and datetime.datetime.today() > delete_date

    def flush(self):
        """ Flush and reindex metadata attributes """
        self.delete_date = None
        self._reindex()
        return

    def _reindex(self):
        """ Reindex metadata attributes when needed """
        self.context.reindexObject(idxs=self._IDXS)


def delete_date(object, portal, **kw):
    """ Register annotated property delete_date to get it into the catalog"""
    adapted = IExpires(object, None)
    if adapted is not None:
        delete_date = adapted.delete_date
        if delete_date and isinstance(delete_date, datetime.datetime):
            return delete_date.strftime('%Y-%m-%d %H:%M:%S')
    return


registerIndexableAttribute('delete_date', delete_date)

def to_be_deleted(object, portal, **kw):
    """ Register annotated property to_be_deleted to get it into the catalog """
    adapted = IExpires(object, None)
    if adapted is not None:
        to_be_deleted = adapted.to_be_deleted()
        return to_be_deleted
    return


registerIndexableAttribute('to_be_deleted', to_be_deleted)