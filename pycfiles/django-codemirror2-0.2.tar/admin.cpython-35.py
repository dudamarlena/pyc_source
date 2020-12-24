# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/alex/source/git/django-codemirror2/examples/testapp/admin.py
# Compiled at: 2016-02-02 21:43:59
# Size of source mod 2**32: 930 bytes
from django.contrib import admin
from codemirror2.widgets import CodeMirrorEditor
from testapp.models import TestCss, TestHTML

class TestCssAdmin(admin.ModelAdmin):

    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.attname == 'css':
            kwargs['widget'] = CodeMirrorEditor(options={'mode': 'css'})
        return super(TestCssAdmin, self).formfield_for_dbfield(db_field, **kwargs)


class TestHTMLAdmin(admin.ModelAdmin):

    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.attname == 'html':
            kwargs['widget'] = CodeMirrorEditor(options={'mode': 'htmlmixed'}, modes=[
             'css', 'xml', 'javascript', 'htmlmixed'])
        return super(TestHTMLAdmin, self).formfield_for_dbfield(db_field, **kwargs)


admin.site.register(TestCss, TestCssAdmin)
admin.site.register(TestHTML, TestHTMLAdmin)