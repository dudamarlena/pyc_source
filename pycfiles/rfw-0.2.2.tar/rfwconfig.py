# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/sk/seckiss/rfw/rfw/rfwconfig.py
# Compiled at: 2014-03-26 05:27:12
import logging, sys, types, os.path, re, config, iputil, timeutil
from ConfigParser import NoOptionError
log = logging.getLogger('rfw.rfwconfig')

class RfwConfig(config.Config):

    def __init__(self, path):
        self._whitelist = None
        try:
            config.Config.__init__(self, path)
            if self.is_outward_server():
                self.outward_server_port()
                self.outward_server_ip()
            if self.is_local_server():
                self.local_server_port()
                self.is_local_server_authentication()
            self.is_non_restful()
            if self.is_outward_server() or self.is_local_server_authentication():
                self.auth_username()
                self.auth_password()
            self.whitelist_file()
            self.whitelist()
            self.iptables_path()
            self.default_expire()
        except config.ConfigError as e:
            log.error(str(e))
            sys.exit(1)
        except Exception as e:
            log.error(self.config_error(str(e)))
            sys.exit(1)

        try:
            if self.is_outward_server():
                self.outward_server_certfile()
                self.outward_server_keyfile()
        except config.ConfigError as e:
            log.error(str(e))
            log.error('Before running rfw you must generate or import certificates. See /etc/rfw/deploy/README.rst')
            sys.exit(1)

        return

    def is_outward_server(self):
        return self._getflag('outward.server', 'outward.server not enabled. Ignoring outward.server.port and outward.server.ip if present.')

    def outward_server_port(self):
        if self.is_outward_server():
            port = self._get('outward.server.port')
            if port and iputil.validate_port(port):
                return port
            raise self.config_error('Wrong outward.server.port value. It should be a single number from the 1..65535 range')
        else:
            self.config_error('outward.server.port read while outward.server not enabled')

    def outward_server_ip(self):
        if self.is_outward_server():
            try:
                return self._get('outward.server.ip')
            except NoOptionError as e:
                raise self.config_error(str(e))

        else:
            raise self.config_error('outward.server.ip read while outward.server not enabled')

    def outward_server_certfile(self):
        if self.is_outward_server():
            return self._getfile('outward.server.certfile')
        raise self.config_error('outward.server.certfile read while outward.server not enabled')

    def outward_server_keyfile(self):
        if self.is_outward_server():
            return self._getfile('outward.server.keyfile')
        raise self.config_error('outward.server.keyfile read while outward.server not enabled')

    def is_local_server(self):
        return self._getflag('local.server', 'local.server not enabled. Ignoring local.server.port if present.')

    def local_server_port(self):
        if self.is_local_server():
            try:
                port = self._get('local.server.port')
                if port and iputil.validate_port(port):
                    return port
                raise self.config_error('Wrong local.server.port value. It should be a single number from the 1..65535 range')
            except NoOptionError as e:
                raise self.config_error(str(e))

        else:
            raise self.config_error('local.server.port read while local.server not enabled')

    def is_non_restful(self):
        return self._getflag('non.restful')

    def is_local_server_authentication(self):
        if self.is_local_server():
            return self._getflag('local.server.authentication')
        raise self.config_error('local.server.authentication read while local.server not enabled')

    def auth_username(self):
        if self.is_outward_server() or self.is_local_server_authentication():
            try:
                username = self._get('auth.username')
                if username:
                    return username
                raise self.config_error('auth.username cannot be empty')
            except NoOptionError as e:
                raise self.config_error(str(e))

        else:
            raise self.config_error('auth.username read while outward.server not enabled and local.server.authentication not enabled')

    def auth_password(self):
        if self.is_outward_server() or self.is_local_server_authentication():
            try:
                password = self._get('auth.password')
                if password:
                    return password
                raise self.config_error('auth.password cannot be empty')
            except NoOptionError as e:
                raise self.config_error(str(e))

        else:
            raise self.config_error('auth.password read while outward.server not enabled and local.server.authentication not enabled')

    def _chain_action(self, name):
        try:
            action = self._get(name)
            if action:
                action = action.upper()
                if action in ('DROP', 'ACCEPT'):
                    return action
                raise self.config_error(('allowed values for {} are DROP or ACCEPT').format(name))
            else:
                raise self.config_error(('{} cannot be empty. Allowed values are DROP or ACCEPT').format(name))
        except NoOptionError as e:
            raise self.config_error(str(e))

    def whitelist_file(self):
        return self._getfile('whitelist.file')

    def whitelist(self):
        if self._whitelist is None:
            wfile = self.whitelist_file()
            with open(wfile) as (f):
                lines = f.readlines()
            ips = [ iputil.validate_ip_cidr(line, allow_no_mask=True) for line in lines if line.strip() and not line.strip().startswith('#') ]
            if False in ips:
                raise self.config_error(('Wrong IP address format in {}').format(wfile))
            if not ips:
                raise self.config_error(('Could not find a valid IP address in {}').format(wfile))
            self._whitelist = ips
        return self._whitelist

    def iptables_path(self):
        ipt = self._get('iptables.path')
        if ipt:
            return ipt
        raise self.config_error('iptables.path cannot be empty')

    def default_expire(self):
        """return parsed default.expire in seconds as string
        """
        exp = self._get('default.expire')
        if not exp:
            raise self.config_error('default.expire missing')
        interval = timeutil.parse_interval(exp)
        if interval is None:
            raise self.config_error('default.expire missing or incorrect format')
        else:
            return str(interval)
        return