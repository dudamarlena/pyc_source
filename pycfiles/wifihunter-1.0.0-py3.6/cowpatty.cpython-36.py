# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/src/plugins/cowpatty.py
# Compiled at: 2020-01-19 08:11:50
# Size of source mod 2**32: 1124 bytes
from .dependency import Dependency
from ..config import Configuration
from ..handlers.color import Color
from ..handlers.process import Process
from ..plugins.hashcat import HcxPcapTool
import os, re

class Cowpatty(Dependency):
    __doc__ = ' Wrapper for Cowpatty program. '
    dependency_required = False
    dependency_name = 'cowpatty'
    dependency_url = 'https://tools.kali.org/wireless-attacks/cowpatty'

    @staticmethod
    def crack_handshake(handshake, show_command=False):
        command = [
         'cowpatty',
         '-f', Configuration.wordlist,
         '-r', handshake.capfile,
         '-s', handshake.essid]
        if show_command:
            Color.pl('{+} {D}Running: {W}{P}%s{W}' % ' '.join(command))
        process = Process(command)
        stdout, stderr = process.get_output()
        key = None
        for line in stdout.split('\n'):
            if 'The PSK is "' in line:
                key = line.split('"', 1)[1][:-2]
                break

        return key