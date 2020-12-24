# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/bouma/projects/pythonunited/provgroningen/buildout/src/djinn_core/djinn_core/__init__.py
# Compiled at: 2014-12-08 04:48:46
from urls import urlpatterns

def get_urls():
    return urlpatterns


def get_js():
    return [
     'djinn_core.js']


def get_css():
    return [
     'djinn_core.css']