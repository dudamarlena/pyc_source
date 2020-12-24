# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-intel/egg/djangopypi/migrations/0002_refactoring.py
# Compiled at: 2015-10-27 08:49:00
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        db.delete_table('djangopypi_project')
        db.delete_table('djangopypi_project_classifiers')
        db.create_table('djangopypi_distribution', (
         (
          'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
         (
          'release', self.gf('django.db.models.fields.related.ForeignKey')(related_name='distributions', to=orm['djangopypi.Release'])),
         (
          'content', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
         (
          'md5_digest', self.gf('django.db.models.fields.CharField')(max_length=32, blank=True)),
         (
          'filetype', self.gf('django.db.models.fields.CharField')(max_length=32)),
         (
          'pyversion', self.gf('django.db.models.fields.CharField')(max_length=16, blank=True)),
         (
          'comment', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
         (
          'signature', self.gf('django.db.models.fields.TextField')(blank=True)),
         (
          'created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
         (
          'uploader', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User']))))
        db.send_create_signal('djangopypi', ['Distribution'])
        db.create_table('djangopypi_review', (
         (
          'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
         (
          'release', self.gf('django.db.models.fields.related.ForeignKey')(related_name='reviews', to=orm['djangopypi.Release'])),
         (
          'rating', self.gf('django.db.models.fields.PositiveSmallIntegerField')(blank=True)),
         (
          'comment', self.gf('django.db.models.fields.TextField')(blank=True))))
        db.send_create_signal('djangopypi', ['Review'])
        db.create_table('djangopypi_package', (
         (
          'name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255, primary_key=True)),
         (
          'auto_hide', self.gf('django.db.models.fields.BooleanField')(default=True, blank=True)),
         (
          'allow_comments', self.gf('django.db.models.fields.BooleanField')(default=True, blank=True))))
        db.send_create_signal('djangopypi', ['Package'])
        db.create_table('djangopypi_package_owners', (
         (
          'id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
         (
          'package', models.ForeignKey(orm['djangopypi.package'], null=False)),
         (
          'user', models.ForeignKey(orm['auth.user'], null=False))))
        db.create_unique('djangopypi_package_owners', ['package_id', 'user_id'])
        db.create_table('djangopypi_package_maintainers', (
         (
          'id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
         (
          'package', models.ForeignKey(orm['djangopypi.package'], null=False)),
         (
          'user', models.ForeignKey(orm['auth.user'], null=False))))
        db.create_unique('djangopypi_package_maintainers', ['package_id', 'user_id'])
        db.delete_column('djangopypi_classifier', 'id')
        db.alter_column('djangopypi_classifier', 'name', self.gf('django.db.models.fields.CharField')(max_length=255, primary_key=True))
        db.delete_column('djangopypi_release', 'md5_digest')
        db.delete_column('djangopypi_release', 'filetype')
        db.delete_column('djangopypi_release', 'upload_time')
        db.delete_column('djangopypi_release', 'pyversion')
        db.delete_column('djangopypi_release', 'project_id')
        db.delete_column('djangopypi_release', 'platform')
        db.delete_column('djangopypi_release', 'signature')
        db.delete_column('djangopypi_release', 'distribution')
        db.add_column('djangopypi_release', 'package', self.gf('django.db.models.fields.related.ForeignKey')(default='', related_name='releases', to=orm['djangopypi.Package']), keep_default=False)
        db.add_column('djangopypi_release', 'metadata_version', self.gf('django.db.models.fields.CharField')(default='1.0', max_length=64), keep_default=False)
        db.add_column('djangopypi_release', 'package_info', self.gf('djangopypi.models.PackageInfoField')(default=''), keep_default=False)
        db.add_column('djangopypi_release', 'hidden', self.gf('django.db.models.fields.BooleanField')(default=False, blank=True), keep_default=False)
        db.add_column('djangopypi_release', 'created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, default='1970-01-01 00:00:00', blank=True), keep_default=False)
        db.delete_unique('djangopypi_release', ['project_id', 'platform', 'distribution', 'version', 'pyversion'])
        db.create_unique('djangopypi_release', ['version', 'package_id'])

    def backwards(self, orm):
        db.create_table('djangopypi_project', (
         (
          'updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
         (
          'description', self.gf('django.db.models.fields.TextField')(blank=True)),
         (
          'metadata_version', self.gf('django.db.models.fields.CharField')(default=1.0, max_length=64)),
         (
          'owner', self.gf('django.db.models.fields.related.ForeignKey')(related_name='projects', to=orm['auth.User'])),
         (
          'summary', self.gf('django.db.models.fields.TextField')(blank=True)),
         (
          'name', self.gf('django.db.models.fields.CharField')(max_length=255, unique=True)),
         (
          'license', self.gf('django.db.models.fields.TextField')(blank=True)),
         (
          'author', self.gf('django.db.models.fields.CharField')(max_length=128, blank=True)),
         (
          'home_page', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
         (
          'download_url', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
         (
          'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
         (
          'author_email', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True))))
        db.send_create_signal('djangopypi', ['Project'])
        db.create_table('djangopypi_project_classifiers', (
         (
          'id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
         (
          'project', models.ForeignKey(orm['djangopypi.project'], null=False)),
         (
          'classifier', models.ForeignKey(orm['djangopypi.classifier'], null=False))))
        db.create_unique('djangopypi_project_classifiers', ['project_id', 'classifier_id'])
        db.delete_table('djangopypi_distribution')
        db.delete_table('djangopypi_review')
        db.delete_table('djangopypi_package')
        db.delete_table('djangopypi_package_owners')
        db.delete_table('djangopypi_package_maintainers')
        db.alter_column('djangopypi_classifier', 'name', self.gf('django.db.models.fields.CharField')(max_length=255, unique=True))
        db.add_column('djangopypi_release', 'md5_digest', self.gf('django.db.models.fields.CharField')(default='', max_length=255, blank=True), keep_default=False)
        db.add_column('djangopypi_release', 'filetype', self.gf('django.db.models.fields.CharField')(default='', max_length=255, blank=True), keep_default=False)
        db.add_column('djangopypi_release', 'upload_time', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, default='1970-01-01 00:00:00', blank=True), keep_default=False)
        db.add_column('djangopypi_release', 'pyversion', self.gf('django.db.models.fields.CharField')(default='', max_length=255, blank=True), keep_default=False)
        db.add_column('djangopypi_release', 'project', self.gf('django.db.models.fields.related.ForeignKey')(default='', related_name='releases', to=orm['djangopypi.Project']), keep_default=False)
        db.add_column('djangopypi_release', 'platform', self.gf('django.db.models.fields.CharField')(default='', max_length=255, blank=True), keep_default=False)
        db.add_column('djangopypi_release', 'signature', self.gf('django.db.models.fields.CharField')(default='', max_length=128, blank=True), keep_default=False)
        db.add_column('djangopypi_release', 'distribution', self.gf('django.db.models.fields.files.FileField')(default='', max_length=100), keep_default=False)
        db.delete_column('djangopypi_release', 'package_id')
        db.delete_column('djangopypi_release', 'metadata_version')
        db.delete_column('djangopypi_release', 'package_info')
        db.delete_column('djangopypi_release', 'hidden')
        db.delete_column('djangopypi_release', 'created')
        db.create_unique('djangopypi_release', ['project_id', 'platform', 'distribution', 'version', 'pyversion'])
        db.delete_unique('djangopypi_release', ['version', 'package_id'])

    models = {'auth.group': {'Meta': {'object_name': 'Group'}, 'id': (
                           'django.db.models.fields.AutoField', [], {'primary_key': 'True'}), 
                      'name': (
                             'django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}), 
                      'permissions': (
                                    'django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})}, 
       'auth.permission': {'Meta': {'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'}, 'codename': (
                                      'django.db.models.fields.CharField', [], {'max_length': '100'}), 
                           'content_type': (
                                          'django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}), 
                           'id': (
                                'django.db.models.fields.AutoField', [], {'primary_key': 'True'}), 
                           'name': (
                                  'django.db.models.fields.CharField', [], {'max_length': '50'})}, 
       'auth.user': {'Meta': {'object_name': 'User'}, 'date_joined': (
                                   'django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}), 
                     'email': (
                             'django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}), 
                     'first_name': (
                                  'django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}), 
                     'groups': (
                              'django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}), 
                     'id': (
                          'django.db.models.fields.AutoField', [], {'primary_key': 'True'}), 
                     'is_active': (
                                 'django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}), 
                     'is_staff': (
                                'django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}), 
                     'is_superuser': (
                                    'django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}), 
                     'last_login': (
                                  'django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}), 
                     'last_name': (
                                 'django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}), 
                     'password': (
                                'django.db.models.fields.CharField', [], {'max_length': '128'}), 
                     'user_permissions': (
                                        'django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}), 
                     'username': (
                                'django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})}, 
       'contenttypes.contenttype': {'Meta': {'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"}, 'app_label': (
                                                'django.db.models.fields.CharField', [], {'max_length': '100'}), 
                                    'id': (
                                         'django.db.models.fields.AutoField', [], {'primary_key': 'True'}), 
                                    'model': (
                                            'django.db.models.fields.CharField', [], {'max_length': '100'}), 
                                    'name': (
                                           'django.db.models.fields.CharField', [], {'max_length': '100'})}, 
       'djangopypi.classifier': {'Meta': {'object_name': 'Classifier'}, 'name': (
                                        'django.db.models.fields.CharField', [], {'max_length': '255', 'primary_key': 'True'})}, 
       'djangopypi.distribution': {'Meta': {'unique_together': "(('release', 'filetype', 'pyversion'),)", 'object_name': 'Distribution'}, 'comment': (
                                             'django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}), 
                                   'content': (
                                             'django.db.models.fields.files.FileField', [], {'max_length': '100'}), 
                                   'created': (
                                             'django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}), 
                                   'filetype': (
                                              'django.db.models.fields.CharField', [], {'max_length': '32'}), 
                                   'id': (
                                        'django.db.models.fields.AutoField', [], {'primary_key': 'True'}), 
                                   'md5_digest': (
                                                'django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'}), 
                                   'pyversion': (
                                               'django.db.models.fields.CharField', [], {'max_length': '16', 'blank': 'True'}), 
                                   'release': (
                                             'django.db.models.fields.related.ForeignKey', [], {'related_name': "'distributions'", 'to': "orm['djangopypi.Release']"}), 
                                   'signature': (
                                               'django.db.models.fields.TextField', [], {'blank': 'True'}), 
                                   'uploader': (
                                              'django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})}, 
       'djangopypi.package': {'Meta': {'object_name': 'Package'}, 'allow_comments': (
                                               'django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}), 
                              'auto_hide': (
                                          'django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}), 
                              'maintainers': (
                                            'django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'packages_maintained'", 'blank': 'True', 'to': "orm['auth.User']"}), 
                              'name': (
                                     'django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255', 'primary_key': 'True'}), 
                              'owners': (
                                       'django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'packages_owned'", 'blank': 'True', 'to': "orm['auth.User']"})}, 
       'djangopypi.release': {'Meta': {'unique_together': "(('package', 'version'),)", 'object_name': 'Release'}, 'created': (
                                        'django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}), 
                              'hidden': (
                                       'django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}), 
                              'id': (
                                   'django.db.models.fields.AutoField', [], {'primary_key': 'True'}), 
                              'metadata_version': (
                                                 'django.db.models.fields.CharField', [], {'default': "'1.0'", 'max_length': '64'}), 
                              'package': (
                                        'django.db.models.fields.related.ForeignKey', [], {'related_name': "'releases'", 'to': "orm['djangopypi.Package']"}), 
                              'package_info': (
                                             'djangopypi.models.PackageInfoField', [], {}), 
                              'version': (
                                        'django.db.models.fields.CharField', [], {'max_length': '128'})}, 
       'djangopypi.review': {'Meta': {'object_name': 'Review'}, 'comment': (
                                       'django.db.models.fields.TextField', [], {'blank': 'True'}), 
                             'id': (
                                  'django.db.models.fields.AutoField', [], {'primary_key': 'True'}), 
                             'rating': (
                                      'django.db.models.fields.PositiveSmallIntegerField', [], {'blank': 'True'}), 
                             'release': (
                                       'django.db.models.fields.related.ForeignKey', [], {'related_name': "'reviews'", 'to': "orm['djangopypi.Release']"})}}
    complete_apps = [
     'djangopypi']