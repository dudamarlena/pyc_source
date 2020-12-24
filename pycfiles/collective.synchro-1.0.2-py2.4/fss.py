# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/collective/synchro/plugins/fss.py
# Compiled at: 2008-12-16 18:21:19
"""
fss plugin
"""
from zope.interface import implements
from Products.CMFCore.utils import getToolByName
from Products.Archetypes.BaseUnit import BaseUnit
from Products.Archetypes.config import TOOL_NAME
from zLOG import LOG, DEBUG, INFO
from collective.synchro.data import FssPluginData
from collective.synchro.interfaces import IFssExporter
from collective.synchro.interfaces import IFssImporter
from collective.synchro import config
if config.HAS_FSS_27:
    from iw.fss.FileSystemStorage import FileSystemStorage
elif config.HAS_FSS_26:
    from Products.FileSystemStorage.FileSystemStorage import FileSystemStorage

class FssExporter:
    """
    fss plugin dispatcher
    """
    __module__ = __name__
    implements(IFssExporter)

    def __init__(self, context):
        self.context = context

    def _getListAttributeStorage(self):
        """
        return a dictionnary listing of all fss fields
        portal_type => (field1, field2)
        """
        if not config.HAS_FSS:
            return ()
        attool = getToolByName(self.context, 'archetype_tool')
        rtypes = attool.listRegisteredTypes()
        fss_fields = {}
        for rtype in rtypes:
            ptype = rtype['portal_type']
            fieldnames = []
            schema = rtype['schema']
            for field in schema.fields():
                fieldname = field.getName()
                storage = field.storage
                if isinstance(storage, FileSystemStorage):
                    fieldnames.append(fieldname)

            if fieldnames:
                fss_fields[ptype] = fieldnames

        return fss_fields

    def exportData(self):
        """
        export an IPlugginData
        """
        context = self.context
        dataexport = FssPluginData()
        fss_fields = self._getListAttributeStorage()
        if fss_fields:
            ctool = getToolByName(context, 'portal_catalog')
            query = {'portal_type': fss_fields.keys(), 'path': ('/').join(self.context.getPhysicalPath())}
            brains = ctool(**query)
            objs = []
            if len(brains):
                objs = [ br.getObject() for br in brains ]
            storage = FileSystemStorage()
            for obj in objs:
                fnames = fss_fields[obj.portal_type]
                for fname in fnames:
                    f = obj.getField(fname)
                    value = storage.get(fname, obj)
                    if hasattr(value, 'getData'):
                        value = value.getData()
                    data = {'file': value, 'filename': f.getFilename(obj), 'mimetype': f.getContentType(obj)}
                    portal_url = getToolByName(context, 'portal_url')
                    context_path = portal_url.getRelativeContentPath(context)
                    obj_path = portal_url.getRelativeContentPath(obj)
                    relative_url = ('/').join(obj_path[len(context_path) - 1:])
                    dataexport.getData().append([relative_url, fname, data])

        return dataexport


class FssImporter:
    """
    fss plugin importer
    """
    __module__ = __name__
    implements(IFssImporter)

    def __init__(self, data):
        self.data = data

    def importData(self, context):
        """
        import an IPluginData
        """
        data = self.data
        for (rurl, fname, infos) in data.getData():
            curl = rurl
            object = context.unrestrictedTraverse(curl, None)
            if object:
                base_unit = BaseUnit(name=fname, file=infos['file'], instance=object, filename=infos['filename'], mimetype=infos['mimetype'])
                object.getField(fname).set(object, base_unit)

        return