# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\robopython\robo\light.py
# Compiled at: 2020-03-04 11:05:05
from binascii import hexlify

class Light(object):

    def __init__(self, name, ble, mqtt, protocol, default_topic, id_num, trigger_id):
        self.is_connected = 1
        self.name = name
        self.id = id_num
        self.trigger_id = trigger_id
        self.trigger_status = None
        self.BLE = ble
        self.MQTT = mqtt
        self.protocol = protocol
        self.default_topic = default_topic
        return

    def connected(self):
        self.is_connected = 1
        print 'Light' + str(self.id) + ' connected'

    def disconnected(self):
        self.is_connected = 0
        print 'Light' + str(self.id) + ' disconnected'

    def get_light(self, topic=None):
        packet_size = 3
        command_id = 128
        payload_size = 1
        module_id = self.id - 1
        command = bytearray([packet_size, command_id, payload_size, module_id])
        if topic is None:
            topic = self.default_topic
        if self.is_connected == 1:
            if self.protocol == 'BLE':
                self.BLE.write_to_robo(self.BLE.write_uuid, command)
                light = hexlify(self.BLE.read_from_robo())
                light = [ light[i:i + 2] for i in xrange(0, len(light), 2) ]
                if len(light) != 5:
                    return
                light_lvl = int(light[(-2)], 16) * 256 + int(light[(-3)], 16)
                return light_lvl
            if self.protocol == 'MQTT':
                command = self.MQTT.get_mqtt_cmd([command_id, payload_size, module_id])
                self.MQTT.message = 'None'
                self.MQTT.publish(topic, command)
                while self.MQTT.message[0:2] != '80':
                    time.sleep(0.01)

                light = self.MQTT.message
                if light is None:
                    return
                light = [ light[i:i + 2] for i in xrange(0, len(light), 2) ]
                if len(light) != 5:
                    return
                light_lvl = int(light[3], 16) * 256 + int(light[2], 16)
                return light_lvl
        print self.name + ' is NOT Connected!'
        return

    def set_trigger(self, value, comparator, topic=None):
        packet_size = 6
        command_id = 178
        payload_size = 4
        module_id = self.id - 1
        command = bytearray([packet_size, command_id, payload_size, self.trigger_id, module_id, comparator, value])
        if topic is None:
            topic = self.default_topic
        if self.is_connected == 1:
            if self.protocol == 'BLE':
                self.BLE.write_to_robo(self.BLE.write_uuid, command)
                return
            if self.protocol == 'MQTT':
                pass
        print self.name + ' is NOT Connected!'
        return

    def triggered(self, cmd_id, cmd_status):
        if self.trigger_id == cmd_id:
            self.trigger_status = cmd_status

    def check_trigger(self):
        value = self.trigger_status
        if value is None:
            return False
        else:
            self.trigger_status = None
            return True