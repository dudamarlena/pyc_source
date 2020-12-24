# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/breno/Envs/djangoplus/lib/python3.6/site-packages/djangoplus/utils/serialization.py
# Compiled at: 2018-09-24 08:48:06
# Size of source mod 2**32: 538 bytes
import zlib, base64, pickle
from django.apps import apps

def dumps_qs_query(qs):
    query = base64.b64encode(zlib.compress(pickle.dumps(qs.query)))[::-1].decode('utf-8')
    return '{}:::{}:::{}'.format(qs.model._meta.app_label, qs.model.__name__, query)


def loads_qs_query(s):
    app_label, model_name, query = s.split(':::')
    query = pickle.loads(zlib.decompress(base64.b64decode(query[::-1])))
    qs = apps.get_model(app_label, model_name).objects.all()
    qs.query = query
    return qs