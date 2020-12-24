# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/test/bibliopixel/project/types/spi_interface_test.py
# Compiled at: 2019-08-11 12:22:47
# Size of source mod 2**32: 487 bytes
from .base import TypesBaseTest
from bibliopixel.drivers.SPI.interfaces import SPI_INTERFACES

class SpiInterfaceTypesTest(TypesBaseTest):

    def test_some(self):
        self.make('spi_interface', 'FILE')
        self.make('spi_interface', 'DUMMY')
        self.make('spi_interface', SPI_INTERFACES.PYDEV)
        with self.assertRaises(ValueError):
            self.make('spi_interface', 7)
        with self.assertRaises(KeyError):
            self.make('spi_interface', 'NONE')