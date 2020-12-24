# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/lukasz/develop/workspace/monolith/build/lib/monolith/__init__.py
# Compiled at: 2013-11-25 18:24:00
# Size of source mod 2**32: 311 bytes
"""
monolith is an argparse based command line interface framework
"""
VERSION = (0, 3, 3, 'dev')
__version__ = '.'.join(str(each) for each in VERSION[:4])

def get_version():
    """
    Returns shorter version (digit parts only) as string.
    """
    return '.'.join(str(each) for each in VERSION[:4])