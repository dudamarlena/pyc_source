# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ana/dev/dexy-clean/dexy/filters/api.py
# Compiled at: 2020-03-18 15:12:33
# Size of source mod 2**32: 5578 bytes
from dexy.utils import file_exists
import dexy.filter, json, os

class ApiFilter(dexy.filter.DexyFilter):
    __doc__ = '\n    Base class for filters which post content to a remote API.\n    \n    This class provides standard formats and locations for storing\n    configuration and authentication information.\n\n    Need to read config for the API in general, such as the base URL and an API\n    key for authentication.\n\n    Also need to read config for the particular task/document being uploaded.\n    This could be stored in the .dexy config entry, but this has two drawbacks.\n    First, it makes it difficult to bulk define documents according to a\n    pattern. Secondly, it makes it very difficult for dexy to modify this\n    configuration to add additional information, such as the returned id for a\n    newly created document.\n\n    So, it is preferable to define a local file (defined by a relative path to\n    the document in question) which can be overridden per-document in which we\n    just store the API-related config and which can be modified by dexy without\n    concern about identifying the entry in a .dexy file or accidentally\n    overwriting some unrelated information.\n    '
    aliases = ['apis']
    _settings = {'master-api-key-file':('Master API key file for user.', '~/.dexyapis'), 
     'project-api-key-file':('API key file for project.', '.dexyapis'), 
     'api-username':('The username to sign into the API with.', None), 
     'api-password':('The password to sign into the API with.', None), 
     'api-url':('The url of the API endpoint.', None), 
     'document-api-config-file':('Filename to store config for a file (can only have 1 per directory, dexy looks for suffix format first.',
 None), 
     'document-api-config-postfix':('Suffix to attach to content filename to indicate this is the config for that file.',
 '-config.json'), 
     'api-key-name':('The name of this API', None)}

    def api_key_locations(self):
        return [
         self.setting('project-api-key-file'), self.setting('master-api-key-file')]

    def docmd_create_keyfile(self):
        return self.create_keyfile('master-api-key-file')

    def create_keyfile(self, keyfilekey):
        """
        Creates a key file.
        """
        key_filename = os.path.expanduser(self.setting(keyfilekey))
        if file_exists(key_filename):
            raise dexy.exceptions.UserFeedback('File %s already exists!' % key_filename)
        keyfile_content = {}
        for filter_instance in dexy.filter.Filter:
            if isinstance(filter_instance, ApiFilter):
                api_key_name = filter_instance.__class__ == ApiFilter or filter_instance.setting('api-key-name')
                keyfile_content[api_key_name] = {}
                for k, v in filter_instance.setting_values().items():
                    if k.startswith('api_'):
                        keyfile_content[api_key_name][k.replace('api_', '')] = 'TODO'

        with open(key_filename, 'w') as (f):
            json.dump(keyfile_content, f, sort_keys=True, indent=4)

    def document_config_file(self):
        postfix_config_filename = '%s%s' % (os.path.splitext(self.output_data.name)[0], self.setting('document-api-config-postfix'))
        if file_exists(postfix_config_filename):
            return postfix_config_filename
        return os.path.join(self.output_data.parent_dir(), self.setting('document-api-config-file'))

    def read_document_config(self):
        document_config = self.document_config_file()
        if file_exists(document_config):
            with open(document_config, 'r') as (f):
                return json.load(f)
        else:
            msg = "Filter %s needs a file %s, couldn't find it."
            raise dexy.exceptions.UserFeedback(msg % (self.alias, document_config))

    def save_document_config(self, config):
        document_config = self.document_config_file()
        with open(document_config, 'w') as (f):
            json.dump(config, f, sort_keys=True, indent=4)

    def read_param(self, param_name):
        param_value = None
        for filename in self.api_key_locations():
            if '~' in filename:
                filename = os.path.expanduser(filename)
            if file_exists(filename):
                with open(filename, 'r') as (f):
                    params = json.load(f)
                    if self.setting('api-key-name') in params:
                        param_value = params[self.setting('api-key-name')].get(param_name)
            if param_value:
                break

        if param_value:
            if isinstance(param_value, str):
                if param_value.startswith('$'):
                    param_value_from_env = os.getenv(param_value.lstrip('$'))
                    if not param_value_from_env:
                        raise KeyError('Bash variable %s not defined in this environment!' % param_value)
                    param_value = param_value_from_env
        if param_value:
            return param_value
        msg = 'Could not find %s for %s in: %s' % (param_name, self.setting('api-key-name'), ', '.join(self.api_key_locations()))
        raise KeyError(msg)