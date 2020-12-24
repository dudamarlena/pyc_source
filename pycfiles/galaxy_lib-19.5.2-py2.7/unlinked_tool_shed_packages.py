# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/galaxy/tools/deps/resolvers/unlinked_tool_shed_packages.py
# Compiled at: 2018-04-20 03:19:42
"""
Backup resolvers for when dependencies can not be loaded from the database.
Mainly suited for testing stage.

Ideally all dependencies will be stored in the database
    when a tool is added from a Tool Shed.
That should remain the preferred way of locating dependencies.

In cases where that is not possible
    for example during testing this resolver can act as a backup.
This resolver looks not just for manually added dependencies
    but also ones added from a Tool Shed.

This tool is still under development so the default behaviour could change.
It has been tested when placed in the same directory as galaxy_packages.py

At the time of writing July 3 2015 this resolver has to be plugged in.
See bottom for instructions on how to add this resolver.

"""
import logging
from os import listdir
from os.path import exists, getmtime, join
from . import Dependency, NullDependency
from .galaxy_packages import BaseGalaxyPackageDependencyResolver
log = logging.getLogger(__name__)
MANUAL = 'manual'
PREFERRED_OWNERS = MANUAL + ',iuc,devteam'

class UnlinkedToolShedPackageDependencyResolver(BaseGalaxyPackageDependencyResolver):
    dict_collection_visible_keys = BaseGalaxyPackageDependencyResolver.dict_collection_visible_keys + ['preferred_owners', 'select_by_owner']
    resolver_type = 'unlinked_tool_shed_packages'

    def __init__(self, dependency_manager, **kwds):
        super(UnlinkedToolShedPackageDependencyResolver, self).__init__(dependency_manager, **kwds)
        self.preferred_owners = kwds.get('preferred_owners', PREFERRED_OWNERS).split(',')
        self.select_by_owner = str(kwds.get('select_by_owner', 'true')).lower() != 'false'

    def _find_dep_versioned(self, name, version, type='package', **kwds):
        try:
            possibles = self._find_possible_dependencies(name, version, type)
            if len(possibles) == 0:
                log.debug("Unable to find dependency,'%s' '%s' '%s'", name, version, type)
                return NullDependency(version=version, name=name)
            if len(possibles) == 1:
                return possibles[0].dependency
            return self._select_preferred_dependency(possibles).dependency
        except Exception:
            log.exception("Unexpected error hunting for dependency '%s' '%s''%s'", name, version, type)
            return NullDependency(version=version, name=name)

    def _find_possible_dependencies(self, name, version, type):
        possibles = []
        if exists(self.base_path):
            path = join(self.base_path, name, version)
            if exists(path):
                package = self._galaxy_package_dep(path, version, name, type, True)
                if not isinstance(package, NullDependency):
                    log.debug("Found dependency '%s' '%s' '%s' at '%s'", name, version, type, path)
                    possibles.append(CandidateDependency(package, path))
                for owner in listdir(path):
                    owner_path = join(path, owner)
                    for package_name in listdir(owner_path):
                        if package_name.lower().startswith('package_' + name.lower()):
                            package_path = join(owner_path, package_name)
                            for revision in listdir(package_path):
                                revision_path = join(package_path, revision)
                                package = self._galaxy_package_dep(revision_path, version, name, type, True)
                                if not isinstance(package, NullDependency):
                                    log.debug("Found dependency '%s' '%s' '%s' at '%s'", name, version, type, revision_path)
                                    possibles.append(CandidateDependency(package, package_path, owner))

        return possibles

    def _select_preferred_dependency(self, possibles, by_owner=None):
        if by_owner is None:
            by_owner = self.select_by_owner
        preferred = []
        if by_owner:
            for owner in self.preferred_owners:
                for candidate in possibles:
                    if candidate.owner == owner:
                        preferred.append(candidate)

                if len(preferred) == 1:
                    log.debug("Picked dependency based on owner '%s'", owner)
                    return preferred[0]
                if len(preferred) > 1:
                    log.debug("Multiple dependency found with owner '%s'", owner)
                    break

        if len(preferred) == 0:
            preferred = possibles
        latest_modified = 0
        for candidate in preferred:
            modified = getmtime(candidate.path)
            if latest_modified < modified:
                latest_candidate = candidate
                latest_modified = modified

        log.debug("Picking dependency at '%s' as it was the last modified", latest_candidate.path)
        return latest_candidate


class CandidateDependency(Dependency):
    dict_collection_visible_keys = Dependency.dict_collection_visible_keys + ['dependency', 'path', 'owner']
    dependency_type = 'unlinked_tool_shed_package'

    @property
    def exact(self):
        return self.dependency.exact

    def __init__(self, dependency, path, owner=MANUAL):
        self.dependency = dependency
        self.path = path
        self.owner = owner

    def shell_commands(self):
        """
        Return shell commands to enable this dependency.
        """
        return self.dependency.shell_commands()


__all__ = ('UnlinkedToolShedPackageDependencyResolver', )