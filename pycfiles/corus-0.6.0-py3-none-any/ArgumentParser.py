# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/zwsun/workspace/python/corunner/corunner/common/ArgumentParser.py
# Compiled at: 2013-11-05 08:27:51
import NetUtil

def parseHosts(hosts):
    localIP = NetUtil.getLocalIP()
    nodes = []
    splits = hosts.split(',')
    for split in splits:
        if split.find('..') > 0:
            segments = split.split('..')
            if len(segments) != 2:
                raise ValueError('Unknown format of hosts: %s' % hosts)
            if segments[1].find('.') >= 0:
                raise ValueError('Unknown format of hosts: %s' % hosts)
            start = 0
            end = int(segments[1])
            port = None
            if segments[0].find(':') > 0:
                port = segments[0].split(':')[1]
                start = int(segments[0][segments[0].rfind('.') + 1:segments[0].rfind(':')])
            else:
                start = int(segments[0][segments[0].rfind('.') + 1:])
            prefix = segments[0][:segments[0].rfind('.') + 1]
            for i in range(start, end + 1):
                ip = prefix + str(i)
                if NetUtil.isLocal(ip):
                    ip = localIP
                if port == None:
                    nodes.append(ip)
                else:
                    nodes.append(ip + ':' + port)

        elif NetUtil.isLocal(split):
            nodes.append(localIP)
        else:
            nodes.append(split)

    return nodes