# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/toil/utils/toilUpdateEC2Instances.py
# Compiled at: 2020-04-03 17:41:24
# Size of source mod 2**32: 1327 bytes
"""
Updates Toil's internal list of EC2 instance types.
"""
from __future__ import absolute_import
import logging, socket
from toil.lib.ec2nodes import updateStaticEC2Instances
logger = logging.getLogger(__name__)

def internetConnection():
    """
    Returns True if there is an internet connection present, and False otherwise.

    :return:
    """
    try:
        socket.create_connection(('www.stackoverflow.com', 80))
        return True
    except OSError:
        pass

    return False


def main():
    if not internetConnection():
        raise RuntimeError('No internet.  Updating the EC2 Instance list requires internet.')
    updateStaticEC2Instances()


if __name__ == '__main__':
    main()