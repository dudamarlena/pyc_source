# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bibliopixel/drivers/SPI/errors.py
# Compiled at: 2019-08-11 12:22:47
# Size of source mod 2**32: 749 bytes
PERMISSION_ERROR = 'Cannot access SPI device.\nPlease see\n\n    https://github.com/maniacallabs/bibliopixel/wiki/SPI-Setup\n\nfor details.\n'
CANT_FIND_ERROR = 'Cannot find SPI device.\nPlease see\n\n    https://github.com/maniacallabs/bibliopixel/wiki/SPI-Setup\n\nfor details.\n'
CANT_IMPORT_PERIPHERY_ERROR = '\nUnable to import periphery. Please install:\n    pip install python-periphery\n\nPlease see\n    https://github.com/maniacallabs/bibliopixel/wiki/SPI-Setup\n\nfor details.\n'
BAD_FORMAT_ERROR = '\nWhen using py-spidev, `dev` must be in the format /dev/spidev*.*\nPlease see https://github.com/maniacallabs/bibliopixel/wiki/SPI-Setup\n'
CANT_IMPORT_SPIDEV_ERROR = '\nUnable to import spidev. Please install:\n\n    pip install spidev\n'