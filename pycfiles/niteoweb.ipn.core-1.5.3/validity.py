# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/matej/workarea/nw1/niteoweb.ipn.core/src/niteoweb/ipn/core/validity.py
# Compiled at: 2013-10-03 07:39:59
"""View for finding expired members and disabling them."""
from DateTime import DateTime
from five import grok
from niteoweb.ipn.core import DISABLED
from niteoweb.ipn.core.interfaces import IIPN
from plone import api
from Products.CMFCore.interfaces import ISiteRoot
from zope.component import getAdapter
import logging, transaction
logger = logging.getLogger('niteoweb.ipn.core')

class Validity(grok.View):
    """Find members with expired validity and disable them."""
    grok.context(ISiteRoot)
    grok.require('zope2.View')

    def render(self):
        """Check for expired members and disable them."""
        messages = [
         'START validity check.']
        secret = api.portal.get_registry_record('niteoweb.ipn.core.validity.secret')
        if self.request.get('secret') != secret:
            return 'Wrong secret. Please configure it in control panel.'
        ipn = getAdapter(self.context, IIPN)
        now = DateTime()
        for member in api.user.get_users():
            if DISABLED in [ g.id for g in api.group.get_groups(user=member) ]:
                continue
            valid_to = member.getProperty('valid_to')
            if valid_to < now:
                messages.append("Disabling member '%s' (%s)." % (
                 member.id, valid_to.strftime('%Y/%m/%d')))
                if not self.request.get('dry-run'):
                    ipn.disable_member(email=member.id, product_id=member.getProperty('product_id'), trans_type='cronjob')
                    transaction.commit()

        return ('\n').join(messages)