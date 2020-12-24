# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/rerb/src/aashe/django-membersuite-auth/django_membersuite_auth/migrations/0001_initial.py
# Compiled at: 2019-01-16 12:27:58
import django
from django.conf import settings
from django.db import models
from distutils.version import StrictVersion
if StrictVersion(django.get_version()) < StrictVersion('1.7'):
    from south.db import db
    from south.v2 import SchemaMigration

    class Migration(SchemaMigration):

        def forwards(self, orm):
            db.create_table('django_membersuite_auth_membersuiteportaluser', (
             (
              'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
             (
              'user',
              self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True)),
             (
              'membersuite_id',
              self.gf('django.db.models.fields.CharField')(unique=True, max_length=64)),
             (
              'is_member',
              self.gf('django.db.models.fields.BooleanField')(default=False))))
            db.send_create_signal('django_membersuite_auth', [
             'MemberSuitePortalUser'])

        def backwards(self, orm):
            db.delete_table('django_membersuite_auth_membersuiteportaluser')

        models = {'auth.group': {'Meta': {'object_name': 'Group'}, 'id': (
                               'django.db.models.fields.AutoField', [], {'primary_key': 'True'}), 
                          'name': (
                                 'django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}), 
                          'permissions': (
                                        'django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})}, 
           'auth.permission': {'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'}, 'codename': (
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
                                     'django.db.models.fields.BooleanField', [], {'default': 'True'}), 
                         'is_staff': (
                                    'django.db.models.fields.BooleanField', [], {'default': 'False'}), 
                         'is_superuser': (
                                        'django.db.models.fields.BooleanField', [], {'default': 'False'}), 
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
           'contenttypes.contenttype': {'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"}, 'app_label': (
                                                    'django.db.models.fields.CharField', [], {'max_length': '100'}), 
                                        'id': (
                                             'django.db.models.fields.AutoField', [], {'primary_key': 'True'}), 
                                        'model': (
                                                'django.db.models.fields.CharField', [], {'max_length': '100'}), 
                                        'name': (
                                               'django.db.models.fields.CharField', [], {'max_length': '100'})}, 
           'django_membersuite_auth.membersuiteportaluser': {'Meta': {'object_name': 'MemberSuitePortalUser'}, 'id': (
                                                                  'django.db.models.fields.AutoField', [], {'primary_key': 'True'}), 
                                                             'is_member': (
                                                                         'django.db.models.fields.BooleanField', [], {'default': 'False'}), 
                                                             'membersuite_id': (
                                                                              'django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '64'}), 
                                                             'user': (
                                                                    'django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True'})}}
        complete_apps = [
         'django_membersuite_auth']


else:
    import django.db.models.deletion
    from django.db import migrations

    class Migration(migrations.Migration):
        initial = True
        dependencies = [
         migrations.swappable_dependency(settings.AUTH_USER_MODEL)]
        operations = [
         migrations.CreateModel(name='MemberSuitePortalUser', fields=[
          (
           'id',
           models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
          (
           'membersuite_id',
           models.CharField(max_length=64, unique=True)),
          (
           'is_member',
           models.BooleanField(default=False)),
          (
           'user',
           models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL))])]