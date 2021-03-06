# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /aehostd/cfg.py
# Compiled at: 2020-05-12 08:42:04
# Size of source mod 2**32: 12749 bytes
__doc__ = '\naehostd.cfg - configuration vars\n'
import os, socket, pwd, grp, logging
from configparser import ConfigParser
import collections
from .base import IdempotentFile
DEFAULT_SECTION = 'aehostd'

def val_list(cfg_val):
    """
    Returns list of values splitted from space- or comma-separated string
    with all white-spaces stripped
    """
    val_set = set()
    res = []
    for val in (cfg_val or ).strip().replace(',', '\n').replace(' ', '\n').split('\n'):
        val = val.strip()
        if val and val not in val_set:
            res.append(val)
            val_set.add(val)
        return res


def val_set(cfg_val):
    """
    Returns set of values splitted from space- or comma-separated string
    with all white-spaces stripped
    """
    return set(val_list(cfg_val))


def rotated_val_list(cfg_val, rval=None):
    """
    Returns list of values splitted by val_list() rotated by rval.
    """
    if not cfg_val:
        return []
    lst = collections.deque(sorted(val_list(cfg_val)))
    if rval is None:
        rval = hash(socket.getfqdn()) % len(lst)
    lst.rotate(rval)
    return lst


class ConfigParameters:
    """ConfigParameters"""
    __slots__ = ('aehost_vaccount', 'aehost_vaccount_t', 'aehost_vaccount_t', 'binddn',
                 'bindpwfile', 'cache_ttl', 'conn_ttl', 'cvtsudoers_exec', 'gecos_tmpl',
                 'gid', 'homedir_tmpl', 'loginshell_default', 'loginshell_override',
                 'loglevel', 'logsocket', 'monitor', 'netaddr_level', 'netaddr_refresh',
                 'nss_ignore_gids', 'nss_ignore_groups', 'nss_ignore_uids', 'nss_ignore_users',
                 'nss_max_gid', 'nss_max_uid', 'nss_min_gid', 'nss_min_uid', 'pam_authc_cache_attrs',
                 'pam_authc_cache_ttl', 'pam_authz_search', 'pam_passmod_deny_msg',
                 'refresh_sleep', 'socketpath', 'socketperms', 'sockettimeout', 'sshkeys_dir',
                 'sudoers_file', 'sudoers_includedir', 'timelimit', 'tls_cacertfile',
                 'tls_cert', 'tls_key', 'uid', 'uid', 'uri_list', 'uri_pool', 'vgroup_gid2attr',
                 'vgroup_name2attr', 'vgroup_name_prefix', 'vgroup_rgid_offset',
                 'vgroup_role_map', 'visudo_exec')
    cfg_type_map = {'monitor':float, 
     'refresh_sleep':float, 
     'search_timelimit':float, 
     'cache_ttl':float, 
     'conn_ttl':float, 
     'loglevel':int, 
     'netaddr_level':int, 
     'netaddr_refresh':float, 
     'nss_max_gid':int, 
     'nss_max_uid':int, 
     'nss_min_gid':int, 
     'nss_min_uid':int, 
     'uri_list':val_list, 
     'uri_pool':rotated_val_list, 
     'sockettimeout':float, 
     'timelimit':int, 
     'vgroup_rgid_offset':int, 
     'bindpwfile':IdempotentFile, 
     'pam_authc_cache_attrs':val_set, 
     'pam_authc_cache_ttl':float}

    def __init__(self):
        self.uid = None
        self.gid = None
        self.loglevel = logging.INFO
        self.logsocket = None
        self.monitor = -1.0
        self.socketpath = '/var/run/aehostd/socket'
        self.sockettimeout = 10.0
        self.socketperms = '0666'
        self.uri_list = []
        self.uri_pool = []
        self.binddn = None
        self.bindpwfile = IdempotentFile('/var/lib/aehostd/aehostd.pw')
        self.timelimit = 6.0
        self.cache_ttl = 6.0
        self.tls_cacertfile = None
        self.tls_cert = None
        self.tls_key = None
        self.conn_ttl = 1800.0
        self.nss_ignore_users = {x.pw_name for x in pwd.getpwall()}
        self.nss_ignore_uids = {x.pw_uid for x in pwd.getpwall()}
        self.nss_ignore_groups = {x.gr_name for x in grp.getgrall()}
        self.nss_ignore_gids = {x.pw_gid for x in pwd.getpwall()}
        self.refresh_sleep = 60.0
        self.nss_min_uid = 0
        self.nss_min_gid = 0
        self.nss_max_uid = 65500
        self.nss_max_gid = 65500
        self.netaddr_refresh = -1.0
        self.netaddr_level = 2
        self.vgroup_name_prefix = 'ae-vgrp-'
        self.vgroup_rgid_offset = 9000
        self.sshkeys_dir = None
        self.aehost_vaccount = 'aehost-init:x:9042:9042:AE-DIR virtual host init account:/tmp:/usr/sbin/nologin'
        self.gecos_tmpl = 'AE-DIR user {username}'
        self.homedir_tmpl = None
        self.loginshell_default = '/usr/sbin/nologin'
        self.loginshell_override = None
        self.sudoers_file = '/var/lib/aehostd/ae-dir-sudoers-export'
        self.sudoers_includedir = '/etc/sudoers.d'
        self.visudo_exec = '/usr/sbin/visudo'
        self.cvtsudoers_exec = '/usr/bin/cvtsudoers'
        self.pam_authz_search = None
        self.pam_passmod_deny_msg = None
        self.pam_authc_cache_attrs = {
         'username',
         'password'}
        self.pam_authc_cache_ttl = -1.0
        self.aehost_vaccount_t = self._passwd_tuple(self.aehost_vaccount)

    @staticmethod
    def _passwd_tuple(pw_str):
        """
        split passwd line into tuple
        """
        passwd_fields = pw_str.split(':')
        return (
         passwd_fields[0],
         passwd_fields[1],
         int(passwd_fields[2]),
         int(passwd_fields[3]),
         passwd_fields[4],
         passwd_fields[5],
         passwd_fields[6])

    def get_ldap_uris(self):
        """
        return combined list of LDAP URIs to connect to
        derived from config parameters 'uri_pool' and 'uri_list'
        """
        return list(self.uri_pool)[:] + list(reversed(self.uri_list))

    def read_config(self, cfg_filename):
        """
        read and parse config file into dict
        """
        if not os.path.exists(cfg_filename):
            raise SystemExit('Configuration file %r is missing!' % cfg_filename)
        else:
            cfg_parser = ConfigParser(interpolation=None,
              default_section=DEFAULT_SECTION)
            cfg_parser.read([cfg_filename])
            for key in sorted(cfg_parser.defaults()):
                if not hasattr(self, key):
                    raise ValueError('Unknown config key-word %r' % key)
                type_func = self.cfg_type_map.get(key, str)
                raw_val = cfg_parser.get(DEFAULT_SECTION, key)
                try:
                    val = type_func(raw_val)
                except ValueError:
                    raise ValueError('Invalid value for %r. Expected %s string, but got %r' % (
                     key, type_func.__name__, raw_val))
                else:
                    setattr(CFG, key, val)

            self.vgroup_role_map = {'aeVisibleGroups':(self.vgroup_rgid_offset + 0, self.vgroup_name_prefix + 'role-all'),  'aeLoginGroups':(
              self.vgroup_rgid_offset + 1, self.vgroup_name_prefix + 'role-login'), 
             'aeLogStoreGroups':(
              self.vgroup_rgid_offset + 2, self.vgroup_name_prefix + 'role-log'), 
             'aeSetupGroups':(
              self.vgroup_rgid_offset + 3, self.vgroup_name_prefix + 'role-setup')}
            self.vgroup_gid2attr = dict([(
             val[0], attr) for attr, val in self.vgroup_role_map.items()])
            self.vgroup_name2attr = dict([(
             val[1], attr) for attr, val in self.vgroup_role_map.items()])
            self.aehost_vaccount_t = self._passwd_tuple(self.aehost_vaccount)
            if self.uid is None:
                pw_user = pwd.getpwuid(os.getuid())
            else:
                pw_user = pwd.getpwnam(self.uid)
            self.uid = pw_user.pw_uid
            if self.gid is None:
                self.gid = pw_user.pw_gid
            else:
                self.gid = grp.getgrnam(self.gid).gr_gid


CFG = ConfigParameters()