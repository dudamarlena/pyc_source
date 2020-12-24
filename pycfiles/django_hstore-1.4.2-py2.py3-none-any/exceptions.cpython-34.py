# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /var/www/django-hstore/django_hstore/exceptions.py
# Compiled at: 2015-06-28 18:07:27
# Size of source mod 2**32: 309 bytes
from __future__ import unicode_literals, absolute_import

class HStoreDictException(Exception):
    json_error_message = None

    def __init__(self, *args, **kwargs):
        self.json_error_message = kwargs.pop('json_error_message', None)
        super(HStoreDictException, self).__init__(*args, **kwargs)