# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/kevin/virtualenvs/kd/src/chalk/chalk/migrations/0002_add_field_article_meta_description.py
# Compiled at: 2013-08-27 18:51:01
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models
try:
    from django.contrib.auth import get_user_model
except ImportError:
    from django.contrib.auth.models import User
else:
    User = get_user_model()

user_orm_label = '%s.%s' % (User._meta.app_label, User._meta.object_name)
user_model_label = '%s.%s' % (User._meta.app_label, User._meta.module_name)

class Migration(SchemaMigration):

    def forwards(self, orm):
        db.add_column('chalk_article', 'meta_description', self.gf('django.db.models.fields.TextField')(default='', blank=True), keep_default=False)

    def backwards(self, orm):
        db.delete_column('chalk_article', 'meta_description')

    models = {user_model_label: {'Meta': {'object_name': User.__name__, 'db_table': "'%s'" % User._meta.db_table}, User._meta.pk.attname: (
                                                'django.db.models.fields.AutoField', [], {'primary_key': 'True', 'db_column': "'%s'" % User._meta.pk.column})}, 
       'chalk.article': {'Meta': {'ordering': "['-publication_date']", 'object_name': 'Article'}, 'author': (
                                  'django.db.models.fields.related.ForeignKey', [], {'to': "orm['%s']" % user_orm_label}), 
                         'content': (
                                   'django.db.models.fields.TextField', [], {}), 
                         'content_html': (
                                        'django.db.models.fields.TextField', [], {'blank': 'True'}), 
                         'created': (
                                   'django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}), 
                         'excerpt': (
                                   'django.db.models.fields.TextField', [], {'blank': 'True'}), 
                         'excerpt_html': (
                                        'django.db.models.fields.TextField', [], {'blank': 'True'}), 
                         'id': (
                              'django.db.models.fields.AutoField', [], {'primary_key': 'True'}), 
                         'meta_description': (
                                            'django.db.models.fields.TextField', [], {'blank': 'True'}), 
                         'modified': (
                                    'django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}), 
                         'protect_html': (
                                        'django.db.models.fields.BooleanField', [], {'default': 'False'}), 
                         'publication_date': (
                                            'django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2013, 8, 25, 0, 0)'}), 
                         'published': (
                                     'django.db.models.fields.BooleanField', [], {'default': 'False'}), 
                         'slug': (
                                'django.db.models.fields.SlugField', [], {'max_length': '250'}), 
                         'title': (
                                 'django.db.models.fields.CharField', [], {'max_length': '250'})}}
    complete_apps = [
     'chalk']