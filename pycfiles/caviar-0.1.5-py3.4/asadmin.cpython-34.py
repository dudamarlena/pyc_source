# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/caviar/engine/asadmin.py
# Compiled at: 2017-10-25 18:02:55
# Size of source mod 2**32: 4127 bytes
"""
Asadmin module.
"""
import random, string

class Asadmin:
    __doc__ = '\n\tAsadmin utility.\n\t'

    def __init__(self, ssh_session_fact, das_machine, master_password):
        self._Asadmin__ssh_session = ssh_session_fact.session(das_machine.appserver_user, das_machine.host)
        self._Asadmin__das_machine = das_machine
        self._Asadmin__master_password = master_password

    def __create_pwd_id(self):
        return ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(8))

    def __run(self, cmd, host=None, port=None, user=None, passwords=None, params=None):
        try:
            args = []
            args.extend(['--terse', 'true'])
            args.extend(['--echo', 'false'])
            args.extend(['--interactive', 'false'])
            if host is not None:
                args.extend(['--host', host])
            if port is not None:
                args.extend(['--port', port])
            if user is not None:
                args.extend(['--user', user])
            pwd_id = None
            if passwords is not None:
                pwd_id = self._Asadmin__create_pwd_id()
                any(self._Asadmin__ssh_session.execute(self._Asadmin__das_machine.create_password_file_cmd(pwd_id, passwords)))
                args.extend([
                 '--passwordfile',
                 self._Asadmin__das_machine.password_file_path(pwd_id)])
            args.append(cmd)
            if params is not None:
                args.extend(params)
            yield from self._Asadmin__ssh_session.execute(self._Asadmin__das_machine.asadmin_cmd(args))
        finally:
            if pwd_id is not None:
                any(self._Asadmin__ssh_session.execute(self._Asadmin__das_machine.delete_password_file_cmd(pwd_id)))

    def list_domains(self):
        params = []
        params.append('--long')
        params.extend(['--header', 'false'])
        for line in self._Asadmin__run(cmd='list-domains', params=params):
            values = line.split()
            yield {'name': values[0], 
             'admin-host': values[1], 
             'admin-port': values[2], 
             'running': values[3] == 'true', 
             'restart-required': values[4] == 'true'}

    def create_domain(self, name, admin_user, admin_password):
        params = []
        params.extend(['--usemasterpassword', 'true'])
        params.extend(['--savemasterpassword', 'true'])
        params.append(name)
        any(self._Asadmin__run(cmd='create-domain', params=params, host=self._Asadmin__das_machine.host, user=admin_user, passwords={'AS_ADMIN_MASTERPASSWORD': self._Asadmin__master_password, 
         'AS_ADMIN_PASSWORD': admin_password}))

    def enable_secure_admin(self, admin_port, admin_user, admin_password):
        any(self._Asadmin__run(cmd='enable-secure-admin', host=self._Asadmin__das_machine.host, port=admin_port, user=admin_user, passwords={'AS_ADMIN_PASSWORD': admin_password}))

    def set_admin_listener_host(self, admin_port, admin_user, admin_password):
        params = []
        params.append('configs.config.server-config.network-config.network-listeners.network-listener.admin-listener.address={}'.format(self._Asadmin__das_machine.host))
        any(self._Asadmin__run(cmd='set', params=params, host=self._Asadmin__das_machine.host, port=admin_port, user=admin_user, passwords={'AS_ADMIN_PASSWORD': admin_password}))

    def start_domain(self, name):
        params = []
        params.append(name)
        any(self._Asadmin__run(cmd='start-domain', params=params, passwords={'AS_ADMIN_MASTERPASSWORD': self._Asadmin__master_password}))

    def stop_domain(self, name):
        params = []
        params.append(name)
        any(self._Asadmin__run(cmd='stop-domain', params=params, passwords={'AS_ADMIN_MASTERPASSWORD': self._Asadmin__master_password}))