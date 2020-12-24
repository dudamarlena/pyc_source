# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/snakeflake/snakeflake.py
# Compiled at: 2020-03-28 09:58:23
# Size of source mod 2**32: 9184 bytes
"""
.. module:: snakeflake

Snakeflake Main Class

This module defines the Snakeflake Generator and Snakeflake classes.
"""
from snakeflake import config, exceptions, utils
import datetime, math

class SnakeflakeGenerator:
    __doc__ = 'The Snakeflake generator.\n    \n    This class allows one to generate snakeflakes quickly and easily\n    after initializing. It also manages serial number incrementing.\n\n    Attributes:\n        :var constants config.SnakeflakeGeneratorConfig:\n        :ivar epoch datetime.datetime:\n        :ivar machine_id int:\n        :ivar timestamp_method builtin_function_or_method:\n        :ivar serial int:\n    '

    def __init__(self, genconfig: config.SnakeflakeGeneratorConfig):
        """
        Args:
            genconfig: The config to initialize the generator.
        
        Raises:
            exceptions.ExceededBitsException: If the machine ID exceeds the number of bits allocated.
        """
        self.constants = genconfig.constants
        self.epoch = genconfig.epoch
        self.machine_id = genconfig.machine_id
        self.timestamp_method = genconfig.timestamp_method
        self.serial = 0
        if self.machine_id > 2 ** self.constants.machine_id_bits:
            raise exceptions.ExceededBitsException(utils.format_error(self.machine_id, 'The machine ID exceeds the number of bits allocated.'))
            return

    def next_snakeflake(self):
        """Returns the next snakeflake as an object and increments the serial.
        
        Returns:
            Snakeflake: The snakeflake object
        
        Raises:
            exceptions.ExceededTimeException: If too much time has passed to be able to generate a snakeflake.
            exceptions.EpochFutureException: If the epoch is in the future.
        """
        now = self.timestamp_method()
        ret = Snakeflake.from_generator(now, self)
        ret.calculate_snakeflake()
        self.serial += 1
        return ret

    def next_id(self):
        """Calls :meth:`next_snakeflake` and returns the next snakeflake ID.
        
        Returns:
            int: The snakeflake ID.
        
        Raises:
            exceptions.ExceededTimeException: If too much time has passed to be able to generate a snakeflake.
            exceptions.EpochFutureException: If the epoch is in the future.
        """
        return self.next_snakeflake().get_id()


class Snakeflake:
    __doc__ = 'Defines a snakeflake\n    \n    This class holds the attributes of a snakeflake and\n    calculates the actual snakeflake ID.\n\n    Attributes:\n        :ivar timestamp datetime.datetime:\n        :ivar serial int:\n        :ivar machine_id int:\n        :ivar epoch datetime.datetime:\n        :ivar constants config.SnakeflakeGeneratorConfig:\n        :ivar snakeflake_id int:\n    '

    def __init__(self, timestamp: datetime.datetime, serial: int, machine_id: int, epoch: datetime.datetime=None, constants: config.SnakeflakeConstants=None, snakeflake_id: int=None):
        """
        Please try to use the :meth:`classmethods <from_generator>` to generate snakeflakes instead.

        Args:
            timestamp: The timestamp of the snakeflake.
            serial: The serial number of the snakeflake.
            machine_id: The machine ID of the snakeflake.
            epoch: When this snakeflake started counting from.
            constants: The constants this snakeflake uses.
            snakeflake_id: The ID of this snakeflake.
                This should only be specified if you are deriving information from a snakeflake ID.
        """
        self.timestamp = timestamp
        self.serial = serial
        self.machine_id = machine_id
        if epoch == None:
            epoch = utils.world_epoch()
        self.epoch = epoch
        if constants == None:
            constants = config.SnakeflakeConstants.defaults()
        self.constants = constants
        self.snakeflake_id = snakeflake_id

    def __eq__(self, other):
        return abs(utils.timestamp_to_microseconds(self.timestamp) - utils.timestamp_to_microseconds(other.timestamp)) <= self.constants.timescale and self.serial == other.serial and self.machine_id == other.machine_id and self.snakeflake_id == other.snakeflake_id

    def __ne__(self, other):
        return not self.__eq__(other)

    @classmethod
    def from_generator(cls, timestamp: datetime.datetime, generator: SnakeflakeGenerator):
        """
        Generates a snakeflake using data from the generator object.
        Note that this will not increment the serial number of the generator itself.
        Please instead generate snakeflakes from the :class:`SnakeflakeGenerator` directly for this functionality.

        The snakeflake ID itself will not be calculated until :meth:`calculate_snakeflake` is run.

        Args:
            timestamp: The timestamp of the snakeflake.
            generator: The generator with the data that will be used to generate the snakeflake.
        """
        return cls(timestamp, generator.serial, generator.machine_id, generator.epoch, generator.constants, None)

    @classmethod
    def from_snakeflake(cls, snakeflake_id: int, epoch: datetime.datetime=None, constants: config.SnakeflakeConstants=None):
        """
        Generates a snakeflake from a snakeflake ID. This is usually
        used for reverse-engineering the timestamp of a snakeflake,
        although the serial and machine IDs will also be calculated.

        Note that the resulting attributes will not be calculated until
        :meth:`reverse_calculate_snakeflake` is run.

        Args:
            snakeflake_id: The snakeflake.
            epoch: When this snakeflake started counting from.
            constants: The constants this snakeflake uses.
        """
        return cls(None, None, None, epoch, constants, snakeflake_id)

    def calculate_snakeflake(self):
        """Calculates a snakeflake.
        
        This method calculates and updates the :ivar:`snakeflake_id` attribute
        based on the :ivar:`timestamp`, :ivar:`serial`, and :ivar:`machine_id`
        attributes set upon initialization.
        """
        timestamp = self.timestamp - self.epoch
        timestamp /= datetime.timedelta(microseconds=1)
        timestamp /= self.constants.timescale
        timestamp = math.floor(timestamp)
        if timestamp < 0:
            raise exceptions.EpochFutureException(utils.format_error(self.machine_id, 'The epoch is in the future.'))
            return
        if timestamp > 2 ** self.constants.timestamp_bits:
            raise exceptions.ExceededTimeException(utils.format_error(self.machine_id, 'Too much time has passed from the epoch to be able to generate a snakeflake.'))
            return
        new_snakeflake = 0
        snakeflake_builder_components = [
         (
          timestamp, self.constants.serial_bits),
         (
          self.serial, self.constants.machine_id_bits),
         (
          self.machine_id, 0)]
        for value, bitcount in snakeflake_builder_components:
            new_snakeflake += value
            new_snakeflake = new_snakeflake << bitcount

        self.serial = (self.serial + 1) % 2 ** self.constants.serial_bits
        self.snakeflake_id = new_snakeflake

    def reverse_calculate_snakeflake(self):
        """
        Calculates and updates the snakeflake's attributes from the
        :ivar:`ID <snakeflake_id>`.
        Typically used with the :meth:`from_snakeflake` classmethod.
        """
        snakeflake_component_lengths = (
         self.constants.machine_id_bits,
         self.constants.serial_bits,
         self.constants.timestamp_bits)
        w_snakeflake = self.snakeflake_id
        res = []
        for b in snakeflake_component_lengths:
            res += [w_snakeflake & utils.bitfill(b)]
            w_snakeflake = w_snakeflake >> b

        self.machine_id, self.serial, timestamp = res
        timestamp *= self.constants.timescale
        timestamp = datetime.timedelta(microseconds=timestamp)
        self.timestamp = self.epoch + timestamp

    def calculate(self):
        """A generic "smart" calculation method that runs either
        :meth:`calculate_snakeflake` or :meth:`reverse_calculate_snakeflake`
        depending on the current attributes set."""
        if self.snakeflake_id == None:
            self.calculate_snakeflake()
        else:
            self.reverse_calculate_snakeflake()

    def get_id(self):
        """
        Returns:
            int: The snakeflake ID
        """
        return self.snakeflake_id