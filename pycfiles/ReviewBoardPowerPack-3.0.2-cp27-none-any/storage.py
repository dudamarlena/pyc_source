# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /rbpowerpack/sshdb/storage.py
# Compiled at: 2019-06-17 15:11:31
from __future__ import unicode_literals
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from reviewboard.ssh.storage import SSHStorage, FileSSHStorage
from rbpowerpack.sshdb.models import StoredHostKeys, StoredUserKey
from rbpowerpack.sshdb.secrets import has_valid_sshdb_secret_key

class DBSSHStorage(SSHStorage):

    def __init__(self, namespace=None, *args, **kwargs):
        namespace = namespace or None
        if not has_valid_sshdb_secret_key():
            raise ImproperlyConfigured(b'settings.SSHDB_SECRET_KEY must be defined and set to a 32-character unguessable string for sshdb')
        super(DBSSHStorage, self).__init__(namespace=namespace, *args, **kwargs)
        self._file_storage = FileSSHStorage(namespace=namespace, *args, **kwargs)
        return

    def read_user_key(self):
        try:
            stored_key = StoredUserKey.objects.get(namespace=self.namespace)
            return stored_key.get_key()
        except StoredUserKey.DoesNotExist:
            return

        return

    def write_user_key(self, key):
        stored_key, is_new = StoredUserKey.objects.get_or_create(namespace=self.namespace)
        stored_key.set_key(key)
        stored_key.save()

    def delete_user_key(self):
        StoredUserKey.objects.filter(namespace=self.namespace).delete()

    def read_authorized_keys(self):
        return self._file_storage.read_authorized_keys()

    def read_host_keys(self):
        try:
            stored_keys = StoredHostKeys.objects.get(namespace=self.namespace)
            lines = []
            for line in stored_keys.host_keys.splitlines():
                line = line.strip()
                if line and line[0] != b'#':
                    lines.append(line)

            return lines
        except StoredHostKeys.DoesNotExist:
            return []

    def import_host_keys(self, lines):
        """Imports a host keys blog.

        This is used internally by the import-ssh-keys management command.
        """
        stored_keys, is_new = StoredHostKeys.objects.get_or_create(namespace=self.namespace)
        stored_keys.host_keys = (b'\n').join(lines)
        stored_keys.save()

    def add_host_key(self, hostname, key):
        stored_keys, is_new = StoredHostKeys.objects.get_or_create(namespace=self.namespace)
        stored_keys.host_keys += b'%s %s %s\n' % (hostname, key.get_name(),
         key.get_base64())
        stored_keys.save()

    def replace_host_key(self, hostname, old_key, new_key):
        stored_keys, is_new = StoredHostKeys.objects.get_or_create(namespace=self.namespace)
        if is_new:
            stored_keys.host_keys = b'%s %s %s\n' % (hostname,
             new_key.get_name(),
             new_key.get_base64())
        else:
            old_key_base64 = old_key.get_base64()
            lines = stored_keys.host_keys.splitlines()
            stored_keys.host_keys = b''
            for line in lines:
                parts = line.strip().split(b' ')
                if parts[(-1)] == old_key_base64:
                    parts[1] = new_key.get_name()
                    parts[-1] = new_key.get_base64()
                stored_keys.host_keys += (b' ').join(parts) + b'\n'

        stored_keys.save()


_storage_name = b'%s.%s' % (DBSSHStorage.__module__, DBSSHStorage.__name__)

def enable_sshdb(import_keys=False):
    """Enables the SSH database storage backend."""
    if not has_valid_sshdb_secret_key():
        return False
    settings.RBSSH_STORAGE_BACKEND = _storage_name
    if import_keys:
        from rbpowerpack.sshdb.importer import import_sshdb_keys
        import_sshdb_keys()
    return True


def disable_sshdb():
    """Disables the SSH database storage backend."""
    storage_backend = getattr(settings, b'RBSSH_STORAGE_BACKEND', None)
    if storage_backend == _storage_name:
        delattr(settings, b'RBSSH_STORAGE_BACKEND')
    return