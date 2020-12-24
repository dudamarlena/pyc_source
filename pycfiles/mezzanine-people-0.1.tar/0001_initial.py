# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dougevenhouse/Virtualenvs/eci_website/eci_website/mezzanine_people/migrations/0001_initial.py
# Compiled at: 2014-05-09 15:15:42
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        db.create_table('mezzanine_people_person', (
         (
          'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
         (
          'keywords_string', self.gf('django.db.models.fields.CharField')(max_length=500, blank=True)),
         (
          'site', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sites.Site'])),
         (
          'title', self.gf('django.db.models.fields.CharField')(max_length=500)),
         (
          'slug', self.gf('django.db.models.fields.CharField')(max_length=2000, null=True, blank=True)),
         (
          '_meta_title', self.gf('django.db.models.fields.CharField')(max_length=500, null=True, blank=True)),
         (
          'description', self.gf('django.db.models.fields.TextField')(blank=True)),
         (
          'gen_description', self.gf('django.db.models.fields.BooleanField')(default=True)),
         (
          'created', self.gf('django.db.models.fields.DateTimeField')(null=True)),
         (
          'updated', self.gf('django.db.models.fields.DateTimeField')(null=True)),
         (
          'status', self.gf('django.db.models.fields.IntegerField')(default=2)),
         (
          'publish_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
         (
          'expiry_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
         (
          'short_url', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
         (
          'in_sitemap', self.gf('django.db.models.fields.BooleanField')(default=True)),
         (
          'content', self.gf('mezzanine.core.fields.RichTextField')()),
         (
          'first_name', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
         (
          'last_name', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
         (
          'mugshot', self.gf('mezzanine.core.fields.FileField')(max_length=255, null=True, blank=True)),
         (
          'mugshot_credit', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
         (
          'email', self.gf('django.db.models.fields.EmailField')(max_length=75, blank=True)),
         (
          'bio', self.gf('mezzanine.core.fields.RichTextField')(default='', blank=True)),
         (
          'job_title', self.gf('django.db.models.fields.CharField')(max_length=60, blank=True)),
         (
          'order', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0))))
        db.send_create_signal('mezzanine_people', ['Person'])
        m2m_table_name = db.shorten_name('mezzanine_people_person_categories')
        db.create_table(m2m_table_name, (
         (
          'id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
         (
          'person', models.ForeignKey(orm['mezzanine_people.person'], null=False)),
         (
          'personcategory', models.ForeignKey(orm['mezzanine_people.personcategory'], null=False))))
        db.create_unique(m2m_table_name, ['person_id', 'personcategory_id'])
        db.create_table('mezzanine_people_personlink', (
         (
          'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
         (
          'name', self.gf('django.db.models.fields.CharField')(max_length=50)),
         (
          'url', self.gf('django.db.models.fields.URLField')(max_length=200)),
         (
          'person', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mezzanine_people.Person']))))
        db.send_create_signal('mezzanine_people', ['PersonLink'])
        db.create_table('mezzanine_people_personcategory', (
         (
          'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
         (
          'site', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sites.Site'])),
         (
          'title', self.gf('django.db.models.fields.CharField')(max_length=500)),
         (
          'slug', self.gf('django.db.models.fields.CharField')(max_length=2000, null=True, blank=True))))
        db.send_create_signal('mezzanine_people', ['PersonCategory'])

    def backwards(self, orm):
        db.delete_table('mezzanine_people_person')
        db.delete_table(db.shorten_name('mezzanine_people_person_categories'))
        db.delete_table('mezzanine_people_personlink')
        db.delete_table('mezzanine_people_personcategory')

    models = {'mezzanine_people.person': {'Meta': {'ordering': "('order', 'last_name', 'first_name')", 'object_name': 'Person'}, '_meta_title': (
                                                 'django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}), 
                                   'bio': (
                                         'mezzanine.core.fields.RichTextField', [], {'default': "''", 'blank': 'True'}), 
                                   'categories': (
                                                'django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'people'", 'blank': 'True', 'to': "orm['mezzanine_people.PersonCategory']"}), 
                                   'content': (
                                             'mezzanine.core.fields.RichTextField', [], {}), 
                                   'created': (
                                             'django.db.models.fields.DateTimeField', [], {'null': 'True'}), 
                                   'description': (
                                                 'django.db.models.fields.TextField', [], {'blank': 'True'}), 
                                   'email': (
                                           'django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}), 
                                   'expiry_date': (
                                                 'django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}), 
                                   'first_name': (
                                                'django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}), 
                                   'gen_description': (
                                                     'django.db.models.fields.BooleanField', [], {'default': 'True'}), 
                                   'id': (
                                        'django.db.models.fields.AutoField', [], {'primary_key': 'True'}), 
                                   'in_sitemap': (
                                                'django.db.models.fields.BooleanField', [], {'default': 'True'}), 
                                   'job_title': (
                                               'django.db.models.fields.CharField', [], {'max_length': '60', 'blank': 'True'}), 
                                   'keywords_string': (
                                                     'django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}), 
                                   'last_name': (
                                               'django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}), 
                                   'mugshot': (
                                             'mezzanine.core.fields.FileField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}), 
                                   'mugshot_credit': (
                                                    'django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}), 
                                   'order': (
                                           'django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}), 
                                   'publish_date': (
                                                  'django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}), 
                                   'short_url': (
                                               'django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}), 
                                   'site': (
                                          'django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']"}), 
                                   'slug': (
                                          'django.db.models.fields.CharField', [], {'max_length': '2000', 'null': 'True', 'blank': 'True'}), 
                                   'status': (
                                            'django.db.models.fields.IntegerField', [], {'default': '2'}), 
                                   'title': (
                                           'django.db.models.fields.CharField', [], {'max_length': '500'}), 
                                   'updated': (
                                             'django.db.models.fields.DateTimeField', [], {'null': 'True'})}, 
       'mezzanine_people.personcategory': {'Meta': {'object_name': 'PersonCategory'}, 'id': (
                                                'django.db.models.fields.AutoField', [], {'primary_key': 'True'}), 
                                           'site': (
                                                  'django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']"}), 
                                           'slug': (
                                                  'django.db.models.fields.CharField', [], {'max_length': '2000', 'null': 'True', 'blank': 'True'}), 
                                           'title': (
                                                   'django.db.models.fields.CharField', [], {'max_length': '500'})}, 
       'mezzanine_people.personlink': {'Meta': {'ordering': "('name',)", 'object_name': 'PersonLink'}, 'id': (
                                            'django.db.models.fields.AutoField', [], {'primary_key': 'True'}), 
                                       'name': (
                                              'django.db.models.fields.CharField', [], {'max_length': '50'}), 
                                       'person': (
                                                'django.db.models.fields.related.ForeignKey', [], {'to': "orm['mezzanine_people.Person']"}), 
                                       'url': (
                                             'django.db.models.fields.URLField', [], {'max_length': '200'})}, 
       'sites.site': {'Meta': {'ordering': "(u'domain',)", 'object_name': 'Site', 'db_table': "u'django_site'"}, 'domain': (
                               'django.db.models.fields.CharField', [], {'max_length': '100'}), 
                      'id': (
                           'django.db.models.fields.AutoField', [], {'primary_key': 'True'}), 
                      'name': (
                             'django.db.models.fields.CharField', [], {'max_length': '50'})}}
    complete_apps = [
     'mezzanine_people']