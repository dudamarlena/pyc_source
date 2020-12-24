# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/fftool/__init__.py
# Compiled at: 2016-05-10 01:10:37
import os
from subprocess import Popen, PIPE
__version__ = '0.1.1'
CHANNELS = [
 'release',
 'beta',
 'aurora',
 'nightly']
DEFAULT_CHANNEL = 'nightly'
HERE = os.path.dirname(os.path.realpath(__file__))
DIR_TEMP = '_temp'
DIR_TEMP_BROWSERS = os.path.join(DIR_TEMP, 'browsers')
DIR_CONFIGS = ('{0}/configs').format(HERE)
DIR_TEMP_PROFILES = os.path.join(DIR_TEMP, 'profiles')
PATH_PREFS_ROOT = os.environ.get('PATH_PREFS_ROOT')

def local(cmd):
    output = Popen(cmd, stdout=PIPE, shell=True)
    return output.stdout.read().strip()