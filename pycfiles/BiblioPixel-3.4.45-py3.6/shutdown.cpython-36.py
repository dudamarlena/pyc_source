# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bibliopixel/commands/shutdown.py
# Compiled at: 2019-08-11 12:22:47
# Size of source mod 2**32: 301 bytes
"""
Send an interrupt signal to a BiblioPixel process running on this
machine to kill it

DEPRECATED: use
.. code-block:: bash

    $ kill -int `bpa-pid`

"""
DESCRIPTION = '\nExample:\n`$ bp shutdown`\n\n'
from ..util.signal_handler import make_command
add_arguments, run = make_command('SIGINT')