# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/jwql/website/apps/jwql/admin.py
# Compiled at: 2019-08-26 11:08:03
# Size of source mod 2**32: 775 bytes
"""Customizes the ``jwql`` web app administrative page.

** CURRENTLY NOT IN USE **

Used to customize django's admin interface, and how the data contained
in specific models is portrayed.

Authors
-------

    - Lauren Chambers

References
----------

    For more information please see:
        ``https://docs.djangoproject.com/en/2.0/ref/contrib/admin/``
"""
from django.contrib import admin
from .models import ImageData

class ImageDataAdmin(admin.ModelAdmin):
    list_display = ('filename', 'inst', 'pub_date')
    list_filter = ['pub_date']


admin.site.register(ImageData, ImageDataAdmin)