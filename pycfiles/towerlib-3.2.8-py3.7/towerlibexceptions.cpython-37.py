# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ctyfoxylos/SBP/python/towerlib/towerlib/towerlibexceptions.py
# Compiled at: 2019-10-18 06:12:55
# Size of source mod 2**32: 3541 bytes
"""
Custom exception code for towerlib.

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
    __doc__ = 'The token retrieval failed.'


class InvalidUserLevel(Exception):
    __doc__ = "The value provided is not allowed.\n\n    Valid values ('standard', 'system_auditor', 'system_administrator')\n    "


class InvalidOrganization(Exception):
    __doc__ = 'The organization provided is not a valid organization.'


class InvalidVariables(Exception):
    __doc__ = 'The variables are not valid json.'


class InvalidInventory(Exception):
    __doc__ = 'The inventory provided is invalid.'


class InvalidCredentialType(Exception):
    __doc__ = 'The credential type provided is invalid.'


class InvalidUser(Exception):
    __doc__ = 'The user provided is invalid.'


class InvalidTeam(Exception):
    __doc__ = 'The team provided is invalid.'


class InvalidCredential(Exception):
    __doc__ = 'The credential provided is invalid.'


class InvalidGroup(Exception):
    __doc__ = 'The group provided is invalid.'


class InvalidHost(Exception):
    __doc__ = 'The host provided is invalid.'


class InvalidProject(Exception):
    __doc__ = 'The project provided is not valid.'


class InvalidJobType(Exception):
    __doc__ = "The job type provided is not valid. Valid values (u'run', u'check')."


class InvalidPlaybook(Exception):
    __doc__ = 'The playbook specified does not exist in the project.'


class InvalidInstanceGroup(Exception):
    __doc__ = 'The instance group provided does not exist.'


class InvalidVerbosity(Exception):
    __doc__ = 'The verbosity level provided is not valid. Valid values (0, 1, 2, 3, 4).'


class InvalidJobTemplate(Exception):
    __doc__ = 'The job template provided is not valid.'


class PermissionNotFound(Exception):
    __doc__ = 'The permission was not found in the entity.'


class InvalidValue(Exception):
    __doc__ = 'The value is not valid for the field.'


class InvalidRole(Exception):
    __doc__ = 'The role is not valid for this organization.'