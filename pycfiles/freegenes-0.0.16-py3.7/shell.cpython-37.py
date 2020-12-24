# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/freegenes/client/shell.py
# Compiled at: 2019-09-23 14:12:20
# Size of source mod 2**32: 1257 bytes
"""

Copyright (C) 2019 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""
from freegenes.main import Client

def main(args, options, parser):
    lookup = {'ipython':ipython, 
     'python':python, 
     'bpython':run_bpython}
    shells = [
     'ipython', 'python', 'bpython']
    client = Client()
    for shell in shells:
        try:
            return lookup[shell](client)
        except ImportError:
            pass


def ipython(client):
    """give the user an ipython shell
    """
    try:
        from IPython import embed
    except ImportError:
        return python(client)
    else:
        embed(using=False)


def run_bpython(client):
    """give the user a bpython shell
    """
    try:
        import bpython
    except ImportError:
        return python(client)
    else:
        bpython.embed(locals_={'client': client})


def python(client):
    """give the user a python shell
    """
    import code
    code.interact(local={'client': client})