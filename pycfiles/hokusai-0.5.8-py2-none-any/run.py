# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/isacpetruzzi/Code/artsy/hokusai/hokusai/commands/run.py
# Compiled at: 2019-10-09 12:07:43
from hokusai.lib.command import command
from hokusai.services.command_runner import CommandRunner

@command()
def run(context, cmd, tty, tag, env, constraint, namespace=None):
    if tag is None:
        tag = context
    return CommandRunner(context, namespace=namespace).run(tag, cmd, tty=tty, env=env, constraint=constraint)