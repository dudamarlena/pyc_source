# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mercury_agent/agent.py
# Compiled at: 2019-04-01 19:51:35
# Size of source mod 2**32: 5233 bytes
import logging, time
from mercury.common.clients.rpc.backend import BackEndClient
from mercury.common.exceptions import MercuryCritical, MercuryGeneralException, MercuryConfigurationError
from mercury_agent.capabilities import runtime_capabilities
from mercury_agent.configuration import get_configuration
from mercury_agent.pong import spawn_pong_process
from mercury_agent.register import get_dhcp_ip, register
from mercury_agent.remote_logging import MercuryLogHandler
from mercury_agent.rpc import AgentService
from mercury_agent.inspector import inspect
from mercury_agent.inspector.inspectors.async_inspectors.lldp import LLDPInspector
log = logging.getLogger(__name__)
RETRY_SECONDS = 15

class Agent(object):

    def __init__(self, configuration, logger):
        """

        :param configuration:
        """
        self.configuration = configuration
        self.agent_bind_address = configuration.agent.bind_address
        self.pong_bind_address = configuration.agent.pong_bind_address
        self.rpc_backend_url = self.configuration.agent.remote.backend_url
        self.log_handler = logger
        if not self.rpc_backend_url:
            raise MercuryCritical('Missing rpc backend in local configuration')
        self.backend = BackEndClient((self.rpc_backend_url), linger=0,
          response_timeout=10,
          rcv_retry=3)

    def run(self, dhcp_ip_method='simple'):
        log.debug('Agent: %s, Pong: %s' % (self.agent_bind_address,
         self.pong_bind_address))
        log.info('Running inspectors')
        device_info = inspect.inspect()
        log.info('Registering device inventory for MercuryID {}'.format(device_info['mercury_id']))
        log.info('Starting pong service')
        spawn_pong_process(self.pong_bind_address)
        log.info('Registering device')
        local_ip = get_dhcp_ip(device_info, method=dhcp_ip_method)
        local_ipv6 = None
        while True:
            result = register(self.backend, device_info, local_ip, local_ipv6, runtime_capabilities)
            if result.get('error'):
                log.info('Registration was not successful, retrying...')
                time.sleep(RETRY_SECONDS)
            else:
                log.info('Device has been registered successfully')
                break

        if self.log_handler is not None:
            log.info('Injecting MercuryID for remote logging')
            self.log_handler.set_mercury_id(device_info['mercury_id'])
            log.info('Injection completed')
        try:
            LLDPInspector(device_info, self.backend).inspect()
        except MercuryGeneralException as mge:
            log.error('Caught recoverable exception running async inspector: {}'.format(mge))

        log.info('Starting agent rpc service: %s' % self.agent_bind_address)
        agent_service = AgentService(self.agent_bind_address, self.rpc_backend_url)
        agent_service.start()


def setup_logging(configuration):
    logging.basicConfig(level=(configuration.logging.level), format=(configuration.logging.format))
    mercury_logger = logging.getLogger('mercury_agent')
    mercury_logger.info('Starting Agent')
    logging.getLogger('mercury_agent.pong').setLevel(configuration.agent.pong_log_level)
    logging.getLogger('hpssa._cli').setLevel(logging.ERROR)
    log_service_url = configuration.agent.remote.log_service_url
    if log_service_url:
        mh = MercuryLogHandler(configuration.agent.remote.log_service_url)
        mercury_logger.addHandler(mh)
        return mh
    else:
        return


def main():
    try:
        configuration = get_configuration()
    except MercuryConfigurationError as mce:
        import sys
        print(('Error in configuration: {}'.format(mce)), file=(sys.stderr))
        sys.exit(1)

    mercury_handler = setup_logging(configuration)
    agent = Agent(configuration, mercury_handler)
    agent.run(configuration.agent.dhcp_ip_source)


if __name__ == '__main__':
    main()