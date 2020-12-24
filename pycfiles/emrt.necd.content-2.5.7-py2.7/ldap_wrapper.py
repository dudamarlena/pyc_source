# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/emrt/necd/content/utilities/ldap_wrapper.py
# Compiled at: 2019-02-15 13:51:23
from emrt.necd.content.constants import LDAP_BASE
from emrt.necd.content.constants import LDAP_BASE_PROJECTION

def ldap_projection(ldap_const):
    return ldap_const.format(base_dn=LDAP_BASE_PROJECTION)


def ldap_inventory(ldap_const):
    return ldap_const.format(base_dn=LDAP_BASE)


class GetLDAPWrapper(object):

    def __call__(self, context):
        if context.type == 'projection':
            return ldap_projection
        else:
            return ldap_inventory