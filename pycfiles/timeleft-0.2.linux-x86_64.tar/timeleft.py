# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/sauser/anaconda2/lib/python2.7/site-packages/timeleft/timeleft.py
# Compiled at: 2016-04-24 12:47:17
"""
Program to tell you how much time is left on a download.  Simply call the program with two arguments making sure
to include the units for both file size and download speed.

Accounts for conversion between bits and bytes.

Examples:
    $ timeleft 100MB 100MBps
    1.0 second
    $ timeleft 100MB 100mbps
    8.0 seconds
    $ timeleft 100MB 100mb/s
    8.0 seconds
    $ timeleft 100MB 1kbps
    9.0 days, 11.0 hours, 33.0 minutes, 20.0 seconds
    $ 3.4GB 3.4MBps
    17.0 minutes, 4.0 seconds
    $ timeleft 1.5YB 10gbps
    28561641.0 years, 172.0 days, 10.0 hours, 21.0 minutes, 39.25 seconds
    $ timeleft 100GB 100GBPS
    1.0 second

"""
from __future__ import print_function
import sys, re, logging
SPEED = 'speed'
SIZE = 'size'
BASE_UNIT = 1024
PREFIXES = {'b': 1, 
   'B': 8, 
   'K': BASE_UNIT, 
   'M': BASE_UNIT ** 2, 
   'G': BASE_UNIT ** 3, 
   'T': BASE_UNIT ** 4, 
   'P': BASE_UNIT ** 5, 
   'E': BASE_UNIT ** 6, 
   'Z': BASE_UNIT ** 7, 
   'Y': BASE_UNIT ** 8}
logFormatter = logging.Formatter('%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s')
rootLogger = logging.getLogger()
consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logFormatter)
rootLogger.addHandler(consoleHandler)
rootLogger.setLevel(logging.ERROR)

class Measurement:
    """
    Class to handle parsing of speed and size units. Creation of an object automatically parses the input text.
    Raises RuntimeError on unknown unit type or improperly formatted input text.
    """

    def __init__(self, arg):
        rootLogger.log(logging.DEBUG, 'Creating measurement for: "' + arg + '"')
        self.arg = arg
        match = re.search('(\\d+\\.?\\d*)([a-zA-Z/]+)', arg)
        if match is not None:
            self.number = float(match.group(1))
            self.unit = match.group(2)
            rootLogger.log(logging.DEBUG, 'Number is: ' + str(self.number) + ' unit is: ' + self.unit)
            self.base_amount = self._get_base_value(self.unit)
        else:
            raise RuntimeError('"' + arg + '" is not a valid number + unit of measure!')
        return

    def __repr__(self):
        return '{Number: ' + str(self.number) + ', Unit: ' + self.unit + '}'

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.get_type() == other.get_type() and self.get_base_amount() == other.get_base_amount()

    def __ne__(self, other):
        return not self.__eq__(other)

    def get_type(self):
        """
        Return the type of unit of measure (currently only speed and size)
        """
        if '/' in self.unit:
            return SPEED
        else:
            if 'ps' in self.unit.lower():
                return SPEED
            return SIZE

    def get_base_amount(self):
        """
        Return this measurement's value in base units
        e.g., 3 kilobits (using binary notation) = 3 * 1024 = 3072 bits

        For size, this is bits.
        For speed, this is bits per second
        """
        base_value = self._get_base_value(self.unit)
        base_amount = float(base_value) * self.number
        rootLogger.log(logging.DEBUG, 'Base amount for measurement: "' + self.arg + '" is: ' + str(base_amount))
        return base_amount

    @staticmethod
    def _get_prefix_multiplier(prefix):
        if prefix in PREFIXES:
            return PREFIXES[prefix]
        if prefix.upper() in PREFIXES:
            return PREFIXES[prefix.upper()]
        raise RuntimeError('"' + prefix + '" is not a known unit prefix!')

    def _get_base_value(self, unit):
        match = re.search('^([a-zA-Z]+)(?:/|ps|PS|pS|Ps)', unit)
        if match is not None:
            relevant_unit = match.group(1)
        else:
            relevant_unit = unit
        base_amount = 1.0
        rootLogger.log(logging.DEBUG, 'Relevant unit for "' + unit + '" is "' + relevant_unit + '"')
        for character in relevant_unit:
            base_amount *= self._get_prefix_multiplier(character)

        return base_amount


def get_measurements(args):
    """
    Return the measurements derived from the input args

    Input must be properly formatted i.e., an array of length two with one speed measurement and one size measurement.

    :param args: A properly formatted array of string arguments
    :return: A list of parsed measurements.
    """
    if len(args) != 2:
        raise RuntimeError('Must have exactly 2 arguments!')
    else:
        return [ Measurement(arg) for arg in args ]


def get_duration_seconds(measurements):
    """
    Return the number of seconds it takes to process a certain amount of data with a given rate of production.

    Generally used to calculate the amount of time to download a file (Bytes) using bandwidth (Bytes per second).

    Example:
    get_duration_seconds(['2GB', '1GB/s']) returns 2 (seconds)

    :param measurements: An iterable of parsed measurements.
    :return: The number of seconds to process a certain amount of data with a given rate of production
    """
    size = 0
    speed = 0
    for measurement in measurements:
        base_value = measurement.get_base_amount()
        if measurement.get_type() == SPEED:
            speed = base_value
        elif measurement.get_type() == SIZE:
            size = base_value
        else:
            raise RuntimeError('Must have a size unit and a speed unit!')

    if speed != 0 and size != 0:
        rootLogger.log(logging.DEBUG, 'Size: ' + str(size) + ' Speed: ' + str(speed))
        return float(size) / speed
    raise RuntimeError('Must have valid size and speed measurements!')


def get_human_time(seconds):
    """
    Return a string of human-readable time

    :param seconds: Seconds of time
    :return: String of human-readable time
    """
    if seconds < 1:
        return ('{0:.2f}').format(seconds) + ' seconds'
    years, remainder = divmod(seconds, 31536000)
    days, remainder = divmod(remainder, 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, seconds = divmod(remainder, 60)
    text = ''
    time_units = ['years', 'days', 'hours', 'minutes', 'second']
    time_amounts = [years, days, hours, minutes, seconds]
    for i in range(0, len(time_units)):
        time_amount = time_amounts[i]
        if time_amount > 0:
            label = time_units[i]
            text += ', ' + str(time_amount) + ' ' + label
            if time_units[i] == 'second' and time_amount != 1.0:
                text += 's'

    text = text.strip(', ')
    return text


def main():
    rootLogger.log(logging.INFO, 'Starting main.')
    try:
        args = sys.argv[1:]
        measurements = get_measurements(args)
        seconds = get_duration_seconds(measurements)
        print(get_human_time(seconds))
        rootLogger.log(logging.INFO, 'Execution Complete!')
    except RuntimeError as e:
        rootLogger.log(logging.ERROR, 'RuntimeError: ' + str(e))


if __name__ == '__main__':
    main()