# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/johnny/workspaces/lazerball/src/python3.4env/lib/python3.4/site-packages/htdataredirector/units/rfd21733/reader.py
# Compiled at: 2014-10-26 05:07:41
# Size of source mod 2**32: 1840 bytes
from binascii import hexlify
from ...utils import millis
from .registry import Registry

class Reader:
    DEBOUNCE_DELAY = 200
    BUTTON_ZONE_MAP = {'10': 1, 
     '20': 2, 
     '40': 3}
    found_first_packet = False

    def __init__(self, io_dev):
        self.io_dev = io_dev
        self.last_hit = ''

    def __iter__(self):
        registry = Registry()
        self.unit_registry = registry.all()
        return self

    def __next__(self):
        if not self.found_first_packet:
            data = self.find_start()
            self.found_first_packet = True
        else:
            debounce_time = millis()
            data = ''
            while 1:
                data = self.read_ascii(5)
                if data != self.last_hit or not self.bouncing(debounce_time):
                    break

        self.last_hit = data
        return self.parse(data)

    def find_start(self):
        while not self.found_first_packet:
            button = self.read_ascii(1)
            if button in self.BUTTON_ZONE_MAP:
                esn = self.read_ascii(4)
                if esn in self.unit_registry or not self.unit_registry:
                    self.found_first_packet = True
                    return button + esn
                continue

    def read_ascii(self, size):
        data = self.io_dev.read(size)
        return hexlify(data).decode('ascii')

    def parse(self, data):
        zone = None
        if data[0:2] in self.BUTTON_ZONE_MAP:
            zone = self.BUTTON_ZONE_MAP[data[0:2]]
        return {'radioId': data[2:], 
         'zone': zone}

    def bouncing(self, debounce_time):
        return millis() - debounce_time < self.DEBOUNCE_DELAY