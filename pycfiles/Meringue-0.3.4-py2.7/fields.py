# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-intel/egg/meringue/fields.py
# Compiled at: 2015-08-17 17:37:49
import mimetypes
from django import forms
from django.core.files.images import ImageFile, get_image_dimensions
from django.db.models.fields.files import FieldFile, ImageField
from south.modelsinspector import add_introspection_rules

class UploadFieldFile(ImageFile, FieldFile):

    def save(self, name, content, save=True):
        type, format = self.mime()
        if type == 'image' and format in ('jpeg', 'png', 'gif', 'tiff'):
            self._dimensions_cache = get_image_dimensions(content)
            if self.field.width_field:
                setattr(self.instance, self.field.width_field, self.width)
            if self.field.height_field:
                setattr(self.instance, self.field.height_field, self.height)
        super(UploadFieldFile, self).save(name, content, save)

    def delete(self, save=True):
        if hasattr(self, '_dimensions_cache'):
            del self._dimensions_cache
        super(UploadFieldFile, self).delete(save)

    def mime(self):
        try:
            return mimetypes.guess_type(self.name)[0].split('/')
        except AttributeError:
            pass

        return False

    def is_swf(self):
        try:
            return mimetypes.guess_type(self.name)[0] == 'application/x-shockwave-flash'
        except AttributeError:
            return False


class UploadField(ImageField):
    attr_class = UploadFieldFile

    def formfield(self, **kwargs):
        defaults = {'form_class': forms.FileField}
        defaults.update(kwargs)
        return super(ImageField, self).formfield(**defaults)


add_introspection_rules([], ['^meringue\\.fields\\.UploadField'])

class PreviewImageField(ImageField):

    def formfield(self, **kwargs):
        kwargs['widget'] = PreviewImageFileInput
        defaults = kwargs
        return super(PreviewImageField, self).formfield(**defaults)