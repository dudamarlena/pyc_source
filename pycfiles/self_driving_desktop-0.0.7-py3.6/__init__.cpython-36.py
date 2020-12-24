# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/self_driving_desktop/__init__.py
# Compiled at: 2019-05-11 16:22:21
# Size of source mod 2**32: 426 bytes
import click
from self_driving_desktop import parser as P
from self_driving_desktop import recorder as R

@click.command()
@click.argument('playlist')
@click.option('--record', is_flag=True, help='Record to a playlist.')
def drive(playlist, record):
    if record is True:
        doRecord(playlist)
    else:
        doPlay(playlist)


def doPlay(playlist):
    P.run(playlist)


def doRecord(playlist):
    R.do(playlist)