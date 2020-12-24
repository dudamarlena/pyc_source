# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/joel/Workspace/dev/utils/colours.py
# Compiled at: 2020-01-30 11:24:07
# Size of source mod 2**32: 1589 bytes
"""
Utility functions for adding colour codes to strings
"""

def bold(string: str) -> str:
    """Add bold colour codes to string
    
    Args:
        string (str): Input string
    
    Returns:
        str: Bold string
    """
    return '\x1b[1m' + string + '\x1b[0m'


def underline(string: str) -> str:
    """Add underline colour codes to string
    
    Args:
        string (str): Input string
    
    Returns:
        str: Underlined string
    """
    return '\x1b[4m' + string + '\x1b[0m'


def fail(string: str) -> str:
    """Add fail colour codes to string
    
    Args:
        string (str): Input string
    
    Returns:
        str: Fail string
    """
    return '\x1b[91m' + string + '\x1b[0m'


def green(string: str) -> str:
    """Add green colour codes to string
    
    Args:
        string (str): Input string
    
    Returns:
        str: Green string
    """
    return '\x1b[92m' + string + '\x1b[0m'


def warn(string: str) -> str:
    """Add warn colour codes to string
    
    Args:
        string (str): Input string
    
    Returns:
        str: Warn string
    """
    return '\x1b[93m' + string + '\x1b[0m'


def blue(string: str) -> str:
    """Add blue colour codes to string
    
    Args:
        string (str): Input string
    
    Returns:
        str: Blue string
    """
    return '\x1b[94m' + string + '\x1b[0m'


def header(string: str) -> str:
    """Add header colour codes to string
    
    Args:
        string (str): Input string
    
    Returns:
        str: Header string
    """
    return '\x1b[95m' + string + '\x1b[0m'