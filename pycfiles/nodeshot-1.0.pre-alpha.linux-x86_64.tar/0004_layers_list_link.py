# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/nodeshot/core/cms/migrations/0004_layers_list_link.py
# Compiled at: 2015-02-07 15:27:20
import datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models

class Migration(DataMigration):
    OLD_STRING = "javascript:$.createModal({message:'not implemented yet'})"
    NEW_STRING = '#layers'

    def forwards(self, orm):
        """Write your forwards methods here."""
        for menuitem in orm['cms.menuitem'].objects.filter(name__iexact='layers'):
            menuitem.url = self.NEW_STRING
            menuitem.save()

    def backwards(self, orm):
        """Write your backwards methods here."""
        for menuitem in orm['cms.menuitem'].objects.filter(name__iexact='layers'):
            menuitem.url = self.OLD_STRING
            menuitem.save()

    models = {'cms.menuitem': {'Meta': {'ordering': "['order']", 'object_name': 'MenuItem'}, 'access_level': (
                                       'django.db.models.fields.SmallIntegerField', [], {'default': '0'}), 
                        'added': (
                                'django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 11, 28, 0, 0)'}), 
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
                                  'django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 11, 28, 0, 0)'}), 
                        'url': (
                              'django.db.models.fields.CharField', [], {'max_length': '255'})}, 
       'cms.page': {'Meta': {'object_name': 'Page'}, 'access_level': (
                                   'django.db.models.fields.SmallIntegerField', [], {'default': '0'}), 
                    'added': (
                            'django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 11, 28, 0, 0)'}), 
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
                              'django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 11, 28, 0, 0)'})}}
    complete_apps = [
     'cms']
    symmetrical = True