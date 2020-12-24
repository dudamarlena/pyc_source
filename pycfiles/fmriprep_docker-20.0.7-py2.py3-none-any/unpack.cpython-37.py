# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-aejasjrz/wheel/wheel/cli/unpack.py
# Compiled at: 2020-05-05 12:41:47
# Size of source mod 2**32: 673 bytes
from __future__ import print_function
import os.path, sys
from ..wheelfile import WheelFile

def unpack(path, dest='.'):
    """Unpack a wheel.

    Wheel content will be unpacked to {dest}/{name}-{ver}, where {name}
    is the package name and {ver} its version.

    :param path: The path to the wheel.
    :param dest: Destination directory (default to current directory).
    """
    with WheelFile(path) as (wf):
        namever = wf.parsed_filename.group('namever')
        destination = os.path.join(dest, namever)
        print(('Unpacking to: {}...'.format(destination)), end='')
        sys.stdout.flush()
        wf.extractall(destination)
    print('OK')