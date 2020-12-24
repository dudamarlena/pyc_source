# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: pyfeld/pingTest.py
# Compiled at: 2017-11-23 08:41:51
import subprocess, sys

def ping_test_alive(ip):
    cmd = 'ping -W 1 -c 1 ' + ip
    try:
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except Exception as e:
        return 0

    output_received = ''
    while True:
        line = process.stdout.readline()
        if len(line) == 0 and process.poll() != None:
            break
        v = line.decode('utf-8')
        output_received += v

    return '1 received' in output_received


if __name__ == '__main__':
    print ping_test_alive(sys.argv[1])