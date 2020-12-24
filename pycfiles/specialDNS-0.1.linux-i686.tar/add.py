# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/user/.local/lib/python2.7/site-packages/specialDNS/add.py
# Compiled at: 2012-01-01 16:36:35
import info

def add():
    print ('Current names:', info.names)
    print 'Enter a name like verge.info.tm you want to make special.'
    name = raw_input('>').strip()
    if len(name) == 0:
        return
    if raw_input("Is '" + name + "' OK? y/n").startswith('y'):
        info.names += (name,)
        info.save()


if __name__ == '__main__':
    add()