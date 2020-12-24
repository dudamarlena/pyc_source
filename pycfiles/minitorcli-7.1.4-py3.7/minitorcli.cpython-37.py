# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/vincent/Projects/PythonMinitor/minitorcli/minitorcli/minitorcli.py
# Compiled at: 2020-03-06 15:23:37
# Size of source mod 2**32: 12446 bytes
"""
Main code for minitorcli.

.. _Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html

"""
import argparse, logging.config
from time import sleep
import coloredlogs
from minitorcorelib import Configuration, StateManager, Heartbeat, start_application, BootstrapAgent, PortGenerator, TransferAgentFactory, MachineFactory, TunnelFactory
from minitorcorelib.minitorcorelibexceptions import InvalidConfigurationFile
from .lib import setup_link
from .minitorcliexceptions import SetupFailed
__author__ = 'Vincent Schouten <inquiry@intoreflection.co>'
__docformat__ = 'google'
__date__ = '06-04-2019'
__copyright__ = 'Copyright 2019, Vincent Schouten'
__credits__ = ['Vincent Schouten']
__license__ = 'MIT'
__maintainer__ = 'Vincent Schouten'
__email__ = '<inquiry@intoreflection.co>'
__status__ = 'Development'
LOGGER_BASENAME = 'minitorcli'
LOGGER = logging.getLogger(LOGGER_BASENAME)
LOCAL_HEARTBEAT_PORT = 11600
LOCAL_PROXY_PORT = 8080
LOCAL_TRANSFER_PORT = 11700
LOCAL_COMMAND_PORT = 11800
LOCAL_PROXYCHAINS_BINARY_FILE = '/usr/bin/proxychains4'
LOCAL_PROXYCHAINS_CONFIG_FILE = '/tmp/proxychains.conf'
MACHINE_DEPLOY_PATH = '/tmp/'

def get_arguments():
    """
    Gets us the cli arguments.

    Returns the args as parsed from the argsparser.
    """
    parser = argparse.ArgumentParser(description='minitor - anonymizing internet traffic using private servers (cli)')
    parser.add_argument('--config-file', '-c',
      help='The location of the config file',
      dest='config_file',
      action='store',
      default='')
    parser.add_argument('--log-level', '-L',
      help='Provide the log level. Defaults to info.',
      dest='log_level',
      action='store',
      default='info',
      choices=[
     'debug',
     'info',
     'warning',
     'error',
     'critical'])
    args = parser.parse_args()
    return args


def parse_config_file(config_file_path):
    """Parses the configuration file to a (dictionary) object."""
    try:
        configuration = Configuration(config_file_path)
    except InvalidConfigurationFile:
        return
    else:
        if configuration.mode == 'FILE':
            LOGGER.info('mode FILE enabled')
        else:
            if configuration.mode == 'COMMAND':
                LOGGER.info('mode COMMAND enabled')
            else:
                if configuration.mode == 'FOR':
                    LOGGER.info('mode FOR enabled')
                else:
                    if configuration.mode == 'TOR':
                        LOGGER.info('mode TOR enabled')
        return configuration


def main():
    """
    Main method.

    This method holds what you want to execute when
    the script is run on command line.
    """
    args = get_arguments()
    coloredlogs_format = '%(asctime)s %(name)s[%(process)d] %(levelname)s %(message)s'
    coloredlogs.install(fmt=coloredlogs_format, level=(args.log_level.upper()))
    config = parse_config_file(args.config_file)
    port_generator = PortGenerator()
    try:
        with StateManager() as (state):
            for proxy in config.proxies:
                ports = port_generator.get_next_port_ranges()
                transfer_agent = TransferAgentFactory(local_tunnel_fw_port=(ports['local_tunnel_fw_port']), ip_address_i=(proxy['ip_in']),
                  identity_file=(proxy['identity_file']),
                  machine_deploy_path=MACHINE_DEPLOY_PATH,
                  local_proxychains_config_file=LOCAL_PROXYCHAINS_CONFIG_FILE,
                  local_proxychains_binary_path=LOCAL_PROXYCHAINS_BINARY_FILE)
                tunnel = TunnelFactory(local_tunnel_fw_port=(ports['local_tunnel_fw_port']), local_agent_port=(ports['local_agent_port']),
                  count_connection=(ports['count_connection']),
                  ip_address_i=(proxy['ip_in']),
                  identity_file=(proxy['identity_file']),
                  local_proxychains_config_file=LOCAL_PROXYCHAINS_CONFIG_FILE,
                  mode=None)
                bootstrap_agent = BootstrapAgent(tunnel=tunnel, deploy_path=MACHINE_DEPLOY_PATH)
                machine = MachineFactory(tunnel=tunnel, hostname=(proxy['hostname']),
                  ip_address_e=(proxy['ip_out']))
                setup_link(state, transfer_agent, tunnel, bootstrap_agent, machine)

            ports = port_generator.get_next_port_ranges()
            transfer_agent = TransferAgentFactory(local_tunnel_fw_port=(ports['local_tunnel_fw_port']), ip_address_i=(config.destination['ip_in']),
              identity_file=(config.destination['identity_file']),
              machine_deploy_path=MACHINE_DEPLOY_PATH,
              local_proxychains_config_file=LOCAL_PROXYCHAINS_CONFIG_FILE,
              local_proxychains_binary_path=LOCAL_PROXYCHAINS_BINARY_FILE)
            tunnel = TunnelFactory(local_tunnel_fw_port=(ports['local_tunnel_fw_port']), local_agent_port=(ports['local_agent_port']),
              count_connection=(ports['count_connection']),
              ip_address_i=(config.destination['ip_in']),
              identity_file=(config.destination['identity_file']),
              local_proxychains_config_file=LOCAL_PROXYCHAINS_CONFIG_FILE,
              mode=(config.mode),
              local_heartbeat_port=LOCAL_HEARTBEAT_PORT,
              local_browser_port=LOCAL_PROXY_PORT,
              local_transfer_port=LOCAL_TRANSFER_PORT,
              local_command_port=LOCAL_COMMAND_PORT,
              local_forward_connections=(config.forwarders_string))
            bootstrap_agent = BootstrapAgent(tunnel=tunnel, deploy_path=MACHINE_DEPLOY_PATH)
            machine = MachineFactory(tunnel=tunnel, hostname=(config.destination['hostname']),
              mode=(config.mode),
              ip_address_e=(config.destination['ip_out']),
              transfer_port=LOCAL_TRANSFER_PORT,
              command_port=LOCAL_COMMAND_PORT)
            setup_link(state, transfer_agent, tunnel, bootstrap_agent, machine)
            if config.mode == 'FOR':
                LOGGER.info('connections on local ports %s will be forwarded', config.forwarders_ports)
            else:
                if config.mode == 'TOR':
                    LOGGER.info('local port %s will be listening for web traffic', LOCAL_PROXY_PORT)
                else:
                    if config.mode == 'COMMAND':
                        shell_machine = machine
                    else:
                        if config.mode == 'FILE':
                            file_machine = machine
            with Heartbeat(LOCAL_HEARTBEAT_PORT) as (heartbeat):
                LOGGER.info('encrypted tunnel established')
                if config.application:
                    LOGGER.info('starting application...')
                    process = start_application(binary_name=(config.application['binary_name']), binary_location=(config.application['binary_location']))
                    try:
                        while True:
                            sleep(1)

                    except KeyboardInterrupt:
                        process.terminate()

                else:
                    if config.mode == 'COMMAND':
                        LOGGER.warning('the interface does not support shell meta characters ')
                        LOGGER.warning("such as pipe and it's not possible to interact with ")
                        LOGGER.warning('programs that need a response. hit control-c to quit')
                        try:
                            while 1:
                                command = input('enter command: ')
                                response_raw = shell_machine.exec_command(command)
                                response_str = response_raw.decode('utf-8')
                                response_line = response_str.split('\n')
                                for line in response_line:
                                    print('>    %s' % line)

                        except KeyboardInterrupt:
                            raise SystemExit(0)

                    else:
                        if config.mode == 'FILE':
                            file_machine.transfer(metadata_files=(config.files))
                        else:
                            while True:
                                if not heartbeat.is_tunnel_intact:
                                    LOGGER.error('encrypted tunnel has been broken')
                                else:
                                    sleep(1)

    except SetupFailed as msg:
        try:
            LOGGER.error(msg)
            raise SystemExit(1)
        finally:
            msg = None
            del msg