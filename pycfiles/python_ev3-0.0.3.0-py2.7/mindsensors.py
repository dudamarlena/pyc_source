# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-armv5tejl/egg/ev3/mindsensors.py
# Compiled at: 2015-06-06 03:54:19
from .ev3dev import I2CS
from .ev3dev import LegoSensor

class MindSensorI2CS(I2CS):

    @property
    def version(self):
        return self.read_byte_array_as_string(0, 8)

    @property
    def vendor_id(self):
        return self.read_byte_array_as_string(8, 8)

    @property
    def device_id(self):
        return self.read_byte_array_as_string(16, 8)


@I2CS.create_i2c_property(command=(
 65, {'read_only': False}), button_set_1=66, button_set_2=67, x_left=68, y_left=69, x_right=70, y_right=71, up=74, right=75, down=76, left=77, l2=78, r2=79, l1=80, r1=81, triangle=82, circle=83, cross=84, square=85)
class PSPNxV4(MindSensorI2CS):

    def __init__(self, port, addr=1):
        I2CS.__init__(self, port, addr)
        self.command = 73


class AbsoluteIMU(LegoSensor):

    def __init__(self, port=-1):
        LegoSensor.__init__(self, port, name='ms-absolute-imu')
        self._mode = ''

    @property
    def version(self):
        return self.fw_version

    @property
    def compass_cal_start(self):
        self.write_value('command', 'BEGIN-COMP-CAL')

    @property
    def compass_cal_end(self):
        self.write_value('command', 'END-COMP-CAL')

    @property
    def acc_2g(self):
        self.write_value('command', 'ACCEL-2G')

    @property
    def acc_4g(self):
        self.write_value('command', 'ACCEL-4G')

    @property
    def acc_8g(self):
        self.write_value('command', 'ACCEL-8G')

    @property
    def acc_16g(self):
        self.write_value('command', 'ACCEL-16G')

    @property
    def x_acc(self):
        self.mode = 'ACCEL'
        return self.value0

    @property
    def y_acc(self):
        self.mode = 'ACCEL'
        return self.value1

    @property
    def z_acc(self):
        self.mode = 'ACCEL'
        return self.value2

    @property
    def x_tilt(self):
        self.mode = 'TILT'
        return self.value0

    @property
    def y_tilt(self):
        self.mode = 'TILT'
        return self.value1

    @property
    def z_tilt(self):
        self.mode = 'TILT'
        return self.value2

    @property
    def x_raw_magnetic(self):
        self.mode = 'MAG'
        return self.value0

    @property
    def y_raw_magnetic(self):
        self.mode = 'MAG'
        return self.value1

    @property
    def z_raw_magnetic(self):
        self.mode = 'MAG'
        return self.value2

    @property
    def x_gyro(self):
        self.mode = 'GYRO'
        return self.value0

    @property
    def y_gyro(self):
        self.mode = 'GYRO'
        return self.value1

    @property
    def z_gyro(self):
        self.mode = 'COMPASS'
        return self.value0

    @property
    def compass(self):
        self.mode = 'GYRO'
        return self.value2


class MagicWand(MindSensorI2CS):
    val = 255

    def __init__(self, port, addr=56):
        MindSensorI2CS.__init__(self, port, addr)

    def put_data(self, v):
        self.val = v
        MindSensorI2CS.write_byte(self, v)

    def led_all_on(self):
        self.put_data(0)

    def led_all_off(self):
        self.put_data(255)

    def led_on(self, num):
        self.put_data(self.val & 255 - (1 << num - 1))

    def led_off(self, num):
        self.put_data(self.val | 1 << num - 1)