# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/maypatha/Workspace/Github/onlinejudge95/Popper/env/lib/python3.7/site-packages/deploymaadi/configure/commands.py
# Compiled at: 2019-09-18 10:58:46
# Size of source mod 2**32: 374 bytes
from click import echo, pass_context
from . import handlers
from ..cli import entry_point

@entry_point.command(help='Initializes the system by updating and upgrading the package manager.')
@pass_context
def initialize(ctx):
    echo('Initializing configurations...')
    handlers.init(ctx, cfg=(ctx.obj.get('CONFIG')))
    echo('Client initialized successfully!!')