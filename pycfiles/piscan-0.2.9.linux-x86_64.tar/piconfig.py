# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/piscan/piconfig.py
# Compiled at: 2016-03-31 19:41:51
import urllib2, re, sys

def getMAC(interface):
    try:
        str = open('/sys/class/net/' + interface + '/address').read()
    except:
        str = '00:00:00:00:00:00'

    return str[0:17]


configurl = 'http://www.rxwave.com/config/' + getMAC('eth0')
response = urllib2.urlopen(configurl)
configfl = response.read()
orig = configfl.splitlines(configfl.count('\n'))
target = open('/etc/piscan/piscan.ini', 'r+')
origfl = target.read()
newconfig = ''
for line in orig:
    newln = line
    if re.match('^RID:\\s', line, re.I):
        newln = re.sub('^RID:\\s', line, origfl)
    newconfig = newconfig + newln

print newconfig