# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/snakeflake/config.py
# Compiled at: 2020-03-28 09:43:41
# Size of source mod 2**32: 1560 bytes
"""
.. module:: config

Snakeflake Configuration

This module defines the classes related to configuring a Snakeflake generator.
"""
import datetime
from snakeflake.utils import get_ip, ipv4_to_int, world_epoch

class SnakeflakeConstants:
    __doc__ = '\n    The Snakeflake Config class that deals with constants\n    \n    The default values were taken from https://github.com/sony/sonyflake.\n\n    You can change them to suit your needs if you need to, I suppose.\n    '

    def __init__(self, timestamp_bits, timescale, serial_bits, machine_id_bits):
        self.timestamp_bits = timestamp_bits
        self.timescale = timescale
        self.serial_bits = serial_bits
        self.machine_id_bits = machine_id_bits

    @classmethod
    def defaults(cls):
        return cls(39, 10000, 8, 16)


class SnakeflakeGeneratorConfig:
    __doc__ = 'The Snakeflake Generator Config class'

    def __init__(self, epoch: datetime.datetime=None, machine_id: int=None, constants: SnakeflakeConstants=None, timestamp_method=None):
        if epoch == None:
            epoch = world_epoch()
        if constants == None:
            constants = SnakeflakeConstants.defaults()
        if machine_id == None:
            machine_id = ipv4_to_int(get_ip(), constants.machine_id_bits)
        if timestamp_method == None:
            timestamp_method = datetime.datetime.utcnow
        self.epoch = epoch
        self.machine_id = machine_id
        self.constants = constants
        self.timestamp_method = timestamp_method