# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/helpme/utils/memory.py
# Compiled at: 2019-12-09 18:49:03
# Size of source mod 2**32: 2028 bytes
"""
memory.py: part of the helpme package and executable
simple util for getting memory of some process

Still figuring this out, going to be something along these lines
sleep 3 & python memory.py --pid `echo $!`

or

sleep 3 & python -m memory --pid `echo $!`

"""
import argparse, logging, os, psutil, sys, time

def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--pid', type=int, dest='pid', default=None)
    parser.add_argument('--timeout', type=int, dest='timeout', default=1)
    return parser


def get_pid(pid=None):
    """get_pid will return a pid of interest. First we use given variable,
    then environmental variable PID, and then PID of running process
    """
    if pid == None:
        if os.environ.get('PID', None) != None:
            pid = int(os.environ.get('PID'))
        else:
            pid = os.getpid()
    print('pid is %s' % pid)
    return pid


def get_memory_usage(pid=None, timeout=1):
    """get_memory_usage returns a dictionary of resident set size (rss) and virtual
    memory size (vms) for a process of interest, for as long as the process is running
    :param pid: the pid to use:
    :param timeout: the timeout
    :: notes
  
      example: 
 
          sleep 3 & exec python -m memory "$!"
    """
    rss = []
    vms = []
    pid = get_pid(pid)
    process = psutil.Process(pid)
    print(process.status())
    while process.status() == 'running':
        mem = process.memory_info()
        rss.append(mem.rss)
        vms.append(mem.vms)
        time.sleep(timeout)

    result = {'rss':rss,  'vms':vms}
    print(result)


if __name__ == '__main__':
    parser = get_parser()
    args = parser.parse_args()
    get_memory_usage(pid=(args.pid), timeout=(args.timeout))