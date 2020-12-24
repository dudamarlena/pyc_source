# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/michal/workspace/code/django-blastplus/blastplus/urls.py
# Compiled at: 2018-05-23 09:38:26
# Size of source mod 2**32: 335 bytes
from django.urls import path
from blastplus.views import blastn, tblastn, blastn, blastp, blastx
urlpatterns = [
 path('blastn', blastn, name='blastn'),
 path('tblastn', tblastn, name='tblastn'),
 path('blast', blastn, name='blastn'),
 path('blastp', blastp, name='blastp'),
 path('blastx', blastx, name='blastx')]