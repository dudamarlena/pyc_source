# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/test/bibliopixel/drivers/serial/devices_test.py
# Compiled at: 2019-08-11 12:22:47
# Size of source mod 2**32: 1945 bytes
import time, unittest
from ...mark_tests import allpixel_test
from bibliopixel.animation.tests import StripChannelTest
from bibliopixel.drivers.channel_order import ChannelOrder
from bibliopixel.drivers.serial import Serial, LEDTYPE
from bibliopixel.drivers.serial.devices import Devices
from bibliopixel.layout.strip import Strip
from bibliopixel.util import log

class DevicesTest(unittest.TestCase):

    @allpixel_test
    def test_serial(self):
        log.setLogLevel(log.DEBUG)
        devs = Devices(hardware_id='1D50:60AB', baudrate=921600)
        log.info('Serial devices:')
        dev_list = devs.find_serial_devices()
        log.info(dev_list)
        first_dev = dev_list[list(dev_list.keys())[0]][0]
        log.info('Default device:')
        log.info(devs.get_device())
        log.info('Device ID for: ' + first_dev)
        old_id = devs.get_device_id(first_dev)
        log.info(old_id)
        log.info('Setting device ID to 42')
        devs.set_device_id(first_dev, 42, baudrate=921600)
        log.info('New Device ID for: ' + first_dev)
        log.info(devs.get_device_id(first_dev))
        log.info('Restoring device ID to ' + str(old_id))
        devs.set_device_id(first_dev, old_id, baudrate=921600)
        log.info('Device version for: ' + first_dev)
        log.info(devs._get_device_version(first_dev))
        driver = Serial((LEDTYPE.APA102),
          600, SPISpeed=4, c_order=(ChannelOrder.RGB))
        layout = Strip(driver)
        for b in range(7, 256, 8):
            log.info('Set brightness ' + str(b))
            layout.set_brightness(b)
            time.sleep(0.25)

        log.info('Run StripChannelTest')
        anim = StripChannelTest(layout)
        anim.run(amt=1, max_steps=8)
        layout.all_off()
        layout.update()
        log.printer('Test Complete!')