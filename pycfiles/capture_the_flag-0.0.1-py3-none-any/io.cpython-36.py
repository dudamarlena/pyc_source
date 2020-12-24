# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/christian/documented/ctf/ctf/io.py
# Compiled at: 2020-04-23 19:17:14
# Size of source mod 2**32: 433 bytes
"""I/O module."""
import pkg_resources

def resource_path(filename):
    """Returns the path to a resource.

    Args:
        filename (:obj:`str`): Filename to get path to, must be in
            resources directory.

    Returns:
        :obj:`str`: Path to <filename>, relative to resources directory.

    """
    path = pkg_resources.resource_filename(__name__, f"resources/{filename}")
    return path