# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/vwa13376/workspace/uploader/archer/projects/migrations/0001_initial.py
# Compiled at: 2013-08-08 04:50:11
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        db.create_table('projects_filesystem', (
         (
          'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
         (
          'mount_point', self.gf('django.db.models.fields.CharField')(unique=True, max_length=2000))))
        db.send_create_signal('projects', ['FileSystem'])
        db.create_table('projects_project', (
         (
          'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
         (
          'file_system', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['projects.FileSystem'])),
         (
          'directory', self.gf('django.db.models.fields.CharField')(max_length=200))))
        db.send_create_signal('projects', ['Project'])
        db.create_unique('projects_project', ['file_system_id', 'directory'])

    def backwards(self, orm):
        db.delete_unique('projects_project', ['file_system_id', 'directory'])
        db.delete_table('projects_filesystem')
        db.delete_table('projects_project')

    models = {'projects.filesystem': {'Meta': {'object_name': 'FileSystem'}, 'id': (
                                    'django.db.models.fields.AutoField', [], {'primary_key': 'True'}), 
                               'mount_point': (
                                             'django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '2000'})}, 
       'projects.project': {'Meta': {'unique_together': "(('file_system', 'directory'),)", 'object_name': 'Project'}, 'directory': (
                                        'django.db.models.fields.CharField', [], {'max_length': '200'}), 
                            'file_system': (
                                          'django.db.models.fields.related.ForeignKey', [], {'to': "orm['projects.FileSystem']"}), 
                            'id': (
                                 'django.db.models.fields.AutoField', [], {'primary_key': 'True'})}}
    complete_apps = [
     'projects']