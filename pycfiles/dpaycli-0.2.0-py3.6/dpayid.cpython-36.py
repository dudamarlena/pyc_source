# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/dpaycli/dpayid.py
# Compiled at: 2018-10-15 03:19:34
# Size of source mod 2**32: 10273 bytes
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from builtins import str
import json
try:
    from urllib.parse import urlparse, urlencode, urljoin
except ImportError:
    from urlparse import urlparse, urljoin
    from urllib import urlencode

import requests
from .storage import configStorage as config
from six import PY2
from dpaycli.instance import shared_dpay_instance
from dpaycli.amount import Amount

class DPayID(object):
    __doc__ = ' DPayID\n\n        :param str scope: comma separated string with scopes\n            login,offline,vote,comment,delete_comment,comment_options,custom_json,claim_reward_balance\n\n\n        .. code-block:: python\n\n            # Run the login_app in examples and login with a account\n            from dpaycli import DPay\n            from dpaycli.dpayid import DPayID\n            from dpaycli.comment import Comment\n            dpid = DPayID(client_id="dpaycli.app")\n            dpay = DPay(dpayid=dpid)\n            dpay.wallet.unlock("supersecret-passphrase")\n            post = Comment("author/permlink", dpay_instance=dpay)\n            post.upvote(voter="test")  # replace "test" with your account\n\n        Examples for creating dpayid v2 urls for broadcasting in browser:\n        .. testoutput::\n\n            from dpaycli import DPay\n            from dpaycli.account import Account\n            from dpaycli.dpayid import DPayID\n            from pprint import pprint\n            dpay = DPay(nobroadcast=True, unsigned=True)\n            dpid = DPayID(dpay_instance=dpay)\n            acc = Account("test", dpay_instance=dpay)\n            pprint(dpid.url_from_tx(acc.transfer("test1", 1, "BEX", "test")))\n\n        .. testcode::\n\n            \'https://go.dpayid.io/sign/transfer?from=test&to=test1&amount=1.000+BEX&memo=test\'\n\n        .. testoutput::\n\n            from dpaycli import DPay\n            from dpaycli.transactionbuilder import TransactionBuilder\n            from dpayclibase import operations\n            from dpaycli.dpayid import DPayID\n            from pprint import pprint\n            stm = DPay(nobroadcast=True, unsigned=True)\n            dpid = DPayID(dpay_instance=stm)\n            tx = TransactionBuilder(dpay_instance=stm)\n            op = operations.Transfer(**{"from": \'test\',\n                                        "to": \'test1\',\n                                        "amount": \'1.000 BEX\',\n                                        "memo": \'test\'})\n            tx.appendOps(op)\n            pprint(dpid.url_from_tx(tx.json()))\n\n        .. testcode::\n\n            \'https://go.dpayid.io/sign/transfer?from=test&to=test1&amount=1.000+BEX&memo=test\'\n\n    '

    def __init__(self, dpay_instance=None, *args, **kwargs):
        self.dpay = dpay_instance or shared_dpay_instance()
        self.access_token = None
        self.get_refresh_token = kwargs.get('get_refresh_token', False)
        self.hot_sign_redirect_uri = kwargs.get('hot_sign_redirect_uri', config['hot_sign_redirect_uri'])
        if self.hot_sign_redirect_uri == '':
            self.hot_sign_redirect_uri = None
        self.client_id = kwargs.get('client_id', config['dpid_client_id'])
        self.scope = kwargs.get('scope', 'login')
        self.oauth_base_url = kwargs.get('oauth_base_url', config['oauth_base_url'])
        self.dpid_api_url = kwargs.get('dpid_api_url', config['dpid_api_url'])

    @property
    def headers(self):
        return {'Authorization': self.access_token}

    def get_login_url(self, redirect_uri, **kwargs):
        """ Returns a login url for receiving token from dpayid
        """
        client_id = kwargs.get('client_id', self.client_id)
        scope = kwargs.get('scope', self.scope)
        get_refresh_token = kwargs.get('get_refresh_token', self.get_refresh_token)
        params = {'client_id':client_id, 
         'redirect_uri':redirect_uri, 
         'scope':scope}
        if get_refresh_token:
            params.update({'response_type': 'code'})
        if PY2:
            return urljoin(self.oauth_base_url, 'authorize?' + urlencode(params).replace('%2C', ','))
        else:
            return urljoin(self.oauth_base_url, 'authorize?' + urlencode(params, safe=','))

    def get_access_token(self, code):
        post_data = {'grant_type':'authorization_code', 
         'code':code, 
         'client_id':self.client_id, 
         'client_secret':self.dpay.wallet.getTokenForAccountName(self.client_id)}
        r = requests.post((urljoin(self.dpid_api_url, 'oauth2/token/')),
          data=post_data)
        return r.json()

    def me(self, username=None):
        """ Calls the me function from dpayid

        .. code-block:: python

            from dpaycli.dpayid import DPayID
            dpid = DPayID()
            dpid.dpay.wallet.unlock("supersecret-passphrase")
            dpid.me(username="test")

        """
        if username:
            self.set_username(username)
        url = urljoin(self.dpid_api_url, 'me/')
        r = requests.post(url, headers=(self.headers))
        return r.json()

    def set_access_token(self, access_token):
        """ Is needed for broadcast() and me()
        """
        self.access_token = access_token

    def set_username(self, username, permission='posting'):
        """ Set a username for the next broadcast() or me operation()
            The necessary token is fetched from the wallet
        """
        if permission != 'posting':
            self.access_token = None
            return
        self.access_token = self.dpay.wallet.getTokenForAccountName(username)

    def broadcast(self, operations, username=None):
        """ Broadcast a operations

            Sample operations:

            .. code-block:: js

                [
                    [
                        'vote', {
                                    'voter': 'gandalf',
                                    'author': 'gtg',
                                    'permlink': 'dpay-pressure-4-need-for-speed',
                                    'weight': 10000
                                }
                    ]
                ]

        """
        url = urljoin(self.dpid_api_url, 'broadcast/')
        data = {'operations': operations}
        if username:
            self.set_username(username)
        headers = self.headers.copy()
        headers.update({'Content-Type':'application/json; charset=utf-8', 
         'Accept':'application/json'})
        r = requests.post(url, headers=headers, data=(json.dumps(data)))
        try:
            return r.json()
        except ValueError:
            return r.content

    def refresh_access_token(self, code, scope):
        post_data = {'grant_type':'refresh_token', 
         'refresh_token':code, 
         'client_id':self.client_id, 
         'client_secret':self.dpay.wallet.getTokenForAccountName(self.client_id), 
         'scope':scope}
        r = requests.post((urljoin(self.dpid_api_url, 'oauth2/token/')),
          data=post_data)
        return r.json()

    def revoke_token(self, access_token):
        post_data = {'access_token': access_token}
        r = requests.post((urljoin(self.dpid_api_url, 'oauth2/token/revoke')),
          data=post_data)
        return r.json()

    def update_user_metadata(self, metadata):
        put_data = {'user_metadata': metadata}
        r = requests.put((urljoin(self.dpid_api_url, 'me/')),
          data=put_data,
          headers=(self.headers))
        return r.json()

    def url_from_tx(self, tx, redirect_uri=None):
        """ Creates a link for broadcasting an operation

            :param dict tx: includes the operation, which should be broadcast
            :param str redirect_uri: Redirects to this uri, when set
        """
        if not isinstance(tx, dict):
            tx = tx.json()
        if 'operations' not in tx or not tx['operations']:
            return ''
        else:
            urls = []
            operations = tx['operations']
            for op in operations:
                operation = op[0]
                params = op[1]
                for key in params:
                    value = params[key]
                    if isinstance(value, list) and len(value) == 3:
                        try:
                            amount = Amount(value, dpay_instance=(self.dpay))
                            params[key] = str(amount)
                        except:
                            amount = None

                    else:
                        if isinstance(value, bool):
                            if value:
                                params[key] = 1
                            else:
                                params[key] = 0

                urls.append(self.create_hot_sign_url(operation, params, redirect_uri=redirect_uri))

            if len(urls) == 1:
                return urls[0]
            return urls

    def create_hot_sign_url(self, operation, params, redirect_uri=None):
        """ Creates a link for broadcasting an operation

            :param str operation: operation name (e.g.: vote)
            :param dict params: operation dict params
            :param str redirect_uri: Redirects to this uri, when set
        """
        if not isinstance(operation, str) or not isinstance(params, dict):
            raise ValueError('Invalid Request.')
        else:
            base_url = self.dpid_api_url.replace('/api', '')
            if redirect_uri == '':
                redirect_uri = None
            if redirect_uri is None:
                if self.hot_sign_redirect_uri is not None:
                    redirect_uri = self.hot_sign_redirect_uri
            if redirect_uri is not None:
                params.update({'redirect_uri': redirect_uri})
        for key in params:
            if isinstance(params[key], list):
                params[key] = json.dumps(params[key])

        params = urlencode(params)
        url = urljoin(base_url, 'sign/%s' % operation)
        url += '?' + params
        return url