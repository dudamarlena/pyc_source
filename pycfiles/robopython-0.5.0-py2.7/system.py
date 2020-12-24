# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\robopython\robo\system.py
# Compiled at: 2020-03-04 11:05:03
from binascii import hexlify

class System(object):

    def __init__(self, name, ble, mqtt, protocol, default_topic, action_id):
        self.is_connected = 1
        self.name = name
        self.chargeLevel = 0
        self.chargeStatus = 'Unknown'
        self.firmwareVersion = None
        self.robotSound = 0
        self.cheerSound = 1
        self.honkSound = 2
        self.catSound = 3
        self.alarmSound = 4
        self.dogSound = 5
        self.laserSound = 6
        self.dingSound = 7
        self.sounds = [self.robotSound, self.cheerSound, self.honkSound, self.catSound, self.alarmSound, self.dogSound,
         self.laserSound, self.dingSound]
        self.action_id = action_id
        self.action_status = None
        self.BLE = ble
        self.MQTT = mqtt
        self.protocol = protocol
        self.default_topic = default_topic
        return

    def connected(self):
        self.is_connected = 1

    def disconnected(self):
        self.is_connected = 0

    def get_battery_stats(self, topic=None):
        status_options = ['Unknown', 'Discharging', 'Charging', 'Full']
        packet_size = 2
        command_id = 16
        payload = 0
        if topic is None:
            topic = self.default_topic
        if self.protocol == 'BLE':
            self.BLE.write_to_robo(self.BLE.write_uuid, bytearray([packet_size, command_id, payload]))
            charge_data = hexlify(self.BLE.read_from_robo())
            charge_data = [ charge_data[i:i + 2] for i in xrange(0, len(charge_data), 2) ]
            if len(charge_data) == 4:
                self.chargeLevel = int(charge_data[(-2)], 16)
                self.chargeStatus = int(charge_data[(-1)], 16)
                if self.chargeStatus <= 3:
                    self.chargeStatus = status_options[self.chargeStatus]
            return [
             self.chargeLevel, self.chargeStatus]
        else:
            if self.protocol == 'MQTT':
                command = self.MQTT.get_mqtt_cmd([command_id, payload])
                self.MQTT.publish(topic, command)
                charge_data = self.MQTT.message
                if charge_data is None:
                    return
                charge_data = [ charge_data[i:i + 2] for i in xrange(0, len(charge_data), 2) ]
                self.chargeLevel = int(charge_data[(-2)], 16)
                self.chargeStatus = int(charge_data[(-1)], 16)
                if self.chargeLevel > 100:
                    self.chargeLevel = 100
                if self.chargeStatus <= 3:
                    self.chargeStatus = status_options[self.chargeStatus]
                return [self.chargeLevel, self.chargeStatus]
            return

    def get_firmware_version(self, topic=None):
        packet_size = 2
        command_id = 7
        payload = 0
        if topic is None:
            topic = self.default_topic
        if self.protocol == 'BLE':
            self.BLE.write_to_robo(self.BLE.write_uuid, bytearray([packet_size, command_id, payload]))
            fw_data = hexlify(self.BLE.read_from_robo())
            fw_data = [ fw_data[i:i + 2] for i in xrange(0, len(fw_data), 2) ]
            return fw_data
        else:
            if self.protocol == 'MQTT':
                command = self.MQTT.get_mqtt_cmd([command_id, payload])
                self.MQTT.publish(topic, command)
                fw_data = self.MQTT.message
                if fw_data is None:
                    return
                fw_data = [ int(fw_data[i:i + 2], 16) for i in xrange(0, len(fw_data), 2) ]
                fw_data = fw_data[2:]
                FW_Version = ('').join(chr(i) for i in fw_data)
                return FW_Version
            return

    def get_sound_clips(self, topic=None):
        packet_size = 2
        command_id = 96
        payload = 0
        if topic is None:
            topic = self.default_topic
        if self.protocol == 'BLE':
            self.BLE.write_to_robo(self.BLE.write_uuid, bytearray([packet_size, command_id, payload]))
            clip_data = hexlify(self.BLE.read_from_robo())
            clip_data = [ clip_data[i:i + 2] for i in xrange(0, len(clip_data), 2) ]
            return clip_data
        else:
            if self.protocol == 'MQTT':
                command = self.MQTT.get_mqtt_cmd([command_id, payload])
                self.MQTT.publish(topic, command)
                clips_data = self.MQTT.message
                if clips_data is None:
                    return
                clips_data = [ clips_data[i:i + 2] for i in xrange(0, len(clips_data), 2) ]
                return clips_data
            return

    def play_sound(self, sound, topic=None):
        packet_size = 3
        command_id = 97
        payload_size = 1
        if topic is None:
            topic = self.default_topic
        if self.protocol == 'BLE':
            self.BLE.write_to_robo(self.BLE.write_uuid, bytearray([packet_size, command_id, payload_size, sound]))
            return
        else:
            if self.protocol == 'MQTT':
                command = self.MQTT.get_mqtt_cmd([command_id, payload_size, sound])
                self.MQTT.publish(topic, command)
                return
            return

    def set_tune(self, tune, tempo, topic=None):
        packet_size = 4
        command_id = 146
        payload_size = 2
        if topic is None:
            topic = self.default_topic
        if self.protocol == 'BLE':
            self.BLE.write_to_robo(self.BLE.write_uuid, bytearray([packet_size, command_id, payload_size, tune, tempo]))
            return
        else:
            if self.protocol == 'MQTT':
                command = self.MQTT.get_mqtt_cmd([command_id, payload_size, tune, tempo])
                self.MQTT.publish(topic, command)
                return
            return

    def upload_custom_tune(self, tune, index, topic=None):
        length = len(tune)
        MAX_TUNE_SIZE = 240
        if length > MAX_TUNE_SIZE:
            print 'The length of this tune is larger than the limit of: ' + str(MAX_TUNE_SIZE) + ' notes'
            return
        else:
            packet_size = length + 3
            command_id = 147
            payload_size = length + 1
            if topic is None:
                topic = self.default_topic
            if self.protocol == 'BLE':
                payload = [
                 packet_size, command_id, payload_size, index]
                for i in range(0, length):
                    payload.append(tune[i])

                self.BLE.write_to_robo(self.BLE.write_uuid, bytearray(payload))
                return
            if self.protocol == 'MQTT':
                payload = [
                 command_id, payload_size, index]
                for i in range(0, length):
                    payload.append(tune[i])

                command = self.MQTT.get_mqtt_cmd(payload)
                self.MQTT.publish(topic, command)
                return
            return

    def kill_tune(self):
        self.set_tune(240, 0)

    def play_custom_tune(self, tempo):
        self.set_tune(255, tempo)

    def play_note(self, note, beat, tempo, topic=None):
        packet_size = 3
        command_id = 148
        payload_size = 2
        r = range(0, 16)
        if beat not in r or note not in r:
            print 'Beat and/or Note is out of range'
            return
        else:
            beat = 15
            note = (note << 4) + beat
            if topic is None:
                topic = self.default_topic
            if self.protocol == 'BLE':
                self.BLE.write_to_robo(self.BLE.write_uuid, bytearray([packet_size, command_id, payload_size, note, tempo]))
                return
            if self.protocol == 'MQTT':
                command = self.MQTT.get_mqtt_cmd([command_id, payload_size, note, tempo])
                self.MQTT.publish(topic, command)
                return
            return

    def action_complete(self, id, cmd_status):
        self.action_status = cmd_status

    def check_action(self):
        value = self.action_status
        if self.action_status is None:
            return False
        else:
            self.action_status = None
            return True