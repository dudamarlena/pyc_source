# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win-amd64\egg\aigpy\systemHelper.py
# Compiled at: 2019-10-26 00:11:28
# Size of source mod 2**32: 2686 bytes
__doc__ = '\n@File    :   systemHelper.py\n@Time    :   2018/12/20\n@Author  :   Yaron Huang \n@Version :   1.0\n@Contact :   yaronhuang@qq.com\n@Desc    :   \n'
import os, platform, subprocess

def getOwnPath(in__file__):
    return os.path.dirname(os.path.realpath(in__file__))


def isWindows():
    sysName = platform.system()
    return sysName == 'Windows'


def isLinux():
    sysName = platform.system()
    return sysName == 'Linux'


def getProcessID(name):
    """get processid by name"""
    try:
        retid = []
        if isLinux():
            lines = os.popen('ps aux | grep "' + name + '" | grep -v grep').readlines()
            if len(lines) <= 0:
                return []
            for item in lines:
                array = item.split()
                retid.append(int(array[1]))

        else:
            import psutil
            pidList = list(psutil.process_iter())
            for item in pidList:
                stri = str(item)
                stri = stri[15:-1]
                itname = stri[stri.find('name') + 6:-1]
                indx = itname.find(',')
                if indx >= 0:
                    itname = itname[0:indx - 1]
                if itname != name:
                    continue
                pid = stri[stri.find('pid') + 4:stri.find('name') - 2]
                retid.append(int(pid))

        return retid
    except:
        return []


def killProcess(proid):
    try:
        if isLinux():
            os.popen('kill -9 ' + str(proid))
            lines = os.popen('ps ' + str(proid)).readlines()
            if len(lines) <= 1:
                return True
        else:
            lines = os.popen('tasklist | findstr ' + str(proid)).readlines()
            if len(lines) <= 0:
                return True
            unread2 = os.popen('taskkill /pid %s /f' % str(proid))
        return False
    except:
        return False


def openPort(port):
    cmds = [
     'iptables -I INPUT -m state --state NEW -m tcp -p tcp --dport ' + str(port) + ' -j ACCEPT',
     'iptables -I INPUT -m state --state NEW -m udp -p udp --dport ' + str(port) + ' -j ACCEPT',
     'ip6tables -I INPUT -m state --state NEW -m tcp -p tcp --dport ' + str(port) + ' -j ACCEPT',
     'ip6tables -I INPUT -m state --state NEW -m udp -p udp --dport ' + str(port) + ' -j ACCEPT']
    for item in cmds:
        subprocess.call(item, shell=False)