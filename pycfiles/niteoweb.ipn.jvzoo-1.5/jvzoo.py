# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/matej/workarea/nw1/niteoweb.ipn.jvzoo/src/niteoweb/ipn/jvzoo/jvzoo.py
# Compiled at: 2013-12-19 07:23:47
"""The @@jvzoo view that handles JVZoo purchase notifications."""
from five import grok
from niteoweb.ipn.core.interfaces import IIPN
from niteoweb.ipn.jvzoo.interfaces import SecretKeyNotSet
from niteoweb.ipn.jvzoo.interfaces import UnknownTransactionType
from plone import api
from Products.CMFCore.interfaces import ISiteRoot
from zope.component import getAdapter
import transaction, hashlib, logging
logger = logging.getLogger('niteoweb.ipn.jvzoo')

class JVZoo(grok.View):
    """A view for handling IPN POST requests from JVZOO."""
    grok.context(ISiteRoot)
    grok.require('zope2.View')
    TYPES_TO_ACTIONS = {'SALE': 'enable_member', 
       'BILL': 'enable_member', 
       'RFND': 'disable_member', 
       'CGBK': 'disable_member', 
       'INSF': 'disable_member', 
       'CANCEL-REBILL': 'disable_member', 
       'UNCANCEL-REBILL': 'enable_member'}

    def render(self):
        """Handler for JVZoo IPN POST requests."""
        if not self.request.form:
            msg = 'No POST request.'
            logger.warning(('{0}: {1}').format(api.user.get_current(), msg))
            return msg
        params = dict(self.request.form)
        params['secretkey'] = api.portal.get_registry_record('niteoweb.ipn.jvzoo.interfaces.IJVZooSettings.secretkey')
        try:
            self._verify_POST(params)
            data = self._parse_POST(params)
            user = self.get_user_by_email(data['email'])
            if user:
                username = user.getUserName()
            else:
                username = data['email']
            logger.info(("{0}: POST successfully parsed for '{1}'.").format(api.user.get_current(), username))
            ipn = getAdapter(self.context, IIPN)
            trans_type = data['trans_type']
            if trans_type in self.TYPES_TO_ACTIONS:
                action = self.TYPES_TO_ACTIONS[trans_type]
                logger.info(("{0}: Calling '{1}' in niteoweb.ipn.core.").format(api.user.get_current(), action))
                params = {'email': username, 
                   'product_id': data['product_id'], 
                   'trans_type': data['trans_type'], 
                   'fullname': data.get('fullname'), 
                   'affiliate': data.get('affiliate')}
                getattr(ipn, action)(**params)
            else:
                raise UnknownTransactionType("Unknown Transaction Type '%s'." % trans_type)
        except KeyError as ex:
            msg = 'POST parameter missing: %s' % ex
            logger.warning(('{0}: {1}').format(api.user.get_current(), msg))
            transaction.abort()
            return msg
        except AssertionError:
            msg = 'Checksum verification failed.'
            logger.warning(('{0}: {1}').format(api.user.get_current(), msg))
            transaction.abort()
            return msg
        except Exception as ex:
            msg = 'POST handling failed: %s' % ex
            logger.warning(('{0}: {1}').format(api.user.get_current(), msg))
            transaction.abort()
            return msg

        return 'Done.'

    def _verify_POST(self, params):
        """Verifies if received POST is a valid JVZoo POST request.

        :param params: POST parameters sent by JVZoo Notification Service
        :type params: dict

        """
        if not params['secretkey']:
            raise SecretKeyNotSet('JVZoo secret-key is not set.')
        strparams = ''
        for key in iter(sorted(params.iterkeys())):
            if key in ('cverify', 'secretkey'):
                continue
            strparams += unicode(params[key] + '|', 'utf-8')

        strparams += params['secretkey']
        sha = hashlib.sha1(strparams.encode('utf-8')).hexdigest().upper()
        assert params['cverify'] == sha[:8], 'Checksum verification failed.'

    def _parse_POST(self, params):
        """Parse POST from JVZoo and extract information we need.

        :param params: POST parameters sent by JVZoo Notification Service
        :type params: dict

        """
        return {'email': params['ccustemail'], 
           'fullname': '%s' % params['ccustname'].decode('utf-8'), 
           'product_id': params['cproditem'], 
           'affiliate': params['ctransaffiliate'], 
           'trans_type': params['ctransaction']}

    def get_user_by_email(self, email):
        user = api.user.get(username=email)
        if user is not None:
            return user
        else:
            email_lower = email.lower()
            for u in api.user.get_users():
                if email_lower == u.getProperty('billing_email', '').lower():
                    return u

            return