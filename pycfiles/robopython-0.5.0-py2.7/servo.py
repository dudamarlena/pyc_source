# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\robopython\robo\servo.py
# Compiled at: 2020-03-04 11:05:03


class Servo(object):

    def __init__(self, name, ble, mqtt, protocol, default_topic, id_num, action_id):
        self.is_connected = 0
        self.name = name
        self.id = id_num
        self.action_id = action_id
        self.action_status = None
        self.BLE = ble
        self.MQTT = mqtt
        self.protocol = protocol
        self.default_topic = default_topic
        return

    def connected(self):
        self.is_connected = 1
        print 'Servo' + str(self.id) + ' connected'

    def disconnected(self):
        self.is_connected = 0
        print 'Servo' + str(self.id) + ' disconnected'

    def set_angle(self, angle, topic=None):
        assert type(angle) is int, 'Angle must be an integer'
        packet_size = 6
        command_id = 161
        payload_size = 4
        module_id = self.id - 1
        angleH = angle / 256
        angleL = angle % 256
        command = bytearray([packet_size, command_id, payload_size, self.action_id, module_id, angleH, angleL])
        if topic is None:
            topic = self.default_topic
        if angle < 0 or angle > 355:
            print 'Angle must be between 0-355'
            return
        else:
            if self.is_connected == 1:
                if self.protocol == 'BLE':
                    self.BLE.write_to_robo(self.BLE.write_uuid, command)
                    return
                if self.protocol == 'MQTT':
                    command = self.MQTT.get_mqtt_cmd([command_id, payload_size, module_id, angle])
                    self.MQTT.publish(topic, command)
                    return
            print self.name + ' is NOT Connected!'
            return

    def get_encoder(self):
        pass

    def action_complete(self, id, cmd_status):
        self.action_status = cmd_status

    def check_action(self):
        value = self.action_status
        if self.action_status is None:
            return False
        else:
            self.action_status = None
            return True