# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bibliopixel/drivers/SPI/interfaces.py
# Compiled at: 2019-08-11 12:22:47
# Size of source mod 2**32: 3888 bytes
import os, math
from . import errors
from ...util import log
from ..spi_interfaces import SPI_INTERFACES

class SpiBaseInterface(object):
    __doc__ = ' abstract class for different spi backends'

    def __init__(self, dev, spi_speed):
        self._dev = dev
        self._spi_speed = spi_speed

    def send_packet(self, data):
        """SHOULD BE PRIVATE"""
        raise NotImplementedError

    def compute_packet(self, data):
        """SHOULD BE PRIVATE"""
        return data

    def error(self, text):
        """SHOULD BE PRIVATE"""
        msg = 'Error with dev: {}, spi_speed: {} - {}'.format(self._dev, self._spi_speed, text)
        log.error(msg)
        raise IOError(msg)


class SpiFileInterface(SpiBaseInterface):
    __doc__ = ' using os open/write to send data'

    def __init__(self, **kwargs):
        (super().__init__)(**kwargs)
        if not os.path.exists(self._dev):
            self.error(errors.CANT_FIND_ERROR)
        self._spi = open(self._dev, 'wb')
        log.info('file io spi dev {:s}'.format(self._dev))

    def send_packet(self, data):
        """SHOULD BE PRIVATE"""
        package_size = 4032
        for i in range(int(math.ceil(len(data) / package_size))):
            start = i * package_size
            end = (i + 1) * package_size
            self._spi.write(data[start:end])
            self._spi.flush()


class SpiPeripheryInterface(SpiBaseInterface):
    __doc__ = ' using `python-periphery` to send data'

    def __init__(self, **kwargs):
        (super().__init__)(**kwargs)
        if not os.path.exists(self._dev):
            self.error(errors.CANT_FIND_ERROR)
        try:
            from periphery import SPI
            self._spi = SPI(self._dev, 0, self._spi_speed * 1000000.0)
        except ImportError:
            self.error(errors.CANT_IMPORT_PERIPHERY_ERROR)

        log.info('periphery spi dev {:s} speed @ {:.2f} MHz'.format(self._dev, self._spi.max_speed / 1000000.0))

    def send_packet(self, data):
        """SHOULD BE PRIVATE"""
        package_size = 4032
        for i in range(int(math.ceil(len(data) / package_size))):
            start = i * package_size
            end = (i + 1) * package_size
            self._spi.transfer(data[start:end])


class SpiPyDevInterface(SpiBaseInterface):
    __doc__ = ' using py-spidev to send data'

    def __init__(self, **kwargs):
        (super().__init__)(**kwargs)
        d = self._dev.replace('/dev/spidev', '')
        ids = (int(i) for i in d.split('.'))
        try:
            self._device_id, self._device_cs = ids
        except:
            self.error(errors.BAD_FORMAT_ERROR)

        if not os.path.exists(self._dev):
            self.error(errors.CANT_FIND_ERROR)
        try:
            fd = open(self._dev, 'r')
            fd.close()
        except IOError as e:
            if e.errno == 13:
                self.error(errors.PERMISSION_ERROR)
            else:
                raise e

        try:
            import spidev
            self._spi = spidev.SpiDev()
        except ImportError:
            self.error(errors.CANT_IMPORT_SPIDEV_ERROR)

        self._spi.open(self._device_id, self._device_cs)
        self._spi.max_speed_hz = int(self._spi_speed * 1000000.0)
        log.info('py-spidev dev {:s} speed @ {:.2f} MHz'.format(self._dev, self._spi.max_speed_hz / 1000000.0))

    def send_packet(self, data):
        """SHOULD BE PRIVATE"""
        self._spi.xfer2(list(data))


class SpiDummyInterface(SpiBaseInterface):
    __doc__ = ' interface for testing proposal'

    def send_packet(self, data):
        """ do nothing """
        pass


_SPI_INTERFACES = [
 SpiFileInterface,
 SpiPyDevInterface,
 SpiPeripheryInterface,
 SpiDummyInterface]