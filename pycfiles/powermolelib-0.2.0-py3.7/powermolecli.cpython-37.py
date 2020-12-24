# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/vincent/Projects/PythonPowerMole/powermolecli/powermolecli/powermolecli.py
# Compiled at: 2020-05-13 15:41:04
# Size of source mod 2**32: 9734 bytes
__doc__ = '\nMain code for powermolecli.\n\n.. _Google Python Style Guide:\n   http://google.github.io/styleguide/pyguide.html\n\n'
import argparse, logging.config
from time import sleep
import coloredlogs
from powermolelib import Configuration, StateManager, Heartbeat, start_application, write_ssh_config_file, TransferAgent, Tunnel, ForAssistant, TorAssistant, InteractiveAssistant, FileAssistant, BootstrapAgent
from powermolelib.powermolelibexceptions import InvalidConfigurationFile
from .lib import setup_link
from .powermolecliexceptions import SetupFailed
__author__ = 'Vincent Schouten <inquiry@intoreflection.co>'
__docformat__ = 'google'
__date__ = '12-05-2020'
__copyright__ = 'Copyright 2020, Vincent Schouten'
__credits__ = ['Vincent Schouten']
__license__ = 'MIT'
__maintainer__ = 'Vincent Schouten'
__email__ = '<inquiry@intoreflection.co>'
__status__ = 'Development'
LOGGER_BASENAME = 'minitorcli'
LOGGER = logging.getLogger(LOGGER_BASENAME)
LOCAL_PATH_SSH_CFG = '/tmp/ssh_cfg_minitor'
LOCAL_HEARTBEAT_PORT = 11600
LOCAL_PROXY_PORT = 8080
LOCAL_TRANSFER_PORT = 11700
LOCAL_COMMAND_PORT = 11800
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
        elif configuration.mode == 'INTERACTIVE':
            LOGGER.info('mode INTERACTIVE enabled')
        elif configuration.mode == 'FOR':
            LOGGER.info('mode FOR enabled')
        elif configuration.mode == 'TOR':
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
    if not config:
        return
    try:
        with StateManager() as (state):
            write_ssh_config_file(LOCAL_PATH_SSH_CFG, config.gateways, config.destination)
            transferagent = TransferAgent(LOCAL_PATH_SSH_CFG, config.all_hosts)
            if config.mode == 'FOR':
                tunnel = Tunnel(LOCAL_PATH_SSH_CFG, config.mode, config.all_hosts, config.forwarders_string)
                bootstrapagent = BootstrapAgent(tunnel, MACHINE_DEPLOY_PATH)
                assistant = ForAssistant(tunnel)
            elif config.mode == 'TOR':
                tunnel = Tunnel(LOCAL_PATH_SSH_CFG, config.mode, config.all_hosts)
                bootstrapagent = BootstrapAgent(tunnel, MACHINE_DEPLOY_PATH)
                assistant = TorAssistant(tunnel, '0.0.0.0')
            elif config.mode == 'FILE':
                tunnel = Tunnel(LOCAL_PATH_SSH_CFG, config.mode, config.all_hosts)
                bootstrapagent = BootstrapAgent(tunnel, MACHINE_DEPLOY_PATH)
                assistant = FileAssistant(tunnel, LOCAL_TRANSFER_PORT)
            elif config.mode == 'INTERACTIVE':
                tunnel = Tunnel(LOCAL_PATH_SSH_CFG, config.mode, config.all_hosts)
                bootstrapagent = BootstrapAgent(tunnel, MACHINE_DEPLOY_PATH)
                assistant = InteractiveAssistant(tunnel, LOCAL_COMMAND_PORT)
            setup_link(state, transferagent, tunnel, bootstrapagent, assistant)
            with Heartbeat(LOCAL_HEARTBEAT_PORT) as (heartbeat):
                if config.mode == 'FOR':
                    LOGGER.info('connections on local ports %s will be forwarded', config.forwarders_ports)
                    LOGGER.info('READY')
                elif config.mode == 'TOR':
                    LOGGER.info('local port %s will be listening for web traffic', LOCAL_PROXY_PORT)
                    LOGGER.info('READY')
                elif config.mode == 'INTERACTIVE':
                    LOGGER.warning('the interface does not support shell meta characters ')
                    LOGGER.warning("such as pipe and it's not possible to interact with ")
                    LOGGER.warning('programs that need a response. hit control-c to quit')
                    try:
                        while 1:
                            command = input('enter command: ')
                            response_raw = assistant.exec_command(command)
                            response_str = response_raw.decode('utf-8')
                            response_line = response_str.split('\n')
                            for line in response_line:
                                print('>    %s' % line)

                    except KeyboardInterrupt:
                        raise SystemExit(0)

                elif config.mode == 'FILE':
                    assistant.transfer(metadata_files=(config.files))
                    raise SystemExit(0)
                if config.application:
                    LOGGER.info('starting application...')
                    process = start_application(binary_name=(config.application['binary_name']), binary_location=(config.application['binary_location']))
                    try:
                        while True:
                            sleep(1)

                    except KeyboardInterrupt:
                        process.terminate()
                        raise SystemExit(0)

                while True:
                    if not heartbeat.is_tunnel_intact:
                        LOGGER.error('encrypted tunnel has been broken')
                    sleep(1)

    except SetupFailed as msg:
        try:
            LOGGER.error(msg)
            raise SystemExit(1)
        finally:
            msg = None
            del msg