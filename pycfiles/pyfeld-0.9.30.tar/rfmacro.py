# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: pyfeld/rfmacro.py
# Compiled at: 2017-11-23 08:41:51
from __future__ import unicode_literals
import subprocess, sys, threading
from time import sleep
import re
from texttable import Texttable
from pyfeld.pingTest import ping_test_alive
try:
    from pyfeld.rfcmd import RfCmd
except:
    pass

sshcmd = b'ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null root@'
scpcmd = b'scp -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null '

class UpdateProcessesFreeToKill:

    def __init__(self):
        self.processList = list()

    def runCommand(self, cmd):
        try:
            process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            self.processList.append(process)
        except Exception as e:
            return 0

    def killall(self):
        for proc in self.processList:
            proc.kill()


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


def get_ips():
    RfCmd.discover()
    result = RfCmd.get_device_ips(False, b'list')
    return result


def show_pretty_versions():
    result_list = list()
    header_list = [b'IP', b'Role', b'Version', b'Name', b'Streamcast version']
    result_list.append(header_list)
    print b'Versions installed:'
    ips = get_ips()
    for ip in ips:
        line = retrieve(sshcmd + ip + b' cat /var/raumfeld-1.0/device-role.json')
        if b'true' in line:
            moreinfo = b'host'
        else:
            moreinfo = b'slave'
        renderer_name = RfCmd.get_device_name_by_ip(ip)
        line = retrieve(sshcmd + ip + b' cat /etc/raumfeld-version')
        line_streamcast = retrieve(sshcmd + ip + b' streamcastd --version')
        single_result = list()
        single_result.append(ip)
        single_result.append(moreinfo)
        single_result.append(line.rstrip())
        single_result.append(renderer_name)
        single_result.append(line_streamcast.rstrip())
        result_list.append(single_result)

    t = Texttable(250)
    t.add_rows(result_list)
    print t.draw()


def show_versions():
    print b'Versions installed:'
    ips = get_ips()
    for ip in ips:
        line = retrieve(sshcmd + ip + b' cat /var/raumfeld-1.0/device-role.json')
        if b'true' in line:
            moreinfo = b'host'
        else:
            moreinfo = b'slave'
        renderer_name = RfCmd.get_device_name_by_ip(ip)
        line = retrieve(sshcmd + ip + b' cat /etc/raumfeld-version')
        line_streamcast = retrieve(sshcmd + ip + b' streamcastd --version')
        print ip + b'\t' + moreinfo + b'\t' + line.rstrip() + b'\t' + line_streamcast.rstrip() + b'\t' + str(renderer_name)


def clean_host_keys():
    print b'cleaning host_keys:'
    ips = get_ips()
    for ip in ips:
        line = retrieve(b'ssh-keygen -R ' + ip)
        print ip + b':\t' + line.rstrip()


def single_device_update(free_to_kill, ip, url):
    cmd = sshcmd + ip + b' raumfeld-update --force ' + url
    print b'running cmd: ' + cmd
    free_to_kill.runCommand(cmd)


def force_update(url):
    print b'Force updating with url ' + url
    ips = get_ips()
    processes = list()
    device_pingable = dict()
    free_to_kill = UpdateProcessesFreeToKill()
    count = 0
    for ip in ips:
        proc = threading.Thread(target=single_device_update, args=(free_to_kill, ip, url))
        proc.start()
        processes.append(proc)
        device_pingable[ip] = True
        count += 1

    temp_count = count
    print b'Waiting for action...'
    sleep(5)
    while count > 0:
        sleep(10)
        print b''
        for ip in ips:
            if device_pingable[ip]:
                print b'testing if ping alive: ' + ip + b' ' + str(RfCmd.map_ip_to_friendly_name(ip))
                if not ping_test_alive(ip):
                    device_pingable[ip] = False
                    count -= 1

    count = temp_count
    print b'Rebooting in progress...'
    while count > 0:
        sleep(10)
        print b''
        for ip in ips:
            if not device_pingable[ip]:
                print b'testing if ping reborn: ' + ip + b' ' + str(RfCmd.map_ip_to_friendly_name(ip))
                if ping_test_alive(ip):
                    device_pingable[ip] = True
                    count -= 1

    print b'done updating shells. Leaving the houses now.'
    free_to_kill.killall()
    for proc in processes:
        proc.join()

    print b'Processes joined joyfully'


def single_device_command(ip, cmd):
    cmd = sshcmd + ip + b' ' + cmd
    print (b'running cmd on device {0}: {1}').format(ip, cmd)
    lines = retrieve(cmd)
    print (b'result from {0}').format(ip)
    print lines


def ssh_command(cmd):
    print b'Send command to all devices: ' + cmd
    ips = get_ips()
    processes = list()
    for ip in ips:
        proc = threading.Thread(target=single_device_command, args=(ip, cmd))
        proc.start()
        processes.append(proc)

    for proc in processes:
        proc.join()


def scp_up_file(local_file, target_location):
    print b'Copy file:'
    ips = get_ips()
    for ip in ips:
        line = retrieve(scpcmd + (b' {1} root@{0}:{2}').format(ip, local_file, target_location))
        print ip + b':\t' + line.rstrip()


def scp_down_file(remote_file, target_file):
    print b'Copy file:'
    ips = get_ips()
    for ip in ips:
        line = retrieve(scpcmd + (b' root@{0}:{1} {2}').format(ip, remote_file, target_file))
        print ip + b':\t' + line.rstrip()


def usage(argv):
    print (b'Usage: {0} COMMAND [params]').format(argv[0])
    print b'Execute macrocommands over ssh for interacting with raumfeld if you got many devices, these need SSH access allowed'
    print b'COMMAND may be one of the following'
    print b'version                   show versions'
    print b'update <URL>              force update'
    print b'ssh <command>             any shell available on device, command in quotes'
    print b'upload <file> <target>    copy a file to a target location'
    print b'download <file> <target>  copy a file from device to target'
    print b''
    print b'clean-hostkeys     clean all host keys to avoid security messages'


def run_macro(argv):
    if len(argv) < 2:
        usage(argv)
        sys.exit(2)
    command = argv[1]
    if command == b'version':
        show_pretty_versions()
    elif command == b'update':
        force_update(argv[2])
    elif command == b'ssh':
        ssh_command((b' ').join(argv[2:]))
    elif command == b'upload':
        scp_up_file(argv[2], argv[3])
    elif command == b'download':
        scp_down_file(argv[2], argv[3])
    elif command == b'clean-hostkeys':
        clean_host_keys()
    else:
        print (b'Unknown command {0}').format(command)
        usage(argv)


def run_main():
    run_macro(sys.argv)


if __name__ == b'__main__':
    run_main()