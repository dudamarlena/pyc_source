# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python3.7/site-packages/aprt/outdated.py
# Compiled at: 2019-08-02 08:01:39
# Size of source mod 2**32: 2803 bytes
from . import alpm

def provides_dep(package, other_package):
    """ Check if a package provides a dependency of another package. """
    for dep in other_package.alldepends():
        if package.providesName(dep.name):
            return True

    return False


def package_path(repository_dir, package, compression='xz'):
    return '{}/{}-{}-{}.pkg.tar.{}'.format(repository_dir, package.name, package.version(), package.get_value('arch'), compression)


def find_newer_deps(package, repository_dir, universe, ignore, quick):
    built_package = alpm.read_package_file(package_path(repository_dir, package))
    for installed in built_package.installed():
        if installed.name in ignore:
            continue
        try:
            if not provides_dep(universe[installed.name], package):
                continue
        except KeyError:
            continue

        new_version = universe[installed.name].version()
        if installed.version() < new_version:
            yield (
             installed.name, installed.version(), new_version)
            if quick:
                return


def find_outdated(repository, repository_dir, universe, ignore, quick):
    for name, package in repository.items():
        newer_deps = list(find_newer_deps(package, repository_dir, universe, ignore, quick))
        if newer_deps:
            yield (
             name, newer_deps)