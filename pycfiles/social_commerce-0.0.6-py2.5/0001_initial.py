# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/socialcommerce/apps/cms/plugins/text/migrations/0001_initial.py
# Compiled at: 2009-10-31 23:19:40
from south.db import db
from django.db import models
from cms.plugins.text.models import *

class Migration:

    def forwards(self, orm):
        db.create_table('text_text', (
         (
          'body', models.TextField(_('body'))),
         (
          'cmsplugin_ptr', models.OneToOneField(orm['cms.CMSPlugin']))))
        db.send_create_signal('text', ['Text'])

    def backwards(self, orm):
        db.delete_table('text_text')

    models = {'cms.cmsplugin': {'_stub': True, 
                         'id': (
                              'models.AutoField', [], {'primary_key': 'True'})}, 
       'cms.page': {'Meta': {'ordering': "('tree_id','lft')"}, '_stub': True, 
                    'id': (
                         'models.AutoField', [], {'primary_key': 'True'})}}