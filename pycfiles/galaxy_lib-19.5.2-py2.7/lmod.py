# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/galaxy/tools/deps/resolvers/lmod.py
# Compiled at: 2018-04-20 03:19:42
"""
This is a prototype dependency resolver to be able to use the "LMOD environment modules system" from TACC to solve package requirements

LMOD official website: https://www.tacc.utexas.edu/research-development/tacc-projects/lmod

LMOD @ Github: https://github.com/TACC/Lmod

"""
import logging
from os import getenv
from os.path import exists
from subprocess import PIPE, Popen
from six import StringIO
from . import Dependency, DependencyResolver, MappableDependencyResolver, NullDependency
log = logging.getLogger(__name__)
DEFAULT_LMOD_PATH = getenv('LMOD_CMD')
DEFAULT_SETTARG_PATH = getenv('LMOD_SETTARG_CMD')
DEFAULT_MODULEPATH = getenv('MODULEPATH')
DEFAULT_MAPPING_FILE = 'config/lmod_modules_mapping.yml'
INVALID_LMOD_PATH_MSG = 'The following LMOD executable could not be found: %s. Either your LMOD Dependency Resolver is misconfigured or LMOD is improperly installed on your system !'
EMPTY_MODULEPATH_MSG = 'No valid LMOD MODULEPATH defined ! Either your LMOD Dependency Resolver is misconfigured or LMOD is improperly installed on your system !'

class LmodDependencyResolver(DependencyResolver, MappableDependencyResolver):
    """Dependency resolver based on the LMOD environment modules system"""
    dict_collection_visible_keys = DependencyResolver.dict_collection_visible_keys + ['base_path', 'modulepath']
    resolver_type = 'lmod'

    def __init__(self, dependency_manager, **kwds):
        self._set_default_mapping_file(kwds)
        self._setup_mapping(dependency_manager, **kwds)
        self.versionless = _string_as_bool(kwds.get('versionless', 'false'))
        self.lmodexec = kwds.get('lmodexec', DEFAULT_LMOD_PATH)
        self.settargexec = kwds.get('settargexec', DEFAULT_SETTARG_PATH)
        self.modulepath = kwds.get('modulepath', DEFAULT_MODULEPATH)
        self.module_checker = AvailModuleChecker(self, self.modulepath)

    def _set_default_mapping_file(self, resolver_attributes):
        if 'mapping_files' not in resolver_attributes:
            if exists(DEFAULT_MAPPING_FILE):
                resolver_attributes['mapping_files'] = DEFAULT_MAPPING_FILE

    def resolve(self, requirement, **kwds):
        requirement = self._expand_mappings(requirement)
        name, version, type = requirement.name, requirement.version, requirement.type
        if type != 'package':
            return NullDependency(version=version, name=name)
        else:
            if self.__has_module(name, version):
                return LmodDependency(self, name, version, exact=True)
            if self.versionless and self.__has_module(name, None):
                return LmodDependency(self, name, None, exact=False)
            return NullDependency(version=version, name=name)

    def __has_module(self, name, version):
        return self.module_checker.has_module(name, version)


class AvailModuleChecker(object):
    """Parses the output of Lmod 'module avail' command to get the list of available modules."""

    def __init__(self, lmod_dependency_resolver, modulepath):
        self.lmod_dependency_resolver = lmod_dependency_resolver
        self.modulepath = modulepath

    def has_module(self, module, version):
        if version is None:
            available_modules = self.__get_list_of_available_modules(True)
        else:
            available_modules = self.__get_list_of_available_modules(False)
        for module_name, module_version in available_modules:
            names_match = module == module_name
            module_match = names_match and (version is None or module_version == version)
            if module_match:
                return True

        return False

    def __get_list_of_available_modules(self, default_version_only=False):
        raw_output = self.__get_module_avail_command_output(default_version_only).decode('utf-8')
        for line in StringIO(raw_output):
            line = line and line.strip()
            if not line or line.startswith('/'):
                continue
            module_parts = line.split('/')
            if len(module_parts) == 2:
                yield (
                 module_parts[0], module_parts[1])

    def __get_module_avail_command_output(self, default_version_only=False):
        lmodexec = self.lmod_dependency_resolver.lmodexec
        if not exists(lmodexec):
            raise Exception(INVALID_LMOD_PATH_MSG % lmodexec)
        if self.modulepath == '' or self.modulepath is None:
            raise Exception(EMPTY_MODULEPATH_MSG)
        if default_version_only:
            module_avail_command = [
             lmodexec, '-t', '-d', 'avail']
        else:
            module_avail_command = [
             lmodexec, '-t', 'avail']
        return Popen(module_avail_command, stdout=PIPE, stderr=PIPE, env={'MODULEPATH': self.modulepath}, close_fds=True).communicate()[1]


class LmodDependency(Dependency):
    """Prepare the commands required to solve the dependency and add them to the script used to run a tool in Galaxy."""
    dict_collection_visible_keys = Dependency.dict_collection_visible_keys + ['module_name', 'module_version']
    dependency_type = 'lmod'

    def __init__(self, lmod_dependency_resolver, module_name, module_version=None, exact=True):
        self.lmod_dependency_resolver = lmod_dependency_resolver
        self.module_name = module_name
        self.module_version = module_version
        self._exact = exact

    @property
    def name(self):
        return self.module_name

    @property
    def version(self):
        return self.module_version

    @property
    def exact(self):
        return self._exact

    def shell_commands(self):
        module_to_load = self.module_name
        if self.module_version:
            module_to_load = '%s/%s' % (self.module_name, self.module_version)
        command = 'MODULEPATH=%s; ' % self.lmod_dependency_resolver.modulepath
        command += 'export MODULEPATH; '
        command += 'eval `%s load %s` ' % (self.lmod_dependency_resolver.lmodexec, module_to_load)
        if self.lmod_dependency_resolver.settargexec is not None:
            command += '&& eval `%s -s sh`' % self.lmod_dependency_resolver.settargexec
        return command


def _string_as_bool(value):
    return str(value).lower() == 'true'


__all__ = ('LmodDependencyResolver', )