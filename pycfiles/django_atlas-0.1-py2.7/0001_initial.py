# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/atlas/migrations/0001_initial.py
# Compiled at: 2015-04-21 15:30:03
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models
from django.conf import settings

class Migration(SchemaMigration):

    def forwards(self, orm):
        db_engine = settings.DATABASES['default']['ENGINE']
        if db_engine.rfind('mysql') == -1:
            db.create_table('atlas_country', (
             (
              'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
             (
              'name', self.gf('django.db.models.fields.CharField')(max_length=50)),
             (
              'country_code', self.gf('django.db.models.fields.CharField')(unique=True, max_length=2, db_index=True)),
             (
              'border', self.gf('django.contrib.gis.db.models.fields.MultiPolygonField')(blank=True, null=True, geography=True))))
            db.send_create_signal('atlas', ['Country'])
            db.create_table('atlas_region', (
             (
              'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
             (
              'name', self.gf('django.db.models.fields.CharField')(max_length=128)),
             (
              'code', self.gf('django.db.models.fields.CharField')(max_length=2, db_index=True)),
             (
              'border', self.gf('django.contrib.gis.db.models.fields.MultiPolygonField')(blank=True, null=True, geography=True)),
             (
              'country', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['atlas.Country']))))
            db.send_create_signal('atlas', ['Region'])
            db.create_unique('atlas_region', ['country_id', 'code'])
            db.create_table('atlas_city', (
             (
              'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
             (
              'name', self.gf('django.db.models.fields.CharField')(max_length=128, db_index=True)),
             (
              'coordinates', self.gf('atlas.fields.CoordinateField')(blank=True, null=True, geography=True)),
             (
              'region', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['atlas.Region'], null=True, blank=True)),
             (
              'country', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['atlas.Country']))))
            db.send_create_signal('atlas', ['City'])
            db.create_table('atlas_location', (
             (
              'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
             (
              'name', self.gf('django.db.models.fields.CharField')(max_length=128, db_index=True)),
             (
              'coordinates', self.gf('atlas.fields.CoordinateField')(blank=True, null=True, geography=True)),
             (
              'country', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['atlas.Country'])),
             (
              'city', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['atlas.City'], null=True, blank=True)),
             (
              'description', self.gf('django.db.models.fields.TextField')(max_length=1024, null=True, blank=True)),
             (
              'photo', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['photologue.Photo'], null=True, blank=True)),
             (
              'category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['category.Category'], null=True, blank=True))))
            db.send_create_signal('atlas', ['Location'])
        else:
            if not db.dry_run:
                sql = '\n                    SET FOREIGN_KEY_CHECKS=0;\n                    CREATE TABLE `atlas_country` (`id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `name` varchar(50) NOT NULL, `country_code` varchar(2) NOT NULL UNIQUE, `border` MULTIPOLYGON NULL);\n                    CREATE TABLE `atlas_region` (`id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `name` varchar(128) NOT NULL, `code` varchar(2) NOT NULL, `border` MULTIPOLYGON NULL, `country_id` integer NOT NULL);\n                    ALTER TABLE `atlas_region` ADD CONSTRAINT `atlas_region_country_id_545200d9bb67aa36_uniq` UNIQUE (`country_id`, `code`);\n                    CREATE TABLE `atlas_city` (`id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `name` varchar(128) NOT NULL, `coordinates` POINT NULL, `region_id` integer NULL, `country_id` integer NOT NULL);\n                    CREATE TABLE `atlas_location` (`id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `name` varchar(128) NOT NULL, `coordinates` POINT NULL, `country_id` integer NOT NULL, `city_id` integer NULL, `description` longtext NULL, `photo_id` integer NULL, `category_id` integer NULL);\n                    CREATE INDEX `atlas_region_65da3d2c` ON `atlas_region` (`code`);\n                    ALTER TABLE `atlas_region` ADD CONSTRAINT `country_id_refs_id_688446d03ef69106` FOREIGN KEY (`country_id`) REFERENCES `atlas_country` (`id`);\n                    CREATE INDEX `atlas_region_534dd89` ON `atlas_region` (`country_id`);\n                    CREATE INDEX `atlas_city_52094d6e` ON `atlas_city` (`name`);\n                    ALTER TABLE `atlas_city` ADD CONSTRAINT `region_id_refs_id_4877f50311a5997e` FOREIGN KEY (`region_id`) REFERENCES `atlas_region` (`id`);\n                    CREATE INDEX `atlas_city_f6a8b032` ON `atlas_city` (`region_id`);\n                    ALTER TABLE `atlas_city` ADD CONSTRAINT `country_id_refs_id_51bbc9cfa50a0b7d` FOREIGN KEY (`country_id`) REFERENCES `atlas_country` (`id`);\n                    CREATE INDEX `atlas_city_534dd89` ON `atlas_city` (`country_id`);\n                    CREATE INDEX `atlas_location_52094d6e` ON `atlas_location` (`name`);\n                    ALTER TABLE `atlas_location` ADD CONSTRAINT `country_id_refs_id_3a0bfa099c9ea063` FOREIGN KEY (`country_id`) REFERENCES `atlas_country` (`id`);\n                    CREATE INDEX `atlas_location_534dd89` ON `atlas_location` (`country_id`);\n                    ALTER TABLE `atlas_location` ADD CONSTRAINT `city_id_refs_id_136a507ad0769b15` FOREIGN KEY (`city_id`) REFERENCES `atlas_city` (`id`);\n                    CREATE INDEX `atlas_location_586a73b5` ON `atlas_location` (`city_id`);\n                    ALTER TABLE `atlas_location` ADD CONSTRAINT `photo_id_refs_id_764ca670382ba838` FOREIGN KEY (`photo_id`) REFERENCES `photologue_photo` (`id`);\n                    CREATE INDEX `atlas_location_7c6c8bb1` ON `atlas_location` (`photo_id`);\n                    ALTER TABLE `atlas_location` ADD CONSTRAINT `category_id_refs_id_71ba6eba4d7f8101` FOREIGN KEY (`category_id`) REFERENCES `category_category` (`id`);\n                    CREATE INDEX `atlas_location_42dc49bc` ON `atlas_location` (`category_id`);\n                    SET FOREIGN_KEY_CHECKS=1;'
                for s in sql.split(';'):
                    if s:
                        db.execute(s + ';')

            db.send_create_signal('atlas', ['Country'])
            db.send_create_signal('atlas', ['Region'])
            db.send_create_signal('atlas', ['City'])
            db.send_create_signal('atlas', ['Location'])

    def backwards(self, orm):
        db.delete_unique('atlas_region', ['country_id', 'code'])
        db.delete_table('atlas_country')
        db.delete_table('atlas_region')
        db.delete_table('atlas_city')
        db.delete_table('atlas_location')

    models = {'category.category': {'Meta': {'ordering': "('title',)", 'object_name': 'Category'}, 'id': (
                                  'django.db.models.fields.AutoField', [], {'primary_key': 'True'}), 
                             'parent': (
                                      'django.db.models.fields.related.ForeignKey', [], {'to': "orm['category.Category']", 'null': 'True', 'blank': 'True'}), 
                             'slug': (
                                    'django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '255'}), 
                             'title': (
                                     'django.db.models.fields.CharField', [], {'max_length': '200'})}, 
       'atlas.city': {'Meta': {'ordering': "('name',)", 'object_name': 'City'}, 'coordinates': (
                                    'atlas.fields.CoordinateField', [], {'blank': 'True', 'null': 'True', 'geography': 'True'}), 
                      'country': (
                                'django.db.models.fields.related.ForeignKey', [], {'to': "orm['atlas.Country']"}), 
                      'id': (
                           'django.db.models.fields.AutoField', [], {'primary_key': 'True'}), 
                      'name': (
                             'django.db.models.fields.CharField', [], {'max_length': '128', 'db_index': 'True'}), 
                      'region': (
                               'django.db.models.fields.related.ForeignKey', [], {'to': "orm['atlas.Region']", 'null': 'True', 'blank': 'True'})}, 
       'atlas.country': {'Meta': {'ordering': "('name',)", 'object_name': 'Country'}, 'border': (
                                  'django.contrib.gis.db.models.fields.MultiPolygonField', [], {'blank': 'True', 'null': 'True', 'geography': 'True'}), 
                         'country_code': (
                                        'django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '2', 'db_index': 'True'}), 
                         'id': (
                              'django.db.models.fields.AutoField', [], {'primary_key': 'True'}), 
                         'name': (
                                'django.db.models.fields.CharField', [], {'max_length': '50'})}, 
       'atlas.location': {'Meta': {'object_name': 'Location'}, 'category': (
                                     'django.db.models.fields.related.ForeignKey', [], {'to': "orm['category.Category']", 'null': 'True', 'blank': 'True'}), 
                          'city': (
                                 'django.db.models.fields.related.ForeignKey', [], {'to': "orm['atlas.City']", 'null': 'True', 'blank': 'True'}), 
                          'coordinates': (
                                        'atlas.fields.CoordinateField', [], {'blank': 'True', 'null': 'True', 'geography': 'True'}), 
                          'country': (
                                    'django.db.models.fields.related.ForeignKey', [], {'to': "orm['atlas.Country']"}), 
                          'description': (
                                        'django.db.models.fields.TextField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}), 
                          'id': (
                               'django.db.models.fields.AutoField', [], {'primary_key': 'True'}), 
                          'name': (
                                 'django.db.models.fields.CharField', [], {'max_length': '128', 'db_index': 'True'}), 
                          'photo': (
                                  'django.db.models.fields.related.ForeignKey', [], {'to': "orm['photologue.Photo']", 'null': 'True', 'blank': 'True'})}, 
       'atlas.region': {'Meta': {'ordering': "('name',)", 'unique_together': "(('country', 'code'),)", 'object_name': 'Region'}, 'border': (
                                 'django.contrib.gis.db.models.fields.MultiPolygonField', [], {'blank': 'True', 'null': 'True', 'geography': 'True'}), 
                        'code': (
                               'django.db.models.fields.CharField', [], {'max_length': '2', 'db_index': 'True'}), 
                        'country': (
                                  'django.db.models.fields.related.ForeignKey', [], {'to': "orm['atlas.Country']"}), 
                        'id': (
                             'django.db.models.fields.AutoField', [], {'primary_key': 'True'}), 
                        'name': (
                               'django.db.models.fields.CharField', [], {'max_length': '128'})}, 
       'photologue.photo': {'Meta': {'ordering': "['-date_added']", 'object_name': 'Photo'}, 'caption': (
                                      'django.db.models.fields.TextField', [], {'blank': 'True'}), 
                            'crop_from': (
                                        'django.db.models.fields.CharField', [], {'default': "'center'", 'max_length': '10', 'blank': 'True'}), 
                            'date_added': (
                                         'django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}), 
                            'date_taken': (
                                         'django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}), 
                            'effect': (
                                     'django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'photo_related'", 'null': 'True', 'to': "orm['photologue.PhotoEffect']"}), 
                            'id': (
                                 'django.db.models.fields.AutoField', [], {'primary_key': 'True'}), 
                            'image': (
                                    'django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}), 
                            'is_public': (
                                        'django.db.models.fields.BooleanField', [], {'default': 'True'}), 
                            'tags': (
                                   'photologue.models.TagField', [], {'max_length': '255', 'blank': 'True'}), 
                            'title': (
                                    'django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}), 
                            'title_slug': (
                                         'django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'}), 
                            'view_count': (
                                         'django.db.models.fields.PositiveIntegerField', [], {'default': '0'})}, 
       'photologue.photoeffect': {'Meta': {'object_name': 'PhotoEffect'}, 'background_color': (
                                                     'django.db.models.fields.CharField', [], {'default': "'#FFFFFF'", 'max_length': '7'}), 
                                  'brightness': (
                                               'django.db.models.fields.FloatField', [], {'default': '1.0'}), 
                                  'color': (
                                          'django.db.models.fields.FloatField', [], {'default': '1.0'}), 
                                  'contrast': (
                                             'django.db.models.fields.FloatField', [], {'default': '1.0'}), 
                                  'description': (
                                                'django.db.models.fields.TextField', [], {'blank': 'True'}), 
                                  'filters': (
                                            'django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}), 
                                  'id': (
                                       'django.db.models.fields.AutoField', [], {'primary_key': 'True'}), 
                                  'name': (
                                         'django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'}), 
                                  'reflection_size': (
                                                    'django.db.models.fields.FloatField', [], {'default': '0'}), 
                                  'reflection_strength': (
                                                        'django.db.models.fields.FloatField', [], {'default': '0.6'}), 
                                  'sharpness': (
                                              'django.db.models.fields.FloatField', [], {'default': '1.0'}), 
                                  'transpose_method': (
                                                     'django.db.models.fields.CharField', [], {'max_length': '15', 'blank': 'True'})}}
    complete_apps = [
     'atlas']