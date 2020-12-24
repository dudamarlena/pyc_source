# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/nodeshot/core/cms/migrations/0002_auto__add_field_menuitem_classes__add_field_menuitem_parent.py
# Compiled at: 2015-01-18 16:37:18
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        db.add_column('cms_menuitem', 'classes', self.gf('django.db.models.fields.CharField')(default='', max_length=50, blank=True), keep_default=False)
        db.add_column('cms_menuitem', 'parent', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cms.MenuItem'], null=True, blank=True), keep_default=False)

    def backwards(self, orm):
        db.delete_column('cms_menuitem', 'classes')
        db.delete_column('cms_menuitem', 'parent_id')

    models = {'cms.menuitem': {'Meta': {'ordering': "['order']", 'object_name': 'MenuItem'}, 'access_level': (
                                       'django.db.models.fields.SmallIntegerField', [], {'default': '0'}), 
                        'added': (
                                'django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 6, 3, 0, 0)'}), 
                        'classes': (
                                  'django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}), 
                        'id': (
                             'django.db.models.fields.AutoField', [], {'primary_key': 'True'}), 
                        'is_published': (
                                       'django.db.models.fields.BooleanField', [], {'default': 'True'}), 
                        'name': (
                               'django.db.models.fields.CharField', [], {'max_length': '50'}), 
                        'order': (
                                'django.db.models.fields.PositiveIntegerField', [], {'blank': 'True'}), 
                        'parent': (
                                 'django.db.models.fields.related.ForeignKey', [], {'to': "orm['cms.MenuItem']", 'null': 'True', 'blank': 'True'}), 
                        'updated': (
                                  'django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 6, 3, 0, 0)'}), 
                        'url': (
                              'django.db.models.fields.CharField', [], {'max_length': '255'})}, 
       'cms.page': {'Meta': {'object_name': 'Page'}, 'access_level': (
                                   'django.db.models.fields.SmallIntegerField', [], {'default': '0'}), 
                    'added': (
                            'django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 6, 3, 0, 0)'}), 
                    'content': (
                              'django.db.models.fields.TextField', [], {}), 
                    'id': (
                         'django.db.models.fields.AutoField', [], {'primary_key': 'True'}), 
                    'is_published': (
                                   'django.db.models.fields.BooleanField', [], {'default': 'True'}), 
                    'meta_description': (
                                       'django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}), 
                    'meta_keywords': (
                                    'django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}), 
                    'meta_robots': (
                                  'django.db.models.fields.CharField', [], {'default': "'index, follow'", 'max_length': '50'}), 
                    'slug': (
                           'django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50', 'blank': 'True'}), 
                    'title': (
                            'django.db.models.fields.CharField', [], {'max_length': '50'}), 
                    'updated': (
                              'django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 6, 3, 0, 0)'})}}
    complete_apps = [
     'cms']