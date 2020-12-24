# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-armv7l/egg/PI_INFO_SENDER/Adafruit_BME280.py
# Compiled at: 2016-09-01 23:01:42
import logging, time
BME280_I2CADDR = 119
BME280_OSAMPLE_1 = 1
BME280_OSAMPLE_2 = 2
BME280_OSAMPLE_4 = 3
BME280_OSAMPLE_8 = 4
BME280_OSAMPLE_16 = 5
BME280_REGISTER_DIG_T1 = 136
BME280_REGISTER_DIG_T2 = 138
BME280_REGISTER_DIG_T3 = 140
BME280_REGISTER_DIG_P1 = 142
BME280_REGISTER_DIG_P2 = 144
BME280_REGISTER_DIG_P3 = 146
BME280_REGISTER_DIG_P4 = 148
BME280_REGISTER_DIG_P5 = 150
BME280_REGISTER_DIG_P6 = 152
BME280_REGISTER_DIG_P7 = 154
BME280_REGISTER_DIG_P8 = 156
BME280_REGISTER_DIG_P9 = 158
BME280_REGISTER_DIG_H1 = 161
BME280_REGISTER_DIG_H2 = 225
BME280_REGISTER_DIG_H3 = 227
BME280_REGISTER_DIG_H4 = 228
BME280_REGISTER_DIG_H5 = 229
BME280_REGISTER_DIG_H6 = 230
BME280_REGISTER_DIG_H7 = 231
BME280_REGISTER_CHIPID = 208
BME280_REGISTER_VERSION = 209
BME280_REGISTER_SOFTRESET = 224
BME280_REGISTER_CONTROL_HUM = 242
BME280_REGISTER_CONTROL = 244
BME280_REGISTER_CONFIG = 245
BME280_REGISTER_PRESSURE_DATA = 247
BME280_REGISTER_TEMP_DATA = 250
BME280_REGISTER_HUMIDITY_DATA = 253

class BME280(object):

    def __init__(self, mode=BME280_OSAMPLE_1, address=BME280_I2CADDR, i2c=None, **kwargs):
        self._logger = logging.getLogger('Adafruit_BMP.BMP085')
        if mode not in [BME280_OSAMPLE_1, BME280_OSAMPLE_2, BME280_OSAMPLE_4,
         BME280_OSAMPLE_8, BME280_OSAMPLE_16]:
            raise ValueError(('Unexpected mode value {0}.  Set mode to one of BME280_ULTRALOWPOWER, BME280_STANDARD, BME280_HIGHRES, or BME280_ULTRAHIGHRES').format(mode))
        self._mode = mode
        if i2c is None:
            import Adafruit_GPIO.I2C as I2C
            i2c = I2C
        self._device = i2c.get_i2c_device(address, **kwargs)
        self._load_calibration()
        self._device.write8(BME280_REGISTER_CONTROL, 63)
        self.t_fine = 0.0
        return

    def _load_calibration(self):
        self.dig_T1 = self._device.readS16LE(BME280_REGISTER_DIG_T1)
        self.dig_T2 = self._device.readS16LE(BME280_REGISTER_DIG_T2)
        self.dig_T3 = self._device.readS16LE(BME280_REGISTER_DIG_T3)
        self.dig_P1 = self._device.readU16LE(BME280_REGISTER_DIG_P1)
        self.dig_P2 = self._device.readS16LE(BME280_REGISTER_DIG_P2)
        self.dig_P3 = self._device.readS16LE(BME280_REGISTER_DIG_P3)
        self.dig_P4 = self._device.readS16LE(BME280_REGISTER_DIG_P4)
        self.dig_P5 = self._device.readS16LE(BME280_REGISTER_DIG_P5)
        self.dig_P6 = self._device.readS16LE(BME280_REGISTER_DIG_P6)
        self.dig_P7 = self._device.readS16LE(BME280_REGISTER_DIG_P7)
        self.dig_P8 = self._device.readS16LE(BME280_REGISTER_DIG_P8)
        self.dig_P9 = self._device.readS16LE(BME280_REGISTER_DIG_P9)
        self.dig_H1 = self._device.readU8(BME280_REGISTER_DIG_H1)
        self.dig_H2 = self._device.readS16LE(BME280_REGISTER_DIG_H2)
        self.dig_H3 = self._device.readU8(BME280_REGISTER_DIG_H3)
        self.dig_H6 = self._device.readS8(BME280_REGISTER_DIG_H7)
        h4 = self._device.readS8(BME280_REGISTER_DIG_H4)
        h4 = h4 << 24 >> 20
        self.dig_H4 = h4 | self._device.readU8(BME280_REGISTER_DIG_H5) & 15
        h5 = self._device.readS8(BME280_REGISTER_DIG_H6)
        h5 = h5 << 24 >> 20
        self.dig_H5 = h5 | self._device.readU8(BME280_REGISTER_DIG_H5) >> 4 & 15

    def read_raw_temp(self):
        """Reads the raw (uncompensated) temperature from the sensor."""
        meas = self._mode
        self._device.write8(BME280_REGISTER_CONTROL_HUM, meas)
        meas = self._mode << 5 | self._mode << 2 | 1
        self._device.write8(BME280_REGISTER_CONTROL, meas)
        sleep_time = 0.00125 + 0.0023 * (1 << self._mode)
        sleep_time = sleep_time + 0.0023 * (1 << self._mode) + 0.000575
        sleep_time = sleep_time + 0.0023 * (1 << self._mode) + 0.000575
        time.sleep(sleep_time)
        msb = self._device.readU8(BME280_REGISTER_TEMP_DATA)
        lsb = self._device.readU8(BME280_REGISTER_TEMP_DATA + 1)
        xlsb = self._device.readU8(BME280_REGISTER_TEMP_DATA + 2)
        raw = (msb << 16 | lsb << 8 | xlsb) >> 4
        return raw

    def read_raw_pressure(self):
        """Reads the raw (uncompensated) pressure level from the sensor."""
        msb = self._device.readU8(BME280_REGISTER_PRESSURE_DATA)
        lsb = self._device.readU8(BME280_REGISTER_PRESSURE_DATA + 1)
        xlsb = self._device.readU8(BME280_REGISTER_PRESSURE_DATA + 2)
        raw = (msb << 16 | lsb << 8 | xlsb) >> 4
        return raw

    def read_raw_humidity(self):
        """Assumes that the temperature has already been read """
        msb = self._device.readU8(BME280_REGISTER_HUMIDITY_DATA)
        lsb = self._device.readU8(BME280_REGISTER_HUMIDITY_DATA + 1)
        raw = msb << 8 | lsb
        return raw

    def read_temperature(self):
        """Gets the compensated temperature in degrees celsius."""
        UT = float(self.read_raw_temp())
        var1 = (UT / 16384.0 - self.dig_T1 / 1024.0) * float(self.dig_T2)
        var2 = (UT / 131072.0 - self.dig_T1 / 8192.0) * (UT / 131072.0 - self.dig_T1 / 8192.0) * float(self.dig_T3)
        self.t_fine = int(var1 + var2)
        temp = (var1 + var2) / 5120.0
        return temp

    def read_pressure(self):
        """Gets the compensated pressure in Pascals."""
        adc = self.read_raw_pressure()
        var1 = self.t_fine / 2.0 - 64000.0
        var2 = var1 * var1 * self.dig_P6 / 32768.0
        var2 = var2 + var1 * self.dig_P5 * 2.0
        var2 = var2 / 4.0 + self.dig_P4 * 65536.0
        var1 = (self.dig_P3 * var1 * var1 / 524288.0 + self.dig_P2 * var1) / 524288.0
        var1 = (1.0 + var1 / 32768.0) * self.dig_P1
        if var1 == 0:
            return 0
        p = 1048576.0 - adc
        p = (p - var2 / 4096.0) * 6250.0 / var1
        var1 = self.dig_P9 * p * p / 2147483648.0
        var2 = p * self.dig_P8 / 32768.0
        p = p + (var1 + var2 + self.dig_P7) / 16.0
        return p

    def read_humidity(self):
        adc = self.read_raw_humidity()
        h = self.t_fine - 76800.0
        h = (adc - (self.dig_H4 * 64.0 + self.dig_H5 / 16384.8 * h)) * (self.dig_H2 / 65536.0 * (1.0 + self.dig_H6 / 67108864.0 * h * (1.0 + self.dig_H3 / 67108864.0 * h)))
        h = h * (1.0 - self.dig_H1 * h / 524288.0)
        if h > 100:
            h = 100
        elif h < 0:
            h = 0
        return h