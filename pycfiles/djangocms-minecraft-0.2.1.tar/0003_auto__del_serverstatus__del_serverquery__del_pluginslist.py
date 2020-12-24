# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/growlf/django/apps/djangocms-minecraft/djangocms_minecraft/migrations/0003_auto__del_serverstatus__del_serverquery__del_pluginslist.py
# Compiled at: 2014-08-28 10:58:55
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        db.delete_table('djangocms_minecraft_serverstatus')
        db.delete_table('djangocms_minecraft_serverquery')
        db.delete_table('djangocms_minecraft_pluginslist')

    def backwards(self, orm):
        db.create_table('djangocms_minecraft_serverstatus', (
         (
          'mchost', self.gf('django.db.models.fields.IPAddressField')(default='127.0.0.1', max_length=15)),
         (
          'cmsplugin_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['cms.CMSPlugin'], unique=True, primary_key=True)),
         (
          'mcport', self.gf('django.db.models.fields.PositiveIntegerField')(default=25565))))
        db.send_create_signal('djangocms_minecraft', ['ServerStatus'])
        db.create_table('djangocms_minecraft_serverquery', (
         (
          'mcport', self.gf('django.db.models.fields.PositiveIntegerField')(default=25565)),
         (
          'mchost', self.gf('django.db.models.fields.IPAddressField')(default='127.0.0.1', max_length=15)),
         (
          'cmsplugin_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['cms.CMSPlugin'], unique=True, primary_key=True)),
         (
          'map_url', self.gf('django.db.models.fields.CharField')(default='http://www.thenetyeti.com:8123/?mapname=surface&zoom=8', max_length=80))))
        db.send_create_signal('djangocms_minecraft', ['ServerQuery'])
        db.create_table('djangocms_minecraft_pluginslist', (
         (
          'mchost', self.gf('django.db.models.fields.IPAddressField')(default='127.0.0.1', max_length=15)),
         (
          'cmsplugin_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['cms.CMSPlugin'], unique=True, primary_key=True)),
         (
          'mcport', self.gf('django.db.models.fields.PositiveIntegerField')(default=25565))))
        db.send_create_signal('djangocms_minecraft', ['PluginsList'])

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
       'djangocms_minecraft.minecraftserver': {'Meta': {'object_name': 'MinecraftServer', '_ormbases': ['cms.CMSPlugin']}, 'cmsplugin_ptr': (
                                                               'django.db.models.fields.related.OneToOneField', [], {'to': "orm['cms.CMSPlugin']", 'unique': 'True', 'primary_key': 'True'}), 
                                               'map_url': (
                                                         'django.db.models.fields.CharField', [], {'default': "'http://www.thenetyeti.com:8123/?mapname=surface&zoom=8'", 'max_length': '80'}), 
                                               'mchost': (
                                                        'django.db.models.fields.GenericIPAddressField', [], {'default': "'127.0.0.1'", 'max_length': '39'}), 
                                               'mcport': (
                                                        'django.db.models.fields.PositiveIntegerField', [], {'default': '25565'}), 
                                               'name': (
                                                      'django.db.models.fields.CharField', [], {'max_length': '50'}), 
                                               'rconport': (
                                                          'django.db.models.fields.PositiveIntegerField', [], {'default': '25565'})}}
    complete_apps = [
     'djangocms_minecraft']