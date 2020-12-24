# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/etheno/parity.py
# Compiled at: 2019-06-27 23:49:12
# Size of source mod 2**32: 5355 bytes
import atexit, json, os, tempfile
from .client import JSONRPCError
from .genesis import geth_to_parity
from .jsonrpcclient import JSONRPCClient
from .keyfile import create_keyfile_json
from .utils import find_open_port, format_hex_address, int_to_bytes

def make_config(genesis_path, base_path, port, accounts, password_file, **kwargs):
    return '[parity]\npublic_node = false\nno_download = false\nno_consensus = false\nno_persistent_txqueue = false\n\nchain = "{genesis_path}"\nbase_path = "{base_path}"\ndb_path = "{base_path}/chains"\nkeys_path = "{base_path}/keys"\n\n[account]\nunlock = [{account_addresses}]\npassword = ["{password_file}"]\n\n[network]\nport = {port}\nmin_peers = 1\nmax_peers = 1\nid = {chainId}\ndiscovery = false\n\n[rpc]\ndisable = false\nport = {rpc_port}\ninterface = "local"\napis = ["web3", "eth", "pubsub", "net", "parity", "parity_pubsub", "traces", "rpc", "shh", "shh_pubsub"]\nhosts = ["none"]\n\n[websockets]\ndisable = true\n\n[ipc]\ndisable = true\n\n[secretstore]\ndisable = true\n\n[ipfs]\nenable = false\n\n[mining]\nauthor = "{miner}"\nengine_signer = "{miner}"\nforce_sealing = true\nreseal_on_txs = "all"\n#reseal_min_period = 4000\n#reseal_max_period = 60000\n#gas_floor_target = "4700000"\n#gas_cap = "6283184"\n#tx_queue_gas = "off"\n#tx_gas_limit = "6283184"\n#tx_time_limit = 500 #ms\n#remove_solved = false\n#notify_work = ["http://localhost:3001"]\nrefuse_service_transactions = false\n\n[footprint]\ntracing = "auto"\npruning = "auto"\npruning_history = 64\npruning_memory = 32\ncache_size_db = 128\ncache_size_blocks = 8\ncache_size_queue = 40\ncache_size_state = 25\ncache_size = 128 # Overrides above caches with total size\nfast_and_loose = false\ndb_compaction = "ssd"\nfat_db = "auto"\nscale_verifiers = true\nnum_verifiers = 6\n\n[snapshots]\ndisable_periodic = false\n\n[misc]\nlogging = "own_tx=trace"\nlog_file = "{log_path}"\ncolor = true\n'.format(genesis_path=genesis_path,
      base_path=base_path,
      port=(find_open_port(30303)),
      rpc_port=port,
      log_path=(kwargs.get('log_path', '%s/parity.log' % base_path)),
      chainId=(kwargs.get('chainId', 1)),
      miner=(format_hex_address(accounts[(-1)], True)),
      account_addresses=(', '.join(map(lambda s: '"0x%s"' % s, map(format_hex_address, accounts)))),
      password_file=password_file).encode('utf-8')


class ParityClient(JSONRPCClient):

    def __init__(self, genesis, port=8546):
        super().__init__('Parity', genesis, port)
        self._unlock_accounts = True
        self.config = None
        atexit.register(ParityClient.shutdown.__get__(self, ParityClient))

    def etheno_set(self):
        super().etheno_set()
        self.import_account(self.miner_account.private_key)
        self.config = self.logger.make_constant_logged_file(make_config(genesis_path=(self.logger.to_log_path(self.genesis_file)),
          base_path=(self.logger.to_log_path(self.datadir)),
          port=(self.port),
          chainId=(self.genesis['config']['chainId']),
          accounts=(tuple(self.accounts)),
          password_file=(self.logger.to_log_path(self.passwords))),
          prefix='config',
          suffix='.toml')

    def write_passwords(self, outfile):
        outfile.write(b'etheno')

    def write_genesis(self, outfile):
        parity_genesis = geth_to_parity(self.genesis)
        parity_genesis['genesis']['author'] = format_hex_address(self.miner_account.address, True)
        outfile.write(json.dumps(parity_genesis).encode('utf-8'))

    def import_account(self, private_key):
        keyfile = create_keyfile_json(int_to_bytes(private_key), b'etheno')
        keyfile_json = json.dumps(keyfile)
        keysdir = os.path.join(self.datadir, 'keys', 'etheno')
        os.makedirs(keysdir, exist_ok=True)
        output = tempfile.NamedTemporaryFile(prefix='account', suffix='.key', dir=keysdir, delete=False)
        try:
            output.write(keyfile_json.encode('utf-8'))
        finally:
            output.close()

        if self.log_directory is None:
            self._tempfiles.append(output)

    def unlock_account(self, account):
        addr = format_hex_address(account, True)
        self.logger.info('Unlocking Parity account %s...' % addr)
        return self.post({'id':addr, 
         'jsonrpc':'2.0', 
         'method':'personal_unlockAccount', 
         'params':[
          addr, 'etheno', None]})

    def post(self, data, unlock_if_necessary=None):
        if unlock_if_necessary is None:
            unlock_if_necessary = self._unlock_accounts
        try:
            return super().post(data)
        except JSONRPCError as e:
            try:
                if unlock_if_necessary:
                    if 'data' in e.result['error']:
                        if e.result['error']['data'].lower() == 'notunlocked':
                            self.unlock_account(int(data['params'][0]['from'], 16))
                            return self.post(data, unlock_if_necessary=False)
                raise e
            finally:
                e = None
                del e

    def get_start_command(self, unlock_accounts=True):
        return [
         '/usr/bin/env', 'parity', '--config', self.logger.to_log_path(self.config), '--fast-unlock', '--jsonrpc-apis=all']

    def start(self, unlock_accounts=True):
        self._unlock_accounts = unlock_accounts
        super().start(unlock_accounts=unlock_accounts)