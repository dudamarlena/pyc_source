# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/runner/work/pkgcheck/pkgcheck/build/lib/pkgcheck/checks/repo.py
# Compiled at: 2020-02-09 15:46:32
# Size of source mod 2**32: 2887 bytes
import os
from snakeoil.osutils import pjoin
from .. import base, git, results, sources
from ..packages import RawCPV
from ..utils import is_binary
from . import GentooRepoCheck

class BinaryFile(results.Error):
    __doc__ = 'Binary file found in the repository.'

    def __init__(self, path):
        super().__init__()
        self.path = path

    @property
    def desc(self):
        return f"binary file found in repository: {self.path!r}"


class RepoDirCheck(GentooRepoCheck):
    __doc__ = 'Scan all files in the repository for issues.'
    scope = base.repo_scope
    _source = sources.EmptySource
    required_addons = (git.GitAddon,)
    known_results = frozenset([BinaryFile])
    ignored_root_dirs = frozenset(['.git'])

    def __init__(self, *args, git_addon):
        (super().__init__)(*args)
        self.gitignored = git_addon.gitignored
        self.repo = self.options.target_repo
        self.ignored_paths = {pjoin(self.repo.location, x) for x in self.ignored_root_dirs}
        self.dirs = [self.repo.location]

    def finish(self):
        while self.dirs:
            for entry in os.scandir(self.dirs.pop()):
                if entry.is_dir(follow_symlinks=False):
                    if entry.path in self.ignored_paths or self.gitignored(entry.path):
                        pass
                    else:
                        self.dirs.append(entry.path)
                else:
                    if is_binary(entry.path):
                        rel_path = self.gitignored(entry.path) or entry.path[len(self.repo.location) + 1:]
                        yield BinaryFile(rel_path)


class EmptyCategoryDir(results.CategoryResult, results.Warning):
    __doc__ = 'Empty category directory in the repository.'
    scope = base.repo_scope

    @property
    def desc(self):
        return f"empty category directory: {self.category}"


class EmptyPackageDir(results.PackageResult, results.Warning):
    __doc__ = 'Empty package directory in the repository.'
    scope = base.repo_scope

    @property
    def desc(self):
        return f"empty package directory: {self.category}/{self.package}"


class EmptyDirsCheck(GentooRepoCheck):
    __doc__ = 'Scan for empty category or package directories.'
    scope = base.repo_scope
    _source = sources.EmptySource
    known_results = frozenset([EmptyCategoryDir, EmptyPackageDir])

    def __init__(self, *args):
        (super().__init__)(*args)
        self.repo = self.options.target_repo

    def finish(self):
        for cat, pkgs in sorted(self.repo.packages.items()):
            if not pkgs:
                yield EmptyCategoryDir(pkg=(RawCPV(cat, None, None)))
            else:
                for pkg in sorted(pkgs):
                    versions = self.repo.versions[(cat, pkg)]
                    if not versions:
                        yield EmptyPackageDir(pkg=(RawCPV(cat, pkg, None)))