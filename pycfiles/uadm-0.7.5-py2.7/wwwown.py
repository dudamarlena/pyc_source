# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/uadm/wwwown.py
# Compiled at: 2012-07-04 08:12:35
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
     'chown -R www-data:www-data %s' % CONF_MAP['UADM_DOCROOT']]
    exec_cmd_list(cmd_list)


if __name__ == '__main__':
    run(sys.argv)