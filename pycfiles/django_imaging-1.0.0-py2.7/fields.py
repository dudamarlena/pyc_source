# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/imaging/fields.py
# Compiled at: 2012-06-08 08:51:22
from django.db import models
from django import forms
from django.utils.translation import ugettext as _
from django.db.models.signals import post_save
from imaging.models import Image
from imaging.widgets import ImageSelection
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

class CommaSeparatedIntField(forms.CharField):
    widget = ImageSelection

    def clean(self, value):
        value = super(CommaSeparatedIntField, self).clean(value)
        if value == '':
            return value
        valuelist = [
         '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ',']
        for char in value:
            if char not in valuelist:
                raise forms.ValidationError(_('Image field error, please contact administrator'))

        return value


def save_relations(sender, **kwargs):
    """Take care about image order and image connection to a model"""
    value_dict = getattr(kwargs['instance'], kwargs['instance']._imaging_fname).split(',')
    for i, v in enumerate(value_dict):
        try:
            image = Image.objects.get(pk=v)
            image.ordering = i
            image.content_object = kwargs['instance']
            image.save()
        except:
            pass


class ImagingField(models.Field):
    __metaclass__ = models.SubfieldBase

    def __init__(self, *args, **kwargs):
        kwargs['default'] = ''
        super(ImagingField, self).__init__(*args, **kwargs)

    def contribute_to_class(self, cls, name):
        super(ImagingField, self).contribute_to_class(cls, name)
        setattr(cls, self.name + '_set2', generic.GenericRelation(Image))

    def pre_save(self, model_instance, add):
        setattr(model_instance, '_imaging_fname', self.name)
        post_save.connect(save_relations, sender=model_instance.__class__)
        return getattr(model_instance, self.attname)

    def db_type(self, connection=None):
        return 'char(255)'

    def formfield(self, **kwargs):
        defaults = {'form_class': CommaSeparatedIntField}
        defaults.update(kwargs)
        return super(ImagingField, self).formfield(**defaults)


try:
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules([
     (
      [
       ImagingField], [], {})], [
     '^imaging\\.fields\\.ImagingField'])
except ImportError:
    pass