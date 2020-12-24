# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/matej/workarea/nw1/niteoweb.ipn.core/src/niteoweb/ipn/core/ipn.py
# Compiled at: 2014-03-07 04:17:27
"""Module providing IPN actions."""
from DateTime import DateTime
from five import grok
from niteoweb.ipn.core import DISABLED
from niteoweb.ipn.core import PGI
from niteoweb.ipn.core.interfaces import IIPN
from niteoweb.ipn.core.interfaces import MemberDisabledEvent
from niteoweb.ipn.core.interfaces import MemberEnabledEvent
from niteoweb.ipn.core.interfaces import MissingParamError
from niteoweb.ipn.core.interfaces import InvalidParamValueError
from plone import api
from Products.CMFCore.interfaces import ISiteRoot
from zope.event import notify
import logging
logger = logging.getLogger('niteoweb.ipn.core')

class IPN(grok.MultiAdapter):
    """IPN actions."""
    grok.adapts(ISiteRoot)
    grok.implements(IIPN)

    def __init__(self, context):
        """Initialize the IPN portal adapter.

        :param context: Portal object.
        """
        self.context = context

    def enable_member(self, email=None, product_id=None, trans_type=None, fullname=None, affiliate=None, note=''):
        """Enable an existing or create a new member.

        :param email: Email of the member, also used as username.
        :type email: string
        :param product_id: ID of product that Member has purchased.
        :type product_id: string
        :param trans_type: Type of transaction that occurred.
        :type trans_type: string
        :param fullname: Member's fullname, required only when creating a new
            member.
        :type fullname: string
        :param affiliate: Member's affiliate, needed only when creating a new
            member.
        :type affiliate: string

        :returns: None

        """
        logger.info(("{0}: START enable_member:{1} for '{2}'.").format(api.user.get_current(), trans_type, email))
        if not email:
            raise MissingParamError("Parameter 'email' is missing.")
        if not product_id:
            raise MissingParamError("Parameter 'product_id' is missing.")
        if not trans_type:
            raise MissingParamError("Parameter 'trans_type' is missing.")
        product_group = api.group.get(groupname=PGI % product_id)
        if not product_group:
            raise InvalidParamValueError("Could not find group with id '%s'." % product_id)
        if not api.user.get(username=email):
            if not fullname:
                raise MissingParamError("Parameter 'fullname' is needed to create a new member.")
            if not affiliate:
                raise MissingParamError("Parameter 'affiliate' is needed to create a new member.")
            logger.info(('{0}: Creating a new member: {1}').format(api.user.get_current(), email))
            properties = dict(product_id=product_id, fullname=fullname, affiliate=affiliate)
            api.user.create(email=email, properties=properties)
        member = api.user.get(username=email)
        if DISABLED in [ g.id for g in api.group.get_groups(user=member) ]:
            logger.info(("{0}: Removing member '{1}' from Disabled group.").format(api.user.get_current(), member.id))
            api.group.remove_user(groupname=DISABLED, user=member)
        if 'Member' not in api.user.get_roles(user=member):
            logger.info(("{0}: Granting member '{1}' the Member role.").format(api.user.get_current(), member.id))
            api.user.grant_roles(user=member, roles=['Member'])
        if product_group not in api.group.get_groups(user=member):
            api.group.add_user(user=member, group=product_group)
            logger.info(("{0}: Added member '{1}' to product group '{2}'.").format(api.user.get_current(), member.id, product_group))
        member.setMemberProperties(mapping={'product_id': product_id})
        product_validity = int(product_group.getProperty('validity'))
        if product_validity < 1:
            raise InvalidParamValueError("Validity for group '%s' is not a positive integer: %i" % (
             product_group.id, product_validity))
        valid_to = DateTime() + product_validity
        member.setMemberProperties(mapping={'valid_to': valid_to})
        logger.info(("{0}: Member's ({1}) valid_to date set to {2}.").format(api.user.get_current(), member.id, valid_to.strftime('%Y/%m/%d')))
        self._add_to_member_history(member, ('{timestamp}|{action}|{product_id}|{ttype}|{note}').format(timestamp=DateTime().strftime('%Y/%m/%d %H:%M:%S'), product_id=product_id, ttype=trans_type, action='enable_member', note=note))
        notify(MemberEnabledEvent(member.id))
        logger.info(("{0}: END enable_member:{1} for '{2}'.").format(api.user.get_current(), trans_type, email))

    def disable_member(self, email=None, product_id=None, trans_type=None, **kwargs):
        """Disable an existing member.

        :param email: Email of the member, also used as username.
        :type email: string
        :param product_id: ID of product that Member has purchased.
        :type product_id: string
        :param trans_type: Type of transaction that occurred.
        :type trans_type: string

        :returns: None

        """
        logger.info(("{0}: START disable_member:{1} for '{2}'.").format(api.user.get_current(), trans_type, email))
        note = ''
        if not email:
            raise MissingParamError("Parameter 'email' is missing.")
        if not trans_type:
            raise MissingParamError("Parameter 'trans_type' is missing.")
        member = api.user.get(username=email)
        if not member:
            raise InvalidParamValueError("Cannot disable a nonexistent member: '%s'." % email)
        if member not in api.user.get_users(groupname=DISABLED):
            logger.info(("{0}: Adding member '{1}' to Disabled group.").format(api.user.get_current(), member.id))
            api.group.add_user(groupname=DISABLED, user=member)
        other_groups = [ g for g in api.group.get_groups(user=member) if g.id not in [DISABLED, 'AuthenticatedUsers']
                       ]
        if other_groups:
            note = 'removed from groups: '
            for group in other_groups:
                logger.info(("{0}: Removing member '{1}' from group '{2}'.").format(api.user.get_current(), member.id, group.id))
                api.group.remove_user(group=group, user=member)
                note += '%s, ' % group.id

        if 'Member' in api.user.get_roles(user=member):
            logger.info(("{0}: Revoking member '{1}' the Member role.").format(api.user.get_current(), member.id))
            api.user.revoke_roles(user=member, roles=['Member'])
        self._add_to_member_history(member, ('{timestamp}|{action}|{product_id}|{ttype}|{note}').format(timestamp=DateTime().strftime('%Y/%m/%d %H:%M:%S'), product_id=product_id, ttype=trans_type, action='disable_member', note=note))
        notify(MemberDisabledEvent(member.id))
        logger.info(("{0}: END disable_member:{1} for '{2}'.").format(api.user.get_current(), trans_type, email))

    def _add_to_member_history(self, member, msg):
        """Add a record to member's history.

        :param msg: Message to add to member's history
        :type msg: string

        :returns: None

        """
        history = list(member.getProperty('history'))
        history.append(msg)
        member.setMemberProperties(mapping={'history': history})