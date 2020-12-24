# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/springheel/command_line.py
# Compiled at: 2019-12-15 23:20:58
# Size of source mod 2**32: 248 bytes
import springheel

def build():
    """Generate a Springheel site."""
    springheel.build()


def init():
    """Initialize a Springheel project."""
    springheel.init()


def version():
    """Print version information."""
    springheel.version()