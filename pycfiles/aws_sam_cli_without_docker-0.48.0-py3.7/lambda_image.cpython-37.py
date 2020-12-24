# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/samcli/local/docker/lambda_image.py
# Compiled at: 2020-03-21 12:32:11
# Size of source mod 2**32: 7555 bytes
"""
Generates a Docker Image to be used for invoking a function locally
"""
import uuid, logging, hashlib
from enum import Enum
from pathlib import Path
import docker
from samcli.commands.local.cli_common.user_exceptions import ImageBuildException
from samcli.lib.utils.tar import create_tarball
LOG = logging.getLogger(__name__)

class Runtime(Enum):
    nodejs = 'nodejs'
    nodejs43 = 'nodejs4.3'
    nodejs610 = 'nodejs6.10'
    nodejs810 = 'nodejs8.10'
    nodejs10x = 'nodejs10.x'
    nodejs12x = 'nodejs12.x'
    python27 = 'python2.7'
    python36 = 'python3.6'
    python37 = 'python3.7'
    python38 = 'python3.8'
    ruby25 = 'ruby2.5'
    ruby27 = 'ruby2.7'
    java8 = 'java8'
    java11 = 'java11'
    go1x = 'go1.x'
    dotnetcore20 = 'dotnetcore2.0'
    dotnetcore21 = 'dotnetcore2.1'
    provided = 'provided'

    @classmethod
    def has_value(cls, value):
        """
        Checks if the enum has this value

        :param string value: Value to check
        :return bool: True, if enum has the value
        """
        return any((value == item.value for item in cls))


class LambdaImage:
    _LAYERS_DIR = '/opt'
    _DOCKER_LAMBDA_REPO_NAME = 'lambci/lambda'
    _SAM_CLI_REPO_NAME = 'samcli/lambda'

    def __init__(self, layer_downloader, skip_pull_image, force_image_build, docker_client=None):
        """

        Parameters
        ----------
        layer_downloader samcli.local.layers.layer_downloader.LayerDownloader
            LayerDownloader to download layers locally
        skip_pull_image bool
            True if the image should not be pulled from DockerHub
        force_image_build bool
            True to download the layer and rebuild the image even if it exists already on the system
        docker_client docker.DockerClient
            Optional docker client object
        """
        self.layer_downloader = layer_downloader
        self.skip_pull_image = skip_pull_image
        self.force_image_build = force_image_build
        self.docker_client = docker_client or docker.from_env()

    def build(self, runtime, layers):
        """
        Build the image if one is not already on the system that matches the runtime and layers

        Parameters
        ----------
        runtime str
            Name of the Lambda runtime
        layers list(samcli.commands.local.lib.provider.Layer)
            List of layers

        Returns
        -------
        str
            The image to be used (REPOSITORY:TAG)
        """
        base_image = '{}:{}'.format(self._DOCKER_LAMBDA_REPO_NAME, runtime)
        if not layers:
            LOG.debug('Skipping building an image since no layers were defined')
            return base_image
        downloaded_layers = self.layer_downloader.download_all(layers, self.force_image_build)
        docker_image_version = self._generate_docker_image_version(downloaded_layers, runtime)
        image_tag = '{}:{}'.format(self._SAM_CLI_REPO_NAME, docker_image_version)
        image_not_found = False
        try:
            self.docker_client.images.get(image_tag)
        except docker.errors.ImageNotFound:
            LOG.info('Image was not found.')
            image_not_found = True

        if self.force_image_build or image_not_found or any((layer.is_defined_within_template for layer in downloaded_layers)):
            LOG.info('Building image...')
            self._build_image(base_image, image_tag, downloaded_layers)
        return image_tag

    @staticmethod
    def _generate_docker_image_version(layers, runtime):
        """
        Generate the Docker TAG that will be used to create the image

        Parameters
        ----------
        layers list(samcli.commands.local.lib.provider.Layer)
            List of the layers

        runtime str
            Runtime of the image to create

        Returns
        -------
        str
            String representing the TAG to be attached to the image
        """
        return runtime + '-' + hashlib.sha256('-'.join([layer.name for layer in layers]).encode('utf-8')).hexdigest()[0:25]

    def _build_image(self, base_image, docker_tag, layers):
        """
        Builds the image

        Parameters
        ----------
        base_image str
            Base Image to use for the new image
        docker_tag
            Docker tag (REPOSITORY:TAG) to use when building the image
        layers list(samcli.commands.local.lib.provider.Layer)
            List of Layers to be use to mount in the image

        Returns
        -------
        None

        Raises
        ------
        samcli.commands.local.cli_common.user_exceptions.ImageBuildException
            When docker fails to build the image
        """
        dockerfile_content = self._generate_dockerfile(base_image, layers)
        dockerfile_name = 'dockerfile_' + str(uuid.uuid4())
        full_dockerfile_path = Path(self.layer_downloader.layer_cache, dockerfile_name)
        try:
            with open(str(full_dockerfile_path), 'w') as (dockerfile):
                dockerfile.write(dockerfile_content)
            tar_paths = {str(full_dockerfile_path): 'Dockerfile'}
            for layer in layers:
                tar_paths[layer.codeuri] = '/' + layer.name

            with create_tarball(tar_paths) as (tarballfile):
                try:
                    self.docker_client.images.build(fileobj=tarballfile,
                      custom_context=True,
                      rm=True,
                      tag=docker_tag,
                      pull=(not self.skip_pull_image))
                except (docker.errors.BuildError, docker.errors.APIError):
                    LOG.exception('Failed to build Docker Image')
                    raise ImageBuildException('Building Image failed.')

        finally:
            if full_dockerfile_path.exists():
                full_dockerfile_path.unlink()

    @staticmethod
    def _generate_dockerfile(base_image, layers):
        """
        Generate the Dockerfile contents

        A generated Dockerfile will look like the following:
        ```
        FROM lambci/lambda:python3.6

        ADD --chown=sbx_user1051:495 layer1 /opt
        ADD --chown=sbx_user1051:495 layer2 /opt
        ```

        Parameters
        ----------
        base_image str
            Base Image to use for the new image
        layers list(samcli.commands.local.lib.provider.Layer)
            List of Layers to be use to mount in the image

        Returns
        -------
        str
            String representing the Dockerfile contents for the image

        """
        dockerfile_content = 'FROM {}\n'.format(base_image)
        for layer in layers:
            dockerfile_content = dockerfile_content + 'ADD --chown=sbx_user1051:495 {} {}\n'.format(layer.name, LambdaImage._LAYERS_DIR)

        return dockerfile_content