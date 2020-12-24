# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\sboon\AppData\Local\Temp\pip-install-ptdbtr91\quarchpy\quarchpy\connection_specific\connection_QPS.py
# Compiled at: 2020-03-25 05:10:07
# Size of source mod 2**32: 2952 bytes
import sys, socket, time, datetime, subprocess, os, random, time

class QpsInterface:

    def __init__(self, host='127.0.0.1', port=9822):
        self.host = host
        self.port = port
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((host, port))
        time.sleep(1)
        self.recv()
        time.sleep(1)

    def recv(self):
        if sys.hexversion >= 50331648:
            response = self.client.recv(4096)
            i = 0
            for b in response:
                if b > 0:
                    i += 1
                else:
                    break

            return response[:i].decode('utf-8', 'ignore')
        return self.client.recv(4096)

    def send(self, data):
        if sys.hexversion >= 50331648:
            self.client.send(data.encode())
        else:
            self.client.send(data)

    def sendCmdVerbose(self, cmd):
        cmd = cmd + '\r\n'
        self.send(cmd)
        response = self.recv().strip()
        pos = response.rfind('\r\n>')
        return response[:pos]

    def connect(self, targetDevice):
        self.sendCmdVerbose('$connect ' + targetDevice)
        time.sleep(0.3)

    def disconnect(self, targetDevice):
        self.sendCmdVerbose('$disconnect')

    def getDeviceList(self, scan=True):
        deviceList = []
        scanWait = 2
        foundDevices = '1'
        foundDevices2 = '2'
        if scan:
            devString = self.sendCmdVerbose('$scan')
            time.sleep(scanWait)
            while foundDevices not in foundDevices2:
                foundDevices = self.sendCmdVerbose('$list')
                time.sleep(scanWait)
                foundDevices2 = self.sendCmdVerbose('$list')

        else:
            foundDevices = self.sendCmdVerbose('$list')
        response = self.sendCmdVerbose('$list')
        time.sleep(2)
        response2 = self.sendCmdVerbose('$list')
        while response != response2:
            response = response2
            response2 = self.sendCmdVerbose('$list')
            time.sleep(1)

        if 'no device' in response.lower() or 'no module' in response.lower():
            return [
             response.strip()]
        if len(response) > 0:
            if response[0].isdigit:
                sa = response.split()
                for s in sa:
                    if ')' not in s and '>' not in s:
                        deviceList.append(s)

        return deviceList