# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/ssh/storage.py
# Compiled at: 2020-02-11 04:03:56
from __future__ import unicode_literals
import logging, os
from django.utils.translation import ugettext_lazy as _
import paramiko
from reviewboard.ssh.errors import MakeSSHDirError, UnsupportedSSHKeyError

class SSHStorage(object):

    def __init__(self, namespace=None):
        self.namespace = namespace

    def read_user_key(self):
        """Reads the user key.

        This will return an instance of :py:mod:`paramiko.PKey` representing
        the user key, if one exists. Otherwise, it will return None.
        """
        raise NotImplementedError

    def write_user_key(self, key):
        """Writes a user key.

        The user key will be stored, and can be accessed later by
        read_user_key.

        This will raise UnsupportedSSHKeyError if ``key`` isn't a
        :py:mod:`paramiko.RSAKey` or :py:mod:`paramiko.DSSKey`.

        It may also raise :py:mod:`paramiko.SSHException` for key-related
        errors.
        """
        raise NotImplementedError

    def delete_user_key(self, key):
        """Deletes a user key.

        The user key, if it exists, will be removed from storage.

        If no user key exists, this will do nothing.
        """
        raise NotImplementedError

    def read_authorized_keys(self):
        """Reads a list of authorized keys.

        The authorized keys are returned as a list of raw key data, which
        can then be converted into classes as needed.
        """
        raise NotImplementedError

    def read_host_keys(self):
        """Reads a list of known host keys.

        This known host keys are returned as a list of raw key data, which
        can then be converted into classes as needed.
        """
        raise NotImplementedError

    def add_host_key(self, hostname, key):
        """Adds a known key for a given host.

        This will store a mapping of the key and hostname so that future
        access to the server will know the host is legitimate.
        """
        raise NotImplementedError

    def replace_host_key(self, hostname, old_key, new_key):
        """Replaces a host key in the known hosts list with another.

        This is used for replacing host keys that have changed.
        """
        raise NotImplementedError


class FileSSHStorage(SSHStorage):
    DEFAULT_KEY_FILES = (
     (
      paramiko.RSAKey, b'id_rsa'),
     (
      paramiko.DSSKey, b'id_dsa'))
    SSH_DIRS = ('.ssh', 'ssh')
    _ssh_dir = None

    def get_user_key_info(self):
        for cls, filename in self.DEFAULT_KEY_FILES:
            for sshdir in self.SSH_DIRS:
                path = os.path.join(self.get_ssh_dir(sshdir), filename)
                if os.path.isfile(path):
                    return (cls, path)

        return (None, None)

    def read_user_key(self):
        cls, path = self.get_user_key_info()
        if path:
            return cls.from_private_key_file(path)
        else:
            return

    def write_user_key(self, key):
        key_filename = None
        for cls, filename in self.DEFAULT_KEY_FILES:
            if isinstance(key, cls):
                key_filename = filename

        if not key_filename:
            raise UnsupportedSSHKeyError()
        sshdir = self.ensure_ssh_dir()
        filename = os.path.join(sshdir, key_filename)
        key.write_private_key_file(filename)
        return

    def delete_user_key(self):
        cls, path = self.get_user_key_info()
        if path:
            os.unlink(path)

    def read_authorized_keys(self):
        filename = os.path.join(self.get_ssh_dir(), b'authorized_keys')
        try:
            fp = open(filename, b'r')
            lines = fp.readlines()
            fp.close()
            return lines
        except IOError as e:
            logging.warning(b'Unable to read SSH authorized_keys file %s: %s' % (
             filename, e))
            raise

    def read_host_keys(self):
        filename = self.get_host_keys_filename()
        lines = []
        if os.path.exists(filename):
            try:
                with open(filename, b'r') as (f):
                    for line in f:
                        line = line.strip()
                        if line and line[0] != b'#':
                            lines.append(line)

            except IOError as e:
                logging.error(b'Unable to read host keys file %s: %s' % (
                 filename, e))

        return lines

    def add_host_key(self, hostname, key):
        self.ensure_ssh_dir()
        filename = self.get_host_keys_filename()
        try:
            with open(filename, b'a') as (fp):
                fp.write(b'%s %s %s\n' % (hostname, key.get_name(),
                 key.get_base64()))
        except IOError as e:
            raise IOError(_(b'Unable to write host keys file %(filename)s: %(error)s') % {b'filename': filename, 
               b'error': e})

    def replace_host_key(self, hostname, old_key, new_key):
        filename = self.get_host_keys_filename()
        if not os.path.exists(filename):
            self.add_host_key(hostname, new_key)
            return
        try:
            with open(filename, b'r') as (fp):
                lines = fp.readlines()
            old_key_base64 = old_key.get_base64()
        except IOError as e:
            raise IOError(_(b'Unable to read host keys file %(filename)s: %(error)s') % {b'filename': filename, 
               b'error': e})

        try:
            with open(filename, b'w') as (fp):
                for line in lines:
                    parts = line.strip().split(b' ')
                    if parts[(-1)] == old_key_base64:
                        parts[1] = new_key.get_name()
                        parts[-1] = new_key.get_base64()
                    fp.write((b' ').join(parts) + b'\n')

        except IOError as e:
            raise IOError(_(b'Unable to write host keys file %(filename)s: %(error)s') % {b'filename': filename, 
               b'error': e})

    def get_host_keys_filename(self):
        """Returns the path to the known host keys file."""
        return os.path.join(self.get_ssh_dir(), b'known_hosts')

    def get_ssh_dir(self, ssh_dir_name=None):
        """Returns the path to the SSH directory on the system.

        By default, this will attempt to find either a .ssh or ssh directory.
        If ``ssh_dir_name`` is specified, the search will be skipped, and we'll
        use that name instead.
        """
        path = self._ssh_dir
        if not path or ssh_dir_name:
            path = os.path.expanduser(b'~')
            if not ssh_dir_name:
                ssh_dir_name = None
                for name in self.SSH_DIRS:
                    if os.path.exists(os.path.join(path, name)):
                        ssh_dir_name = name
                        break

                if not ssh_dir_name:
                    ssh_dir_name = self.SSH_DIRS[0]
            path = os.path.join(path, ssh_dir_name)
            if not ssh_dir_name:
                self.__class__._ssh_dir = path
        if self.namespace:
            return os.path.join(path, self.namespace)
        else:
            return path
            return

    def ensure_ssh_dir(self):
        """Ensures the existance of the .ssh directory.

        If the directory doesn't exist, it will be created.
        The full path to the directory will be returned.

        Callers are expected to handle any exceptions. This may raise
        IOError for any problems in creating the directory.
        """
        sshdir = self.get_ssh_dir()
        if not os.path.exists(sshdir):
            try:
                os.makedirs(sshdir, 448)
            except OSError:
                raise MakeSSHDirError(sshdir)

        return sshdir