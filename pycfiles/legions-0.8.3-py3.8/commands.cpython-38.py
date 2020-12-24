# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/legions/commands/commands.py
# Compiled at: 2020-05-07 10:49:55
# Size of source mod 2**32: 21066 bytes
import asyncio, os, socket, typing, requests
from nubia import command, argument
from termcolor import cprint
import legions.context as context
from legions.version import __version__
from legions.network.web3 import Web3
from legions.utils.helper_functions import getChainName
INFURA_URL = 'https://mainnet.infura.io/v3/c3914c0859de473b9edcd6f723b4ea69'
PEER_SAMPLE = 'enode://000331f91e4343a7145be69f1d455b470d9ba90bdb6d74fe671b28af481361c931b632f03c03dde5ec4c34f2289064ccd4775f758fb95e9496a1bd5a619ae0fe@lfbn-lyo-1-210-35.w86-202.abo.wanadoo.fr:30303'
w3 = Web3()
w3.connect(INFURA_URL)
LEGION_TEST_PASS = 'Legion2019'
LEGION_TEST_PRV = '0x28d96497361cfc7cde5f253232d1ea300333891792d5922991d98683e1fb05c6'
Protocols = [
 'http', 'rpc', 'ipc', 'ws']
host = None

@command(aliases=['sethost'])
@argument('host', description='Address of the RPC Node', aliases=['u'])
def sethost(host: str):
    """
    Setup the Web3 connection (RPC, IPC, HTTP) - This should be the first step 
    """
    if host is None:
        cprint("Missing Argument 'host'?", 'red')
        return 0
    else:
        ctx = context.get_context()
        cprint('Input: {}'.format(host), 'yellow')
        cprint('Verbose? {}'.format(ctx.verbose), 'yellow')
        w3.connect(host)
        if w3.isConnected():
            cprint('Web3 API Version: {}'.format(w3.api), 'green')
            cprint('connected to: {}'.format(w3.node_uri), 'green')
            cprint('Version: {}'.format(w3.clientVersion), 'green')
        else:
            cprint('Web3 API Version: {}'.format(w3.api), 'red')
        cprint('Cannot connect to: {} '.format(host), 'red')
    return 0


@command('getnodeinfo')
def getnodeinfo():
    """
    Prints information about the node (run setnode before this) 
    """
    if w3.isConnected():
        cprint('Web3 API Version: {}'.format(w3.api), 'white')
        cprint('connected to: {}'.format(w3.node_uri), 'white')
        cprint('Version: {}'.format(w3.clientVersion), 'green')
        cprint('----------------------------------------------------------------')
        cprint('Last Block Number: {}'.format(w3.eth.blockNumber), 'green')
        cprint('Chain: {} (ChainID: {})'.format(getChainName(w3.eth.chainId), w3.eth.chainId), 'green')
        cprint('Protocol Version: {}'.format(w3.eth.protocolVersion), 'green')
        cprint('Is Listening: {}'.format(w3.net.listening), 'green')
        cprint('Peer Count: {}'.format(w3.net.peerCount), 'green')
        cprint('Is Syncing: {}'.format(w3.eth.syncing), 'green')
        cprint('Is Mining: {}'.format(w3.eth.mining), 'green')
        cprint('Hash Rate: {}'.format(w3.eth.hashrate), 'green')
        cprint('Gas Price: {}'.format(w3.eth.gasPrice), 'green')
        cprint('----------------------------------------------------------------')
        try:
            cprint('Coinbase Account: {}'.format(w3.eth.coinbase), 'green')
        except Exception as e:
            try:
                cprint('Coinbase not available: {}'.format(e), 'red')
            finally:
                e = None
                del e

        else:
            cprint('Accounts', 'green')
            for account in w3.eth.accounts:
                cprint('- {}'.format(account), 'green')

    else:
        cprint('Web3 API Version: {}'.format(w3.api), 'red')
        cprint('Cannot connect to: {} '.format(host), 'red')
        cprint('Did you run sethost?', 'red')
    return 0


@command('version')
def version():
    """
    Print Versions (If connected to a node it will print the host version too)
    """
    cprint('Legion Version: {}'.format(__version__), 'white')
    cprint('Web3 API Version: {}'.format(w3.api), 'white')
    if w3.isConnected():
        cprint('connected to: {}'.format(w3.node_uri), 'green')
        cprint('Version: {}'.format(w3.clientVersion), 'green')
    else:
        cprint('Not connected to any hosts.', 'red')


@command
class Investigate:
    __doc__ = 'Investigate further in the node (e.g. check if accounts are unlocked, etc)'

    def __init__(self) -> None:
        if not w3.isConnected():
            cprint('Web3 API Version: {}'.format(w3.api), 'red')
            cprint('Cannot connect to: {} '.format(host), 'red')
            cprint('Did you run sethost?', 'red')
            return None

    @command('accounts')
    @argument('all', description='Show me all the details', aliases=['A'])
    @argument('intrusive',
      description='Be intrusive, try to make new accounts, etc',
      aliases=[
     'i'])
    def investigate_accounts(self, all: bool=True, intrusive: bool=True):
        """
        Investigate accounts (e.g. check if accounts are unlocked, etc)
        """
        if w3.isConnected():
            coinbase = None
            try:
                coinbase = w3.eth.coinbase
            except Exception as e:
                try:
                    cprint('Coinbase not available: {}'.format(e), 'red')
                finally:
                    e = None
                    del e

            else:
                accounts = w3.eth.accounts
                if len(accounts) == 0:
                    cprint('No accounts found', 'red')
                    if type(coinbase) is None:
                        cprint('Nothing to do here')
                        return 0
                elif all:
                    for account in accounts:
                        cprint('Balance of {} is : {}'.format(account, w3.eth.getBalance(account)), 'white')

                else:
                    cprint('Number of Accounts: {}'.format(len(w3.eth.accounts)), 'green')
                if 'parity' in w3.clientVersion.lower():
                    ww3 = w3.parity
                else:
                    if 'geth' in w3.clientVersion.lower():
                        ww3 = w3.geth
                    elif intrusive:
                        try:
                            cprint('importRawKey: {}'.format(ww3.personal.importRawKey(LEGION_TEST_PRV, LEGION_TEST_PASS)), 'green')
                        except Exception as e:
                            try:
                                cprint('importRawKey: {}'.format(e), 'yellow')
                            finally:
                                e = None
                                del e

                        try:
                            cprint('newAccount: {}'.format(ww3.personal.newAccount(LEGION_TEST_PASS)), 'white')
                        except Exception as e:
                            try:
                                cprint('newAccount: {}'.format(e), 'yellow')
                            finally:
                                e = None
                                del e

                cprint('----------------------------------------------------------------')

    @command('admin')
    @argument('intrusive',
      description='Be intrusive, try to add peers, etc', aliases=['i'])
    def investigate_admin(self, intrusive: bool=False):
        """
        Investigate accounts (e.g. functionalities under the admin_ namespace)
        """
        cprint('clientVersion: {}'.format(w3.clientVersion), 'white')
        if 'geth' in w3.clientVersion.lower():
            if intrusive:
                try:
                    cprint('AddPeer: {}'.format(w3.geth.admin.add_peer(PEER_SAMPLE)), 'green')
                except Exception as e:
                    try:
                        cprint('AddPeer: {}'.format(e), 'yellow')
                    finally:
                        e = None
                        del e

                else:
                    try:
                        cprint('datadir: {}'.format(w3.geth.admin.datadir()), 'green')
                    except Exception as e:
                        try:
                            cprint('datadir: {}'.format(e), 'yellow')
                        finally:
                            e = None
                            del e

                    else:
                        try:
                            cprint('nodeInfo: {}'.format(w3.geth.admin.nodeInfo()), 'green')
                        except Exception as e:
                            try:
                                cprint('nodeInfo {}'.format(e), 'yellow')
                            finally:
                                e = None
                                del e

                        else:
                            try:
                                cprint('peers: {}'.format(w3.geth.admin.peers()), 'green')
                            except Exception as e:
                                try:
                                    cprint('peers {}'.format(e), 'yellow')
                                finally:
                                    e = None
                                    del e

                            else:
                                try:
                                    cprint('txpool.status: {}'.format(w3.geth.txpool.status()), 'green')
                                except Exception as e:
                                    try:
                                        cprint('txpool.status {}'.format(e), 'yellow')
                                    finally:
                                        e = None
                                        del e

                                try:
                                    cprint('shh.version: {}'.format(w3.geth.shh.version()), 'green')
                                except Exception as e:
                                    try:
                                        cprint('shh.version: {}'.format(e), 'yellow')
                                    finally:
                                        e = None
                                        del e

                                try:
                                    cprint('Wshh.info: {}'.format(w3.geth.shh.info()), 'green')
                                except Exception as e:
                                    try:
                                        cprint('shh.info: {}'.format(e), 'yellow')
                                    finally:
                                        e = None
                                        del e

            else:
                pass
        if 'parity' in w3.clientVersion.lower():
            try:
                cprint('versionInfo: {}'.format(w3.parity_versionInfo()), 'green')
            except Exception as e:
                try:
                    cprint('versionInfo: {}'.format(e), 'yellow')
                finally:
                    e = None
                    del e

    @command('sign')
    def investigate_sign(self, msg: str='Legions Test', account: str=None, intrusive: bool=True):
        """
        Investigate signature functionalities 
        """
        if w3.isConnected():
            coinbase = None
            try:
                coinbase = w3.eth.coinbase
            except Exception as e:
                try:
                    cprint('Coinbase not available: {}'.format(e), 'red')
                finally:
                    e = None
                    del e

            else:
                accounts = w3.eth.accounts
                if len(accounts) == 0:
                    cprint('No accounts found', 'red')
                    if type(coinbase) is None:
                        cprint('Nothing to do here')
                        return 0
                if account is None:
                    for account in accounts:
                        try:
                            cprint('Signing "{}" by "{}" \n=> "{}"'.format(msg, account, w3.eth.sign(account, text=msg).hex()), 'white')
                        except Exception as e:
                            try:
                                cprint('failed to sign by {}: '.format(account, e))
                            finally:
                                e = None
                                del e

                else:
                    try:
                        cprint('Signing "{}" by "{}" \n=> "{}"'.format(msg, account, w3.eth.sign(account, text=msg).hex()), 'white')
                    except Exception as e:
                        try:
                            cprint('failed to sign by {}: '.format(account, e))
                        finally:
                            e = None
                            del e


@command
class Query:
    __doc__ = 'Query Blockchain (Storage, balance, etc)'

    def __init__(self) -> None:
        if not w3.isConnected():
            cprint('Web3 API Version: {}'.format(w3.api), 'white')
            cprint('Not using a custom node. Run sethost to connect to your node', 'red')
            os.environ['WEB3_PROVIDER_URI'] = INFURA_URL
            cprint('Connecting to Infura...', 'green')

    @command('balance')
    @argument('address', description='Address of the account', aliases=['a'])
    @argument('block',
      description='(Optional) Block number for the query (default latest)',
      aliases=[
     'b'])
    def get_balance(self, address: str, block: int=None):
        """
        Get Balance of an account
        """
        if address is None:
            cprint("Missing Argument 'address'?", 'red')
            return 0
        if block is None:
            block = w3.eth.blockNumber
        address = Web3.toChecksumAddress(address)
        balance = w3.eth.getBalance(address, block_identifier=block)
        cprint('Balance of {} is : {} wei ({} Eth)'.format(address, balance, Web3.fromWei(balance, 'ether')), 'green')

    @command('storage')
    @argument('address', description='Address of the account', aliases=['a'])
    @argument('count', description='Number of storage slots to read', aliases=['i'])
    @argument('block',
      description='(Optional) Block number for the query (default latest)',
      aliases=[
     'b'])
    def get_storage(self, address: str, count: int=10, block: int=None):
        """
        Get the first "count" number of an address. count default = 10
        """
        if address is None:
            cprint("Missing Argument 'address'?", 'red')
            return 0
        if block is None:
            block = w3.eth.blockNumber
        address = Web3.toChecksumAddress(address)
        for i in range(0, count):
            hex_text = None
            try:
                hex_text = Web3.toText(w3.eth.getStorageAt(address, i, block_identifier=block))
            except:
                try:
                    hex_text = Web3.toInt(w3.eth.getStorageAt(address, i, block_identifier=block))
                except:
                    hex_text = None

            else:
                cprint('Storage {} = {} ({})'.format(i, Web3.toHex(w3.eth.getStorageAt(address, i, block_identifier=block)), hex_text), 'green')

    @command('code')
    @argument('address', description='Address of the account', aliases=['a'])
    @argument('block',
      description='(Optional) Block number for the query (default latest)',
      aliases=[
     'b'])
    def get_code(self, address: str, block: int=None):
        """
        Get code of the smart contract at address
        """
        if address is None:
            cprint("Missing Argument 'address'?", 'red')
            return 0
        if block is None:
            block = w3.eth.blockNumber
        address = Web3.toChecksumAddress(address)
        cprint('Code of {} = \n {}'.format(address, Web3.toHex(w3.eth.getCode(address, block_identifier=block))), 'yellow')

    @command('block')
    @argument('block', description='Block number (default latest)', aliases=['b'])
    def get_block(self, block: int=None):
        """
        Get block details by block number
        """
        if block is None:
            block = w3.eth.blockNumber
        cprint('block {} details = \n {}'.format(block, w3.eth.getBlock(block_identifier=block)), 'yellow')

    @command('transaction')
    @argument('hash', description='Transaction hash to query', aliases=['t'])
    @argument('block',
      description='(Optional) Block number for the query (default latest)',
      aliases=[
     'b'])
    def get_transaction(self, hash: str, block: int=None):
        """
        Get transaction details by hash
        """
        if hash is None:
            cprint("Missing Argument 'hash'?", 'red')
            return 0
        if block is None:
            block = w3.eth.blockNumber
        cprint('transaction {} details = \n {}'.format(hash, w3.eth.getTransaction(hash)), 'yellow')

    @command('command')
    @argument('method', description='RPC Method to be used (e.g. eth_getBalance)')
    @argument('args', description='Arguments for the RPC method (comma separated)')
    @argument('block',
      description='(Optional) Block number for the query (default latest)',
      aliases=[
     'b'])
    def get_transaction(self, method: str, args: str=None, block: int=None):
        """
        Manual RPC method with args
        """
        if method is None:
            cprint("Missing Argument 'method'?", 'red')
            return 0
            if block is None:
                block = w3.eth.blockNumber
        else:
            try:
                cprint('{}({}): {} \n'.format(method, args, w3.manager.request_blocking(method, [str(args), block])), 'green')
            except Exception as e:
                try:
                    cprint('failed {}({}) :  {} \n'.format(method, args, e), 'yellow')
                finally:
                    e = None
                    del e

    @command('ecrecover')
    @argument('data', description='The data which hash was signed')
    @argument('dataHash', description='The hash of the data')
    @argument('signedData', description='Signed data')
    def get_ecrecover(self, signedData: str, data: str=None, dataHash: str=None):
        """
        Get address associated with the signature (ecrecover)
        """
        if data is None:
            if dataHash is None:
                cprint("Missing Argument, either 'dataHash' or 'data' must be passed?", 'red')
                return 0
        try:
            if data is not None:
                from eth_account.messages import encode_defunct, _hash_eip191_message
                hex_message_hash = w3.toHex(_hash_eip191_message(encode_defunct(hexstr=data)))
            else:
                if dataHash is not None:
                    hex_message_hash = dataHash
            sig = w3.toBytes(hexstr=signedData)
            v, hex_r, hex_s = w3.toInt(sig[(-1)]), w3.toHex(sig[:32]), w3.toHex(sig[32:64])
            address = w3.eth.account.recoverHash(hex_message_hash, signature=sig)
            cprint('Address: {}'.format(address), 'green')
            cprint('r: {}\ns: {}\nv: {} '.format(hex_r, hex_s, v), 'white')
        except Exception as e:
            try:
                cprint('failed to get address: {} \n'.format(e), 'yellow')
            finally:
                e = None
                del e