# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/aomi/model/ssh.py
# Compiled at: 2017-11-17 12:53:02
# Size of source mod 2**32: 799 bytes
__doc__ = ' SSH Dynamic Credentials '
from aomi.model.resource import Secret
from aomi.validation import sanitize_mount

class SSHRole(Secret):
    """SSHRole"""
    resource_key = 'ssh_creds'
    required_fields = ['key_type']
    backend = 'ssh'

    def __init__(self, obj, opt):
        super(SSHRole, self).__init__(obj, opt)
        self.mount = sanitize_mount(obj.get('mount', 'ssh'))
        a_name = obj.get('name', obj['ssh_creds'])
        self.path = '%s/roles/%s' % (self.mount, a_name)
        self._obj = {'key_type': obj['key_type']}
        if 'cidr_list' in obj:
            self._obj['cidr_list'] = ','.join(obj['cidr_list'])
        if 'default_user' in obj:
            self._obj['default_user'] = obj['default_user']
        self.tunable(obj)