# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/caviar/provider/machinery/docker/server.py
# Compiled at: 2017-10-25 18:02:55
# Size of source mod 2**32: 2460 bytes
import caviar, caviar.provider.machinery.docker.machine
DOMAIN_DIR = '/var/glassfish/domains'
NODE_DIR = '/var/glassfish/nodes'

class ServerMachine(caviar.provider.machinery.docker.machine.Machine):

    def __init__(self, client, container_id, appserver_user, appserver_public_key_path):
        super().__init__(client, container_id)
        self._ServerMachine__DISABLE_PUBLIC_KEY_CHECK_PARAM = '-oStrictHostKeyChecking=no'
        self._ServerMachine__appserver_user = appserver_user
        self._ServerMachine__appserver_public_key_path = appserver_public_key_path

    @property
    def appserver_user(self):
        return self._ServerMachine__appserver_user

    @property
    def appserver_public_key_path(self):
        return self._ServerMachine__appserver_public_key_path

    def password_file_path(self, pwd_id):
        return '/tmp/passwords-{}.txt'.format(pwd_id)

    def asadmin_cmd(self, asadmin_args):
        args = []
        args.append('$HOME/bin/asadmin')
        args.extend(asadmin_args)
        return ' '.join(args)

    def create_password_file_cmd(self, pwd_id, passwords):
        return "echo '{}' >> {}".format('\n'.join(['{}={}'.format(key, value) for key, value in passwords.items()]), self.password_file_path(pwd_id))

    def delete_password_file_cmd(self, pwd_id):
        return 'rm {}'.format(self.password_file_path(pwd_id))

    def install_master_password_cmd(self, domain_name, node_name, node_host):
        mkdir_cmd = "ssh {} {}@{} 'mkdir -p {}/{}/agent' 2> /dev/null".format(self._ServerMachine__DISABLE_PUBLIC_KEY_CHECK_PARAM, self.appserver_user, node_host, NODE_DIR, node_name)
        copy_cmd = 'scp {} {}/{}/config/master-password {}@{}:{}/{}/agent 2> /dev/null'.format(self._ServerMachine__DISABLE_PUBLIC_KEY_CHECK_PARAM, DOMAIN_DIR, domain_name, self.appserver_user, node_host, NODE_DIR, node_name)
        return ' && '.join([mkdir_cmd, copy_cmd])