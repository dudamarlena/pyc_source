# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jonasbraun/Coding/iekadou/django-lare/django_lare/context_processors.py
# Compiled at: 2015-06-02 05:26:22
# Size of source mod 2**32: 66 bytes


def lare_information(request):
    return {'lare': request.lare}