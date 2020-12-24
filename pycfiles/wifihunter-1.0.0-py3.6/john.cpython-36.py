# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/src/plugins/john.py
# Compiled at: 2020-01-19 08:13:30
# Size of source mod 2**32: 2034 bytes
from .dependency import Dependency
from ..config import Configuration
from ..handlers.color import Color
from ..handlers.process import Process
from ..plugins.hashcat import HcxPcapTool
import os

class John(Dependency):
    __doc__ = ' Wrapper for John program. '
    dependency_required = False
    dependency_name = 'john'
    dependency_url = 'http://www.openwall.com/john/'

    @staticmethod
    def crack_handshake(handshake, show_command=False):
        john_file = HcxPcapTool.generate_john_file(handshake,
          show_command=show_command)
        formats_stdout = Process(['john', '--list=formats']).stdout()
        if 'wpapsk-opencl' in formats_stdout:
            john_format = 'wpapsk-opencl'
        else:
            if 'wpapsk-cuda' in formats_stdout:
                john_format = 'wpapsk-cuda'
            else:
                john_format = 'wpapsk'
        command = [
         'john',
         '--format=%s' % john_format,
         '--wordlist', Configuration.wordlist,
         john_file]
        if show_command:
            Color.pl('{+} {D}Running: {W}{P}%s{W}' % ' '.join(command))
        else:
            process = Process(command)
            process.wait()
            command = [
             'john', '--show', john_file]
            if show_command:
                Color.pl('{+} {D}Running: {W}{P}%s{W}' % ' '.join(command))
            process = Process(command)
            stdout, stderr = process.get_output()
            if '0 password hashes cracked' in stdout:
                key = None
            else:
                for line in stdout.split('\n'):
                    if handshake.capfile in line:
                        key = line.split(':')[1]
                        break

        if os.path.exists(john_file):
            os.remove(john_file)
        return key