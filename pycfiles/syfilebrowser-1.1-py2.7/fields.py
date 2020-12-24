# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/syfilebrowser/fields.py
# Compiled at: 2016-04-18 13:43:20
from __future__ import unicode_literals
from future.builtins import str
from future.builtins import super
import os, datetime
from django.db import models
from django import forms
from django.core.files.storage import default_storage
from django.forms.widgets import Input
from django.db.models.fields import Field
from django.template.loader import render_to_string
from django.utils.encoding import smart_str
from django.utils.translation import ugettext_lazy as _
from syfilebrowser.settings import *
from syfilebrowser.base import FileObject
from syfilebrowser.functions import url_to_path, get_directory
from future.utils import with_metaclass

class FileBrowseWidget(Input):
    input_type = b'text'

    class Media:
        js = (
         os.path.join(URL_FILEBROWSER_MEDIA, b'js/AddSyFileBrowser.js'),)

    def __init__(self, attrs=None):
        self.directory = attrs.get(b'directory', b'')
        self.extensions = attrs.get(b'extensions', b'')
        self.format = attrs.get(b'format', b'')
        if attrs is not None:
            self.attrs = attrs.copy()
        else:
            self.attrs = {}
        return

    def render(self, name, value, attrs=None):
        if value is None:
            value = b''
        directory = self.directory
        if self.directory:
            if callable(self.directory):
                directory = self.directory()
            directory = os.path.normpath(datetime.datetime.now().strftime(directory))
            fullpath = os.path.join(get_directory(), directory)
            if not default_storage.isdir(fullpath):
                default_storage.makedirs(fullpath)
        final_attrs = self.build_attrs(attrs, type=self.input_type, name=name)
        final_attrs[b'search_icon'] = URL_FILEBROWSER_MEDIA + b'img/syfilebrowser_icon_show.gif'
        final_attrs[b'directory'] = directory
        final_attrs[b'extensions'] = self.extensions
        final_attrs[b'format'] = self.format
        final_attrs[b'ADMIN_THUMBNAIL'] = ADMIN_THUMBNAIL
        final_attrs[b'DEBUG'] = DEBUG
        if value != b'':
            try:
                final_attrs[b'directory'] = os.path.split(value.path_relative_directory)[0]
            except:
                pass

        return render_to_string(b'syfilebrowser/custom_field.html', dict(locals(), MEDIA_URL=MEDIA_URL))


class FileBrowseFormField(forms.CharField):
    widget = FileBrowseWidget
    default_error_messages = {b'extension': _(b'Extension %(ext)s is not allowed. Only %(allowed)s is allowed.')}

    def __init__(self, max_length=None, min_length=None, directory=None, extensions=None, format=None, *args, **kwargs):
        self.max_length, self.min_length = max_length, min_length
        self.directory = directory
        self.extensions = extensions
        if format:
            self.format = format or b''
            self.extensions = extensions or EXTENSIONS.get(format)
        super(FileBrowseFormField, self).__init__(*args, **kwargs)

    def clean(self, value):
        value = super(FileBrowseFormField, self).clean(value)
        if value == b'':
            return value
        file_extension = os.path.splitext(value)[1].lower().split(b'?')[0]
        if self.extensions and file_extension not in self.extensions:
            raise forms.ValidationError(self.error_messages[b'extension'] % {b'ext': file_extension, b'allowed': (b', ').join(self.extensions)})
        return value


class FileBrowseField(with_metaclass(models.SubfieldBase, Field)):

    def __init__(self, *args, **kwargs):
        self.directory = kwargs.pop(b'directory', b'')
        self.extensions = kwargs.pop(b'extensions', b'')
        self.format = kwargs.pop(b'format', b'')
        return super(FileBrowseField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        if not value or isinstance(value, FileObject):
            return value
        return FileObject(url_to_path(value))

    def get_db_prep_value(self, value, connection, prepared=False):
        if value is None:
            return
        else:
            return smart_str(value)

    def get_manipulator_field_objs(self):
        return [oldforms.TextField]

    def get_internal_type(self):
        return b'CharField'

    def formfield(self, **kwargs):
        attrs = {}
        attrs[b'directory'] = self.directory
        attrs[b'extensions'] = self.extensions
        attrs[b'format'] = self.format
        defaults = {b'form_class': FileBrowseFormField, 
           b'widget': FileBrowseWidget(attrs=attrs), 
           b'directory': self.directory, 
           b'extensions': self.extensions, 
           b'format': self.format}
        defaults.update(kwargs)
        return super(FileBrowseField, self).formfield(**defaults)


try:
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules([], [b'^syfilebrowser\\.fields\\.FileBrowseField'])
except ImportError:
    pass