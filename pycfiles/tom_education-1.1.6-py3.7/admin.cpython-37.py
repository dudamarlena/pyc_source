# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/tom_education/admin.py
# Compiled at: 2020-04-29 07:56:29
# Size of source mod 2**32: 646 bytes
from django import forms
from django.contrib import admin
from tom_education.models import ObservationTemplate, PipelineProcess
from tom_dataproducts.models import DataProduct

@admin.register(ObservationTemplate)
class ObservationTemplateAdmin(admin.ModelAdmin):
    list_display = ('name', 'target', 'facility')


class DataProductAdminForm(forms.ModelForm):

    class Meta:
        model = DataProduct
        fields = '__all__'
        widgets = {'data_product_type': forms.Textarea(attrs={'cols': 98})}


class DataProductAdmin(admin.ModelAdmin):
    form = DataProductAdminForm


admin.site.register(PipelineProcess)