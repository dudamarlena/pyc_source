# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bibliopixel/commands/kill.py
# Compiled at: 2019-08-11 12:22:47
# Size of source mod 2**32: 328 bytes
"""
Send a kill signal to a BiblioPixel process running on this
machine to abruptly kill it

DEPRECATED: use

.. code-block:: bash

    $ kill -kill `bpa-pid`

"""
DESCRIPTION = '\nExample:\n\n.. code-block:: bash\n\n    $ bp kill\n\n'
from ..util.signal_handler import make_command
add_arguments, run = make_command('SIGKILL')