# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/bouma/gitprojects/provgroningen/buildout/src/djinn_contenttypes/djinn_contenttypes/__init__.py
# Compiled at: 2015-02-10 14:58:13


def get_js():
    return ['djinn_contenttypes.js']


def get_css():
    return [
     'djinn_contenttypes.css']


def get_urls():
    from urls import urlpatterns
    return urlpatterns