# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\robopython\robo\display.py
# Compiled at: 2020-03-04 11:05:06
from binascii import hexlify
import time

class Display(object):

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
        print 'Display' + str(self.id) + ' connected'

    def disconnected(self):
        self.is_connected = 0
        print 'Display' + str(self.id) + ' disconnected'

    def action_complete(self, cmd_id, cmd_status):
        self.action_status = cmd_status

    def check_action(self):
        value = self.action_status
        if value is None:
            return False
        else:
            self.action_status = None
            print 'Display Action Completed'
            return True

    def animate(self, animation_num, repeats, reverse, orientation, num_frames=0, frame_rateH=0, frame_rateL=0):
        command_id = 84
        packet_size = 10
        payload_size = 8
        command = bytearray([packet_size, command_id, payload_size, self.action_id, self.id - 1, animation_num, repeats, reverse, orientation, num_frames, frame_rateH, frame_rateL])
        self.BLE.write_to_robo(self.BLE.write_uuid, command)

    def image(self, image_num, orientation, delay):
        command_id = 88
        packet_size = 8
        payload_size = 6
        delay_H = delay / 256
        delay_L = delay % 256
        command = bytearray([packet_size, command_id, payload_size, self.action_id, self.id - 1, image_num, orientation, delay_H, delay_L])
        self.BLE.write_to_robo(self.BLE.write_uuid, command)

    def custom_image(self, image, orientation, delay):
        self.reset()
        command_id = 87
        packet_size = 19
        payload_size = 17
        rows1 = image[:16]
        rows2 = image[16:]
        byte1 = (self.id - 1 << 2) + 0
        byte2 = (self.id - 1 << 2) + 1
        command1 = [
         packet_size, command_id, payload_size, byte1]
        command1.extend(rows1)
        command1 = bytearray(command1)
        command2 = [packet_size, command_id, payload_size, byte2]
        command2.extend(rows2)
        command2 = bytearray(command2)
        self.BLE.write_to_robo(self.BLE.write_uuid, command1)
        self.BLE.write_to_robo(self.BLE.write_uuid, command2)
        self.image(255, orientation, delay)

    def custom_animation(self, animation, repeats, reverse, orientation, frame_rate):
        self.reset()
        command_id = 85
        packet_size = 19
        payload_size = 17
        frame_rateH = frame_rate / 256
        frame_rateL = frame_rate % 256
        length = len(animation)
        if length > 5 or length < 0:
            return
        for num, frame in enumerate(animation):
            rows1 = frame[:16]
            rows2 = frame[16:]
            byte1 = num << 3 | self.id - 1 << 1 | 0
            byte2 = num << 3 | self.id - 1 << 1 | 1
            command1 = [
             packet_size, command_id, payload_size, byte1]
            command1.extend(rows1)
            command1 = bytearray(command1)
            command2 = [packet_size, command_id, payload_size, byte2]
            command2.extend(rows2)
            command2 = bytearray(command2)
            self.BLE.write_to_robo(self.BLE.write_uuid, command1)
            self.BLE.write_to_robo(self.BLE.write_uuid, command2)

        self.animate(255, repeats, reverse, orientation, length, frame_rateH, frame_rateL)

    def reset(self):
        command_id = 90
        packet_size = 3
        payload_size = 1
        command = [
         packet_size, command_id, payload_size, self.id - 1]
        self.BLE.write_to_robo(self.BLE.write_uuid, command)

    def load_text(self, text_block, index):
        length = len(text_block)
        if length > 14:
            return
        command_id = 86
        packet_size = 5 + length
        payload_size = packet_size - 2
        command = [
         packet_size, command_id, payload_size, self.id - 1, index, length]
        command.extend(text_block)
        self.BLE.write_to_robo(self.BLE.write_uuid, command)

    def print_text(self, text_string, scroll_rate, orientation=0):
        self.reset()
        length = len(text_string)
        text_block = []
        command_id = 89
        packet_size = 8
        payload_size = 6
        scroll_rateH = scroll_rate / 256
        scroll_rateL = scroll_rate % 256
        text_payload = []
        chars = []
        count = 0
        findex = 0
        block_size = 14
        for index, char in enumerate(text_string):
            if count == block_size:
                self.load_text(text_payload, findex)
                text_payload = []
                chars = []
                findex += block_size
                count = 0
            text_payload.append(ord(char))
            chars.append(char)
            count += 1

        if text_payload:
            self.load_text(text_payload, findex)
        command = [packet_size, command_id, payload_size, self.action_id, self.id - 1, orientation, length, scroll_rateH, scroll_rateL]
        self.BLE.write_to_robo(self.BLE.write_uuid, command)