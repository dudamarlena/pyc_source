# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hachterberg/dev/fastr/fastr/fastr/resources/plugins/targetplugins/dockertarget.py
# Compiled at: 2019-06-04 03:32:43
# Size of source mod 2**32: 6233 bytes
"""
The module containing the classes describing the targets.
"""
import os, time, threading
from typing import List
import isodate, requests, fastr
from fastr import exceptions
from fastr.core.target import Target, ProcessUsageCollection, TargetResult
try:
    import docker
    DOCKER_AVAILABLE = True
except ImportError:
    docker = None
    DOCKER_AVAILABLE = False

class DockerTarget(Target):
    __doc__ = '\n    A tool target that is located in a Docker images. Can be run using\n    docker-py. A docker target only need two variables: the binary to call within the\n    docker container, and the docker container to use.\n\n\n    .. code-block:: json\n\n        {\n          "arch": "*",\n          "os": "*",\n          "binary": "bin/test.py",\n          "docker_image": "fastr/test"\n        }\n\n    .. code-block:: xml\n\n        <target os="*" arch="*" binary="bin/test.py" docker_image="fastr/test">\n\n    '

    def __init__(self, binary, docker_image):
        """
        Define a new docker target.

        :param str docker_image: Docker image to use
        """
        if not DOCKER_AVAILABLE:
            raise exceptions.FastrOptionalModuleNotAvailableError('Target cannot be used, module "docker" unavailable')
        self.binary = binary
        self._docker_image = docker_image
        self.docker_api = 'unix://var/run/docker.sock'
        self._docker_client = docker.DockerClient(base_url=(self.docker_api), version='auto')
        self._container = None
        self._running_container = False

    def __enter__(self):
        super(DockerTarget, self).__enter__()

    def __exit__(self, exc_type, exc_value, traceback):
        self._container = None

    @property
    def container(self):
        return self._container

    def run_command(self, command: List) -> TargetResult:
        mounts = list(fastr.config.mounts.values())
        fastr.log.info('DOCKER MOUNTS: {}'.format(mounts))
        binds = {x:{'bind':x,  'mode':'ro'} for x in mounts if os.path.exists(x) if os.path.exists(x)}
        binds[fastr.config.mounts['tmp']]['mode'] = 'rw'
        fastr.log.info('Docker binds: {}'.format(binds))
        fastr.log.info('Creating Docker container')
        container = self._docker_client.containers.run(image=(self._docker_image),
          entrypoint=(command[0]),
          command=(command[1:]),
          detach=True,
          volumes=binds,
          network_disabled=False,
          user=('{}:{}'.format(os.getuid(), os.getgid())),
          working_dir=(os.path.abspath(os.curdir)),
          environment=(dict(os.environ)))
        self._running_container = True
        sysuse = ProcessUsageCollection()
        monitor_thread = threading.Thread(target=(self.monitor_docker), name='DockerMonitor',
          args=(
         container, sysuse))
        monitor_thread.daemon = True
        monitor_thread.start()
        start_time = time.time()
        fastr.log.info('Waiting for Docker container to finish')
        return_code = container.wait()
        fastr.log.info('Docker container is done')
        end_time = time.time()
        stdout = container.logs(stdout=True, stderr=False, stream=False, timestamps=False)
        stderr = container.logs(stdout=False, stderr=True, stream=False, timestamps=False)
        self._running_container = False
        if monitor_thread.is_alive():
            monitor_thread.join(2 * self._MONITOR_INTERVAL)
            if monitor_thread.is_alive():
                fastr.log.warning('Ignoring unresponsive monitor thread!')
        container.remove()
        return TargetResult(return_code=return_code,
          stdout=stdout,
          stderr=stderr,
          command=command,
          resource_usage=(list(sysuse)),
          time_elapsed=(end_time - start_time))

    def monitor_docker(self, container, resources):
        """
        Monitor a docker container and profile the cpu, memory and io use.
        Register the resource use every _MONITOR_INTERVAL seconds.

        :param ContainerCollection container: process to monitor
        :param ProcessUsageCollection resources: list to append measurements to
        """
        try:
            while self._running_container:
                stat = container.stats(stream=False, decode=True)
                timestamp = isodate.isodatetime.parse_datetime(stat['read'])
                usage = resources.usage_type(timestamp=(timestamp.isoformat()), cpu_percent=(stat['cpu_stats']['cpu_usage']['total_usage']),
                  vmem=(-1.0),
                  rmem=(stat['memory_stats'].get('rss')),
                  read_bytes=0.0,
                  write_bytes=0.0)
                resources.append(usage)
                if self._running_container:
                    time.sleep(self._MONITOR_INTERVAL)

        except requests.exceptions.ReadTimeout:
            fastr.log.info('Docker Monitor timed out')