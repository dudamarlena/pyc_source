# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/cert_issuer/blockchain_handlers/ethereum/connectors.py
# Compiled at: 2020-03-18 12:43:21
# Size of source mod 2**32: 9659 bytes
import logging, time, requests
try:
    from urllib2 import urlopen, HTTPError
    from urllib import urlencode
except ImportError:
    from urllib.request import urlopen, HTTPError
    from urllib.parse import urlencode

from cert_core import Chain
from cert_issuer.models import ServiceProviderConnector
from cert_issuer.errors import BroadcastError
BROADCAST_RETRY_INTERVAL = 30
MAX_BROADCAST_ATTEMPTS = 3

class EthereumServiceProviderConnector(ServiceProviderConnector):

    def __init__(self, ethereum_chain, api_key, local_node=False):
        self.ethereum_chain = ethereum_chain
        self.api_key = api_key
        self.local_node = local_node

    def get_balance(self, address):
        for m in get_providers_for_chain(self.ethereum_chain, self.local_node):
            try:
                logging.debug('m=%s', m)
                balance = m.get_balance(address, self.api_key)
                return balance
            except Exception as e:
                logging.warning(e)

        return 0

    def get_address_nonce(self, address):
        for m in get_providers_for_chain(self.ethereum_chain, self.local_node):
            try:
                logging.debug('m=%s', m)
                nonce = m.get_address_nonce(address, self.api_key)
                return nonce
            except Exception as e:
                logging.warning(e)

        return 0

    def broadcast_tx(self, tx):
        last_exception = None
        final_tx_id = None
        for attempt_number in range(0, MAX_BROADCAST_ATTEMPTS):
            for m in get_providers_for_chain(self.ethereum_chain, self.local_node):
                try:
                    logging.debug('m=%s', m)
                    txid = m.broadcast_tx(tx, self.api_key)
                    if txid:
                        logging.info('Broadcasting succeeded with method_provider=%s, txid=%s', str(m), txid)
                        if final_tx_id:
                            if final_tx_id != txid:
                                logging.error('This should never happen; fail and investigate if it does. Got conflicting tx_ids=%s and %s. Hextx=%s', final_tx_id, txid, tx.as_hex())
                                raise Exception('Got conflicting tx_ids.')
                        final_tx_id = txid
                    return txid
                except Exception as e:
                    logging.warning('Caught exception trying provider %s. Trying another. Exception=%s', str(m), e)
                    last_exception = e

            if final_tx_id:
                return final_tx_id
            logging.warning('Broadcasting failed. Waiting before retrying. This is attempt number %d', attempt_number)
            time.sleep(BROADCAST_RETRY_INTERVAL)

        logging.error('Failed broadcasting through all providers')
        logging.error(last_exception, exc_info=True)
        raise BroadcastError(last_exception)


class EtherscanBroadcaster(object):

    def __init__(self, base_url):
        self.base_url = base_url

    def broadcast_tx(self, tx, api_token):
        tx_hex = tx
        broadcast_url = self.base_url + '?module=proxy&action=eth_sendRawTransaction'
        if api_token:
            broadcast_url += '&apikey=%s' % api_token
        response = requests.post(broadcast_url, data={'hex': tx_hex})
        if 'error' in response.json():
            logging.error('Etherscan returned an error: %s', response.json()['error'])
            raise BroadcastError(response.json()['error'])
        if int(response.status_code) == 200:
            if response.json().get('message', None) == 'NOTOK':
                raise BroadcastError(response.json().get('result', None))
            tx_id = response.json().get('result', None)
            logging.info('Transaction ID obtained from broadcast through Etherscan: %s', tx_id)
            return tx_id
        logging.error('Error broadcasting the transaction through the Etherscan API. Error msg: %s', response.text)
        raise BroadcastError(response.text)

    def get_balance(self, address, api_token):
        """
        returns the balance in wei
        with some inspiration from PyWallet
        """
        broadcast_url = self.base_url + '?module=account&action=balance'
        broadcast_url += '&address=%s' % address
        broadcast_url += '&tag=pending'
        if api_token:
            broadcast_url += '&apikey=%s' % api_token
        response = requests.get(broadcast_url)
        if int(response.status_code) == 200:
            if response.json().get('message', None) == 'NOTOK':
                raise BroadcastError(response.json().get('result', None))
            balance = int(response.json().get('result', None))
            logging.info('Balance check succeeded: %s', response.json())
            return balance
        raise BroadcastError(response.text)

    def get_address_nonce(self, address, api_token):
        """
        Looks up the address nonce of this address
        Neccesary for the transaction creation
        """
        broadcast_url = self.base_url + '?module=proxy&action=eth_getTransactionCount'
        broadcast_url += '&address=%s' % address
        broadcast_url += '&tag=pending'
        if api_token:
            broadcast_url += '&apikey=%s' % api_token
        response = requests.get(broadcast_url)
        if int(response.status_code) == 200:
            if response.json().get('message', None) == 'NOTOK':
                raise BroadcastError(response.json().get('result', None))
            nonce = int(response.json().get('result', None), 0)
            logging.info('Nonce check went correct: %s', response.json())
            return nonce
        logging.info('response error checking nonce')
        raise BroadcastError('Error checking the nonce through the Etherscan API. Error msg: %s', response.text)


class MyEtherWalletBroadcaster(object):

    def __init__(self, base_url):
        self.base_url = base_url

    def broadcast_tx(self, tx, api_token):
        data = {'jsonrpc':'2.0', 
         'method':'eth_sendRawTransaction', 
         'params':[
          '0x' + tx], 
         'id':1}
        response = requests.post((self.base_url), json=data)
        if 'error' in response.json():
            logging.error('MyEtherWallet returned an error: %s', response.json()['error'])
            raise BroadcastError(response.json()['error'])
        if int(response.status_code) == 200:
            tx_id = response.json().get('result', None)
            logging.info('Transaction ID obtained from broadcast through MyEtherWallet: %s', tx_id)
            return tx_id
        logging.error('Error broadcasting the transaction through MyEtherWallet. Error msg: %s', response.text)
        raise BroadcastError(response.text)

    def get_balance(self, address, api_token):
        """
        returns the balance in wei
        """
        data = {'jsonrpc':'2.0', 
         'method':'eth_getBalance', 
         'params':[
          address, 'latest'], 
         'id':1}
        response = requests.post((self.base_url), json=data)
        if int(response.status_code) == 200:
            logging.info('Balance check response: %s', response.json())
            balance = int(response.json().get('result', None), 0)
            logging.info('Balance check succeeded: %s', response.json())
            return balance
        logging.error('Error getting balance through MyEtherWallet. Error msg: %s', response.text)
        raise BroadcastError(response.text)

    def get_address_nonce(self, address, api_token):
        """
        Looks up the address nonce of this address
        Neccesary for the transaction creation
        """
        data = {'jsonrpc':'2.0', 
         'method':'eth_getTransactionCount', 
         'params':[
          address, 'pending'], 
         'id':1}
        response = requests.post((self.base_url), json=data)
        if int(response.status_code) == 200:
            nonce = int(response.json().get('result', None), 0)
            logging.info('Nonce check went correct: %s', response.json())
            return nonce
        logging.info('response error checking nonce')
        raise BroadcastError('Error checking the nonce through the MyEtherWallet API. Error msg: %s', response.text)


connectors = {}
eth_provider_list = []
eth_provider_list.append(EtherscanBroadcaster('https://api.etherscan.io/api'))
eth_provider_list.append(MyEtherWalletBroadcaster('https://api.myetherwallet.com/eth'))
connectors[Chain.ethereum_mainnet] = eth_provider_list
rop_provider_list = []
rop_provider_list.append(EtherscanBroadcaster('https://ropsten.etherscan.io/api'))
rop_provider_list.append(MyEtherWalletBroadcaster('https://api.myetherwallet.com/rop'))
connectors[Chain.ethereum_ropsten] = rop_provider_list

def get_providers_for_chain(chain, local_node=False):
    return connectors[chain]