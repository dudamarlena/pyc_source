# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/operators/docker_operator.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 11089 bytes
import json
from airflow.hooks.docker_hook import DockerHook
from airflow.exceptions import AirflowException
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
from airflow.utils.file import TemporaryDirectory
from docker import APIClient, tls
import ast

class DockerOperator(BaseOperator):
    """DockerOperator"""
    template_fields = ('command', 'environment')
    template_ext = ('.sh', '.bash')

    @apply_defaults
    def __init__(self, image, api_version=None, command=None, cpus=1.0, docker_url='unix://var/run/docker.sock', environment=None, force_pull=False, mem_limit=None, host_tmp_dir=None, network_mode=None, tls_ca_cert=None, tls_client_cert=None, tls_client_key=None, tls_hostname=None, tls_ssl_version=None, tmp_dir='/tmp/airflow', user=None, volumes=None, working_dir=None, xcom_push=False, xcom_all=False, docker_conn_id=None, dns=None, dns_search=None, auto_remove=False, shm_size=None, *args, **kwargs):
        (super(DockerOperator, self).__init__)(*args, **kwargs)
        self.api_version = api_version
        self.auto_remove = auto_remove
        self.command = command
        self.cpus = cpus
        self.dns = dns
        self.dns_search = dns_search
        self.docker_url = docker_url
        self.environment = environment or {}
        self.force_pull = force_pull
        self.image = image
        self.mem_limit = mem_limit
        self.host_tmp_dir = host_tmp_dir
        self.network_mode = network_mode
        self.tls_ca_cert = tls_ca_cert
        self.tls_client_cert = tls_client_cert
        self.tls_client_key = tls_client_key
        self.tls_hostname = tls_hostname
        self.tls_ssl_version = tls_ssl_version
        self.tmp_dir = tmp_dir
        self.user = user
        self.volumes = volumes or []
        self.working_dir = working_dir
        self.xcom_push_flag = xcom_push
        self.xcom_all = xcom_all
        self.docker_conn_id = docker_conn_id
        self.shm_size = shm_size
        self.cli = None
        self.container = None

    def get_hook(self):
        return DockerHook(docker_conn_id=(self.docker_conn_id),
          base_url=(self.docker_url),
          version=(self.api_version),
          tls=(self._DockerOperator__get_tls_config()))

    def execute(self, context):
        self.log.info('Starting docker container from image %s', self.image)
        tls_config = self._DockerOperator__get_tls_config()
        if self.docker_conn_id:
            self.cli = self.get_hook().get_conn()
        else:
            self.cli = APIClient(base_url=(self.docker_url),
              version=(self.api_version),
              tls=tls_config)
        if self.force_pull or len(self.cli.images(name=(self.image))) == 0:
            self.log.info('Pulling docker image %s', self.image)
            for l in self.cli.pull((self.image), stream=True):
                output = json.loads(l.decode('utf-8').strip())
                if 'status' in output:
                    self.log.info('%s', output['status'])

        with TemporaryDirectory(prefix='airflowtmp', dir=(self.host_tmp_dir)) as (host_tmp_dir):
            self.environment['AIRFLOW_TMP_DIR'] = self.tmp_dir
            self.volumes.append('{0}:{1}'.format(host_tmp_dir, self.tmp_dir))
            self.container = self.cli.create_container(command=(self.get_command()),
              environment=(self.environment),
              host_config=self.cli.create_host_config(auto_remove=(self.auto_remove),
              binds=(self.volumes),
              network_mode=(self.network_mode),
              shm_size=(self.shm_size),
              dns=(self.dns),
              dns_search=(self.dns_search),
              cpu_shares=(int(round(self.cpus * 1024))),
              mem_limit=(self.mem_limit)),
              image=(self.image),
              user=(self.user),
              working_dir=(self.working_dir))
            self.cli.start(self.container['Id'])
            line = ''
            for line in self.cli.attach(container=(self.container['Id']), stdout=True,
              stderr=True,
              stream=True):
                line = line.strip()
                if hasattr(line, 'decode'):
                    line = line.decode('utf-8')
                self.log.info(line)

            result = self.cli.wait(self.container['Id'])
            if result['StatusCode'] != 0:
                raise AirflowException('docker container failed: ' + repr(result))
            if self.xcom_push_flag:
                if self.xcom_all:
                    return self.cli.logs(container=(self.container['Id']))
                else:
                    return str(line)

    def get_command(self):
        if isinstance(self.command, str):
            if self.command.strip().find('[') == 0:
                commands = ast.literal_eval(self.command)
        else:
            commands = self.command
        return commands

    def on_kill(self):
        if self.cli is not None:
            self.log.info('Stopping docker container')
            self.cli.stop(self.container['Id'])

    def __get_tls_config(self):
        tls_config = None
        if self.tls_ca_cert:
            if self.tls_client_cert:
                if self.tls_client_key:
                    tls_config = tls.TLSConfig(ca_cert=(self.tls_ca_cert),
                      client_cert=(
                     self.tls_client_cert, self.tls_client_key),
                      verify=True,
                      ssl_version=(self.tls_ssl_version),
                      assert_hostname=(self.tls_hostname))
                    self.docker_url = self.docker_url.replace('tcp://', 'https://')
        return tls_config