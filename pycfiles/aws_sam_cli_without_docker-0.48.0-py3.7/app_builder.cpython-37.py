# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/samcli/lib/build/app_builder.py
# Compiled at: 2020-03-21 12:32:11
# Size of source mod 2**32: 13791 bytes
"""
Builds the application
"""
import os, io, json, logging, pathlib, docker
from aws_lambda_builders.builder import LambdaBuilder
from aws_lambda_builders.exceptions import LambdaBuilderError
from aws_lambda_builders import RPC_PROTOCOL_VERSION as lambda_builders_protocol_version
import samcli.lib.utils.osutils as osutils
from samcli.local.docker.lambda_build_container import LambdaBuildContainer
from .workflow_config import get_workflow_config, supports_build_in_container
LOG = logging.getLogger(__name__)

class UnsupportedBuilderLibraryVersionError(Exception):

    def __init__(self, container_name, error_msg):
        msg = "You are running an outdated version of Docker container '{container_name}' that is not compatible withthis version of SAM CLI. Please upgrade to continue to continue with build. Reason: '{error_msg}'"
        Exception.__init__(self, msg.format(container_name=container_name, error_msg=error_msg))


class ContainerBuildNotSupported(Exception):
    pass


class BuildError(Exception):
    pass


class ApplicationBuilder:
    __doc__ = '\n    Class to build an entire application. Currently, this class builds Lambda functions only, but there is nothing that\n    is stopping this class from supporting other resource types. Building in context of Lambda functions refer to\n    converting source code into artifacts that can be run on AWS Lambda\n    '

    def __init__(self, functions_to_build, build_dir, base_dir, manifest_path_override=None, container_manager=None, parallel=False, mode=None):
        """
        Initialize the class

        Parameters
        ----------
        functions_to_build: Iterator
            Iterator that can vend out functions available in the SAM template

        build_dir : str
            Path to the directory where we will be storing built artifacts

        base_dir : str
            Path to a folder. Use this folder as the root to resolve relative source code paths against

        container_manager : samcli.local.docker.manager.ContainerManager
            Optional. If provided, we will attempt to build inside a Docker Container

        parallel : bool
            Optional. Set to True to build each function in parallel to improve performance

        mode : str
            Optional, name of the build mode to use ex: 'debug'
        """
        self._functions_to_build = functions_to_build
        self._build_dir = build_dir
        self._base_dir = base_dir
        self._manifest_path_override = manifest_path_override
        self._container_manager = container_manager
        self._parallel = parallel
        self._mode = mode

    def build(self):
        """
        Build the entire application

        Returns
        -------
        dict
            Returns the path to where each resource was built as a map of resource's LogicalId to the path string
        """
        result = {}
        for lambda_function in self._functions_to_build:
            LOG.info("Building resource '%s'", lambda_function.name)
            result[lambda_function.name] = self._build_function(lambda_function.name, lambda_function.codeuri, lambda_function.runtime, lambda_function.handler)

        return result

    def update_template(self, template_dict, original_template_path, built_artifacts):
        """
        Given the path to built artifacts, update the template to point appropriate resource CodeUris to the artifacts
        folder

        Parameters
        ----------
        template_dict
        original_template_path : str
            Path where the template file will be written to

        built_artifacts : dict
            Map of LogicalId of a resource to the path where the the built artifacts for this resource lives

        Returns
        -------
        dict
            Updated template
        """
        original_dir = os.path.dirname(original_template_path)
        for logical_id, resource in template_dict.get('Resources', {}).items():
            if logical_id not in built_artifacts:
                continue
            artifact_relative_path = os.path.relpath(built_artifacts[logical_id], original_dir)
            resource_type = resource.get('Type')
            properties = resource.setdefault('Properties', {})
            if resource_type == 'AWS::Serverless::Function':
                properties['CodeUri'] = artifact_relative_path
            if resource_type == 'AWS::Lambda::Function':
                properties['Code'] = artifact_relative_path

        return template_dict

    def _build_function(self, function_name, codeuri, runtime, handler):
        """
        Given the function information, this method will build the Lambda function. Depending on the configuration
        it will either build the function in process or by spinning up a Docker container.

        Parameters
        ----------
        function_name : str
            Name or LogicalId of the function

        codeuri : str
            Path to where the code lives

        runtime : str
            AWS Lambda function runtime

        Returns
        -------
        str
            Path to the location where built artifacts are available
        """
        code_dir = str(pathlib.Path(self._base_dir, codeuri).resolve())
        config = get_workflow_config(runtime, code_dir, self._base_dir)
        artifacts_dir = str(pathlib.Path(self._build_dir, function_name))
        with osutils.mkdir_temp() as (scratch_dir):
            manifest_path = self._manifest_path_override or os.path.join(code_dir, config.manifest_name)
            build_method = self._build_function_in_process
            if self._container_manager:
                build_method = self._build_function_on_container
            options = ApplicationBuilder._get_build_options(config.language, handler)
            return build_method(config, code_dir, artifacts_dir, scratch_dir, manifest_path, runtime, options)

    @staticmethod
    def _get_build_options(language, handler):
        """
        Parameters
        ----------
        language str
            Language of the runtime
        handler str
            Handler value of the Lambda Function Resource
        Returns
        -------
        dict
            Dictionary that represents the options to pass to the builder workflow or None if options are not needed
        """
        if language == 'go':
            return {'artifact_executable_name': handler}

    def _build_function_in_process(self, config, source_dir, artifacts_dir, scratch_dir, manifest_path, runtime, options):
        builder = LambdaBuilder(language=(config.language), dependency_manager=(config.dependency_manager),
          application_framework=(config.application_framework))
        try:
            builder.build(source_dir, artifacts_dir,
              scratch_dir,
              manifest_path,
              runtime=runtime,
              executable_search_paths=(config.executable_search_paths),
              mode=(self._mode),
              options=options)
        except LambdaBuilderError as ex:
            try:
                raise BuildError(str(ex))
            finally:
                ex = None
                del ex

        return artifacts_dir

    def _build_function_on_container(self, config, source_dir, artifacts_dir, scratch_dir, manifest_path, runtime, options):
        if not self._container_manager.is_docker_reachable:
            raise BuildError('Docker is unreachable. Docker needs to be running to build inside a container.')
        container_build_supported, reason = supports_build_in_container(config)
        if not container_build_supported:
            raise ContainerBuildNotSupported(reason)
        log_level = LOG.getEffectiveLevel()
        container = LambdaBuildContainer(lambda_builders_protocol_version, (config.language),
          (config.dependency_manager),
          (config.application_framework),
          source_dir,
          manifest_path,
          runtime,
          log_level=log_level,
          optimizations=None,
          options=options,
          executable_search_paths=(config.executable_search_paths),
          mode=(self._mode))
        try:
            try:
                self._container_manager.run(container)
            except docker.errors.APIError as ex:
                try:
                    if 'executable file not found in $PATH' in str(ex):
                        raise UnsupportedBuilderLibraryVersionError(container.image, '{} executable not found in container'.format(container.executable_name))
                finally:
                    ex = None
                    del ex

            stdout_stream = io.BytesIO()
            stderr_stream = osutils.stderr()
            container.wait_for_logs(stdout=stdout_stream, stderr=stderr_stream)
            stdout_data = stdout_stream.getvalue().decode('utf-8')
            LOG.debug('Build inside container returned response %s', stdout_data)
            response = self._parse_builder_response(stdout_data, container.image)
            LOG.debug('Build inside container was successful. Copying artifacts from container to host')
            result_dir_in_container = response['result']['artifacts_dir'] + '/.'
            container.copy(result_dir_in_container, artifacts_dir)
        finally:
            self._container_manager.stop(container)

        LOG.debug('Build inside container succeeded')
        return artifacts_dir

    @staticmethod
    def _parse_builder_response(stdout_data, image_name):
        try:
            response = json.loads(stdout_data)
        except Exception:
            LOG.debug('Builder crashed')
            raise

        if 'error' in response:
            error = response.get('error', {})
            err_code = error.get('code')
            msg = error.get('message')
            if 400 <= err_code < 500:
                raise BuildError(msg)
            if err_code == 505:
                raise UnsupportedBuilderLibraryVersionError(image_name, msg)
            if err_code == -32601:
                LOG.debug('Builder library does not support the supplied method')
                raise UnsupportedBuilderLibraryVersionError(image_name, msg)
            LOG.debug('Builder crashed')
            raise ValueError(msg)
        return response