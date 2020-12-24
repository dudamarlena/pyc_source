# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/kejser/Projects/Pygrametl/Respository/docs/_exts/version.py
# Compiled at: 2018-12-08 09:11:17
# Size of source mod 2**32: 3302 bytes
"""Extracts the version number from all source files of the pygrametl package,
   the largest version number is then computed from list of extracted numbers
   and used as the version number for the Pypi package.
"""
from distutils.version import StrictVersion
import glob, os, sys, rtdmockup
if os.path.exists('./conf.py'):
    package_path = '../'
else:
    if os.path.exists('./setup.py'):
        package_path = './'
    else:
        raise IOError('could not determine correct path of the pygrametl folder')
pygrametl_path = package_path + 'pygrametl/'
sys.path.insert(0, os.path.abspath(package_path))
sys.path.insert(0, os.path.abspath(pygrametl_path))
rtdmockup.mockModules(['pygrametl.jythonsupport', 'java', 'java.sql'])

def get_package_version():
    """Extracts the highest version number of the pygrametl python files"""
    version_number = StrictVersion('0.0')
    python_files = glob.glob(pygrametl_path + '*.py')
    for python_file in python_files:
        module_name = os.path.basename(python_file)[:-3]
        version = __import__(module_name).__version__
        if version.endswith(('a', 'b')):
            strict_version = StrictVersion(version + '1')
        else:
            strict_version = StrictVersion(version)
        if strict_version > version_number:
            version_number = strict_version

    return str(version_number)