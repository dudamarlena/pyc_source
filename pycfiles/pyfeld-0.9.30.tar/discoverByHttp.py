# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: pyfeld/discoverByHttp.py
# Compiled at: 2017-11-23 08:41:51
import threading, urllib3
from pyfeld.getRaumfeld import RaumfeldDeviceSettings

class DiscoverByHttp:

    def __init__(self):
        self.found_ip = None
        local_ip = RaumfeldDeviceSettings.get_local_ip_address()
        decomposed = local_ip.split('.')
        self.processes = list()
        for i in range(1, 256):
            ip = decomposed[0] + '.' + decomposed[1] + '.' + decomposed[2] + '.' + str(i)
            p = 'http://' + ip + ':47365/WelcomePage'
            proc = threading.Thread(target=self.get, args=(p, ip, 2.0, 7.0))
            proc.start()
            self.processes.append(proc)

        for proc in self.processes:
            proc.join()

        return

    def kill_after_found(self):
        for proc in self.processes:
            proc.kill()

    def get(self, url, ip, timeoutConnect, timeoutRead):
        headers = {'CONTENT-TYPE': 'text/xml; charset="utf-8"', 
           'USER-AGENT': 'uPNP/1.0'}
        try:
            timeout = urllib3.util.timeout.Timeout(connect=timeoutConnect, read=timeoutRead)
            http = urllib3.PoolManager(timeout=timeout)
            r = http.request('GET', url, headers=headers)
            if r.status == 200:
                self.found_ip = ip
                print 'found ' + ip
                self.kill_after_found()
        except Exception as e:
            pass

    def found_IP(self):
        return self.found_ip


if __name__ == '__main__':
    db = DiscoverByHttp()
    print db.found_IP()