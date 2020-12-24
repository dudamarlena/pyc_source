# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/socialcommerce/apps/cms/migrations/0003_remove_placeholder.py
# Compiled at: 2009-10-31 23:19:40
from south.db import db
from django.db import models
from cms.models import *

class Migration:

    def forwards(self, orm):
        db.delete_table('cms_placeholder')

    def backwards(self, orm):
        db.create_table('cms_placeholder', (
         (
          'body', models.TextField()),
         (
          'language', models.CharField(_('language'), db_index=True, max_length=3, editable=False, blank=False)),
         (
          'id', models.AutoField(primary_key=True)),
         (
          'name', models.CharField(_('slot'), max_length=50, editable=False, db_index=True)),
         (
          'page', models.ForeignKey(orm.Page, editable=False, verbose_name=_('page')))))
        db.send_create_signal('cms', ['Placeholder'])