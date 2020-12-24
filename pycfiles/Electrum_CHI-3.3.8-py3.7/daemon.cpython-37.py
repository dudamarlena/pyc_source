# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/electrum_chi/electrum/daemon.py
# Compiled at: 2019-08-24 06:36:07
# Size of source mod 2**32: 14655 bytes
import asyncio, ast, os, time, traceback, select, sys, threading
from typing import Dict, Optional, Tuple
import jsonrpclib
from .jsonrpc import VerifyingJSONRPCServer
from .version import ELECTRUM_VERSION
from .network import Network
from .util import json_decode, DaemonThread, to_string, create_and_start_event_loop, profiler, standardize_path
from .wallet import Wallet, Abstract_Wallet
from .storage import WalletStorage
from .commands import known_commands, Commands
from .simple_config import SimpleConfig
from .exchange_rate import FxThread
from .plugin import run_hook
from .logging import get_logger
from . import compatibility_rpc
_logger = get_logger(__name__)

def get_lockfile(config: SimpleConfig):
    return os.path.join(config.path, 'daemon')


def remove_lockfile(lockfile):
    os.unlink(lockfile)


def get_fd_or_server(config: SimpleConfig):
    """Tries to create the lockfile, using O_EXCL to
    prevent races.  If it succeeds it returns the FD.
    Otherwise try and connect to the server specified in the lockfile.
    If this succeeds, the server is returned.  Otherwise remove the
    lockfile and try again."""
    lockfile = get_lockfile(config)
    while True:
        try:
            return (
             os.open(lockfile, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 420), None)
        except OSError:
            pass

        server = get_server(config)
        if server is not None:
            return (
             None, server)
        remove_lockfile(lockfile)


def get_server(config: SimpleConfig) -> Optional[jsonrpclib.Server]:
    lockfile = get_lockfile(config)
    while True:
        create_time = None
        try:
            with open(lockfile) as (f):
                (host, port), create_time = ast.literal_eval(f.read())
                rpc_user, rpc_password = get_rpc_credentials(config)
                if rpc_password == '':
                    server_url = 'http://%s:%d' % (host, port)
                else:
                    server_url = 'http://%s:%s@%s:%d' % (
                     rpc_user, rpc_password, host, port)
                server = jsonrpclib.Server(server_url)
            server.ping()
            return server
        except Exception as e:
            try:
                _logger.info(f"failed to connect to JSON-RPC server: {e}")
            finally:
                e = None
                del e

        if create_time:
            if create_time < time.time() - 1.0:
                return
        time.sleep(1.0)


def get_rpc_credentials(config: SimpleConfig) -> Tuple[(str, str)]:
    rpc_user = config.get('rpcuser', None)
    rpc_password = config.get('rpcpassword', None)
    if rpc_user is None or rpc_password is None:
        rpc_user = 'user'
        import ecdsa, base64
        bits = 128
        nbytes = bits // 8 + (bits % 8 > 0)
        pw_int = ecdsa.util.randrange(pow(2, bits))
        pw_b64 = base64.b64encode(pw_int.to_bytes(nbytes, 'big'), b'-_')
        rpc_password = to_string(pw_b64, 'ascii')
        config.set_key('rpcuser', rpc_user)
        config.set_key('rpcpassword', rpc_password, save=True)
    else:
        if rpc_password == '':
            _logger.warning('RPC authentication is disabled.')
    return (
     rpc_user, rpc_password)


class Daemon(DaemonThread):

    @profiler
    def __init__(self, config: SimpleConfig, fd=None, *, listen_jsonrpc=True):
        DaemonThread.__init__(self)
        self.config = config
        if fd is None:
            if listen_jsonrpc:
                fd, server = get_fd_or_server(config)
                if fd is None:
                    raise Exception('failed to lock daemon; already running?')
        else:
            self.asyncio_loop, self._stop_loop, self._loop_thread = create_and_start_event_loop()
            if config.get('offline'):
                self.network = None
            else:
                self.network = Network(config)
            self.network._loop_thread = self._loop_thread
        self.fx = FxThread(config, self.network)
        if self.network:
            self.network.start([self.fx.run])
        self.gui = None
        self.wallets = {}
        self.server = None
        self.compat_server = None
        if listen_jsonrpc:
            self.init_server(config, fd)
        self.start()

    def init_server(self, config: SimpleConfig, fd):
        host = config.get('rpchost', '127.0.0.1')
        port = config.get('rpcport', 0)
        rpc_user, rpc_password = get_rpc_credentials(config)
        try:
            server = VerifyingJSONRPCServer((host, port), logRequests=False, rpc_user=rpc_user,
              rpc_password=rpc_password)
        except Exception as e:
            try:
                self.logger.error(f"cannot initialize RPC server on host {host}: {repr(e)}")
                self.server = None
                os.close(fd)
                return
            finally:
                e = None
                del e

        os.write(fd, bytes(repr((server.socket.getsockname(), time.time())), 'utf8'))
        os.close(fd)
        self.server = server
        server.register_function(self.ping, 'ping')
        server.register_function(self.run_gui, 'gui')
        server.register_function(self.run_daemon, 'daemon')
        self.cmd_runner = Commands(self.config, None, self.network)
        for cmdname in known_commands:
            server.register_function(getattr(self.cmd_runner, cmdname), cmdname)

        server.register_function(self.run_cmdline, 'run_cmdline')
        compat_port = config.get('rpcportcompat', 0)
        if compat_port != 0:
            self.compat_server = compatibility_rpc.Server((host, compat_port), logRequests=False,
              rpc_user=rpc_user,
              rpc_password=rpc_password,
              cmd_runner=(self.cmd_runner))

    def ping(self):
        return True

    def run_daemon(self, config_options):
        asyncio.set_event_loop(self.asyncio_loop)
        config = SimpleConfig(config_options)
        sub = config.get('subcommand')
        assert sub in (None, 'start', 'stop', 'status', 'load_wallet', 'close_wallet')
        if sub in (None, 'start'):
            response = 'Daemon already running'
        else:
            if sub == 'load_wallet':
                path = config.get_wallet_path()
                wallet = self.load_wallet(path, config.get('password'))
                if wallet is not None:
                    self.cmd_runner.wallet = wallet
                    run_hook('load_wallet', wallet, None)
                response = wallet is not None
            else:
                if sub == 'close_wallet':
                    path = config.get_wallet_path()
                    path = standardize_path(path)
                    if path in self.wallets:
                        self.stop_wallet(path)
                        response = True
                    else:
                        response = False
                else:
                    if sub == 'status':
                        if self.network:
                            net_params = self.network.get_parameters()
                            current_wallet = self.cmd_runner.wallet
                            current_wallet_path = current_wallet.storage.path if current_wallet else None
                            response = {'path':self.network.config.path, 
                             'server':net_params.host, 
                             'blockchain_height':self.network.get_local_height(), 
                             'server_height':self.network.get_server_height(), 
                             'spv_nodes':len(self.network.get_interfaces()), 
                             'connected':self.network.is_connected(), 
                             'auto_connect':net_params.auto_connect, 
                             'version':ELECTRUM_VERSION, 
                             'wallets':{k:w.is_up_to_date() for k, w in self.wallets.items()}, 
                             'current_wallet':current_wallet_path, 
                             'fee_per_kb':self.config.fee_per_kb()}
                        else:
                            response = 'Daemon offline'
                    else:
                        if sub == 'stop':
                            self.stop()
                            response = 'Daemon stopped'
                        return response

    def run_gui(self, config_options):
        config = SimpleConfig(config_options)
        if self.gui:
            if hasattr(self.gui, 'new_window'):
                config.open_last_wallet()
                path = config.get_wallet_path()
                self.gui.new_window(path, config.get('url'))
                response = 'ok'
            else:
                response = 'error: current GUI does not support multiple windows'
        else:
            response = 'Error: Electrum-CHI is running in daemon mode. Please stop the daemon first.'
        return response

    def load_wallet(self, path, password) -> Optional[Abstract_Wallet]:
        path = standardize_path(path)
        if path in self.wallets:
            wallet = self.wallets[path]
            return wallet
        else:
            storage = WalletStorage(path, manual_upgrades=True)
            return storage.file_exists() or None
        if storage.is_encrypted():
            if not password:
                return
            storage.decrypt(password)
        if storage.requires_split():
            return
        if storage.requires_upgrade():
            return
        if storage.get_action():
            return
        wallet = Wallet(storage)
        wallet.start_network(self.network)
        self.wallets[path] = wallet
        return wallet

    def add_wallet(self, wallet: Abstract_Wallet):
        path = wallet.storage.path
        path = standardize_path(path)
        self.wallets[path] = wallet

    def get_wallet(self, path):
        path = standardize_path(path)
        return self.wallets.get(path)

    def delete_wallet(self, path):
        self.stop_wallet(path)
        if os.path.exists(path):
            os.unlink(path)
            return True
        return False

    def stop_wallet(self, path):
        path = standardize_path(path)
        wallet = self.wallets.pop(path, None)
        if not wallet:
            return
        wallet.stop_threads()

    def run_cmdline(self, config_options):
        asyncio.set_event_loop(self.asyncio_loop)
        password = config_options.get('password')
        new_password = config_options.get('new_password')
        config = SimpleConfig(config_options)
        config.fee_estimates = self.network.config.fee_estimates.copy()
        config.mempool_fees = self.network.config.mempool_fees.copy()
        cmdname = config.get('cmd')
        cmd = known_commands[cmdname]
        if cmd.requires_wallet:
            path = config.get_wallet_path()
            path = standardize_path(path)
            wallet = self.wallets.get(path)
            if wallet is None:
                return {'error': 'Wallet "%s" is not loaded. Use "electrum-chi daemon load_wallet"' % os.path.basename(path)}
        else:
            wallet = None
        args = map(lambda x: config.get(x), cmd.params)
        args = [json_decode(i) for i in args]
        kwargs = {}
        for x in cmd.options:
            kwargs[x] = config_options.get(x) if x in ('password', 'new_password') else config.get(x)

        cmd_runner = Commands(config, wallet, self.network)
        func = getattr(cmd_runner, cmd.name)
        try:
            result = func(*args, **kwargs)
        except TypeError as e:
            try:
                raise Exception('Wrapping TypeError to prevent JSONRPC-Pelix from hiding traceback') from e
            finally:
                e = None
                del e

        return result

    def run(self):
        while self.is_running():
            servers = []
            if self.server is not None:
                servers.append(self.server)
            if self.compat_server is not None:
                servers.append(self.compat_server)
            if len(servers) == 0:
                time.sleep(0.1)
            else:
                timeout = 0.1
                ready, _, _ = select.select(servers, [], [], timeout)
                if len(ready) > 0:
                    ready[0].handle_request()

        for k, wallet in self.wallets.items():
            wallet.stop_threads()

        if self.network:
            self.logger.info('shutting down network')
            self.network.stop()
        self.asyncio_loop.call_soon_threadsafe(self._stop_loop.set_result, 1)
        self._loop_thread.join(timeout=1)
        self.on_stop()

    def stop(self):
        if self.gui:
            self.gui.stop()
        self.logger.info('stopping, removing lockfile')
        remove_lockfile(get_lockfile(self.config))
        DaemonThread.stop(self)

    def init_gui(self, config, plugins):
        threading.current_thread().setName('GUI')
        gui_name = config.get('gui', 'qt')
        if gui_name in ('lite', 'classic'):
            gui_name = 'qt'
        gui = __import__(('electrum.gui.' + gui_name), fromlist=['electrum'])
        self.gui = gui.ElectrumGui(config, self, plugins)
        try:
            self.gui.main()
        except BaseException as e:
            try:
                self.logger.exception('')
            finally:
                e = None
                del e