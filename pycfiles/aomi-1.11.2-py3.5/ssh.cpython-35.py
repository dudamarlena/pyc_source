# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/aomi/model/ssh.py
# Compiled at: 2017-11-17 12:53:02
# Size of source mod 2**32: 799 bytes
""" SSH Dynamic Credentials """
from aomi.model.resource import Secret
from aomi.validation import sanitize_mount

class SSHRole(Secret):
    __doc__ = 'SSH Credential Backend'
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