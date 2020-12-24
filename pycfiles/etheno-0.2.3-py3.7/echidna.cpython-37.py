# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/etheno/echidna.py
# Compiled at: 2019-06-27 23:49:12
# Size of source mod 2**32: 7647 bytes
import os, subprocess, tempfile
from .ascii_escapes import decode
from .etheno import EthenoPlugin
from .utils import ConstantTemporaryFile, format_hex_address
ECHIDNA_CONTRACT = b'pragma solidity ^0.4.24;\ncontract C {\n  mapping(int => int) public s;\n  int public stored = 1337;\n  function save(int key, int value) public {\n    s[key] = value;\n  }\n  function remove(int key) public {\n    delete s[key];\n  }\n  function setStored(int value) public {\n    stored = value;\n  }\n  function f(uint, int, int[]) public { }\n  function g(bool, int, address[]) public { }\n  function echidna_() public returns (bool) {\n    return true;\n  }\n}\n'
ECHIDNA_CONFIG = b'outputRawTxs: true\nquiet: true\ndashboard: false\ngasLimit: 0xfffff\n'

def echidna_exists():
    return subprocess.call(['/usr/bin/env', 'echidna-test', '--help'], stdout=(subprocess.DEVNULL)) == 0


def stack_exists():
    return subprocess.call(['/usr/bin/env', 'stack', '--help'], stdout=(subprocess.DEVNULL)) == 0


def git_exists():
    return subprocess.call(['/usr/bin/env', 'git', '--version'], stdout=(subprocess.DEVNULL)) == 0


def install_echidna(allow_reinstall=False):
    if not allow_reinstall:
        if echidna_exists():
            return
    if not git_exists():
        raise Exception('Git must be installed in order to install Echidna')
    else:
        if not stack_exists():
            raise Exception('Haskell Stack must be installed in order to install Echidna. On OS X you can easily install it using Homebrew: `brew install haskell-stack`')
    with tempfile.TemporaryDirectory() as (path):
        subprocess.check_call(['/usr/bin/env', 'git', 'clone', 'https://github.com/trailofbits/echidna.git', path])
        subprocess.call(['/usr/bin/env', 'git', 'checkout', 'dev-etheno'], cwd=path)
        subprocess.check_call(['/usr/bin/env', 'stack', 'install'], cwd=path)


def decode_binary_json(text):
    orig = text
    text = decode(text).strip()
    if not text.startswith(b'['):
        return
    offset = len(orig) - len(text)
    orig = text
    text = text[1:].strip()
    offset += len(orig) - len(text)
    if text[:1] != b'"':
        raise ValueError("Malformed JSON list! Expected '%s' but instead got '%s' at offset %d" % ('"', text[0:1].decode(), offset))
    text = text[1:]
    offset += 1
    if text[-1:] != b']':
        raise ValueError("Malformed JSON list! Expected '%s' but instead got '%s' at offset %d" % (']', chr(text[(-1)]), offset + len(text) - 1))
    text = text[:-1].strip()
    if text[-1:] != b'"':
        raise ValueError("Malformed JSON list! Expected '%s' but instead got '%s' at offset %d" % ('"', chr(text[(-1)]), offset + len(text) - 1))
    return text[:-1]


class EchidnaPlugin(EthenoPlugin):

    def __init__(self, transaction_limit=None, contract_source=None):
        self._transaction = 0
        self.limit = transaction_limit
        self.contract_address = None
        if contract_source is None:
            self.contract_source = ECHIDNA_CONTRACT
        else:
            self.contract_source = contract_source
        self.contract_bytecode = None

    def added(self):
        self.contract_bytecode = self.compile(self.contract_source)

    def run(self):
        if not self.etheno.accounts:
            self.logger.info('Etheno does not know about any accounts, so Echidna has nothing to do!')
            self._shutdown()
            return
        if self.contract_source is None:
            self.logger.error('Error compiling source contract')
            self._shutdown()
        self.logger.info('Deploying Echidna test contract...')
        self.contract_address = format_hex_address(self.etheno.deploy_contract(self.etheno.accounts[0], self.contract_bytecode), True)
        if self.contract_address is None:
            self.logger.error('Unable to deploy Echidna test contract!')
            self._shutdown()
            return
        self.logger.info('Deployed Echidna test contract to %s' % self.contract_address)
        config = self.logger.make_constant_logged_file(ECHIDNA_CONFIG, prefix='echidna', suffix='.yaml')
        sol = self.logger.make_constant_logged_file((self.contract_source), prefix='echidna', suffix='.sol')
        echidna_args = ['/usr/bin/env', 'echidna-test', self.logger.to_log_path(sol), '--config', self.logger.to_log_path(config)]
        run_script = self.logger.make_constant_logged_file((' '.join(echidna_args)), prefix='run_echidna', suffix='.sh')
        os.chmod(run_script, 493)
        echidna = subprocess.Popen(echidna_args, stderr=(subprocess.DEVNULL), stdout=(subprocess.PIPE), bufsize=1, universal_newlines=True, cwd=(self.log_directory))
        while not self.limit is None:
            if self._transaction < self.limit:
                line = echidna.stdout.readline()
                if line != b'':
                    txn = decode_binary_json(line)
                    if txn is None:
                        continue
                    self.emit_transaction(txn)
            else:
                break

        self._shutdown()

    def _shutdown(self):
        etheno = self.etheno
        self.etheno.remove_plugin(self)
        etheno.shutdown()

    def compile(self, solidity):
        with ConstantTemporaryFile(solidity, prefix='echidna', suffix='.sol') as (contract):
            solc = subprocess.Popen(['/usr/bin/env', 'solc', '--bin', contract], stderr=(subprocess.PIPE), stdout=(subprocess.PIPE), bufsize=1, universal_newlines=True)
            errors = solc.stderr.read().strip()
            output = solc.stdout.read()
            if solc.wait() != 0:
                self.logger.error(f"{errors}\n{output}")
                return
            if errors:
                if solidity == ECHIDNA_CONTRACT:
                    self.logger.debug(errors)
                else:
                    self.logger.warning(errors)
            binary_key = 'Binary:'
            offset = output.find(binary_key)
            if offset < 0:
                self.logger.error(f"Could not parse `solc` output:\n{output}")
                return
            code = hex(int(output[offset + len(binary_key):].strip(), 16))
            self.logger.debug(f"Compiled contract code: {code}")
            return code

    def emit_transaction(self, txn):
        self._transaction += 1
        transaction = {'id':1, 
         'jsonrpc':'2.0', 
         'method':'eth_sendTransaction', 
         'params':[
          {'from':format_hex_address(self.etheno.accounts[0], True), 
           'to':self.contract_address, 
           'gasPrice':'0x%x' % self.etheno.master_client.get_gas_price(), 
           'value':'0x0', 
           'data':'0x%s' % txn.hex()}]}
        gas = self.etheno.estimate_gas(transaction)
        if gas is None:
            self.logger.warning(f"All clients were unable to estimate the gas cost for transaction {self._transaction}. This typically means that Echidna emitted a transaction that is too large.")
            return
        gas = '0x%x' % gas
        self.logger.info(f"Estimated gas cost for Transaction {self._transaction}: {gas}")
        transaction['params'][0]['gas'] = gas
        self.logger.info('Emitting Transaction %d' % self._transaction)
        self.etheno.post(transaction)


if __name__ == '__main__':
    install_echidna(allow_reinstall=True)