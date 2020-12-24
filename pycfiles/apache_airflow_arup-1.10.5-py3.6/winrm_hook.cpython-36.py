# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/hooks/winrm_hook.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 10941 bytes
import getpass
from winrm.protocol import Protocol
from airflow.exceptions import AirflowException
from airflow.hooks.base_hook import BaseHook

class WinRMHook(BaseHook):
    __doc__ = "\n    Hook for winrm remote execution using pywinrm.\n\n    :seealso: https://github.com/diyan/pywinrm/blob/master/winrm/protocol.py\n\n    :param ssh_conn_id: connection id from airflow Connections from where\n        all the required parameters can be fetched like username and password.\n        Thought the priority is given to the param passed during init\n    :type ssh_conn_id: str\n    :param endpoint: When not set, endpoint will be constructed like this:\n        'http://{remote_host}:{remote_port}/wsman'\n    :type endpoint: str\n    :param remote_host: Remote host to connect to. Ignored if `endpoint` is set.\n    :type remote_host: str\n    :param remote_port: Remote port to connect to. Ignored if `endpoint` is set.\n    :type remote_port: int\n    :param transport: transport type, one of 'plaintext' (default), 'kerberos', 'ssl', 'ntlm', 'credssp'\n    :type transport: str\n    :param username: username to connect to the remote_host\n    :type username: str\n    :param password: password of the username to connect to the remote_host\n    :type password: str\n    :param service: the service name, default is HTTP\n    :type service: str\n    :param keytab: the path to a keytab file if you are using one\n    :type keytab: str\n    :param ca_trust_path: Certification Authority trust path\n    :type ca_trust_path: str\n    :param cert_pem: client authentication certificate file path in PEM format\n    :type cert_pem: str\n    :param cert_key_pem: client authentication certificate key file path in PEM format\n    :type cert_key_pem: str\n    :param server_cert_validation: whether server certificate should be validated on\n        Python versions that support it; one of 'validate' (default), 'ignore'\n    :type server_cert_validation: str\n    :param kerberos_delegation: if True, TGT is sent to target server to\n        allow multiple hops\n    :type kerberos_delegation: bool\n    :param read_timeout_sec: maximum seconds to wait before an HTTP connect/read times out (default 30).\n        This value should be slightly higher than operation_timeout_sec,\n        as the server can block *at least* that long.\n    :type read_timeout_sec: int\n    :param operation_timeout_sec: maximum allowed time in seconds for any single wsman\n        HTTP operation (default 20). Note that operation timeouts while receiving output\n        (the only wsman operation that should take any significant time,\n        and where these timeouts are expected) will be silently retried indefinitely.\n    :type operation_timeout_sec: int\n    :param kerberos_hostname_override: the hostname to use for the kerberos exchange\n        (defaults to the hostname in the endpoint URL)\n    :type kerberos_hostname_override: str\n    :param message_encryption: Will encrypt the WinRM messages if set\n        and the transport auth supports message encryption. (Default 'auto')\n    :type message_encryption: str\n    :param credssp_disable_tlsv1_2: Whether to disable TLSv1.2 support and work with older\n        protocols like TLSv1.0, default is False\n    :type credssp_disable_tlsv1_2: bool\n    :param send_cbt: Will send the channel bindings over a HTTPS channel (Default: True)\n    :type send_cbt: bool\n    "

    def __init__(self, ssh_conn_id=None, endpoint=None, remote_host=None, remote_port=5985, transport='plaintext', username=None, password=None, service='HTTP', keytab=None, ca_trust_path=None, cert_pem=None, cert_key_pem=None, server_cert_validation='validate', kerberos_delegation=False, read_timeout_sec=30, operation_timeout_sec=20, kerberos_hostname_override=None, message_encryption='auto', credssp_disable_tlsv1_2=False, send_cbt=True):
        super(WinRMHook, self).__init__(ssh_conn_id)
        self.ssh_conn_id = ssh_conn_id
        self.endpoint = endpoint
        self.remote_host = remote_host
        self.remote_port = remote_port
        self.transport = transport
        self.username = username
        self.password = password
        self.service = service
        self.keytab = keytab
        self.ca_trust_path = ca_trust_path
        self.cert_pem = cert_pem
        self.cert_key_pem = cert_key_pem
        self.server_cert_validation = server_cert_validation
        self.kerberos_delegation = kerberos_delegation
        self.read_timeout_sec = read_timeout_sec
        self.operation_timeout_sec = operation_timeout_sec
        self.kerberos_hostname_override = kerberos_hostname_override
        self.message_encryption = message_encryption
        self.credssp_disable_tlsv1_2 = credssp_disable_tlsv1_2
        self.send_cbt = send_cbt
        self.client = None
        self.winrm_protocol = None

    def get_conn(self):
        if self.client:
            return self.client
        else:
            self.log.debug('Creating WinRM client for conn_id: %s', self.ssh_conn_id)
            if self.ssh_conn_id is not None:
                conn = self.get_connection(self.ssh_conn_id)
                if self.username is None:
                    self.username = conn.login
                if self.password is None:
                    self.password = conn.password
                if self.remote_host is None:
                    self.remote_host = conn.host
                if conn.extra is not None:
                    extra_options = conn.extra_dejson
                    if 'endpoint' in extra_options:
                        self.endpoint = str(extra_options['endpoint'])
                    if 'remote_port' in extra_options:
                        self.remote_port = int(extra_options['remote_port'])
                    if 'transport' in extra_options:
                        self.transport = str(extra_options['transport'])
                    if 'service' in extra_options:
                        self.service = str(extra_options['service'])
                    if 'keytab' in extra_options:
                        self.keytab = str(extra_options['keytab'])
                    if 'ca_trust_path' in extra_options:
                        self.ca_trust_path = str(extra_options['ca_trust_path'])
                    if 'cert_pem' in extra_options:
                        self.cert_pem = str(extra_options['cert_pem'])
                    if 'cert_key_pem' in extra_options:
                        self.cert_key_pem = str(extra_options['cert_key_pem'])
                    if 'server_cert_validation' in extra_options:
                        self.server_cert_validation = str(extra_options['server_cert_validation'])
                    if 'kerberos_delegation' in extra_options:
                        self.kerberos_delegation = str(extra_options['kerberos_delegation']).lower() == 'true'
                    if 'read_timeout_sec' in extra_options:
                        self.read_timeout_sec = int(extra_options['read_timeout_sec'])
                    if 'operation_timeout_sec' in extra_options:
                        self.operation_timeout_sec = int(extra_options['operation_timeout_sec'])
                    if 'kerberos_hostname_override' in extra_options:
                        self.kerberos_hostname_override = str(extra_options['kerberos_hostname_override'])
                    if 'message_encryption' in extra_options:
                        self.message_encryption = str(extra_options['message_encryption'])
                    if 'credssp_disable_tlsv1_2' in extra_options:
                        self.credssp_disable_tlsv1_2 = str(extra_options['credssp_disable_tlsv1_2']).lower() == 'true'
                    if 'send_cbt' in extra_options:
                        self.send_cbt = str(extra_options['send_cbt']).lower() == 'true'
            if not self.remote_host:
                raise AirflowException('Missing required param: remote_host')
            if not self.username:
                self.log.debug("username to WinRM to host: %s is not specified for connection id %s. Using system's default provided by getpass.getuser()", self.remote_host, self.ssh_conn_id)
                self.username = getpass.getuser()
            if not self.endpoint:
                self.endpoint = 'http://{0}:{1}/wsman'.format(self.remote_host, self.remote_port)
            try:
                if self.password:
                    if self.password.strip():
                        self.winrm_protocol = Protocol(endpoint=(self.endpoint),
                          transport=(self.transport),
                          username=(self.username),
                          password=(self.password),
                          service=(self.service),
                          keytab=(self.keytab),
                          ca_trust_path=(self.ca_trust_path),
                          cert_pem=(self.cert_pem),
                          cert_key_pem=(self.cert_key_pem),
                          server_cert_validation=(self.server_cert_validation),
                          kerberos_delegation=(self.kerberos_delegation),
                          read_timeout_sec=(self.read_timeout_sec),
                          operation_timeout_sec=(self.operation_timeout_sec),
                          kerberos_hostname_override=(self.kerberos_hostname_override),
                          message_encryption=(self.message_encryption),
                          credssp_disable_tlsv1_2=(self.credssp_disable_tlsv1_2),
                          send_cbt=(self.send_cbt))
                self.log.info('Establishing WinRM connection to host: %s', self.remote_host)
                self.client = self.winrm_protocol.open_shell()
            except Exception as error:
                error_msg = 'Error connecting to host: {0}, error: {1}'.format(self.remote_host, error)
                self.log.error(error_msg)
                raise AirflowException(error_msg)

            return self.client