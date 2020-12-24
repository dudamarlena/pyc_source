# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ale/progr/github/wasp-general/wasp_general/version.py
# Compiled at: 2018-01-17 05:18:06
# Size of source mod 2**32: 1977 bytes
import os, json, subprocess
with open(os.path.join(os.path.dirname(__file__), 'package.json'), 'r') as (f):
    __package_data__ = json.load(f)

def package_version():
    result = __package_data__['numeric_version']
    if __package_data__['dev_suffix'] is True:
        try:
            cwd = os.getcwd()
            try:
                os.chdir(os.path.dirname(__file__))
                with open(os.devnull, 'w') as (f):
                    output = subprocess.check_output(['git', 'rev-parse', 'HEAD'], stderr=f)
                if isinstance(output, bytes) is True:
                    output = output.decode()
                result += '.dev%s' % output[:7]
            finally:
                os.chdir(cwd)

        except (subprocess.CalledProcessError, OSError):
            result += '--'

    return result


__author__ = __package_data__['author']
__email__ = __package_data__['author_email']
__credits__ = __package_data__['credits']
__license__ = __package_data__['license']
__copyright__ = __package_data__['copyright']
__status__ = __package_data__['status']
__version__ = package_version()