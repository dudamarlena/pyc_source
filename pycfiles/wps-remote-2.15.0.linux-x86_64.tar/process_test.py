# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/alessio/Envs/remote-wps/lib/python2.7/site-packages/wpsremote/process_test.py
# Compiled at: 2016-03-16 12:38:32
import os, psutil, time
logPath = 'C:\\tmp\\processlogs'
if not os.path.exists(logPath):
    os.mkdir(logPath)
separator = '-' * 150
format = '%7s %7s %7s %7s %7s %12s %12s %30s %30s, %s'
format2 = '%7s %7s %7s %7.4f %7.2f %12s %12s %30s %30s, %s'
while 1:
    logPath = 'C:\\tmp\\processlogs\\procLog%i.log' % int(time.time())
    f = open(logPath, 'w')
    f.write(separator + '\n')
    f.write(time.ctime() + '\n')
    f.write(format % ('PID', 'PPID', 'STATUS', '%CPU', '%MEM', 'VMS', 'RSS', 'USER',
                      'NAME', 'PATH'))
    f.write('\n')
    for proc in psutil.process_iter():
        process = psutil.Process(proc.pid).as_dict()
        pid = str(process['pid'])
        ppid = str(process['ppid'])
        status = process['status']
        cpu_percent = process['cpu_percent']
        mem_percent = process['memory_percent']
        rss = str(process['memory_info'].rss)
        vms = str(process['memory_info'].vms)
        username = process['username']
        name = process['name']
        path = process['cwd']
        f.write(format2 % (pid, ppid, status, cpu_percent, mem_percent, vms, rss, username, name, path))
        f.write('\n\n')

    f.close()
    print 'Finished log update!'
    time.sleep(300)
    print 'writing new log data!'