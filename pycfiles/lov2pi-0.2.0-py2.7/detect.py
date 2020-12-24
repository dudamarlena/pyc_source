# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-intel/egg/lov2pi/detect.py
# Compiled at: 2015-08-13 04:02:42
import platform, re
UNKNOWN = 'unknown'
RASPBERRY_PI = 'rpi'
BEAGLEBONE_BLACK = 'bbb'
MINNOWBOARD = 'mb'

def platform_detect():
    """Detect if running on the Raspberry Pi or Beaglebone Black and return the
    platform type.  Will return RASPBERRY_PI, BEAGLEBONE_BLACK, or UNKNOWN."""
    try:
        pi = pi_version()
        if pi is not None:
            return RASPBERRY_PI
    except Exception as e:
        return UNKNOWN

    plat = platform.platform()
    if plat.lower().find('armv7l-with-debian') > -1:
        return BEAGLEBONE_BLACK
    else:
        if plat.lower().find('armv7l-with-ubuntu') > -1:
            return BEAGLEBONE_BLACK
        if plat.lower().find('armv7l-with-glibc2.4') > -1:
            return BEAGLEBONE_BLACK
        try:
            import mraa
            if mraa.getPlatformName() == 'MinnowBoard MAX':
                return MINNOWBOARD
        except ImportError:
            pass

        return UNKNOWN


def pi_revision():
    """Detect the revision number of a Raspberry Pi, useful for changing
    functionality like default I2C bus based on revision."""
    with open('/proc/cpuinfo', 'r') as (infile):
        for line in infile:
            match = re.match('Revision\\s+:\\s+.*(\\w{4})$', line, flags=re.IGNORECASE)
            if match and match.group(1) in ('0000', '0002', '0003'):
                return 1
            if match:
                return 2

        raise RuntimeError('Could not determine Raspberry Pi revision.')


def pi_version():
    """Detect the version of the Raspberry Pi.  Returns either 1, 2 or
    None depending on if it's a Raspberry Pi 1 (model A, B, A+, B+),
    Raspberry Pi 2 (model B+), or not a Raspberry Pi.
    """
    with open('/proc/cpuinfo', 'r') as (infile):
        cpuinfo = infile.read()
    match = re.search('^Hardware\\s+:\\s+(\\w+)$', cpuinfo, flags=re.MULTILINE | re.IGNORECASE)
    if not match:
        return
    else:
        if match.group(1) == 'BCM2708':
            return 1
        else:
            if match.group(1) == 'BCM2709':
                return 2
            return

        return