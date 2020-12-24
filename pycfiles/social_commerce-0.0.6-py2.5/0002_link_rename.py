# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/socialcommerce/apps/cms/plugins/picture/migrations/0002_link_rename.py
# Compiled at: 2009-10-31 23:19:40
from south.db import db
from django.db import models
from cms.plugins.picture.models import *

class Migration:

    def forwards(self, orm):
        db.rename_column('picture_picture', 'link', 'url')

    def backwards(self, orm):
        db.rename_column('picture_picture', 'url', 'link')