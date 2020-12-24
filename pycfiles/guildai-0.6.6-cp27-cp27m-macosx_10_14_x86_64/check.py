# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./guild/external/pip/_internal/operations/check.py
# Compiled at: 2019-09-10 15:18:29
"""Validation of dependencies of packages
"""
from collections import namedtuple
from pip._vendor.packaging.utils import canonicalize_name
from pip._internal.operations.prepare import make_abstract_dist
from pip._internal.utils.misc import get_installed_distributions
from pip._internal.utils.typing import MYPY_CHECK_RUNNING
if MYPY_CHECK_RUNNING:
    from pip._internal.req.req_install import InstallRequirement
    from typing import Any, Callable, Dict, Iterator, Optional, Set, Tuple, List
    PackageSet = Dict[(str, 'PackageDetails')]
    Missing = Tuple[(str, Any)]
    Conflicting = Tuple[(str, str, Any)]
    MissingDict = Dict[(str, List[Missing])]
    ConflictingDict = Dict[(str, List[Conflicting])]
    CheckResult = Tuple[(MissingDict, ConflictingDict)]
PackageDetails = namedtuple('PackageDetails', ['version', 'requires'])

def create_package_set_from_installed(**kwargs):
    """Converts a list of distributions into a PackageSet.
    """
    if kwargs == {}:
        kwargs = {'local_only': False, 'skip': ()}
    package_set = {}
    for dist in get_installed_distributions(**kwargs):
        name = canonicalize_name(dist.project_name)
        package_set[name] = PackageDetails(dist.version, dist.requires())

    return package_set


def check_package_set(package_set, should_ignore=None):
    """Check if a package set is consistent

    If should_ignore is passed, it should be a callable that takes a
    package name and returns a boolean.
    """
    if should_ignore is None:

        def should_ignore(name):
            return False

    missing = dict()
    conflicting = dict()
    for package_name in package_set:
        missing_deps = set()
        conflicting_deps = set()
        if should_ignore(package_name):
            continue
        for req in package_set[package_name].requires:
            name = canonicalize_name(req.project_name)
            if name not in package_set:
                missed = True
                if req.marker is not None:
                    missed = req.marker.evaluate()
                if missed:
                    missing_deps.add((name, req))
                continue
            version = package_set[name].version
            if not req.specifier.contains(version, prereleases=True):
                conflicting_deps.add((name, version, req))

        if missing_deps:
            missing[package_name] = sorted(missing_deps, key=str)
        if conflicting_deps:
            conflicting[package_name] = sorted(conflicting_deps, key=str)

    return (
     missing, conflicting)


def check_install_conflicts(to_install):
    """For checking if the dependency graph would be consistent after     installing given requirements
    """
    package_set = create_package_set_from_installed()
    would_be_installed = _simulate_installation_of(to_install, package_set)
    whitelist = _create_whitelist(would_be_installed, package_set)
    return (
     package_set,
     check_package_set(package_set, should_ignore=lambda name: name not in whitelist))


def _simulate_installation_of(to_install, package_set):
    """Computes the version of packages after installing to_install.
    """
    installed = set()
    for inst_req in to_install:
        dist = make_abstract_dist(inst_req).dist(finder=None)
        name = canonicalize_name(dist.key)
        package_set[name] = PackageDetails(dist.version, dist.requires())
        installed.add(name)

    return installed


def _create_whitelist(would_be_installed, package_set):
    packages_affected = set(would_be_installed)
    for package_name in package_set:
        if package_name in packages_affected:
            continue
        for req in package_set[package_name].requires:
            if canonicalize_name(req.name) in packages_affected:
                packages_affected.add(package_name)
                break

    return packages_affected