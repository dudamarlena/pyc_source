# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/dpaycli/transactionbuilder.py
# Compiled at: 2018-10-15 03:19:34
# Size of source mod 2**32: 18830 bytes
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from builtins import str
from future.utils import python_2_unicode_compatible
import logging
from dpaycligraphenebase.py23 import bytes_types, integer_types, string_types, text_type
from .account import Account
from .utils import formatTimeFromNow
from .dpayid import DPayID
from dpayclibase.objects import Operation
from dpaycligraphenebase.account import PrivateKey, PublicKey
from dpayclibase.signedtransactions import Signed_Transaction
from dpayclibase import transactions, operations
from .exceptions import InsufficientAuthorityError, MissingKeyError, InvalidWifError, WalletLocked, OfflineHasNoRPCException
from dpaycli.instance import shared_dpay_instance
log = logging.getLogger(__name__)

@python_2_unicode_compatible
class TransactionBuilder(dict):
    __doc__ = ' This class simplifies the creation of transactions by adding\n        operations and signers.\n        To build your own transactions and sign them\n\n        :param dict tx: transaction (Optional). If not set, the new transaction is created.\n        :param int expiration: Delay in seconds until transactions are supposed\n            to expire *(optional)* (default is 30)\n        :param DPay dpay_instance: If not set, shared_dpay_instance() is used\n\n        .. testcode::\n\n           from dpaycli.transactionbuilder import TransactionBuilder\n           from dpayclibase.operations import Transfer\n           from dpaycli import DPay\n           wif = "5KQwrPbwdL6PhXujxW37FSSQZ1JiwsST4cqQzDeyXtP79zkvFD3"\n           stm = DPay(nobroadcast=True, keys={\'active\': wif})\n           tx = TransactionBuilder(dpay_instance=stm)\n           transfer = {"from": "test", "to": "test1", "amount": "1 BEX", "memo": ""}\n           tx.appendOps(Transfer(transfer))\n           tx.appendSigner("test", "active") # or tx.appendWif(wif)\n           signed_tx = tx.sign()\n           broadcast_tx = tx.broadcast()\n\n    '

    def __init__(self, tx={}, use_condenser_api=True, dpay_instance=None, **kwargs):
        self.dpay = dpay_instance or shared_dpay_instance()
        self.clear()
        if tx:
            if isinstance(tx, dict):
                super(TransactionBuilder, self).__init__(tx)
                self.ops = tx['operations']
                self._require_reconstruction = False
        else:
            self._require_reconstruction = True
        self._use_condenser_api = use_condenser_api
        self.set_expiration(kwargs.get('expiration', self.dpay.expiration))

    def set_expiration(self, p):
        """Set expiration date"""
        self.expiration = p

    def is_empty(self):
        """Check if ops is empty"""
        return not len(self.ops) > 0

    def list_operations(self):
        """List all ops"""
        if self.dpay.is_connected():
            if self.dpay.rpc.get_use_appbase():
                appbase = not self._use_condenser_api
        else:
            appbase = False
        return [Operation(o, appbase=appbase, prefix=(self.dpay.prefix)) for o in self.ops]

    def _is_signed(self):
        """Check if signatures exists"""
        return 'signatures' in self and bool(self['signatures'])

    def _is_constructed(self):
        """Check if tx is already constructed"""
        return 'expiration' in self and bool(self['expiration'])

    def _is_require_reconstruction(self):
        return self._require_reconstruction

    def _set_require_reconstruction(self):
        self._require_reconstruction = True

    def _unset_require_reconstruction(self):
        self._require_reconstruction = False

    def __repr__(self):
        return str(self)

    def __str__(self):
        return str(self.json())

    def __getitem__(self, key):
        if key not in self:
            self.constructTx()
        return dict(self).__getitem__(key)

    def get_parent(self):
        """ TransactionBuilders don't have parents, they are their own parent
        """
        return self

    def json(self, with_prefix=False):
        """ Show the transaction as plain json
        """
        if not self._is_constructed() or self._is_require_reconstruction():
            self.constructTx()
        json_dict = dict(self)
        if with_prefix:
            json_dict['prefix'] = self.dpay.prefix
        return json_dict

    def appendOps(self, ops, append_to=None):
        """ Append op(s) to the transaction builder

            :param list ops: One or a list of operations
        """
        if isinstance(ops, list):
            self.ops.extend(ops)
        else:
            self.ops.append(ops)
        self._set_require_reconstruction()

    def appendSigner(self, account, permission):
        """ Try to obtain the wif key from the wallet by telling which account
            and permission is supposed to sign the transaction
            It is possible to add more than one signer.
        """
        if not self.dpay.is_connected():
            return
        else:
            if permission not in ('active', 'owner', 'posting'):
                raise AssertionError('Invalid permission')
            else:
                account = Account(account, dpay_instance=(self.dpay))
                if permission not in account:
                    account = Account(account, dpay_instance=(self.dpay), lazy=False, full=True)
                    account.clear_cache()
                    account.refresh()
                if permission not in account:
                    account = Account(account, dpay_instance=(self.dpay))
                if permission not in account:
                    raise AssertionError('Could not access permission')
                required_treshold = account[permission]['weight_threshold']
                if self.dpay.wallet.locked():
                    raise WalletLocked()
                if self.dpay.use_dpid:
                    self.dpay.dpayid.set_username(account['name'], permission)
                    return

            def fetchkeys(account, perm, level=0):
                if level > 2:
                    return []
                else:
                    r = []
                    for authority in account[perm]['key_auths']:
                        try:
                            wif = self.dpay.wallet.getPrivateKeyForPublicKey(authority[0])
                            if wif:
                                r.append([wif, authority[1]])
                        except ValueError:
                            pass
                        except MissingKeyError:
                            pass

                    if sum([x[1] for x in r]) < required_treshold:
                        for authority in account[perm]['account_auths']:
                            auth_account = Account((authority[0]),
                              dpay_instance=(self.dpay))
                            r.extend(fetchkeys(auth_account, perm, level + 1))

                    return r

            if account['name'] not in self.signing_accounts:
                if isinstance(account, PublicKey):
                    self.wifs.add(self.dpay.wallet.getPrivateKeyForPublicKey(str(account)))
                else:
                    if permission not in account:
                        raise AssertionError('Could not access permission')
                    else:
                        required_treshold = account[permission]['weight_threshold']
                        keys = fetchkeys(account, permission)
                        if not keys:
                            if permission == 'posting':
                                _keys = fetchkeys(account, 'active')
                                keys.extend(_keys)
                        if not keys:
                            if permission != 'owner':
                                _keys = fetchkeys(account, 'owner')
                                keys.extend(_keys)
                    for x in keys:
                        self.wifs.add(x[0])

                self.signing_accounts.append(account['name'])

    def appendWif(self, wif):
        """ Add a wif that should be used for signing of the transaction.

            :param string wif: One wif key to use for signing
                a transaction.
        """
        if wif:
            try:
                PrivateKey(wif, prefix=(self.dpay.prefix))
                self.wifs.add(wif)
            except:
                raise InvalidWifError

    def clearWifs(self):
        """Clear all stored wifs"""
        self.wifs = set()

    def constructTx(self, ref_block_num=None, ref_block_prefix=None):
        """ Construct the actual transaction and store it in the class's dict
            store

        """
        ops = list()
        if self.dpay.is_connected():
            if self.dpay.rpc.get_use_appbase():
                appbase = not self._use_condenser_api
        else:
            appbase = False
        for op in self.ops:
            ops.extend([Operation(op, appbase=appbase, prefix=(self.dpay.prefix))])

        expiration = formatTimeFromNow(self.expiration or self.dpay.expiration)
        if ref_block_num is None or ref_block_prefix is None:
            ref_block_num, ref_block_prefix = transactions.getBlockParams(self.dpay.rpc)
        self.tx = Signed_Transaction(ref_block_prefix=ref_block_prefix,
          expiration=expiration,
          operations=ops,
          ref_block_num=ref_block_num,
          custom_chains=(self.dpay.custom_chains),
          prefix=(self.dpay.prefix))
        super(TransactionBuilder, self).update(self.tx.json())
        self._unset_require_reconstruction()

    def sign(self, reconstruct_tx=True):
        """ Sign a provided transaction with the provided key(s)
            One or many wif keys to use for signing a transaction.
            The wif keys can be provided by "appendWif" or the
            signer can be defined "appendSigner". The wif keys
            from all signer that are defined by "appendSigner
            will be loaded from the wallet.

            :param bool reconstruct_tx: when set to False and tx
                is already contructed, it will not reconstructed
                and already added signatures remain

        """
        if not self._is_constructed() or self._is_constructed() and reconstruct_tx:
            self.constructTx()
        if 'operations' not in self or not self['operations']:
            return
        if self.dpay.use_dpid:
            return
        else:
            if self.dpay.rpc is not None:
                operations.default_prefix = self.dpay.chain_params['prefix']
            else:
                if 'blockchain' in self:
                    operations.default_prefix = self['blockchain']['prefix']
            try:
                signedtx = Signed_Transaction(**self.json(with_prefix=True))
                signedtx.add_custom_chains(self.dpay.custom_chains)
            except:
                raise ValueError('Invalid TransactionBuilder Format')

            if not any(self.wifs):
                raise MissingKeyError
            signedtx.sign((self.wifs), chain=(self.dpay.chain_params))
            self['signatures'].extend(signedtx.json().get('signatures'))
            return signedtx

    def verify_authority(self):
        """ Verify the authority of the signed transaction
        """
        try:
            self.dpay.rpc.set_next_node_on_empty_reply(False)
            if self.dpay.rpc.get_use_appbase():
                args = {'trx': self.json()}
            else:
                args = self.json()
            ret = self.dpay.rpc.verify_authority(args, api='database')
            if not ret:
                raise InsufficientAuthorityError
            else:
                if isinstance(ret, dict):
                    if 'valid' in ret:
                        if not ret['valid']:
                            raise InsufficientAuthorityError
        except Exception as e:
            raise e

    def get_potential_signatures(self):
        """ Returns public key from signature
        """
        if not self.dpay.is_connected():
            raise OfflineHasNoRPCException('No RPC available in offline mode!')
        else:
            self.dpay.rpc.set_next_node_on_empty_reply(False)
            if self.dpay.rpc.get_use_appbase():
                args = {'trx': self.json()}
            else:
                args = self.json()
        ret = self.dpay.rpc.get_potential_signatures(args, api='database')
        if 'keys' in ret:
            ret = ret['keys']
        return ret

    def get_transaction_hex(self):
        """ Returns a hex value of the transaction
        """
        if not self.dpay.is_connected():
            raise OfflineHasNoRPCException('No RPC available in offline mode!')
        else:
            self.dpay.rpc.set_next_node_on_empty_reply(False)
            if self.dpay.rpc.get_use_appbase():
                args = {'trx': self.json()}
            else:
                args = self.json()
        ret = self.dpay.rpc.get_transaction_hex(args, api='database')
        if 'hex' in ret:
            ret = ret['hex']
        return ret

    def get_required_signatures(self, available_keys=list()):
        """ Returns public key from signature
        """
        if not self.dpay.is_connected():
            raise OfflineHasNoRPCException('No RPC available in offline mode!')
        else:
            self.dpay.rpc.set_next_node_on_empty_reply(False)
            if self.dpay.rpc.get_use_appbase():
                args = {'trx':self.json(), 
                 'available_keys':available_keys}
                ret = self.dpay.rpc.get_required_signatures(args, api='database')
            else:
                ret = self.dpay.rpc.get_required_signatures((self.json()), available_keys, api='database')
        return ret

    def broadcast(self, max_block_age=-1):
        """ Broadcast a transaction to the dPay network
            Returns the signed transaction and clears itself
            after broadast

            Clears itself when broadcast was not successfully.

            :param int max_block_age: paramerter only used
                for appbase ready nodes

        """
        if not self._is_signed():
            self.sign()
        else:
            if 'operations' not in self or not self['operations']:
                return
            ret = self.json()
            if self.dpay.is_connected():
                if self.dpay.rpc.get_use_appbase():
                    if not self._use_condenser_api:
                        args = {'trx':self.json(), 
                         'max_block_age':max_block_age}
                        broadcast_api = 'network_broadcast'
                    else:
                        args = self.json()
                        broadcast_api = 'condenser'
            args = self.json()
            broadcast_api = 'network_broadcast'
        if self.dpay.nobroadcast:
            log.info('Not broadcasting anything!')
            self.clear()
            return ret
        else:
            try:
                self.dpay.rpc.set_next_node_on_empty_reply(False)
                if self.dpay.use_dpid:
                    ret = self.dpay.dpayid.broadcast(self['operations'])
                else:
                    if self.dpay.blocking:
                        ret = self.dpay.rpc.broadcast_transaction_synchronous(args,
                          api=broadcast_api)
                        if 'trx' in ret:
                            (ret.update)(**ret.get('trx'))
                    else:
                        self.dpay.rpc.broadcast_transaction(args,
                          api=broadcast_api)
            except Exception as e:
                self.clear()
                raise e

            self.clear()
            return ret

    def clear(self):
        self.ops = []
        self.wifs = set()
        self.signing_accounts = []
        self['expiration'] = None
        super(TransactionBuilder, self).__init__({})

    def addSigningInformation(self, account, permission, reconstruct_tx=False):
        """ This is a private method that adds side information to a
            unsigned/partial transaction in order to simplify later
            signing (e.g. for multisig or coldstorage)

            Not needed when "appendWif" was already or is going to be used

            FIXME: Does not work with owner keys!

            :param bool reconstruct_tx: when set to False and tx
                is already contructed, it will not reconstructed
                and already added signatures remain

        """
        if not self._is_constructed() or self._is_constructed() and reconstruct_tx:
            self.constructTx()
        else:
            self['blockchain'] = self.dpay.chain_params
            if isinstance(account, PublicKey):
                self['missing_signatures'] = [str(account)]
            else:
                accountObj = Account(account, dpay_instance=(self.dpay))
                authority = accountObj[permission]
                self.update({'required_authorities': {accountObj['name']: authority}})
                for account_auth in authority['account_auths']:
                    account_auth_account = Account((account_auth[0]), dpay_instance=(self.dpay))
                    self['required_authorities'].update({account_auth[0]: account_auth_account.get(permission)})

                self['missing_signatures'] = [x[0] for x in authority['key_auths']]
                for account_auth in authority['account_auths']:
                    account_auth_account = Account((account_auth[0]), dpay_instance=(self.dpay))
                    self['missing_signatures'].extend([x[0] for x in account_auth_account[permission]['key_auths']])

    def appendMissingSignatures(self):
        """ Store which accounts/keys are supposed to sign the transaction

            This method is used for an offline-signer!
        """
        missing_signatures = self.get('missing_signatures', [])
        for pub in missing_signatures:
            try:
                wif = self.dpay.wallet.getPrivateKeyForPublicKey(pub)
                if wif:
                    self.appendWif(wif)
            except MissingKeyError:
                wif = None