# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /var/www/django-hstore/django_hstore/compat.py
# Compiled at: 2015-06-28 18:07:27
# Size of source mod 2**32: 365 bytes
import sys

class UnicodeMixin(object):
    __doc__ = '\n    Mixin class to handle defining the proper __str__/__unicode__\n    methods in Python 2 or 3.\n    '
    if sys.version_info[0] >= 3:

        def __str__(self):
            return self.__unicode__()

    else:

        def __str__(self):
            return self.__unicode__().encode('utf8')