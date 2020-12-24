# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/protonvpn_gtk/utils/system.py
# Compiled at: 2020-01-04 07:05:35
# Size of source mod 2**32: 900 bytes
import os, subprocess, time

def is_connected() -> bool:
    """ Check if VPN is connected."""
    openvpn_pids = subprocess.run([
     'pgrep', 'openvpn'],
      stdout=(subprocess.PIPE)).stdout.decode('utf-8').split()
    return bool(openvpn_pids)


def is_killswitch_active(config_dir: str) -> bool:
    """ Check if Kill Switch is active """
    return os.path.isfile(os.path.join(config_dir, 'iptables.backup'))


def is_server_reachable(server: str) -> bool:
    """ Check if the VPN Server is reachable """
    ping = subprocess.run(['ping', '-c', '1', server], stdout=(subprocess.PIPE),
      stderr=(subprocess.PIPE))
    return ping.returncode == 0


def kill_openvpn(signal: str='-15') -> bool:
    """ Kiell openvpn process """
    subprocess.run(['pkill', signal, 'openvpn'])
    time.sleep(0.5)
    return is_connected()