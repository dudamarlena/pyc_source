# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mercury_agent/configuration.py
# Compiled at: 2019-04-01 19:51:35
# Size of source mod 2**32: 4709 bytes
import logging
from mercury.common.configuration import MercuryConfiguration
log = logging.getLogger(__name__)
AGENT_CONFIG_FILE = 'mercury-agent.yaml'
__configuration = {}

def parse_options():
    configuration = MercuryConfiguration('mercury-agent',
      AGENT_CONFIG_FILE,
      description='The Mercury Agent')
    (
     configuration.add_option('agent.bind_address', help_string='The interface and port for socket binding',
       default='tcp://127.0.0.1:9003'),)
    configuration.add_option('agent.pong_bind_address', help_string='Interface and port for the pongservice',
      default='tcp://127.0.0.1:9004')
    configuration.add_option('agent.dhcp_ip_source', help_string='The method of determining dhcp_ip',
      default='simple',
      one_of=[
     'simple', 'udhcpd', 'routing_table'])
    configuration.add_option('agent.remote.backend_url', proc_cmdline_argument='MERCURY_BACKEND',
      help_string='The ZeroMQ URL of the backend service',
      required=True)
    configuration.add_option('agent.remote.log_service_url', proc_cmdline_argument='MERCURY_LOG_SERVICE',
      help_string='Optional logging service zURL',
      default=None)
    configuration.add_option('agent.hardware.raid.storcli_path', cli_argument='--storcli_path',
      env_variable='STORCLI_PATH',
      default='storcli64')
    configuration.add_option('agent.hardware.raid.hpssacli_path', cli_argument='--hpssacli_path',
      env_variable='HPSSACLI_PATH',
      default='hpssacli')
    configuration.add_option('agent.local_ip', cli_argument='--local-ip',
      env_variable='MERCURY_AGENT_ADDRESS',
      help_string='The address which will be advertisedto the backend for communication withthis agent')
    configuration.add_option('agent.pong_log_level', cli_argument='--pong-log-level',
      default='ERROR',
      help_string='The pong process log level')
    configuration.add_option('agent.hardware.obm.racadm_path', cli_argument='--racadm-path',
      env_variable='RACADM_PATH',
      help_string='The location of the racadm binary',
      default='racadm')
    configuration.add_option('agent.hardware.megacli_bin', help_string='megacli binary',
      default='/usr/local/sbin/megacli')
    configuration.add_option('agent.hardware.mce_threshold', help_string='The maximum number of corrected machine check exceptions which can occur before an error is raised',
      default=20,
      special_type=int)
    configuration.add_option('agent.hardware.oem.hp.hpasmcli_path', help_string='The path of the hpasmcli binary',
      env_variable='HPASMCLI_PATH',
      default='hpasmcli')
    return configuration.scan_options()


def get_configuration():
    global __configuration
    if not __configuration:
        __configuration = parse_options()
    return __configuration