# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/darpy/unpack.py
# Compiled at: 2017-11-03 16:11:30
from __future__ import print_function
import sys, os, tempfile
from darpy.constants import PIP_INSTALL_CMD
from darpy.common import darpy_run

def _execute_unpack(args):
    unpackdir = tempfile.mkdtemp()
    print(('unpacking into {}').format(unpackdir), file=sys.stderr)
    darpy_run(('tar -C "{}" -xzf "{}" .').format(unpackdir, args.PKG_FILE))
    if args.virtualenv:
        pip_prefix = os.path.join(args.virtualenv, 'bin/python') + ' -m '
    else:
        pip_prefix = ''
    darpy_run(pip_prefix + PIP_INSTALL_CMD.format(unpackdir))
    darpy_run(('rm -r "{}"').format(unpackdir))


def add_unpack_command(subparsers):
    unpack_parser = subparsers.add_parser('unpack', func=_execute_unpack, help='UnPack a Package')
    unpack_parser.add_argument('PKG_FILE', help='An archive built with `darpy pack`')
    unpack_parser.add_argument('--virtualenv', help='Unpack into virtualenv (as opposed to whatever the current `pip` is wired up to)')