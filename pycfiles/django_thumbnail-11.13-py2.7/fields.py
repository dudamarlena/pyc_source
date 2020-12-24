# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-intel/egg/sorl/thumbnail/fields.py
# Compiled at: 2012-12-12 10:05:53
from __future__ import with_statement
from django.db import models
from django.db.models import Q
from django import forms
from django.utils.translation import ugettext_lazy as _
from sorl.thumbnail import default
__all__ = ('ImageField', 'ImageFormField')

class ImageField(models.FileField):

    def delete_file(self, instance, sender, **kwargs):
        """
        Adds deletion of thumbnails and key kalue store references to the
        parent class implementation. Only called in Django < 1.2.5
        """
        file_ = getattr(instance, self.attname)
        query = Q(**{self.name: file_.name}) & ~Q(pk=instance.pk)
        qs = sender._default_manager.filter(query)
        if file_ and file_.name != self.default and not qs:
            default.backend.delete(file_)
        elif file_:
            file_.close()

    def formfield(self, **kwargs):
        defaults = {'form_class': ImageFormField}
        defaults.update(kwargs)
        return super(ImageField, self).formfield(**defaults)

    def save_form_data(self, instance, data):
        if data is not None:
            setattr(instance, self.name, data or '')
        return

    def south_field_triple(self):
        from south.modelsinspector import introspector
        cls_name = '%s.%s' % (self.__class__.__module__, self.__class__.__name__)
        args, kwargs = introspector(self)
        return (cls_name, args, kwargs)


class ImageFormField(forms.FileField):
    default_error_messages = {'invalid_image': _('Upload a valid image. The file you uploaded was either not an image or a corrupted image.')}

    def to_python(self, data):
        """
        Checks that the file-upload field data contains a valid image (GIF,
        JPG, PNG, possibly others -- whatever the engine supports).
        """
        f = super(ImageFormField, self).to_python(data)
        if f is None:
            return
        else:
            if hasattr(data, 'temporary_file_path'):
                with open(data.temporary_file_path(), 'rb') as (fp):
                    raw_data = fp.read()
            elif hasattr(data, 'read'):
                raw_data = data.read()
            else:
                raw_data = data['content']
            if not default.engine.is_valid_image(raw_data):
                raise forms.ValidationError(self.error_messages['invalid_image'])
            if hasattr(f, 'seek') and callable(f.seek):
                f.seek(0)
            return f