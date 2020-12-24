# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/kyle/git/flask-xxl/flask_xxl/apps/page/fields.py
# Compiled at: 2018-06-20 18:52:33
from wtforms import fields, widgets

class CKTextEditorWidget(widgets.TextArea):

    def __call__(self, field, **kwargs):
        if kwargs.get('class_', False):
            kwargs['class_'] += ' ckeditor'
        else:
            kwargs['class_'] = 'ckeditor'
        kwargs['rows'] = '8'
        return super(CKTextEditorWidget, self).__call__(field, **kwargs)


class CKTextEditorField(fields.TextAreaField):
    widget = CKTextEditorWidget()