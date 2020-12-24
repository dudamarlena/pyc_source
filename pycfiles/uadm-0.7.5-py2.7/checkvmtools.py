# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/uadm/checkvmtools.py
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
    send_report('The computer has rebooted.', subject_prefix='INFO')
    cmd_list = [
     'mkdir -p /var/lib/uadm',
     cfb(str('\n            bash -c "\n                [[ -f /var/lib/uadm/checkkernel_`uname -r` ]] \n                &&  \n                    (echo No new kernel;) \n                ||  \n                    (echo A new kernel was installed;\n                    /usr/bin/vmware-config-tools.pl -d\n                        && (touch /var/lib/uadm/checkkernel_`uname -r`;\n                            echo VMTools were upgraded;\n                            exit 0;)\n                    )\n            "\n            '))]
    exec_cmd_list(cmd_list)


if __name__ == '__main__':
    run(sys.argv)