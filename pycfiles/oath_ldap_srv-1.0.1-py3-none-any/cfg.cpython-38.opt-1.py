# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /oathldap_srv/cfg.py
# Compiled at: 2020-04-13 16:52:27
# Size of source mod 2**32: 3042 bytes
"""
oathldap_srv.cfg - configuration vars
"""
import os, logging, ipaddress
from configparser import ConfigParser
from ldap0.ldapurl import LDAPUrl

def val_list(cfg_val):
    """
    Returns list of int or str values splitted from space- or
    comma-separated string with all white-spaces stripped
    """
    val_set = set()
    res = []
    for val in (cfg_val or '').strip().replace(',', '\n').replace(' ', '\n').split('\n'):
        val = val.strip()
        if val and val not in val_set:
            try:
                val = int(val)
            except ValueError:
                pass
            else:
                res.append(val)
                val_set.add(val)
        return res


def ldap_url_list(cfg_val):
    """
    Returns list of LDAPUrl instances from space- or comma-separated string
    """
    return [LDAPUrl(val) for val in val_list(cfg_val)]


def ip_network_list(cfg_val):
    """
    Returns list of IPNetwork instances from space- or comma-separated string
    """
    return [ipaddress.ip_network(val) for val in val_list(cfg_val)]


class Config:
    __doc__ = '\n    method-less class containing all config params\n    '
    default_section = None
    type_map = {'log_level': str.upper}
    required_params = ()
    socket_path = None
    log_level = 'INFO'
    logging_conf = None
    logger_name = None
    log_vars = []

    def __init__(self, cfg_filename):
        """
        read and parse config file into dict
        """
        if not os.path.exists(cfg_filename):
            raise SystemExit('Configuration file %r is missing!' % (cfg_filename,))
        cfg_parser = ConfigParser(interpolation=None,
          default_section=(self.default_section))
        cfg_parser.read([cfg_filename])
        for key in sorted(cfg_parser.defaults()):
            if not hasattr(self, key):
                raise SystemExit('Unknown config key-word %r' % (key,))
            type_func = self.type_map.get(key, str)
            raw_val = cfg_parser.get(self.default_section, key)
            try:
                val = type_func(raw_val)
            except ValueError:
                raise SystemExit('Invalid value for %r. Expected %s string, but got %r' % (
                 key, type_func.__name__, raw_val))
            else:
                setattr(self, key, val)
        else:
            for key in self.required_params:
                if not hasattr(self, key) or getattr(self, key) is None:
                    raise SystemExit('Mandatory config parameter %r missing' % (key,))