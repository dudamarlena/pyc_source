# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/afshari9978/Projects/namaki_backend/avishan/admin.py
# Compiled at: 2020-04-21 05:34:55
# Size of source mod 2**32: 1559 bytes
from django.contrib import admin
from django.contrib.admin.sites import AlreadyRegistered
from django.db import models
from avishan.models import AvishanModel

def maker(source: list) -> list:
    output = []
    for item in source:
        if isinstance(item, models.Field):
            output.append(item.name)
        else:
            output.append(item)
    else:
        return output


for model in AvishanModel.get_non_abstract_models():
    model_admin_dict = {'list_filter':maker(model.django_admin_list_filter),  'list_max_show_all':model.django_admin_list_max_show_all, 
     'list_per_page':model.django_admin_list_per_page, 
     'raw_id_fields':maker(model.django_admin_raw_id_fields), 
     'readonly_fields':maker(model.django_admin_readonly_fields), 
     'search_fields':maker(model.django_admin_search_fields)}
    for field in model.get_fields():
        if isinstance(field, models.DateField):
            if not field.auto_now_add:
                if field.auto_now:
                    model_admin_dict['readonly_fields'].append(field.name)
                if model.django_admin_date_hierarchy:
                    model_admin_dict['date_hierarchy'] = model.django_admin_date_hierarchy
                if len(model.django_admin_list_display) > 0:
                    model_admin_dict['list_display'] = maker(model.django_admin_list_display)
            model_admin = type(model.class_snake_case_name() + '_admin', (admin.ModelAdmin,), model_admin_dict)
            try:
                admin.site.register(model, model_admin)
            except AlreadyRegistered:
                pass