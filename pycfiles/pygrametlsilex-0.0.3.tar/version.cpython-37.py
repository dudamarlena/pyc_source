# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/kejser/Projects/Pygrametl/Respository/docs/_exts/version.py
# Compiled at: 2018-12-08 09:11:17
# Size of source mod 2**32: 3302 bytes
__doc__ = 'Extracts the version number from all source files of the pygrametl package,\n   the largest version number is then computed from list of extracted numbers\n   and used as the version number for the Pypi package.\n'
from distutils.version import StrictVersion
import glob, os, sys, rtdmockup
if os.path.exists('./conf.py'):
    package_path = '../'
elif os.path.exists('./setup.py'):
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