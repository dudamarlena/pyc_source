# uncompyle6 version 3.7.4
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/net6mon/uuid.py
# Compiled at: 2006-06-20 07:07:59


def unixgetaddr(program):
    """Get the hardware address on a Unix machine."""
    from os import popen
    for line in popen(program):
        words = line.lower().split()
        if 'hwaddr' in words:
            addr = words[(words.index('hwaddr') + 1)]
            return int(addr.replace(':', ''), 16)
        if 'ether' in words:
            addr = words[(words.index('ether') + 1)]
            return str(addr.replace(':', ''))


def wingetaddr(program):
    """Get the hardware address on a Windows machine."""
    from os import popen
    for line in popen(program + ' /all'):
        if line.strip().lower().startswith('physical address'):
            addr = line.split(':')[(-1)].strip()
            return str(addr.replace('-', ''))


def getaddr():
    """Get the hardware address as a 48-bit integer."""
    from os.path import join, isfile
    for dir in ['/sbin', '/usr/sbin', 'c:\\windows', 'c:\\windows\\system', 'c:\\windows\\system32']:
        if isfile(join(dir, 'ifconfig')):
            return str(unixgetaddr(join(dir, 'ifconfig')))
        if isfile(join(dir, 'ipconfig.exe')):
            return str(wingetaddr(join(dir, 'ipconfig.exe')))