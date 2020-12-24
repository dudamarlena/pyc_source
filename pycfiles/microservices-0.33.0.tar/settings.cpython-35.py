# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/viator/coding/code/microservices/microservices/http/settings.py
# Compiled at: 2017-03-07 04:59:57
# Size of source mod 2**32: 1248 bytes
from flask_api import settings
from microservices.http.renderers import MicroserviceJSONRenderer, MicroserviceBrowsableAPIRenderer
from microservices.http.resources import ResourceSchema

class MicroserviceAPISettings(settings.APISettings):

    @property
    def IN_RESOURCES(self):
        default = [
         'methods',
         'url']
        return self.user_config.get('IN_RESOURCES', default)

    @property
    def DEFAULT_PARSERS(self):
        default = [
         'flask_api.parsers.JSONParser',
         'flask_api.parsers.URLEncodedParser',
         'flask_api.parsers.MultiPartParser']
        val = self.user_config.get('DEFAULT_PARSERS', default)
        return settings.perform_imports(val, 'DEFAULT_PARSERS')

    @property
    def DEFAULT_RENDERERS(self):
        default = [
         MicroserviceJSONRenderer,
         MicroserviceBrowsableAPIRenderer]
        val = self.user_config.get('DEFAULT_RENDERERS', default)
        return settings.perform_imports(val, 'DEFAULT_RENDERERS')

    @property
    def SCHEMA(self):
        default = ResourceSchema()
        user_schema = self.user_config.get('SCHEMA', default)
        default.update(user_schema)
        return default