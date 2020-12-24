# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/vsm/ssh_keys.py
# Compiled at: 2016-06-13 14:11:03
"""
Keys Service
"""
from vsm import flags
from vsm.openstack.common import log as logging
LOG = logging.getLogger(__name__)
FLAGS = flags.FLAGS

class SSHManager(object):
    """Chooses a host to create storages."""

    def __init__(self, fpath=FLAGS.authorized_keys):
        self._fpath = fpath or FLAGS.authorized_keys
        self._key_list = open(self._fpath, 'r').readlines()

    def _get_hostname(self, key):
        if key.find('@') != -1:
            return key.split('@')[1].strip()

    def _flush_key_file(self):
        fd = open(self._fpath, 'w')
        for k in self._key_list:
            fd.write(k + '\n')

        fd.close()

    def _find_key(self, key):
        for k in self._key_list:
            if k.find(key.strip()) != -1:
                return True

        return False

    def _append_key(self, key):
        if self._find_key(key) == False:
            self._key_list.append(key)
            fd = open(self._fpath, 'a+')
            fd.write(key)
            fd.close()

    def _is_new_key(self, key):
        host = self._get_hostname(key)
        for k in self._key_list:
            h = self._get_hostname(k)
            if h.find(host) != -1 or host.find(h) != -1:
                return False

        return True

    def _find_old_key(self, key):
        host = self._get_hostname(key)
        for k in self._key_list:
            h = self._get_hostname(k)
            if h.find(host) != -1 or host.find(h) != -1:
                return k

        return

    def _update_key(self, key):
        if self._find_key(key) == False:
            if self._is_new_key(key):
                self._key_list.remove(self._find_old_key(key))
                self._flush_key_file()
            else:
                self._append_key(key)