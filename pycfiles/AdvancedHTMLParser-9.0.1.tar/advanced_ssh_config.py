# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/moul/Git/moul/advanced-ssh-config/venv2.6/lib/python2.6/site-packages/advanced_ssh_config/advanced_ssh_config.py
# Compiled at: 2015-03-23 05:07:58
from __future__ import absolute_import, division, print_function, unicode_literals
import subprocess, os, sys, re, logging
from collections import OrderedDict
from time import sleep
from .config import Config
from .utils import safe_makedirs, value_interpolate, construct_proxy_commands, shellquotemultiple
from . import __version__

class AdvancedSshConfig(object):

    def __init__(self, hostname=None, port=None, configfiles=None, verbose=False, dry_run=False, proxy_type=b'nc', timeout=180, use_python_socket=False, ssh_config_file=b'~/.ssh/config', force=False):
        self.verbose, self.dry_run = verbose, dry_run
        self.hostname, self.port = hostname, port
        self.proxy_type, self.timeout = proxy_type, timeout
        self.user_python_socket = use_python_socket
        self.logger = logging.getLogger(b'assh.AdvancedSshConfig')
        if not configfiles:
            configfiles = [b'/etc/ssh/config.advanced',
             b'~/.ssh/config.advanced']
        self.config = Config(configfiles=configfiles)
        self.ssh_config_file = ssh_config_file
        ssh_config_file_version = self.ssh_config_file_version()
        if ssh_config_file_version != __version__:
            self.logger.error((b'ssh_config file is at version {}, but Advanced SSH config is at version {}').format(ssh_config_file_version, __version__))
        self.force = force

    @property
    def controlpath_dir(self):
        controlpath = self.config.get(b'controlpath', b'default', b'/tmp/advssh_cm/')
        directory = os.path.dirname(os.path.expanduser(controlpath))
        directory = os.path.join(directory, self.hostname)
        directory = os.path.dirname(directory)
        return directory

    def ssh_config_file_version(self, filename=None):
        if not filename:
            filename = self.ssh_config_file
        try:
            filepath = os.path.expanduser(filename)
            f = open(filepath, b'r')
            first_line = f.readline()
            if first_line.startswith(b'# assh version: '):
                return first_line.split(b' ')[(-1)].strip()
            return
        except IOError:
            return

        return

    def get_routing(self):
        routing = {}
        safe_makedirs(self.controlpath_dir)
        section = None
        for sect in self.config.parser.sections():
            if re.match(sect, self.hostname):
                section = sect

        self.logger.debug((b'section "{}" ').format(section))
        path = self.hostname.split(b'/')
        args = {}
        options = {b'p': b'Port', 
           b'l': b'User', 
           b'h': b'Hostname', 
           b'i': b'IdentityFile'}
        default_options = {b'p': None, 
           b'h': path[0]}
        if self.port:
            default_options[b'p'] = self.port
        updated = False
        for key in options:
            cfval = self.config.get(options[key], path[0], default_options.get(key))
            value = value_interpolate(cfval)
            if cfval != value:
                updated = True
                self.config.parser.set(section, options[key], value)
                args[key] = value
            self.logger.debug(b'get (-%-1s) %-12s : %s', key, options[key], value)
            if value:
                args[key] = value

        self.write_sshconfig()
        self.logger.debug(b'Config updated. Need to restart SSH!?')
        self.logger.debug((b'args: {}').format(args))
        routing[b'verbose'] = self.verbose
        routing[b'proxy_type'] = self.proxy_type
        for special_key in ('comment', 'password', 'gateways', 'reallocalcommand'):
            routing[special_key] = self.config.get(special_key, path[(-1)], None)

        if not routing[b'gateways']:
            routing[b'gateways'] = [
             b'direct']
        else:
            routing[b'gateways'] = routing[b'gateways'].split(b' ')
        routing[b'gateway_route'] = path[1:]
        routing[b'hostname'] = args[b'h']
        routing[b'port'] = self.port
        if not routing[b'port'] and b'p' in args:
            routing[b'port'] = int(args[b'p'])
        if not routing[b'port']:
            routing[b'port'] = 22
        routing[b'proxy_commands'] = construct_proxy_commands(routing)
        self.logger.debug(b'Routing:')
        for (key, value) in routing.iteritems():
            self.logger.debug((b'  {0}: {1}').format(key, value))

        return routing

    def connect(self, routing):
        for gateway in routing[b'gateways']:
            if gateway != b'direct':
                routing[b'gateway_route'] += [gateway]
                self.logger.info((b'Using gateway: {}').format(routing[b'gateway_route']))
            else:
                self.logger.info(b'Direct connection')
            cmd = []
            if len(routing[b'gateway_route']):
                cmd += [b'ssh', (b'/').join(routing[b'gateway_route'])]
                cmd.append(shellquotemultiple(routing[b'proxy_commands']))
                self.logger.info((b'cmd: {}').format(cmd))
            else:
                cmd = routing[b'proxy_commands'][0]
            self.logger.info((b'Connection command {}').format(map(str, cmd)))
            if not self.dry_run:
                self.connect_once(routing, cmd)

    def connect_once(self, routing, cmd):
        comment = routing.get(b'comment', None)
        if comment:
            sys.stderr.write((b'{}\n').format((b'\n').join(comment)))
        password = routing.get(b'password', None)
        if password:
            sys.stderr.write((b'password: {}\n').format(password))
        rlc_process = None
        if routing[b'reallocalcommand']:
            self.logger.info((b'Executing localcommand: {}').format(routing[b'reallocalcommand']))
            rlc_cmd = [
             b'/bin/sh', b'-c', routing[b'reallocalcommand']]
            rlc_process = subprocess.Popen(rlc_cmd, stdout=sys.stderr, stderr=sys.stderr)
            sleep(0.1)
        if self.user_python_socket and not len(routing[b'gateway_route']):
            self.logger.info(b'Using Python socket')
            from .network import Socket
            socket = Socket(routing[b'hostname'], routing[b'port'])
            socket.run()
        else:
            self.logger.info(b'Using ProxyCommand')
            proxy_process = subprocess.Popen(map(str, cmd))
            if proxy_process.wait() != 0:
                self.logger.critical(b'There were some errors')
        if rlc_process is not None:
            print(rlc_process)
            rlc_process.kill()
        return

    def write_sshconfig(self, filename=None):
        if not self.force and self.ssh_config_file_version() != __version__:
            self.logger.error(b'Cannot save ssh_config_file, versions differ. Use -f to force')
            return False
        if not filename:
            filename = self.ssh_config_file
        config = self.build_sshconfig()
        if self.dry_run:
            self.logger.error((b'Without dry-run, the file {} should be replaced by the following content').format(filename))
            self.logger.error((b'\n').join(config))
        else:
            fhandle = open(os.path.expanduser(filename), b'w+')
            fhandle.write((b'\n').join(config))
            fhandle.close()

    def build_sshconfig(self):
        config = []
        config.append((b'# assh version: {}').format(__version__))
        config.append(b'')
        hosts = self.prepare_sshconfig()
        od = OrderedDict(sorted(hosts.items()))
        for entry in od.values():
            if entry.host in ('*', 'default'):
                continue
            else:
                config += entry.build_sshconfig()

        if b'default' in hosts:
            config += hosts[b'default'].build_sshconfig()
        return config

    def prepare_sshconfig(self):
        hosts = {}
        for host in self.config.full.values():
            host.resolve()
            hosts[host.host] = host

        return hosts