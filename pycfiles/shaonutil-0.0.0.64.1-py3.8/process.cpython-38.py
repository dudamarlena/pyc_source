# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\shaonutil\process.py
# Compiled at: 2020-04-04 17:15:37
# Size of source mod 2**32: 4554 bytes
"""Process"""
import psutil, wmi, os, subprocess

def is_process_exist(process_name):
    pids = []
    processes = list_processes()
    for process_id_, process_name_ in processes:
        if process_name_ == process_name:
            pids.append(process_id_)
        if len(pids) == 0:
            return False
        return pids


def kill_duplicate_process(process_name, log):
    """Kill a process if there is more than one instance is running."""
    if log:
        print('Killing duplicate processes')
    pids = is_process_exist(process_name)
    if len(pids) > 1:
        for pid in pids[1:]:
            killProcess_ByPid(pid)


def killProcess_ByAll(PROCNAME):
    for proc in psutil.process_iter():
        if proc.name() == PROCNAME:
            proc.kill()


def killProcess_ByPid(pid):
    p = psutil.Process(pid)
    p.terminate()


def list_processes(sort='name', save_file=False, log=False):
    processes = []
    c = wmi.WMI()
    if sort == 'pid':
        processes_pid = {}
        for process in c.Win32_Process():
            processes_pid[process.ProcessId] = process
        else:
            for pid in sorted(processes_pid.keys()):
                processes.append(processes_pid[pid])

    else:
        if sort == 'name':
            processes_name = {}
            process_strings = []
            for process in c.Win32_Process():
                processes_name[process.Name] = process
                process_strings.append(process.Name)
            else:
                process_strings.sort()
                processes = [processes_name[process_name] for process_name in process_strings]

        else:
            processes_ = []
            if save_file:
                file_ = open('running_list.txt', 'w+')
            for process in processes:
                if log:
                    print(process.ProcessId, process.Name)

        processes_.append((process.ProcessId, process.Name))
        if save_file:
            file_.write(f"{process.ProcessId} {process.Name}\n")
        if save_file:
            file_.close()
        return processes_


def computer_idle_mode():
    kill_running_app_list = [
     'kited.exe', 'sublime_text.exe', 'AoE2DE_s.exe', 'BattleServer.exe', 'conhost.exe', 'python.exe']


def obj_details_dump(obj):
    """check dump"""
    for attr in dir(obj):
        print('obj.%s = %r' % (attr, getattr(obj, attr)))