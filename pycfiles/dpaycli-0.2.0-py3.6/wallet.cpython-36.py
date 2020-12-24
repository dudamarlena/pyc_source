# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/dpaycli/wallet.py
# Compiled at: 2018-10-15 03:27:18
# Size of source mod 2**32: 23692 bytes
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from builtins import str, bytes
from builtins import object
import logging, os, hashlib
from dpaycligraphenebase import bip38
from dpaycligraphenebase.account import PrivateKey
from dpaycli.instance import shared_dpay_instance
from .account import Account
from .aes import AESCipher
from .exceptions import MissingKeyError, InvalidWifError, WalletExists, WalletLocked, WrongMasterPasswordException, NoWalletException, OfflineHasNoRPCException, AccountDoesNotExistsException
from dpaycliapi.exceptions import NoAccessApi
from dpaycligraphenebase.py23 import py23_bytes
from .storage import configStorage as config
try:
    import keyring
    if not isinstance(keyring.get_keyring(), keyring.backends.fail.Keyring):
        KEYRING_AVAILABLE = True
    else:
        KEYRING_AVAILABLE = False
except ImportError:
    KEYRING_AVAILABLE = False

log = logging.getLogger(__name__)

class Wallet(object):
    __doc__ = ' The wallet is meant to maintain access to private keys for\n        your accounts. It either uses manually provided private keys\n        or uses a SQLite database managed by storage.py.\n\n        :param DPayNodeRPC rpc: RPC connection to a DPay node\n        :param array,dict,string keys: Predefine the wif keys to shortcut the\n               wallet database\n\n        Three wallet operation modes are possible:\n\n        * **Wallet Database**: Here, dpaycli loads the keys from the\n          locally stored wallet SQLite database (see ``storage.py``).\n          To use this mode, simply call ``DPay()`` without the\n          ``keys`` parameter\n        * **Providing Keys**: Here, you can provide the keys for\n          your accounts manually. All you need to do is add the wif\n          keys for the accounts you want to use as a simple array\n          using the ``keys`` parameter to ``DPay()``.\n        * **Force keys**: This more is for advanced users and\n          requires that you know what you are doing. Here, the\n          ``keys`` parameter is a dictionary that overwrite the\n          ``active``, ``owner``, ``posting`` or ``memo`` keys for\n          any account. This mode is only used for *foreign*\n          signatures!\n\n        A new wallet can be created by using:\n\n        .. code-block:: python\n\n           from dpaycli import DPay\n           dpay = DPay()\n           dpay.wallet.wipe(True)\n           dpay.wallet.create("supersecret-passphrase")\n\n        This will raise an exception if you already have a wallet installed.\n\n\n        The wallet can be unlocked for signing using\n\n        .. code-block:: python\n\n           from dpaycli import DPay\n           dpay = DPay()\n           dpay.wallet.unlock("supersecret-passphrase")\n\n        A private key can be added by using the\n        :func:`dpay.wallet.Wallet.addPrivateKey` method that is available\n        **after** unlocking the wallet with the correct passphrase:\n\n        .. code-block:: python\n\n           from dpaycli import DPay\n           dpay = DPay()\n           dpay.wallet.unlock("supersecret-passphrase")\n           dpay.wallet.addPrivateKey("5xxxxxxxxxxxxxxxxxxxx")\n\n        .. note:: The private key has to be either in hexadecimal or in wallet\n                  import format (wif) (starting with a ``5``).\n\n    '
    masterpassword = None
    configStorage = None
    MasterPassword = None
    keyStorage = None
    tokenStorage = None
    keys = {}
    token = {}
    keyMap = {}

    def __init__(self, dpay_instance=None, *args, **kwargs):
        self.dpay = dpay_instance or shared_dpay_instance()
        if 'wif' in kwargs:
            if 'keys' not in kwargs:
                kwargs['keys'] = kwargs['wif']
        else:
            master_password_set = False
            if 'keys' in kwargs:
                self.setKeys(kwargs['keys'])
            else:
                from .storage import keyStorage, MasterPassword
                self.MasterPassword = MasterPassword
                master_password_set = True
                self.keyStorage = keyStorage
            if 'token' in kwargs:
                self.setToken(kwargs['token'])
            else:
                from .storage import tokenStorage
            if not master_password_set:
                from .storage import MasterPassword
                self.MasterPassword = MasterPassword
            self.tokenStorage = tokenStorage

    @property
    def prefix(self):
        if self.dpay.is_connected():
            prefix = self.dpay.prefix
        else:
            prefix = config['prefix']
        return prefix or 'DWB'

    @property
    def rpc(self):
        if not self.dpay.is_connected():
            raise OfflineHasNoRPCException('No RPC available in offline mode!')
        return self.dpay.rpc

    def setKeys(self, loadkeys):
        """ This method is strictly only for in memory keys that are
            passed to Wallet/DPay with the ``keys`` argument
        """
        log.debug('Force setting of private keys. Not using the wallet database!')
        self.clear_local_keys()
        if isinstance(loadkeys, dict):
            Wallet.keyMap = loadkeys
            loadkeys = list(loadkeys.values())
        else:
            if not isinstance(loadkeys, list):
                loadkeys = [
                 loadkeys]
        for wif in loadkeys:
            pub = self._get_pub_from_wif(wif)
            Wallet.keys[pub] = str(wif)

    def setToken(self, loadtoken):
        """ This method is strictly only for in memory token that are
            passed to Wallet/DPay with the ``token`` argument
        """
        log.debug('Force setting of private token. Not using the wallet database!')
        self.clear_local_token()
        if isinstance(loadtoken, dict):
            Wallet.token = loadtoken
        else:
            raise ValueError('token must be a dict variable!')

    def unlock(self, pwd=None):
        """ Unlock the wallet database
        """
        if not self.created():
            raise NoWalletException
        if not pwd:
            self.tryUnlockFromEnv()
        elif self.masterpassword is None:
            if config[self.MasterPassword.config_key]:
                self.masterpwd = self.MasterPassword(pwd)
                self.masterpassword = self.masterpwd.decrypted_master

    def tryUnlockFromEnv(self):
        """ Try to fetch the unlock password from UNLOCK environment variable and keyring when no password is given.
        """
        password_storage = self.dpay.config['password_storage']
        if password_storage == 'environment':
            if 'UNLOCK' in os.environ:
                log.debug('Trying to use environmental variable to unlock wallet')
                pwd = os.environ.get('UNLOCK')
                self.unlock(pwd)
        elif password_storage == 'keyring':
            if KEYRING_AVAILABLE:
                log.debug('Trying to use keyring to unlock wallet')
                pwd = keyring.get_password('dpaycli', 'wallet')
                self.unlock(pwd)
        else:
            raise WrongMasterPasswordException

    def lock(self):
        """ Lock the wallet database
        """
        self.masterpassword = None

    def unlocked(self):
        """ Is the wallet database unlocked?
        """
        return not self.locked()

    def locked(self):
        """ Is the wallet database locked?
        """
        if Wallet.keys:
            return False
        else:
            try:
                self.tryUnlockFromEnv()
            except WrongMasterPasswordException:
                pass

            return not bool(self.masterpassword)

    def changePassphrase(self, new_pwd):
        """ Change the passphrase for the wallet database
        """
        if self.locked():
            raise AssertionError()
        self.masterpwd.changePassword(new_pwd)

    def created(self):
        """ Do we have a wallet database already?
        """
        if len(self.getPublicKeys()):
            return True
        else:
            if self.MasterPassword.config_key in config:
                return True
            return False

    def create(self, pwd):
        """ Alias for newWallet()
        """
        self.newWallet(pwd)

    def newWallet(self, pwd):
        """ Create a new wallet database
        """
        if self.created():
            raise WalletExists('You already have created a wallet!')
        self.masterpwd = self.MasterPassword(pwd)
        self.masterpassword = self.masterpwd.decrypted_master
        self.masterpwd.saveEncrytpedMaster()

    def wipe(self, sure=False):
        """ Purge all data in wallet database
        """
        if not sure:
            log.error('You need to confirm that you are sure and understand the implications of wiping your wallet!')
            return
        from .storage import keyStorage, tokenStorage, MasterPassword
        MasterPassword.wipe(sure)
        keyStorage.wipe(sure)
        tokenStorage.wipe(sure)
        self.clear_local_keys()

    def clear_local_keys(self):
        """Clear all manually provided keys"""
        Wallet.keys = {}
        Wallet.keyMap = {}

    def clear_local_token(self):
        """Clear all manually provided token"""
        Wallet.token = {}

    def encrypt_wif(self, wif):
        """ Encrypt a wif key
        """
        if self.locked():
            raise AssertionError()
        return format(bip38.encrypt(PrivateKey(wif, prefix=(self.prefix)), self.masterpassword), 'encwif')

    def decrypt_wif(self, encwif):
        """ decrypt a wif key
        """
        try:
            PrivateKey(encwif, prefix=(self.prefix))
            return encwif
        except (ValueError, AssertionError):
            pass

        if self.locked():
            raise AssertionError()
        return format(bip38.decrypt(encwif, self.masterpassword), 'wif')

    def deriveChecksum(self, s):
        """ Derive the checksum
        """
        checksum = hashlib.sha256(py23_bytes(s, 'ascii')).hexdigest()
        return checksum[:4]

    def encrypt_token(self, token):
        """ Encrypt a token key
        """
        if self.locked():
            raise AssertionError()
        aes = AESCipher(self.masterpassword)
        return '{}${}'.format(self.deriveChecksum(token), aes.encrypt(token))

    def decrypt_token(self, enctoken):
        """ decrypt a wif key
        """
        if self.locked():
            raise AssertionError()
        aes = AESCipher(self.masterpassword)
        checksum, encrypted_token = enctoken.split('$')
        try:
            decrypted_token = aes.decrypt(encrypted_token)
        except:
            raise WrongMasterPasswordException

        if checksum != self.deriveChecksum(decrypted_token):
            raise WrongMasterPasswordException
        return decrypted_token

    def _get_pub_from_wif(self, wif):
        """ Get the pubkey as string, from the wif key as string
        """
        if isinstance(wif, PrivateKey):
            wif = str(wif)
        try:
            return format(PrivateKey(wif).pubkey, self.prefix)
        except:
            raise InvalidWifError('Invalid Private Key Format. Please use WIF!')

    def addToken(self, name, token):
        if self.tokenStorage:
            if not self.created():
                raise NoWalletException
            self.tokenStorage.add(name, self.encrypt_token(token))

    def getTokenForAccountName(self, name):
        """ Obtain the private token for a given public name

            :param str name: Public name
        """
        if Wallet.token:
            if name in Wallet.token:
                return Wallet.token[name]
            raise MissingKeyError('No private token for {} found'.format(name))
        else:
            if not self.created():
                raise NoWalletException
            else:
                if not self.unlocked():
                    raise WalletLocked
                enctoken = self.tokenStorage.getTokenForPublicName(name)
                raise enctoken or MissingKeyError('No private token for {} found'.format(name))
            return self.decrypt_token(enctoken)

    def removeTokenFromPublicName(self, name):
        """ Remove a token from the wallet database

            :param str name: token to be removed
        """
        if self.tokenStorage:
            if not self.created():
                raise NoWalletException
            self.tokenStorage.delete(name)

    def addPrivateKey(self, wif):
        """Add a private key to the wallet database

            :param str wif: Private key
        """
        pub = self._get_pub_from_wif(wif)
        if isinstance(wif, PrivateKey):
            wif = str(wif)
        if self.keyStorage:
            if not self.created():
                raise NoWalletException
            self.keyStorage.add(self.encrypt_wif(wif), pub)

    def getPrivateKeyForPublicKey(self, pub):
        """ Obtain the private key for a given public key

            :param str pub: Public Key
        """
        if Wallet.keys:
            if pub in Wallet.keys:
                return Wallet.keys[pub]
            raise MissingKeyError('No private key for {} found'.format(pub))
        else:
            if not self.created():
                raise NoWalletException
            else:
                if not self.unlocked():
                    raise WalletLocked
                encwif = self.keyStorage.getPrivateKeyForPublicKey(pub)
                raise encwif or MissingKeyError('No private key for {} found'.format(pub))
            return self.decrypt_wif(encwif)

    def removePrivateKeyFromPublicKey(self, pub):
        """ Remove a key from the wallet database

            :param str pub: Public key
        """
        if self.keyStorage:
            if not self.created():
                raise NoWalletException
            self.keyStorage.delete(pub)

    def removeAccount(self, account):
        """ Remove all keys associated with a given account

            :param str account: name of account to be removed
        """
        accounts = self.getAccounts()
        for a in accounts:
            if a['name'] == account:
                self.removePrivateKeyFromPublicKey(a['pubkey'])

    def getKeyForAccount(self, name, key_type):
        """ Obtain `key_type` Private Key for an account from the wallet database

            :param str name: Account name
            :param str key_type: key type, has to be one of "owner", "active",
                "posting" or "memo"
        """
        if key_type not in ('owner', 'active', 'posting', 'memo'):
            raise AssertionError('Wrong key type')
        else:
            if key_type in Wallet.keyMap:
                return Wallet.keyMap.get(key_type)
            else:
                if self.rpc.get_use_appbase():
                    account = self.rpc.find_accounts({'accounts': [name]}, api='database')['accounts']
                else:
                    account = self.rpc.get_account(name)
            if not account:
                return
            if len(account) == 0:
                return
        if key_type == 'memo':
            key = self.getPrivateKeyForPublicKey(account[0]['memo_key'])
            if key:
                return key
        else:
            key = None
            for authority in account[0][key_type]['key_auths']:
                try:
                    key = self.getPrivateKeyForPublicKey(authority[0])
                    if key:
                        return key
                except MissingKeyError:
                    key = None

            if key is None:
                raise MissingKeyError('No private key for {} found'.format(name))
            return

    def getKeysForAccount(self, name, key_type):
        """ Obtain a List of `key_type` Private Keys for an account from the wallet database

            :param str name: Account name
            :param str key_type: key type, has to be one of "owner", "active",
                "posting" or "memo"
        """
        if key_type not in ('owner', 'active', 'posting', 'memo'):
            raise AssertionError('Wrong key type')
        else:
            if key_type in Wallet.keyMap:
                return Wallet.keyMap.get(key_type)
            else:
                if self.rpc.get_use_appbase():
                    account = self.rpc.find_accounts({'accounts': [name]}, api='database')['accounts']
                else:
                    account = self.rpc.get_account(name)
            if not account:
                return
            if len(account) == 0:
                return
        if key_type == 'memo':
            key = self.getPrivateKeyForPublicKey(account[0]['memo_key'])
            if key:
                return [
                 key]
        else:
            keys = []
            key = None
            for authority in account[0][key_type]['key_auths']:
                try:
                    key = self.getPrivateKeyForPublicKey(authority[0])
                    if key:
                        keys.append(key)
                except MissingKeyError:
                    key = None

            if key is None:
                raise MissingKeyError('No private key for {} found'.format(name))
            return keys
            return

    def getOwnerKeyForAccount(self, name):
        """ Obtain owner Private Key for an account from the wallet database
        """
        return self.getKeyForAccount(name, 'owner')

    def getMemoKeyForAccount(self, name):
        """ Obtain owner Memo Key for an account from the wallet database
        """
        return self.getKeyForAccount(name, 'memo')

    def getActiveKeyForAccount(self, name):
        """ Obtain owner Active Key for an account from the wallet database
        """
        return self.getKeyForAccount(name, 'active')

    def getPostingKeyForAccount(self, name):
        """ Obtain owner Posting Key for an account from the wallet database
        """
        return self.getKeyForAccount(name, 'posting')

    def getOwnerKeysForAccount(self, name):
        """ Obtain list of all owner Private Keys for an account from the wallet database
        """
        return self.getKeysForAccount(name, 'owner')

    def getActiveKeysForAccount(self, name):
        """ Obtain list of all owner Active Keys for an account from the wallet database
        """
        return self.getKeysForAccount(name, 'active')

    def getPostingKeysForAccount(self, name):
        """ Obtain list of all owner Posting Keys for an account from the wallet database
        """
        return self.getKeysForAccount(name, 'posting')

    def getAccountFromPrivateKey(self, wif):
        """ Obtain account name from private key
        """
        pub = self._get_pub_from_wif(wif)
        return self.getAccountFromPublicKey(pub)

    def getAccountsFromPublicKey(self, pub):
        """ Obtain all account names associated with a public key

            :param str pub: Public key
        """
        if not self.dpay.is_connected():
            raise OfflineHasNoRPCException('No RPC available in offline mode!')
        else:
            self.dpay.rpc.set_next_node_on_empty_reply(False)
            if self.dpay.rpc.get_use_appbase():
                names = self.dpay.rpc.get_key_references({'keys': [pub]}, api='account_by_key')['accounts']
            else:
                names = self.dpay.rpc.get_key_references([pub], api='account_by_key')
        for name in names:
            for i in name:
                yield i

    def getAccountFromPublicKey(self, pub):
        """ Obtain the first account name from public key

            :param str pub: Public key

            Note: this returns only the first account with the given key. To
            get all accounts associated with a given public key, use
            ``getAccountsFromPublicKey``.
        """
        names = list(self.getAccountsFromPublicKey(pub))
        if not names:
            return
        else:
            return names[0]

    def getAllAccounts(self, pub):
        """ Get the account data for a public key (all accounts found for this
            public key)

            :param str pub: Public key
        """
        for name in self.getAccountsFromPublicKey(pub):
            try:
                account = Account(name, dpay_instance=(self.dpay))
            except AccountDoesNotExistsException:
                continue

            yield {'name':account['name'], 
             'account':account, 
             'type':self.getKeyType(account, pub), 
             'pubkey':pub}

    def getAccount(self, pub):
        """ Get the account data for a public key (first account found for this
            public key)

            :param str pub: Public key
        """
        name = self.getAccountFromPublicKey(pub)
        if not name:
            return {'name':None, 
             'type':None,  'pubkey':pub}
        try:
            account = Account(name, dpay_instance=(self.dpay))
        except:
            return
            return {'name':account['name'], 
             'account':account, 
             'type':self.getKeyType(account, pub), 
             'pubkey':pub}

    def getKeyType(self, account, pub):
        """ Get key type

            :param dpaycli.account.Account/dict account: Account data
            :param str pub: Public key

        """
        for authority in ('owner', 'active', 'posting'):
            for key in account[authority]['key_auths']:
                if pub == key[0]:
                    return authority

        if pub == account['memo_key']:
            return 'memo'

    def getAccounts(self):
        """ Return all accounts installed in the wallet database
        """
        pubkeys = self.getPublicKeys()
        accounts = []
        for pubkey in pubkeys:
            if pubkey[:len(self.prefix)] == self.prefix:
                accounts.extend(self.getAllAccounts(pubkey))

        return accounts

    def getPublicKeys(self):
        """ Return all installed public keys
        """
        if self.keyStorage:
            return self.keyStorage.getPublicKeys()
        else:
            return list(Wallet.keys.keys())

    def getPublicNames(self):
        """ Return all installed public token
        """
        if self.tokenStorage:
            return self.tokenStorage.getPublicNames()
        else:
            return list(Wallet.token.keys())