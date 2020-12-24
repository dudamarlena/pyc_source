# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\dhclientlist\drivers\tp_link\generic.py
# Compiled at: 2013-08-03 14:45:14
import requests, re, json

def get(address, username, password):
    GROUP_LENGTH = 4
    page = requests.get('http://%s/userRpm/AssignedIpAddrListRpm.htm' % address, auth=(username, password))
    list_str = re.search('(var DHCPDynList = new Array\\(([^\\)]*)\\))', page.content.replace('\n', '')).groups()[1]
    list_arr = json.loads('[%s]' % list_str)
    list_arr = list_arr[0:len(list_arr) // GROUP_LENGTH * GROUP_LENGTH]
    groups = [ {'name': list_arr[i], 'mac': list_arr[(i + 1)], 'ip': list_arr[(i + 2)], 'lease': list_arr[(i + 3)]} for i in range(len(list_arr))[0::GROUP_LENGTH]
             ]
    return groups