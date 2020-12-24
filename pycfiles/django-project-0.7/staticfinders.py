# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: E:\workspace\django-template-project\source\conf\apps\web\staticfinders.py
# Compiled at: 2011-06-19 09:35:56
from django.core.files.storage import FileSystemStorage
from django.contrib.staticfiles.finders import BaseStorageFinder
from django.conf import settings

class StaticRootFinder(BaseStorageFinder):
    storage = FileSystemStorage(settings.STATIC_ROOT, settings.STATIC_URL)