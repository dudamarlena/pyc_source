# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/downloads/__init__.py
# Compiled at: 2015-04-29 07:49:41
import os, os.path
from django.conf import settings
from downloads.models import TEMP_UPLOAD_FOLDER
tmp_abs_path = os.path.join(settings.MEDIA_ROOT, TEMP_UPLOAD_FOLDER)
if not os.path.exists(tmp_abs_path):
    try:
        os.mkdir(tmp_abs_path, 644)
    except OSError:
        pass