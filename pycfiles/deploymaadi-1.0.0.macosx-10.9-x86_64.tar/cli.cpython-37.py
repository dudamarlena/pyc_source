# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/maypatha/Workspace/Github/onlinejudge95/Popper/env/lib/python3.7/site-packages/deploymaadi/cli.py
# Compiled at: 2019-09-18 09:48:49
# Size of source mod 2**32: 427 bytes
import json, pathlib
from click import group, pass_context

@group()
@pass_context
def entry_point(ctx):
    ctx.ensure_object(dict)
    config_file_path = pathlib.Path.cwd() / 'etc' / 'config.json'
    with config_file_path.open(mode='r') as (fp):
        config_object = json.load(fp)
    ctx.obj['CONFIG'] = config_object


from .configure import commands as configure
entry_point.add_command(configure.initialize)