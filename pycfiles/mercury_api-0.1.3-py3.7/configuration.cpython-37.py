# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mercury_api/configuration.py
# Compiled at: 2018-09-27 14:18:55
# Size of source mod 2**32: 2615 bytes
from mercury.common.configuration import MercuryConfiguration
API_CONFIG_FILE = 'mercury-api.yaml'

def options(configuration):
    """ A single place to add program options """
    configuration.add_option('api.host',
      default='0.0.0.0',
      help_string='The host address to bind to')
    configuration.add_option('api.port',
      default=9005,
      special_type=int,
      help_string='The host address to bind to')
    configuration.add_option('api.inventory.inventory_router',
      '--api-inventory-router',
      default='tcp://127.0.0.1:9000',
      help_string='The inventory router url')
    configuration.add_option('api.rpc.rpc_router',
      '--api-rpc-router',
      default='tcp://127.0.0.1:9001',
      help_string='The RPC router url')
    configuration.add_option('api.paging.limit',
      default=250,
      special_type=int,
      help_string='The number of return results')
    configuration.add_option('api.paging.offset_id',
      default=None,
      help_string='The paging offset id')
    configuration.add_option('api.paging.sort_direction',
      default=1,
      special_type=int,
      help_string='The paging sort direction, default is 1 (ascending)')
    configuration.add_option('api.logging.log_file',
      default='mercury-api.log',
      help_string='The log file path')
    configuration.add_option('api.logging.level',
      default='DEBUG', help_string='The app log level')
    configuration.add_option('api.logging.console_out',
      default=True,
      special_type=bool,
      help_string='Stream log output to the console')


def get_api_configuration():
    api_configuration = MercuryConfiguration('mercury-api', API_CONFIG_FILE)
    options(api_configuration)
    return api_configuration.scan_options()