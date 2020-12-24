# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\Aaswaini Dev\PycharmProjects\FinanceCRM\apps\csv_importer\utils.py
# Compiled at: 2020-04-27 11:23:46
# Size of source mod 2**32: 2309 bytes
from django.db.models import ForeignKey, ManyToOneRel, AutoField, ManyToManyRel, ManyToManyField

def get_required_fields(model):
    fields = model._meta.get_fields()
    required_fields = []
    for f in fields:
        if f.name in model.csv_upload_compulsory_fields:
            if isinstance(model._meta.get_field(f.name), ForeignKey):
                required_fields.append(f.name + '_id')
            else:
                required_fields.append(f.name)
            if hasattr(f, 'blank') and f.blank == False:
                if isinstance(model._meta.get_field(f.name), ForeignKey):
                    if f.name in model.fk_handle_by_id:
                        required_fields.append(f.name + '_id')
                required_fields.append(f.name)

    return required_fields


def get_optional_fields(model):
    fields = model._meta.get_fields()
    optional_field = []
    for f in fields:
        if not isinstance(f, AutoField):
            if f.name in model.csv_upload_compulsory_fields:
                pass
            elif not (hasattr(f, 'blank') and f.blank == False) and not isinstance(model._meta.get_field(f.name), ManyToOneRel) and not isinstance(model._meta.get_field(f.name), ManyToManyField):
                optional_field.append(f.name)

    return optional_field


def get_fk_fields(model):
    fields = model._meta.get_fields()
    fk_fields = []
    for f in fields:
        if isinstance(f, AutoField):
            pass
        else:
            if isinstance(model._meta.get_field(f.name), ForeignKey):
                fk_fields.append(f.name)

    return fk_fields