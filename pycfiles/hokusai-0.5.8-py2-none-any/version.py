# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/isacpetruzzi/Code/artsy/hokusai/hokusai/commands/version.py
# Compiled at: 2019-10-09 12:07:43
import os
from hokusai.lib.command import command
from hokusai.lib.common import print_green
from hokusai.version import VERSION

@command(config_check=False)
def version():
    print_green(VERSION)