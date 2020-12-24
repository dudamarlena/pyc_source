# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ST7735/__init__.py
# Compiled at: 2020-03-17 11:10:24
import numbers, time, numpy as np, spidev, RPi.GPIO as GPIO
__version__ = '0.0.3'
BG_SPI_CS_BACK = 0
BG_SPI_CS_FRONT = 1
SPI_CLOCK_HZ = 16000000
ST7735_TFTWIDTH = 80
ST7735_TFTHEIGHT = 160
ST7735_COLS = 132
ST7735_ROWS = 162
ST7735_NOP = 0
ST7735_SWRESET = 1
ST7735_RDDID = 4
ST7735_RDDST = 9
ST7735_SLPIN = 16
ST7735_SLPOUT = 17
ST7735_PTLON = 18
ST7735_NORON = 19
ST7735_INVOFF = 32
ST7735_INVON = 33
ST7735_DISPOFF = 40
ST7735_DISPON = 41
ST7735_CASET = 42
ST7735_RASET = 43
ST7735_RAMWR = 44
ST7735_RAMRD = 46
ST7735_PTLAR = 48
ST7735_MADCTL = 54
ST7735_COLMOD = 58
ST7735_FRMCTR1 = 177
ST7735_FRMCTR2 = 178
ST7735_FRMCTR3 = 179
ST7735_INVCTR = 180
ST7735_DISSET5 = 182
ST7735_PWCTR1 = 192
ST7735_PWCTR2 = 193
ST7735_PWCTR3 = 194
ST7735_PWCTR4 = 195
ST7735_PWCTR5 = 196
ST7735_VMCTR1 = 197
ST7735_RDID1 = 218
ST7735_RDID2 = 219
ST7735_RDID3 = 220
ST7735_RDID4 = 221
ST7735_GMCTRP1 = 224
ST7735_GMCTRN1 = 225
ST7735_PWCTR6 = 252
ST7735_BLACK = 0
ST7735_BLUE = 31
ST7735_GREEN = 2016
ST7735_RED = 63488
ST7735_CYAN = 2047
ST7735_MAGENTA = 63519
ST7735_YELLOW = 65504
ST7735_WHITE = 65535

def color565(r, g, b):
    """Convert red, green, blue components to a 16-bit 565 RGB value. Components
    should be values 0 to 255.
    """
    return (r & 248) << 8 | (g & 252) << 3 | b >> 3


def image_to_data(image, rotation=0):
    """Generator function to convert a PIL image to 16-bit 565 RGB bytes."""
    pb = np.rot90(np.array(image.convert('RGB')), rotation // 90).astype('uint16')
    color = (pb[:, :, 0] & 248) << 8 | (pb[:, :, 1] & 252) << 3 | pb[:, :, 2] >> 3
    return np.dstack((color >> 8 & 255, color & 255)).flatten().tolist()


class ST7735(object):
    """Representation of an ST7735 TFT LCD."""

    def __init__(self, port, cs, dc, backlight=None, rst=None, width=ST7735_TFTWIDTH, height=ST7735_TFTHEIGHT, rotation=90, offset_left=None, offset_top=None, invert=True, spi_speed_hz=4000000):
        """Create an instance of the display using SPI communication.

        Must provide the GPIO pin number for the D/C pin and the SPI driver.

        Can optionally provide the GPIO pin number for the reset pin as the rst parameter.

        :param port: SPI port number
        :param cs: SPI chip-select number (0 or 1 for BCM
        :param backlight: Pin for controlling backlight
        :param rst: Reset pin for ST7735
        :param width: Width of display connected to ST7735
        :param height: Height of display connected to ST7735
        :param rotation: Rotation of display connected to ST7735
        :param offset_left: COL offset in ST7735 memory
        :param offset_top: ROW offset in ST7735 memory
        :param invert: Invert display
        :param spi_speed_hz: SPI speed (in Hz)

        """
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        self._spi = spidev.SpiDev(port, cs)
        self._spi.mode = 0
        self._spi.lsbfirst = False
        self._spi.max_speed_hz = spi_speed_hz
        self._dc = dc
        self._rst = rst
        self._width = width
        self._height = height
        self._rotation = rotation
        self._invert = invert
        if offset_left is None:
            offset_left = (ST7735_COLS - width) // 2
        self._offset_left = offset_left
        if offset_top is None:
            offset_top = (ST7735_ROWS - height) // 2
        self._offset_top = offset_top
        GPIO.setup(dc, GPIO.OUT)
        self._backlight = backlight
        if backlight is not None:
            GPIO.setup(backlight, GPIO.OUT)
            GPIO.output(backlight, GPIO.LOW)
            time.sleep(0.1)
            GPIO.output(backlight, GPIO.HIGH)
        if rst is not None:
            GPIO.setup(rst, GPIO.OUT)
        self.reset()
        self._init()
        return

    def send(self, data, is_data=True, chunk_size=4096):
        """Write a byte or array of bytes to the display. Is_data parameter
        controls if byte should be interpreted as display data (True) or command
        data (False).  Chunk_size is an optional size of bytes to write in a
        single SPI transaction, with a default of 4096.
        """
        GPIO.output(self._dc, is_data)
        if isinstance(data, numbers.Number):
            data = [
             data & 255]
        self._spi.xfer3(data)

    def set_backlight(self, value):
        """Set the backlight on/off."""
        if self._backlight is not None:
            GPIO.output(self._backlight, value)
        return

    @property
    def width(self):
        if self._rotation == 0 or self._rotation == 180:
            return self._width
        return self._height

    @property
    def height(self):
        if self._rotation == 0 or self._rotation == 180:
            return self._height
        return self._width

    def command(self, data):
        """Write a byte or array of bytes to the display as command data."""
        self.send(data, False)

    def data(self, data):
        """Write a byte or array of bytes to the display as display data."""
        self.send(data, True)

    def reset(self):
        """Reset the display, if reset pin is connected."""
        if self._rst is not None:
            GPIO.output(self._rst, 1)
            time.sleep(0.5)
            GPIO.output(self._rst, 0)
            time.sleep(0.5)
            GPIO.output(self._rst, 1)
            time.sleep(0.5)
        return

    def _init(self):
        self.command(ST7735_SWRESET)
        time.sleep(0.15)
        self.command(ST7735_SLPOUT)
        time.sleep(0.5)
        self.command(ST7735_FRMCTR1)
        self.data(1)
        self.data(44)
        self.data(45)
        self.command(ST7735_FRMCTR2)
        self.data(1)
        self.data(44)
        self.data(45)
        self.command(ST7735_FRMCTR3)
        self.data(1)
        self.data(44)
        self.data(45)
        self.data(1)
        self.data(44)
        self.data(45)
        self.command(ST7735_INVCTR)
        self.data(7)
        self.command(ST7735_PWCTR1)
        self.data(162)
        self.data(2)
        self.data(132)
        self.command(ST7735_PWCTR2)
        self.data(10)
        self.data(0)
        self.command(ST7735_PWCTR4)
        self.data(138)
        self.data(42)
        self.command(ST7735_PWCTR5)
        self.data(138)
        self.data(238)
        self.command(ST7735_VMCTR1)
        self.data(14)
        if self._invert:
            self.command(ST7735_INVON)
        else:
            self.command(ST7735_INVOFF)
        self.command(ST7735_MADCTL)
        self.data(200)
        self.command(ST7735_COLMOD)
        self.data(5)
        self.command(ST7735_CASET)
        self.data(0)
        self.data(self._offset_left)
        self.data(0)
        self.data(self._width + self._offset_left - 1)
        self.command(ST7735_RASET)
        self.data(0)
        self.data(self._offset_top)
        self.data(0)
        self.data(self._height + self._offset_top - 1)
        self.command(ST7735_GMCTRP1)
        self.data(2)
        self.data(28)
        self.data(7)
        self.data(18)
        self.data(55)
        self.data(50)
        self.data(41)
        self.data(45)
        self.data(41)
        self.data(37)
        self.data(43)
        self.data(57)
        self.data(0)
        self.data(1)
        self.data(3)
        self.data(16)
        self.command(ST7735_GMCTRN1)
        self.data(3)
        self.data(29)
        self.data(7)
        self.data(6)
        self.data(46)
        self.data(44)
        self.data(41)
        self.data(45)
        self.data(46)
        self.data(46)
        self.data(55)
        self.data(63)
        self.data(0)
        self.data(0)
        self.data(2)
        self.data(16)
        self.command(ST7735_NORON)
        time.sleep(0.1)
        self.command(ST7735_DISPON)
        time.sleep(0.1)

    def begin(self):
        """Set up the display

        Deprecated. Included in __init__.

        """
        pass

    def set_window(self, x0=0, y0=0, x1=None, y1=None):
        """Set the pixel address window for proceeding drawing commands. x0 and
        x1 should define the minimum and maximum x pixel bounds.  y0 and y1
        should define the minimum and maximum y pixel bound.  If no parameters
        are specified the default will be to update the entire display from 0,0
        to width-1,height-1.
        """
        if x1 is None:
            x1 = self._width - 1
        if y1 is None:
            y1 = self._height - 1
        y0 += self._offset_top
        y1 += self._offset_top
        x0 += self._offset_left
        x1 += self._offset_left
        self.command(ST7735_CASET)
        self.data(x0 >> 8)
        self.data(x0)
        self.data(x1 >> 8)
        self.data(x1)
        self.command(ST7735_RASET)
        self.data(y0 >> 8)
        self.data(y0)
        self.data(y1 >> 8)
        self.data(y1)
        self.command(ST7735_RAMWR)
        return

    def display(self, image):
        """Write the provided image to the hardware.

        :param image: Should be RGB format and the same dimensions as the display hardware.

        """
        self.set_window()
        pixelbytes = list(image_to_data(image, self._rotation))
        self.data(pixelbytes)