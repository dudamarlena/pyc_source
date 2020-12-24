# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/collective/cu3er/browser/viewlets.py
# Compiled at: 2010-05-22 18:32:52
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.layout.viewlets.common import ViewletBase

class CU3ERViewlet(ViewletBase):
    index = ViewPageTemplateFile('templates/cu3er.pt')

    def available(self):
        schema = getattr(self.context, 'Schema', None)
        if schema is None:
            return
        else:
            field = schema().getField('cu3er_enabled')
            if field is None:
                return
            return field.get(self.context)

    def get_height(self):
        schema = getattr(self.context, 'Schema', None)
        if schema is None:
            return
        else:
            field = schema().getField('cu3er_height')
            if field is None:
                return
            return field.get(self.context)

    def get_width(self):
        schema = getattr(self.context, 'Schema', None)
        if schema is None:
            return
        else:
            field = schema().getField('cu3er_width')
            if field is None:
                return
            return field.get(self.context)

    def get_js_config(self):
        return 'var flashvars = {};\n            flashvars.xml = "collective.cu3er.config.xml";\n            var attributes = {};\n            attributes.wmode = "transparent";\n            attributes.id = "slider";\n            swfobject.embedSWF("++resource++collective.cu3er.cu3er.swf", "cu3er-object", "%(width)s", "%(height)s", "9", "++resource++collective.cu3er.expressInstall.swf", flashvars, attributes);' % dict(height=self.get_height(), width=self.get_width())

    def get_css_config(self):
        return '#cu3er-object {width: %(width)spx; outline:0;}' % dict(width=self.get_width())