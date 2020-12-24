# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/samcli/local/docker/lambda_build_container.py
# Compiled at: 2020-03-21 12:32:11
# Size of source mod 2**32: 8300 bytes
"""
Represents Lambda Build Containers.
"""
import json, logging, pathlib
from .container import Container
LOG = logging.getLogger(__name__)

class LambdaBuildContainer(Container):
    __doc__ = '\n    Class to manage Build containers that are capable of building AWS Lambda functions.\n    This container mounts necessary folders, issues a command to the Lambda Builder CLI,\n    and if the build was successful, copies back artifacts to the host filesystem\n    '
    _LAMBCI_IMAGE_REPO_NAME = 'lambci/lambda'
    _BUILDERS_EXECUTABLE = 'lambda-builders'

    def __init__(self, protocol_version, language, dependency_manager, application_framework, source_dir, manifest_path, runtime, optimizations=None, options=None, executable_search_paths=None, log_level=None, mode=None):
        abs_manifest_path = pathlib.Path(manifest_path).resolve()
        manifest_file_name = abs_manifest_path.name
        manifest_dir = str(abs_manifest_path.parent)
        source_dir = str(pathlib.Path(source_dir).resolve())
        container_dirs = LambdaBuildContainer._get_container_dirs(source_dir, manifest_dir)
        executable_search_paths = LambdaBuildContainer._convert_to_container_dirs(host_paths_to_convert=executable_search_paths,
          host_to_container_path_mapping={source_dir: container_dirs['source_dir'], 
         manifest_dir: container_dirs['manifest_dir']})
        request_json = self._make_request(protocol_version, language, dependency_manager, application_framework, container_dirs, manifest_file_name, runtime, optimizations, options, executable_search_paths, mode)
        image = LambdaBuildContainer._get_image(runtime)
        entry = LambdaBuildContainer._get_entrypoint(request_json)
        cmd = []
        additional_volumes = {manifest_dir: {'bind':container_dirs['manifest_dir'],  'mode':'ro'}}
        env_vars = None
        if log_level:
            env_vars = {'LAMBDA_BUILDERS_LOG_LEVEL': log_level}
        super(LambdaBuildContainer, self).__init__(image,
          cmd,
          (container_dirs['source_dir']),
          source_dir,
          additional_volumes=additional_volumes,
          entrypoint=entry,
          env_vars=env_vars)

    @property
    def executable_name(self):
        return LambdaBuildContainer._BUILDERS_EXECUTABLE

    @staticmethod
    def _make_request(protocol_version, language, dependency_manager, application_framework, container_dirs, manifest_file_name, runtime, optimizations, options, executable_search_paths, mode):
        return json.dumps({'jsonschema':'2.0', 
         'id':1, 
         'method':'LambdaBuilder.build', 
         'params':{'__protocol_version':protocol_version, 
          'capability':{'language':language, 
           'dependency_manager':dependency_manager, 
           'application_framework':application_framework}, 
          'source_dir':container_dirs['source_dir'], 
          'artifacts_dir':container_dirs['artifacts_dir'], 
          'scratch_dir':container_dirs['scratch_dir'], 
          'manifest_path':'{}/{}'.format(container_dirs['manifest_dir'], manifest_file_name), 
          'runtime':runtime, 
          'optimizations':optimizations, 
          'options':options, 
          'executable_search_paths':executable_search_paths, 
          'mode':mode}})

    @staticmethod
    def _get_entrypoint(request_json):
        return [LambdaBuildContainer._BUILDERS_EXECUTABLE, request_json]

    @staticmethod
    def _get_container_dirs(source_dir, manifest_dir):
        """
        Provides paths to directories within the container that is required by the builder

        Parameters
        ----------
        source_dir : str
            Path to the function source code

        manifest_dir : str
            Path to the directory containing manifest

        Returns
        -------
        dict
            Contains paths to source, artifacts, scratch & manifest directories
        """
        base = '/tmp/samcli'
        result = {'source_dir':'{}/source'.format(base), 
         'artifacts_dir':'{}/artifacts'.format(base), 
         'scratch_dir':'{}/scratch'.format(base), 
         'manifest_dir':'{}/manifest'.format(base)}
        if pathlib.PurePath(source_dir) == pathlib.PurePath(manifest_dir):
            result['manifest_dir'] = result['source_dir']
        return result

    @staticmethod
    def _convert_to_container_dirs(host_paths_to_convert, host_to_container_path_mapping):
        """
        Use this method to convert a list of host paths to a list of equivalent paths within the container
        where the given host path is mounted. This is necessary when SAM CLI needs to pass path information to
        the Lambda Builder running within the container.

        If a host path is not mounted within the container, then this method simply passes the path to the result
        without any changes.

        Ex:
            [ "/home/foo", "/home/bar", "/home/not/mounted"]  => ["/tmp/source", "/tmp/manifest", "/home/not/mounted"]

        Parameters
        ----------
        host_paths_to_convert : list
            List of paths in host that needs to be converted

        host_to_container_path_mapping : dict
            Mapping of paths in host to the equivalent paths within the container

        Returns
        -------
        list
            Equivalent paths within the container
        """
        if not host_paths_to_convert:
            return host_paths_to_convert
        mapping = {str(pathlib.Path(p).resolve()):v for p, v in host_to_container_path_mapping.items()}
        result = []
        for original_path in host_paths_to_convert:
            abspath = str(pathlib.Path(original_path).resolve())
            if abspath in mapping:
                result.append(mapping[abspath])
            else:
                result.append(original_path)
                LOG.debug("Cannot convert host path '%s' to its equivalent path within the container. Host path is not mounted within the container", abspath)

        return result

    @staticmethod
    def _get_image(runtime):
        runtime_to_images = {'nodejs10.x': 'amazon/lambda-build-node10.x'}
        return runtime_to_images.get(runtime, '{}:build-{}'.format(LambdaBuildContainer._LAMBCI_IMAGE_REPO_NAME, runtime))