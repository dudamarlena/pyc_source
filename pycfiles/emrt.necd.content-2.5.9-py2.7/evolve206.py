# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/emrt/necd/content/upgrades/evolve206.py
# Compiled at: 2019-02-15 13:51:23
from functools import partial
from operator import itemgetter
import plone.api as api
from emrt.necd.content.constants import ROLE_SE
PRINCIPAL = itemgetter(0)
ROLES = itemgetter(1)

def run(_):
    catalog = api.portal.get_tool('portal_catalog')
    review_folders = [ brain.getObject() for brain in catalog(portal_type='ReviewFolder') ]
    for folder in review_folders:
        update_localroles(folder)
        folder.reindexObject()


def update_localroles(context):
    """ Recursively update local roles """
    map(update_localroles, context.objectValues())
    new_roles = map(updated_roles, context.get_local_roles())
    for principal, roles in new_roles:
        context.manage_setLocalRoles(principal, roles)


def updated_roles(entry):
    """ Rename 'NECDReviewer' to ROLE_SE """

    def rename(src, dest, item):
        if item == src:
            return dest
        return item

    necdrev_to_se = partial(rename, 'NECDReviewer', ROLE_SE)
    new_roles = tuple(set(map(necdrev_to_se, ROLES(entry))))
    return (PRINCIPAL(entry), new_roles)