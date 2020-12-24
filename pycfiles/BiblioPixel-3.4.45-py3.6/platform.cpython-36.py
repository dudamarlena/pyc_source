# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bibliopixel/util/platform.py
# Compiled at: 2019-08-11 12:22:47
# Size of source mod 2**32: 1414 bytes
import platform, subprocess
MAC = 'Darwin'
WINDOWS = 'Windows'
CPUINFO_FILE = '/proc/cpuinfo'

class Platform:

    def __init__(self):
        self.platform = platform.system()
        self.version = platform.version()
        self.release = platform.release()
        self.python_version = platform.python_version()
        try:
            self.cpuinfo = [i.strip() for i in open(CPUINFO_FILE)]
        except:
            self.cpuinfo = []

        def is_rpi_line(i):
            return i.startswith('Hardware') and i.endswith('BCM2708')

        self.is_raspberry_pi = any(is_rpi_line(i) for i in self.cpuinfo)
        self.is_linux = self.platform == 'linux'
        platform_version = ()
        if self.is_linux:
            self.platform = platform.linux_distribution()[0].lower()
        else:
            if self.platform == WINDOWS:
                platform_version = platform.win32_ver()
            else:
                if self.platform == MAC:
                    release, versioninfo, machine = platform.mac_ver()
                    platform_version = (release, machine)
                    for i in ('features', 'brand_string'):
                        s = subprocess.check_output(('sysctl', 'machdep.cpu.' + i))
                        self.cpuinfo.append(s.decode().strip())

        self.platform_version = ':'.join(platform_version)