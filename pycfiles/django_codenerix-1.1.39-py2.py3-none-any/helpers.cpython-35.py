# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/www.django/makarthy/codenerix/lib/helpers.py
# Compiled at: 2017-11-28 06:03:36
# Size of source mod 2**32: 854 bytes
from codenerix.helpers import upload_path as upload_path_original

def upload_path(instance, filename):
    return upload_path_original(instance, filename)