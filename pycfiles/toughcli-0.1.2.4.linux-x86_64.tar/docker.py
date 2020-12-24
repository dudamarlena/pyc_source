# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python2.7/site-packages/toughcli/service/docker.py
# Compiled at: 2016-04-12 04:10:48
import os

def auto_install():
    os.system('curl -sSL https://get.daocloud.io/docker | sh')
    os.system('curl -L https://get.daocloud.io/docker/compose/releases/download/1.5.2/docker-compose-`uname -s`-`uname -m` > /usr/local/bin/docker-compose')
    os.system('chmod +x /usr/local/bin/docker-compose')
    os.system('chmod +x `which docker-compose`')
    os.system('chkconfig docker on')
    os.system('service docker start')


def update():
    os.system('chmod +x `which docker-compose`')