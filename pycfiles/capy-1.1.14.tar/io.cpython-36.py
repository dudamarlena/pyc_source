# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/christian/documented/ctf/ctf/io.py
# Compiled at: 2020-04-23 19:17:14
# Size of source mod 2**32: 433 bytes
__doc__ = 'I/O module.'
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