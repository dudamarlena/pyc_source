# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/polyinterface/polyinterface.py
# Compiled at: 2020-04-13 17:37:50
# Size of source mod 2**32: 39511 bytes
__doc__ = '\nPython Interface for UDI Polyglot v2 NodeServers\nby Einstein.42 (James Milne) milne.james@gmail.com\n'
import warnings
from copy import deepcopy
from dotenv import load_dotenv
import json, ssl, logging, __main__ as main, markdown2, os
from os.path import join, expanduser
import paho.mqtt.client as mqtt
try:
    import queue
except ImportError:
    import Queue as queue

import re, sys, select
from threading import Thread, current_thread
import time, netifaces
from .polylogger import LOGGER
DEBUG = False
PY2 = sys.version_info[0] == 2
if PY2:
    string_types = basestring
else:
    string_types = str

class LoggerWriter(object):

    def __init__(self, level):
        self.level = level

    def write(self, message):
        if isinstance(message, string_types):
            if not re.match('^\\s*$', message):
                self.level(message.strip())
        else:
            self.level('ERROR: message was not a string: {}'.format(message))

    def flush(self):
        pass


def get_network_interface(interface='default'):
    """
        Returns the network interface which contains addr, broadcasts, and netmask elements

        :param interface: The interface name to check, default grabs
        """
    gws = netifaces.gateways()
    LOGGER.debug('gws: {}'.format(gws))
    rt = False
    if interface in gws:
        gwd = gws[interface][netifaces.AF_INET]
        LOGGER.debug('gw: {}={}'.format(interface, gwd))
        ifad = netifaces.ifaddresses(gwd[1])
        rt = ifad[netifaces.AF_INET]
        LOGGER.debug('ifad: {}={}'.format(gwd[1], rt))
        return rt[0]
    LOGGER.error('No {} in gateways:{}'.format(interface, gws))
    return {'addr':False, 
     'broadcast':False,  'netmask':False}


def init_interface():
    sys.stdout = LoggerWriter(LOGGER.debug)
    sys.stderr = LoggerWriter(LOGGER.error)
    warnings.simplefilter('error', UserWarning)
    try:
        load_dotenv(join(expanduser('~') + '/.polyglot/.env'))
    except UserWarning as err:
        try:
            LOGGER.warning(('File does not exist: {}.'.format(join(expanduser('~') + '/.polyglot/.env'))), exc_info=True)
        finally:
            err = None
            del err

    warnings.resetwarnings()
    init = select.select([sys.stdin], [], [], 1)[0]
    if init:
        line = sys.stdin.readline()
        try:
            line = json.loads(line)
            os.environ['PROFILE_NUM'] = line['profileNum']
            os.environ['MQTT_HOST'] = line['mqttHost']
            os.environ['MQTT_PORT'] = line['mqttPort']
            os.environ['TOKEN'] = line['token']
            LOGGER.info('Received Config from STDIN.')
        except Exception as err:
            try:
                LOGGER.error('Invalid formatted input %s for line: %s', line, err, exc_info=True)
            finally:
                err = None
                del err


def unload_interface():
    sys.stdout = sys.__stdout__
    sys.stderr = sys.__stderr__
    LOGGER.handlers = []


class Interface(object):
    CUSTOM_CONFIG_DOCS_FILE_NAME = 'POLYGLOT_CONFIG.md'
    SERVER_JSON_FILE_NAME = 'server.json'
    _Interface__exists = False

    def __init__(self, envVar=None):
        if self._Interface__exists:
            warnings.warn('Only one Interface is allowed.')
            return
            self.config = None
            self.connected = False
            self.profileNum = os.environ.get('PROFILE_NUM')
            if self.profileNum is None:
                if envVar is not None:
                    self.profileNum = os.environ.get(envVar)
            if self.profileNum is None:
                LOGGER.error('Profile Number not found in STDIN or .env file. Exiting.')
                sys.exit(1)
            self.profileNum = str(self.profileNum)
            self.topicPolyglotConnection = 'udi/polyglot/connections/polyglot'
            self.topicInput = 'udi/polyglot/ns/{}'.format(self.profileNum)
            self.topicSelfConnection = 'udi/polyglot/connections/{}'.format(self.profileNum)
            self._threads = {}
            self._threads['socket'] = Thread(target=(self._startMqtt), name='Interface')
            self._mqttc = mqtt.Client(envVar, True)
            self._mqttc.on_connect = self._connect
            self._mqttc.on_message = self._message
            self._mqttc.on_subscribe = self._subscribe
            self._mqttc.on_disconnect = self._disconnect
            self._mqttc.on_publish = self._publish
            self._mqttc.on_log = self._log
            self.useSecure = True
            if 'USE_HTTPS' in os.environ:
                self.useSecure = os.environ['USE_HTTPS']
            if self.useSecure is True:
                if 'MQTT_CERTPATH' in os.environ:
                    self._mqttc.tls_set(ca_certs=(os.environ['MQTT_CERTPATH'] + '/polyglot.crt'),
                      certfile=(os.environ['MQTT_CERTPATH'] + '/client.crt'),
                      keyfile=(os.environ['MQTT_CERTPATH'] + '/client_private.key'),
                      tls_version=(ssl.PROTOCOL_TLSv1_2))
                else:
                    self._mqttc.tls_set(ca_certs=(join(expanduser('~') + '/.polyglot/ssl/polyglot.crt')),
                      certfile=(join(expanduser('~') + '/.polyglot/ssl/client.crt')),
                      keyfile=(join(expanduser('~') + '/.polyglot/ssl/client_private.key')),
                      tls_version=(ssl.PROTOCOL_TLSv1_2))
        else:
            self.loop = None
            self.inQueue = queue.Queue()
            self.isyVersion = None
            self._server = os.environ.get('MQTT_HOST') or 
            self._port = os.environ.get('MQTT_PORT') or 
            self.polyglotConnected = False
            self._Interface__configObservers = []
            self._Interface__stopObservers = []
            Interface._Interface__exists = True
            self.custom_params_docs_file_sent = False
            self.custom_params_pending_docs = ''
            try:
                self.network_interface = self.get_network_interface()
                LOGGER.info('Connect: Network Interface: {}'.format(self.network_interface))
            except:
                self.network_interface = False
                LOGGER.error('Failed to determine Network Interface', exc_info=True)

    def onConfig(self, callback):
        """
        Gives the ability to bind any methods to be run when the config is received.
        """
        self._Interface__configObservers.append(callback)

    def onStop(self, callback):
        """
        Gives the ability to bind any methods to be run when the stop command is received.
        """
        self._Interface__stopObservers.append(callback)

    def _connect(self, mqttc, userdata, flags, rc):
        """
        The callback for when the client receives a CONNACK response from the server.
        Subscribing in on_connect() means that if we lose the connection and
        reconnect then subscriptions will be renewed.

        :param mqttc: The client instance for this callback
        :param userdata: The private userdata for the mqtt client. Not used in Polyglot
        :param flags: The flags set on the connection.
        :param rc: Result code of connection, 0 = Success, anything else is a failure
        """
        if current_thread().name != 'MQTT':
            current_thread().name = 'MQTT'
        elif rc == 0:
            self.connected = True
            results = []
            LOGGER.info('MQTT Connected with result code ' + str(rc) + ' (Success)')
            results.append((self.topicInput, tuple(self._mqttc.subscribe(self.topicInput))))
            results.append((self.topicPolyglotConnection, tuple(self._mqttc.subscribe(self.topicPolyglotConnection))))
            for topic, (result, mid) in results:
                if result == 0:
                    LOGGER.info('MQTT Subscribing to topic: ' + topic + ' - ' + ' MID: ' + str(mid) + ' Result: ' + str(result))
                else:
                    LOGGER.info('MQTT Subscription to ' + topic + ' failed. This is unusual. MID: ' + str(mid) + ' Result: ' + str(result))
                    self._mqttc.reconnect()

            self._mqttc.publish((self.topicSelfConnection), (json.dumps({'connected':True, 
             'node':self.profileNum})),
              retain=True)
            LOGGER.info('Sent Connected message to Polyglot')
        else:
            LOGGER.error('MQTT Failed to connect. Result code: ' + str(rc))

    def _message(self, mqttc, userdata, msg):
        """
        The callback for when a PUBLISH message is received from the server.

        :param mqttc: The client instance for this callback
        :param userdata: The private userdata for the mqtt client. Not used in Polyglot
        :param flags: The flags set on the connection.
        :param msg: Dictionary of MQTT received message. Uses: msg.topic, msg.qos, msg.payload
        """
        try:
            inputCmds = [
             'query', 'command', 'result', 'status', 'shortPoll', 'longPoll', 'delete']
            parsed_msg = json.loads(msg.payload.decode('utf-8'))
            if DEBUG:
                LOGGER.debug('MQTT Received Message: {}: {}'.format(msg.topic, parsed_msg))
            if 'node' in parsed_msg:
                if parsed_msg['node'] != 'polyglot':
                    return
                del parsed_msg['node']
                for key in parsed_msg:
                    if DEBUG:
                        LOGGER.debug('MQTT Processing Message: {}: {}'.format(msg.topic, parsed_msg))
                    if key == 'config':
                        self.inConfig(parsed_msg[key])
                    elif key == 'connected':
                        self.polyglotConnected = parsed_msg[key]
                    elif key == 'stop':
                        LOGGER.debug('Received stop from Polyglot... Shutting Down.')
                        self.stop()
                    elif key in inputCmds:
                        self.input(parsed_msg)
                    else:
                        LOGGER.error('Invalid command received in message from Polyglot: {}'.format(key))

            else:
                LOGGER.error('MQTT Received Unknown Message: {}: {}'.format(msg.topic, parsed_msg))
        except ValueError as err:
            try:
                LOGGER.error(('MQTT Received Payload Error: {}'.format(err)), exc_info=True)
            finally:
                err = None
                del err

        except Exception as ex:
            try:
                template = 'An exception of type {0} occured. Arguments:\n{1!r}'
                message = template.format(type(ex).__name__, ex.args)
                LOGGER.error(('MQTT Received Unknown Error: ' + message), exc_info=True)
            finally:
                ex = None
                del ex

    def _disconnect(self, mqttc, userdata, rc):
        """
        The callback for when a DISCONNECT occurs.

        :param mqttc: The client instance for this callback
        :param userdata: The private userdata for the mqtt client. Not used in Polyglot
        :param rc: Result code of connection, 0 = Graceful, anything else is unclean
        """
        self.connected = False
        if rc != 0:
            LOGGER.info('MQTT Unexpected disconnection. Trying reconnect.')
            try:
                self._mqttc.reconnect()
            except Exception as ex:
                try:
                    template = 'An exception of type {0} occured. Arguments:\n{1!r}'
                    message = template.format(type(ex).__name__, ex.args)
                    LOGGER.error('MQTT Connection error: ' + message)
                finally:
                    ex = None
                    del ex

        else:
            LOGGER.info('MQTT Graceful disconnection.')

    def _log(self, mqttc, userdata, level, string):
        """ Use for debugging MQTT Packets, disable for normal use, NOISY. """
        if DEBUG:
            LOGGER.info('MQTT Log - {}: {}'.format(str(level), str(string)))

    def _subscribe(self, mqttc, userdata, mid, granted_qos):
        """ Callback for Subscribe message. Unused currently. """
        LOGGER.info('MQTT Subscribed Succesfully for Message ID: {} - QoS: {}'.format(str(mid), str(granted_qos)))

    def _publish(self, mqttc, userdata, mid):
        """ Callback for publish message. Unused currently. """
        if DEBUG:
            LOGGER.info('MQTT Published message ID: {}'.format(str(mid)))

    def start(self):
        for _, thread in self._threads.items():
            thread.start()

    def _startMqtt(self):
        """
        The client start method. Starts the thread for the MQTT Client
        and publishes the connected message.
        """
        LOGGER.info('Connecting to MQTT... {}:{}'.format(self._server, self._port))
        done = False
        while not done:
            try:
                self._mqttc.connect_async('{}'.format(self._server), int(self._port), 10)
                self._mqttc.loop_forever()
                done = True
            except ssl.SSLError as e:
                try:
                    LOGGER.error(('MQTT Connection SSLError: {}, Will retry in a few seconds.'.format(e)), exc_info=True)
                    time.sleep(3)
                finally:
                    e = None
                    del e

            except Exception as ex:
                try:
                    template = 'An exception of type {0} occurred. Arguments:\n{1!r}'
                    message = template.format(type(ex).__name__, ex.args)
                    LOGGER.error(('MQTT Connection error: {}'.format(message)), exc_info=True)
                    done = True
                finally:
                    ex = None
                    del ex

        LOGGER.debug('MQTT Done:')

    def stop(self):
        """
        The client stop method. If the client is currently connected
        stop the thread and disconnect. Publish the disconnected
        message if clean shutdown.
        """
        if self.connected:
            LOGGER.info('Disconnecting from MQTT... {}:{}'.format(self._server, self._port))
            self._mqttc.publish((self.topicSelfConnection), (json.dumps({'node':self.profileNum,  'connected':False})), retain=True)
            self._mqttc.loop_stop()
            self._mqttc.disconnect()
        try:
            for watcher in self._Interface__stopObservers:
                watcher()

        except KeyError as e:
            try:
                LOGGER.exception(('KeyError in gotConfig: {}'.format(e)), exc_info=True)
            finally:
                e = None
                del e

    def send(self, message):
        """
        Formatted Message to send to Polyglot. Connection messages are sent automatically from this module
        so this method is used to send commands to/from Polyglot and formats it for consumption
        """
        if not isinstance(message, dict):
            if self.connected:
                warnings.warn('payload not a dictionary')
                return False
        try:
            message['node'] = self.profileNum
            self._mqttc.publish((self.topicInput), (json.dumps(message)), retain=False)
        except TypeError as err:
            try:
                LOGGER.error(('MQTT Send Error: {}'.format(err)), exc_info=True)
            finally:
                err = None
                del err

    def addNode(self, node):
        """
        Add a node to the NodeServer

        :param node: Dictionary of node settings. Keys: address, name, node_def_id, primary, and drivers are required.
        """
        LOGGER.info('Adding node {}({})'.format(node.name, node.address))
        message = {'addnode': {'nodes': [
                               {'address':node.address, 
                                'name':node.name, 
                                'node_def_id':node.id, 
                                'primary':node.primary, 
                                'drivers':node.drivers, 
                                'hint':node.hint}]}}
        self.send(message)

    def saveCustomData(self, data):
        """
        Send custom dictionary to Polyglot to save and be retrieved on startup.

        :param data: Dictionary of key value pairs to store in Polyglot database.
        """
        LOGGER.info('Sending customData to Polyglot.')
        message = {'customdata': data}
        self.send(message)

    def saveCustomParams(self, data):
        """
        Send custom dictionary to Polyglot to save and be retrieved on startup.

        :param data: Dictionary of key value pairs to store in Polyglot database.
        """
        LOGGER.info('Sending customParams to Polyglot.')
        message = {'customparams': data}
        self.send(message)

    def addNotice(self, data):
        """
        Add custom notice to front-end for this NodeServers

        :param data: String of characters to add as a notification in the front-end.
        """
        LOGGER.info('Sending addnotice to Polyglot: {}'.format(data))
        message = {'addnotice': data}
        self.send(message)

    def removeNotice(self, data):
        """
        Add custom notice to front-end for this NodeServers

        :param data: Index of notices list to remove.
        """
        LOGGER.info('Sending removenotice to Polyglot for index {}'.format(data))
        message = {'removenotice': data}
        self.send(message)

    def restart(self):
        """
        Send a command to Polyglot to restart this NodeServer
        """
        LOGGER.info('Asking Polyglot to restart me.')
        message = {'restart': {}}
        self.send(message)

    def installprofile(self):
        LOGGER.info('Sending Install Profile command to Polyglot.')
        message = {'installprofile': {'reboot': False}}
        self.send(message)

    def delNode(self, address):
        """
        Delete a node from the NodeServer

        :param node: Dictionary of node settings. Keys: address, name, node_def_id, primary, and drivers are required.
        """
        LOGGER.info('Removing node {}'.format(address))
        message = {'removenode': {'address': address}}
        self.send(message)

    def getNode(self, address):
        """
        Get Node by Address of existing nodes.
        """
        try:
            for node in self.config['nodes']:
                if node['address'] == address:
                    return node

            return False
        except KeyError:
            LOGGER.error('Usually means we have not received the config yet.', exc_info=True)
            return False

    def inConfig(self, config):
        """
        Save incoming config received from Polyglot to Interface.config and then do any functions
        that are waiting on the config to be received.
        """
        self.config = config
        self.isyVersion = config['isyVersion']
        try:
            for watcher in self._Interface__configObservers:
                watcher(config)

            self.send_custom_config_docs()
        except KeyError as e:
            try:
                LOGGER.error(('KeyError in gotConfig: {}'.format(e)), exc_info=True)
            finally:
                e = None
                del e

    def input(self, command):
        self.inQueue.put(command)

    def supports_feature(self, feature):
        return True

    def get_md_file_data(self, fileName):
        data = ''
        if os.path.isfile(fileName):
            data = markdown2.markdown_path(fileName)
        return data

    def send_custom_config_docs(self):
        data = ''
        if not self.custom_params_docs_file_sent:
            data = self.get_md_file_data(Interface.CUSTOM_CONFIG_DOCS_FILE_NAME)
        else:
            data = self.config.get('customParamsDoc', '')
        if not self.custom_params_docs_file_sent or len(self.custom_params_pending_docs) > 0:
            data += self.custom_params_pending_docs
            self.custom_params_docs_file_sent = True
            self.custom_params_pending_docs = ''
            self.config['customParamsDoc'] = data
            self.send({'customparamsdoc': data})

    def add_custom_config_docs(self, data, clearCurrentData=False):
        if clearCurrentData:
            self.custom_params_docs_file_sent = False
        self.custom_params_pending_docs += data
        self.send_custom_config_docs()

    def save_typed_params(self, data):
        """
        Send custom parameters descriptions to Polyglot to be used
        in front end UI configuration screen
        Accepts list of objects with the followin properties
            name - used as a key when data is sent from UI
            title - displayed in UI
            defaultValue - optionanl
            type - optional, can be 'NUMBER', 'STRING' or 'BOOLEAN'.
                Defaults to 'STRING'
            desc - optional, shown in tooltip in UI
            isRequired - optional, True/False, when set, will not validate UI
                input if it's empty
            isList - optional, True/False, if set this will be treated as list
                of values or objects by UI
            params - optional, can contain a list of objects. If present, then
                this (parent) is treated as object / list of objects by UI,
                otherwise, it's treated as a single / list of single values
        """
        LOGGER.info('Sending typed parameters to Polyglot.')
        if type(data) is not list:
            data = [
             data]
        message = {'typedparams': data}
        self.send(message)

    def get_network_interface(self, interface='default'):
        return get_network_interface(interface=interface)

    def get_server_data(self, check_profile=True, build_profile=None):
        """
        get_server_data: Loads the server.json and returns as a dict
        :param check_profile: Calls the check_profile method if True
        """
        serverdata = {'version': 'unknown'}
        try:
            with open(Interface.SERVER_JSON_FILE_NAME) as (data):
                serverdata = json.load(data)
        except Exception as err:
            try:
                LOGGER.error(('get_server_data: failed to read file {0}: {1}'.format(Interface.SERVER_JSON_FILE_NAME, err)), exc_info=True)
                return serverdata
            finally:
                err = None
                del err

        data.close()
        try:
            version = serverdata['credits'][0]['version']
        except (KeyError, ValueError):
            LOGGER.info('Version (credits[0][version]) not found in server.json.')
            version = '0.0.0.0'

        serverdata['version'] = version
        if 'profile_version' not in serverdata:
            serverdata['profile_version'] = None
        LOGGER.debug('get_server_data: {}'.format(serverdata))
        if check_profile:
            self.check_profile(serverdata, build_profile=build_profile)
        return serverdata

    def check_profile(self, serverdata, build_profile=None):
        """
        Check if the profile is up to date by comparing the server.json profile_version
        against the profile_version stored in the db customData
        The profile will be installed if necessary.
        """
        LOGGER.debug('check_profile:      config={}'.format(self.config))
        cdata = deepcopy(self.config['customData'])
        LOGGER.debug('check_profile:      customData={}'.format(cdata))
        LOGGER.debug('check_profile: profile_version={}'.format(serverdata['profile_version']))
        if serverdata['profile_version'] is None:
            LoGGER.info('check_profile: Ignoring since nodeserver does not have profile_version')
            return
        update_profile = False
        if 'profile_version' not in cdata:
            LOGGER.info('check_profile: Updated needed since it has never been recorded.')
            update_profile = True
        elif serverdata['profile_version'] == cdata['profile_version']:
            LOGGER.info('check_profile: No updated needed: "{}" == "{}"'.format(serverdata['profile_version'], cdata['profile_version']))
            update_profile = False
        else:
            LOGGER.info('check_profile: Updated needed: "{}" == "{}"'.format(serverdata['profile_version'], cdata['profile_version']))
            update_profile = True
        if update_profile:
            if build_profile:
                LOGGER.info('Building Profile...')
                build_profile()
            st = self.installprofile()
            cdata['profile_version'] = serverdata['profile_version']
            self.saveCustomData(cdata)


class Node(object):
    """Node"""

    def __init__(self, controller, primary, address, name):
        try:
            self.controller = controller
            self.parent = self.controller
            self.primary = primary
            self.address = address
            self.name = name
            self.polyConfig = None
            self.drivers = deepcopy(self.drivers)
            self._drivers = deepcopy(self.drivers)
            self.isPrimary = None
            self.config = None
            self.timeAdded = None
            self.enabled = None
            self.added = None
        except KeyError as err:
            try:
                LOGGER.error(('Error Creating node: {}'.format(err)), exc_info=True)
            finally:
                err = None
                del err

    def _convertDrivers(self, drivers):
        return deepcopy(drivers)

    def setDriver(self, driver, value, report=True, force=False, uom=None):
        for d in self.drivers:
            if d['driver'] == driver:
                d['value'] = value
                if uom is not None:
                    d['uom'] = uom
                if report:
                    self.reportDriver(d, report, force)
                break

    def reportDriver(self, driver, report, force):
        for d in self._drivers:
            if d['driver'] == driver['driver']:
                if str(d['value']) != str(driver['value']) or d['uom'] != driver['uom'] or force:
                    LOGGER.info('Updating Driver {} - {}: {}, uom: {}'.format(self.address, driver['driver'], driver['value'], driver['uom']))
                    d['value'] = deepcopy(driver['value'])
                    if d['uom'] != driver['uom']:
                        d['uom'] = deepcopy(driver['uom'])
                message = {'status': {'address':self.address, 
                            'driver':driver['driver'], 
                            'value':str(driver['value']), 
                            'uom':driver['uom']}}
                self.controller.poly.send(message)
                break

    def reportCmd(self, command, value=None, uom=None):
        message = {'command': {'address':self.address, 
                     'command':command}}
        if value is not None:
            if uom is not None:
                message['command']['value'] = str(value)
                message['command']['uom'] = uom
        self.controller.poly.send(message)

    def reportDrivers(self):
        LOGGER.info('Updating All Drivers to ISY for {}({})'.format(self.name, self.address))
        self.updateDrivers(self.drivers)
        for driver in self.drivers:
            message = {'status': {'address':self.address, 
                        'driver':driver['driver'], 
                        'value':driver['value'], 
                        'uom':driver['uom']}}
            self.controller.poly.send(message)

    def updateDrivers(self, drivers):
        self._drivers = deepcopy(drivers)

    def query(self):
        self.reportDrivers()

    def status(self):
        self.reportDrivers()

    def runCmd(self, command):
        if command['cmd'] in self.commands:
            fun = self.commands[command['cmd']]
            fun(self, command)

    def start(self):
        pass

    def getDriver(self, dv):
        for index, node in enumerate(self.controller.poly.config['nodes']):
            if node['address'] == self.address:
                for index, driver in enumerate(node['drivers']):
                    if driver['driver'] == dv:
                        return driver['value']

    def toJSON(self):
        LOGGER.debug(json.dumps(self.__dict__))

    def __rep__(self):
        return self.toJSON()

    id = ''
    commands = {}
    drivers = []
    sends = {}
    hint = [0, 0, 0, 0]


class Controller(Node):
    """Controller"""
    _Controller__exists = False

    def __init__(self, poly, name='Controller'):
        if self._Controller__exists:
            warnings.warn('Only one Controller is allowed.')
            return
        try:
            self.controller = self
            self.parent = self.controller
            self.poly = poly
            self.poly.onConfig(self._gotConfig)
            self.poly.onStop(self.stop)
            self.name = name
            self.address = 'controller'
            self.primary = self.address
            self._drivers = deepcopy(self.drivers)
            self._nodes = {}
            self.config = None
            self.nodes = {self.address: self}
            self._threads = {}
            self._threads['input'] = Thread(target=(self._parseInput), name='Controller')
            self._threads['ns'] = Thread(target=(self.start), name='NodeServer')
            self.polyConfig = None
            self.isPrimary = None
            self.timeAdded = None
            self.enabled = None
            self.added = None
            self.started = False
            self.nodesAdding = []
            self._startThreads()
        except KeyError as err:
            try:
                LOGGER.error(('Error Creating node: {}'.format(err)), exc_info=True)
            finally:
                err = None
                del err

    def _gotConfig(self, config):
        self.polyConfig = config
        for node in config['nodes']:
            self._nodes[node['address']] = node
            if node['address'] in self.nodes:
                n = self.nodes[node['address']]
                n.updateDrivers(node['drivers'])
                n.config = node
                n.isPrimary = node['isprimary']
                n.timeAdded = node['timeAdded']
                n.enabled = node['enabled']
                n.added = node['added']

        if self.address not in self._nodes:
            self.addNode(self)
            LOGGER.info('Waiting on Controller node to be added.......')
        if not self.started:
            self.nodes[self.address] = self
            self.started = True
            self._threads['ns'].start()

    def _startThreads(self):
        self._threads['input'].daemon = True
        self._threads['ns'].daemon = True
        self._threads['input'].start()

    def _parseInput--- This code section failed: ---

 L. 828       0_2  SETUP_LOOP          462  'to 462'

 L. 829         4  LOAD_FAST                'self'
                6  LOAD_ATTR                poly
                8  LOAD_ATTR                inQueue
               10  LOAD_METHOD              get
               12  CALL_METHOD_0         0  ''
               14  STORE_FAST               'input'

 L. 830     16_18  SETUP_LOOP          446  'to 446'
               20  LOAD_FAST                'input'
               22  GET_ITER         
             24_0  COME_FROM           432  '432'
             24_1  COME_FROM           372  '372'
            24_26  FOR_ITER            444  'to 444'
               28  STORE_FAST               'key'

 L. 831        30  LOAD_FAST                'key'
               32  LOAD_STR                 'command'
               34  COMPARE_OP               ==
               36  POP_JUMP_IF_FALSE   202  'to 202'

 L. 832        38  LOAD_FAST                'input'
               40  LOAD_FAST                'key'
               42  BINARY_SUBSCR    
               44  LOAD_STR                 'address'
               46  BINARY_SUBSCR    
               48  LOAD_FAST                'self'
               50  LOAD_ATTR                nodes
               52  COMPARE_OP               in
               54  POP_JUMP_IF_FALSE   166  'to 166'

 L. 833        56  SETUP_EXCEPT         90  'to 90'

 L. 834        58  LOAD_FAST                'self'
               60  LOAD_ATTR                nodes
               62  LOAD_FAST                'input'
               64  LOAD_FAST                'key'
               66  BINARY_SUBSCR    
               68  LOAD_STR                 'address'
               70  BINARY_SUBSCR    
               72  BINARY_SUBSCR    
               74  LOAD_METHOD              runCmd
               76  LOAD_FAST                'input'
               78  LOAD_FAST                'key'
               80  BINARY_SUBSCR    
               82  CALL_METHOD_1         1  ''
               84  POP_TOP          
               86  POP_BLOCK        
               88  JUMP_ABSOLUTE       200  'to 200'
             90_0  COME_FROM_EXCEPT     56  '56'

 L. 835        90  DUP_TOP          
               92  LOAD_GLOBAL              Exception
               94  COMPARE_OP               exception-match
               96  POP_JUMP_IF_FALSE   162  'to 162'
               98  POP_TOP          
              100  STORE_FAST               'err'
              102  POP_TOP          
              104  SETUP_FINALLY       150  'to 150'

 L. 836       106  LOAD_GLOBAL              LOGGER
              108  LOAD_ATTR                error
              110  LOAD_STR                 '_parseInput: failed {}.runCmd({}) {}'
              112  LOAD_METHOD              format
              114  LOAD_FAST                'input'
              116  LOAD_FAST                'key'
              118  BINARY_SUBSCR    
              120  LOAD_STR                 'address'
              122  BINARY_SUBSCR    
              124  LOAD_FAST                'input'
              126  LOAD_FAST                'key'
              128  BINARY_SUBSCR    
              130  LOAD_STR                 'cmd'
              132  BINARY_SUBSCR    
              134  LOAD_FAST                'err'
              136  CALL_METHOD_3         3  ''
              138  LOAD_CONST               True
              140  LOAD_CONST               ('exc_info',)
              142  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              144  POP_TOP          
              146  POP_BLOCK        
              148  LOAD_CONST               None
            150_0  COME_FROM_FINALLY   104  '104'
              150  LOAD_CONST               None
              152  STORE_FAST               'err'
              154  DELETE_FAST              'err'
              156  END_FINALLY      
              158  POP_EXCEPT       
              160  JUMP_ABSOLUTE       200  'to 200'
            162_0  COME_FROM            96  '96'
              162  END_FINALLY      
              164  JUMP_FORWARD        200  'to 200'
            166_0  COME_FROM            54  '54'

 L. 838       166  LOAD_GLOBAL              LOGGER
              168  LOAD_METHOD              error
              170  LOAD_STR                 '_parseInput: received command {} for a node that is not in memory: {}'
              172  LOAD_METHOD              format
              174  LOAD_FAST                'input'
              176  LOAD_FAST                'key'
              178  BINARY_SUBSCR    
              180  LOAD_STR                 'cmd'
              182  BINARY_SUBSCR    
              184  LOAD_FAST                'input'
              186  LOAD_FAST                'key'
              188  BINARY_SUBSCR    
              190  LOAD_STR                 'address'
              192  BINARY_SUBSCR    
              194  CALL_METHOD_2         2  ''
              196  CALL_METHOD_1         1  ''
              198  POP_TOP          
            200_0  COME_FROM           164  '164'
              200  JUMP_BACK            24  'to 24'
            202_0  COME_FROM            36  '36'

 L. 839       202  LOAD_FAST                'key'
              204  LOAD_STR                 'result'
              206  COMPARE_OP               ==
              208  POP_JUMP_IF_FALSE   226  'to 226'

 L. 840       210  LOAD_FAST                'self'
              212  LOAD_METHOD              _handleResult
              214  LOAD_FAST                'input'
              216  LOAD_FAST                'key'
              218  BINARY_SUBSCR    
              220  CALL_METHOD_1         1  ''
              222  POP_TOP          
              224  JUMP_BACK            24  'to 24'
            226_0  COME_FROM           208  '208'

 L. 841       226  LOAD_FAST                'key'
              228  LOAD_STR                 'delete'
              230  COMPARE_OP               ==
              232  POP_JUMP_IF_FALSE   244  'to 244'

 L. 842       234  LOAD_FAST                'self'
              236  LOAD_METHOD              _delete
              238  CALL_METHOD_0         0  ''
              240  POP_TOP          
              242  JUMP_BACK            24  'to 24'
            244_0  COME_FROM           232  '232'

 L. 843       244  LOAD_FAST                'key'
              246  LOAD_STR                 'shortPoll'
              248  COMPARE_OP               ==
          250_252  POP_JUMP_IF_FALSE   264  'to 264'

 L. 844       254  LOAD_FAST                'self'
              256  LOAD_METHOD              shortPoll
              258  CALL_METHOD_0         0  ''
              260  POP_TOP          
              262  JUMP_BACK            24  'to 24'
            264_0  COME_FROM           250  '250'

 L. 845       264  LOAD_FAST                'key'
              266  LOAD_STR                 'longPoll'
              268  COMPARE_OP               ==
          270_272  POP_JUMP_IF_FALSE   284  'to 284'

 L. 846       274  LOAD_FAST                'self'
              276  LOAD_METHOD              longPoll
              278  CALL_METHOD_0         0  ''
              280  POP_TOP          
              282  JUMP_BACK            24  'to 24'
            284_0  COME_FROM           270  '270'

 L. 847       284  LOAD_FAST                'key'
              286  LOAD_STR                 'query'
              288  COMPARE_OP               ==
          290_292  POP_JUMP_IF_FALSE   366  'to 366'

 L. 848       294  LOAD_FAST                'input'
              296  LOAD_FAST                'key'
              298  BINARY_SUBSCR    
              300  LOAD_STR                 'address'
              302  BINARY_SUBSCR    
              304  LOAD_FAST                'self'
              306  LOAD_ATTR                nodes
              308  COMPARE_OP               in
          310_312  POP_JUMP_IF_FALSE   338  'to 338'

 L. 849       314  LOAD_FAST                'self'
              316  LOAD_ATTR                nodes
              318  LOAD_FAST                'input'
              320  LOAD_FAST                'key'
              322  BINARY_SUBSCR    
              324  LOAD_STR                 'address'
              326  BINARY_SUBSCR    
              328  BINARY_SUBSCR    
              330  LOAD_METHOD              query
              332  CALL_METHOD_0         0  ''
              334  POP_TOP          
              336  JUMP_FORWARD        364  'to 364'
            338_0  COME_FROM           310  '310'

 L. 850       338  LOAD_FAST                'input'
              340  LOAD_FAST                'key'
              342  BINARY_SUBSCR    
              344  LOAD_STR                 'address'
              346  BINARY_SUBSCR    
              348  LOAD_STR                 'all'
              350  COMPARE_OP               ==
          352_354  POP_JUMP_IF_FALSE   442  'to 442'

 L. 851       356  LOAD_FAST                'self'
              358  LOAD_METHOD              query
              360  CALL_METHOD_0         0  ''
              362  POP_TOP          
            364_0  COME_FROM           336  '336'
              364  JUMP_BACK            24  'to 24'
            366_0  COME_FROM           290  '290'

 L. 852       366  LOAD_FAST                'key'
              368  LOAD_STR                 'status'
              370  COMPARE_OP               ==
              372  POP_JUMP_IF_FALSE    24  'to 24'

 L. 853       374  LOAD_FAST                'input'
              376  LOAD_FAST                'key'
              378  BINARY_SUBSCR    
              380  LOAD_STR                 'address'
              382  BINARY_SUBSCR    
              384  LOAD_FAST                'self'
              386  LOAD_ATTR                nodes
              388  COMPARE_OP               in
          390_392  POP_JUMP_IF_FALSE   418  'to 418'

 L. 854       394  LOAD_FAST                'self'
              396  LOAD_ATTR                nodes
              398  LOAD_FAST                'input'
              400  LOAD_FAST                'key'
              402  BINARY_SUBSCR    
              404  LOAD_STR                 'address'
              406  BINARY_SUBSCR    
              408  BINARY_SUBSCR    
              410  LOAD_METHOD              status
              412  CALL_METHOD_0         0  ''
              414  POP_TOP          
              416  JUMP_BACK            24  'to 24'
            418_0  COME_FROM           390  '390'

 L. 855       418  LOAD_FAST                'input'
              420  LOAD_FAST                'key'
              422  BINARY_SUBSCR    
              424  LOAD_STR                 'address'
              426  BINARY_SUBSCR    
              428  LOAD_STR                 'all'
              430  COMPARE_OP               ==
              432  POP_JUMP_IF_FALSE    24  'to 24'

 L. 856       434  LOAD_FAST                'self'
              436  LOAD_METHOD              status
              438  CALL_METHOD_0         0  ''
              440  POP_TOP          
            442_0  COME_FROM           352  '352'
              442  JUMP_BACK            24  'to 24'
              444  POP_BLOCK        
            446_0  COME_FROM_LOOP       16  '16'

 L. 857       446  LOAD_FAST                'self'
              448  LOAD_ATTR                poly
              450  LOAD_ATTR                inQueue
              452  LOAD_METHOD              task_done
              454  CALL_METHOD_0         0  ''
              456  POP_TOP          
              458  JUMP_BACK             4  'to 4'
              460  POP_BLOCK        
            462_0  COME_FROM_LOOP        0  '0'

Parse error at or near `COME_FROM_LOOP' instruction at offset 446_0

    def _handleResult(self, result):
        try:
            if 'addnode' in result:
                if result['addnode']['success']:
                    if not result['addnode']['address'] == self.address:
                        self.nodes[result['addnode']['address']].start()
                    if result['addnode']['address'] in self.nodesAdding:
                        self.nodesAdding.remove(result['addnode']['address'])
                else:
                    del self.nodes[result['addnode']['address']]
        except (KeyError, ValueError) as err:
            try:
                LOGGER.error(('handleResult: {}'.format(err)), exc_info=True)
            finally:
                err = None
                del err

    def _delete(self):
        """
        Intermediate message that stops MQTT before sending to overrideable method for delete.
        """
        self.poly.stop()
        self.delete()

    def _convertDrivers(self, drivers):
        return deepcopy(drivers)

    def delete(self):
        """
        Incoming delete message from Polyglot. This NodeServer is being deleted.
        You have 5 seconds before the process is killed. Cleanup and disconnect.
        """
        pass

    def addNode(self, node, update=False):
        if node.address in self._nodes:
            node._drivers = self._nodes[node.address]['drivers']
            for driver in node.drivers:
                for existing in self._nodes[node.address]['drivers']:
                    if driver['driver'] == existing['driver']:
                        driver['value'] = existing['value']

        self.nodes[node.address] = node
        self.nodesAdding.append(node.address)
        self.poly.addNode(node)
        return node

    def updateNode(self, node):
        self.nodes[node.address] = node
        self.nodesAdding.append(node.address)
        self.poly.addNode(node)

    def delNode(self, address):
        """
        Just send it along if requested, should be able to delete the node even if it isn't
        in our config anywhere. Usually used for normalization.
        """
        if address in self.nodes:
            del self.nodes[address]
        self.poly.delNode(address)

    def longPoll(self):
        pass

    def shortPoll(self):
        pass

    def query(self):
        for node in self.nodes:
            self.nodes[node].reportDrivers()

    def status(self):
        for node in self.nodes:
            self.nodes[node].reportDrivers()

    def runForever(self):
        self._threads['input'].join()

    def start(self):
        pass

    def saveCustomData(self, data):
        if not isinstance(data, dict):
            LOGGER.error("saveCustomData: data isn't a dictionary. Ignoring.")
        else:
            self.poly.saveCustomData(data)

    def addCustomParam(self, data):
        if not isinstance(data, dict):
            LOGGER.error("addCustomParam: data isn't a dictionary. Ignoring.")
        else:
            newData = self.poly.config['customParams']
            newData.update(data)
            self.poly.saveCustomParams(newData)

    def removeCustomParam(self, data):
        try:
            basestring
        except NameError:
            basestring = str

        if not isinstance(data, basestring):
            LOGGER.error("removeCustomParam: data isn't a string. Ignoring.")
        else:
            try:
                newData = deepcopy(self.poly.config['customParams'])
                newData.pop(data)
                self.poly.saveCustomParams(newData)
            except KeyError:
                LOGGER.error(('{} not found in customParams. Ignoring...'.format(data)), exc_info=True)

    def getCustomParam(self, data):
        params = deepcopy(self.poly.config['customParams'])
        return params.get(data)

    def addNotice(self, data, key=None):
        if not isinstance(data, dict):
            self.poly.addNotice({'key':key,  'value':data})
        elif 'value' in data:
            self.poly.addNotice(data)
        else:
            for key, value in data.items():
                self.poly.addNotice({'key':key,  'value':value})

    def removeNotice(self, key):
        data = {'key': str(key)}
        self.poly.removeNotice(data)

    def getNotices(self):
        return self.poly.config['notices']

    def removeNoticesAll--- This code section failed: ---

 L.1011         0  LOAD_GLOBAL              type
                2  LOAD_FAST                'self'
                4  LOAD_ATTR                poly
                6  LOAD_ATTR                config
                8  LOAD_STR                 'notices'
               10  BINARY_SUBSCR    
               12  CALL_FUNCTION_1       1  ''
               14  LOAD_GLOBAL              dict
               16  COMPARE_OP               ==
               18  POP_JUMP_IF_FALSE    58  'to 58'

 L.1012        20  SETUP_LOOP          114  'to 114'
               22  LOAD_FAST                'self'
               24  LOAD_ATTR                poly
               26  LOAD_ATTR                config
               28  LOAD_STR                 'notices'
               30  BINARY_SUBSCR    
               32  LOAD_METHOD              keys
               34  CALL_METHOD_0         0  ''
               36  GET_ITER         
               38  FOR_ITER             54  'to 54'
               40  STORE_FAST               'key'

 L.1013        42  LOAD_FAST                'self'
               44  LOAD_METHOD              removeNotice
               46  LOAD_FAST                'key'
               48  CALL_METHOD_1         1  ''
               50  POP_TOP          
               52  JUMP_BACK            38  'to 38'
               54  POP_BLOCK        
               56  JUMP_FORWARD        114  'to 114'
             58_0  COME_FROM            18  '18'

 L.1015        58  LOAD_GLOBAL              len
               60  LOAD_FAST                'self'
               62  LOAD_ATTR                poly
               64  LOAD_ATTR                config
               66  LOAD_STR                 'notices'
               68  BINARY_SUBSCR    
               70  CALL_FUNCTION_1       1  ''
               72  POP_JUMP_IF_FALSE   114  'to 114'

 L.1016        74  SETUP_LOOP          114  'to 114'
               76  LOAD_GLOBAL              range
               78  LOAD_GLOBAL              len
               80  LOAD_FAST                'self'
               82  LOAD_ATTR                poly
               84  LOAD_ATTR                config
               86  LOAD_STR                 'notices'
               88  BINARY_SUBSCR    
               90  CALL_FUNCTION_1       1  ''
               92  CALL_FUNCTION_1       1  ''
               94  GET_ITER         
               96  FOR_ITER            112  'to 112'
               98  STORE_FAST               'i'

 L.1017       100  LOAD_FAST                'self'
              102  LOAD_METHOD              removeNotice
              104  LOAD_FAST                'i'
              106  CALL_METHOD_1         1  ''
              108  POP_TOP          
              110  JUMP_BACK            96  'to 96'
              112  POP_BLOCK        
            114_0  COME_FROM_LOOP       74  '74'
            114_1  COME_FROM            72  '72'
            114_2  COME_FROM            56  '56'
            114_3  COME_FROM_LOOP       20  '20'

Parse error at or near `COME_FROM' instruction at offset 114_2

    def stop(self):
        """ Called on nodeserver stop """
        pass

    id = 'controller'
    commands = {}
    drivers = [{'driver':'ST',  'value':0,  'uom':2}]


if __name__ == '__main__':
    sys.exit(0)
if hasattr(main, '__file__'):
    init_interface()