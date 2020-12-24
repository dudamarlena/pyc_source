# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/john/pycharm_workspace/sop/unified_platform/libs/unified/shawty/migrations/0001_initial.py
# Compiled at: 2012-11-12 17:53:22
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        db.create_table('shawty_shawtyurl', (
         (
          'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
         (
          'long_url', self.gf('django.db.models.fields.CharField')(max_length=4095)),
         (
          'short_url', self.gf('django.db.models.fields.CharField')(max_length=4095)),
         (
          'short_url_id', self.gf('django.db.models.fields.CharField')(max_length=32)),
         (
          'created_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
         (
          'modified_date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True))))
        db.send_create_signal('shawty', ['ShawtyURL'])

    def backwards(self, orm):
        db.delete_table('shawty_shawtyurl')

    models = {'shawty.shawtyurl': {'Meta': {'object_name': 'ShawtyURL'}, 'created_date': (
                                           'django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}), 
                            'id': (
                                 'django.db.models.fields.AutoField', [], {'primary_key': 'True'}), 
                            'long_url': (
                                       'django.db.models.fields.CharField', [], {'max_length': '4095'}), 
                            'modified_date': (
                                            'django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}), 
                            'short_url': (
                                        'django.db.models.fields.CharField', [], {'max_length': '4095'}), 
                            'short_url_id': (
                                           'django.db.models.fields.CharField', [], {'max_length': '32'})}}
    complete_apps = [
     'shawty']