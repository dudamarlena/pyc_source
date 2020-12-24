# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /aehostd/cfg.py
# Compiled at: 2020-03-29 09:22:38
# Size of source mod 2**32: 10012 bytes
"""
aehostd.cfg - configuration vars
"""
from __future__ import absolute_import
import os, socket, pwd, grp, logging
from configparser import RawConfigParser
import collections
from .base import IdempotentFile

def val_list(cfg_val):
    """
    Returns list of values splitted from space- or comma-separated string
    with all white-spaces stripped
    """
    val_set = set()
    res = []
    for val in (cfg_val or '').strip().replace(' ', ',').split(','):
        val = val.strip()
        if val and val not in val_set:
            res.append(val)
            val_set.add(val)
        return res


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
    __doc__ = '\n    method-less class containing all config params\n    '
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
     'pam_authc_cache_ttl':float}
    uid = None
    gid = None
    loglevel = logging.INFO
    logsocket = None
    monitor = -1.0
    socketpath = '/var/run/aehostd/socket'
    sockettimeout = 10.0
    socketperms = '0666'
    uri_list = []
    uri_pool = []
    binddn = None
    bindpwfile = IdempotentFile('/var/lib/aehostd/aehostd.pw')
    timelimit = 6.0
    cache_ttl = 6.0
    tls_cacertfile = None
    tls_cert = None
    tls_key = None
    conn_ttl = 1800.0
    nss_ignore_users = {x.pw_name for x in pwd.getpwall()}
    nss_ignore_uids = {x.pw_uid for x in pwd.getpwall()}
    nss_ignore_groups = {x.gr_name for x in grp.getgrall()}
    nss_ignore_gids = {x.pw_gid for x in pwd.getpwall()}
    refresh_sleep = 60.0
    nss_min_uid = 0
    nss_min_gid = 0
    nss_max_uid = 65500
    nss_max_gid = 65500
    netaddr_refresh = -1.0
    netaddr_level = 2
    vgroup_name_prefix = 'ae-vgrp-'
    vgroup_rgid_offset = 9000
    sshkeys_dir = None
    aehost_vaccount = 'aehost-init:x:9042:9042:AE-DIR virtual host init account:/tmp:/usr/sbin/nologin'
    gecos_tmpl = 'AE-DIR user {username}'
    homedir_tmpl = None
    loginshell_default = '/usr/sbin/nologin'
    loginshell_override = None
    sudoers_file = '/var/lib/aehostd/ae-dir-sudoers-export'
    sudoers_includedir = '/etc/sudoers.d'
    visudo_exec = '/usr/sbin/visudo'
    cvtsudoers_exec = '/usr/bin/cvtsudoers'
    pam_authz_search = None
    pam_passmod_deny_msg = None
    pam_authc_cache_ttl = -1.0

    def __init__(self):
        self.aehost_vaccount_t = self._passwd_tuple(self.aehost_vaccount)

    @staticmethod
    def _passwd_tuple(pw_str):
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
        return list(self.uri_pool)[:] + list(reversed(self.uri_list))

    def read_config(self, cfg_filename):
        """
        read and parse config file into dict
        """
        if not os.path.exists(cfg_filename):
            raise SystemExit('Configuration file %r is missing!' % cfg_filename)
        else:
            cfg_parser = RawConfigParser()
            cfg_parser.read([cfg_filename])
            for key in sorted(cfg_parser.options('aehostd')):
                if not hasattr(self, key):
                    raise ValueError('Unknown config key-word %r' % key)
                type_func = self.cfg_type_map.get(key, str)
                raw_val = cfg_parser.get('aehostd', key)
                try:
                    val = type_func(raw_val)
                except ValueError:
                    raise ValueError('Invalid value for %r. Expected %s string, but got %r' % (
                     key, type_func.__name__, raw_val))
                else:
                    setattr(CFG, key, val)
            else:
                self.vgroup_role_map = {'aeVisibleGroups':(
                  self.vgroup_rgid_offset + 0, self.vgroup_name_prefix + 'role-all'), 
                 'aeLoginGroups':(
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