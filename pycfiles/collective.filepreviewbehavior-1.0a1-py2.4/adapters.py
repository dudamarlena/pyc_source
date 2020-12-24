# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-i386/egg/collective/filepreviewbehavior/adapters.py
# Compiled at: 2010-01-11 09:34:53
import re, logging
from five import grok
from zope.schema import getFieldsInOrder
from Products.CMFCore.utils import getToolByName
from Products.PortalTransforms.libtransforms.utils import MissingBinary
from Products import ARFilePreview
from plone.dexterity.utils import iterSchemata
from plone.rfc822.interfaces import IPrimaryField
from collective.filepreviewbehavior import interfaces
LOG = logging.getLogger('collective.filepreviewbehavior')

class ToPreviewableObject(ARFilePreview.adapters.ToPreviewableObject, grok.Adapter):
    __module__ = __name__
    grok.implements(ARFilePreview.interfaces.IPreviewable)
    grok.context(interfaces.IPreviewable)

    class _replacer(object):
        __module__ = __name__

        def __init__(self, sublist, instance):
            self.sublist = sublist
            self.instance = instance

        def __call__(self, match):
            prefix = match.group(1)
            inside = match.group(2)
            postfix = match.group(3)
            if inside.startswith('./'):
                inside = inside[2:]
            if inside in self.sublist:
                inside = '%s/@@preview_provider?image=%s' % (self.instance.getId(), inside)
            result = '<img%s src="%s"%s>' % (prefix, inside, postfix)
            return result

    def getPrimaryField(self):
        for schema in iterSchemata(self.context):
            for (name, field) in getFieldsInOrder(schema):
                if IPrimaryField.providedBy(field):
                    return field

        return

    def getPreview(self, mimetype='text/html'):
        data = self.annotations[self.key]['html']
        if mimetype != 'text/html' and data:
            transforms = getToolByName(self.context, 'portal_transforms')
            primary = self.getPreview()
            filename = primary.get(self.context).filename + '.html'
            return str(transforms.convertTo(mimetype, data.encode('utf8'), mimetype='text/html', filename=filename)).decode('utf8')
        return data

    def buildAndStorePreview(self):
        self.clearSubObjects()
        transforms = getToolByName(self.context, 'portal_transforms')
        file = self.getPrimaryField().get(self.context)
        data = None
        if file:
            try:
                data = transforms.convertTo('text/html', file.data, filename=file.filename)
            except MissingBinary, e:
                LOG.error(str(e))

        if data is None:
            self.setPreview('')
            return
        html_converted = data.getData()
        html_converted = re.sub('\uf06c', '', html_converted)
        subobjs = data.getSubObjects()
        if len(subobjs) > 0:
            for (id, data) in subobjs.items():
                self.setSubObject(id, data)

            html_converted = self._re_imgsrc.sub(self._replacer(subobjs.keys(), self.context), html_converted)
        self.setPreview(html_converted.decode('utf-8', 'replace'))
        self.context.reindexObject()
        return