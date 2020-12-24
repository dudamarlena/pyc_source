# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/kraken/Projects/websites/django-formaldehyde/formaldehyde/formaldehyde/fieldsets.py
# Compiled at: 2015-01-30 09:43:51
from __future__ import unicode_literals
from django import forms
from django.utils import six
from .conf import settings

class Fieldline(object):

    def __init__(self, form, fieldline, layoutline):
        self.form = form
        if not hasattr(fieldline, b'__iter__') or isinstance(fieldline, six.text_type):
            self.fields = [
             fieldline]
        else:
            self.fields = fieldline
        if not hasattr(layoutline, b'__iter__') or isinstance(fieldline, six.integer_types):
            self.layout = [
             layoutline]
        else:
            self.layout = layoutline
        self.layout_cols = settings.GRID_COLUMN_NUMBER - settings.FIRST_LABEL_COLUMN_SIZE
        if len(self.fields) > 1:
            self.layout_cols = int(self.layout_cols / len(self.fields) - 1)
        self.__index = 0
        self.__len = max(len(self.fields), len(self.layout))

    def __iter__(self):
        return self

    def __next__(self):
        return self.next()

    def next(self):
        if self.__index >= self.__len:
            raise StopIteration()
        field = self.fields[self.__index] if self.__index < len(self.fields) else None
        if field:
            print self.form
            field = self.form[field]
        layout = self.layout[self.__index] if self.__index < len(self.layout) else None
        if not layout:
            layout = self.layout_cols
        self.__index += 1
        return (
         field, layout)


class Fieldset(object):

    def __init__(self, form, legend, fields, layout, description, classes):
        self.form = form
        self.legend = legend
        self.fields = fields
        self.layout = layout
        self.description = description
        self.classes = classes
        self.__index = 0
        self.__len = max(len(self.fields), len(self.layout))

    def __iter__(self):
        return self

    def __next__(self):
        return self.next()

    def next(self):
        if self.__index >= self.__len:
            raise StopIteration()
        fieldline = Fieldline(form=self.form, fieldline=self.fields[self.__index] if self.__index < len(self.fields) else None, layoutline=self.layout[self.__index] if self.__index < len(self.layout) else None)
        self.__index += 1
        return fieldline


class FieldsetFormMixin(object):

    def __init__(self, *args, **kwargs):
        super(FieldsetFormMixin, self).__init__(*args, **kwargs)
        assert isinstance(self, forms.BaseForm)
        self.meta = getattr(self, b'MetaForm', None)
        self.fieldsets = None
        if self.meta and self.meta.fieldsets:
            self.fieldsets = self._fieldsets
        return

    def _fieldsets(self):
        if self.meta and self.meta.fieldsets:
            for legend, data in self.meta.fieldsets:
                yield Fieldset(form=self, legend=legend, fields=data.get(b'fields', tuple()), layout=data.get(b'layout', tuple()), description=data.get(b'description', b''), classes=data.get(b'classes', b''))