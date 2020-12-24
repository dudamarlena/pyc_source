# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/site-packages/bootstrap3_wysihtml5x/__init__.py
# Compiled at: 2014-10-27 12:41:13
"""
django-bootstrap3-wysihtml5x - Simple Django app that allows using the rich text editor Wysihtml5 in text fields.
"""
default_app_config = 'bootstrap3_wysihtml5x.apps.Bootstrap3Wysihtml5xConfig'
VERSION = (1, 0, 0, 'b', 1)

def get_version():
    version = '%s.%s' % (VERSION[0], VERSION[1])
    if VERSION[2]:
        version = '%s.%s' % (version, VERSION[2])
    if VERSION[3] != 'f':
        version = '%s%s%s' % (version, VERSION[3], VERSION[4])
    return version