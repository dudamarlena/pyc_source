# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/cert_issuer/issuer.py
# Compiled at: 2018-12-05 14:02:34
# Size of source mod 2**32: 1352 bytes
__doc__ = '\nBase class for building blockchain transactions to issue Blockchain Certificates.\n'
import logging
from cert_issuer.errors import BroadcastError
MAX_TX_RETRIES = 5

class Issuer:

    def __init__(self, certificate_batch_handler, transaction_handler, max_retry=MAX_TX_RETRIES):
        self.certificate_batch_handler = certificate_batch_handler
        self.transaction_handler = transaction_handler
        self.max_retry = max_retry

    def issue(self, chain):
        """
        Issue the certificates on the blockchain
        :return:
        """
        blockchain_bytes = self.certificate_batch_handler.prepare_batch()
        for attempt_number in range(0, self.max_retry):
            try:
                txid = self.transaction_handler.issue_transaction(blockchain_bytes)
                self.certificate_batch_handler.finish_batch(txid, chain)
                logging.info('Broadcast transaction with txid %s', txid)
                return txid
            except BroadcastError:
                logging.warning('Failed broadcast reattempts. Trying to recreate transaction. This is attempt number %d', attempt_number)

        logging.error('All attempts to broadcast failed. Try rerunning issuer.')
        raise BroadcastError('All attempts to broadcast failed. Try rerunning issuer.')