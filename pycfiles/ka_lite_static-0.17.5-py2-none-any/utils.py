# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-jkXn_D/django-js-reverse/tests/utils.py
# Compiled at: 2018-07-11 18:15:31
from django.core.urlresolvers import get_script_prefix, set_script_prefix

class script_prefix(object):

    def __init__(self, newpath):
        self.newpath = newpath
        self.oldprefix = get_script_prefix()

    def __enter__(self):
        set_script_prefix(self.newpath)

    def __exit__(self, type, value, traceback):
        set_script_prefix(self.oldprefix)