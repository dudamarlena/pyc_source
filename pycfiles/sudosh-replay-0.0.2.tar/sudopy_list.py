# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /var/log/bin/release/sudosh/app/sudopy_list.py
# Compiled at: 2014-06-03 11:14:08
import subprocess

def sudo_list():
    sudoList = []
    handle = subprocess.Popen('sudosh-replay', shell=True, stdout=subprocess.PIPE)
    output = handle.communicate()[0]
    llist = output.split('\n')
    for line in llist:
        item = line.split()
        List = []
        for one in item:
            one.strip()
            List.append(one)

        if len(List) != 0:
            dt = List[0].split('/')
            dt = [
             dt[2], dt[0], dt[1]]
            List[0] = ('/').join(dt)
            sudoList.append(List)

    return sudoList


def sudolist_filterbytime(sudolist=[], filter={'date': ''}):
    sudo_rt = []
    if sudolist is None:
        return sudo_rt
    else:
        if filter['date'] == '':
            return sudolist
        for sudo in sudolist:
            if filter['date'] == sudo[0]:
                sudo_rt.append(sudo)

        return sudo_rt