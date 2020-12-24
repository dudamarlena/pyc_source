# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /code/s3direct/urls.py
# Compiled at: 2019-07-26 07:43:54
# Size of source mod 2**32: 295 bytes
from django.conf.urls import url
from s3direct.views import get_upload_params, generate_aws_v4_signature
urlpatterns = [
 url('^get_upload_params/', get_upload_params, name='s3direct'),
 url('^get_aws_v4_signature/', generate_aws_v4_signature,
   name='s3direct-signing')]