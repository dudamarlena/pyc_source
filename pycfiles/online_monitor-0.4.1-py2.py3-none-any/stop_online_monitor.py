# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/davidlp/git/online_monitor/online_monitor/stop_online_monitor.py
# Compiled at: 2018-07-05 04:39:41
import psutil

def main():
    for proc in psutil.process_iter():
        if any(name in proc.name() for name in ['start_producer', 'start_converter', 'start_online']) or any(name in ('').join(proc.cmdline()) for name in ['start_producer', 'start_converter', 'start_online']):
            proc.kill()


if __name__ == '__main__':
    main()