# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/niflow_manager/cli/main.py
# Compiled at: 2020-03-13 12:49:48
# Size of source mod 2**32: 307 bytes
import click
from .. import __version__
from .init import init
from .install import install
from .build import build
from .test import test

@click.group()
@click.version_option(__version__)
def main():
    pass


main.command()(init)
main.command()(install)
main.command()(build)
main.command()(test)