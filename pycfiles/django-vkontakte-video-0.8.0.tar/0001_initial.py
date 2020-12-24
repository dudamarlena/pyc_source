# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ramusus/workspace/manufacture_old/env/src/django-vkontakte-video/vkontakte_video/migrations/0001_initial.py
# Compiled at: 2015-03-06 07:14:43
from django.db import models
from south.db import db
from south.utils import datetime_utils as datetime
from south.v2 import SchemaMigration

class Migration(SchemaMigration):

    def forwards(self, orm):
        db.create_table('vkontakte_video_album', (
         (
          'fetched', self.gf('django.db.models.fields.DateTimeField')(db_index=True, null=True, blank=True)),
         (
          'remote_id', self.gf('django.db.models.fields.BigIntegerField')(primary_key=True)),
         (
          'owner_content_type',
          self.gf('django.db.models.fields.related.ForeignKey')(related_name='content_type_owners_vkontakte_video_albums', null=True, to=orm['contenttypes.ContentType'])),
         (
          'owner_id', self.gf('django.db.models.fields.BigIntegerField')(null=True, db_index=True)),
         (
          'photo_160', self.gf('django.db.models.fields.URLField')(default='', max_length=255)),
         (
          'videos_count', self.gf('django.db.models.fields.PositiveIntegerField')()),
         (
          'title', self.gf('django.db.models.fields.CharField')(max_length='200'))))
        db.send_create_signal('vkontakte_video', ['Album'])
        db.create_table('vkontakte_video_video', (
         (
          'fetched', self.gf('django.db.models.fields.DateTimeField')(db_index=True, null=True, blank=True)),
         (
          'remote_id', self.gf('django.db.models.fields.BigIntegerField')(primary_key=True)),
         (
          'owner_content_type',
          self.gf('django.db.models.fields.related.ForeignKey')(related_name='content_type_owners_vkontakte_video_videos', null=True, to=orm['contenttypes.ContentType'])),
         (
          'owner_id', self.gf('django.db.models.fields.BigIntegerField')(null=True, db_index=True)),
         (
          'likes_count', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, db_index=True)),
         (
          'comments_count', self.gf('django.db.models.fields.PositiveIntegerField')(null=True)),
         (
          'album',
          self.gf('django.db.models.fields.related.ForeignKey')(related_name='videos', null=True, to=orm['vkontakte_video.Album'])),
         (
          'title', self.gf('django.db.models.fields.CharField')(max_length=255)),
         (
          'description', self.gf('django.db.models.fields.TextField')()),
         (
          'duration', self.gf('django.db.models.fields.PositiveIntegerField')()),
         (
          'views_count', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
         (
          'link', self.gf('django.db.models.fields.URLField')(max_length=255)),
         (
          'photo_130', self.gf('django.db.models.fields.URLField')(max_length=255)),
         (
          'player', self.gf('django.db.models.fields.URLField')(max_length=255)),
         (
          'date', self.gf('django.db.models.fields.DateTimeField')(db_index=True))))
        db.send_create_signal('vkontakte_video', ['Video'])
        m2m_table_name = db.shorten_name('vkontakte_video_video_likes_users')
        db.create_table(m2m_table_name, (
         (
          'id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
         (
          'video', models.ForeignKey(orm['vkontakte_video.video'], null=False)),
         (
          'user', models.ForeignKey(orm['vkontakte_users.user'], null=False))))
        db.add_column('vkontakte_video_video_likes_users', 'time_from', self.gf('django.db.models.fields.DateTimeField')(null=True, db_index=True), keep_default=False)
        db.add_column('vkontakte_video_video_likes_users', 'time_to', self.gf('django.db.models.fields.DateTimeField')(null=True, db_index=True), keep_default=False)

    def backwards(self, orm):
        db.delete_table('vkontakte_video_album')
        db.delete_table('vkontakte_video_video')
        db.delete_table(db.shorten_name('vkontakte_video_video_likes_users'))

    models = {'contenttypes.contenttype': {'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"}, 'app_label': (
                                                'django.db.models.fields.CharField', [], {'max_length': '100'}), 
                                    'id': (
                                         'django.db.models.fields.AutoField', [], {'primary_key': 'True'}), 
                                    'model': (
                                            'django.db.models.fields.CharField', [], {'max_length': '100'}), 
                                    'name': (
                                           'django.db.models.fields.CharField', [], {'max_length': '100'})}, 
       'vkontakte_comments.comment': {'Meta': {'object_name': 'Comment'}, 'archived': (
                                                 'django.db.models.fields.BooleanField', [], {'default': 'False'}), 
                                      'author_content_type': (
                                                            'django.db.models.fields.related.ForeignKey', [], {'related_name': "u'content_type_authors_vkontakte_comments_comments'", 'null': 'True', 'to': "orm['contenttypes.ContentType']"}), 
                                      'author_id': (
                                                  'django.db.models.fields.BigIntegerField', [], {'null': 'True', 'db_index': 'True'}), 
                                      'date': (
                                             'django.db.models.fields.DateTimeField', [], {'db_index': 'True'}), 
                                      'fetched': (
                                                'django.db.models.fields.DateTimeField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}), 
                                      'id': (
                                           'django.db.models.fields.AutoField', [], {'primary_key': 'True'}), 
                                      'likes_count': (
                                                    'django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'db_index': 'True'}), 
                                      'likes_users': (
                                                    'm2m_history.fields.ManyToManyHistoryField', [], {'related_name': "'like_comments'", 'symmetrical': 'False', 'to': "orm['vkontakte_users.User']"}), 
                                      'object_content_type': (
                                                            'django.db.models.fields.related.ForeignKey', [], {'related_name': "'content_type_objects_vkontakte_comments'", 'to': "orm['contenttypes.ContentType']"}), 
                                      'object_id': (
                                                  'django.db.models.fields.BigIntegerField', [], {'db_index': 'True'}), 
                                      'owner_content_type': (
                                                           'django.db.models.fields.related.ForeignKey', [], {'related_name': "u'content_type_owners_vkontakte_comments_comments'", 'null': 'True', 'to': "orm['contenttypes.ContentType']"}), 
                                      'owner_id': (
                                                 'django.db.models.fields.BigIntegerField', [], {'null': 'True', 'db_index': 'True'}), 
                                      'remote_id': (
                                                  'django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '20'}), 
                                      'reply_for_content_type': (
                                                               'django.db.models.fields.related.ForeignKey', [], {'related_name': "'replies'", 'null': 'True', 'to': "orm['contenttypes.ContentType']"}), 
                                      'reply_for_id': (
                                                     'django.db.models.fields.BigIntegerField', [], {'null': 'True', 'db_index': 'True'}), 
                                      'reply_to': (
                                                 'django.db.models.fields.related.ForeignKey', [], {'to': "orm['vkontakte_comments.Comment']", 'null': 'True'}), 
                                      'text': (
                                             'django.db.models.fields.TextField', [], {})}, 
       'vkontakte_places.city': {'Meta': {'object_name': 'City'}, 'area': (
                                        'django.db.models.fields.CharField', [], {'max_length': '100'}), 
                                 'country': (
                                           'django.db.models.fields.related.ForeignKey', [], {'related_name': "'cities'", 'null': 'True', 'to': "orm['vkontakte_places.Country']"}), 
                                 'fetched': (
                                           'django.db.models.fields.DateTimeField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}), 
                                 'id': (
                                      'django.db.models.fields.AutoField', [], {'primary_key': 'True'}), 
                                 'name': (
                                        'django.db.models.fields.CharField', [], {'max_length': '50'}), 
                                 'region': (
                                          'django.db.models.fields.CharField', [], {'max_length': '100'}), 
                                 'remote_id': (
                                             'django.db.models.fields.BigIntegerField', [], {'unique': 'True'})}, 
       'vkontakte_places.country': {'Meta': {'object_name': 'Country'}, 'fetched': (
                                              'django.db.models.fields.DateTimeField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}), 
                                    'id': (
                                         'django.db.models.fields.AutoField', [], {'primary_key': 'True'}), 
                                    'name': (
                                           'django.db.models.fields.CharField', [], {'max_length': '50'}), 
                                    'remote_id': (
                                                'django.db.models.fields.BigIntegerField', [], {'unique': 'True'})}, 
       'vkontakte_users.user': {'Meta': {'object_name': 'User'}, 'about': (
                                        'django.db.models.fields.TextField', [], {}), 
                                'activity': (
                                           'django.db.models.fields.TextField', [], {}), 
                                'albums': (
                                         'django.db.models.fields.PositiveIntegerField', [], {'default': '0'}), 
                                'audios': (
                                         'django.db.models.fields.PositiveIntegerField', [], {'default': '0'}), 
                                'bdate': (
                                        'django.db.models.fields.CharField', [], {'max_length': '100'}), 
                                'books': (
                                        'django.db.models.fields.TextField', [], {}), 
                                'city': (
                                       'django.db.models.fields.related.ForeignKey', [], {'to': "orm['vkontakte_places.City']", 'null': 'True', 'on_delete': 'models.SET_NULL'}), 
                                'counters_updated': (
                                                   'django.db.models.fields.DateTimeField', [], {'null': 'True'}), 
                                'country': (
                                          'django.db.models.fields.related.ForeignKey', [], {'to': "orm['vkontakte_places.Country']", 'null': 'True', 'on_delete': 'models.SET_NULL'}), 
                                'facebook': (
                                           'django.db.models.fields.CharField', [], {'max_length': '500'}), 
                                'facebook_name': (
                                                'django.db.models.fields.CharField', [], {'max_length': '500'}), 
                                'faculty': (
                                          'django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}), 
                                'faculty_name': (
                                               'django.db.models.fields.CharField', [], {'max_length': '500'}), 
                                'fetched': (
                                          'django.db.models.fields.DateTimeField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}), 
                                'first_name': (
                                             'django.db.models.fields.CharField', [], {'max_length': '200'}), 
                                'followers': (
                                            'django.db.models.fields.PositiveIntegerField', [], {'default': '0'}), 
                                'friends': (
                                          'django.db.models.fields.PositiveIntegerField', [], {'default': '0'}), 
                                'friends_count': (
                                                'django.db.models.fields.PositiveIntegerField', [], {'default': '0'}), 
                                'friends_users': (
                                                'django.db.models.fields.related.ManyToManyField', [], {'related_name': "'followers_users'", 'symmetrical': 'False', 'to': "orm['vkontakte_users.User']"}), 
                                'games': (
                                        'django.db.models.fields.TextField', [], {}), 
                                'graduation': (
                                             'django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}), 
                                'has_avatar': (
                                             'django.db.models.fields.BooleanField', [], {'default': 'True', 'db_index': 'True'}), 
                                'has_mobile': (
                                             'django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}), 
                                'home_phone': (
                                             'django.db.models.fields.CharField', [], {'max_length': '50'}), 
                                'interests': (
                                            'django.db.models.fields.TextField', [], {}), 
                                'is_deactivated': (
                                                 'django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}), 
                                'last_name': (
                                            'django.db.models.fields.CharField', [], {'max_length': '200'}), 
                                'livejournal': (
                                              'django.db.models.fields.CharField', [], {'max_length': '500'}), 
                                'mobile_phone': (
                                               'django.db.models.fields.CharField', [], {'max_length': '50'}), 
                                'movies': (
                                         'django.db.models.fields.TextField', [], {}), 
                                'mutual_friends': (
                                                 'django.db.models.fields.PositiveIntegerField', [], {'default': '0'}), 
                                'notes': (
                                        'django.db.models.fields.PositiveIntegerField', [], {'default': '0'}), 
                                'photo': (
                                        'django.db.models.fields.URLField', [], {'max_length': '200'}), 
                                'photo_big': (
                                            'django.db.models.fields.URLField', [], {'max_length': '200'}), 
                                'photo_medium': (
                                               'django.db.models.fields.URLField', [], {'max_length': '200'}), 
                                'photo_medium_rec': (
                                                   'django.db.models.fields.URLField', [], {'max_length': '200'}), 
                                'photo_rec': (
                                            'django.db.models.fields.URLField', [], {'max_length': '200'}), 
                                'rate': (
                                       'django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}), 
                                'relation': (
                                           'django.db.models.fields.SmallIntegerField', [], {'null': 'True'}), 
                                'remote_id': (
                                            'django.db.models.fields.BigIntegerField', [], {'primary_key': 'True'}), 
                                'screen_name': (
                                              'django.db.models.fields.CharField', [], {'max_length': '100', 'db_index': 'True'}), 
                                'sex': (
                                      'django.db.models.fields.IntegerField', [], {'null': 'True'}), 
                                'skype': (
                                        'django.db.models.fields.CharField', [], {'max_length': '500'}), 
                                'subscriptions': (
                                                'django.db.models.fields.PositiveIntegerField', [], {'default': '0'}), 
                                'sum_counters': (
                                               'django.db.models.fields.PositiveIntegerField', [], {'default': '0'}), 
                                'timezone': (
                                           'django.db.models.fields.IntegerField', [], {'null': 'True'}), 
                                'tv': (
                                     'django.db.models.fields.TextField', [], {}), 
                                'twitter': (
                                          'django.db.models.fields.CharField', [], {'max_length': '500'}), 
                                'university': (
                                             'django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}), 
                                'university_name': (
                                                  'django.db.models.fields.CharField', [], {'max_length': '500'}), 
                                'user_photos': (
                                              'django.db.models.fields.PositiveIntegerField', [], {'default': '0'}), 
                                'user_videos': (
                                              'django.db.models.fields.PositiveIntegerField', [], {'default': '0'}), 
                                'videos': (
                                         'django.db.models.fields.PositiveIntegerField', [], {'default': '0'}), 
                                'wall_comments': (
                                                'django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'})}, 
       'vkontakte_video.album': {'Meta': {'object_name': 'Album'}, 'fetched': (
                                           'django.db.models.fields.DateTimeField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}), 
                                 'owner_content_type': (
                                                      'django.db.models.fields.related.ForeignKey', [], {'related_name': "u'content_type_owners_vkontakte_video_albums'", 'null': 'True', 'to': "orm['contenttypes.ContentType']"}), 
                                 'owner_id': (
                                            'django.db.models.fields.BigIntegerField', [], {'null': 'True', 'db_index': 'True'}), 
                                 'photo_160': (
                                             'django.db.models.fields.URLField', [], {'default': "''", 'max_length': '255'}), 
                                 'remote_id': (
                                             'django.db.models.fields.BigIntegerField', [], {'primary_key': 'True'}), 
                                 'title': (
                                         'django.db.models.fields.CharField', [], {'max_length': "'200'"}), 
                                 'videos_count': (
                                                'django.db.models.fields.PositiveIntegerField', [], {})}, 
       'vkontakte_video.video': {'Meta': {'object_name': 'Video'}, 'album': (
                                         'django.db.models.fields.related.ForeignKey', [], {'related_name': "'videos'", 'null': 'True', 'to': "orm['vkontakte_video.Album']"}), 
                                 'comments_count': (
                                                  'django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}), 
                                 'date': (
                                        'django.db.models.fields.DateTimeField', [], {'db_index': 'True'}), 
                                 'description': (
                                               'django.db.models.fields.TextField', [], {}), 
                                 'duration': (
                                            'django.db.models.fields.PositiveIntegerField', [], {}), 
                                 'fetched': (
                                           'django.db.models.fields.DateTimeField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}), 
                                 'likes_count': (
                                               'django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'db_index': 'True'}), 
                                 'likes_users': (
                                               'm2m_history.fields.ManyToManyHistoryField', [], {'related_name': "'like_videos'", 'symmetrical': 'False', 'to': "orm['vkontakte_users.User']"}), 
                                 'link': (
                                        'django.db.models.fields.URLField', [], {'max_length': '255'}), 
                                 'owner_content_type': (
                                                      'django.db.models.fields.related.ForeignKey', [], {'related_name': "u'content_type_owners_vkontakte_video_videos'", 'null': 'True', 'to': "orm['contenttypes.ContentType']"}), 
                                 'owner_id': (
                                            'django.db.models.fields.BigIntegerField', [], {'null': 'True', 'db_index': 'True'}), 
                                 'photo_130': (
                                             'django.db.models.fields.URLField', [], {'max_length': '255'}), 
                                 'player': (
                                          'django.db.models.fields.URLField', [], {'max_length': '255'}), 
                                 'remote_id': (
                                             'django.db.models.fields.BigIntegerField', [], {'primary_key': 'True'}), 
                                 'title': (
                                         'django.db.models.fields.CharField', [], {'max_length': '255'}), 
                                 'views_count': (
                                               'django.db.models.fields.PositiveIntegerField', [], {'default': '0'})}, 
       'vkontakte_wall.post': {'Meta': {'object_name': 'Post'}, 'archived': (
                                          'django.db.models.fields.BooleanField', [], {'default': 'False'}), 
                               'attachments': (
                                             'django.db.models.fields.TextField', [], {}), 
                               'author_content_type': (
                                                     'django.db.models.fields.related.ForeignKey', [], {'related_name': "u'content_type_authors_vkontakte_wall_posts'", 'null': 'True', 'to': "orm['contenttypes.ContentType']"}), 
                               'author_id': (
                                           'django.db.models.fields.BigIntegerField', [], {'null': 'True', 'db_index': 'True'}), 
                               'comments_count': (
                                                'django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}), 
                               'copy_owner_content_type': (
                                                         'django.db.models.fields.related.ForeignKey', [], {'related_name': "'vkontakte_wall_copy_posts'", 'null': 'True', 'to': "orm['contenttypes.ContentType']"}), 
                               'copy_owner_id': (
                                               'django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'db_index': 'True'}), 
                               'copy_post': (
                                           'django.db.models.fields.related.ForeignKey', [], {'related_name': "'wall_reposts'", 'null': 'True', 'to': "orm['vkontakte_wall.Post']"}), 
                               'copy_text': (
                                           'django.db.models.fields.TextField', [], {}), 
                               'date': (
                                      'django.db.models.fields.DateTimeField', [], {'db_index': 'True'}), 
                               'fetched': (
                                         'django.db.models.fields.DateTimeField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}), 
                               'geo': (
                                     'django.db.models.fields.TextField', [], {}), 
                               'id': (
                                    'django.db.models.fields.AutoField', [], {'primary_key': 'True'}), 
                               'likes_count': (
                                             'django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'db_index': 'True'}), 
                               'likes_users': (
                                             'm2m_history.fields.ManyToManyHistoryField', [], {'related_name': "'like_posts'", 'symmetrical': 'False', 'to': "orm['vkontakte_users.User']"}), 
                               'media': (
                                       'django.db.models.fields.TextField', [], {}), 
                               'online': (
                                        'django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True'}), 
                               'owner_content_type': (
                                                    'django.db.models.fields.related.ForeignKey', [], {'related_name': "u'content_type_owners_vkontakte_wall_posts'", 'null': 'True', 'to': "orm['contenttypes.ContentType']"}), 
                               'owner_id': (
                                          'django.db.models.fields.BigIntegerField', [], {'null': 'True', 'db_index': 'True'}), 
                               'post_source': (
                                             'django.db.models.fields.TextField', [], {}), 
                               'raw_html': (
                                          'django.db.models.fields.TextField', [], {}), 
                               'raw_json': (
                                          'annoying.fields.JSONField', [], {'default': '{}', 'null': 'True'}), 
                               'remote_id': (
                                           'django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '20'}), 
                               'reply_count': (
                                             'django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}), 
                               'reposts_count': (
                                               'django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'db_index': 'True'}), 
                               'reposts_users': (
                                               'm2m_history.fields.ManyToManyHistoryField', [], {'related_name': "'reposts_posts'", 'symmetrical': 'False', 'to': "orm['vkontakte_users.User']"}), 
                               'signer_id': (
                                           'django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}), 
                               'text': (
                                      'django.db.models.fields.TextField', [], {})}}
    complete_apps = [
     'vkontakte_video']