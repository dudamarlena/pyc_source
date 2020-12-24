# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: pyfeld/hasprocess.py
# Compiled at: 2017-11-23 08:41:51
from __future__ import unicode_literals
import subprocess, sys, threading, re

def retrieve(cmd):
    try:
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except Exception as e:
        return 0

    lines = b''
    while True:
        nextline = process.stdout.readline()
        if len(nextline) == 0 and process.poll() != None:
            break
        lines += nextline.decode(b'utf-8')

    return lines


sshcmd = b'ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null root@'

def single_device_command(ip, cmd):
    cmd = sshcmd + ip + b' ' + cmd
    lines = retrieve(cmd)
    return lines.split(b'\n')


def get_ps_list(ip):
    processes_found = single_device_command(ip, b'ps -T')
    return processes_found


def usage(argv):
    print (b'Usage: {0} [OPTIONS] ip').format(argv[0])
    print b'get process list of device on given ip (needs ssh access to device via root)'
    print b'OPTIONS:'
    print b'  -m, --missing     show only missing processes'
    print b'  -e, --existent    show only existent processes'
    print b'  -a, --all         show the complete ps list'


def list_of_expected_command():
    return [
     [
      b'/usr/bin/rfpd', b'rfpd (soundbar/deck)', False],
     [
      b'logger -t', b'config-service gdbus', False],
     [
      b'/system/chrome/cast_shell', b'cast_shell', True],
     [
      b'bluetoothd', b'bluetoothd', False],
     [
      b'rf-bluetoothd', b'rf-bluetoothd', False],
     [
      b'avahi-daemon', b'avahi-daemon', False],
     [
      b'dbus-daemon', b'dbus-daemon', False],
     [
      b'/usr/sbin/connmand', b'connmand', False],
     [
      b'/usr/sbin/wpa_supplicant', b'wpa_supplicant', False],
     [
      b'{gdbus} config-service', b'config-service gdbus', False],
     [
      b'{gdbus} master-process', b'master-process gdbus', False],
     [
      b'{gdbus} meta-server', b'meta-server gdbus', False],
     [
      b'{gdbus} renderer', b'renderer gdbus', False],
     [
      b'{gdbus} run-streamcastd', b'run-streamcastd gdbus', False],
     [
      b'{gdbus} stream-decoder', b'stream-decoder gdbus', False],
     [
      b'{gdbus} stream-relay', b'stream-relay gdbus', False],
     [
      b'{gdbus} web-service', b'web-service gdbus', False],
     [
      b'{gmain} config-service', b'config-service gmain', True],
     [
      b'{gmain} master-process', b'master-process gmain', True],
     [
      b'{gmain} meta-server', b'meta-server gmain', True],
     [
      b'{gmain} raumfeld-report-daemon', b'raumfeld-report-daemon gmain', True],
     [
      b'{gmain} renderer', b'renderer gmain', True],
     [
      b'{gmain} run-streamcastd', b'run-streamcastd gmain', True],
     [
      b'{gmain} stream-decoder', b'stream-decoder gmain', True],
     [
      b'{gmain} stream-relay', b'stream-relay gmain', True],
     [
      b'{gmain} web-service', b'web-service gmain', True],
     [
      b'{IdleCallbackHel} renderer', b'renderer IdleCallbackHelper', True],
     [
      b'{pool} meta-server', b'meta-server pool', False],
     [
      b'{pool} run-streamcastd', b'run-streamcastd pool', False],
     [
      b'{pool} web-service', b'web-service pool', False],
     [
      b'[cifsiod]', b'cifsiod', False],
     [
      b'[cifsd]', b'cifsd', False],
     [
      b'/usr/bin/dbus-daemon', b'dbus-daemon', True],
     [
      b'{start-master-pr}', b'start-master-process.sh', True],
     [
      b'/usr/sbin/wpa_supplicant', b'wpa_supplicant', False]]


class ProcessItem:

    def __init__(self, name, exists):
        self.name = name
        self.exists = exists


def run_main(argv):
    if len(argv) < 2:
        usage(argv)
        sys.exit(2)
    cmds = list_of_expected_command()
    show_what = b'simple'
    arg_pos = 1
    while argv[arg_pos].startswith(b'-'):
        if argv[arg_pos].startswith(b'--'):
            option = argv[arg_pos][2:]
        else:
            option = argv[arg_pos]
        arg_pos += 1
        if option in ('m', 'missing'):
            show_what = b'missing'
        elif option in ('e', 'existent'):
            show_what = b'existent'
        elif option in ('a', 'all'):
            show_what = b'all'

    ps_list = get_ps_list(argv[arg_pos])
    pos = ps_list[0].find(b'COMMAND')
    ps_list = ps_list[1:]
    clean_list = list()
    for cmd in cmds:
        p_process = ProcessItem(cmd[1], False)
        for item in ps_list:
            item = b' ' + item[pos:]
            item = item.replace(b' ./', b' ')
            item = item.strip()
            if cmd[0] in item:
                p_process.exists = True

        clean_list.append(p_process)

    clean_list.sort(key=lambda x: x.name, reverse=False)
    for ci in clean_list:
        if ci.exists:
            if show_what in ('existent', 'all', 'simple'):
                tickmark = b'[x]'
                print (tickmark, ci.name)
        elif show_what in ('missing', 'all', 'simple'):
            tickmark = b'[ ]'
            print (tickmark, ci.name)


if __name__ == b'__main__':
    run_main(sys.argv)