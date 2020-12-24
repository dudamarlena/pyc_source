# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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
    __doc__ = '\n    Execute a command inside a docker container.\n\n    A temporary directory is created on the host and\n    mounted into a container to allow storing files\n    that together exceed the default disk size of 10GB in a container.\n    The path to the mounted directory can be accessed\n    via the environment variable ``AIRFLOW_TMP_DIR``.\n\n    If a login to a private registry is required prior to pulling the image, a\n    Docker connection needs to be configured in Airflow and the connection ID\n    be provided with the parameter ``docker_conn_id``.\n\n    :param image: Docker image from which to create the container.\n        If image tag is omitted, "latest" will be used.\n    :type image: str\n    :param api_version: Remote API version. Set to ``auto`` to automatically\n        detect the server\'s version.\n    :type api_version: str\n    :param auto_remove: Auto-removal of the container on daemon side when the\n        container\'s process exits.\n        The default is False.\n    :type auto_remove: bool\n    :param command: Command to be run in the container. (templated)\n    :type command: str or list\n    :param cpus: Number of CPUs to assign to the container.\n        This value gets multiplied with 1024. See\n        https://docs.docker.com/engine/reference/run/#cpu-share-constraint\n    :type cpus: float\n    :param dns: Docker custom DNS servers\n    :type dns: list[str]\n    :param dns_search: Docker custom DNS search domain\n    :type dns_search: list[str]\n    :param docker_url: URL of the host running the docker daemon.\n        Default is unix://var/run/docker.sock\n    :type docker_url: str\n    :param environment: Environment variables to set in the container. (templated)\n    :type environment: dict\n    :param force_pull: Pull the docker image on every run. Default is False.\n    :type force_pull: bool\n    :param mem_limit: Maximum amount of memory the container can use.\n        Either a float value, which represents the limit in bytes,\n        or a string like ``128m`` or ``1g``.\n    :type mem_limit: float or str\n    :param host_tmp_dir: Specify the location of the temporary directory on the host which will\n        be mapped to tmp_dir. If not provided defaults to using the standard system temp directory.\n    :type host_tmp_dir: str\n    :param network_mode: Network mode for the container.\n    :type network_mode: str\n    :param tls_ca_cert: Path to a PEM-encoded certificate authority\n        to secure the docker connection.\n    :type tls_ca_cert: str\n    :param tls_client_cert: Path to the PEM-encoded certificate\n        used to authenticate docker client.\n    :type tls_client_cert: str\n    :param tls_client_key: Path to the PEM-encoded key used to authenticate docker client.\n    :type tls_client_key: str\n    :param tls_hostname: Hostname to match against\n        the docker server certificate or False to disable the check.\n    :type tls_hostname: str or bool\n    :param tls_ssl_version: Version of SSL to use when communicating with docker daemon.\n    :type tls_ssl_version: str\n    :param tmp_dir: Mount point inside the container to\n        a temporary directory created on the host by the operator.\n        The path is also made available via the environment variable\n        ``AIRFLOW_TMP_DIR`` inside the container.\n    :type tmp_dir: str\n    :param user: Default user inside the docker container.\n    :type user: int or str\n    :param volumes: List of volumes to mount into the container, e.g.\n        ``[\'/host/path:/container/path\', \'/host/path2:/container/path2:ro\']``.\n    :type volumes: list\n    :param working_dir: Working directory to\n        set on the container (equivalent to the -w switch the docker client)\n    :type working_dir: str\n    :param xcom_push: Does the stdout will be pushed to the next step using XCom.\n        The default is False.\n    :type xcom_push: bool\n    :param xcom_all: Push all the stdout or just the last line.\n        The default is False (last line).\n    :type xcom_all: bool\n    :param docker_conn_id: ID of the Airflow connection to use\n    :type docker_conn_id: str\n    :param shm_size: Size of ``/dev/shm`` in bytes. The size must be\n        greater than 0. If omitted uses system default.\n    :type shm_size: int\n    '
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