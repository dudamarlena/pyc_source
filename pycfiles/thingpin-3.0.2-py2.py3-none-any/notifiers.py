# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/mgk/projects/thingpin/src/thingpin/notifiers.py
# Compiled at: 2015-12-18 10:12:23
import os, sys, logging
from thingamon import Client, Thing
from Adafruit_IO import MQTTClient

def create_notifier(name, config):
    if name == 'adafruit':
        return AdafruitNotifier(**config)
    if name == 'aws':
        return AWSIoTNotifier(**config)


class Notifier(object):
    pass


class AWSIoTNotifier(Notifier):

    def __init__(self, host=None, client_cert=None, private_key=None, aws_iot_message_unit_cost=5e-06, estimated_change_freq=0.0, debug=False):
        """
        Create an AWS IoT MQTT notifier

        Args:
            host (str): host name of AWS IoT endpoint
            client_cert (str): name of client certificate file
            private_key (str): name of private key for client certificate
            aws_iot_message_unit_cost (float): cost of an AWS IoT message
                used to estimate monthly cost of operating this thingpin
            estimated_change_freq (float): estimate of how often each
                pin will change. Only used for guessing AWS costs at startup.
            debug (bool): if True log all MQTT traffic.
        """
        self.log = logging.getLogger('thingpin')
        self.host = host
        self.client_cert = os.path.expanduser(client_cert)
        self.private_key = os.path.expanduser(private_key)
        self.debug = debug
        self.client = None
        self.log.info(('AWS monthly cost guesstimate ${:,.8f}').format(estimated_change_freq * 60 * 60 * 24 * 30 * aws_iot_message_unit_cost))
        self.log.info('(dont take the guesstimate too seriously!)')
        return

    def initialize(self):
        self.client = Client(self.host, client_cert_filename=self.client_cert, private_key_filename=self.private_key, log_mqtt=self.debug)

    def cleanup(self):
        self.client.disconnect()

    def notify(self, name, value):
        Thing(name, self.client).publish_state(value)


class AdafruitNotifier(Notifier):

    def __init__(self, username=None, api_key=None, host='io.adafruit.com', port=1883):
        """
        Create an Adafruit MQTT notifier

        Args:
            host (str): host name of Adafruit MQTT broker
            port (int): port of Adafruit MQTT broker
            username (str): Adafruit IO username
            api_key (str): Adafruit IO API key
        """
        self.log = logging.getLogger('thingpin')
        self.username = username
        self.api_key = api_key
        self.host = host
        self.port = port
        self.client = None
        return

    def initialize(self):
        self.client = MQTTClient(self.username, self.api_key, service_host=self.host, service_port=self.port)

        def on_disconnect(client):
            if client.disconnect_reason != 0:
                self.log.info('client disconnected, exiting')
                os._exit(1)

        self.client.on_disconnect = on_disconnect
        self.client.connect()
        self.log.info('connected to Adafruit')
        self.client.loop_background()

    def cleanup(self):
        self.client.disconnect()

    def notify(self, name, value):
        self.log.info(('Adafruit IO: publish({}={})').format(name, value))
        self.client.publish(name, value['state'])