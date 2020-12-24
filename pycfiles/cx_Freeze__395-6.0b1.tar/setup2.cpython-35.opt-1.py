# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: \.\cx_Freeze\samples\pytz\setup2.py
# Compiled at: 2020-01-04 18:05:46
# Size of source mod 2**32: 883 bytes
__doc__ = 'A setup script to demonstrate build using pytz\n   This version requires the zoneinfo in the file system\n'
import distutils, sys, os
from cx_Freeze import setup, Executable
dir_name = 'exe.%s-%s.2' % (
 distutils.util.get_platform(), sys.version[0:3])
build_exe = os.path.join('build', dir_name)
setup(name='test_pytz', version='0.2', description='cx_Freeze script to test pytz', executables=[
 Executable('test_pytz.py')], options={'build_exe': {'zip_include_packages': ['*'], 
               'zip_exclude_packages': ['pytz'], 
               'build_exe': build_exe}})