# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/shuyucms/generic/utils.py
# Compiled at: 2016-08-01 10:53:25
from __future__ import unicode_literals
from django.contrib.contenttypes.models import ContentType
from .models import Keyword, AssignedKeyword

def sync_keywords(string, pk, atype, ctype):
    keywords = string.split(b' ')
    if len(keywords):
        cmod = ContentType.objects.get(app_label=atype, model=ctype)
        content_id = cmod.id
        existing_objs = AssignedKeyword.objects.filter(content_type=content_id, object_pk=pk)
        existing_list = [ key.keyword_id for key in existing_objs ]
        for e_obj in existing_objs:
            if e_obj.keyword.title not in keywords:
                existing_objs.filter(id=e_obj.id).delete()

        order = -1
        for ky in keywords:
            if len(ky):
                order += 1
                key1_objs = Keyword.objects.filter(title__exact=ky)
                key2_objs = Keyword.objects.filter(title__exact=str(ky.encode(b'utf8')))
                key_obj = key2_objs[0] if len(key2_objs) else None
                if key_obj is None and len(key1_objs):
                    key_obj = key1_objs[0]
                if key_obj is not None:
                    if key_obj.id not in existing_list:
                        new_data = {b'content_type': cmod, b'object_pk': pk, b'keyword': key_obj, b'_order': order}
                        AssignedKeyword.objects.create(**new_data)
                    else:
                        new_data = {b'_order': order}
                        existing_objs.filter(keyword=key_obj.id).update(**new_data)
                else:
                    new_data = {b'title': ky}
                    new_obj = Keyword.objects.create(**new_data)
                    new_assign = {b'content_type': cmod, b'object_pk': pk, b'keyword': new_obj, b'_order': order}
                    AssignedKeyword.objects.create(**new_assign)

    return