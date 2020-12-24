# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/emrt/necd/content/upgrades/evolve207.py
# Compiled at: 2019-02-15 13:51:23
from functools import partial
from operator import attrgetter
import plone.api as api
from emrt.necd.content import utils
from emrt.necd.content import constants
COUNTRY = attrgetter('country')
APPEND_MINUS = partial(utils.append_string, '-')
COUNTRY_MSE = partial(APPEND_MINUS, constants.LDAP_MSEXPERT)

def set_role(rolename, principal):
    return (
     principal, (rolename,))


def run(_):
    catalog = api.portal.get_tool('portal_catalog')
    review_folders = [ brain.getObject() for brain in catalog(portal_type='ReviewFolder')
                     ]
    for folder in review_folders:
        update_localroles(folder)
        folder.reindexObject()


def update_localroles(context):
    """ Set local roles for reviewfolder.
        The MSE-country LDAP groups don't have anything assigned
        so this time we can be greedy and not check existing roles.
    """
    observations = context.objectValues()
    countries = tuple(set(map(COUNTRY, observations)))
    roles_to_map = tuple(map(COUNTRY_MSE, countries))
    set_mse_role = partial(set_role, constants.ROLE_MSE)
    local_roles = tuple(map(set_mse_role, roles_to_map))
    for principal, roles in local_roles:
        context.manage_setLocalRoles(principal, roles)