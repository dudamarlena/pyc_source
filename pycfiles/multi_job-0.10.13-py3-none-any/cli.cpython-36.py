# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/joel/Workspace/dev/dev/cli.py
# Compiled at: 2020-01-12 15:33:23
# Size of source mod 2**32: 418 bytes
import sys

def generate(scripts, jobs):
    interface = 'Usage:'
    exec_path = ' '.join(sys.argv[:2])
    for name, params in [(i.name, i.params) for i in scripts + jobs]:
        interface += f"\n {exec_path} {name} {fmt(params) if params else ''} [--quiet --check]"

    return interface


def fmt(params):
    return ' '.join(sorted([f"[<{i}>]" if params[i] else f"<{i}>" for i in params.keys()]))