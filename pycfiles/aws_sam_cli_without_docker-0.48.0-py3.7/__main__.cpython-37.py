# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/samcli/__main__.py
# Compiled at: 2020-03-21 12:32:11
# Size of source mod 2**32: 318 bytes
"""
Invokable Module for CLI

python -m samcli
"""
from samcli.cli.main import cli
if __name__ == '__main__':
    cli(prog_name='sam')