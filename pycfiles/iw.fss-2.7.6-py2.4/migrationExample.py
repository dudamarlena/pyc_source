# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/iw/fss/Extensions/migrationExample.py
# Compiled at: 2008-10-23 05:55:16
import StringIO
from zope.component import getUtility
from Products.CMFCore.utils import getToolByName
from Products.Archetypes.Field import FileField, StringField, TextField
from Products.Archetypes.Storage import AttributeStorage
from iw.fss.FileSystemStorage import FileSystemStorage
from iw.fss.interfaces import IConf

def migrateToFSStorage(self):
    r"""
    Migrate File and Images FileFields to FSStorage
    
    /!\ Assertion is made that the schema definition has been migrated to define
    FSS as storage for interested fields
    """
    try:
        conf = getUtility(IConf, 'globalconf')()
    except AttributeError:
        raise ValueError, 'install and configure FileSystemStorage first!'

    out = StringIO.StringIO()
    cat = getToolByName(self, 'portal_catalog')
    brains = cat({'portal_type': ['File', 'Image']})
    attr_storage = AttributeStorage()
    fss_storage = FileSystemStorage()
    for b in brains:
        o = b.getObject()
        print >> out, ('/').join(o.getPhysicalPath()), ':',
        if o.UID() is None:
            o._register()
            o._updateCatalog(o.aq_parent)
            print >> out, 'UID was None, set to: ', o.UID(),
        for f in o.Schema().fields():
            if not isinstance(f, FileField):
                continue
            storage = f.getStorage()
            if not isinstance(storage, FileSystemStorage):
                continue
            name = f.getName()
            print >> out, "'%s'" % name,
            if f.get_size(o) != 0:
                print >> out, 'already set',
                continue
            try:
                content = attr_storage.get(name, o)
            except AttributeError:
                print >> out, 'no old value',
                continue

            attr_storage.unset(name, o)
            fss_storage.initializeField(o, f)
            f.set(o, content)
            if f.get_size(o) == 0:
                print >> out, 'unset',
                f.set(o, 'DELETE_FILE')
            print >> out, ',',

        print >> out, ''

    return out.getvalue()