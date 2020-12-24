# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/huangyong/my_development/python/django_pro/bookstore/DjangoQiniu/views.py
# Compiled at: 2017-05-09 04:50:35
from django.http import JsonResponse
import qiniu
from django.conf import settings

def qiniu_token(request):
    q = qiniu.Auth(settings.QINIU_ACCESS_KEY, settings.QINIU_SECRET_KEY)
    bucket_name = settings.QINIU_BUCKET_NAME
    token = q.upload_token(bucket_name)
    return JsonResponse({'uptoken': token})