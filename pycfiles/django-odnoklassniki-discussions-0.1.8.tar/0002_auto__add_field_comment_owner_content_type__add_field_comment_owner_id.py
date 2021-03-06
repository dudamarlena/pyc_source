# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ramusus/workspace/manufacture_old/env/src/django-odnoklassniki-discussions/odnoklassniki_discussions/migrations/0002_auto__add_field_comment_owner_content_type__add_field_comment_owner_id.py
# Compiled at: 2015-03-06 07:17:02
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        db.add_column('odnoklassniki_discussions_comment', 'owner_content_type', self.gf('django.db.models.fields.related.ForeignKey')(default=None, related_name='odnoklassniki_comments_owners', to=orm['contenttypes.ContentType']), keep_default=False)
        db.add_column('odnoklassniki_discussions_comment', 'owner_id', self.gf('django.db.models.fields.BigIntegerField')(default=None, db_index=True), keep_default=False)
        return

    def backwards(self, orm):
        db.delete_column('odnoklassniki_discussions_comment', 'owner_content_type_id')
        db.delete_column('odnoklassniki_discussions_comment', 'owner_id')

    models = {'contenttypes.contenttype': {'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"}, 'app_label': (
                                                'django.db.models.fields.CharField', [], {'max_length': '100'}), 
                                    'id': (
                                         'django.db.models.fields.AutoField', [], {'primary_key': 'True'}), 
                                    'model': (
                                            'django.db.models.fields.CharField', [], {'max_length': '100'}), 
                                    'name': (
                                           'django.db.models.fields.CharField', [], {'max_length': '100'})}, 
       'odnoklassniki_discussions.comment': {'Meta': {'object_name': 'Comment'}, 'attrs': (
                                                     'annoying.fields.JSONField', [], {'null': 'True'}), 
                                             'author_content_type': (
                                                                   'django.db.models.fields.related.ForeignKey', [], {'related_name': "'odnoklassniki_comments_authors'", 'to': "orm['contenttypes.ContentType']"}), 
                                             'author_id': (
                                                         'django.db.models.fields.BigIntegerField', [], {'db_index': 'True'}), 
                                             'date': (
                                                    'django.db.models.fields.DateTimeField', [], {}), 
                                             'discussion': (
                                                          'django.db.models.fields.related.ForeignKey', [], {'related_name': "'comments'", 'to': "orm['odnoklassniki_discussions.Discussion']"}), 
                                             'fetched': (
                                                       'django.db.models.fields.DateTimeField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}), 
                                             'id': (
                                                  'django.db.models.fields.CharField', [], {'max_length': '68', 'primary_key': 'True'}), 
                                             'liked_it': (
                                                        'django.db.models.fields.BooleanField', [], {'default': 'False'}), 
                                             'likes_count': (
                                                           'django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}), 
                                             'owner_content_type': (
                                                                  'django.db.models.fields.related.ForeignKey', [], {'related_name': "'odnoklassniki_comments_owners'", 'to': "orm['contenttypes.ContentType']"}), 
                                             'owner_id': (
                                                        'django.db.models.fields.BigIntegerField', [], {'db_index': 'True'}), 
                                             'reply_to_author_content_type': (
                                                                            'django.db.models.fields.related.ForeignKey', [], {'related_name': "'odnoklassniki_comments_reply_to_authors'", 'null': 'True', 'to': "orm['contenttypes.ContentType']"}), 
                                             'reply_to_author_id': (
                                                                  'django.db.models.fields.BigIntegerField', [], {'null': 'True', 'db_index': 'True'}), 
                                             'reply_to_comment': (
                                                                'django.db.models.fields.related.ForeignKey', [], {'to': "orm['odnoklassniki_discussions.Comment']", 'null': 'True'}), 
                                             'text': (
                                                    'django.db.models.fields.TextField', [], {}), 
                                             'type': (
                                                    'django.db.models.fields.CharField', [], {'max_length': '20'})}, 
       'odnoklassniki_discussions.discussion': {'Meta': {'object_name': 'Discussion'}, 'attrs': (
                                                        'annoying.fields.JSONField', [], {'null': 'True'}), 
                                                'author_content_type': (
                                                                      'django.db.models.fields.related.ForeignKey', [], {'related_name': "'odnoklassniki_discussions_authors'", 'to': "orm['contenttypes.ContentType']"}), 
                                                'author_id': (
                                                            'django.db.models.fields.BigIntegerField', [], {'db_index': 'True'}), 
                                                'comments_count': (
                                                                 'django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}), 
                                                'date': (
                                                       'django.db.models.fields.DateTimeField', [], {}), 
                                                'entities': (
                                                           'annoying.fields.JSONField', [], {'null': 'True'}), 
                                                'fetched': (
                                                          'django.db.models.fields.DateTimeField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}), 
                                                'id': (
                                                     'django.db.models.fields.BigIntegerField', [], {'primary_key': 'True'}), 
                                                'last_activity_date': (
                                                                     'django.db.models.fields.DateTimeField', [], {'null': 'True'}), 
                                                'last_user_access_date': (
                                                                        'django.db.models.fields.DateTimeField', [], {'null': 'True'}), 
                                                'liked_it': (
                                                           'django.db.models.fields.BooleanField', [], {'default': 'False'}), 
                                                'likes_count': (
                                                              'django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}), 
                                                'message': (
                                                          'django.db.models.fields.TextField', [], {}), 
                                                'new_comments_count': (
                                                                     'django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}), 
                                                'owner_content_type': (
                                                                     'django.db.models.fields.related.ForeignKey', [], {'related_name': "'odnoklassniki_discussions_owners'", 'to': "orm['contenttypes.ContentType']"}), 
                                                'owner_id': (
                                                           'django.db.models.fields.BigIntegerField', [], {'db_index': 'True'}), 
                                                'ref_objects': (
                                                              'annoying.fields.JSONField', [], {'null': 'True'}), 
                                                'title': (
                                                        'django.db.models.fields.TextField', [], {}), 
                                                'type': (
                                                       'django.db.models.fields.CharField', [], {'max_length': '20'})}}
    complete_apps = [
     'odnoklassniki_discussions']