# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/dpaycli/cli.py
# Compiled at: 2018-10-15 03:27:18
# Size of source mod 2**32: 124373 bytes
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from builtins import bytes, int, str
import os, ast, json, sys
from prettytable import PrettyTable
from datetime import datetime, timedelta
import pytz, time, math, random, logging, click, re
from dpaycli.instance import set_shared_dpay_instance, shared_dpay_instance
from dpaycli.amount import Amount
from dpaycli.price import Price
from dpaycli.account import Account
from dpaycli.dpay import DPay
from dpaycli.comment import Comment
from dpaycli.market import Market
from dpaycli.block import Block
from dpaycli.profile import Profile
from dpaycli.wallet import Wallet
from dpaycli.dpayid import DPayID
from dpaycli.asset import Asset
from dpaycli.witness import Witness, WitnessesRankedByVote, WitnessesVotedByAccount
from dpaycli.blockchain import Blockchain
from dpaycli.utils import formatTimeString, construct_authorperm
from dpaycli.vote import AccountVotes, ActiveVotes
from dpaycli import exceptions
from dpaycli.version import version as __version__
from dpaycli.asciichart import AsciiChart
from dpaycli.transactionbuilder import TransactionBuilder
from timeit import default_timer as timer
from dpayclibase import operations
from dpaycligraphenebase.account import PrivateKey, PublicKey, BrainKey
from dpaycligraphenebase.base58 import Base58
from dpaycli.nodelist import NodeList
from dpaycli.conveyor import Conveyor
from dpaycli.rc import RC
click.disable_unicode_literals_warning = True
log = logging.getLogger(__name__)
try:
    import keyring
    if not isinstance(keyring.get_keyring(), keyring.backends.fail.Keyring):
        KEYRING_AVAILABLE = True
    else:
        KEYRING_AVAILABLE = False
except ImportError:
    KEYRING_AVAILABLE = False

FUTURES_MODULE = None
if not FUTURES_MODULE:
    try:
        from concurrent.futures import ThreadPoolExecutor, wait, as_completed
        FUTURES_MODULE = 'futures'
    except ImportError:
        FUTURES_MODULE = None

availableConfigurationKeys = [
 'default_account',
 'default_vote_weight',
 'nodes',
 'password_storage',
 'client_id']

def prompt_callback(ctx, param, value):
    if value in ('yes', 'y', 'ye'):
        value = True
    else:
        print('Please write yes, ye or y to confirm!')
        ctx.abort()


def asset_callback(ctx, param, value):
    if value not in ('BEX', 'BBD'):
        print('Please BEX or BBD as asset!')
        ctx.abort()
    else:
        return value


def prompt_flag_callback(ctx, param, value):
    if not value:
        ctx.abort()


def unlock_wallet(stm, password=None):
    if stm.unsigned:
        if stm.nobroadcast:
            return True
        password_storage = stm.config['password_storage']
        if not password:
            if KEYRING_AVAILABLE:
                if password_storage == 'keyring':
                    password = keyring.get_password('dpaycli', 'wallet')
    else:
        if not password:
            if password_storage == 'environment':
                if 'UNLOCK' in os.environ:
                    password = os.environ.get('UNLOCK')
        if bool(password):
            stm.wallet.unlock(password)
        else:
            password = click.prompt('Password to unlock wallet', confirmation_prompt=False, hide_input=True)
            stm.wallet.unlock(password)
    if stm.wallet.locked():
        if password_storage == 'keyring' or password_storage == 'environment':
            print('Wallet could not be unlocked with %s!' % password_storage)
            password = click.prompt('Password to unlock wallet', confirmation_prompt=False, hide_input=True)
            if bool(password):
                unlock_wallet(stm, password=password)
                return stm.wallet.locked() or True
        else:
            print('Wallet could not be unlocked!')
        return False
    else:
        print('Wallet Unlocked!')
        return True


def node_answer_time(node):
    try:
        stm_local = DPay(node=node, num_retries=2, num_retries_call=2, timeout=10)
        start = timer()
        stm_local.get_config(use_stored_data=False)
        stop = timer()
        rpc_answer_time = stop - start
    except KeyboardInterrupt:
        rpc_answer_time = float('inf')
        raise KeyboardInterrupt()
    except:
        rpc_answer_time = float('inf')

    return rpc_answer_time


@click.group(chain=True)
@click.option('--node',
  '-n', default='', help='URL for public DPay API (e.g. https://api.dpays.io)')
@click.option('--offline',
  '-o', is_flag=True, default=False, help='Prevent connecting to network')
@click.option('--no-broadcast',
  '-d', is_flag=True, default=False, help='Do not broadcast')
@click.option('--no-wallet',
  '-p', is_flag=True, default=False, help='Do not load the wallet')
@click.option('--unsigned',
  '-x', is_flag=True, default=False, help='Nothing will be signed')
@click.option('--create-link',
  '-l', is_flag=True, default=False, help='Creates dpayid links from all broadcast operations')
@click.option('--dpayid',
  '-s', is_flag=True, default=False, help='Uses a dpayid token to broadcast (only broadcast operation with posting permission)')
@click.option('--expires',
  '-e', default=30, help='Delay in seconds until transactions are supposed to expire(defaults to 60)')
@click.option('--verbose',
  '-v', default=3, help='Verbosity')
@click.version_option(version=__version__)
def cli(node, offline, no_broadcast, no_wallet, unsigned, create_link, dpayid, expires, verbose):
    log = logging.getLogger(__name__)
    verbosity = ['critical', 'error', 'warn', 'info', 'debug'][int(min(verbose, 4))]
    log.setLevel(getattr(logging, verbosity.upper()))
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch = logging.StreamHandler()
    ch.setLevel(getattr(logging, verbosity.upper()))
    ch.setFormatter(formatter)
    log.addHandler(ch)
    if create_link:
        dpid = DPayID()
        no_broadcast = True
        unsigned = True
    else:
        dpid = None
    debug = verbose > 0
    stm = DPay(node=node,
      nobroadcast=no_broadcast,
      offline=offline,
      nowallet=no_wallet,
      unsigned=unsigned,
      use_dpid=dpayid,
      expiration=expires,
      dpayid=dpid,
      debug=debug,
      num_retries=10,
      num_retries_call=3,
      timeout=15,
      autoconnect=False)
    set_shared_dpay_instance(stm)


@cli.command()
@click.argument('key')
@click.argument('value')
def set(key, value):
    """ Set default_account, default_vote_weight or nodes

        set [key] [value]

        Examples:

        Set the default vote weight to 50 %:
        set default_vote_weight 50
    """
    stm = shared_dpay_instance()
    if key == 'default_account':
        if stm.rpc is not None:
            stm.rpc.rpcconnect()
        stm.set_default_account(value)
    else:
        if key == 'default_vote_weight':
            stm.set_default_vote_weight(value)
        else:
            if key == 'nodes' or key == 'node':
                if bool(value) or value != 'default':
                    stm.set_default_nodes(value)
                else:
                    stm.set_default_nodes('')
            else:
                if key == 'password_storage':
                    stm.config['password_storage'] = value
                    if KEYRING_AVAILABLE:
                        if value == 'keyring':
                            password = click.prompt('Password to unlock wallet (Will be stored in keyring)', confirmation_prompt=False, hide_input=True)
                            password = keyring.set_password('dpaycli', 'wallet', password)
                    if KEYRING_AVAILABLE:
                        if value != 'keyring':
                            try:
                                keyring.delete_password('dpaycli', 'wallet')
                            except keyring.errors.PasswordDeleteError:
                                print('')

                    if value == 'environment':
                        print('The wallet password can be stored in the UNLOCK environment variable to skip password prompt!')
                else:
                    if key == 'client_id':
                        stm.config['client_id'] = value
                    else:
                        if key == 'hot_sign_redirect_uri':
                            stm.config['hot_sign_redirect_uri'] = value
                        else:
                            if key == 'dpid_api_url':
                                stm.config['dpid_api_url'] = value
                            else:
                                if key == 'oauth_base_url':
                                    stm.config['oauth_base_url'] = value
                                else:
                                    print('wrong key')


@cli.command()
@click.option('--results', is_flag=True, default=False, help='Shows result of changing the node.')
def nextnode(results):
    """ Uses the next node in list
    """
    stm = shared_dpay_instance()
    if stm.rpc is not None:
        stm.rpc.rpcconnect()
    stm.move_current_node_to_front()
    node = stm.get_default_nodes()
    offline = stm.offline
    if len(node) < 2:
        print('At least two nodes are needed!')
        return
    node = node[1:] + [node[0]]
    if not offline:
        stm.rpc.next()
        stm.get_blockchain_version()
    else:
        while not offline and node[0] != stm.rpc.url and len(node) > 1:
            node = node[1:] + [node[0]]

        stm.set_default_nodes(node)
        if not results:
            return
        t = PrettyTable(['Key', 'Value'])
        t.align = 'l'
        if not offline:
            t.add_row(['Node-Url', stm.rpc.url])
        else:
            t.add_row(['Node-Url', node[0]])
        if not offline:
            t.add_row(['Version', stm.get_blockchain_version()])
        else:
            t.add_row(['Version', 'dpay is in offline mode...'])
    print(t)


@cli.command()
@click.option('--raw',
  is_flag=True, default=False, help='Returns only the raw value')
@click.option('--sort',
  is_flag=True, default=False, help='Sort all nodes by ping value')
@click.option('--remove',
  is_flag=True, default=False, help='Remove node with errors from list')
@click.option('--threading',
  is_flag=True, default=False, help='Use a thread for each node')
def pingnode(raw, sort, remove, threading):
    """ Returns the answer time in milliseconds
    """
    stm = shared_dpay_instance()
    if stm.rpc is not None:
        stm.rpc.rpcconnect()
    else:
        nodes = stm.get_default_nodes()
        if not raw:
            t = PrettyTable(['Node', 'Answer time [ms]'])
            t.align = 'l'
        if sort:
            ping_times = []
            for node in nodes:
                ping_times.append(1000.0)

            if threading:
                if FUTURES_MODULE:
                    pool = ThreadPoolExecutor(max_workers=(len(nodes) + 1))
                    futures = []
            for i in range(len(nodes)):
                try:
                    if not threading or not FUTURES_MODULE:
                        ping_times[i] = node_answer_time(nodes[i])
                    else:
                        futures.append(pool.submit(node_answer_time, nodes[i]))
                    if not threading or not FUTURES_MODULE:
                        print('node %s results in %.2f' % (nodes[i], ping_times[i]))
                except KeyboardInterrupt:
                    ping_times[i] = float('inf')
                    break

            if threading:
                if FUTURES_MODULE:
                    ping_times = [r.result() for r in as_completed(futures)]
            sorted_arg = sorted((range(len(ping_times))), key=(ping_times.__getitem__))
            sorted_nodes = []
            for i in sorted_arg:
                if not remove or ping_times[i] != float('inf'):
                    sorted_nodes.append(nodes[i])

            stm.set_default_nodes(sorted_nodes)
            if not raw:
                for i in sorted_arg:
                    t.add_row([nodes[i], '%.2f' % (ping_times[i] * 1000)])

                print(t)
            else:
                print(ping_times[sorted_arg])
        else:
            node = stm.rpc.url
            rpc_answer_time = node_answer_time(node)
            rpc_time_str = '%.2f' % (rpc_answer_time * 1000)
            if raw:
                print(rpc_time_str)
                return
            t.add_row([node, rpc_time_str])
            print(t)


@cli.command()
@click.option('--version',
  is_flag=True, default=False, help='Returns only the raw version value')
@click.option('--url',
  is_flag=True, default=False, help='Returns only the raw url value')
def currentnode(version, url):
    """ Sets the currently working node at the first place in the list
    """
    stm = shared_dpay_instance()
    if stm.rpc is not None:
        stm.rpc.rpcconnect()
    else:
        offline = stm.offline
        stm.move_current_node_to_front()
        node = stm.get_default_nodes()
        if version:
            if not offline:
                print(stm.get_blockchain_version())
                return
        if version:
            if offline:
                print('Node is offline')
                return
        if url:
            if not offline:
                print(stm.rpc.url)
                return
            else:
                t = PrettyTable(['Key', 'Value'])
                t.align = 'l'
                if not offline:
                    t.add_row(['Node-Url', stm.rpc.url])
                else:
                    t.add_row(['Node-Url', node[0]])
            offline or t.add_row(['Version', stm.get_blockchain_version()])
        else:
            t.add_row(['Version', 'dpay is in offline mode...'])
    print(t)


@cli.command()
@click.option('--show',
  '-s', is_flag=True, default=False, help='Prints the updated nodes')
@click.option('--test',
  '-t', is_flag=True, default=False, help='Do change the node list, only print the newest nodes setup.')
@click.option('--only-https',
  '-h', is_flag=True, default=False, help='Use only https nodes.')
@click.option('--only-wss',
  '-w', is_flag=True, default=False, help='Use only websocket nodes.')
@click.option('--only-appbase',
  '-a', is_flag=True, default=False, help='Use only appbase nodes')
@click.option('--only-non-appbase',
  '-n', is_flag=True, default=False, help='Use only non-appbase nodes')
def updatenodes(show, test, only_https, only_wss, only_appbase, only_non_appbase):
    """ Update the nodelist from @fullnodeupdate
    """
    stm = shared_dpay_instance()
    if stm.rpc is not None:
        stm.rpc.rpcconnect()
    t = PrettyTable(['node', 'Version', 'score'])
    t.align = 'l'
    nodelist = NodeList()
    nodelist.update_nodes(dpay_instance=stm)
    nodes = nodelist.get_nodes(normal=(not only_appbase), appbase=(not only_non_appbase), wss=(not only_https), https=(not only_wss))
    if show or test:
        sorted_nodes = sorted(nodelist, key=(lambda node: node['score']), reverse=True)
        for node in sorted_nodes:
            if node['url'] in nodes:
                score = float('{0:.1f}'.format(node['score']))
                t.add_row([node['url'], node['version'], score])

        print(t)
    if not test:
        stm.set_default_nodes(nodes)


@cli.command()
def config():
    """ Shows local configuration
    """
    stm = shared_dpay_instance()
    t = PrettyTable(['Key', 'Value'])
    t.align = 'l'
    for key in stm.config:
        if key in availableConfigurationKeys and key != 'nodes' and key != 'node':
            t.add_row([key, stm.config[key]])

    node = stm.get_default_nodes()
    nodes = json.dumps(node, indent=4)
    t.add_row(['nodes', nodes])
    if 'password_storage' not in availableConfigurationKeys:
        t.add_row(['password_storage', stm.config['password_storage']])
    t.add_row(['data_dir', stm.config.data_dir])
    print(t)


@cli.command()
@click.option('--wipe', is_flag=True, default=False, help='Wipe old wallet without prompt.')
def createwallet(wipe):
    """ Create new wallet with a new password
    """
    stm = shared_dpay_instance()
    if stm.wallet.created():
        if not wipe:
            wipe_answer = click.prompt("'Do you want to wipe your wallet? Are your sure? This is IRREVERSIBLE! If you dont have a backup you may lose access to your account! [y/n]", default='n')
            if wipe_answer in ('y', 'ye', 'yes'):
                stm.wallet.wipe(True)
            else:
                return
    if wipe:
        stm.wallet.wipe(True)
    password = None
    password = click.prompt('New wallet password', confirmation_prompt=True, hide_input=True)
    if not bool(password):
        print('Password cannot be empty! Quitting...')
        return
    password_storage = stm.config['password_storage']
    if KEYRING_AVAILABLE:
        if password_storage == 'keyring':
            password = keyring.set_password('dpaycli', 'wallet', password)
    if password_storage == 'environment':
        print('The new wallet password can be stored in the UNLOCK environment variable to skip password prompt!')
    stm.wallet.create(password)
    set_shared_dpay_instance(stm)


@cli.command()
@click.option('--test-unlock', is_flag=True, default=False, help='test if unlock is sucessful')
def walletinfo(test_unlock):
    """ Show info about wallet
    """
    stm = shared_dpay_instance()
    t = PrettyTable(['Key', 'Value'])
    t.align = 'l'
    t.add_row(['created', stm.wallet.created()])
    t.add_row(['locked', stm.wallet.locked()])
    t.add_row(['Number of stored keys', len(stm.wallet.getPublicKeys())])
    t.add_row(['sql-file', stm.wallet.keyStorage.sqlDataBaseFile])
    password_storage = stm.config['password_storage']
    t.add_row(['password_storage', password_storage])
    password = os.environ.get('UNLOCK')
    if password is not None:
        t.add_row(['UNLOCK env set', 'yes'])
    else:
        t.add_row(['UNLOCK env set', 'no'])
    if KEYRING_AVAILABLE:
        t.add_row(['keyring installed', 'yes'])
    else:
        t.add_row(['keyring installed', 'no'])
    if test_unlock:
        if unlock_wallet(stm):
            t.add_row(['Wallet unlock', 'successful'])
        else:
            t.add_row(['Wallet unlock', 'not working'])
    print(t)


@cli.command()
@click.option('--unsafe-import-key', help='WIF key to parse (unsafe, unless shell history is deleted afterwards)',
  multiple=True)
def parsewif(unsafe_import_key):
    """ Parse a WIF private key without importing
    """
    stm = shared_dpay_instance()
    if stm.rpc is not None:
        stm.rpc.rpcconnect()
    else:
        if unsafe_import_key:
            for key in unsafe_import_key:
                try:
                    pubkey = PrivateKey(key, prefix=(stm.prefix)).pubkey
                    print(pubkey)
                    account = stm.wallet.getAccountFromPublicKey(str(pubkey))
                    account = Account(account, dpay_instance=stm)
                    key_type = stm.wallet.getKeyType(account, str(pubkey))
                    print('Account: %s - %s' % (account['name'], key_type))
                except Exception as e:
                    print(str(e))

        else:
            while True:
                wifkey = click.prompt('Enter private key', confirmation_prompt=False, hide_input=True)
                if not wifkey or wifkey == 'quit' or wifkey == 'exit':
                    break
                try:
                    pubkey = PrivateKey(wifkey, prefix=(stm.prefix)).pubkey
                    print(pubkey)
                    account = stm.wallet.getAccountFromPublicKey(str(pubkey))
                    account = Account(account, dpay_instance=stm)
                    key_type = stm.wallet.getKeyType(account, str(pubkey))
                    print('Account: %s - %s' % (account['name'], key_type))
                except Exception as e:
                    print(str(e))
                    continue


@cli.command()
@click.option('--unsafe-import-key', help='Private key to import to wallet (unsafe, unless shell history is deleted afterwards)')
def addkey(unsafe_import_key):
    """ Add key to wallet

        When no [OPTION] is given, a password prompt for unlocking the wallet
        and a prompt for entering the private key are shown.
    """
    stm = shared_dpay_instance()
    if stm.rpc is not None:
        stm.rpc.rpcconnect()
    if not unlock_wallet(stm):
        return
    if not unsafe_import_key:
        unsafe_import_key = click.prompt('Enter private key', confirmation_prompt=False, hide_input=True)
    stm.wallet.addPrivateKey(unsafe_import_key)
    set_shared_dpay_instance(stm)


@cli.command()
@click.option('--confirm', prompt='Are your sure? This is IRREVERSIBLE! If you dont have a backup you may lose access to your account!',
  hide_input=False,
  callback=prompt_flag_callback,
  is_flag=True,
  confirmation_prompt=False,
  help='Please confirm!')
@click.argument('pub')
def delkey(confirm, pub):
    """ Delete key from the wallet

        PUB is the public key from the private key
        which will be deleted from the wallet
    """
    stm = shared_dpay_instance()
    if stm.rpc is not None:
        stm.rpc.rpcconnect()
    if not unlock_wallet(stm):
        return
    stm.wallet.removePrivateKeyFromPublicKey(pub)
    set_shared_dpay_instance(stm)


@cli.command()
@click.option('--import-brain-key', help='Imports a brain key and derives a private and public key', is_flag=True, default=False)
@click.option('--sequence', help='Sequence number, influences the derived private key. (default is 0)', default=0)
def keygen(import_brain_key, sequence):
    """ Creates a new random brain key and prints its derived private key and public key.
        The generated key is not stored.
    """
    if import_brain_key:
        brain_key = click.prompt('Enter brain key', confirmation_prompt=False, hide_input=True)
    else:
        brain_key = None
    bk = BrainKey(brainkey=brain_key, sequence=sequence)
    t = PrettyTable(['Key', 'Value'])
    t.align = 'l'
    t.add_row(['Brain Key', bk.get_brainkey()])
    t.add_row(['Private Key', str(bk.get_private())])
    t.add_row(['Public Key', format(bk.get_public(), 'DWB')])
    print(t)


@cli.command()
@click.argument('name')
@click.option('--unsafe-import-token', help='Private key to import to wallet (unsafe, unless shell history is deleted afterwards)')
def addtoken(name, unsafe_import_token):
    """ Add key to wallet

        When no [OPTION] is given, a password prompt for unlocking the wallet
        and a prompt for entering the private key are shown.
    """
    stm = shared_dpay_instance()
    if stm.rpc is not None:
        stm.rpc.rpcconnect()
    if not unlock_wallet(stm):
        return
    if not unsafe_import_token:
        unsafe_import_token = click.prompt('Enter private token', confirmation_prompt=False, hide_input=True)
    stm.wallet.addToken(name, unsafe_import_token)
    set_shared_dpay_instance(stm)


@cli.command()
@click.option('--confirm', prompt='Are your sure?',
  hide_input=False,
  callback=prompt_flag_callback,
  is_flag=True,
  confirmation_prompt=False,
  help='Please confirm!')
@click.argument('name')
def deltoken(confirm, name):
    """ Delete name from the wallet

        name is the public name from the private token
        which will be deleted from the wallet
    """
    stm = shared_dpay_instance()
    if stm.rpc is not None:
        stm.rpc.rpcconnect()
    if not unlock_wallet(stm):
        return
    stm.wallet.removeTokenFromPublicName(name)
    set_shared_dpay_instance(stm)


@cli.command()
def listkeys():
    """ Show stored keys
    """
    stm = shared_dpay_instance()
    t = PrettyTable(['Available Key'])
    t.align = 'l'
    for key in stm.wallet.getPublicKeys():
        t.add_row([key])

    print(t)


@cli.command()
def listtoken():
    """ Show stored token
    """
    stm = shared_dpay_instance()
    t = PrettyTable(['name', 'scope', 'status'])
    t.align = 'l'
    if not unlock_wallet(stm):
        return
    dpid = DPayID(dpay_instance=stm)
    for name in stm.wallet.getPublicNames():
        ret = dpid.me(username=name)
        if 'error' in ret:
            t.add_row([name, '-', ret['error']])
        else:
            t.add_row([name, ret['scope'], 'ok'])

    print(t)


@cli.command()
def listaccounts():
    """Show stored accounts"""
    stm = shared_dpay_instance()
    if stm.rpc is not None:
        stm.rpc.rpcconnect()
    t = PrettyTable(['Name', 'Type', 'Available Key'])
    t.align = 'l'
    for account in stm.wallet.getAccounts():
        t.add_row([
         account['name'] or 'n/a', account['type'] or 'n/a',
         account['pubkey']])

    print(t)


@cli.command()
@click.argument('post', nargs=1)
@click.argument('vote_weight', nargs=1, required=False)
@click.option('--weight', '-w', help='Vote weight (from 0.1 to 100.0)')
@click.option('--account', '-a', help='Voter account name')
def upvote(post, vote_weight, account, weight):
    """Upvote a post/comment

        POST is @author/permlink
    """
    stm = shared_dpay_instance()
    if stm.rpc is not None:
        stm.rpc.rpcconnect()
    if not weight:
        if vote_weight:
            weight = vote_weight
            raise weight.replace('.', '', 1).isdigit() or ValueError('vote_weight must be a float!')
        else:
            weight = float(weight)
            if weight > 100:
                raise ValueError('Maximum vote weight is 100.0!')
            elif weight < -100:
                raise ValueError('Minimum vote weight is -100.0!')
    else:
        if not weight:
            if not vote_weight:
                weight = stm.config['default_vote_weight']
    if not account:
        account = stm.config['default_account']
    if not unlock_wallet(stm):
        return
    try:
        post = Comment(post, dpay_instance=stm)
        tx = post.upvote(weight, voter=account)
        if stm.unsigned:
            if stm.nobroadcast:
                if stm.dpayid is not None:
                    tx = stm.dpayid.url_from_tx(tx)
    except exceptions.VotingInvalidOnArchivedPost:
        print('Post/Comment is older than 7 days! Did not upvote.')
        tx = {}

    tx = json.dumps(tx, indent=4)
    print(tx)


@cli.command()
@click.argument('post', nargs=1)
@click.argument('vote_weight', nargs=1, required=False)
@click.option('--account', '-a', help='Voter account name')
@click.option('--weight', '-w', default=100.0, help='Vote weight (from 0.1 to 100.0)')
def downvote(post, vote_weight, account, weight):
    """Downvote a post/comment

        POST is @author/permlink
    """
    stm = shared_dpay_instance()
    if stm.rpc is not None:
        stm.rpc.rpcconnect()
    if not weight:
        if vote_weight:
            weight = vote_weight
            raise weight.replace('.', '', 1).isdigit() or ValueError('vote_weight must be a float!')
        else:
            weight = float(weight)
            if weight > 100:
                raise ValueError('Maximum vote weight is 100.0!')
            elif weight < -100:
                raise ValueError('Minimum vote weight is -100.0!')
    else:
        if not weight:
            if not vote_weight:
                weight = stm.config['default_vote_weight']
    if not account:
        account = stm.config['default_account']
    if not unlock_wallet(stm):
        return
    try:
        post = Comment(post, dpay_instance=stm)
        tx = post.downvote(weight, voter=account)
        if stm.unsigned:
            if stm.nobroadcast:
                if stm.dpayid is not None:
                    tx = stm.dpayid.url_from_tx(tx)
    except exceptions.VotingInvalidOnArchivedPost:
        print('Post/Comment is older than 7 days! Did not downvote.')
        tx = {}

    tx = json.dumps(tx, indent=4)
    print(tx)


@cli.command()
@click.argument('to', nargs=1)
@click.argument('amount', nargs=1)
@click.argument('asset', nargs=1, callback=asset_callback)
@click.argument('memo', nargs=1, required=False)
@click.option('--account', '-a', help='Transfer from this account')
def transfer(to, amount, asset, memo, account):
    """Transfer BBD/BEX"""
    stm = shared_dpay_instance()
    if stm.rpc is not None:
        stm.rpc.rpcconnect()
    if not account:
        account = stm.config['default_account']
    if not bool(memo):
        memo = ''
    if not unlock_wallet(stm):
        return
    acc = Account(account, dpay_instance=stm)
    tx = acc.transfer(to, amount, asset, memo)
    if stm.unsigned:
        if stm.nobroadcast:
            if stm.dpayid is not None:
                tx = stm.dpayid.url_from_tx(tx)
    tx = json.dumps(tx, indent=4)
    print(tx)


@cli.command()
@click.argument('amount', nargs=1)
@click.option('--account', '-a', help='Powerup from this account')
@click.option('--to', help='Powerup this account', default=None)
def powerup(amount, account, to):
    """Power up (vest BEX as BEX POWER)"""
    stm = shared_dpay_instance()
    if stm.rpc is not None:
        stm.rpc.rpcconnect()
    if not account:
        account = stm.config['default_account']
    if not unlock_wallet(stm):
        return
    acc = Account(account, dpay_instance=stm)
    try:
        amount = float(amount)
    except:
        amount = str(amount)

    tx = acc.transfer_to_vesting(amount, to=to)
    if stm.unsigned:
        if stm.nobroadcast:
            if stm.dpayid is not None:
                tx = stm.dpayid.url_from_tx(tx)
    tx = json.dumps(tx, indent=4)
    print(tx)


@cli.command()
@click.argument('amount', nargs=1)
@click.option('--account', '-a', help='Powerup from this account')
def powerdown(amount, account):
    """Power down (start withdrawing VESTS from DPay POWER)

        amount is in VESTS
    """
    stm = shared_dpay_instance()
    if stm.rpc is not None:
        stm.rpc.rpcconnect()
    if not account:
        account = stm.config['default_account']
    if not unlock_wallet(stm):
        return
    acc = Account(account, dpay_instance=stm)
    try:
        amount = float(amount)
    except:
        amount = str(amount)

    tx = acc.withdraw_vesting(amount)
    if stm.unsigned:
        if stm.nobroadcast:
            if stm.dpayid is not None:
                tx = stm.dpayid.url_from_tx(tx)
    tx = json.dumps(tx, indent=4)
    print(tx)


@cli.command()
@click.argument('amount', nargs=1)
@click.argument('to_account', nargs=1)
@click.option('--account', '-a', help='Powerup from this account')
def delegate(amount, to_account, account):
    """Delegate (start delegate VESTS to another account)

        amount is in VESTS / DPay
    """
    stm = shared_dpay_instance()
    if stm.rpc is not None:
        stm.rpc.rpcconnect()
    if not account:
        account = stm.config['default_account']
    if not unlock_wallet(stm):
        return
    acc = Account(account, dpay_instance=stm)
    try:
        amount = float(amount)
    except:
        amount = Amount((str(amount)), dpay_instance=stm)
        if amount.symbol == stm.dpay_symbol:
            amount = stm.bp_to_vests(float(amount))

    tx = acc.delegate_vesting_shares(to_account, amount)
    if stm.unsigned:
        if stm.nobroadcast:
            if stm.dpayid is not None:
                tx = stm.dpayid.url_from_tx(tx)
    tx = json.dumps(tx, indent=4)
    print(tx)


@cli.command()
@click.argument('to', nargs=1)
@click.option('--percentage', default=100, help='The percent of the withdraw to go to the "to" account')
@click.option('--account', '-a', help='Powerup from this account')
@click.option('--auto_vest', help='Set to true if the from account should receive the VESTS asVESTS, or false if it should receive them as BEX.', is_flag=True)
def powerdownroute(to, percentage, account, auto_vest):
    """Setup a powerdown route"""
    stm = shared_dpay_instance()
    if stm.rpc is not None:
        stm.rpc.rpcconnect()
    if not account:
        account = stm.config['default_account']
    if not unlock_wallet(stm):
        return
    acc = Account(account, dpay_instance=stm)
    tx = acc.set_withdraw_vesting_route(to, percentage, auto_vest=auto_vest)
    if stm.unsigned:
        if stm.nobroadcast:
            if stm.dpayid is not None:
                tx = stm.dpayid.url_from_tx(tx)
    tx = json.dumps(tx, indent=4)
    print(tx)


@cli.command()
@click.argument('amount', nargs=1)
@click.option('--account', '-a', help='Powerup from this account')
def convert(amount, account):
    """Convert BEXDollars to DPay (takes a week to settle)"""
    stm = shared_dpay_instance()
    if stm.rpc is not None:
        stm.rpc.rpcconnect()
    if not account:
        account = stm.config['default_account']
    if not unlock_wallet(stm):
        return
    acc = Account(account, dpay_instance=stm)
    try:
        amount = float(amount)
    except:
        amount = str(amount)

    tx = acc.convert(amount)
    if stm.unsigned:
        if stm.nobroadcast:
            if stm.dpayid is not None:
                tx = stm.dpayid.url_from_tx(tx)
    tx = json.dumps(tx, indent=4)
    print(tx)


@cli.command()
def changewalletpassphrase():
    """ Change wallet password
    """
    stm = shared_dpay_instance()
    if not unlock_wallet(stm):
        return
    newpassword = None
    newpassword = click.prompt('New wallet password', confirmation_prompt=True, hide_input=True)
    if not bool(newpassword):
        print('Password cannot be empty! Quitting...')
        return
    password_storage = stm.config['password_storage']
    if KEYRING_AVAILABLE:
        if password_storage == 'keyring':
            keyring.set_password('dpaycli', 'wallet', newpassword)
    if password_storage == 'environment':
        print('The new wallet password can be stored in the UNLOCK invironment variable to skip password prompt!')
    stm.wallet.changePassphrase(newpassword)


@cli.command()
@click.argument('account', nargs=(-1))
def power(account):
    """ Shows vote power and bandwidth
    """
    stm = shared_dpay_instance()
    if stm.rpc is not None:
        stm.rpc.rpcconnect()
    if len(account) == 0:
        if 'default_account' in stm.config:
            account = [
             stm.config['default_account']]
    for name in account:
        a = Account(name, dpay_instance=stm)
        print('\n@%s' % a.name)
        a.print_info(use_table=True)


@cli.command()
@click.argument('account', nargs=(-1))
def balance(account):
    """ Shows balance
    """
    stm = shared_dpay_instance()
    if stm.rpc is not None:
        stm.rpc.rpcconnect()
    if len(account) == 0:
        if 'default_account' in stm.config:
            account = [
             stm.config['default_account']]
    for name in account:
        a = Account(name, dpay_instance=stm)
        print('\n@%s' % a.name)
        t = PrettyTable(['Account', 'BEX', 'BBD', 'VESTS'])
        t.align = 'r'
        t.add_row([
         'Available',
         str(a.balances['available'][0]),
         str(a.balances['available'][1]),
         str(a.balances['available'][2])])
        t.add_row([
         'Rewards',
         str(a.balances['rewards'][0]),
         str(a.balances['rewards'][1]),
         str(a.balances['rewards'][2])])
        t.add_row([
         'Savings',
         str(a.balances['savings'][0]),
         str(a.balances['savings'][1]),
         'N/A'])
        t.add_row([
         'TOTAL',
         str(a.balances['total'][0]),
         str(a.balances['total'][1]),
         str(a.balances['total'][2])])
        print(t)


@cli.command()
@click.argument('account', nargs=(-1), required=False)
def interest(account):
    """ Get information about interest payment
    """
    stm = shared_dpay_instance()
    if stm.rpc is not None:
        stm.rpc.rpcconnect()
    if not account:
        if 'default_account' in stm.config:
            account = [
             stm.config['default_account']]
    t = PrettyTable([
     'Account', 'Last Interest Payment', 'Next Payment',
     'Interest rate', 'Interest'])
    t.align = 'r'
    for a in account:
        a = Account(a, dpay_instance=stm)
        i = a.interest()
        t.add_row([
         a['name'],
         i['last_payment'],
         'in %s' % i['next_payment_duration'],
         '%.1f%%' % i['interest_rate'],
         '%.3f %s' % (i['interest'], 'BBD')])

    print(t)


@cli.command()
@click.argument('account', nargs=(-1), required=False)
def follower(account):
    """ Get information about followers
    """
    stm = shared_dpay_instance()
    if stm.rpc is not None:
        stm.rpc.rpcconnect()
    if not account:
        if 'default_account' in stm.config:
            account = [
             stm.config['default_account']]
    for a in account:
        a = Account(a, dpay_instance=stm)
        print('\nFollowers statistics for @%s (please wait...)' % a.name)
        followers = a.get_followers(False)
        followers.print_summarize_table(tag_type='Followers')


@cli.command()
@click.argument('account', nargs=(-1), required=False)
def following(account):
    """ Get information about following
    """
    stm = shared_dpay_instance()
    if stm.rpc is not None:
        stm.rpc.rpcconnect()
    if not account:
        if 'default_account' in stm.config:
            account = [
             stm.config['default_account']]
    for a in account:
        a = Account(a, dpay_instance=stm)
        print('\nFollowing statistics for @%s (please wait...)' % a.name)
        following = a.get_following(False)
        following.print_summarize_table(tag_type='Following')


@cli.command()
@click.argument('account', nargs=(-1), required=False)
def muter(account):
    """ Get information about muter
    """
    stm = shared_dpay_instance()
    if stm.rpc is not None:
        stm.rpc.rpcconnect()
    if not account:
        if 'default_account' in stm.config:
            account = [
             stm.config['default_account']]
    for a in account:
        a = Account(a, dpay_instance=stm)
        print('\nMuters statistics for @%s (please wait...)' % a.name)
        muters = a.get_muters(False)
        muters.print_summarize_table(tag_type='Muters')


@cli.command()
@click.argument('account', nargs=(-1), required=False)
def muting(account):
    """ Get information about muting
    """
    stm = shared_dpay_instance()
    if stm.rpc is not None:
        stm.rpc.rpcconnect()
    if not account:
        if 'default_account' in stm.config:
            account = [
             stm.config['default_account']]
    for a in account:
        a = Account(a, dpay_instance=stm)
        print('\nMuting statistics for @%s (please wait...)' % a.name)
        muting = a.get_mutings(False)
        muting.print_summarize_table(tag_type='Muting')


@cli.command()
@click.argument('account', nargs=1, required=False)
def permissions(account):
    """ Show permissions of an account
    """
    stm = shared_dpay_instance()
    if stm.rpc is not None:
        stm.rpc.rpcconnect()
    if not account:
        if 'default_account' in stm.config:
            account = stm.config['default_account']
    account = Account(account, dpay_instance=stm)
    t = PrettyTable(['Permission', 'Threshold', 'Key/Account'], hrules=0)
    t.align = 'r'
    for permission in ('owner', 'active', 'posting'):
        auths = []
        for type_ in ('account_auths', 'key_auths'):
            for authority in account[permission][type_]:
                auths.append('%s (%d)' % (authority[0], authority[1]))

        t.add_row([
         permission,
         account[permission]['weight_threshold'],
         '\n'.join(auths)])

    print(t)


@cli.command()
@click.argument('foreign_account', nargs=1, required=False)
@click.option('--permission', default='posting', help='The permission to grant (defaults to "posting")')
@click.option('--account', '-a', help='The account to allow action for')
@click.option('--weight', help='The weight to use instead of the (full) threshold. If the weight is smaller than the threshold, additional signatures are required')
@click.option('--threshold', help="The permission's threshold that needs to be reached by signatures to be able to interact")
def allow(foreign_account, permission, account, weight, threshold):
    """Allow an account/key to interact with your account

        foreign_account: The account or key that will be allowed to interact with account.
            When not given, password will be asked, from which a public key is derived.
            This derived key will then interact with your account.
    """
    stm = shared_dpay_instance()
    if stm.rpc is not None:
        stm.rpc.rpcconnect()
    if not account:
        account = stm.config['default_account']
    if not unlock_wallet(stm):
        return
    if permission not in ('posting', 'active', 'owner'):
        print('Wrong permission, please use: posting, active or owner!')
        return
    acc = Account(account, dpay_instance=stm)
    if not foreign_account:
        from dpaycligraphenebase.account import PasswordKey
        pwd = click.prompt('Password for Key Derivation', confirmation_prompt=True, hide_input=True)
        foreign_account = format(PasswordKey(account, pwd, permission).get_public(), stm.prefix)
    if threshold is not None:
        threshold = int(threshold)
    tx = acc.allow(foreign_account, weight=weight, permission=permission, threshold=threshold)
    if stm.unsigned:
        if stm.nobroadcast:
            if stm.dpayid is not None:
                tx = stm.dpayid.url_from_tx(tx)
    tx = json.dumps(tx, indent=4)
    print(tx)


@cli.command()
@click.argument('foreign_account', nargs=1, required=False)
@click.option('--permission', default='posting', help='The permission to grant (defaults to "posting")')
@click.option('--account', '-a', help='The account to disallow action for')
@click.option('--threshold', help="The permission's threshold that needs to be reached by signatures to be able to interact")
def disallow(foreign_account, permission, account, threshold):
    """Remove allowance an account/key to interact with your account"""
    stm = shared_dpay_instance()
    if stm.rpc is not None:
        stm.rpc.rpcconnect()
    if not account:
        account = stm.config['default_account']
    if not unlock_wallet(stm):
        return
    if permission not in ('posting', 'active', 'owner'):
        print('Wrong permission, please use: posting, active or owner!')
        return
    if threshold is not None:
        threshold = int(threshold)
    acc = Account(account, dpay_instance=stm)
    if not foreign_account:
        from dpaycligraphenebase.account import PasswordKey
        pwd = click.prompt('Password for Key Derivation', confirmation_prompt=True)
        foreign_account = [format(PasswordKey(account, pwd, permission).get_public(), stm.prefix)]
    tx = acc.disallow(foreign_account, permission=permission, threshold=threshold)
    if stm.unsigned:
        if stm.nobroadcast:
            if stm.dpayid is not None:
                tx = stm.dpayid.url_from_tx(tx)
    tx = json.dumps(tx, indent=4)
    print(tx)


@cli.command()
@click.argument('creator', nargs=1, required=True)
@click.option('--fee', help='When fee is 0 (default) a subsidized account is claimed and can be created later with create_claimed_account', default=0)
@click.option('--number', '-n', help='Number of subsidized accounts to be claimed (default = 1), when fee = 0 BEX', default=1)
def claimaccount(creator, fee, number):
    """Claim account for claimed account creation."""
    stm = shared_dpay_instance()
    if stm.rpc is not None:
        stm.rpc.rpcconnect()
    if not creator:
        creator = stm.config['default_account']
    if not unlock_wallet(stm):
        return
    else:
        creator = Account(creator, dpay_instance=stm)
        fee = Amount(('%.3f %s' % (float(fee), stm.dpay_symbol)), dpay_instance=stm)
        tx = None
        if stm.unsigned:
            if stm.nobroadcast:
                if stm.dpayid is not None:
                    tx = stm.claim_account(creator, fee=fee)
                    tx = stm.dpayid.url_from_tx(tx)
        if float(fee) == 0:
            rc = RC(dpay_instance=stm)
            current_costs = stm.get_rc_cost(rc.get_resource_count(tx_size=200, new_account_op_count=1))
            current_mana = creator.get_rc_manabar()['current_mana']
            last_mana = current_mana
            cnt = 0
            print('Current costs %.2f G RC - current mana %.2f G RC' % (current_costs / 1000000000.0, current_mana / 1000000000.0))
            print('Account can claim %d accounts' % int(current_mana / current_costs))
            while current_costs + 10 < current_mana and cnt < number:
                if cnt > 0:
                    print('Current costs %.2f G RC - current mana %.2f G RC' % (current_costs / 1000000000.0, current_mana / 1000000000.0))
                    tx = json.dumps(tx, indent=4)
                    print(tx)
                cnt += 1
                tx = stm.claim_account(creator, fee=fee)
                time.sleep(10)
                creator.refresh()
                current_mana = creator.get_rc_manabar()['current_mana']
                print('Account claimed and %.2f G RC paid.' % ((last_mana - current_mana) / 1000000000.0))
                last_mana = current_mana

            if cnt == 0:
                print('Not enough RC for a claim!')
        else:
            tx = stm.claim_account(creator, fee=fee)
    if tx is not None:
        tx = json.dumps(tx, indent=4)
        print(tx)


@cli.command()
@click.argument('accountname', nargs=1, required=True)
@click.option('--account', '-a', help='Account that pays the fee')
@click.option('--create-claimed-account', '-c', help='Instead of paying the account creation fee a subsidized account is created.', is_flag=True, default=False)
def newaccount(accountname, account, create_claimed_account):
    """Create a new account"""
    stm = shared_dpay_instance()
    if stm.rpc is not None:
        stm.rpc.rpcconnect()
    if not account:
        account = stm.config['default_account']
    if not unlock_wallet(stm):
        return
    else:
        acc = Account(account, dpay_instance=stm)
        password = click.prompt('New Account Passphrase', confirmation_prompt=True, hide_input=True)
        if not password:
            print('You cannot chose an empty password')
            return
        if create_claimed_account:
            tx = stm.create_claimed_account(accountname, creator=acc, password=password)
        else:
            tx = stm.create_account(accountname, creator=acc, password=password)
    if stm.unsigned:
        if stm.nobroadcast:
            if stm.dpayid is not None:
                tx = stm.dpayid.url_from_tx(tx)
    tx = json.dumps(tx, indent=4)
    print(tx)


@cli.command()
@click.argument('variable', nargs=1, required=False)
@click.argument('value', nargs=1, required=False)
@click.option('--account', '-a', help='setprofile as this user')
@click.option('--pair', '-p', help='"Key=Value" pairs', multiple=True)
def setprofile(variable, value, account, pair):
    """Set a variable in an account's profile"""
    stm = shared_dpay_instance()
    if stm.rpc is not None:
        stm.rpc.rpcconnect()
    keys = []
    values = []
    if pair:
        for p in pair:
            key, value = p.split('=')
            keys.append(key)
            values.append(value)

    if variable:
        if value:
            keys.append(variable)
            values.append(value)
    profile = Profile(keys, values)
    if not account:
        account = stm.config['default_account']
    if not unlock_wallet(stm):
        return
    acc = Account(account, dpay_instance=stm)
    json_metadata = Profile(acc['json_metadata'] if acc['json_metadata'] else {})
    json_metadata.update(profile)
    tx = acc.update_account_profile(json_metadata)
    if stm.unsigned:
        if stm.nobroadcast:
            if stm.dpayid is not None:
                tx = stm.dpayid.url_from_tx(tx)
    tx = json.dumps(tx, indent=4)
    print(tx)


@cli.command()
@click.argument('variable', nargs=(-1), required=True)
@click.option('--account', '-a', help='delprofile as this user')
def delprofile(variable, account):
    """Delete a variable in an account's profile"""
    stm = shared_dpay_instance()
    if stm.rpc is not None:
        stm.rpc.rpcconnect()
    if not account:
        account = stm.config['default_account']
    if not unlock_wallet(stm):
        return
    acc = Account(account, dpay_instance=stm)
    json_metadata = Profile(acc['json_metadata'])
    for var in variable:
        json_metadata.remove(var)

    tx = acc.update_account_profile(json_metadata)
    if stm.unsigned:
        if stm.nobroadcast:
            if stm.dpayid is not None:
                tx = stm.dpayid.url_from_tx(tx)
    tx = json.dumps(tx, indent=4)
    print(tx)


@cli.command()
@click.argument('account', nargs=1, required=True)
@click.option('--roles', help='Import specified keys (owner, active, posting, memo).', default=['active', 'posting', 'memo'])
def importaccount(account, roles):
    """Import an account using a passphrase"""
    from dpaycligraphenebase.account import PasswordKey
    stm = shared_dpay_instance()
    if stm.rpc is not None:
        stm.rpc.rpcconnect()
    if not unlock_wallet(stm):
        return
    account = Account(account, dpay_instance=stm)
    imported = False
    password = click.prompt('Account Passphrase', confirmation_prompt=False, hide_input=True)
    if not password:
        print('You cannot chose an empty Passphrase')
        return
    if 'owner' in roles:
        owner_key = PasswordKey((account['name']), password, role='owner')
        owner_pubkey = format(owner_key.get_public_key(), stm.prefix)
        if owner_pubkey in [x[0] for x in account['owner']['key_auths']]:
            print('Importing owner key!')
            owner_privkey = owner_key.get_private_key()
            stm.wallet.addPrivateKey(owner_privkey)
            imported = True
    if 'active' in roles:
        active_key = PasswordKey((account['name']), password, role='active')
        active_pubkey = format(active_key.get_public_key(), stm.prefix)
        if active_pubkey in [x[0] for x in account['active']['key_auths']]:
            print('Importing active key!')
            active_privkey = active_key.get_private_key()
            stm.wallet.addPrivateKey(active_privkey)
            imported = True
    if 'posting' in roles:
        posting_key = PasswordKey((account['name']), password, role='posting')
        posting_pubkey = format(posting_key.get_public_key(), stm.prefix)
        if posting_pubkey in [x[0] for x in account['posting']['key_auths']]:
            print('Importing posting key!')
            posting_privkey = posting_key.get_private_key()
            stm.wallet.addPrivateKey(posting_privkey)
            imported = True
    if 'memo' in roles:
        memo_key = PasswordKey((account['name']), password, role='memo')
        memo_pubkey = format(memo_key.get_public_key(), stm.prefix)
        if memo_pubkey == account['memo_key']:
            print('Importing memo key!')
            memo_privkey = memo_key.get_private_key()
            stm.wallet.addPrivateKey(memo_privkey)
            imported = True
    if not imported:
        print('No matching key(s) found. Password correct?')


@cli.command()
@click.option('--account', '-a', help='The account to updatememokey action for')
@click.option('--key', help='The new memo key')
def updatememokey(account, key):
    """Update an account's memo key"""
    stm = shared_dpay_instance()
    if stm.rpc is not None:
        stm.rpc.rpcconnect()
    if not account:
        account = stm.config['default_account']
    if not unlock_wallet(stm):
        return
    acc = Account(account, dpay_instance=stm)
    if not key:
        from dpaycligraphenebase.account import PasswordKey
        pwd = click.prompt('Password for Memo Key Derivation', confirmation_prompt=True, hide_input=True)
        memo_key = PasswordKey(account, pwd, 'memo')
        key = format(memo_key.get_public_key(), stm.prefix)
        memo_privkey = memo_key.get_private_key()
        if not stm.nobroadcast:
            stm.wallet.addPrivateKey(memo_privkey)
    tx = acc.update_memo_key(key)
    if stm.unsigned:
        if stm.nobroadcast:
            if stm.dpayid is not None:
                tx = stm.dpayid.url_from_tx(tx)
    tx = json.dumps(tx, indent=4)
    print(tx)


@cli.command()
@click.argument('witness', nargs=1)
@click.option('--account', '-a', help='Your account')
def approvewitness(witness, account):
    """Approve a witnesses"""
    stm = shared_dpay_instance()
    if stm.rpc is not None:
        stm.rpc.rpcconnect()
    if not account:
        account = stm.config['default_account']
    if not unlock_wallet(stm):
        return
    acc = Account(account, dpay_instance=stm)
    tx = acc.approvewitness(witness, approve=True)
    if stm.unsigned:
        if stm.nobroadcast:
            if stm.dpayid is not None:
                tx = stm.dpayid.url_from_tx(tx)
    tx = json.dumps(tx, indent=4)
    print(tx)


@cli.command()
@click.argument('witness', nargs=1)
@click.option('--account', '-a', help='Your account')
def disapprovewitness(witness, account):
    """Disapprove a witnesses"""
    stm = shared_dpay_instance()
    if stm.rpc is not None:
        stm.rpc.rpcconnect()
    if not account:
        account = stm.config['default_account']
    if not unlock_wallet(stm):
        return
    acc = Account(account, dpay_instance=stm)
    tx = acc.disapprovewitness(witness)
    if stm.unsigned:
        if stm.nobroadcast:
            if stm.dpayid is not None:
                tx = stm.dpayid.url_from_tx(tx)
    tx = json.dumps(tx, indent=4)
    print(tx)


@cli.command()
@click.option('--file', help='Load transaction from file. If "-", read from stdin (defaults to "-")')
def sign(file):
    """Sign a provided transaction with available and required keys"""
    stm = shared_dpay_instance()
    if stm.rpc is not None:
        stm.rpc.rpcconnect()
    elif file and file != '-':
        if not os.path.isfile(file):
            raise Exception('File %s does not exist!' % file)
        with open(file) as (fp):
            tx = fp.read()
    else:
        tx = click.get_text_stream('stdin')
    tx = ast.literal_eval(tx)
    tx = stm.sign(tx)
    tx = json.dumps(tx, indent=4)
    print(tx)


@cli.command()
@click.option('--file', help='Load transaction from file. If "-", read from stdin (defaults to "-")')
def broadcast(file):
    """broadcast a signed transaction"""
    stm = shared_dpay_instance()
    if stm.rpc is not None:
        stm.rpc.rpcconnect()
    elif file and file != '-':
        if not os.path.isfile(file):
            raise Exception('File %s does not exist!' % file)
        with open(file) as (fp):
            tx = fp.read()
    else:
        tx = click.get_text_stream('stdin')
    tx = ast.literal_eval(tx)
    tx = stm.broadcast(tx)
    tx = json.dumps(tx, indent=4)
    print(tx)


@cli.command()
@click.option('--bbd-to-bex', '-i', help='Show ticker in BBD/BEX', is_flag=True, default=False)
def ticker(bbd_to_dpay):
    """ Show ticker
    """
    stm = shared_dpay_instance()
    if stm.rpc is not None:
        stm.rpc.rpcconnect()
    t = PrettyTable(['Key', 'Value'])
    t.align = 'l'
    market = Market(dpay_instance=stm)
    ticker = market.ticker()
    for key in ticker:
        if key in ('highest_bid', 'latest', 'lowest_ask') and bbd_to_dpay:
            t.add_row([key, str(ticker[key].as_base('BBD'))])
        elif key in 'percent_change' and bbd_to_dpay:
            t.add_row([key, '%.2f %%' % -ticker[key]])
        else:
            if key in 'percent_change':
                t.add_row([key, '%.2f %%' % ticker[key]])
            else:
                t.add_row([key, str(ticker[key])])

    print(t)


@cli.command()
@click.option('--width', '-w', help='Plot width (default 75)', default=75)
@click.option('--height', '-h', help='Plot height (default 15)', default=15)
@click.option('--ascii', help='Use only ascii symbols', is_flag=True, default=False)
def pricehistory(width, height, ascii):
    """ Show price history
    """
    stm = shared_dpay_instance()
    if stm.rpc is not None:
        stm.rpc.rpcconnect()
    else:
        feed_history = stm.get_feed_history()
        current_base = Amount((feed_history['current_median_history']['base']), dpay_instance=stm)
        current_quote = Amount((feed_history['current_median_history']['quote']), dpay_instance=stm)
        price_history = feed_history['price_history']
        price = []
        for h in price_history:
            base = Amount((h['base']), dpay_instance=stm)
            quote = Amount((h['quote']), dpay_instance=stm)
            price.append(base.amount / quote.amount)

        if ascii:
            charset = 'ascii'
        else:
            charset = 'utf8'
    chart = AsciiChart(height=height, width=width, offset=4, placeholder='{:6.2f} $', charset=charset)
    print('\n            Price history for BEX (median price %4.2f $)\n' % (float(current_base) / float(current_quote)))
    chart.adapt_on_series(price)
    chart.new_chart()
    chart.add_axis()
    chart._draw_h_line((chart._map_y(float(current_base) / float(current_quote))), 1, (int(chart.n / chart.skip)), line=(chart.char_set['curve_hl_dot']))
    chart.add_curve(price)
    print(str(chart))


@cli.command()
@click.option('--days', '-d', help='Limit the days of shown trade history (default 7)', default=7.0)
@click.option('--hours', help='Limit the intervall history intervall (default 2 hours)', default=2.0)
@click.option('--bbd-to-bex', '-i', help='Show ticker in BBD/BEX', is_flag=True, default=False)
@click.option('--limit', '-l', help='Limit number of trades which is fetched at each intervall point (default 100)', default=100)
@click.option('--width', '-w', help='Plot width (default 75)', default=75)
@click.option('--height', '-h', help='Plot height (default 15)', default=15)
@click.option('--ascii', help='Use only ascii symbols', is_flag=True, default=False)
def tradehistory(days, hours, bbd_to_dpay, limit, width, height, ascii):
    """ Show price history
    """
    stm = shared_dpay_instance()
    if stm.rpc is not None:
        stm.rpc.rpcconnect()
    else:
        m = Market(dpay_instance=stm)
        utc = pytz.timezone('UTC')
        stop = utc.localize(datetime.utcnow())
        start = stop - timedelta(days=days)
        intervall = timedelta(hours=hours)
        trades = m.trade_history(start=start, stop=stop, limit=limit, intervall=intervall)
        price = []
        if bbd_to_dpay:
            base_str = stm.dpay_symbol
        else:
            base_str = stm.bbd_symbol
        for trade in trades:
            base = 0
            quote = 0
            for order in trade:
                base += float(order.as_base(base_str)['base'])
                quote += float(order.as_base(base_str)['quote'])

            price.append(base / quote)

        if ascii:
            charset = 'ascii'
        else:
            charset = 'utf8'
        chart = AsciiChart(height=height, width=width, offset=3, placeholder='{:6.2f} ', charset=charset)
        if bbd_to_dpay:
            print('\n     Trade history %s - %s \n\nBBD/BEX' % (formatTimeString(start), formatTimeString(stop)))
        else:
            print('\n     Trade history %s - %s \n\nBEX/BBD' % (formatTimeString(start), formatTimeString(stop)))
    chart.adapt_on_series(price)
    chart.new_chart()
    chart.add_axis()
    chart.add_curve(price)
    print(str(chart))


@cli.command()
@click.option('--chart', help='Enable charting', is_flag=True)
@click.option('--limit', '-l', help='Limit number of returned open orders (default 25)', default=25)
@click.option('--show-date', help='Show dates', is_flag=True, default=False)
@click.option('--width', '-w', help='Plot width (default 75)', default=75)
@click.option('--height', '-h', help='Plot height (default 15)', default=15)
@click.option('--ascii', help='Use only ascii symbols', is_flag=True, default=False)
def orderbook(chart, limit, show_date, width, height, ascii):
    """Obtain orderbook of the internal market"""
    stm = shared_dpay_instance()
    if stm.rpc is not None:
        stm.rpc.rpcconnect()
    else:
        market = Market(dpay_instance=stm)
        orderbook = market.orderbook(limit=limit, raw_data=False)
        if not show_date:
            header = [
             'Asks Sum BBD', 'Sell Orders', 'Bids Sum BBD', 'Buy Orders']
        else:
            header = [
             'Asks date', 'Sell Orders', 'Bids date', 'Buy Orders']
    t = PrettyTable(header, hrules=0)
    t.align = 'r'
    asks = []
    bids = []
    asks_date = []
    bids_date = []
    sumsum_asks = []
    sum_asks = 0
    sumsum_bids = []
    sum_bids = 0
    n = 0
    for order in orderbook['asks']:
        asks.append(order)
        sum_asks += float(order.as_base('BBD')['base'])
        sumsum_asks.append(sum_asks)

    if n < len(asks):
        n = len(asks)
    for order in orderbook['bids']:
        bids.append(order)
        sum_bids += float(order.as_base('BBD')['base'])
        sumsum_bids.append(sum_bids)

    if n < len(bids):
        n = len(bids)
    if show_date:
        for order in orderbook['asks_date']:
            asks_date.append(order)

        if n < len(asks_date):
            n = len(asks_date)
        for order in orderbook['bids_date']:
            bids_date.append(order)

        if n < len(bids_date):
            n = len(bids_date)
    if chart:
        if ascii:
            charset = 'ascii'
        else:
            charset = 'utf8'
        chart = AsciiChart(height=height, width=width, offset=4, placeholder=' {:10.2f} $', charset=charset)
        print('\n            Orderbook \n')
        chart.adapt_on_series(sumsum_asks[::-1] + sumsum_bids)
        chart.new_chart()
        chart.add_axis()
        y0 = chart._map_y(chart.minimum)
        y1 = chart._map_y(chart.maximum)
        chart._draw_v_line((y0 + 1), y1, (int(chart.n / chart.skip / 2)), line=(chart.char_set['curve_vl_dot']))
        chart.add_curve(sumsum_asks[::-1] + sumsum_bids)
        print(str(chart))
        return
    for i in range(n):
        row = []
        if len(asks_date) > i:
            row.append(formatTimeString(asks_date[i]))
        else:
            if show_date:
                row.append([''])
            else:
                if len(sumsum_asks) > i:
                    if not show_date:
                        row.append('%.2f' % sumsum_asks[i])
                if not show_date:
                    row.append([''])
            if len(asks) > i:
                row.append(str(asks[i]))
            else:
                row.append([''])
        if len(bids_date) > i:
            row.append(formatTimeString(bids_date[i]))
        else:
            if show_date:
                row.append([''])
            else:
                if len(sumsum_bids) > i:
                    if not show_date:
                        row.append('%.2f' % sumsum_bids[i])
                if not show_date:
                    row.append([''])
            if len(bids) > i:
                row.append(str(bids[i]))
            else:
                row.append([''])
        t.add_row(row)

    print(t)


@cli.command()
@click.argument('amount', nargs=1)
@click.argument('asset', nargs=1)
@click.argument('price', nargs=1, required=False)
@click.option('--account', '-a', help='Buy with this account (defaults to "default_account")')
@click.option('--orderid', help='Set an orderid')
def buy(amount, asset, price, account, orderid):
    """Buy BEX or BBD from the internal market

        Limit buy price denoted in (BBD per BEX)
    """
    stm = shared_dpay_instance()
    if stm.rpc is not None:
        stm.rpc.rpcconnect()
    else:
        if account is None:
            account = stm.config['default_account']
        else:
            if asset == stm.bbd_symbol:
                market = Market(base=(Asset(stm.dpay_symbol)), quote=(Asset(stm.bbd_symbol)), dpay_instance=stm)
            else:
                market = Market(base=(Asset(stm.bbd_symbol)), quote=(Asset(stm.dpay_symbol)), dpay_instance=stm)
        if price is None:
            orderbook = market.orderbook(limit=1, raw_data=False)
            if asset == stm.dpay_symbol:
                if len(orderbook['bids']) > 0:
                    p = Price((orderbook['bids'][0]['base']), (orderbook['bids'][0]['quote']), dpay_instance=stm).invert()
                    p_show = p
            if len(orderbook['asks']) > 0:
                p = Price((orderbook['asks'][0]['base']), (orderbook['asks'][0]['quote']), dpay_instance=stm).invert()
                p_show = p
            price_ok = click.prompt('Is the following Price ok: %s [y/n]' % str(p_show))
            if price_ok not in ('y', 'ye', 'yes'):
                return
        else:
            p = Price((float(price)), ('%s:%s' % (stm.bbd_symbol, stm.dpay_symbol)), dpay_instance=stm)
    if not unlock_wallet(stm):
        return
    a = Amount((float(amount)), asset, dpay_instance=stm)
    acc = Account(account, dpay_instance=stm)
    tx = market.buy(p, a, account=acc, orderid=orderid)
    if stm.unsigned:
        if stm.nobroadcast:
            if stm.dpayid is not None:
                tx = stm.dpayid.url_from_tx(tx)
    tx = json.dumps(tx, indent=4)
    print(tx)


@cli.command()
@click.argument('amount', nargs=1)
@click.argument('asset', nargs=1)
@click.argument('price', nargs=1, required=False)
@click.option('--account', '-a', help='Sell with this account (defaults to "default_account")')
@click.option('--orderid', help='Set an orderid')
def sell(amount, asset, price, account, orderid):
    """Sell BEX or BBD from the internal market

        Limit sell price denoted in (BBD per BEX)
    """
    stm = shared_dpay_instance()
    if stm.rpc is not None:
        stm.rpc.rpcconnect()
    else:
        if asset == stm.bbd_symbol:
            market = Market(base=(Asset(stm.dpay_symbol)), quote=(Asset(stm.bbd_symbol)), dpay_instance=stm)
        else:
            market = Market(base=(Asset(stm.bbd_symbol)), quote=(Asset(stm.dpay_symbol)), dpay_instance=stm)
        if not account:
            account = stm.config['default_account']
        orderbook = price or market.orderbook(limit=1, raw_data=False)
        if asset == stm.bbd_symbol:
            if len(orderbook['bids']) > 0:
                p = Price((orderbook['bids'][0]['base']), (orderbook['bids'][0]['quote']), dpay_instance=stm).invert()
                p_show = p
            else:
                p = Price((orderbook['asks'][0]['base']), (orderbook['asks'][0]['quote']), dpay_instance=stm).invert()
                p_show = p
            price_ok = click.prompt('Is the following Price ok: %s [y/n]' % str(p_show))
            if price_ok not in ('y', 'ye', 'yes'):
                return
        else:
            p = Price((float(price)), ('%s:%s' % (stm.bbd_symbol, stm.dpay_symbol)), dpay_instance=stm)
    if not unlock_wallet(stm):
        return
    a = Amount((float(amount)), asset, dpay_instance=stm)
    acc = Account(account, dpay_instance=stm)
    tx = market.sell(p, a, account=acc, orderid=orderid)
    if stm.unsigned:
        if stm.nobroadcast:
            if stm.dpayid is not None:
                tx = stm.dpayid.url_from_tx(tx)
    tx = json.dumps(tx, indent=4)
    print(tx)


@cli.command()
@click.argument('orderid', nargs=1)
@click.option('--account', '-a', help='Sell with this account (defaults to "default_account")')
def cancel(orderid, account):
    """Cancel order in the internal market"""
    stm = shared_dpay_instance()
    if stm.rpc is not None:
        stm.rpc.rpcconnect()
    market = Market(dpay_instance=stm)
    if not account:
        account = stm.config['default_account']
    if not unlock_wallet(stm):
        return
    acc = Account(account, dpay_instance=stm)
    tx = market.cancel(orderid, account=acc)
    if stm.unsigned:
        if stm.nobroadcast:
            if stm.dpayid is not None:
                tx = stm.dpayid.url_from_tx(tx)
    tx = json.dumps(tx, indent=4)
    print(tx)


@cli.command()
@click.argument('account', nargs=1, required=False)
def openorders(account):
    """Show open orders"""
    stm = shared_dpay_instance()
    if stm.rpc is not None:
        stm.rpc.rpcconnect()
    market = Market(dpay_instance=stm)
    if not account:
        account = stm.config['default_account']
    acc = Account(account, dpay_instance=stm)
    openorders = market.accountopenorders(account=acc)
    t = PrettyTable(['Orderid', 'Created', 'Order', 'Account'], hrules=0)
    t.align = 'r'
    for order in openorders:
        t.add_row([order['orderid'],
         formatTimeString(order['created']),
         str(order['order']),
         account])

    print(t)


@cli.command()
@click.argument('identifier', nargs=1)
@click.option('--account', '-a', help='Repost as this user')
def repost(identifier, account):
    """Repost an existing post"""
    stm = shared_dpay_instance()
    if stm.rpc is not None:
        stm.rpc.rpcconnect()
    if not account:
        account = stm.config['default_account']
    if not unlock_wallet(stm):
        return
    acc = Account(account, dpay_instance=stm)
    post = Comment(identifier, dpay_instance=stm)
    tx = post.repost(account=acc)
    if stm.unsigned:
        if stm.nobroadcast:
            if stm.dpayid is not None:
                tx = stm.dpayid.url_from_tx(tx)
    tx = json.dumps(tx, indent=4)
    print(tx)


@cli.command()
@click.argument('follow', nargs=1)
@click.option('--account', '-a', help='Follow from this account')
@click.option('--what', help='Follow these objects (defaults to ["blog"])', default=['blog'])
def follow(follow, account, what):
    """Follow another account"""
    stm = shared_dpay_instance()
    if stm.rpc is not None:
        stm.rpc.rpcconnect()
    if not account:
        account = stm.config['default_account']
    if isinstance(what, str):
        what = [
         what]
    if not unlock_wallet(stm):
        return
    acc = Account(account, dpay_instance=stm)
    tx = acc.follow(follow, what=what)
    if stm.unsigned:
        if stm.nobroadcast:
            if stm.dpayid is not None:
                tx = stm.dpayid.url_from_tx(tx)
    tx = json.dumps(tx, indent=4)
    print(tx)


@cli.command()
@click.argument('mute', nargs=1)
@click.option('--account', '-a', help='Mute from this account')
@click.option('--what', help='Mute these objects (defaults to ["ignore"])', default=['ignore'])
def mute(mute, account, what):
    """Mute another account"""
    stm = shared_dpay_instance()
    if stm.rpc is not None:
        stm.rpc.rpcconnect()
    if not account:
        account = stm.config['default_account']
    if isinstance(what, str):
        what = [
         what]
    if not unlock_wallet(stm):
        return
    acc = Account(account, dpay_instance=stm)
    tx = acc.follow(mute, what=what)
    if stm.unsigned:
        if stm.nobroadcast:
            if stm.dpayid is not None:
                tx = stm.dpayid.url_from_tx(tx)
    tx = json.dumps(tx, indent=4)
    print(tx)


@cli.command()
@click.argument('unfollow', nargs=1)
@click.option('--account', '-a', help='UnFollow/UnMute from this account')
def unfollow(unfollow, account):
    """Unfollow/Unmute another account"""
    stm = shared_dpay_instance()
    if stm.rpc is not None:
        stm.rpc.rpcconnect()
    if not account:
        account = stm.config['default_account']
    if not unlock_wallet(stm):
        return
    acc = Account(account, dpay_instance=stm)
    tx = acc.unfollow(unfollow)
    if stm.unsigned:
        if stm.nobroadcast:
            if stm.dpayid is not None:
                tx = stm.dpayid.url_from_tx(tx)
    tx = json.dumps(tx, indent=4)
    print(tx)


@cli.command()
@click.option('--witness', help='Witness name')
@click.option('--maximum_block_size', help='Max block size')
@click.option('--account_creation_fee', help='Account creation fee')
@click.option('--bbd_interest_rate', help='BBD interest rate in percent')
@click.option('--url', help='Witness URL')
@click.option('--signing_key', help='Signing Key')
def witnessupdate(witness, maximum_block_size, account_creation_fee, bbd_interest_rate, url, signing_key):
    """Change witness properties"""
    stm = shared_dpay_instance()
    if stm.rpc is not None:
        stm.rpc.rpcconnect()
    if not witness:
        witness = stm.config['default_account']
    if not unlock_wallet(stm):
        return
    witness = Witness(witness, dpay_instance=stm)
    props = witness['props']
    if account_creation_fee is not None:
        props['account_creation_fee'] = str(Amount(('%.3f %s' % (float(account_creation_fee), stm.dpay_symbol)), dpay_instance=stm))
    if maximum_block_size is not None:
        props['maximum_block_size'] = int(maximum_block_size)
    if bbd_interest_rate is not None:
        props['bbd_interest_rate'] = int(float(bbd_interest_rate) * 100)
    tx = witness.update(signing_key or witness['signing_key'], url or witness['url'], props)
    if stm.unsigned:
        if stm.nobroadcast:
            if stm.dpayid is not None:
                tx = stm.dpayid.url_from_tx(tx)
    tx = json.dumps(tx, indent=4)
    print(tx)


@cli.command()
@click.argument('witness', nargs=1)
def witnessdisable(witness):
    """Disable a witness"""
    stm = shared_dpay_instance()
    if stm.rpc is not None:
        stm.rpc.rpcconnect()
    if not witness:
        witness = stm.config['default_account']
    if not unlock_wallet(stm):
        return
    witness = Witness(witness, dpay_instance=stm)
    if not witness.is_active:
        print('Cannot disable a disabled witness!')
        return
    props = witness['props']
    tx = witness.update('DWB1111111111111111111111111111111114T1Anm', witness['url'], props)
    if stm.unsigned:
        if stm.nobroadcast:
            if stm.dpayid is not None:
                tx = stm.dpayid.url_from_tx(tx)
    tx = json.dumps(tx, indent=4)
    print(tx)


@cli.command()
@click.argument('witness', nargs=1)
@click.argument('signing_key', nargs=1)
def witnessenable(witness, signing_key):
    """Enable a witness"""
    stm = shared_dpay_instance()
    if stm.rpc is not None:
        stm.rpc.rpcconnect()
    if not witness:
        witness = stm.config['default_account']
    if not unlock_wallet(stm):
        return
    witness = Witness(witness, dpay_instance=stm)
    props = witness['props']
    tx = witness.update(signing_key, witness['url'], props)
    if stm.unsigned:
        if stm.nobroadcast:
            if stm.dpayid is not None:
                tx = stm.dpayid.url_from_tx(tx)
    tx = json.dumps(tx, indent=4)
    print(tx)


@cli.command()
@click.argument('witness', nargs=1)
@click.argument('pub_signing_key', nargs=1)
@click.option('--maximum_block_size', help='Max block size', default=65536)
@click.option('--account_creation_fee', help='Account creation fee', default=0.1)
@click.option('--bbd_interest_rate', help='BBD interest rate in percent', default=0.0)
@click.option('--url', help='Witness URL', default='')
def witnesscreate(witness, pub_signing_key, maximum_block_size, account_creation_fee, bbd_interest_rate, url):
    """Create a witness"""
    stm = shared_dpay_instance()
    if stm.rpc is not None:
        stm.rpc.rpcconnect()
    if not unlock_wallet(stm):
        return
    props = {'account_creation_fee':Amount('%.3f %s' % (float(account_creation_fee), stm.dpay_symbol), dpay_instance=stm),  'maximum_block_size':int(maximum_block_size), 
     'bbd_interest_rate':int(bbd_interest_rate * 100)}
    tx = stm.witness_update(pub_signing_key, url, props, account=witness)
    if stm.unsigned:
        if stm.nobroadcast:
            if stm.dpayid is not None:
                tx = stm.dpayid.url_from_tx(tx)
    tx = json.dumps(tx, indent=4)
    print(tx)


@cli.command()
@click.argument('witness', nargs=1)
@click.argument('wif', nargs=1)
@click.option('--account_creation_fee', help='Account creation fee (float)')
@click.option('--account_subsidy_budget', help='Account subisidy per block')
@click.option('--account_subsidy_decay', help='Per block decay of the account subsidy pool')
@click.option('--maximum_block_size', help='Max block size')
@click.option('--bbd_interest_rate', help='BBD interest rate in percent')
@click.option('--new_signing_key', help='Set new signing key')
@click.option('--url', help='Witness URL')
def witnessproperties(witness, wif, account_creation_fee, account_subsidy_budget, account_subsidy_decay, maximum_block_size, bbd_interest_rate, new_signing_key, url):
    """Update witness properties of witness WITNESS with the witness signing key WIF"""
    stm = shared_dpay_instance()
    if stm.rpc is not None:
        stm.rpc.rpcconnect()
    props = {}
    if account_creation_fee is not None:
        props['account_creation_fee'] = Amount(('%.3f %s' % (float(account_creation_fee), stm.dpay_symbol)), dpay_instance=stm)
    if account_subsidy_budget is not None:
        props['account_subsidy_budget'] = int(account_subsidy_budget)
    if account_subsidy_decay is not None:
        props['account_subsidy_decay'] = int(account_subsidy_decay)
    if maximum_block_size is not None:
        props['maximum_block_size'] = int(maximum_block_size)
    if bbd_interest_rate is not None:
        props['bbd_interest_rate'] = int(bbd_interest_rate * 100)
    if new_signing_key is not None:
        props['new_signing_key'] = new_signing_key
    if url is not None:
        props['url'] = url
    tx = stm.witness_set_properties(wif, witness, props)
    if stm.unsigned:
        if stm.nobroadcast:
            if stm.dpayid is not None:
                tx = stm.dpayid.url_from_tx(tx)
    tx = json.dumps(tx, indent=4)
    print(tx)


@cli.command()
@click.argument('witness', nargs=1)
@click.argument('wif', nargs=1, required=False)
@click.option('--base', '-b', help='Set base manually, when not set the base is automatically calculated.')
@click.option('--quote', '-q', help='DPay quote manually, when not set the base is automatically calculated.')
@click.option('--support-peg', help='Supports peg adjusting the quote, is overwritten by --set-quote!', is_flag=True, default=False)
def witnessfeed(witness, wif, base, quote, support_peg):
    """Publish price feed for a witness"""
    stm = shared_dpay_instance()
    if stm.rpc is not None:
        stm.rpc.rpcconnect()
    else:
        if wif is None:
            if not unlock_wallet(stm):
                return
        else:
            witness = Witness(witness, dpay_instance=stm)
            market = Market(dpay_instance=stm)
            old_base = witness['bbd_exchange_rate']['base']
            old_quote = witness['bbd_exchange_rate']['quote']
            last_published_price = Price((witness['bbd_exchange_rate']), dpay_instance=stm)
            dpay_usd = None
            print('Old price %.3f (base: %s, quote %s)' % (float(last_published_price), old_base, old_quote))
            if quote is None:
                if not support_peg:
                    quote = Amount(('1.000 %s' % stm.dpay_symbol), dpay_instance=stm)
            if quote is None:
                latest_price = market.ticker()['latest']
                if dpay_usd is None:
                    dpay_usd = market.dpay_usd_implied()
                bbd_usd = float(latest_price.as_base(stm.bbd_symbol)) * dpay_usd
                quote = Amount((1.0 / bbd_usd), (stm.dpay_symbol), dpay_instance=stm)
            else:
                if str(quote[-5:]).upper() == stm.dpay_symbol:
                    quote = Amount(quote, dpay_instance=stm)
                else:
                    quote = Amount(quote, (stm.dpay_symbol), dpay_instance=stm)
                if base is None:
                    if dpay_usd is None:
                        dpay_usd = market.dpay_usd_implied()
                    base = Amount(dpay_usd, (stm.bbd_symbol), dpay_instance=stm)
                else:
                    if str(quote[-3:]).upper() == stm.bbd_symbol:
                        base = Amount(base, dpay_instance=stm)
                    else:
                        base = Amount(base, (stm.bbd_symbol), dpay_instance=stm)
        new_price = Price(base=base, quote=quote, dpay_instance=stm)
        print('New price %.3f (base: %s, quote %s)' % (float(new_price), base, quote))
        if wif is not None:
            props = {'bbd_exchange_rate': new_price}
            tx = stm.witness_set_properties(wif, witness['owner'], props)
        else:
            tx = witness.feed_publish(base, quote=quote)
    if stm.unsigned:
        if stm.nobroadcast:
            if stm.dpayid is not None:
                tx = stm.dpayid.url_from_tx(tx)
    tx = json.dumps(tx, indent=4)
    print(tx)


@cli.command()
@click.argument('witness', nargs=1)
def witness(witness):
    """ List witness information
    """
    stm = shared_dpay_instance()
    if stm.rpc is not None:
        stm.rpc.rpcconnect()
    else:
        witness = Witness(witness, dpay_instance=stm)
        witness_json = witness.json()
        witness_schedule = stm.get_witness_schedule()
        config = stm.get_config()
        if 'VIRTUAL_SCHEDULE_LAP_LENGTH2' in config:
            lap_length = int(config['VIRTUAL_SCHEDULE_LAP_LENGTH2'])
        else:
            lap_length = int(config['DPAY_VIRTUAL_SCHEDULE_LAP_LENGTH2'])
    rank = 0
    active_rank = 0
    found = False
    witnesses = WitnessesRankedByVote(limit=250, dpay_instance=stm)
    vote_sum = witnesses.get_votes_sum()
    for w in witnesses:
        rank += 1
        if w.is_active:
            active_rank += 1
        elif w['owner'] == witness['owner']:
            found = True
            break

    virtual_time_to_block_num = int(witness_schedule['num_scheduled_witnesses']) / (lap_length / (vote_sum + 1))
    t = PrettyTable(['Key', 'Value'])
    t.align = 'l'
    for key in sorted(witness_json):
        value = witness_json[key]
        if key in ('props', 'bbd_exchange_rate'):
            value = json.dumps(value, indent=4)
        t.add_row([key, value])

    if found:
        t.add_row(['rank', rank])
        t.add_row(['active_rank', active_rank])
    virtual_diff = int(witness_json['virtual_scheduled_time']) - int(witness_schedule['current_virtual_time'])
    block_diff_est = virtual_diff * virtual_time_to_block_num
    if active_rank > 20:
        t.add_row(['virtual_time_diff', virtual_diff])
        t.add_row(['block_diff_est', int(block_diff_est)])
        next_block_s = int(block_diff_est) * 3
        next_block_min = next_block_s / 60
        next_block_h = next_block_min / 60
        next_block_d = next_block_h / 24
        time_diff_est = ''
        if next_block_d > 1:
            time_diff_est = '%.2f days' % next_block_d
        else:
            if next_block_h > 1:
                time_diff_est = '%.2f hours' % next_block_h
            else:
                if next_block_min > 1:
                    time_diff_est = '%.2f minutes' % next_block_min
                else:
                    time_diff_est = '%.2f seconds' % next_block_s
        t.add_row(['time_diff_est', time_diff_est])
    print(t)


@cli.command()
@click.argument('account', nargs=1, required=False)
@click.option('--limit', help='How many witnesses should be shown', default=100)
def witnesses(account, limit):
    """ List witnesses
    """
    stm = shared_dpay_instance()
    if stm.rpc is not None:
        stm.rpc.rpcconnect()
    else:
        if account:
            account = Account(account, dpay_instance=stm)
            account_name = account['name']
            if account['proxy'] != '':
                account_name = account['proxy']
                account_type = 'Proxy'
            else:
                account_type = 'Account'
            witnesses = WitnessesVotedByAccount(account_name, dpay_instance=stm)
            print('%s: @%s (%d of 30)' % (account_type, account_name, len(witnesses)))
        else:
            witnesses = WitnessesRankedByVote(limit=limit, dpay_instance=stm)
    witnesses.printAsTable()


@cli.command()
@click.argument('account', nargs=1, required=False)
@click.option('--direction', default=None, help='in or out')
@click.option('--outgoing', '-o', help='Show outgoing votes', is_flag=True, default=False)
@click.option('--incoming', '-i', help='Show incoming votes', is_flag=True, default=False)
@click.option('--days', '-d', default=2.0, help='Limit shown vote history by this amount of days (default: 2)')
@click.option('--export', '-e', default=None, help='Export results to TXT-file')
def votes(account, direction, outgoing, incoming, days, export):
    """ List outgoing/incoming account votes
    """
    stm = shared_dpay_instance()
    if stm.rpc is not None:
        stm.rpc.rpcconnect()
    if not account:
        account = stm.config['default_account']
    if direction is None:
        if not incoming:
            if not outgoing:
                direction = 'in'
    utc = pytz.timezone('UTC')
    limit_time = utc.localize(datetime.utcnow()) - timedelta(days=days)
    out_votes_str = ''
    in_votes_str = ''
    if direction == 'out' or outgoing:
        votes = AccountVotes(account, start=limit_time, dpay_instance=stm)
        out_votes_str = votes.printAsTable(start=limit_time, return_str=True)
    if direction == 'in' or incoming:
        account = Account(account, dpay_instance=stm)
        votes_list = []
        for v in account.history(start=limit_time, only_ops=['vote']):
            votes_list.append(v)

        votes = ActiveVotes(votes_list, dpay_instance=stm)
        in_votes_str = votes.printAsTable(votee=(account['name']), return_str=True)
    if export:
        with open(export, 'w') as (w):
            w.write(out_votes_str)
            w.write('\n')
            w.write(in_votes_str)
    else:
        print(out_votes_str)
        print(in_votes_str)


@cli.command()
@click.argument('authorperm', nargs=1, required=False)
@click.option('--account', '-a', help='Show only curation for this account')
@click.option('--limit', '-m', help='Show only the first minutes')
@click.option('--min-vote', '-v', help='Show only votes higher than the given value')
@click.option('--max-vote', '-w', help='Show only votes lower than the given value')
@click.option('--min-performance', '-x', help='Show only votes with performance higher than the given value')
@click.option('--max-performance', '-y', help='Show only votes with performance lower than the given value')
@click.option('--payout', default=None, help='Show the curation for a potential payout in BBD as float')
@click.option('--export', '-e', default=None, help='Export results to HTML-file')
@click.option('--short', '-s', is_flag=True, default=False, help='Show only Curation without sum')
@click.option('--length', '-l', help='Limits the permlink character length', default=None)
@click.option('--permlink', '-p', help='Show the permlink for each entry', is_flag=True, default=False)
@click.option('--title', '-t', help='Show the title for each entry', is_flag=True, default=False)
@click.option('--days', '-d', default=7.0, help='Limit shown rewards by this amount of days (default: 7), max is 7 days.')
def curation(authorperm, account, limit, min_vote, max_vote, min_performance, max_performance, payout, export, short, length, permlink, title, days):
    """ Lists curation rewards of all votes for authorperm

        When authorperm is empty or "all", the curation rewards
        for all account votes are shown.

        authorperm can also be a number. e.g. 5 is equivalent to
        the fifth account vote in the given time duration (default is 7 days)

    """
    stm = shared_dpay_instance()
    if stm.rpc is not None:
        stm.rpc.rpcconnect()
    else:
        if authorperm is None:
            authorperm = 'all'
        elif account is None and authorperm is not 'all':
            show_all_voter = True
        else:
            show_all_voter = False
        if authorperm == 'all' or authorperm.isdigit():
            if not account:
                account = stm.config['default_account']
            utc = pytz.timezone('UTC')
            limit_time = utc.localize(datetime.utcnow()) - timedelta(days=days)
            votes = AccountVotes(account, start=limit_time, dpay_instance=stm)
            authorperm_list = [Comment((vote.authorperm), dpay_instance=stm) for vote in votes]
            if authorperm.isdigit():
                if len(authorperm_list) < int(authorperm):
                    raise ValueError('Authorperm id must be lower than %d' % (len(authorperm_list) + 1))
                authorperm_list = [
                 authorperm_list[(int(authorperm) - 1)]['authorperm']]
                all_posts = False
            else:
                all_posts = True
        else:
            authorperm_list = [
             authorperm]
        all_posts = False
    if all_posts:
        if permlink:
            t = PrettyTable(['Author', 'permlink', 'Voting time', 'Vote', 'Early vote loss', 'Curation', 'Performance'])
            t.align = 'l'
    if all_posts and title:
        t = PrettyTable(['Author', 'permlink', 'Voting time', 'Vote', 'Early vote loss', 'Curation', 'Performance'])
        t.align = 'l'
    else:
        if all_posts:
            t = PrettyTable(['Author', 'Voting time', 'Vote', 'Early vote loss', 'Curation', 'Performance'])
            t.align = 'l'
        elif export and permlink:
            t = PrettyTable(['Author', 'permlink', 'Voter', 'Voting time', 'Vote', 'Early vote loss', 'Curation', 'Performance'])
            t.align = 'l'
        elif export and title:
            t = PrettyTable(['Author', 'permlink', 'Voter', 'Voting time', 'Vote', 'Early vote loss', 'Curation', 'Performance'])
            t.align = 'l'
        else:
            if export:
                t = PrettyTable(['Author', 'Voter', 'Voting time', 'Vote', 'Early vote loss', 'Curation', 'Performance'])
                t.align = 'l'
            else:
                t = PrettyTable(['Voter', 'Voting time', 'Vote', 'Early vote loss', 'Curation', 'Performance'])
                t.align = 'l'
    index = 0
    for authorperm in authorperm_list:
        index += 1
        comment = Comment(authorperm, dpay_instance=stm)
        if payout is not None:
            if comment.is_pending():
                payout = float(payout)
        if payout is not None:
            payout = None
        curation_rewards_BBD = comment.get_curation_rewards(pending_payout_BBD=True, pending_payout_value=payout)
        curation_rewards_SP = comment.get_curation_rewards(pending_payout_BBD=False, pending_payout_value=payout)
        rows = []
        sum_curation = [0, 0, 0, 0]
        max_curation = [0, 0, 0, 0, 0, 0]
        highest_vote = [0, 0, 0, 0, 0, 0]
        for vote in comment['active_votes']:
            vote_BBD = stm.rshares_to_bbd(int(vote['rshares']))
            curation_BBD = curation_rewards_BBD['active_votes'][vote['voter']]
            curation_SP = curation_rewards_SP['active_votes'][vote['voter']]
            if vote_BBD > 0:
                penalty = comment.get_curation_penalty(vote_time=(vote['time'])) * vote_BBD
                performance = float(curation_BBD) / vote_BBD * 100
            else:
                performance = 0
                penalty = 0
            vote_befor_min = (vote['time'] - comment['created']).total_seconds() / 60
            sum_curation[0] += vote_BBD
            sum_curation[1] += penalty
            sum_curation[2] += float(curation_SP)
            sum_curation[3] += float(curation_BBD)
            row = [vote['voter'],
             vote_befor_min,
             vote_BBD,
             penalty,
             float(curation_SP),
             performance]
            if row[(-1)] > max_curation[(-1)]:
                max_curation = row
            if row[2] > highest_vote[2]:
                highest_vote = row
            rows.append(row)

        sortedList = sorted(rows, key=(lambda row: row[1]), reverse=False)
        new_row = []
        new_row2 = []
        voter = []
        voter2 = []
        if all_posts or export:
            if permlink:
                if length:
                    new_row = [
                     comment.author, comment.permlink[:int(length)]]
                else:
                    new_row = [
                     comment.author, comment.permlink]
                new_row2 = [
                 '', '']
        if all_posts or export:
            if title:
                if length:
                    new_row = [
                     comment.author, comment.title[:int(length)]]
                else:
                    new_row = [
                     comment.author, comment.title]
                new_row2 = [
                 '', '']
        if all_posts or export:
            new_row = [
             comment.author]
            new_row2 = ['']
        if not all_posts:
            voter = [
             '']
            voter2 = ['']
        found_voter = False
        for row in sortedList:
            if limit is not None:
                if row[1] > float(limit):
                    continue
                else:
                    if min_vote is not None:
                        if float(row[2]) < float(min_vote):
                            continue
                    else:
                        if max_vote is not None:
                            if float(row[2]) > float(max_vote):
                                continue
                        if min_performance is not None:
                            if float(row[5]) < float(min_performance):
                                continue
                    if max_performance is not None:
                        if float(row[5]) > float(max_performance):
                            continue
                if show_all_voter or account == row[0]:
                    if not all_posts:
                        voter = [
                         row[0]]
                    else:
                        if all_posts:
                            new_row[0] = '%d. %s' % (index, comment.author)
                        found_voter = found_voter or True
                    t.add_row(new_row + voter + ['%.1f min' % row[1],
                     '%.3f BBD' % float(row[2]),
                     '%.3f BBD' % float(row[3]),
                     '%.3f BP' % row[4],
                     '%.1f %%' % row[5]])
                    if len(authorperm_list) == 1:
                        new_row = new_row2

        if not short:
            if found_voter:
                t.add_row(new_row2 + voter2 + ['', '', '', '', ''])
                if sum_curation[0] > 0:
                    curation_sum_percentage = sum_curation[3] / sum_curation[0] * 100
                else:
                    curation_sum_percentage = 0
                sum_line = new_row2 + voter2
                sum_line[-1] = 'High. vote'
                t.add_row(sum_line + ['%.1f min' % highest_vote[1],
                 '%.3f BBD' % float(highest_vote[2]),
                 '%.3f BBD' % float(highest_vote[3]),
                 '%.3f BP' % highest_vote[4],
                 '%.1f %%' % highest_vote[5]])
                sum_line[-1] = 'High. Cur.'
                t.add_row(sum_line + ['%.1f min' % max_curation[1],
                 '%.3f BBD' % float(max_curation[2]),
                 '%.3f BBD' % float(max_curation[3]),
                 '%.3f BP' % max_curation[4],
                 '%.1f %%' % max_curation[5]])
                sum_line[-1] = 'Sum'
                t.add_row(sum_line + ['-',
                 '%.3f BBD' % sum_curation[0],
                 '%.3f BBD' % sum_curation[1],
                 '%.3f BP' % sum_curation[2],
                 '%.2f %%' % curation_sum_percentage])
                if all_posts or export:
                    t.add_row(new_row2 + voter2 + ['-', '-', '-', '-', '-'])
            if not (all_posts or export):
                print('curation for %s' % authorperm)
                print(t)

    if export:
        with open(export, 'w') as (w):
            w.write(str(t.get_html_string()))
    if all_posts:
        print('curation for @%s' % account)
        print(t)


@cli.command()
@click.argument('accounts', nargs=(-1), required=False)
@click.option('--only-sum', '-s', help='Show only the sum', is_flag=True, default=False)
@click.option('--post', '-p', help='Show post payout', is_flag=True, default=False)
@click.option('--comment', '-c', help='Show comments payout', is_flag=True, default=False)
@click.option('--curation', '-v', help='Shows  curation', is_flag=True, default=False)
@click.option('--length', '-l', help='Limits the permlink character length', default=None)
@click.option('--author', '-a', help='Show the author for each entry', is_flag=True, default=False)
@click.option('--permlink', '-e', help='Show the permlink for each entry', is_flag=True, default=False)
@click.option('--title', '-t', help='Show the title for each entry', is_flag=True, default=False)
@click.option('--days', '-d', default=7.0, help='Limit shown rewards by this amount of days (default: 7)')
def rewards(accounts, only_sum, post, comment, curation, length, author, permlink, title, days):
    """ Lists received rewards
    """
    stm = shared_dpay_instance()
    if stm.rpc is not None:
        stm.rpc.rpcconnect()
    if not accounts:
        accounts = [
         stm.config['default_account']]
    if not comment:
        if not curation:
            if not post:
                post = True
                permlink = True
    if days < 0:
        days = 1
    utc = pytz.timezone('UTC')
    now = utc.localize(datetime.utcnow())
    limit_time = now - timedelta(days=days)
    for account in accounts:
        sum_reward = [
         0, 0, 0, 0, 0]
        account = Account(account, dpay_instance=stm)
        median_price = Price((stm.get_current_median_history()), dpay_instance=stm)
        m = Market(dpay_instance=stm)
        latest = m.ticker()['latest']
        if author:
            if permlink:
                t = PrettyTable(['Author', 'Permlink', 'Payout', 'BBD', 'BP + BEX', 'Liquid USD', 'Invested USD'])
        if author and title:
            t = PrettyTable(['Author', 'Title', 'Payout', 'BBD', 'BP + BEX', 'Liquid USD', 'Invested USD'])
        else:
            if author:
                t = PrettyTable(['Author', 'Payout', 'BBD', 'BP + BEX', 'Liquid USD', 'Invested USD'])
            else:
                if not author:
                    if permlink:
                        t = PrettyTable(['Permlink', 'Payout', 'BBD', 'BP + BEX', 'Liquid USD', 'Invested USD'])
                    elif not author:
                        if title:
                            t = PrettyTable(['Title', 'Payout', 'BBD', 'BP + BEX', 'Liquid USD', 'Invested USD'])
                    else:
                        t = PrettyTable(['Received', 'BBD', 'BP + BEX', 'Liquid USD', 'Invested USD'])
                else:
                    t.align = 'l'
                    rows = []
                    start_op = account.estimate_virtual_op_num(limit_time)
                    if start_op > 0:
                        start_op -= 1
                only_ops = [
                 'author_reward', 'curation_reward']
                progress_length = (account.virtual_op_count() - start_op) / 1000
                with click.progressbar(account.history(start=start_op, use_block_num=False, only_ops=only_ops), length=progress_length) as (comment_hist):
                    for v in comment_hist:
                        if not curation:
                            if v['type'] == 'curation_reward':
                                continue
                            else:
                                if not post:
                                    if not comment:
                                        if v['type'] == 'author_reward':
                                            continue
                                if v['type'] == 'author_reward':
                                    c = Comment(v, dpay_instance=stm)
                                    try:
                                        c.refresh()
                                    except exceptions.ContentDoesNotExistsException:
                                        continue

                                    if not post:
                                        if not c.is_comment():
                                            continue
                                    if not comment:
                                        if c.is_comment():
                                            continue
                                    payout_BBD = Amount((v['bbd_payout']), dpay_instance=stm)
                                    payout_DPAY = Amount((v['dpay_payout']), dpay_instance=stm)
                                    sum_reward[0] += float(payout_BBD)
                                    sum_reward[1] += float(payout_DPAY)
                                    payout_SP = stm.vests_to_sp(Amount((v['vesting_payout']), dpay_instance=stm))
                                    sum_reward[2] += float(payout_SP)
                                    liquid_USD = float(payout_BBD) / float(latest) * float(median_price) + float(payout_DPAY) * float(median_price)
                                    sum_reward[3] += liquid_USD
                                    invested_USD = float(payout_SP) * float(median_price)
                                    sum_reward[4] += invested_USD
                                    if c.is_comment():
                                        permlink_row = c.parent_permlink
                                    else:
                                        if title:
                                            permlink_row = c.title
                                        else:
                                            permlink_row = c.permlink
                                    rows.append([c['author'],
                                     permlink_row,
                                     (now - formatTimeString(v['timestamp'])).total_seconds() / 60 / 60 / 24,
                                     payout_BBD,
                                     payout_DPAY,
                                     payout_SP,
                                     liquid_USD,
                                     invested_USD])
                                elif v['type'] == 'curation_reward':
                                    reward = Amount((v['reward']), dpay_instance=stm)
                                    payout_SP = stm.vests_to_sp(reward)
                                    liquid_USD = 0
                                    invested_USD = float(payout_SP) * float(median_price)
                                    sum_reward[2] += float(payout_SP)
                                    sum_reward[4] += invested_USD
                                    if title:
                                        c = Comment((construct_authorperm(v['comment_author'], v['comment_permlink'])), dpay_instance=stm)
                                        permlink_row = c.title
                                    else:
                                        permlink_row = v['comment_permlink']
                                    rows.append([v['comment_author'],
                                     permlink_row,
                                     (now - formatTimeString(v['timestamp'])).total_seconds() / 60 / 60 / 24,
                                     0.0,
                                     0.0,
                                     payout_SP,
                                     liquid_USD,
                                     invested_USD])

                sortedList = sorted(rows, key=(lambda row: row[2]), reverse=False)
                if only_sum:
                    sortedList = []
                for row in sortedList:
                    if length:
                        permlink_row = row[1][:int(length)]
                    else:
                        permlink_row = row[1]
                    if author and (permlink or title):
                        t.add_row([row[0],
                         permlink_row,
                         '%.1f days' % row[2],
                         '%.3f' % float(row[3]),
                         '%.3f' % (float(row[4]) + float(row[5])),
                         '%.2f $' % row[6],
                         '%.2f $' % row[7]])
                    elif author:
                        if not (permlink or title):
                            t.add_row([row[0],
                             '%.1f days' % row[2],
                             '%.3f' % float(row[3]),
                             '%.3f' % (float(row[4]) + float(row[5])),
                             '%.2f $' % row[5],
                             '%.2f $' % row[6]])
                    elif not author:
                        if permlink or title:
                            t.add_row([permlink_row,
                             '%.1f days' % row[2],
                             '%.3f' % float(row[3]),
                             '%.3f' % (float(row[4]) + float(row[5])),
                             '%.2f $' % row[5],
                             '%.2f $' % row[6]])
                    else:
                        t.add_row(['%.1f days' % row[2],
                         '%.3f' % float(row[3]),
                         '%.3f' % (float(row[4]) + float(row[5])),
                         '%.2f $' % row[5],
                         '%.2f $' % row[6]])

                if author and (permlink or title):
                    if not only_sum:
                        t.add_row(['', '', '', '', '', '', ''])
                    t.add_row(['Sum',
                     '-',
                     '-',
                     '%.2f BBD' % sum_reward[0],
                     '%.2f BP' % (sum_reward[1] + sum_reward[2]),
                     '%.2f $' % sum_reward[3],
                     '%.2f $' % sum_reward[4]])
                elif not author and not (permlink or title):
                    t.add_row(['', '', '', '', ''])
                    t.add_row(['Sum',
                     '%.2f BBD' % sum_reward[0],
                     '%.2f BP' % (sum_reward[1] + sum_reward[2]),
                     '%.2f $' % sum_reward[2],
                     '%.2f $' % sum_reward[3]])
                else:
                    t.add_row(['', '', '', '', '', ''])
                    t.add_row(['Sum',
                     '-',
                     '%.2f BBD' % sum_reward[0],
                     '%.2f BP' % (sum_reward[1] + sum_reward[2]),
                     '%.2f $' % sum_reward[3],
                     '%.2f $' % sum_reward[4]])
        message = '\nShowing '
        if post:
            if comment + curation == 0:
                message += 'post '
            else:
                if comment + curation == 1:
                    message += 'post and '
                else:
                    message += 'post, '
        if comment:
            if curation == 0:
                message += 'comment '
            else:
                message += 'comment and '
        if curation:
            message += 'curation '
        message += 'rewards for @%s' % account.name
        print(message)
        print(t)


@cli.command()
@click.argument('accounts', nargs=(-1), required=False)
@click.option('--only-sum', '-s', help='Show only the sum', is_flag=True, default=False)
@click.option('--post', '-p', help='Show pending post payout', is_flag=True, default=False)
@click.option('--comment', '-c', help='Show pending comments payout', is_flag=True, default=False)
@click.option('--curation', '-v', help='Shows  pending curation', is_flag=True, default=False)
@click.option('--length', '-l', help='Limits the permlink character length', default=None)
@click.option('--author', '-a', help='Show the author for each entry', is_flag=True, default=False)
@click.option('--permlink', '-e', help='Show the permlink for each entry', is_flag=True, default=False)
@click.option('--title', '-t', help='Show the title for each entry', is_flag=True, default=False)
@click.option('--days', '-d', default=7.0, help='Limit shown rewards by this amount of days (default: 7), max is 7 days.')
def pending(accounts, only_sum, post, comment, curation, length, author, permlink, title, days):
    """ Lists pending rewards
    """
    stm = shared_dpay_instance()
    if stm.rpc is not None:
        stm.rpc.rpcconnect()
    if not accounts:
        accounts = [
         stm.config['default_account']]
    if not comment:
        if not curation:
            if not post:
                post = True
                permlink = True
    if days < 0:
        days = 1
    if days > 7:
        days = 7
    utc = pytz.timezone('UTC')
    limit_time = utc.localize(datetime.utcnow()) - timedelta(days=days)
    for account in accounts:
        sum_reward = [
         0, 0, 0, 0]
        account = Account(account, dpay_instance=stm)
        median_price = Price((stm.get_current_median_history()), dpay_instance=stm)
        m = Market(dpay_instance=stm)
        latest = m.ticker()['latest']
        if author:
            if permlink:
                t = PrettyTable(['Author', 'Permlink', 'Cashout', 'BBD', 'BP', 'Liquid USD', 'Invested USD'])
        if author and title:
            t = PrettyTable(['Author', 'Title', 'Cashout', 'BBD', 'BP', 'Liquid USD', 'Invested USD'])
        else:
            if author:
                t = PrettyTable(['Author', 'Cashout', 'BBD', 'BP', 'Liquid USD', 'Invested USD'])
            else:
                if not author:
                    if permlink:
                        t = PrettyTable(['Permlink', 'Cashout', 'BBD', 'BP', 'Liquid USD', 'Invested USD'])
                else:
                    if not author:
                        if title:
                            t = PrettyTable(['Title', 'Cashout', 'BBD', 'BP', 'Liquid USD', 'Invested USD'])
                        else:
                            t = PrettyTable(['Cashout', 'BBD', 'BP', 'Liquid USD', 'Invested USD'])
                    else:
                        t.align = 'l'
                        rows = []
                        c_list = {}
                        start_op = account.estimate_virtual_op_num(limit_time)
                        if start_op > 0:
                            start_op -= 1
                    progress_length = (account.virtual_op_count() - start_op) / 1000
                    with click.progressbar((map(Comment, account.history(start=start_op, use_block_num=False, only_ops=['comment']))), length=progress_length) as (comment_hist):
                        for v in comment_hist:
                            try:
                                v.refresh()
                            except exceptions.ContentDoesNotExistsException:
                                continue

                            author_reward = v.get_author_rewards()
                            if float(author_reward['total_payout_BBD']) < 0.001:
                                continue
                            if v.permlink in c_list:
                                continue
                            c_list[v.permlink] = 1
                            if not v.is_pending():
                                continue
                            if not post:
                                if not v.is_comment():
                                    continue
                            if not comment:
                                if v.is_comment():
                                    continue
                            if v['author'] != account['name']:
                                continue
                            payout_BBD = author_reward['payout_BBD']
                            sum_reward[0] += float(payout_BBD)
                            payout_SP = author_reward['payout_SP']
                            sum_reward[1] += float(payout_SP)
                            liquid_USD = float(author_reward['payout_BBD']) / float(latest) * float(median_price)
                            sum_reward[2] += liquid_USD
                            invested_USD = float(author_reward['payout_SP']) * float(median_price)
                            sum_reward[3] += invested_USD
                            if v.is_comment():
                                permlink_row = v.permlink
                            else:
                                if title:
                                    permlink_row = v.title
                                else:
                                    permlink_row = v.permlink
                            rows.append([v['author'],
                             permlink_row,
                             (v['created'] - limit_time).total_seconds() / 60 / 60 / 24,
                             payout_BBD,
                             payout_SP,
                             liquid_USD,
                             invested_USD])

                    if curation:
                        votes = AccountVotes(account, start=limit_time, dpay_instance=stm)
                        for vote in votes:
                            c = Comment((vote['authorperm']), dpay_instance=stm)
                            rewards = c.get_curation_rewards()
                            if not rewards['pending_rewards']:
                                continue
                            days_to_payout = (c['created'] - limit_time).total_seconds() / 60 / 60 / 24
                            if days_to_payout < 0:
                                pass
                            else:
                                payout_SP = rewards['active_votes'][account['name']]
                                liquid_USD = 0
                                invested_USD = float(payout_SP) * float(median_price)
                                sum_reward[1] += float(payout_SP)
                                sum_reward[3] += invested_USD
                                if title:
                                    permlink_row = c.title
                                else:
                                    permlink_row = c.permlink
                                rows.append([c['author'],
                                 permlink_row,
                                 days_to_payout,
                                 0.0,
                                 payout_SP,
                                 liquid_USD,
                                 invested_USD])

                    sortedList = sorted(rows, key=(lambda row: row[2]), reverse=True)
                    if only_sum:
                        sortedList = []
                for row in sortedList:
                    if length:
                        permlink_row = row[1][:int(length)]
                    else:
                        permlink_row = row[1]
                    if author and (permlink or title):
                        t.add_row([row[0],
                         permlink_row,
                         '%.1f days' % row[2],
                         '%.3f' % float(row[3]),
                         '%.3f' % float(row[4]),
                         '%.2f $' % row[5],
                         '%.2f $' % row[6]])
                    elif author:
                        if not (permlink or title):
                            t.add_row([row[0],
                             '%.1f days' % row[2],
                             '%.3f' % float(row[3]),
                             '%.3f' % float(row[4]),
                             '%.2f $' % row[5],
                             '%.2f $' % row[6]])
                    elif not author:
                        if permlink or title:
                            t.add_row([permlink_row,
                             '%.1f days' % row[2],
                             '%.3f' % float(row[3]),
                             '%.3f' % float(row[4]),
                             '%.2f $' % row[5],
                             '%.2f $' % row[6]])
                    else:
                        t.add_row(['%.1f days' % row[2],
                         '%.3f' % float(row[3]),
                         '%.3f' % float(row[4]),
                         '%.2f $' % row[5],
                         '%.2f $' % row[6]])

                if author and (permlink or title):
                    if not only_sum:
                        t.add_row(['', '', '', '', '', '', ''])
                    t.add_row(['Sum',
                     '-',
                     '-',
                     '%.2f BBD' % sum_reward[0],
                     '%.2f BP' % sum_reward[1],
                     '%.2f $' % sum_reward[2],
                     '%.2f $' % sum_reward[3]])
                elif not author and not (permlink or title):
                    t.add_row(['', '', '', '', ''])
                    t.add_row(['Sum',
                     '%.2f BBD' % sum_reward[0],
                     '%.2f BP' % sum_reward[1],
                     '%.2f $' % sum_reward[2],
                     '%.2f $' % sum_reward[3]])
                else:
                    t.add_row(['', '', '', '', '', ''])
                    t.add_row(['Sum',
                     '-',
                     '%.2f BBD' % sum_reward[0],
                     '%.2f BP' % sum_reward[1],
                     '%.2f $' % sum_reward[2],
                     '%.2f $' % sum_reward[3]])
        message = '\nShowing pending '
        if post:
            if comment + curation == 0:
                message += 'post '
            else:
                if comment + curation == 1:
                    message += 'post and '
                else:
                    message += 'post, '
        if comment:
            if curation == 0:
                message += 'comment '
            else:
                message += 'comment and '
        if curation:
            message += 'curation '
        message += 'rewards for @%s' % account.name
        print(message)
        print(t)


@cli.command()
@click.argument('account', nargs=1, required=False)
@click.option('--reward_dpay', help='Amount of BEX you would like to claim', default=0)
@click.option('--reward_bbd', help='Amount of BBD you would like to claim', default=0)
@click.option('--reward_vests', help='Amount of VESTS you would like to claim', default=0)
@click.option('--claim_all_dpay', help='Claim all BEX, overwrites reward_dpay', is_flag=True)
@click.option('--claim_all_bbd', help='Claim all BBD, overwrites reward_bbd', is_flag=True)
@click.option('--claim_all_vests', help='Claim all VESTS, overwrites reward_vests', is_flag=True)
def claimreward(account, reward_dpay, reward_bbd, reward_vests, claim_all_dpay, claim_all_bbd, claim_all_vests):
    """Claim reward balances

        By default, this will claim ``all`` outstanding balances.
    """
    stm = shared_dpay_instance()
    if stm.rpc is not None:
        stm.rpc.rpcconnect()
    if not account:
        account = stm.config['default_account']
    acc = Account(account, dpay_instance=stm)
    r = acc.balances['rewards']
    if r[0].amount + r[1].amount + r[2].amount == 0:
        print('Nothing to claim.')
        return
    if not unlock_wallet(stm):
        return
    if claim_all_dpay:
        reward_dpay = r[0]
    if claim_all_bbd:
        reward_bbd = r[1]
    if claim_all_vests:
        reward_vests = r[2]
    tx = acc.claim_reward_balance(reward_dpay, reward_bbd, reward_vests)
    if stm.unsigned:
        if stm.nobroadcast:
            if stm.dpayid is not None:
                tx = stm.dpayid.url_from_tx(tx)
    tx = json.dumps(tx, indent=4)
    print(tx)


@cli.command()
@click.argument('blocknumber', nargs=1, required=False)
@click.option('--trx', '-t', help='Show only one transaction number', default=None)
@click.option('--use-api', '-u', help='Uses the get_potential_signatures api call', is_flag=True, default=False)
def verify(blocknumber, trx, use_api):
    """Returns the public signing keys for a block"""
    stm = shared_dpay_instance()
    if stm.rpc is not None:
        stm.rpc.rpcconnect()
    b = Blockchain(dpay_instance=stm)
    i = 0
    if not blocknumber:
        blocknumber = b.get_current_block_num()
    try:
        int(blocknumber)
        block = Block(blocknumber, dpay_instance=stm)
        if trx is not None:
            i = int(trx)
            trxs = [block.transactions[int(trx)]]
        else:
            trxs = block.transactions
    except Exception:
        trxs = [
         b.get_transaction(blocknumber)]
        blocknumber = trxs[0]['block_num']

    wallet = Wallet(dpay_instance=stm)
    t = PrettyTable(['trx', 'Signer key', 'Account'])
    t.align = 'l'
    if not use_api:
        from dpayclibase.signedtransactions import Signed_Transaction
    for trx in trxs:
        if not use_api:
            signed_tx = Signed_Transaction(trx.copy())
            public_keys = []
            for key in signed_tx.verify(chain=(stm.chain_params), recover_parameter=True):
                public_keys.append(format(Base58(key, prefix=(stm.prefix)), stm.prefix))

        else:
            tx = TransactionBuilder(tx=trx, dpay_instance=stm)
            public_keys = tx.get_potential_signatures()
        accounts = []
        empty_public_keys = []
        for key in public_keys:
            account = wallet.getAccountFromPublicKey(key)
            if account is None:
                empty_public_keys.append(key)
            else:
                accounts.append(account)

        new_public_keys = []
        for key in public_keys:
            if key not in empty_public_keys or use_api:
                new_public_keys.append(key)

        if isinstance(new_public_keys, list):
            if len(new_public_keys) == 1:
                new_public_keys = new_public_keys[0]
            else:
                new_public_keys = json.dumps(new_public_keys, indent=4)
        elif isinstance(accounts, list) and len(accounts) == 1:
            accounts = accounts[0]
        else:
            accounts = json.dumps(accounts, indent=4)
        t.add_row(['%d' % i, new_public_keys, accounts])
        i += 1

    print(t)


@cli.command()
@click.argument('objects', nargs=(-1))
def info(objects):
    """ Show basic blockchain info

        General information about the blockchain, a block, an account,
        a post/comment and a public key
    """
    stm = shared_dpay_instance()
    if stm.rpc is not None:
        stm.rpc.rpcconnect()
    if not objects:
        t = PrettyTable(['Key', 'Value'])
        t.align = 'l'
        info = stm.get_dynamic_global_properties()
        median_price = stm.get_current_median_history()
        dpay_per_mvest = stm.get_dpay_per_mvest()
        chain_props = stm.get_chain_properties()
        price = Amount((median_price['base']), dpay_instance=stm).amount / Amount((median_price['quote']),
          dpay_instance=stm).amount
        for key in info:
            t.add_row([key, info[key]])

        t.add_row(['bex per mvest', dpay_per_mvest])
        t.add_row(['internal price', price])
        t.add_row(['account_creation_fee', chain_props['account_creation_fee']])
        print(t.get_string(sortby='Key'))
    for obj in objects:
        if re.match('^[0-9-]*$', obj) or re.match('^-[0-9]*$', obj) or re.match('^[0-9-]*:[0-9]', obj) or re.match('^[0-9-]*:-[0-9]', obj):
            tran_nr = ''
            if re.match('^[0-9-]*:[0-9-]', obj):
                obj, tran_nr = obj.split(':')
            if int(obj) < 1:
                b = Blockchain(dpay_instance=stm)
                block_number = b.get_current_block_num() + int(obj) - 1
            else:
                block_number = obj
            block = Block(block_number, dpay_instance=stm)
            if block:
                t = PrettyTable(['Key', 'Value'])
                t.align = 'l'
                block_json = block.json()
                for key in sorted(block_json):
                    value = block_json[key]
                    if key == 'transactions' and not bool(tran_nr):
                        t.add_row(['Nr. of transactions', len(value)])
                    elif key == 'transactions' and bool(tran_nr):
                        if int(tran_nr) < 0:
                            tran_nr = len(value) + int(tran_nr)
                        else:
                            tran_nr = int(tran_nr)
                    elif len(value) > tran_nr - 1:
                        if tran_nr > -1:
                            t_value = json.dumps((value[tran_nr]), indent=4)
                            t.add_row(['transaction %d/%d' % (tran_nr, len(value)), t_value])
                        elif key == 'transaction_ids':
                            if not bool(tran_nr):
                                t.add_row(['Nr. of transaction_ids', len(value)])
                        elif key == 'transaction_ids' and bool(tran_nr):
                            if int(tran_nr) < 0:
                                tran_nr = len(value) + int(tran_nr)
                            else:
                                tran_nr = int(tran_nr)
                        elif len(value) > tran_nr - 1:
                            if tran_nr > -1:
                                t.add_row(['transaction_id %d/%d' % (int(tran_nr), len(value)), value[tran_nr]])
                            else:
                                t.add_row([key, value])

                print(t)
            else:
                print('Block number %s unknown' % obj)
        elif re.match('^[a-zA-Z0-9\\-\\._]{2,16}$', obj):
            account = Account(obj, dpay_instance=stm)
            t = PrettyTable(['Key', 'Value'])
            t.align = 'l'
            account_json = account.json()
            for key in sorted(account_json):
                value = account_json[key]
                if key == 'json_metadata':
                    value = json.dumps((json.loads(value or '{}')), indent=4)
                else:
                    if key in ('posting', 'witness_votes', 'active', 'owner'):
                        value = json.dumps(value, indent=4)
                    else:
                        if key == 'reputation':
                            if int(value) > 0:
                                value = int(value)
                                rep = account.rep
                                value = '{:.2f} ({:d})'.format(rep, value)
                if isinstance(value, dict):
                    if 'asset' in value:
                        value = str(account[key])
                t.add_row([key, value])

            print(t)
            try:
                witness = Witness(obj, dpay_instance=stm)
                witness_json = witness.json()
                t = PrettyTable(['Key', 'Value'])
                t.align = 'l'
                for key in sorted(witness_json):
                    value = witness_json[key]
                    if key in ('props', 'bbd_exchange_rate'):
                        value = json.dumps(value, indent=4)
                    t.add_row([key, value])

                print(t)
            except exceptions.WitnessDoesNotExistsException as e:
                print(str(e))

        else:
            if re.match('^' + stm.prefix + '.{48,55}$', obj):
                account = stm.wallet.getAccountFromPublicKey(obj)
                if account:
                    account = Account(account, dpay_instance=stm)
                    key_type = stm.wallet.getKeyType(account, obj)
                    t = PrettyTable(['Account', 'Key_type'])
                    t.align = 'l'
                    t.add_row([account['name'], key_type])
                    print(t)
                else:
                    print('Public Key %s not known' % obj)
            else:
                if re.match('.*@.{3,16}/.*$', obj):
                    post = Comment(obj, dpay_instance=stm)
                    post_json = post.json()
                    if post_json:
                        t = PrettyTable(['Key', 'Value'])
                        t.align = 'l'
                        for key in sorted(post_json):
                            if key in ('body', 'active_votes'):
                                value = 'not shown'
                            else:
                                value = post_json[key]
                            if key in ('json_metadata', ):
                                value = json.loads(value)
                                value = json.dumps(value, indent=4)
                            else:
                                if key in ('tags', 'active_votes'):
                                    value = json.dumps(value, indent=4)
                            t.add_row([key, value])

                        print(t)
                    else:
                        print('Post now known' % obj)
                else:
                    print("Couldn't identify object to read")


@cli.command()
@click.argument('account', nargs=1, required=False)
@click.option('--signing-account', '-s', help='Signing account, when empty account is used.')
def userdata(account, signing_account):
    """ Get the account's email address and phone number.

        The request has to be signed by the requested account or an admin account.
    """
    stm = shared_dpay_instance()
    if stm.rpc is not None:
        stm.rpc.rpcconnect()
    if not unlock_wallet(stm):
        return
    if not account:
        if 'default_account' in stm.config:
            account = stm.config['default_account']
    account = Account(account, dpay_instance=stm)
    if signing_account is not None:
        signing_account = Account(signing_account, dpay_instance=stm)
    c = Conveyor(dpay_instance=stm)
    user_data = c.get_user_data(account, signing_account=signing_account)
    t = PrettyTable(['Key', 'Value'])
    t.align = 'l'
    for key in user_data:
        t.add_row([key, user_data[key]])

    print(t)


@cli.command()
@click.argument('account', nargs=1, required=False)
@click.option('--signing-account', '-s', help='Signing account, when empty account is used.')
def featureflags(account, signing_account):
    """ Get the account's feature flags.

        The request has to be signed by the requested account or an admin account.
    """
    stm = shared_dpay_instance()
    if stm.rpc is not None:
        stm.rpc.rpcconnect()
    if not unlock_wallet(stm):
        return
    if not account:
        if 'default_account' in stm.config:
            account = stm.config['default_account']
    account = Account(account, dpay_instance=stm)
    if signing_account is not None:
        signing_account = Account(signing_account, dpay_instance=stm)
    c = Conveyor(dpay_instance=stm)
    user_data = c.get_feature_flags(account, signing_account=signing_account)
    t = PrettyTable(['Key', 'Value'])
    t.align = 'l'
    for key in user_data:
        t.add_row([key, user_data[key]])

    print(t)


if __name__ == '__main__':
    if getattr(sys, 'frozen', False):
        os.environ['SSL_CERT_FILE'] = os.path.join(sys._MEIPASS, 'lib', 'cert.pem')
        cli(sys.argv[1:])
    else:
        cli()