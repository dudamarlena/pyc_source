# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/samcli/lib/build/workflow_config.py
# Compiled at: 2020-03-21 12:32:11
# Size of source mod 2**32: 9053 bytes
"""
Contains Builder Workflow Configs for different Runtimes
"""
import os, logging
from collections import namedtuple
LOG = logging.getLogger(__name__)
CONFIG = namedtuple('Capability', ['language', 'dependency_manager', 'application_framework', 'manifest_name',
 'executable_search_paths'])
PYTHON_PIP_CONFIG = CONFIG(language='python',
  dependency_manager='pip',
  application_framework=None,
  manifest_name='requirements.txt',
  executable_search_paths=None)
NODEJS_NPM_CONFIG = CONFIG(language='nodejs',
  dependency_manager='npm',
  application_framework=None,
  manifest_name='package.json',
  executable_search_paths=None)
RUBY_BUNDLER_CONFIG = CONFIG(language='ruby',
  dependency_manager='bundler',
  application_framework=None,
  manifest_name='Gemfile',
  executable_search_paths=None)
JAVA_GRADLE_CONFIG = CONFIG(language='java',
  dependency_manager='gradle',
  application_framework=None,
  manifest_name='build.gradle',
  executable_search_paths=None)
JAVA_KOTLIN_GRADLE_CONFIG = CONFIG(language='java',
  dependency_manager='gradle',
  application_framework=None,
  manifest_name='build.gradle.kts',
  executable_search_paths=None)
JAVA_MAVEN_CONFIG = CONFIG(language='java',
  dependency_manager='maven',
  application_framework=None,
  manifest_name='pom.xml',
  executable_search_paths=None)
DOTNET_CLIPACKAGE_CONFIG = CONFIG(language='dotnet',
  dependency_manager='cli-package',
  application_framework=None,
  manifest_name='.csproj',
  executable_search_paths=None)
GO_MOD_CONFIG = CONFIG(language='go',
  dependency_manager='modules',
  application_framework=None,
  manifest_name='go.mod',
  executable_search_paths=None)

class UnsupportedRuntimeException(Exception):
    pass


def get_workflow_config(runtime, code_dir, project_dir):
    """
    Get a workflow config that corresponds to the runtime provided. This method examines contents of the project
    and code directories to determine the most appropriate workflow for the given runtime. Currently the decision is
    based on the presence of a supported manifest file. For runtimes that have more than one workflow, we choose a
    workflow by examining ``code_dir`` followed by ``project_dir`` for presence of a supported manifest.

    Parameters
    ----------
    runtime str
        The runtime of the config

    code_dir str
        Directory where Lambda function code is present

    project_dir str
        Root of the Serverless application project.

    Returns
    -------
    namedtuple(Capability)
        namedtuple that represents the Builder Workflow Config
    """
    selectors_by_runtime = {'python2.7':BasicWorkflowSelector(PYTHON_PIP_CONFIG), 
     'python3.6':BasicWorkflowSelector(PYTHON_PIP_CONFIG), 
     'python3.7':BasicWorkflowSelector(PYTHON_PIP_CONFIG), 
     'python3.8':BasicWorkflowSelector(PYTHON_PIP_CONFIG), 
     'nodejs4.3':BasicWorkflowSelector(NODEJS_NPM_CONFIG), 
     'nodejs6.10':BasicWorkflowSelector(NODEJS_NPM_CONFIG), 
     'nodejs8.10':BasicWorkflowSelector(NODEJS_NPM_CONFIG), 
     'nodejs10.x':BasicWorkflowSelector(NODEJS_NPM_CONFIG), 
     'nodejs12.x':BasicWorkflowSelector(NODEJS_NPM_CONFIG), 
     'ruby2.5':BasicWorkflowSelector(RUBY_BUNDLER_CONFIG), 
     'ruby2.7':BasicWorkflowSelector(RUBY_BUNDLER_CONFIG), 
     'dotnetcore2.0':BasicWorkflowSelector(DOTNET_CLIPACKAGE_CONFIG), 
     'dotnetcore2.1':BasicWorkflowSelector(DOTNET_CLIPACKAGE_CONFIG), 
     'go1.x':BasicWorkflowSelector(GO_MOD_CONFIG), 
     'java8':ManifestWorkflowSelector([
      JAVA_GRADLE_CONFIG._replace(executable_search_paths=[code_dir, project_dir]),
      JAVA_KOTLIN_GRADLE_CONFIG._replace(executable_search_paths=[code_dir, project_dir]),
      JAVA_MAVEN_CONFIG]), 
     'java11':ManifestWorkflowSelector([
      JAVA_GRADLE_CONFIG._replace(executable_search_paths=[code_dir, project_dir]),
      JAVA_KOTLIN_GRADLE_CONFIG._replace(executable_search_paths=[code_dir, project_dir]),
      JAVA_MAVEN_CONFIG])}
    if runtime not in selectors_by_runtime:
        raise UnsupportedRuntimeException("'{}' runtime is not supported".format(runtime))
    selector = selectors_by_runtime[runtime]
    try:
        config = selector.get_config(code_dir, project_dir)
        return config
    except ValueError as ex:
        try:
            raise UnsupportedRuntimeException("Unable to find a supported build workflow for runtime '{}'. Reason: {}".format(runtime, str(ex)))
        finally:
            ex = None
            del ex


def supports_build_in_container(config):
    """
    Given a workflow config, this method provides a boolean on whether the workflow can run within a container or not.

    Parameters
    ----------
    config namedtuple(Capability)
        Config specifying the particular build workflow

    Returns
    -------
    tuple(bool, str)
        True, if this workflow can be built inside a container. False, along with a reason message if it cannot be.
    """

    def _key(c):
        return str(c.language) + str(c.dependency_manager) + str(c.application_framework)

    unsupported = {_key(DOTNET_CLIPACKAGE_CONFIG): 'We do not support building .NET Core Lambda functions within a container. Try building without the container. Most .NET Core functions will build successfully.', 
     _key(GO_MOD_CONFIG): 'We do not support building Go Lambda functions within a container. Try building without the container. Most Go functions will build successfully.'}
    thiskey = _key(config)
    if thiskey in unsupported:
        return (
         False, unsupported[thiskey])
    return (True, None)


class BasicWorkflowSelector:
    __doc__ = '\n    Basic workflow selector that returns the first available configuration in the given list of configurations\n    '

    def __init__(self, configs):
        if not isinstance(configs, list):
            configs = [
             configs]
        self.configs = configs

    def get_config(self, code_dir, project_dir):
        """
        Returns the first available configuration
        """
        return self.configs[0]


class ManifestWorkflowSelector(BasicWorkflowSelector):
    __doc__ = '\n    Selects a workflow by examining the directories for presence of a supported manifest\n    '

    def get_config(self, code_dir, project_dir):
        """
        Finds a configuration by looking for a manifest in the given directories.

        Returns
        -------
        samcli.lib.build.workflow_config.CONFIG
            A supported configuration if one is found

        Raises
        ------
        ValueError
            If none of the supported manifests files are found
        """
        search_dirs = [
         code_dir, project_dir]
        LOG.debug('Looking for a supported build workflow in following directories: %s', search_dirs)
        for config in self.configs:
            if any([self._has_manifest(config, directory) for directory in search_dirs]):
                return config

        raise ValueError("None of the supported manifests '{}' were found in the following paths '{}'".format([config.manifest_name for config in self.configs], search_dirs))

    @staticmethod
    def _has_manifest(config, directory):
        return os.path.exists(os.path.join(directory, config.manifest_name))