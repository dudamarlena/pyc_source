# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/darpy/pack.py
# Compiled at: 2017-11-03 16:11:31
from __future__ import print_function
import sys, os, tempfile
from darpy.constants import PIP_DOWNLOAD_SRC_CMD, PIP_DOWNLOAD_REQ_CMD
from darpy.common import darpy_run

def _execute_pack(args):
    packdir = tempfile.mkdtemp()
    print(('packing into {}').format(packdir), file=sys.stderr)
    for src in args.src:
        darpy_run(PIP_DOWNLOAD_SRC_CMD.format(packdir, src))

    for req in args.requirements:
        darpy_run(PIP_DOWNLOAD_REQ_CMD.format(packdir, req))

    darpy_run(('tar -C "{}" -czf "{}" .').format(packdir, os.path.join(os.getcwd(), 'darpy-pack.tgz')))
    darpy_run(('rm -r "{}"').format(packdir))


def add_pack_command(subparsers):
    pack_parser = subparsers.add_parser('pack', func=_execute_pack, help='Pack a Package')
    pack_parser.add_argument('--src', action='append', default=[], help='Add a package dir installable with pip')
    pack_parser.add_argument('--requirements', action='append', default=[], help='Add a requirements.txt file (`pip install -r` target) to the archive')