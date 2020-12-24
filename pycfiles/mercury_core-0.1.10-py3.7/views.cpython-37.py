# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mercury/boot/views.py
# Compiled at: 2019-02-07 12:47:28
# Size of source mod 2**32: 4393 bytes
import logging
from urllib.parse import urlsplit
import pystache
from flask import request, abort, Response
from flask.views import MethodView
from mercury.common.clients.inventory import InventoryClient
from mercury.boot.configuration import get_boot_configuration
log = logging.getLogger(__name__)
configuration = get_boot_configuration()

class BootView(MethodView):
    __doc__ = '\n    Boot method view\n    '

    def get(self):
        """
        Boot request, transmit the discover script
        :return:
        """
        mercury_boot_url = '://'.join(urlsplit(request.base_url)[:2])
        with open('scripts/discovery.ipxe') as (script_file):
            script = pystache.render(script_file.read(), dict(mercury_boot_url=mercury_boot_url))
        return Response(script, content_type='text/plain')


class DiscoverView(MethodView):
    __doc__ = '\n    Discover method view\n    '

    def __init__(self, *args, **kwargs):
        (super(DiscoverView, self).__init__)(*args, **kwargs)
        inventory_url = configuration.inventory.inventory_router
        self.inventory_client = InventoryClient(inventory_url)

    @staticmethod
    def update_cmdline_backend_options():
        backend_url = configuration.agent.backend_url_cmdline
        log_service_url = configuration.agent.log_service_cmdline
        if backend_url or log_service_url:
            configuration['__BACKEND_OPTIONS__'] = '{}{}'.format(' MERCURY_BACKEND={} '.format(backend_url) if backend_url else ' ', 'MERCURY_LOG_SERVICE={} '.format(log_service_url) if log_service_url else '')
        else:
            configuration['__BACKEND_OPTIONS__'] = ' '

    @staticmethod
    def render_agent_script():
        with open('scripts/agent.ipxe') as (fp):
            template = fp.read()
        DiscoverView.update_cmdline_backend_options()
        return (pystache.render)(template, **configuration)

    @staticmethod
    def plain(message):
        return Response(message, content_type='text/plain')

    def get(self, mac_address):
        """ Attempt to relate a device using the provided mac address """
        result = self.inventory_client.query({'interfaces.address': mac_address},
          projection={'boot':1, 
         'mercury_id':1, 
         'dmi':1})
        if result.get('error'):
            abort(500, result)
        message = result['message']
        if not message['total']:
            log.info('New device: {}'.format(mac_address))
            return self.plain(self.render_agent_script())
        if message['total'] > 1:
            log.error('DUPLICATE MAC ADDRESS: {}'.format(mac_address))
            abort(500, 'Duplicate mac addresses in inventory')
        inventory_data = message['items'][0]
        boot_info = inventory_data.get('boot', {})
        if boot_info.get('script'):
            return pystache.render(boot_info['script'], dict(**inventory_data, **configuration))
        boot_state = boot_info.get('state', 'agent')
        if boot_state == 'local':
            log.info('Booting {} from hard drive'.format(inventory_data['mercury_id']))
            return self.plain('#!ipxe\nexit\n')
        if boot_info == 'rescue':
            log.info('Booting {} to rescue mode'.format(inventory_data['mercury_id']))
            return self.plain('Boot rescue iPXE script here')
        log.info('Booting {} to agent'.format(inventory_data['mercury_id']))
        return self.plain(self.render_agent_script())