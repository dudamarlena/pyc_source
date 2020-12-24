# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bibliopixel/drivers/PiWS281X.py
# Compiled at: 2019-08-11 12:22:47
# Size of source mod 2**32: 4294 bytes
import os, sys
from .channel_order import ChannelOrder
from .driver_base import DriverBase
from ..util import log
from ..colors import gamma
WS_ERROR = '\nPiWS281X Requires the rpi_ws281x C extension.\n\nInstall rpi_ws281x with the following shell commands:\n\n    git clone https://github.com/jgarff/rpi_ws281x.git\n    cd rpi_ws281x\n\n    sudo apt-get install python-dev swig scons\n    sudo scons\n\n    cd python\n    # If using default system python3\n    sudo python3 setup.py build install\n    # If using virtualenv, enter env then run\n    python setup.py build install\n'
SUDO_ERROR = '\nThe PiWS281X driver needs to be run as sudo.  Rerun it with sudo, like this:\n    sudo {command}\n'
try:
    from neopixel import Adafruit_NeoPixel, Color as NeoColor
except:
    NeoColor = None

PIN_CHANNEL = {12:0, 
 18:0, 
 40:0, 
 52:0, 
 13:1, 
 19:1, 
 41:1, 
 45:1, 
 53:1, 
 10:0}
STRIP_TYPES = {3:1050624, 
 4:403703808}

class PiWS281X(DriverBase):
    __doc__ = '\n    Driver for controlling WS281X LEDs via the rpi_ws281x C-extension.\n    Only supported on the Raspberry Pi 2, 3, and Zero\n\n    This driver needs to be run as sudo and requires the rpi_ws281x C extension.\n\n    Install rpi_ws281x with the following shell commands:\n\n        git clone https://github.com/jgarff/rpi_ws281x.git\n        cd rpi_ws281x\n\n        sudo apt-get install python-dev swig scons\n        sudo scons\n\n        cd python\n        # If using default system python3\n        sudo python3 setup.py build install\n        # If using virtualenv, enter env then run\n        python setup.py build install\n\n    Provides the same parameters of :py:class:`.driver_base.DriverBase` as\n    well as those below:\n\n    :param int gpio: GPIO pin to output to. Typically 18 or 13\n    :param int ledFreqHz: WS2812B base data frequency in Hz. Only change to\n        400000 if using very old WS218B LEDs\n    :param int ledDma: DMA channel to use for generating signal\n                       (between 1 and 14)\n    :param bool ledInvert: True to invert the signal\n                       (when using NPN transistor level shift)\n    '

    def __init__(self, num, gamma=gamma.NEOPIXEL, c_order='RGB', gpio=18, ledFreqHz=800000, ledDma=5, ledInvert=False, color_channels=3, brightness=255, **kwds):
        if not NeoColor:
            raise ValueError(WS_ERROR)
        else:
            (super().__init__)(num, c_order=c_order, gamma=gamma, **kwds)
            self.gamma = gamma
            if gpio not in PIN_CHANNEL.keys():
                raise ValueError('{} is not a valid gpio option!')
            try:
                strip_type = STRIP_TYPES[color_channels]
            except:
                raise ValueError('In PiWS281X, color_channels can only be 3 or 4')

        self._strip = Adafruit_NeoPixel(num, gpio, ledFreqHz, ledDma, ledInvert, brightness, PIN_CHANNEL[gpio], strip_type)
        try:
            self._strip.begin()
        except RuntimeError as e:
            if os.geteuid():
                if os.path.basename(sys.argv[0]) in ('bp', 'bibliopixel'):
                    command = [
                     'bp'] + sys.argv[1:]
                else:
                    command = [
                     'python'] + sys.argv
                error = SUDO_ERROR.format(command=(' '.join(command)))
                e.args = (error,) + e.args
            raise

    def set_brightness(self, brightness):
        self._strip.setBrightness(brightness)
        return True

    def _compute_packet(self):
        self._render()
        data = self._buf
        self._packet = [tuple(data[p * 3:p * 3 + 3]) for p in range(len(data) // 3)]

    def _send_packet(self):
        for i, p in enumerate(self._packet):
            self._strip.setPixelColor(i, NeoColor(*p))

        self._strip.show()