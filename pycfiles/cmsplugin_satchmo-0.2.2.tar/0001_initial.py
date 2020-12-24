# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/tomas/prace/vyvoj/cmsplugin_satchmo/cmsplugin_satchmo/migrations/0001_initial.py
# Compiled at: 2014-05-29 15:42:49
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        db.create_table('cmsplugin_satchmoproductplugin', (
         (
          'cmsplugin_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['cms.CMSPlugin'], unique=True, primary_key=True)),
         (
          'style', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
         (
          'product_url_path', self.gf('django.db.models.fields.CharField')(default='/produkty/', max_length=200, blank=True)),
         (
          'product', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['product.Product'])),
         (
          'title', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True))))
        db.send_create_signal('cmsplugin_satchmo', ['SatchmoProductPlugin'])
        db.create_table('cmsplugin_satchmoproductslistplugin', (
         (
          'cmsplugin_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['cms.CMSPlugin'], unique=True, primary_key=True)),
         (
          'style', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
         (
          'product_url_path', self.gf('django.db.models.fields.CharField')(default='/produkty/', max_length=200, blank=True)),
         (
          'list_type', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
         (
          'number', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=5)),
         (
          'site', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sites.Site']))))
        db.send_create_signal('cmsplugin_satchmo', ['SatchmoProductsListPlugin'])
        db.create_table('cmsplugin_satchmocategoryplugin', (
         (
          'cmsplugin_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['cms.CMSPlugin'], unique=True, primary_key=True)),
         (
          'style', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
         (
          'category_url_path', self.gf('django.db.models.fields.CharField')(default='/kategorie/', max_length=200, blank=True)),
         (
          'category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['product.Category'])),
         (
          'title', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True))))
        db.send_create_signal('cmsplugin_satchmo', ['SatchmoCategoryPlugin'])
        db.create_table('cmsplugin_satchmocategorieslistplugin', (
         (
          'cmsplugin_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['cms.CMSPlugin'], unique=True, primary_key=True)),
         (
          'style', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
         (
          'category_url_path', self.gf('django.db.models.fields.CharField')(default='/kategorie/', max_length=200, blank=True)),
         (
          'main_category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['product.Category'], null=True, blank=True)),
         (
          'site', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sites.Site']))))
        db.send_create_signal('cmsplugin_satchmo', ['SatchmoCategoriesListPlugin'])

    def backwards(self, orm):
        db.delete_table('cmsplugin_satchmoproductplugin')
        db.delete_table('cmsplugin_satchmoproductslistplugin')
        db.delete_table('cmsplugin_satchmocategoryplugin')
        db.delete_table('cmsplugin_satchmocategorieslistplugin')

    models = {'cms.cmsplugin': {'Meta': {'object_name': 'CMSPlugin'}, 'changed_date': (
                                        'django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}), 
                         'creation_date': (
                                         'django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}), 
                         'id': (
                              'django.db.models.fields.AutoField', [], {'primary_key': 'True'}), 
                         'language': (
                                    'django.db.models.fields.CharField', [], {'max_length': '15', 'db_index': 'True'}), 
                         'level': (
                                 'django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}), 
                         'lft': (
                               'django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}), 
                         'parent': (
                                  'django.db.models.fields.related.ForeignKey', [], {'to': "orm['cms.CMSPlugin']", 'null': 'True', 'blank': 'True'}), 
                         'placeholder': (
                                       'django.db.models.fields.related.ForeignKey', [], {'to': "orm['cms.Placeholder']", 'null': 'True'}), 
                         'plugin_type': (
                                       'django.db.models.fields.CharField', [], {'max_length': '50', 'db_index': 'True'}), 
                         'position': (
                                    'django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}), 
                         'rght': (
                                'django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}), 
                         'tree_id': (
                                   'django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})}, 
       'cms.placeholder': {'Meta': {'object_name': 'Placeholder'}, 'default_width': (
                                           'django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True'}), 
                           'id': (
                                'django.db.models.fields.AutoField', [], {'primary_key': 'True'}), 
                           'slot': (
                                  'django.db.models.fields.CharField', [], {'max_length': '50', 'db_index': 'True'})}, 
       'cmsplugin_satchmo.satchmocategorieslistplugin': {'Meta': {'object_name': 'SatchmoCategoriesListPlugin', 'db_table': "u'cmsplugin_satchmocategorieslistplugin'"}, 'category_url_path': (
                                                                             'django.db.models.fields.CharField', [], {'default': "'/kategorie/'", 'max_length': '200', 'blank': 'True'}), 
                                                         'cmsplugin_ptr': (
                                                                         'django.db.models.fields.related.OneToOneField', [], {'to': "orm['cms.CMSPlugin']", 'unique': 'True', 'primary_key': 'True'}), 
                                                         'main_category': (
                                                                         'django.db.models.fields.related.ForeignKey', [], {'to': "orm['product.Category']", 'null': 'True', 'blank': 'True'}), 
                                                         'site': (
                                                                'django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']"}), 
                                                         'style': (
                                                                 'django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'})}, 
       'cmsplugin_satchmo.satchmocategoryplugin': {'Meta': {'object_name': 'SatchmoCategoryPlugin', 'db_table': "u'cmsplugin_satchmocategoryplugin'"}, 'category': (
                                                              'django.db.models.fields.related.ForeignKey', [], {'to': "orm['product.Category']"}), 
                                                   'category_url_path': (
                                                                       'django.db.models.fields.CharField', [], {'default': "'/kategorie/'", 'max_length': '200', 'blank': 'True'}), 
                                                   'cmsplugin_ptr': (
                                                                   'django.db.models.fields.related.OneToOneField', [], {'to': "orm['cms.CMSPlugin']", 'unique': 'True', 'primary_key': 'True'}), 
                                                   'style': (
                                                           'django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}), 
                                                   'title': (
                                                           'django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'})}, 
       'cmsplugin_satchmo.satchmoproductplugin': {'Meta': {'object_name': 'SatchmoProductPlugin', 'db_table': "u'cmsplugin_satchmoproductplugin'"}, 'cmsplugin_ptr': (
                                                                  'django.db.models.fields.related.OneToOneField', [], {'to': "orm['cms.CMSPlugin']", 'unique': 'True', 'primary_key': 'True'}), 
                                                  'product': (
                                                            'django.db.models.fields.related.ForeignKey', [], {'to': "orm['product.Product']"}), 
                                                  'product_url_path': (
                                                                     'django.db.models.fields.CharField', [], {'default': "'/produkty/'", 'max_length': '200', 'blank': 'True'}), 
                                                  'style': (
                                                          'django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}), 
                                                  'title': (
                                                          'django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'})}, 
       'cmsplugin_satchmo.satchmoproductslistplugin': {'Meta': {'object_name': 'SatchmoProductsListPlugin', 'db_table': "u'cmsplugin_satchmoproductslistplugin'"}, 'cmsplugin_ptr': (
                                                                       'django.db.models.fields.related.OneToOneField', [], {'to': "orm['cms.CMSPlugin']", 'unique': 'True', 'primary_key': 'True'}), 
                                                       'list_type': (
                                                                   'django.db.models.fields.PositiveSmallIntegerField', [], {}), 
                                                       'number': (
                                                                'django.db.models.fields.PositiveSmallIntegerField', [], {'default': '5'}), 
                                                       'product_url_path': (
                                                                          'django.db.models.fields.CharField', [], {'default': "'/produkty/'", 'max_length': '200', 'blank': 'True'}), 
                                                       'site': (
                                                              'django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']"}), 
                                                       'style': (
                                                               'django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'})}, 
       'product.category': {'Meta': {'ordering': "['site', 'parent__ordering', 'parent__name', 'ordering', 'name']", 'unique_together': "(('site', 'slug'),)", 'object_name': 'Category'}, 'description': (
                                          'django.db.models.fields.TextField', [], {'blank': 'True'}), 
                            'id': (
                                 'django.db.models.fields.AutoField', [], {'primary_key': 'True'}), 
                            'is_active': (
                                        'django.db.models.fields.BooleanField', [], {'default': 'True'}), 
                            'meta': (
                                   'django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}), 
                            'name': (
                                   'django.db.models.fields.CharField', [], {'max_length': '200'}), 
                            'ordering': (
                                       'django.db.models.fields.IntegerField', [], {'default': '0'}), 
                            'parent': (
                                     'django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'child'", 'null': 'True', 'to': "orm['product.Category']"}), 
                            'related_categories': (
                                                 'django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'related_categories_rel_+'", 'null': 'True', 'to': "orm['product.Category']"}), 
                            'site': (
                                   'django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']"}), 
                            'slug': (
                                   'django.db.models.fields.SlugField', [], {'max_length': '50', 'blank': 'True'})}, 
       'product.product': {'Meta': {'ordering': "('site', 'ordering', 'name')", 'unique_together': "(('site', 'sku'), ('site', 'slug'))", 'object_name': 'Product'}, 'active': (
                                    'django.db.models.fields.BooleanField', [], {'default': 'True'}), 
                           'also_purchased': (
                                            'django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'also_purchased_rel_+'", 'null': 'True', 'to': "orm['product.Product']"}), 
                           'category': (
                                      'django.db.models.fields.related.ManyToManyField', [], {'to': "orm['product.Category']", 'symmetrical': 'False', 'blank': 'True'}), 
                           'date_added': (
                                        'django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}), 
                           'description': (
                                         'django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}), 
                           'featured': (
                                      'django.db.models.fields.BooleanField', [], {'default': 'False'}), 
                           'height': (
                                    'django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '6', 'decimal_places': '2', 'blank': 'True'}), 
                           'height_units': (
                                          'django.db.models.fields.CharField', [], {'max_length': '3', 'null': 'True', 'blank': 'True'}), 
                           'id': (
                                'django.db.models.fields.AutoField', [], {'primary_key': 'True'}), 
                           'items_in_stock': (
                                            'django.db.models.fields.DecimalField', [], {'default': "'0'", 'max_digits': '18', 'decimal_places': '6'}), 
                           'length': (
                                    'django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '6', 'decimal_places': '2', 'blank': 'True'}), 
                           'length_units': (
                                          'django.db.models.fields.CharField', [], {'max_length': '3', 'null': 'True', 'blank': 'True'}), 
                           'meta': (
                                  'django.db.models.fields.TextField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}), 
                           'name': (
                                  'django.db.models.fields.CharField', [], {'max_length': '255'}), 
                           'ordering': (
                                      'django.db.models.fields.IntegerField', [], {'default': '0'}), 
                           'related_items': (
                                           'django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'related_items_rel_+'", 'null': 'True', 'to': "orm['product.Product']"}), 
                           'shipclass': (
                                       'django.db.models.fields.CharField', [], {'default': "'DEFAULT'", 'max_length': '10'}), 
                           'short_description': (
                                               'django.db.models.fields.TextField', [], {'default': "''", 'max_length': '200', 'blank': 'True'}), 
                           'site': (
                                  'django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']"}), 
                           'sku': (
                                 'django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}), 
                           'slug': (
                                  'django.db.models.fields.SlugField', [], {'max_length': '255', 'blank': 'True'}), 
                           'taxClass': (
                                      'django.db.models.fields.related.ForeignKey', [], {'to': "orm['product.TaxClass']", 'null': 'True', 'blank': 'True'}), 
                           'taxable': (
                                     'django.db.models.fields.BooleanField', [], {'default': 'True'}), 
                           'total_sold': (
                                        'django.db.models.fields.DecimalField', [], {'default': "'0'", 'max_digits': '18', 'decimal_places': '6'}), 
                           'weight': (
                                    'django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '8', 'decimal_places': '2', 'blank': 'True'}), 
                           'weight_units': (
                                          'django.db.models.fields.CharField', [], {'max_length': '3', 'null': 'True', 'blank': 'True'}), 
                           'width': (
                                   'django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '6', 'decimal_places': '2', 'blank': 'True'}), 
                           'width_units': (
                                         'django.db.models.fields.CharField', [], {'max_length': '3', 'null': 'True', 'blank': 'True'})}, 
       'product.taxclass': {'Meta': {'object_name': 'TaxClass'}, 'description': (
                                          'django.db.models.fields.CharField', [], {'max_length': '30'}), 
                            'id': (
                                 'django.db.models.fields.AutoField', [], {'primary_key': 'True'}), 
                            'title': (
                                    'django.db.models.fields.CharField', [], {'max_length': '20'})}, 
       'sites.site': {'Meta': {'ordering': "('domain',)", 'object_name': 'Site', 'db_table': "'django_site'"}, 'domain': (
                               'django.db.models.fields.CharField', [], {'max_length': '100'}), 
                      'id': (
                           'django.db.models.fields.AutoField', [], {'primary_key': 'True'}), 
                      'name': (
                             'django.db.models.fields.CharField', [], {'max_length': '50'})}}
    complete_apps = [
     'cmsplugin_satchmo']