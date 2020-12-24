# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/socialcommerce/apps/cms/plugins/link/migrations/0004_larger_link_names.py
# Compiled at: 2009-10-31 23:19:40
from south.db import db
from django.db import models
from cms.plugins.link.models import *

class Migration:

    def forwards(self, orm):
        db.alter_column('link_link', 'name', models.CharField(_('name'), max_length=256))

    def backwards(self, orm):
        db.alter_column('link_link', 'name', models.CharField(_('name'), max_length=40))

    models = {'cms.cmsplugin': {'_stub': True, 
                         'id': (
                              'models.AutoField', [], {'primary_key': 'True'})}, 
       'cms.page': {'Meta': {'ordering': "('tree_id','lft')"}, '_stub': True, 
                    'id': (
                         'models.AutoField', [], {'primary_key': 'True'})}, 
       'link.link': {'Meta': {'_bases': ['cms.models.CMSPlugin']}, 'cmsplugin_ptr': (
                                     'models.OneToOneField', ["orm['cms.CMSPlugin']"], {}), 
                     'name': (
                            'models.CharField', ['_("name")'], {'max_length': '256'}), 
                     'page_link': (
                                 'models.ForeignKey', ["orm['cms.Page']"], {'null': 'True', 'blank': 'True'}), 
                     'url': (
                           'models.URLField', ['_("link")'], {'blank': 'True', 'null': 'True', 'verify_exists': 'True'})}}
    complete_apps = [
     'link']