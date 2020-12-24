# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/bouma/gitprojects/provgroningen/buildout/src/djinn_forms/djinn_forms/__init__.py
# Compiled at: 2014-08-05 04:26:28
from urls import urlpatterns

def get_js():
    return [
     'djinn_forms.js', 'djinn_forms_relate.js']


def get_css():
    return [
     'djinn_forms.css']


def get_urls():
    return urlpatterns