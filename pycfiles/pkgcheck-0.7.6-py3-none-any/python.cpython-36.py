# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/runner/work/pkgcheck/pkgcheck/build/lib/pkgcheck/checks/python.py
# Compiled at: 2020-02-09 15:46:32
# Size of source mod 2**32: 9213 bytes
from pkgcore.ebuild.atom import atom
from pkgcore.restrictions import packages, values
from pkgcore.restrictions.boolean import JustOneRestriction, OrRestriction
from snakeoil.sequences import iflatten_instance
from .. import results
from . import Check
ECLASSES = frozenset(['python-r1', 'python-single-r1', 'python-any-r1'])
INTERPRETERS = frozenset([
 'dev-lang/python',
 'dev-python/pypy',
 'dev-python/pypy3',
 'dev-python/pypy-bin',
 'dev-python/pypy3-bin',
 'virtual/pypy',
 'virtual/pypy3'])
CHECK_EXCLUDE = frozenset(['virtual/pypy', 'virtual/pypy3'])
IUSE_PREFIX = 'python_targets_'
IUSE_PREFIX_S = 'python_single_target_'

class MissingPythonEclass(results.VersionResult, results.Warning):
    __doc__ = 'Package depends on Python but does not use the eclasses.\n\n    All packages depending on Python are required to use one of the following\n    python eclasses: python-r1, python-single-r1, or python-any-r1. For\n    documentation on choosing the correct eclass, please see the Python project\n    wiki page on eclasses [#]_.\n\n    .. [#] https://wiki.gentoo.org/wiki/Project:Python/Eclasses\n    '

    def __init__(self, eclass, dep_type, dep, **kwargs):
        (super().__init__)(**kwargs)
        self.eclass = eclass
        self.dep_type = dep_type
        self.dep = dep

    @property
    def desc(self):
        return f'missing {self.eclass} eclass usage for {self.dep_type}="{self.dep}"'


class PythonMissingRequiredUse(results.VersionResult, results.Warning):
    __doc__ = 'Package is missing PYTHON_REQUIRED_USE.\n\n    The python-r1 and python-single-r1 eclasses require the packages to\n    explicitly specify `REQUIRED_USE=${PYTHON_REQUIRED_USE}`. If Python is used\n    conditionally, it can be wrapped in appropriate USE conditionals.\n    '

    @property
    def desc(self):
        return 'missing REQUIRED_USE="${PYTHON_REQUIRED_USE}"'


class PythonMissingDeps(results.VersionResult, results.Warning):
    __doc__ = 'Package is missing PYTHON_DEPS.\n\n    The python-r1 and python-single-r1 eclasses require the packages\n    to explicitly reference `${PYTHON_DEPS}` in RDEPEND (and DEPEND,\n    if necessary); python-any-r1 requires it in DEPEND.\n\n    If Python is used conditionally, the dependency can be wrapped\n    in appropriate USE conditionals.\n    '

    def __init__(self, dep_type, **kwargs):
        (super().__init__)(**kwargs)
        self.dep_type = dep_type

    @property
    def desc(self):
        return f'missing {self.dep_type}="${{PYTHON_DEPS}}"'


class PythonRuntimeDepInAnyR1(results.VersionResult, results.Warning):
    __doc__ = 'Package depends on Python at runtime but uses any-r1 eclass.\n\n    The python-any-r1 eclass is meant to be used purely for build-time\n    dependencies on Python. However, this package lists Python as a runtime\n    dependency. If this is intentional, the package needs to switch to\n    python-r1 or python-single-r1 eclass, otherwise the runtime dependency\n    should be removed.\n    '

    def __init__(self, dep_type, dep, **kwargs):
        (super().__init__)(**kwargs)
        self.dep_type = dep_type
        self.dep = dep

    @property
    def desc(self):
        return f'inherits python-any-r1 with {self.dep_type}="{self.dep}" -- use python-r1 or python-single-r1 instead'


class PythonEclassError(results.VersionResult, results.Error):
    __doc__ = 'Generic python eclass error.'

    def __init__(self, msg, **kwargs):
        (super().__init__)(**kwargs)
        self.msg = msg

    @property
    def desc(self):
        return self.msg


class PythonCheck(Check):
    __doc__ = "Python eclass checks.\n\n    Check whether Python eclasses are used for Python packages, and whether\n    they don't suffer from common mistakes.\n    "
    known_results = frozenset([
     MissingPythonEclass, PythonMissingRequiredUse,
     PythonMissingDeps, PythonRuntimeDepInAnyR1, PythonEclassError])

    @staticmethod
    def get_python_eclass(pkg):
        eclasses = set(ECLASSES).intersection(pkg.inherited)
        if len(eclasses) > 1:
            raise ValueError(f"python eclasses are mutually exclusive: [ {', '.join(eclasses)} ]")
        if eclasses:
            return eclasses.pop()

    def scan_tree_recursively(self, deptree, expected_cls):
        for x in deptree:
            if not isinstance(x, expected_cls):
                for y in self.scan_tree_recursively(x, expected_cls):
                    yield y

        yield deptree

    def check_required_use(self, requse, flags, prefix, container_cls):
        for token in self.scan_tree_recursively(requse, values.ContainmentMatch2):
            if len(flags) > 1:
                if not isinstance(token, container_cls):
                    continue
                matched = set()
                for x in token:
                    if not isinstance(x, values.ContainmentMatch2):
                        pass
                    else:
                        name = next(iter(x.vals))
                        if name.startswith(prefix):
                            matched.add(name[len(prefix):])
                        elif isinstance(token, container_cls):
                            break
                else:
                    if flags == matched:
                        return True

        return False

    def check_depend(self, depend, flags, prefix):
        for token in self.scan_tree_recursively(depend, atom):
            matched = set()
            for x in token:
                if not isinstance(x, packages.Conditional):
                    pass
                else:
                    flag = next(iter(x.restriction.vals))
                    if not flag.startswith(prefix):
                        pass
                    else:
                        if not any(y.key in INTERPRETERS for y in x if isinstance(y, atom)):
                            pass
                        else:
                            matched.add(flag[len(prefix):])

            if matched == flags:
                return True

        return False

    def feed(self, pkg):
        try:
            eclass = self.get_python_eclass(pkg)
        except ValueError as e:
            yield PythonEclassError((str(e)), pkg=pkg)
            return

        if eclass is None:
            if pkg.key in CHECK_EXCLUDE:
                return
            highest_found = None
            for attr in (x.lower() for x in pkg.eapi.dep_keys):
                for p in iflatten_instance(getattr(pkg, attr), atom):
                    if not p.blocks:
                        if p.key in INTERPRETERS:
                            highest_found = (
                             attr, p)
                            break

            if highest_found is not None:
                attr, p = highest_found
                if attr in ('rdepend', 'pdepend'):
                    recomm = 'python-r1 or python-single-r1'
                else:
                    recomm = 'python-any-r1'
                yield MissingPythonEclass(recomm, (attr.upper()), (str(p)), pkg=pkg)
        else:
            if eclass in ('python-r1', 'python-single-r1'):
                iuse = [x.lstrip('+-') for x in pkg.iuse]
                flags = {x[len(IUSE_PREFIX):] for x in iuse if x.startswith(IUSE_PREFIX) if x.startswith(IUSE_PREFIX)}
                s_flags = {x[len(IUSE_PREFIX_S):] for x in iuse if x.startswith(IUSE_PREFIX_S) if x.startswith(IUSE_PREFIX_S)}
                if eclass == 'python-r1':
                    req_use_args = (
                     flags, IUSE_PREFIX, OrRestriction)
                else:
                    req_use_args = (
                     s_flags, IUSE_PREFIX_S, JustOneRestriction)
                if not (self.check_required_use)(pkg.required_use, *req_use_args):
                    yield PythonMissingRequiredUse(pkg=pkg)
                if not (self.check_depend)(pkg.rdepend, *req_use_args[:2]):
                    yield PythonMissingDeps('RDEPEND', pkg=pkg)
            else:
                for attr in ('rdepend', 'pdepend'):
                    for p in iflatten_instance(getattr(pkg, attr), atom):
                        if not p.blocks and p.key in INTERPRETERS:
                            yield PythonRuntimeDepInAnyR1((attr.upper()), (str(p)), pkg=pkg)
                            break

                for attr in ('depend', 'bdepend'):
                    for p in iflatten_instance(getattr(pkg, attr), atom):
                        if not p.blocks and p.key in INTERPRETERS:
                            break
                    else:
                        continue

                    break
                else:
                    yield PythonMissingDeps('DEPEND', pkg=pkg)