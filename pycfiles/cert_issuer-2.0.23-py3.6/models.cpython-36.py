# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/cert_issuer/models.py
# Compiled at: 2018-12-05 14:02:34
# Size of source mod 2**32: 2650 bytes
from abc import abstractmethod
from cert_issuer.config import ESTIMATE_NUM_INPUTS

class BatchHandler(object):

    def __init__(self, secret_manager, certificate_handler, merkle_tree):
        self.certificate_handler = certificate_handler
        self.secret_manager = secret_manager
        self.merkle_tree = merkle_tree

    @abstractmethod
    def pre_batch_actions(self, config):
        pass

    @abstractmethod
    def post_batch_actions(self, config):
        pass

    def set_certificates_in_batch(self, certificates_to_issue):
        self.certificates_to_issue = certificates_to_issue


class CertificateHandler(object):

    @abstractmethod
    def validate_certificate(self, certificate_metadata):
        pass

    @abstractmethod
    def sign_certificate(self, signer, certificate_metadata):
        pass

    @abstractmethod
    def get_byte_array_to_issue(self, certificate_metadata):
        pass

    @abstractmethod
    def add_proof(self, certificate_metadata, merkle_proof):
        pass


class ServiceProviderConnector(object):

    @abstractmethod
    def get_balance(self, address):
        pass

    def broadcast_tx(self, tx):
        pass


class Signer(object):
    __doc__ = '\n    Abstraction for a component that can sign.\n    '

    def __init__(self):
        pass

    @abstractmethod
    def sign_message(self, wif, message_to_sign):
        pass

    @abstractmethod
    def sign_transaction(self, wif, transaction_to_sign):
        pass


class SecretManager(object):

    def __init__(self, signer):
        self.signer = signer
        self.wif = None

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def stop(self):
        pass

    def sign_message(self, message_to_sign):
        return self.signer.sign_message(self.wif, message_to_sign)

    def sign_transaction(self, transaction_to_sign):
        return self.signer.sign_transaction(self.wif, transaction_to_sign)


class TransactionHandler(object):

    @abstractmethod
    def ensure_balance(self):
        pass

    @abstractmethod
    def issue_transaction(self, blockchain_bytes):
        pass


class MockTransactionHandler(TransactionHandler):

    def ensure_balance(self):
        pass

    def issue_transaction(self, op_return_bytes):
        return 'This has not been issued on a blockchain and is for testing only'


class TransactionCreator(object):

    @abstractmethod
    def estimate_cost_for_certificate_batch(self, tx_cost_constants, num_inputs=ESTIMATE_NUM_INPUTS):
        pass

    @abstractmethod
    def create_transaction(self, tx_cost_constants, issuing_address, inputs, op_return_value):
        pass