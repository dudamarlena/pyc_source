# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ramusus/workspace/manufacture_old/env/src/django-facebook-users/facebook_users/migrations/0003_auto__add_field_user_first_name__add_field_user_last_name__add_field_u.py
# Compiled at: 2015-03-06 07:15:54
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        db.add_column('facebook_users_user', 'first_name', self.gf('django.db.models.fields.CharField')(default='', max_length=300), keep_default=False)
        db.add_column('facebook_users_user', 'last_name', self.gf('django.db.models.fields.CharField')(default='', max_length=300), keep_default=False)
        db.add_column('facebook_users_user', 'middle_name', self.gf('django.db.models.fields.CharField')(default='', max_length=300), keep_default=False)
        db.add_column('facebook_users_user', 'gender', self.gf('django.db.models.fields.CharField')(default='', max_length=10), keep_default=False)
        db.add_column('facebook_users_user', 'locale', self.gf('django.db.models.fields.CharField')(default='', max_length=5), keep_default=False)
        db.add_column('facebook_users_user', 'link', self.gf('django.db.models.fields.URLField')(default='', max_length=300), keep_default=False)
        db.add_column('facebook_users_user', 'cover', self.gf('annoying.fields.JSONField')(max_length=500, null=True), keep_default=False)
        db.add_column('facebook_users_user', 'username', self.gf('django.db.models.fields.CharField')(default='', max_length=300), keep_default=False)
        db.add_column('facebook_users_user', 'third_party_id', self.gf('django.db.models.fields.CharField')(default='', max_length=300), keep_default=False)
        db.add_column('facebook_users_user', 'updated_time', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(1970, 1, 1, 0, 0)), keep_default=False)
        db.add_column('facebook_users_user', 'email', self.gf('django.db.models.fields.CharField')(default='', max_length=100), keep_default=False)
        db.add_column('facebook_users_user', 'timezone', self.gf('django.db.models.fields.IntegerField')(null=True), keep_default=False)
        db.add_column('facebook_users_user', 'bio', self.gf('django.db.models.fields.TextField')(default=''), keep_default=False)
        db.add_column('facebook_users_user', 'birthday', self.gf('django.db.models.fields.CharField')(default='', max_length=300), keep_default=False)
        db.add_column('facebook_users_user', 'languages', self.gf('annoying.fields.JSONField')(max_length=500, null=True), keep_default=False)
        db.add_column('facebook_users_user', 'installed', self.gf('annoying.fields.JSONField')(max_length=500, null=True), keep_default=False)
        db.add_column('facebook_users_user', 'verified', self.gf('django.db.models.fields.BooleanField')(default=False), keep_default=False)
        db.add_column('facebook_users_user', 'currency', self.gf('annoying.fields.JSONField')(max_length=500, null=True), keep_default=False)
        db.add_column('facebook_users_user', 'devices', self.gf('annoying.fields.JSONField')(max_length=500, null=True), keep_default=False)
        db.add_column('facebook_users_user', 'education', self.gf('annoying.fields.JSONField')(max_length=500, null=True), keep_default=False)
        db.add_column('facebook_users_user', 'hometown', self.gf('annoying.fields.JSONField')(max_length=500, null=True), keep_default=False)
        db.add_column('facebook_users_user', 'interested_in', self.gf('annoying.fields.JSONField')(max_length=500, null=True), keep_default=False)
        db.add_column('facebook_users_user', 'location', self.gf('annoying.fields.JSONField')(max_length=500, null=True), keep_default=False)
        db.add_column('facebook_users_user', 'payment_pricepoints', self.gf('annoying.fields.JSONField')(max_length=500, null=True), keep_default=False)
        db.add_column('facebook_users_user', 'favorite_athletes', self.gf('annoying.fields.JSONField')(max_length=500, null=True), keep_default=False)
        db.add_column('facebook_users_user', 'favorite_teams', self.gf('annoying.fields.JSONField')(max_length=500, null=True), keep_default=False)
        db.add_column('facebook_users_user', 'political', self.gf('django.db.models.fields.CharField')(default='', max_length=100), keep_default=False)
        db.add_column('facebook_users_user', 'picture', self.gf('django.db.models.fields.CharField')(default='', max_length=100), keep_default=False)
        db.add_column('facebook_users_user', 'quotes', self.gf('django.db.models.fields.CharField')(default='', max_length=100), keep_default=False)
        db.add_column('facebook_users_user', 'relationship_status', self.gf('django.db.models.fields.CharField')(default='', max_length=100), keep_default=False)
        db.add_column('facebook_users_user', 'religion', self.gf('django.db.models.fields.CharField')(default='', max_length=100), keep_default=False)
        db.add_column('facebook_users_user', 'security_settings', self.gf('annoying.fields.JSONField')(max_length=500, null=True), keep_default=False)
        db.add_column('facebook_users_user', 'significant_other', self.gf('annoying.fields.JSONField')(max_length=500, null=True), keep_default=False)
        db.add_column('facebook_users_user', 'video_upload_limits', self.gf('annoying.fields.JSONField')(max_length=500, null=True), keep_default=False)
        db.add_column('facebook_users_user', 'website', self.gf('django.db.models.fields.URLField')(default='', max_length=100), keep_default=False)
        db.add_column('facebook_users_user', 'work', self.gf('annoying.fields.JSONField')(max_length=500, null=True), keep_default=False)

    def backwards(self, orm):
        db.delete_column('facebook_users_user', 'first_name')
        db.delete_column('facebook_users_user', 'last_name')
        db.delete_column('facebook_users_user', 'middle_name')
        db.delete_column('facebook_users_user', 'gender')
        db.delete_column('facebook_users_user', 'locale')
        db.delete_column('facebook_users_user', 'link')
        db.delete_column('facebook_users_user', 'cover')
        db.delete_column('facebook_users_user', 'username')
        db.delete_column('facebook_users_user', 'third_party_id')
        db.delete_column('facebook_users_user', 'updated_time')
        db.delete_column('facebook_users_user', 'email')
        db.delete_column('facebook_users_user', 'timezone')
        db.delete_column('facebook_users_user', 'bio')
        db.delete_column('facebook_users_user', 'birthday')
        db.delete_column('facebook_users_user', 'languages')
        db.delete_column('facebook_users_user', 'installed')
        db.delete_column('facebook_users_user', 'verified')
        db.delete_column('facebook_users_user', 'currency')
        db.delete_column('facebook_users_user', 'devices')
        db.delete_column('facebook_users_user', 'education')
        db.delete_column('facebook_users_user', 'hometown')
        db.delete_column('facebook_users_user', 'interested_in')
        db.delete_column('facebook_users_user', 'location')
        db.delete_column('facebook_users_user', 'payment_pricepoints')
        db.delete_column('facebook_users_user', 'favorite_athletes')
        db.delete_column('facebook_users_user', 'favorite_teams')
        db.delete_column('facebook_users_user', 'political')
        db.delete_column('facebook_users_user', 'picture')
        db.delete_column('facebook_users_user', 'quotes')
        db.delete_column('facebook_users_user', 'relationship_status')
        db.delete_column('facebook_users_user', 'religion')
        db.delete_column('facebook_users_user', 'security_settings')
        db.delete_column('facebook_users_user', 'significant_other')
        db.delete_column('facebook_users_user', 'video_upload_limits')
        db.delete_column('facebook_users_user', 'website')
        db.delete_column('facebook_users_user', 'work')

    models = {'facebook_users.user': {'Meta': {'ordering': "['name']", 'object_name': 'User'}, 'bio': (
                                     'django.db.models.fields.TextField', [], {}), 
                               'birthday': (
                                          'django.db.models.fields.CharField', [], {'max_length': '300'}), 
                               'cover': (
                                       'annoying.fields.JSONField', [], {'max_length': '500', 'null': 'True'}), 
                               'currency': (
                                          'annoying.fields.JSONField', [], {'max_length': '500', 'null': 'True'}), 
                               'devices': (
                                         'annoying.fields.JSONField', [], {'max_length': '500', 'null': 'True'}), 
                               'education': (
                                           'annoying.fields.JSONField', [], {'max_length': '500', 'null': 'True'}), 
                               'email': (
                                       'django.db.models.fields.CharField', [], {'max_length': '100'}), 
                               'favorite_athletes': (
                                                   'annoying.fields.JSONField', [], {'max_length': '500', 'null': 'True'}), 
                               'favorite_teams': (
                                                'annoying.fields.JSONField', [], {'max_length': '500', 'null': 'True'}), 
                               'first_name': (
                                            'django.db.models.fields.CharField', [], {'max_length': '300'}), 
                               'gender': (
                                        'django.db.models.fields.CharField', [], {'max_length': '10'}), 
                               'graph_id': (
                                          'django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}), 
                               'hometown': (
                                          'annoying.fields.JSONField', [], {'max_length': '500', 'null': 'True'}), 
                               'id': (
                                    'django.db.models.fields.AutoField', [], {'primary_key': 'True'}), 
                               'installed': (
                                           'annoying.fields.JSONField', [], {'max_length': '500', 'null': 'True'}), 
                               'interested_in': (
                                               'annoying.fields.JSONField', [], {'max_length': '500', 'null': 'True'}), 
                               'languages': (
                                           'annoying.fields.JSONField', [], {'max_length': '500', 'null': 'True'}), 
                               'last_name': (
                                           'django.db.models.fields.CharField', [], {'max_length': '300'}), 
                               'link': (
                                      'django.db.models.fields.URLField', [], {'max_length': '300'}), 
                               'locale': (
                                        'django.db.models.fields.CharField', [], {'max_length': '5'}), 
                               'location': (
                                          'annoying.fields.JSONField', [], {'max_length': '500', 'null': 'True'}), 
                               'middle_name': (
                                             'django.db.models.fields.CharField', [], {'max_length': '300'}), 
                               'name': (
                                      'django.db.models.fields.CharField', [], {'max_length': '300'}), 
                               'payment_pricepoints': (
                                                     'annoying.fields.JSONField', [], {'max_length': '500', 'null': 'True'}), 
                               'picture': (
                                         'django.db.models.fields.CharField', [], {'max_length': '100'}), 
                               'political': (
                                           'django.db.models.fields.CharField', [], {'max_length': '100'}), 
                               'quotes': (
                                        'django.db.models.fields.CharField', [], {'max_length': '100'}), 
                               'relationship_status': (
                                                     'django.db.models.fields.CharField', [], {'max_length': '100'}), 
                               'religion': (
                                          'django.db.models.fields.CharField', [], {'max_length': '100'}), 
                               'security_settings': (
                                                   'annoying.fields.JSONField', [], {'max_length': '500', 'null': 'True'}), 
                               'significant_other': (
                                                   'annoying.fields.JSONField', [], {'max_length': '500', 'null': 'True'}), 
                               'third_party_id': (
                                                'django.db.models.fields.CharField', [], {'max_length': '300'}), 
                               'timezone': (
                                          'django.db.models.fields.IntegerField', [], {'null': 'True'}), 
                               'updated_time': (
                                              'django.db.models.fields.DateTimeField', [], {}), 
                               'username': (
                                          'django.db.models.fields.CharField', [], {'max_length': '300'}), 
                               'verified': (
                                          'django.db.models.fields.BooleanField', [], {'default': 'False'}), 
                               'video_upload_limits': (
                                                     'annoying.fields.JSONField', [], {'max_length': '500', 'null': 'True'}), 
                               'website': (
                                         'django.db.models.fields.URLField', [], {'max_length': '100'}), 
                               'work': (
                                      'annoying.fields.JSONField', [], {'max_length': '500', 'null': 'True'})}}
    complete_apps = [
     'facebook_users']