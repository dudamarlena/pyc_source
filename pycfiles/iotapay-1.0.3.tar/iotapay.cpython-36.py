# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Anirudha/Documents/blockchain/acyclic/labs/iotapay/iotapay-py/iotapay/iotapay.py
# Compiled at: 2019-03-05 05:32:00
# Size of source mod 2**32: 3640 bytes
from iota import Address, ProposedTransaction, Tag, Transaction, Iota, TryteString, json
import time, json
tag = Tag('ACYCLICIOTAPAYLIOTA99999999')

class Iotapay:

    def __init__(self, provider, seed, address=None):
        self.seed = seed
        self.provider = provider
        self.api = Iota(self.provider, self.seed)

    def pay(self, data):
        try:
            json_data = data['json_data']
            json_string = json.dumps(json_data)
            trytes = TryteString.from_string(json_string)
            print('sending transfer ...')
            sent_transfer = self.api.send_transfer(depth=3,
              transfers=[
             ProposedTransaction(address=(Address(data['to_address'])),
               value=(data['amount']),
               tag=tag,
               message=trytes)])
            print('sent_transfer', sent_transfer)
            bo = sent_transfer['bundle']
            print('bundle', bo)
            return {'status':200, 
             'transaction_hash':bo.as_json_compatible()[0]['hash_'], 
             'message':'Successfully Sent!'}
        except Exception as pe:
            print('pe:', pe)
            return {'status':400, 
             'error':'', 
             'message':str(pe).split('(')[0]}

    def get_balance(self, data):
        try:
            if 'address' in data:
                balance_result = self.api.get_balances([data['address']])
                print('balance_result:', balance_result)
                balance = balance_result['balances'][0]
                return {'status':200, 
                 'balance':balance, 
                 'message':'Successfully Retrieved!'}
            gna_result = self.api.get_new_addresses(index=0, count=50)
            addresses = gna_result['addresses']
            print('addresses:', addresses)
            print('---- ++++ ===' * 10)
            balance_result = self.api.get_balances(addresses)
            print('balance_result:', balance_result)
            balance = 0
            for i in range(len(balance_result['balances'])):
                balance = balance + balance_result['balances'][i]

            print('balance:', balance)
        except Exception as pe:
            print('pe:', pe)
            return {'status':400, 
             'error':''}

    def collect(self, data):
        print('send request to collect payment.')

    def generate_invoice(self, data):
        print('generate invoice.')