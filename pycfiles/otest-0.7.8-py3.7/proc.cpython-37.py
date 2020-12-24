# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/otest/proc.py
# Compiled at: 2019-04-01 13:24:38
# Size of source mod 2**32: 2067 bytes
import datetime, psutil

def find_test_instance(iss, tag):
    match = {'-i':iss, 
     '-t':tag}
    for proc in psutil.process_iter():
        try:
            cmd = proc.cmdline()
        except psutil.AccessDenied:
            continue

        if len(cmd) < 5:
            continue
        flag = 0
        for first, second in match.items():
            try:
                i = cmd.index(first)
            except ValueError:
                break

            if cmd[(i + 1)] != second:
                break
            else:
                flag += 1

        if flag == len(match):
            return proc


def find_test_instances(prog):
    pid = {}
    for proc in psutil.process_iter():
        _name = proc.name()
        if _name in ('python', 'python3', 'Python', 'Python3'):
            try:
                cmd = proc.cmdline()
            except psutil.AccessDenied:
                continue

            if len(cmd) > 5 and cmd[1].endswith(prog):
                i = cmd.index('-i')
                iss = cmd[(i + 1)]
                i = cmd.index('-t')
                tag = cmd[(i + 1)]
                i = cmd.index('-p')
                port = cmd[(i + 1)]
                since = datetime.datetime.fromtimestamp(proc.create_time()).strftime('%Y-%m-%d %H:%M:%S')
                pid[proc.pid] = {'iss':iss,  'tag':tag,  'port':port,  'since':since}

    return pid


def kill_test_instance(iss, tag):
    proc = find_test_instance(iss, tag)
    if proc:
        proc.kill()


def kill_process(pid):
    proc = psutil.Process(pid)
    proc.kill()


def isrunning(iss, tag):
    proc = find_test_instance(iss, tag)
    if proc:
        return proc.pid
    return 0


def pid_isrunning(pid):
    proc = psutil.Process(pid)
    return proc


if __name__ == '__main__':
    inst = find_test_instances('op_test_tool.py')
    print(inst)