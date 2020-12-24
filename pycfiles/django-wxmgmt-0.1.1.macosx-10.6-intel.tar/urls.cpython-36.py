# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/lidayan/pyenv/python3/pypi-distribute/lib/python3.6/site-packages/wxmgmt/urls.py
# Compiled at: 2018-02-25 20:14:49
# Size of source mod 2**32: 433 bytes
"""
    @version: v1.0 
    @author: 李大炎 (dayan.li@chinaredstar.com) 
    @contact: 840286247@qq.com 
    @project: PyCharm 
    @file: urls.py 
    @time: 2018/2/25 下午10:55 
"""
from django.urls import path
from . import views
urlpatterns = [
 path('<str:tenantName>/api/', (views.api), name='api'),
 path('<str:tenantName>/jsticket/', (views.jsticket), name='jsticket')]