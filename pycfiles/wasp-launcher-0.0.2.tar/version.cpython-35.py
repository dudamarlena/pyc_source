# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ale/progr/wasp-launcher/extra/build/pypi_build/wasp_launcher/version.py
# Compiled at: 2017-12-19 04:40:13
# Size of source mod 2**32: 1360 bytes
import subprocess

def revision():
    status, output = subprocess.getstatusoutput('git rev-parse HEAD')
    if status == 0:
        return output[:7]
    return '--'


__author__ = 'Ildar Gafurov'
__numeric_version__ = '0.0.2'
__version__ = '%s.dev%s' % (__numeric_version__, revision())
__credits__ = ['Ildar Gafurov']
__license__ = 'GNU Lesser General Public License v3'
__copyright__ = 'Copyright 2016-2017, The Wasp-launcher'
__email__ = 'dev@binblob.com'
__status__ = 'Development'