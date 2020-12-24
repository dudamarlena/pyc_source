# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/gkarak/workspace/python/django-ninecms/ninecms/utils/manytomany.py
# Compiled at: 2016-04-06 06:07:34
# Size of source mod 2**32: 3676 bytes
""" https://gist.github.com/Wtower/0b181cc06f816e4feac14e7c0aa2e9d0 """
__author__ = 'George Karakostas'
__copyright__ = 'Copyright 2015, George Karakostas'
__licence__ = 'BSD-3'
__email__ = 'gkarak@9-dev.com'
from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple

class ModelBiMultipleChoiceField(forms.ModelMultipleChoiceField):
    __doc__ = ' This shows both ends of m2m in admin '

    def __init__(self, queryset, required=False, widget=None, label=None, initial=None, help_text='', double_list=None, *args, **kwargs):
        """ First add a custom ModelMultipleChoiceField
        Specify a `double_list` label in order to use the double list widget
        Field name should be the same with model's m2m field
        https://www.lasolution.be/blog/related-manytomanyfield-django-admin-site.html
        https://github.com/django/django/blob/master/django/contrib/admin/widgets.py#L24
        """
        if double_list:
            widget = FilteredSelectMultiple(double_list, True)
        super(ModelBiMultipleChoiceField, self).__init__(queryset, required, widget, label, initial, help_text, *args, **kwargs)


class ManyToManyModelForm(forms.ModelForm):
    __doc__ = ' This is a generic form to use with the ModelBiMultipleChoiceField '

    def __init__(self, *args, **kwargs):
        """ Initialize form
        :param args
        :param kwargs
        :return: None
        """
        super(ManyToManyModelForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            for field_name in self.base_fields:
                field = self.base_fields[field_name]
                if type(field).__name__ == 'ModelBiMultipleChoiceField':
                    self.initial[field_name] = getattr(self.instance, field_name).values_list('pk', flat=True)
                    continue

    def save(self, *args, **kwargs):
        """ Handle saving of related
        :param args
        :param kwargs
        :return: instance
        """
        instance = super(ManyToManyModelForm, self).save(*args, **kwargs)
        if instance.pk:
            for field_name in self.base_fields:
                field = self.base_fields[field_name]
                if type(field).__name__ == 'ModelBiMultipleChoiceField':
                    recordset = getattr(self.instance, field_name)
                    records = recordset.all()
                    for record in records:
                        if record not in self.cleaned_data[field_name]:
                            recordset.remove(record)
                            continue

                    for record in self.cleaned_data[field_name]:
                        if record not in records:
                            recordset.add(record)
                            continue

                    continue

        return instance