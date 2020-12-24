# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/vwa13376/workspace/uploader/archer/packages/migrations/0002_auto__chg_field_package_file.py
# Compiled at: 2013-08-08 04:50:11
from south.db import db
from south.v2 import SchemaMigration

class Migration(SchemaMigration):

    def forwards(self, orm):
        db.alter_column('packages_package', 'file', self.gf('django.db.models.fields.files.FileField')(max_length=1024))

    def backwards(self, orm):
        db.alter_column('packages_package', 'file', self.gf('django.db.models.fields.files.FileField')(max_length=100))

    models = {'packages.package': {'Meta': {'object_name': 'Package'}, 'created_at': (
                                         'django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}), 
                            'file': (
                                   'django.db.models.fields.files.FileField', [], {'max_length': '1024'}), 
                            'id': (
                                 'django.db.models.fields.AutoField', [], {'primary_key': 'True'}), 
                            'project': (
                                      'django.db.models.fields.related.ForeignKey', [], {'to': "orm['projects.Project']"}), 
                            'status': (
                                     'django.db.models.fields.IntegerField', [], {}), 
                            'updated_at': (
                                         'django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})}, 
       'projects.filesystem': {'Meta': {'object_name': 'FileSystem'}, 'id': (
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
     'packages']