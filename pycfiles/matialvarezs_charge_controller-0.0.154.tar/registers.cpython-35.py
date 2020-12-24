# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/matias/Documentos/MIS_MODULOS_PYTHON/matialvarezs_python_modules_creator/backend/apps/matialvarezs_charge_controller/github/registers.py
# Compiled at: 2019-08-09 23:32:13
# Size of source mod 2**32: 3120 bytes
import logging
_logger = logging.getLogger(__name__)

def V():
    return [
     'Voltage', 'V']


def A():
    return [
     'Ampere', 'A']


def AH():
    return [
     'Ampere hours', 'Ah']


def W():
    return [
     'Watt', 'W']


def C():
    return [
     'degree Celsius', '°C']


def PC():
    return [
     '%, percentage', '%']


def KWH():
    return [
     'kWh, kiloWatt/hour', 'kWh']


def Ton():
    return [
     '1000kg', 't']


def MO():
    return [
     'milliohm', 'mOhm']


def I():
    return [
     'integer', '']


def SEC():
    return [
     'seconds', 's']


def MIN():
    return [
     'minutes', 'min']


def HOUR():
    return [
     'hours', 'h']


class Value:
    __doc__ = 'Value with unit'

    def __init__(self, register, value):
        self.register = register
        if self.register.times != 1 and value is not None:
            self.value = 1.0 * value / self.register.times
        else:
            self.value = value

    def __str__(self):
        if self.value is None:
            return self.register.name + ' = ' + str(self.value)
        return self.register.name + ' = ' + str(self.value) + self.register.unit()[1]

    def __float__(self):
        return float(self.value)

    def __int__(self):
        return int(self.value)


class Register:

    def __init__(self, name, address, description, unit, times, size=1, code=''):
        self.name = name
        self.address = address
        self.description = description
        self.unit = unit
        self.times = times
        self.size = size
        self.code = code

    def is_coil(self):
        return self.address < 4096

    def is_discrete_input(self):
        return self.address >= 4096 and self.address < 12288

    def is_input_register(self):
        return self.address >= 12288 and self.address < 36864

    def is_holding_register(self):
        return self.address >= 36864

    def decode(self, response):
        if hasattr(response, 'getRegister'):
            mask = rawvalue = lastvalue = 0
            for i in range(self.size):
                lastvalue = response.getRegister(i)
                rawvalue = rawvalue | lastvalue << i * 16
                mask = mask << 16 | 65535

            if lastvalue & 32768 == 32768:
                rawvalue = -(rawvalue ^ mask) - 1
            return Value(self, rawvalue)
        _logger.info('No value for register ' + repr(self.name))
        return Value(self, None)

    def encode(self, value):
        rawvalue = int(value * self.times)
        if rawvalue < 0:
            rawvalue = -rawvalue - 1 ^ 65535
        return rawvalue


class Coil(Register):

    def decode(self, response):
        if hasattr(response, 'bits'):
            return Value(self, response.bits[0])
        _logger.info('No value for coil ' + repr(self.name))
        return Value(self, None)