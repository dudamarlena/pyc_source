# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-vxs8l7gu/pip/pip/_internal/resolution/resolvelib/candidates.py
# Compiled at: 2020-05-05 12:41:36
# Size of source mod 2**32: 15173 bytes
import logging, sys
from pip._vendor.packaging.specifiers import InvalidSpecifier, SpecifierSet
from pip._vendor.packaging.utils import canonicalize_name
from pip._vendor.packaging.version import Version
from pip._internal.req.constructors import install_req_from_editable, install_req_from_line
from pip._internal.req.req_install import InstallRequirement
from pip._internal.utils.misc import normalize_version_info
from pip._internal.utils.packaging import get_requires_python
from pip._internal.utils.typing import MYPY_CHECK_RUNNING
from .base import Candidate, format_name
if MYPY_CHECK_RUNNING:
    from typing import Any, Optional, Sequence, Set, Tuple, Union
    from pip._vendor.packaging.version import _BaseVersion
    from pip._vendor.pkg_resources import Distribution
    from pip._internal.distributions import AbstractDistribution
    from pip._internal.models.link import Link
    from .base import Requirement
    from .factory import Factory
    BaseCandidate = Union[('AlreadyInstalledCandidate', 'EditableCandidate', 'LinkCandidate')]
logger = logging.getLogger(__name__)

def make_install_req_from_link(link, parent):
    if parent.editable:
        raise AssertionError('parent is editable')
    return install_req_from_line((link.url),
      comes_from=(parent.comes_from),
      use_pep517=(parent.use_pep517),
      isolated=(parent.isolated),
      constraint=(parent.constraint),
      options=dict(install_options=(parent.install_options),
      global_options=(parent.global_options),
      hashes=(parent.hash_options)))


def make_install_req_from_editable(link, parent):
    assert parent.editable, 'parent not editable'
    return install_req_from_editable((link.url),
      comes_from=(parent.comes_from),
      use_pep517=(parent.use_pep517),
      isolated=(parent.isolated),
      constraint=(parent.constraint),
      options=dict(install_options=(parent.install_options),
      global_options=(parent.global_options),
      hashes=(parent.hash_options)))


def make_install_req_from_dist(dist, parent):
    ireq = install_req_from_line(('{}=={}'.format(canonicalize_name(dist.project_name), dist.parsed_version)),
      comes_from=(parent.comes_from),
      use_pep517=(parent.use_pep517),
      isolated=(parent.isolated),
      constraint=(parent.constraint),
      options=dict(install_options=(parent.install_options),
      global_options=(parent.global_options),
      hashes=(parent.hash_options)))
    ireq.satisfied_by = dist
    return ireq


class _InstallRequirementBackedCandidate(Candidate):

    def __init__(self, link, ireq, factory, name=None, version=None):
        self.link = link
        self._factory = factory
        self._ireq = ireq
        self._name = name
        self._version = version
        self._dist = None

    def __repr__(self):
        return '{class_name}({link!r})'.format(class_name=(self.__class__.__name__),
          link=(str(self.link)))

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.link == other.link
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    @property
    def name(self):
        """The normalised name of the project the candidate refers to"""
        if self._name is None:
            self._name = canonicalize_name(self.dist.project_name)
        return self._name

    @property
    def version(self):
        if self._version is None:
            self._version = self.dist.parsed_version
        return self._version

    def _prepare_abstract_distribution(self):
        raise NotImplementedError('Override in subclass')

    def _prepare(self):
        if self._dist is not None:
            return
            abstract_dist = self._prepare_abstract_distribution()
            self._dist = abstract_dist.get_pkg_resources_distribution()
            if not self._dist is not None:
                raise AssertionError('Distribution already installed')
        else:
            if not self._name is None:
                assert self._name == canonicalize_name(self._dist.project_name), 'Name mismatch: {!r} vs {!r}'.format(self._name, canonicalize_name(self._dist.project_name))
            if not self._version is None:
                if not self._version == self._dist.parsed_version:
                    raise AssertionError('Version mismatch: {!r} vs {!r}'.format(self._version, self._dist.parsed_version))

    @property
    def dist(self):
        self._prepare()
        return self._dist

    def _get_requires_python_specifier(self):
        requires_python = get_requires_python(self.dist)
        if requires_python is None:
            return
        try:
            spec = SpecifierSet(requires_python)
        except InvalidSpecifier as e:
            try:
                logger.warning('Package %r has an invalid Requires-Python: %s', self.name, e)
                return
            finally:
                e = None
                del e

        return spec

    def get_dependencies(self):
        deps = [self._factory.make_requirement_from_spec(str(r), self._ireq) for r in self.dist.requires()]
        python_dep = self._factory.make_requires_python_requirement(self._get_requires_python_specifier())
        if python_dep:
            deps.append(python_dep)
        return deps

    def get_install_requirement(self):
        self._prepare()
        return self._ireq


class LinkCandidate(_InstallRequirementBackedCandidate):

    def __init__(self, link, parent, factory, name=None, version=None):
        super(LinkCandidate, self).__init__(link=link,
          ireq=(make_install_req_from_link(link, parent)),
          factory=factory,
          name=name,
          version=version)

    def _prepare_abstract_distribution(self):
        return self._factory.preparer.prepare_linked_requirement(self._ireq)


class EditableCandidate(_InstallRequirementBackedCandidate):

    def __init__(self, link, parent, factory, name=None, version=None):
        super(EditableCandidate, self).__init__(link=link,
          ireq=(make_install_req_from_editable(link, parent)),
          factory=factory,
          name=name,
          version=version)

    def _prepare_abstract_distribution(self):
        return self._factory.preparer.prepare_editable_requirement(self._ireq)


class AlreadyInstalledCandidate(Candidate):

    def __init__(self, dist, parent, factory):
        self.dist = dist
        self._ireq = make_install_req_from_dist(dist, parent)
        self._factory = factory
        skip_reason = 'already satisfied'
        factory.preparer.prepare_installed_requirement(self._ireq, skip_reason)

    def __repr__(self):
        return '{class_name}({distribution!r})'.format(class_name=(self.__class__.__name__),
          distribution=(self.dist))

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.name == other.name and self.version == other.version
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    @property
    def name(self):
        return canonicalize_name(self.dist.project_name)

    @property
    def version(self):
        return self.dist.parsed_version

    def get_dependencies(self):
        return [self._factory.make_requirement_from_spec(str(r), self._ireq) for r in self.dist.requires()]

    def get_install_requirement(self):
        pass


class ExtrasCandidate(Candidate):
    __doc__ = 'A candidate that has \'extras\', indicating additional dependencies.\n\n    Requirements can be for a project with dependencies, something like\n    foo[extra].  The extras don\'t affect the project/version being installed\n    directly, but indicate that we need additional dependencies. We model that\n    by having an artificial ExtrasCandidate that wraps the "base" candidate.\n\n    The ExtrasCandidate differs from the base in the following ways:\n\n    1. It has a unique name, of the form foo[extra]. This causes the resolver\n       to treat it as a separate node in the dependency graph.\n    2. When we\'re getting the candidate\'s dependencies,\n       a) We specify that we want the extra dependencies as well.\n       b) We add a dependency on the base candidate (matching the name and\n          version).  See below for why this is needed.\n    3. We return None for the underlying InstallRequirement, as the base\n       candidate will provide it, and we don\'t want to end up with duplicates.\n\n    The dependency on the base candidate is needed so that the resolver can\'t\n    decide that it should recommend foo[extra1] version 1.0 and foo[extra2]\n    version 2.0. Having those candidates depend on foo=1.0 and foo=2.0\n    respectively forces the resolver to recognise that this is a conflict.\n    '

    def __init__(self, base, extras):
        self.base = base
        self.extras = extras

    def __repr__(self):
        return '{class_name}(base={base!r}, extras={extras!r})'.format(class_name=(self.__class__.__name__),
          base=(self.base),
          extras=(self.extras))

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.base == other.base and self.extras == other.extras
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    @property
    def name(self):
        """The normalised name of the project the candidate refers to"""
        return format_name(self.base.name, self.extras)

    @property
    def version(self):
        return self.base.version

    def get_dependencies(self):
        factory = self.base._factory
        valid_extras = self.extras.intersection(self.base.dist.extras)
        invalid_extras = self.extras.difference(self.base.dist.extras)
        if invalid_extras:
            logger.warning('Invalid extras specified in %s: %s', self.name, ','.join(sorted(invalid_extras)))
        deps = [factory.make_requirement_from_spec(str(r), self.base._ireq) for r in self.base.dist.requires(valid_extras)]
        spec = '{}=={}'.format(self.base.name, self.base.version)
        deps.append(factory.make_requirement_from_spec(spec, self.base._ireq))
        return deps

    def get_install_requirement(self):
        pass


class RequiresPythonCandidate(Candidate):

    def __init__(self, py_version_info):
        if py_version_info is not None:
            version_info = normalize_version_info(py_version_info)
        else:
            version_info = sys.version_info[:3]
        self._version = Version('.'.join((str(c) for c in version_info)))

    @property
    def name(self):
        return '<Python fom Requires-Python>'

    @property
    def version(self):
        return self._version

    def get_dependencies(self):
        return []

    def get_install_requirement(self):
        pass