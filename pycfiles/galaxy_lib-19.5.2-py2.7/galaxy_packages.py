# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/galaxy/tools/deps/resolvers/galaxy_packages.py
# Compiled at: 2018-04-20 03:19:42
import logging
from os import listdir
from os.path import basename, exists, isdir, islink, join, realpath
from . import Dependency, DependencyResolver, ListableDependencyResolver, MappableDependencyResolver, NullDependency
from .resolver_mixins import UsesToolDependencyDirMixin
log = logging.getLogger(__name__)

class GalaxyPackageDependency(Dependency):
    dict_collection_visible_keys = Dependency.dict_collection_visible_keys + ['script', 'path', 'version', 'name']
    dependency_type = 'galaxy_package'

    def __init__(self, script, path, name, type, version, exact=True):
        self.script = script
        self.path = path
        self.name = name
        self.type = type
        self.version = version
        self._exact = exact
        assert self.script is not None or self.path is not None
        return

    @property
    def exact(self):
        return self._exact

    def shell_commands(self):
        base_path = self.path
        if self.type == 'package' and self.script is None:
            commands = 'PACKAGE_BASE=%s; export PACKAGE_BASE; PATH="%s/bin:$PATH"; export PATH' % (base_path, base_path)
        else:
            commands = 'PACKAGE_BASE=%s; export PACKAGE_BASE; . %s' % (base_path, self.script)
        return commands


class ToolShedDependency(GalaxyPackageDependency):
    dependency_type = 'tool_shed_package'


class BaseGalaxyPackageDependencyResolver(DependencyResolver, UsesToolDependencyDirMixin):
    dict_collection_visible_keys = DependencyResolver.dict_collection_visible_keys + ['base_path', 'versionless']
    dependency_type = GalaxyPackageDependency

    def __init__(self, dependency_manager, **kwds):
        self.versionless = str(kwds.get('versionless', 'false')).lower() == 'true'
        self._init_base_path(dependency_manager, **kwds)

    def resolve(self, requirement, **kwds):
        """
        Attempt to find a dependency named `name` at version `version`. If version is None, return the "default" version as determined using a
        symbolic link (if found). Returns a triple of: env_script, base_path, real_version
        """
        name, version, type = requirement.name, requirement.version, requirement.type
        if version is None or self.versionless:
            exact = not self.versionless or version is None
            return self._find_dep_default(name, type=type, exact=exact, **kwds)
        else:
            return self._find_dep_versioned(name, version, type=type, **kwds)
            return

    def _find_dep_versioned(self, name, version, type='package', **kwds):
        base_path = self.base_path
        path = join(base_path, name, version)
        return self._galaxy_package_dep(path, version, name, type, True)

    def _find_dep_default(self, name, type='package', exact=True, **kwds):
        base_path = self.base_path
        path = join(base_path, name, 'default')
        if islink(path):
            real_path = realpath(path)
            real_version = basename(real_path)
            return self._galaxy_package_dep(real_path, real_version, name, type, exact)
        else:
            return NullDependency(version=None, name=name)
            return

    def _galaxy_package_dep(self, path, version, name, type, exact):
        script = join(path, 'env.sh')
        if exists(script):
            return self.dependency_type(script, path, name, type, version, exact)
        else:
            if exists(join(path, 'bin')):
                return self.dependency_type(None, path, name, type, version, exact)
            return NullDependency(version=version, name=name)


class GalaxyPackageDependencyResolver(BaseGalaxyPackageDependencyResolver, ListableDependencyResolver, MappableDependencyResolver):
    resolver_type = 'galaxy_packages'

    def __init__(self, dependency_manager, **kwds):
        super(GalaxyPackageDependencyResolver, self).__init__(dependency_manager, **kwds)
        self._setup_mapping(dependency_manager, **kwds)

    def resolve(self, requirement, **kwds):
        requirement = self._expand_mappings(requirement)
        return super(GalaxyPackageDependencyResolver, self).resolve(requirement, **kwds)

    def list_dependencies(self):
        base_path = self.base_path
        for package_name in listdir(base_path):
            package_dir = join(base_path, package_name)
            if isdir(package_dir):
                for version in listdir(package_dir):
                    version_dir = join(package_dir, version)
                    if version == 'default':
                        version = None
                    valid_dependency = _is_dependency_directory(version_dir)
                    if valid_dependency:
                        yield self._to_requirement(package_name, version)

        return


def _is_dependency_directory(directory):
    return exists(join(directory, 'env.sh')) or exists(join(directory, 'bin'))


__all__ = ('GalaxyPackageDependency', 'GalaxyPackageDependencyResolver', 'ToolShedDependency')