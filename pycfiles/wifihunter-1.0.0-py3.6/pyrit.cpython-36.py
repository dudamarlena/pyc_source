# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/src/plugins/pyrit.py
# Compiled at: 2020-01-19 08:13:44
# Size of source mod 2**32: 1974 bytes
from .dependency import Dependency
from ..handlers.process import Process
import re

class Pyrit(Dependency):
    __doc__ = ' Wrapper for Pyrit program. '
    dependency_required = False
    dependency_name = 'pyrit'
    dependency_url = 'https://github.com/JPaulMora/Pyrit/wiki'

    def __init__(self):
        pass

    @staticmethod
    def bssid_essid_with_handshakes(capfile, bssid=None, essid=None):
        if not Pyrit.exists():
            return []
        else:
            command = [
             'pyrit',
             '-r', capfile,
             'analyze']
            pyrit = Process(command, devnull=False)
            current_bssid = current_essid = None
            bssid_essid_pairs = set()
            for line in pyrit.stdout().split('\n'):
                mac_regex = ('[a-zA-Z0-9]{2}:' * 6)[:-1]
                match = re.search("^#\\d+: AccessPoint (%s) \\('(.*)'\\):$" % mac_regex, line)
                if match:
                    current_bssid, current_essid = match.groups()
                    if bssid is not None:
                        if bssid.lower() != current_bssid:
                            current_bssid = None
                            current_essid = None
                    if essid is not None and essid != current_essid:
                        current_bssid = None
                        current_essid = None
                else:
                    if current_bssid is not None:
                        if current_essid is not None:
                            if ', good' in line:
                                bssid_essid_pairs.add((current_bssid, current_essid))

            return list(bssid_essid_pairs)