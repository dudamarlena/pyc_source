# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/secrets/config.py
# Compiled at: 2015-12-23 04:08:42
"""
Configuration file class for LDAP servers

Example file contents:

[default]
server = ldap://localhost/
admin_dn = cn=manager,dc=example,dc=com
uid_format = uid=%(username)s,%(dn)s

[mail]
description = Mail account password
dn = ou=users,dc=mail,dc=example,dc=com
search_fields = cn
uid_attr = cn

[shell]
description = Shell access password
dn = ou=users,dc=shell,dc=example,dc=com

"""
import configobj, os
DEFAULT_PASSWORD_CONFIG = '/etc/secrets.conf'
DEFAULT_SEARCH_FIELDS = [
 'uid',
 'gecos']
DEFAULT_UID_ATTR = [
 'uid']
VALID_CONFIG_FIELDS = [
 'server',
 'dn',
 'admin_dn',
 'uid_format',
 'uid_attr',
 'search_fields',
 'description']

class SecretsConfigError(Exception):
    pass


class SecretsConfig(dict):
    """
    Parser for configuration file of LDAP password servers,
    DN and ADMIN DN values.
    """

    def __init__(self, path=None):
        path = path is not None and path or DEFAULT_PASSWORD_CONFIG
        self.__admin_credentials_cache = {}
        self.defaults = {'server': 'ldap://localhost/', 
           'uid_format': 'uid=%(username)s,%(dn)s', 
           'search_fields': DEFAULT_SEARCH_FIELDS, 
           'uid_attr': DEFAULT_UID_ATTR, 
           'dn': None, 
           'admin_dn': None}
        if not os.path.isfile(path):
            raise SecretsConfigError(('No such file: {0}').format(path))
        if not os.access(path, os.R_OK):
            raise SecretsConfigError(('No permissions to read {0}').format(path))
        config = configobj.ConfigObj(path, list_values=False, interpolation=False)
        for name, settings in config.items():
            fields = {}
            for k, v in settings.items():
                if k not in VALID_CONFIG_FIELDS:
                    raise SecretsConfigError(('Unknown key in configuration: {0}').format(k))
                v = unicode(v, 'utf-8')
                if name == 'default':
                    self.defaults[k] = v
                else:
                    fields[k] = v

            if name == 'default':
                continue
            for k in ['server', 'dn', 'admin_dn', 'uid_format', 'uid_attr', 'search_fields']:
                if not fields.has_key(k):
                    fields[k] = self.defaults[k]

            self[name] = SecretsService(name, **fields)

        return

    def save(self, path):
        """
        Save configuration to given path
        """
        config = configobj.ConfigObj(list_values=False, interpolation=False)
        config['default'] = {}
        for k, v in self.defaults.items():
            if v is None:
                continue
            config['default'][k] = v

        for name, service in self.items():
            config[name] = {}
            for k in VALID_CONFIG_FIELDS:
                v = getattr(service, k)
                if k in self.defaults.keys() and v == self.defaults[k]:
                    continue
                config[name][k] = v

        try:
            config.write(open(path, 'w'))
        except IOError as (ecode, emsg):
            raise SecretsConfigError('Error writing %s: %s' % (path, emsg))

        return

    def get_cached_admin_password(self, server):
        """
        Return cached admin DN password or None if not found
        """
        try:
            return self.__admin_credentials_cache[server]
        except KeyError:
            pass

        if os.access('/etc/ldap.secret', os.R_OK):
            return open('/etc/ldap.secret', 'r').readline().strip()
        else:
            return

    def set_cached_admin_password(self, server, password):
        """
        Stores admin DN password to local cache to be used when
        multiple operatins are requested on same server.
        Always remember to wipe cache with clear_password_cache()
        """
        if self.__admin_credentials_cache.has_key(server):
            for i in enumerate(self.__admin_credentials_cache[server]):
                self.__admin_credentials_cache[server][i] = ''

        self.__admin_credentials_cache[server] = password

    def clear_password_cache(self):
        """
        Clear local admin password cache, overwriting fields with
        empty values before deallocating
        """
        for k, v in self.__admin_credentials_cache.items():
            for i in enumerate(v):
                self.__admin_credentials_cache[k][i] = ''

        self.__admin_credentials_cache.clear()


class SecretsService(object):
    """
    Stores password service configuration entries from SecretsConfig file
    """

    def __init__(self, name, server, dn, admin_dn, uid_format, uid_attr, search_fields, description=None):
        self.name = name
        self.server = server
        self.uid_format = uid_format
        self.uid_attr = uid_attr
        self.dn = dn
        self.admin_dn = admin_dn
        if description is None:
            description = '%s password' % self.name
        self.description = description
        self.search_fields = search_fields
        return

    def __repr__(self):
        return '%s on %s DN %s' % (self.name, self.server, self.dn)