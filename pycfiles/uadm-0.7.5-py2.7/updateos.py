# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/uadm/updateos.py
# Compiled at: 2012-07-03 11:55:48
__author__ = 'Pierre-Yves Langlois'
__copyright__ = 'https://github.com/pylanglois/uadm/blob/master/LICENCE'
__credits__ = ['Pierre-Yves Langlois']
__license__ = 'BSD'
__version__ = '1.0'
__maintainer__ = 'Pierre-Yves Langlois'
__status__ = 'Production'
import sys
from uadm.uadmcore import *

def run(args=[]):
    cmd_list = [
     'apt-get update',
     'apt-get dist-upgrade -y',
     'sleep 1',
     'bash -c "[[ -f /var/run/reboot-required ]] && reboot now || echo \'no need to reboot\' "']
    exec_cmd_list(cmd_list)


if __name__ == '__main__':
    run(sys.argv)