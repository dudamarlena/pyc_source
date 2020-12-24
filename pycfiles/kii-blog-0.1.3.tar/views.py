# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/eliotberriot/Seafile/kii/kii-blog/kii_blog/views.py
# Compiled at: 2015-01-07 09:37:30
from kii.stream import views
from . import models

class EntryList(views.List):
    streamitem_class = models.Entry