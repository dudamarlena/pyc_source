# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: E:\python\hhwork\extra_apps\xadmin\plugins\ueditor.py
# Compiled at: 2019-04-17 23:57:58
# Size of source mod 2**32: 1481 bytes
__author__ = 'bobby'
from django.conf import settings
import xadmin
from DjangoUeditor.models import UEditorField
from DjangoUeditor.widgets import UEditorWidget
from xadmin.views import BaseAdminPlugin, CreateAdminView, UpdateAdminView

class XadminUEditorWidget(UEditorWidget):

    def __init__(self, **kwargs):
        self.ueditor_options = kwargs
        self.Media.js = None
        super(XadminUEditorWidget, self).__init__(kwargs)


class UeditorPlugin(BaseAdminPlugin):

    def get_field_style(self, attrs, db_field, style, **kwargs):
        if style == 'ueditor':
            if isinstance(db_field, UEditorField):
                widget = db_field.formfield().widget
                param = {}
                param.update(widget.ueditor_settings)
                param.update(widget.attrs)
                return {'widget': XadminUEditorWidget(**param)}
        return attrs

    def block_extrahead(self, context, nodes):
        js = '<script type="text/javascript" src="%s"></script>' % (settings.STATIC_URL + 'ueditor1261/ueditor.config.js')
        js += '<script type="text/javascript" src="%s"></script>' % (settings.STATIC_URL + 'ueditor1261/ueditor.all.js')
        nodes.append(js)


xadmin.site.register_plugin(UeditorPlugin, UpdateAdminView)
xadmin.site.register_plugin(UeditorPlugin, CreateAdminView)