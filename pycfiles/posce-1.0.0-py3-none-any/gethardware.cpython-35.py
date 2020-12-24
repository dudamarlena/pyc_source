# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win-amd64\egg\procode\tools\gethardware.py
# Compiled at: 2019-09-04 06:17:32
# Size of source mod 2**32: 7598 bytes
import psutil, datetime, time, platform, subprocess, socket, uuid
from urllib import request
from tools import md5

class GethardWare:
    _sys = 'Windows'

    def __init__(self):
        self._sys = platform.system()

    def get_nowdatetime(self):
        now_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        return now_time

    def get_cpucount(self):
        cpu_count = psutil.cpu_count(logical=False)
        cpu = str(psutil.cpu_percent(1)) + '%'
        r_vlue = {'r_vcpucount': cpu_count, 'r_cpu': cpu}
        return r_vlue

    def get_ram(self):
        free = str(round(psutil.virtual_memory().free / 1073741824.0, 2))
        total = str(round(psutil.virtual_memory().total / 1073741824.0, 2))
        memory = int(psutil.virtual_memory().total - psutil.virtual_memory().free) / float(psutil.virtual_memory().total)
        r_total = '%s G' % total
        r_free = '%s G' % free
        r_memory = '%s %%' % int(memory * 100)
        r_value = {'r_total': r_total, 'r_free': r_free, 'r_memory': r_memory}
        return r_value

    def get_sysstarttimeandusers(self):
        sys_starttime = datetime.datetime.fromtimestamp(psutil.boot_time()).strftime('%Y-%m-%d %H:%M:%S')
        users_count = len(psutil.users())
        users_list = ','.join([u.name for u in psutil.users()])
        r_value = {'r_sys_starttime': sys_starttime, 'r_users': users_list, 'r_usercount': users_count}
        return r_value

    def get_netcard(self):
        netcard_info = []
        net = psutil.net_io_counters()
        bytes_sent = '{0:.2f} Mb'.format(net.bytes_recv / 1024 / 1024)
        bytes_rcvd = '{0:.2f} Mb'.format(net.bytes_sent / 1024 / 1024)
        netcard_info.append(('rcvd_bytes', bytes_rcvd))
        netcard_info.append(('sent_bytes', bytes_sent))
        return netcard_info

    def get_ipAndMac(self):
        ipmac = []
        hostname = socket.gethostname()
        ip = socket.gethostbyname(hostname)
        try:
            res = request.urlopen('http://pv.sohu.com/cityjson')
            request_info = res.read().decode('gbk')
            gw_ip = str(request_info).split('=')[1].split(',')[0].split('"')[3]
        except Exception as e:
            gw_ip = ''

        ipmac.append(('local_ip', ip))
        ipmac.append(('gw_ip', gw_ip))
        mac = uuid.UUID(int=uuid.getnode()).hex[-12:]
        n_mac = ':'.join([mac[e:e + 2] for e in range(0, 11, 2)])
        print(n_mac)
        ipmac.append(('macaddress', n_mac))
        return ipmac

    def get_disk(self):
        r_disk = []
        io = psutil.disk_partitions()
        print(io)
        for i in io:
            try:
                disk_name = str(i.device).split(':')[0] + '盘符'
                o = psutil.disk_usage(i.device)
                r_total = str(int(o.total / 1073741824.0)) + 'G'
                r_used = str(int(o.used / 1073741824.0)) + 'G'
                r_free = str(int(o.free / 1073741824.0)) + 'G'
                r_disk.append((str(disk_name), (r_total, r_used, r_free)))
            except:
                continue

        return r_disk

    def get_macos(self):
        process = subprocess.Popen("ioreg -rd1 -c IOPlatformExpertDevice | awk '/IOPlatformSerialNumber/ { print $3; }'", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        command_output = process.stdout.read().decode('utf-8')
        print(command_output)
        return str(command_output).replace('"', '').replace('\n', '').strip()

    def get_wincpuid(self):
        process = subprocess.Popen('wmic cpu get ProcessorId', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        command_output = process.stdout.read()
        result = str(command_output, 'ascii')
        if result and len(result) > 11:
            if 'ERROR' in result:
                print(-1, '获取CPU地址失败')
            cpuid = result[11:].strip()
        else:
            cpuid = ''
        process = subprocess.Popen('wmic DISKDRIVE get SerialNumber /value', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        command_output = process.stdout.read()
        result = str(command_output, 'ascii').replace('\r', '').replace('\n', '').replace(' ', '')
        try:
            disknid = result.split('SerialNumber=')[1]
        except Exception as e:
            disknid = ''

        if not disknid:
            mac = uuid.UUID(int=uuid.getnode()).hex[-12:]
            n_mac = ':'.join([mac[e:e + 2] for e in range(0, 11, 2)])
        else:
            n_mac = ''
        return cpuid + disknid + n_mac

    def get_cpuidOrSerialNumber(self):
        try:
            onlyNum = ''
            sys = self._sys
            if sys == 'Windows':
                onlyNum = self.get_wincpuid()
            elif sys == 'Darwin':
                onlyNum = self.get_macos()
            onlyNum = md5.genearteMD5(onlyNum)
            return onlyNum
        except Exception as e:
            raise e


if __name__ == '__main__':
    ghw = GethardWare()
    sys = ghw._sys
    if sys == 'Windows':
        print(ghw.get_wincpuid())
        print('当前操作系统是：' + sys)
    elif sys == 'Darwin':
        print('当前操作系统是：Mac')
        print(ghw.get_macos())
else:
    if sys == 'Linux':
        print('当前操作系统是：' + sys)
    print('')
    print(ghw.get_nowdatetime())
    print('')
    cpus = ghw.get_cpucount()
    for k, v in cpus.items():
        print(v)

    print('')
    rams = ghw.get_ram()
    for k1, v1 in rams.items():
        print(str(k1) + ':' + str(v1))

    print('')
    users_time = ghw.get_sysstarttimeandusers()
    for k2, v2 in users_time.items():
        print(v2)

    print('')
    netcards = ghw.get_netcard()
    for k3, v3 in netcards:
        print(v3)

    print('')
    diskinfo = ghw.get_disk()
    for k4, v4 in diskinfo:
        print(k4 + '\n')
        for i in range(len(v4)):
            print(str(v4[i]) + '\n')