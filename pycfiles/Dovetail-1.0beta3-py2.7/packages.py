# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.8-intel/egg/dovetail/directives/packages.py
# Compiled at: 2012-08-01 03:51:57
"""Directives for package/egg requirements and resolution"""
from setuptools.command import easy_install
from pkg_resources import working_set, parse_requirements, VersionConflict
from dovetail.model import TaskWrapper
from dovetail.util import Logger, MissingRequirement, pp_exception

def pp_requirements(requirements):
    """Pretty-print a list of requirements.

    :param requirements: Requirements in the form "pylint" or "coverage>3"
    :type  requirements: list of string
    :rtype: string
    """
    return (', ').join(requirements)


def not_present(requirements, stop_on_error=True):
    """Checks to see which requirements are currently satisfied, returning a list of
    those requirements not satisfied.

    :param requirements: Requirements in the form "pylint" or "coverage>3"
    :type  requirements: list of string
    :param stop_on_error: Default True; if True, if :exc:`pkg_resources.VersionConflict`
                          is raised, this is propagated to the caller. Otherwise the
                          exception is handled.
    :type  stop_on_error: boolean
    :return: A list of unsatisfied requirements - may be empty
    :rtype: list of string
    :raises: :exc:`pkg_resources.VersionConflict` if a requirement is in conflict with the
             environment"""
    result = []
    for requirement in requirements:
        for parsed in parse_requirements(requirement):
            try:
                match = working_set.find(parsed)
                if match is None:
                    Logger.debug(('Missing {0}').format(requirement))
                    result.append(requirement)
                else:
                    Logger.debug(('Requirement {0} is present').format(requirement))
            except VersionConflict:
                Logger.major(('Requirement {0} is in conflict with existing packages - aborting').format(requirement))
                if stop_on_error:
                    raise
                else:
                    result.append(requirement)

    return result


def install(requirements):
    """Uses :mod:`setuptools.commands.easy_install` to install a series of
    package requirements and adjust the system path so they are
    immediately available.

    :param requirements: Requirement specifications as per :program:`easy_install`,
                         eg: "pylint" and "coverage>3"
    :type  requirements: *Either* a string *or* a list of string
    :raises: :exc:`dovetail.util.MissingRequirement` if :program:`easy_install`
             cannot locate or install the requirement

    .. note::

        If you need to set specific :program:`easy_install` behaviour, such as
        loading from a local host, then modify the :program:`easy_install`
        configuration as described in:

        * http://packages.python.org/distribute/easy_install.html#configuration-files
    """
    if isinstance(requirements, basestring):
        requirements = [requirements]
    from pkg_resources import require
    Logger.major(('Installing requirements: {0}').format((' ').join(requirements)))
    for requirement in requirements:
        Logger.major(('  Running: easy_install {0}').format(requirement))
        try:
            easy_install.main([requirement])
        except BaseException as exception:
            raise MissingRequirement(('easy_install could not locate or install {0}: {1}').format(requirement, pp_exception(exception)))

        Logger.log(('  Ensuring {0} is on the system path').format(requirement))
        require(requirement)


def requires(*requirements):
    """Ensures all package requirements are installed before executing Task.

    :param requirements: One or more requirement specifications as per
                         :program:`easy_install`, eg: "pylint" and "coverage>3"
    :type  requirements: string
    :raises: :exc:`dovetail.util.exception.MissingRequirement` if
             :program:`easy_install` cannot locate or install the requirement
    :raises: :exc:`pkg_resources.VersionConflict` if a requirement is in
             conflict with the current environment.=

    .. note::

        If you need to set specific :program:`easy_install` behaviour, such as
        loading from a local host, then modify the :program:`easy_install`
        configuration as described in:

        * http://packages.python.org/distribute/easy_install.html#configuration-files
    """

    def before(execution):
        missing = not_present(requirements)
        if missing:
            Logger.major(('@requires: Going to attempt to install the following requirements: {0}').format(pp_requirements(missing)))
            install(missing)
        else:
            Logger.log(('@requires: Requirements met: {0}').format(pp_requirements(requirements)))

    return TaskWrapper.decorator_maker('@requires', before=before)


class Installed(object):
    """A predicate that returns True if all requirements are met in the Python
    environment.

    :param requirement: A requirement specifications as per
                        :program:`easy_install`, eg: "pylint" and "coverage>3"
    :type  requirement: string
    :param requirements: Additional requirements (optional)
    :type  requirements: string
    :return: True if all specified requirements are satisfied
    :rtype:  boolean
    """

    def __init__(self, requirement, *requirements):
        if requirements is None or len(requirements) == 0:
            self.requirements = [
             requirement]
        else:
            self.requirements = list(requirements)
            self.requirements.insert(0, requirement)
        return

    def __call__(self):
        missing = not_present(self.requirements, stop_on_error=False)
        if len(missing) > 0:
            Logger.log(('Installed: missing requirements: {0}').format(pp_requirements(missing)))
            return False
        else:
            Logger.debug(('Installed: all requirements met: {0}').format(pp_requirements(self.requirements)))
            return True

    def __str__(self):
        return ('Installed({0})').format(pp_requirements(self.requirements))