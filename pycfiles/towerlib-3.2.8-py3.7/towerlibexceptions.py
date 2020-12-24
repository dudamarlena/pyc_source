# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ctyfoxylos/SBP/python/towerlib/towerlib/towerlibexceptions.py
# Compiled at: 2018-07-25 09:48:50
"""
Custom exception code for towerlib

.. _Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html

"""
__author__ = 'Costas Tyfoxylos <ctyfoxylos@schubergphilis.com>'
__docformat__ = 'google'
__date__ = '2018-01-02'
__copyright__ = 'Copyright 2018, Costas Tyfoxylos'
__credits__ = ['Costas Tyfoxylos']
__license__ = 'MIT'
__maintainer__ = 'Costas Tyfoxylos'
__email__ = '<ctyfoxylos@schubergphilis.com>'
__status__ = 'Development'

class AuthFailed(Exception):
    """The token retirieval failed"""
    pass


class InvalidUserLevel(Exception):
    """The value provided is not allowed.

    Valid values ('standard', 'system_auditor', 'system_administrator')
    """
    pass


class InvalidOrganization(Exception):
    """The organization provided is not a valid organization"""
    pass


class InvalidVariables(Exception):
    """The variables are not valid json"""
    pass


class InvalidInventory(Exception):
    """The inventory provided is invalid"""
    pass


class InvalidCredentialType(Exception):
    """The credential type provided is invalid."""
    pass


class InvalidCredentialTypeKind(Exception):
    """The credential type kind provided is invalid.

    Valid values (u'scm', u'ssh', u'vault', u'net', u'cloud', u'insights')
    """
    pass


class InvalidUser(Exception):
    """The user provided is invalid"""
    pass


class InvalidTeam(Exception):
    """The team provided is invalid"""
    pass


class InvalidCredential(Exception):
    """The credential provided is invalid."""
    pass


class InvalidGroup(Exception):
    """The group provided is invalid."""
    pass


class InvalidHost(Exception):
    """The host provided is invalid."""
    pass


class InvalidProject(Exception):
    """The project provided is not valid"""
    pass


class InvalidJobType(Exception):
    """The job type provided is not valid. Valid values (u'run', u'check')"""
    pass


class InvalidPlaybook(Exception):
    """The playbook specified does not exist in the project"""
    pass


class InvalidInstanceGroup(Exception):
    """The instance group provided does not exist"""
    pass


class InvalidVerbosity(Exception):
    """The verbosity level provided is not valid. Valid values (0, 1, 2, 3, 4)"""
    pass


class InvalidJobTemplate(Exception):
    """The job template provided is not valid."""
    pass


class PermissionNotFound(Exception):
    """The premission was not found in the entity"""
    pass