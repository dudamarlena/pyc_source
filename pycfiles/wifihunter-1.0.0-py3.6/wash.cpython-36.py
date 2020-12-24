# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/src/plugins/wash.py
# Compiled at: 2020-01-15 14:43:30
# Size of source mod 2**32: 2369 bytes
from .dependency import Dependency
from ..handlers.target import WPSState
from ..handlers.process import Process
import json

class Wash(Dependency):
    __doc__ = ' Wrapper for Wash program. '
    dependency_required = False
    dependency_name = 'wash'
    dependency_url = 'https://github.com/t6x/reaver-wps-fork-t6x'

    def __init__(self):
        pass

    @staticmethod
    def check_for_wps_and_update_targets(capfile, targets):
        if not Wash.exists():
            return
        command = ['wash',
         '-f', capfile,
         '-j']
        p = Process(command)
        try:
            p.wait()
            lines = p.stdout()
        except:
            return
        else:
            wps_bssids = set()
            locked_bssids = set()
            for line in lines.split('\n'):
                try:
                    obj = json.loads(line)
                    bssid = obj['bssid']
                    locked = obj['wps_locked']
                    if locked != True:
                        wps_bssids.add(bssid)
                    else:
                        locked_bssids.add(bssid)
                except:
                    pass

            for t in targets:
                target_bssid = t.bssid.upper()
                if target_bssid in wps_bssids:
                    t.wps = WPSState.UNLOCKED
                else:
                    if target_bssid in locked_bssids:
                        t.wps = WPSState.LOCKED
                    else:
                        t.wps = WPSState.NONE


if __name__ == '__main__':
    test_file = './tests/files/contains_wps_network.cap'
    target_bssid = 'A4:2B:8C:16:6B:3A'
    from ..handlers.target import Target
    fields = [
     'A4:2B:8C:16:6B:3A',
     '2015-05-27 19:28:44', '2015-05-27 19:28:46',
     '11',
     '54',
     'WPA2', 'CCMP TKIP', 'PSK',
     '-58', '2', '0', '0.0.0.0', '9',
     'Test Router Please Ignore']
    t = Target(fields)
    targets = [t]
    Wash.check_for_wps_and_update_targets(test_file, targets)
    print('Target(BSSID={}).wps = {} (Expected: 1)'.format(targets[0].bssid, targets[0].wps))
    if not targets[0].wps == WPSState.UNLOCKED:
        raise AssertionError