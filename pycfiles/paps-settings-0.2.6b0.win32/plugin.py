# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: \data\p\python\paps-settings\env\Lib\site-packages\paps_settings\plugin.py
# Compiled at: 2016-04-01 20:05:30
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
__author__ = b'd01'
__email__ = b'jungflor@gmail.com'
__copyright__ = b'Copyright (C) 2015-16, Florian JUNG'
__license__ = b'MIT'
__version__ = b'0.1.1'
__date__ = b'2016-04-02'
import logging
from pprint import pformat
import threading, time, base64
from twisted.logger import STDLibLogObserver, globalLogBeginner
from twisted.internet import reactor
from twisted.internet.error import ReactorAlreadyRunning
from autobahn.twisted.websocket import WebSocketClientFactory, WebSocketClientProtocol
from flotils.loadable import loadJSON, saveJSON
from paps.crowd import Plugin, PluginException
from .settable_plugin import SettablePlugin
logger = logging.getLogger(__name__)

class PluginClientProtocol(WebSocketClientProtocol):
    """ Websocket linking the plugin to the webserver """

    def onConnect(self, request):
        logger.debug((b'Server connecting: {}').format(request.peer))

    def onOpen(self):
        logger.debug(b'WebSocket connection open.')
        self._webClient._plugin_protocol = self

    def onMessage(self, payload, isBinary):
        if not isBinary:
            payload = loadJSON(payload.decode(b'utf8'))
            try:
                res = self._webClient.handle_msg(payload)
            except:
                logger.exception((b'Failed to handle {}').format(payload))
                return

            if res:
                self.sendMessage(saveJSON(res, pretty=False).encode(b'utf8'))
        else:
            logger.warning(b'Unsupported: Received binary payload')

    def onClose(self, wasClean, code, reason):
        logger.debug((b'WebSocket connection closed: {}').format(reason))
        self._webClient._plugin_protocol = None
        return


class SettingsPlugin(Plugin):
    """ Class handling plugin to webserver transmission """

    def __init__(self, settings=None):
        if settings is None:
            settings = {}
        super(SettingsPlugin, self).__init__(settings)
        self._host = settings.get(b'host', b'localhost')
        self._port = settings.get(b'port', 5000)
        self._ws_path = settings.get(b'ws_path', b'')
        self._is_debug = settings.get(b'use_debug', False)
        self._factory = None
        self.plugins = {}
        self.plugin_lock = threading.Lock()
        self.people = {}
        self.people_lock = threading.Lock()
        self._plugin_protocol = None
        return

    def on_person_new(self, people):
        with self.people_lock:
            for person in people:
                self.people[person.id] = person

    def on_person_leave(self, people):
        with self.people_lock:
            for person in people:
                del self.people[person.id]

    def on_person_update(self, people):
        with self.people_lock:
            for person in people:
                self.people[person.id] = person

    def _plugin_get(self, plugin_name):
        """
        Find plugins in controller

        :param plugin_name: Name of the plugin to find
        :type plugin_name: str | None
        :return: Plugin or None and error message
        :rtype: (settable_plugin.SettablePlugin | None, str)
        """
        if not plugin_name:
            return (None, 'Plugin name not set')
        else:
            for plugin in self.controller.plugins:
                if not isinstance(plugin, SettablePlugin):
                    continue
                if plugin.name == plugin_name:
                    return (plugin, b'')

            return (
             None, (b"Settable plugin '{}' not found").format(plugin_name))

    def handle_msg(self, payload):
        """
        Handle message for network plugin protocol

        :param payload: Received message
        :type payload: dict
        :return: Response to send (if set)
        :rtype: None | dict
        """
        self.debug((b'\n{}').format(pformat(payload)))
        msg = payload[b'msg']
        res = {b'msg': msg, 
           b'error': b''}
        if msg == b'plugin_list':
            res[b'plugin_names'] = []
            for plugin in self.controller.plugins:
                if isinstance(plugin, SettablePlugin):
                    res[b'plugin_names'].append(plugin.name)

            return res
        if msg == b'plugin_get':
            res[b'plugin'] = {}
            plugin_name = payload.get(b'plugin_name')
            plugin, err = self._plugin_get(plugin_name)
            if not plugin:
                res[b'error'] = err
                return res
            res[b'plugin_name'] = plugin_name
            res[b'plugin'] = plugin.get_info()
            return res
        if msg == b'plugin_resource_list':
            res[b'resource_names'] = []
            plugin_name = payload.get(b'plugin_name')
            plugin, err = self._plugin_get(plugin_name)
            if not plugin:
                res[b'error'] = err
                return res
            res[b'plugin_name'] = plugin_name
            try:
                res[b'resource_names'] = plugin.resource_get_list()
            except PluginException as e:
                if str(e) == b'No resource path set':
                    self.debug((b"Plugin '{}' has no resources").format(plugin.name))
                else:
                    self.exception((b"Failed to get resource list for plugin '{}'").format(plugin.name))

            return res
        if msg == b'plugin_resource_get':
            res[b'resource'] = {}
            plugin_name = payload.get(b'plugin_name')
            resource_name = payload.get(b'resource_name')
            if not resource_name:
                res[b'error'] = b'Resource name not set'
                return res
            plugin, err = self._plugin_get(plugin_name)
            if not plugin:
                res[b'error'] = err
                return res
            res[b'plugin_name'] = plugin_name
            res[b'resource_name'] = resource_name
            res[b'resource'] = dict(plugin.resource_get(resource_name))
            if b'path' in res[b'resource']:
                del res[b'resource'][b'path']
            return res
        if msg == b'plugin_resource_load':
            res[b'resource_data'] = b''
            plugin_name = payload.get(b'plugin_name')
            resource_name = payload.get(b'resource_name')
            if not resource_name:
                res[b'error'] = b'Resource name not set'
                return res
            plugin, err = self._plugin_get(plugin_name)
            if not plugin:
                res[b'error'] = err
                return res
            res[b'plugin_name'] = plugin_name
            res[b'resource_name'] = resource_name
            resource_dict = plugin.resource_get(resource_name)
            if not resource_dict:
                res[b'error'] = (b"Resource '{}' not found").format(resource_name)
                return res
            self.debug((b'Resource {}').format(resource_dict))
            try:
                with open(resource_dict[b'path'], b'rb') as (f):
                    res[b'resource_data'] = base64.b64encode(f.read())
            except:
                self.exception((b"Failed to load '{}'").format(resource_dict[b'path']))
                res[b'error'] = b'Failed to load'

            return res
        if msg == b'plugin_data_get':
            plugin_name = payload.get(b'plugin_name')
            plugin, err = self._plugin_get(plugin_name)
            if not plugin:
                res[b'error'] = err
                return res
            res[b'plugin_name'] = plugin_name
            res[b'data'] = plugin.get_data()
            return res
        if msg == b'plugin_data_set':
            plugin_name = payload.get(b'plugin_name')
            plugin, err = self._plugin_get(plugin_name)
            if not plugin:
                res[b'error'] = err
                return res
            res[b'plugin_name'] = plugin_name
            data = payload.get(b'data')
            if not data:
                res[b'error'] = b'No data provided'
                return res
            try:
                plugin.on_config(data)
            except NotImplementedError:
                res[b'error'] = b'Plugin does not support setting data'
                return res
            except:
                self.exception((b'Failed to set data for {}').format(plugin_name))
                res[b'error'] = b'Failed to set data'
                return res

            return {}
        self.error((b"Unknown cmd '{}'\n{}").format(msg, payload))
        return {}

    def _reactor_start(self):
        try:
            if not reactor.running:
                observer = STDLibLogObserver(name=b'twisted')
                globalLogBeginner.beginLoggingTo([observer])
                reactor.run(False)
            else:
                self.info(b'Reactor already running')
        except ReactorAlreadyRunning:
            self.info(b'Reactor already running')
        except:
            self.exception(b'Failed to start reactor')

    def start(self, blocking=False):
        self.debug(b'()')
        if self._is_running:
            self.debug(b'Already running')
            return
        self._factory = WebSocketClientFactory((b'ws://{}:{}{}').format(self._host, self._port, self._ws_path))
        self._factory.protocol = PluginClientProtocol
        self._factory.protocol._webClient = self
        reactor.connectTCP(self._host, self._port, self._factory)
        a_thread = threading.Thread(target=self._reactor_start)
        a_thread.daemon = True
        a_thread.start()
        super(SettingsPlugin, self).start(blocking)

    def stop(self):
        self.debug(b'()')
        if not self._is_running:
            return
        else:
            if self._plugin_protocol:
                reactor.callFromThread(self._plugin_protocol.sendClose)
                time.sleep(1.0)
            reactor.callFromThread(reactor.stop)
            self._factory = None
            super(SettingsPlugin, self).stop()
            self.info(b'Done')
            return