# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: hokusai/commands/build.py
# Compiled at: 2019-10-09 12:07:43
import os
from hokusai.lib.command import command
from hokusai.services.docker import Docker

@command()
def build(filename):
    Docker().build(filename)