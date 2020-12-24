# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/f1nal/Dropbox/python/jet-bridge/src/packages/jet_bridge_base/jet_bridge_base/configuration.py
# Compiled at: 2019-10-30 05:24:12
# Size of source mod 2**32: 1337 bytes
from jet_bridge_base.settings import set_settings

class Configuration(object):

    def get_type(self):
        pass

    def get_version(self):
        pass

    def get_model_description(self, db_table):
        pass

    def get_hidden_model_description(self):
        return []

    def get_settings(self):
        pass

    def on_model_pre_create(self, model, pk):
        pass

    def on_model_post_create(self, model, instance):
        pass

    def on_model_pre_update(self, model, instance):
        pass

    def on_model_post_update(self, model, instance):
        pass

    def on_model_pre_delete(self, model, instance):
        pass

    def on_model_post_delete(self, model, instance):
        pass

    def media_get_available_name(self, path):
        pass

    def media_exists(self, path):
        pass

    def media_listdir(self, path):
        pass

    def media_get_modified_time(self, path):
        pass

    def media_open(self, path, mode='rb'):
        pass

    def media_save(self, path, content):
        pass

    def media_delete(self, path):
        pass

    def media_url(self, path, request):
        pass


configuration = Configuration()

def set_configuration(new_configuration):
    global configuration
    configuration = new_configuration
    set_settings(configuration.get_settings())