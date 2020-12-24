# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Volumes/Ozgur/Sites/senpilic.com.tr/senpilic/utils/admin.py
# Compiled at: 2012-10-05 07:44:29
from django.conf import settings
from django.contrib.admin import TabularInline, StackedInline
JS = ()

class OrderableStackedInline(StackedInline):
    """Adds necessary media files to regular Django StackedInline"""

    class Media:
        js = JS


class OrderableTabularInline(TabularInline):
    """Adds necessary media files to regular Django TabularInline"""

    class Media:
        js = JS