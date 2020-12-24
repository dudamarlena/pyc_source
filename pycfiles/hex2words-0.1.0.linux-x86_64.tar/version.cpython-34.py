# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/pfigue/Workspace/hex2words/venv-3.4-setup/lib/python3.4/site-packages/hex2words/version.py
# Compiled at: 2015-08-17 04:42:45
# Size of source mod 2**32: 1174 bytes
__version__ = '0.1.0'
__main_author_name__ = 'Pablo Figue'
__main_author_email__ = 'pfigue posteo de'
__authors__ = (
 '%s <%s>' % (__main_author_name__, __main_author_email__),)
__license__ = 'MIT'
__program_name__ = 'hex2words'
__short_description__ = 'Hexadecimal ID/Fingerprint to PGP-words list converter'
__url__ = 'https://bitbucket.org/pfigue/hex2words'

def get_platform_id():
    """Returns a string with the description of the platform.

E.g.:
    Linux-3.8.1-1-mainline; x86_64-64bit; CPython-3.4.3
"""
    import platform
    msg = '{platform}; {arch}; {python_implementation}-{python_version}'
    msg = msg.format(platform=platform.system() + '-' + platform.release(), arch=platform.machine() + '-' + platform.architecture()[0], python_implementation=platform.python_implementation(), python_version=platform.python_version())
    del platform
    return msg