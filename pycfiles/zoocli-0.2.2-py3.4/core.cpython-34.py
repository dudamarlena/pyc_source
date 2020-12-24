# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/zoocli/core.py
# Compiled at: 2015-05-23 16:13:00
# Size of source mod 2**32: 333 bytes
from climb import Climb
from functools import partial
from zoocli.args import ZooArgs
from zoocli.commands import ZooCommands
from zoocli.completer import ZooCompleter
ZooCLI = partial(Climb, 'zoocli', args=ZooArgs, commands=ZooCommands, completer=ZooCompleter)