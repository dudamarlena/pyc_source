# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/samcli/local/docker/manager.py
# Compiled at: 2020-03-21 16:24:37
# Size of source mod 2**32: 5693 bytes
"""
Provides classes that interface with Docker to create, execute and manage containers.
"""
import logging, sys, docker, requests
from samcli.lib.utils.stream_writer import StreamWriter
LOG = logging.getLogger(__name__)

class ContainerManager:
    __doc__ = "\n    This class knows how to interface with Docker to create, execute and manage the container's life cycle. It can\n    run multiple containers in parallel, and also comes with the ability to reuse existing containers in order to\n    serve requests faster. It is also thread-safe.\n    "

    def __init__(self, docker_network_id=None, docker_client=None, skip_pull_image=False):
        """
        Instantiate the container manager

        :param docker_network_id: Optional Docker network to run this container in.
        :param docker_client: Optional docker client object
        :param bool skip_pull_image: Should we pull new Docker container image?
        """
        self.skip_pull_image = skip_pull_image
        self.docker_network_id = docker_network_id
        self.docker_client = docker_client or docker.from_env()

    @property
    def is_docker_reachable(self):
        """
        Checks if Docker daemon is running. This is required for us to invoke the function locally

        Returns
        -------
        bool
            True, if Docker is available, False otherwise
        """
        return True

    def run(self, container, input_data=None, warm=False):
        """
        Create and run a Docker container based on the given configuration.

        :param samcli.local.docker.container.Container container: Container to create and run
        :param input_data: Optional. Input data sent to the container through container's stdin.
        :param bool warm: Indicates if an existing container can be reused. Defaults False ie. a new container will
            be created for every request.
        :raises DockerImagePullFailedException: If the Docker image was not available in the server
        """
        pass

    def stop(self, container):
        """
        Stop and delete the container

        :param samcli.local.docker.container.Container container: Container to stop
        """
        pass

    def pull_image(self, image_name, stream=None):
        """
        Ask Docker to pull the container image with given name.

        Parameters
        ----------
        image_name str
            Name of the image
        stream samcli.lib.utils.stream_writer.StreamWriter
            Optional stream writer to output to. Defaults to stderr

        Raises
        ------
        DockerImagePullFailedException
            If the Docker image was not available in the server
        """
        stream_writer = stream or StreamWriter(sys.stderr)
        try:
            result_itr = self.docker_client.api.pull(image_name, stream=True, decode=True)
        except docker.errors.APIError as ex:
            try:
                LOG.debug('Failed to download image with name %s', image_name)
                raise DockerImagePullFailedException(str(ex))
            finally:
                ex = None
                del ex

        stream_writer.write('\nFetching {} Docker container image...'.format(image_name))
        for _ in result_itr:
            stream_writer.write('.')
            stream_writer.flush()

        stream_writer.write('\n')

    def has_image(self, image_name):
        """
        Is the container image with given name available?

        :param string image_name: Name of the image
        :return bool: True, if image is available. False, otherwise
        """
        try:
            self.docker_client.images.get(image_name)
            return True
        except docker.errors.ImageNotFound:
            return False


class DockerImagePullFailedException(Exception):
    pass