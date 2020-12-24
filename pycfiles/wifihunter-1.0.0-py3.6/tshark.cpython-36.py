# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/src/plugins/tshark.py
# Compiled at: 2020-01-15 14:42:33
# Size of source mod 2**32: 7825 bytes
from .dependency import Dependency
from ..handlers.target import WPSState
from ..handlers.process import Process
import re

class Tshark(Dependency):
    __doc__ = ' Wrapper for Tshark program. '
    dependency_required = False
    dependency_name = 'tshark'
    dependency_url = 'apt-get install wireshark'

    def __init__(self):
        pass

    @staticmethod
    def _extract_src_dst_index_total(line):
        mac_regex = ('[a-zA-Z0-9]{2}:' * 6)[:-1]
        match = re.search('(%s)\\s*.*\\s*(%s).*Message.*(\\d).*of.*(\\d)' % (mac_regex, mac_regex), line)
        if match is None:
            return (None, None, None, None)
        else:
            src, dst, index, total = match.groups()
            return (src, dst, index, total)

    @staticmethod
    def _build_target_client_handshake_map(output, bssid=None):
        target_client_msg_nums = {}
        for line in output.split('\n'):
            src, dst, index, total = Tshark._extract_src_dst_index_total(line)
            if src is None:
                pass
            else:
                index = int(index)
                total = int(total)
                if total != 4:
                    pass
                else:
                    if index % 2 == 1:
                        target = src
                        client = dst
                    else:
                        client = src
                        target = dst
            if bssid is not None:
                if bssid.lower() != target.lower():
                    continue
            target_client_key = '%s,%s' % (target, client)
            if index == 1:
                target_client_msg_nums[target_client_key] = 1
            else:
                if target_client_key not in target_client_msg_nums:
                    continue
                else:
                    if index - 1 != target_client_msg_nums[target_client_key]:
                        continue
                    else:
                        target_client_msg_nums[target_client_key] = index

        return target_client_msg_nums

    @staticmethod
    def bssids_with_handshakes(capfile, bssid=None):
        if not Tshark.exists():
            return []
        else:
            command = ['tshark',
             '-r', capfile,
             '-n',
             '-Y', 'eapol']
            tshark = Process(command, devnull=False)
            target_client_msg_nums = Tshark._build_target_client_handshake_map((tshark.stdout()), bssid=bssid)
            bssids = set()
            for target_client, num in target_client_msg_nums.items():
                if num == 4:
                    this_bssid = target_client.split(',')[0]
                    bssids.add(this_bssid)

            return list(bssids)

    @staticmethod
    def bssid_essid_pairs(capfile, bssid):
        if not Tshark.exists():
            return []
        else:
            ssid_pairs = set()
            command = [
             'tshark',
             '-r', capfile,
             '-n',
             '-Y', '"wlan.fc.type_subtype == 0x08 || wlan.fc.type_subtype == 0x05"']
            tshark = Process(command, devnull=False)
            for line in tshark.stdout().split('\n'):
                mac_regex = ('[a-zA-Z0-9]{2}:' * 6)[:-1]
                match = re.search('(%s) [^ ]* (%s).*.*SSID=(.*)$' % (mac_regex, mac_regex), line)
                if match is None:
                    pass
                else:
                    src, dst, essid = match.groups()
                    if dst.lower() == 'ff:ff:ff:ff:ff:ff':
                        pass
                    else:
                        if bssid is not None:
                            if bssid.lower() == src.lower():
                                ssid_pairs.add((src, essid))
                        else:
                            ssid_pairs.add((src, essid))

            return list(ssid_pairs)

    @staticmethod
    def check_for_wps_and_update_targets(capfile, targets):
        """
            Given a cap file and list of targets, use TShark to
            find which BSSIDs in the cap file use WPS.
            Then update the 'wps' flag for those BSSIDs in the targets.

            Args:
                capfile - .cap file from airodump containing packets
                targets - list of Targets from scan, to be updated
        """
        from ..config import Configuration
        if not Tshark.exists():
            raise ValueError('Cannot detect WPS networks: Tshark does not exist')
        command = [
         'tshark',
         '-r', capfile,
         '-n',
         '-Y', 'wps.wifi_protected_setup_state && wlan.da == ff:ff:ff:ff:ff:ff',
         '-T', 'fields',
         '-e', 'wlan.ta',
         '-e', 'wps.ap_setup_locked',
         '-E', 'separator=,']
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
                if ',' not in line:
                    pass
                else:
                    bssid, locked = line.split(',')
                    if '1' not in locked:
                        wps_bssids.add(bssid.upper())
                    else:
                        locked_bssids.add(bssid.upper())

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
    Tshark.check_for_wps_and_update_targets(test_file, targets)
    print('Target(BSSID={}).wps = {} (Expected: 1)'.format(targets[0].bssid, targets[0].wps))
    assert targets[0].wps == WPSState.UNLOCKED
    print(Tshark.bssids_with_handshakes(test_file, bssid=target_bssid))