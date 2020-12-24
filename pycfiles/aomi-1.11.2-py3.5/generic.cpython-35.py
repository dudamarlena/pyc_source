# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/aomi/model/generic.py
# Compiled at: 2017-11-17 12:53:02
# Size of source mod 2**32: 5285 bytes
"""
Generic Vault Resources
* YAML Variable Files
* Static files
* Generated/Random Secrets
"""
import os
from copy import deepcopy
from uuid import uuid4
import logging
from future.utils import iteritems
from cryptorito import portable_b64encode
import aomi.exceptions
from aomi.model.resource import Secret
from aomi.helpers import random_word, hard_path, open_maybe_binary
from aomi.template import load_vars, load_var_file
from aomi.validation import sanitize_mount, secret_file, check_obj, is_unicode_string
LOG = logging.getLogger(__name__)

class Generic(Secret):
    __doc__ = 'Generic Secrets'
    backend = 'generic'

    def __init__(self, obj, opt):
        super(Generic, self).__init__(obj, opt)
        self.mount = sanitize_mount(obj['mount'])
        self.path = '%s/%s' % (self.mount, obj['path'])


class VarFile(Generic):
    __doc__ = 'Generic VarFile'
    required_fields = ['path', 'mount', 'var_file']
    resource_key = 'var_file'

    def secrets(self):
        return [
         self.secret]

    def __init__(self, obj, opt):
        super(VarFile, self).__init__(obj, opt)
        self.secret = obj['var_file']
        self.filename = obj['var_file']

    def obj(self):
        filename = hard_path(self.filename, self.opt.secrets)
        secret_file(filename)
        template_obj = load_vars(self.opt)
        return load_var_file(filename, template_obj)


class Files(Generic):
    __doc__ = 'Generic File'
    required_fields = ['path', 'mount', 'files']
    resource_key = 'files'

    def secrets(self):
        return [v for _k, v in iteritems(self._obj)]

    def __init__(self, obj, opt):
        super(Files, self).__init__(obj, opt)
        s_obj = {}
        for sfile in obj['files']:
            s_obj[sfile['name']] = sfile['source']

        self._obj = s_obj

    def export(self, directory):
        for name, filename in iteritems(self._obj):
            dest_file = '%s/%s' % (directory, filename)
            dest_dir = os.path.dirname(dest_file)
            if not os.path.isdir(dest_dir):
                os.mkdir(dest_dir, 448)
            secret_h = open(dest_file, 'w')
            secret_h.write(self.existing[name])
            secret_h.close()

    def obj(self):
        s_obj = {}
        for name, filename in iteritems(self._obj):
            actual_file = hard_path(filename, self.opt.secrets)
            secret_file(actual_file)
            data = open_maybe_binary(actual_file)
            try:
                is_unicode_string(data)
                s_obj[name] = data
            except aomi.exceptions.Validation:
                s_obj[name] = portable_b64encode(data)
                self.secret_format = 'binary'

        return s_obj

    def validate(self, obj):
        super(Files, self).validate(obj)
        for fileobj in obj['files']:
            check_obj(['source', 'name'], self.name(), fileobj)


def generated_key(key):
    """Create the proper generated key value"""
    key_name = key['name']
    if key['method'] == 'uuid':
        LOG.debug('Setting %s to a uuid', key_name)
        return str(uuid4())
    if key['method'] == 'words':
        LOG.debug('Setting %s to random words', key_name)
        return random_word()
    if key['method'] == 'static':
        if 'value' not in key.keys():
            raise aomi.exceptions.AomiData('Missing static value')
        LOG.debug('Setting %s to a static value', key_name)
        return key['value']
    raise aomi.exceptions.AomiData('Unexpected generated secret method %s' % key['method'])


class Generated(Generic):
    __doc__ = 'Generic Generated'
    required_fields = ['mount', 'path', 'keys']
    resource_key = 'generated'

    def __init__(self, obj, opt):
        super(Generated, self).__init__(obj['generated'], opt)
        for key in obj['generated']['keys']:
            check_obj(['name', 'method'], 'generated secret entry', key)

        self.keys = obj['generated']['keys']

    def generate_obj(self):
        """Generates the secret object, respecting existing information
        and user specified options"""
        secret_obj = {}
        if self.existing:
            secret_obj = deepcopy(self.existing)
        for key in self.keys:
            key_name = key['name']
            if self.existing and key_name in self.existing and not key.get('overwrite'):
                LOG.debug('Not overwriting %s/%s', self.path, key_name)
                continue
            else:
                secret_obj[key_name] = generated_key(key)

        return secret_obj

    def diff(self, obj=None):
        if self.present and not self.existing:
            return aomi.model.resource.ADD
        if not self.present and self.existing:
            return aomi.model.resource.DEL
        if self.present and self.existing:
            overwrites = [x for x in self.keys if x.get('overwrite')]
            if overwrites:
                pass
            return aomi.model.resource.OVERWRITE
        return aomi.model.resource.NOOP

    def sync(self, vault_client):
        gen_obj = self.generate_obj()
        self._obj = gen_obj
        super(Generated, self).sync(vault_client)