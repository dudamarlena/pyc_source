# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-aejasjrz/pip/pip/_internal/resolution/resolvelib/factory.py
# Compiled at: 2020-05-05 12:41:47
# Size of source mod 2**32: 7574 bytes
from pip._vendor.packaging.utils import canonicalize_name
from pip._internal.exceptions import InstallationError, UnsupportedPythonVersion
from pip._internal.utils.misc import get_installed_distributions
from pip._internal.utils.typing import MYPY_CHECK_RUNNING
from .candidates import AlreadyInstalledCandidate, EditableCandidate, ExtrasCandidate, LinkCandidate, RequiresPythonCandidate
from .requirements import ExplicitRequirement, RequiresPythonRequirement, SpecifierRequirement
if MYPY_CHECK_RUNNING:
    from typing import Dict, Iterator, Optional, Set, Tuple, TypeVar
    from pip._vendor.packaging.specifiers import SpecifierSet
    from pip._vendor.packaging.version import _BaseVersion
    from pip._vendor.pkg_resources import Distribution
    from pip._vendor.resolvelib import ResolutionImpossible
    from pip._internal.index.package_finder import PackageFinder
    from pip._internal.models.link import Link
    from pip._internal.operations.prepare import RequirementPreparer
    from pip._internal.req.req_install import InstallRequirement
    from pip._internal.resolution.base import InstallRequirementProvider
    from .base import Candidate, Requirement
    from .candidates import BaseCandidate
    C = TypeVar('C')
    Cache = Dict[(Link, C)]

class Factory(object):

    def __init__(self, finder, preparer, make_install_req, force_reinstall, ignore_installed, ignore_requires_python, py_version_info=None):
        self.finder = finder
        self.preparer = preparer
        self._python_candidate = RequiresPythonCandidate(py_version_info)
        self._make_install_req_from_spec = make_install_req
        self._force_reinstall = force_reinstall
        self._ignore_requires_python = ignore_requires_python
        self._link_candidate_cache = {}
        self._editable_candidate_cache = {}
        if not ignore_installed:
            self._installed_dists = {canonicalize_name(dist.project_name):dist for dist in get_installed_distributions()}
        else:
            self._installed_dists = {}

    def _make_candidate_from_dist(self, dist, extras, parent):
        base = AlreadyInstalledCandidate(dist, parent, factory=self)
        if extras:
            return ExtrasCandidate(base, extras)
        return base

    def _make_candidate_from_link(self, link, extras, parent, name=None, version=None):
        if parent.editable:
            if link not in self._editable_candidate_cache:
                self._editable_candidate_cache[link] = EditableCandidate(link,
                  parent, factory=self, name=name, version=version)
            base = self._editable_candidate_cache[link]
        else:
            if link not in self._link_candidate_cache:
                self._link_candidate_cache[link] = LinkCandidate(link,
                  parent, factory=self, name=name, version=version)
            base = self._link_candidate_cache[link]
        if extras:
            return ExtrasCandidate(base, extras)
        return base

    def iter_found_candidates(self, ireq, extras):
        name = canonicalize_name(ireq.req.name)
        if not self._force_reinstall:
            installed_dist = self._installed_dists.get(name)
        else:
            installed_dist = None
        found = self.finder.find_best_candidate(project_name=(ireq.req.name),
          specifier=(ireq.req.specifier),
          hashes=ireq.hashes(trust_internet=False))
        for ican in found.iter_applicable():
            if installed_dist is not None:
                if installed_dist.parsed_version == ican.version:
                    continue
            yield self._make_candidate_from_link(link=(ican.link),
              extras=extras,
              parent=ireq,
              name=name,
              version=(ican.version))

        if installed_dist is not None:
            if installed_dist.parsed_version in ireq.req.specifier:
                yield self._make_candidate_from_dist(dist=installed_dist,
                  extras=extras,
                  parent=ireq)

    def make_requirement_from_install_req(self, ireq):
        if ireq.link:
            cand = self._make_candidate_from_link((ireq.link),
              extras=(set()), parent=ireq)
            return ExplicitRequirement(cand)
        return SpecifierRequirement(ireq, factory=self)

    def make_requirement_from_spec(self, specifier, comes_from):
        ireq = self._make_install_req_from_spec(specifier, comes_from)
        return self.make_requirement_from_install_req(ireq)

    def make_requires_python_requirement(self, specifier):
        if self._ignore_requires_python or specifier is None:
            return
        return RequiresPythonRequirement(specifier, self._python_candidate)

    def should_reinstall(self, candidate):
        return candidate.name in self._installed_dists

    def _report_requires_python_error(self, requirement, parent):
        template = 'Package {package!r} requires a different Python: {version} not in {specifier!r}'
        message = template.format(package=(parent.name),
          version=(self._python_candidate.version),
          specifier=(str(requirement.specifier)))
        return UnsupportedPythonVersion(message)

    def get_installation_error(self, e):
        for cause in e.causes:
            if isinstance(cause.requirement, RequiresPythonRequirement):
                return self._report_requires_python_error(cause.requirement, cause.parent)