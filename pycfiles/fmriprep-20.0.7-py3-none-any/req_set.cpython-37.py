# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-vxs8l7gu/pip/pip/_internal/req/req_set.py
# Compiled at: 2020-05-05 12:41:36
# Size of source mod 2**32: 7792 bytes
from __future__ import absolute_import
import logging
from collections import OrderedDict
from pip._vendor.packaging.utils import canonicalize_name
from pip._internal.exceptions import InstallationError
from pip._internal.models.wheel import Wheel
from pip._internal.utils import compatibility_tags
from pip._internal.utils.typing import MYPY_CHECK_RUNNING
if MYPY_CHECK_RUNNING:
    from typing import Dict, Iterable, List, Optional, Tuple
    from pip._internal.req.req_install import InstallRequirement
logger = logging.getLogger(__name__)

class RequirementSet(object):

    def __init__(self, check_supported_wheels=True):
        """Create a RequirementSet.
        """
        self.requirements = OrderedDict()
        self.check_supported_wheels = check_supported_wheels
        self.unnamed_requirements = []

    def __str__(self):
        requirements = sorted((req for req in self.requirements.values() if not req.comes_from),
          key=(lambda req: canonicalize_name(req.name)))
        return ' '.join((str(req.req) for req in requirements))

    def __repr__(self):
        requirements = sorted((self.requirements.values()),
          key=(lambda req: canonicalize_name(req.name)))
        format_string = '<{classname} object; {count} requirement(s): {reqs}>'
        return format_string.format(classname=(self.__class__.__name__),
          count=(len(requirements)),
          reqs=(', '.join((str(req.req) for req in requirements))))

    def add_unnamed_requirement(self, install_req):
        assert not install_req.name
        self.unnamed_requirements.append(install_req)

    def add_named_requirement(self, install_req):
        assert install_req.name
        project_name = canonicalize_name(install_req.name)
        self.requirements[project_name] = install_req

    def add_requirement(self, install_req, parent_req_name=None, extras_requested=None):
        """Add install_req as a requirement to install.

        :param parent_req_name: The name of the requirement that needed this
            added. The name is used because when multiple unnamed requirements
            resolve to the same name, we could otherwise end up with dependency
            links that point outside the Requirements set. parent_req must
            already be added. Note that None implies that this is a user
            supplied requirement, vs an inferred one.
        :param extras_requested: an iterable of extras used to evaluate the
            environment markers.
        :return: Additional requirements to scan. That is either [] if
            the requirement is not applicable, or [install_req] if the
            requirement is applicable and has just been added.
        """
        if not install_req.match_markers(extras_requested):
            logger.info("Ignoring %s: markers '%s' don't match your environment", install_req.name, install_req.markers)
            return ([], None)
            if install_req.link:
                if install_req.link.is_wheel:
                    wheel = Wheel(install_req.link.filename)
                    tags = compatibility_tags.get_supported()
                    if self.check_supported_wheels:
                        if not wheel.supported(tags):
                            raise InstallationError('{} is not a supported wheel on this platform.'.format(wheel.filename))
            assert install_req.is_direct == (parent_req_name is None), "a direct req shouldn't have a parent and also, a non direct req should have a parent"
            if not install_req.name:
                self.add_unnamed_requirement(install_req)
                return ([install_req], None)
        else:
            try:
                existing_req = self.get_requirement(install_req.name)
            except KeyError:
                existing_req = None

            has_conflicting_requirement = parent_req_name is None and existing_req and not existing_req.constraint and existing_req.extras == install_req.extras and existing_req.req.specifier != install_req.req.specifier
            if has_conflicting_requirement:
                raise InstallationError('Double requirement given: {} (already in {}, name={!r})'.format(install_req, existing_req, install_req.name))
            if not existing_req:
                self.add_named_requirement(install_req)
                return (
                 [
                  install_req], install_req)
            return install_req.constraint or existing_req.constraint or ([], existing_req)
        does_not_satisfy_constraint = install_req.link and not (existing_req.link and install_req.link.path == existing_req.link.path)
        if does_not_satisfy_constraint:
            raise InstallationError("Could not satisfy constraints for '{}': installation from path or url cannot be constrained to a version".format(install_req.name))
        existing_req.constraint = False
        existing_req.extras = tuple(sorted(set(existing_req.extras) | set(install_req.extras)))
        logger.debug('Setting %s extras to: %s', existing_req, existing_req.extras)
        return (
         [
          existing_req], existing_req)

    def has_requirement(self, name):
        project_name = canonicalize_name(name)
        return project_name in self.requirements and not self.requirements[project_name].constraint

    def get_requirement(self, name):
        project_name = canonicalize_name(name)
        if project_name in self.requirements:
            return self.requirements[project_name]
        raise KeyError(('No project with the name {name!r}'.format)(**locals()))

    @property
    def all_requirements(self):
        return self.unnamed_requirements + list(self.requirements.values())