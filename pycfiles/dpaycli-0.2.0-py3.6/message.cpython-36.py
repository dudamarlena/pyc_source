# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/dpaycli/message.py
# Compiled at: 2018-10-15 03:18:48
# Size of source mod 2**32: 4647 bytes
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from builtins import object
import re, logging
from binascii import hexlify, unhexlify
from dpaycligraphenebase.ecdsasig import verify_message, sign_message
from dpaycligraphenebase.account import PublicKey
from dpaycli.instance import shared_dpay_instance
from dpaycli.account import Account
from .exceptions import InvalidMessageSignature
from .storage import configStorage as config
log = logging.getLogger(__name__)
MESSAGE_SPLIT = ('-----BEGIN BEX SIGNED MESSAGE-----', '-----BEGIN META-----', '-----BEGIN SIGNATURE-----',
                 '-----END BEX SIGNED MESSAGE-----')
SIGNED_MESSAGE_META = '{message}\naccount={meta[account]}\nmemokey={meta[memokey]}\nblock={meta[block]}\ntimestamp={meta[timestamp]}'
SIGNED_MESSAGE_ENCAPSULATED = '\n{MESSAGE_SPLIT[0]}\n{message}\n{MESSAGE_SPLIT[1]}\naccount={meta[account]}\nmemokey={meta[memokey]}\nblock={meta[block]}\ntimestamp={meta[timestamp]}\n{MESSAGE_SPLIT[2]}\n{signature}\n{MESSAGE_SPLIT[3]}\n'

class Message(object):

    def __init__(self, message, dpay_instance=None):
        self.dpay = dpay_instance or shared_dpay_instance()
        self.message = message

    def sign(self, account=None, **kwargs):
        """ Sign a message with an account's memo key

            :param str account: (optional) the account that owns the bet
                (defaults to ``default_account``)

            :returns: the signed message encapsulated in a known format

        """
        if not account:
            if 'default_account' in config:
                account = config['default_account']
        if not account:
            raise ValueError('You need to provide an account')
        account = Account(account, dpay_instance=(self.dpay))
        info = self.dpay.info()
        meta = dict(timestamp=(info['time']),
          block=(info['head_block_number']),
          memokey=(account['memo_key']),
          account=(account['name']))
        wif = self.dpay.wallet.getPrivateKeyForPublicKey(account['memo_key'])
        message = self.message.strip()
        signature = hexlify(sign_message((SIGNED_MESSAGE_META.format)(**locals()), wif)).decode('ascii')
        message = self.message
        return (SIGNED_MESSAGE_ENCAPSULATED.format)(MESSAGE_SPLIT=MESSAGE_SPLIT, **locals())

    def verify(self, **kwargs):
        """ Verify a message with an account's memo key

            :param str account: (optional) the account that owns the bet
                (defaults to ``default_account``)

            :returns: True if the message is verified successfully

            :raises: InvalidMessageSignature if the signature is not ok

        """
        parts = re.split('|'.join(MESSAGE_SPLIT), self.message)
        parts = [x for x in parts if x.strip()]
        assert len(parts) > 2, 'Incorrect number of message parts'
        message = parts[0].strip()
        signature = parts[2].strip()
        meta = dict(re.findall('(\\S+)=(.*)', parts[1]))
        if 'account' not in meta:
            raise AssertionError()
        if 'memokey' not in meta:
            raise AssertionError()
        if 'block' not in meta:
            raise AssertionError()
        if 'timestamp' not in meta:
            raise AssertionError()
        account = Account((meta.get('account')),
          dpay_instance=(self.dpay))
        if not account['memo_key'] == meta['memokey']:
            log.error('Memo Key of account {} on the Blockchain'.format(account['name']) + 'differs from memo key in the message: {} != {}'.format(account['memo_key'], meta['memokey']))
        message = (SIGNED_MESSAGE_META.format)(**locals())
        pubkey = verify_message(message, unhexlify(signature))
        pk = PublicKey(hexlify(pubkey).decode('ascii'))
        if format(pk, self.dpay.prefix) != meta['memokey']:
            raise InvalidMessageSignature
        return True