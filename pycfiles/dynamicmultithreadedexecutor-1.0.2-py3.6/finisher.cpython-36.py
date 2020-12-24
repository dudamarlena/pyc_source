# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/dynamicmultithreadedexecutor/finisher.py
# Compiled at: 2017-12-28 17:04:54
# Size of source mod 2**32: 1814 bytes
from six.moves.queue import Queue, Empty
import six, logging
from .utils import get_num_input_vars
LOGGER = logging.getLogger(__name__)

def finisher(outq, output_queue_handler, kill_boolean):
    """
    execute output_func one time per item in outq
    output_func will be provided an item from outq and only that

    this function is executed in it's own thread but only single threaded
    :param outq: output queue that we will pull from
    :param output_queue_handler: function to run on every item in outq
    :param kill_boolean: set by worker thread indicates we should all die

    :type outq: Queue
    :type output_queue_handler: callable
    :type kill_boolean: bool
    """
    if not isinstance(outq, Queue):
        raise AssertionError
    else:
        if not callable(output_queue_handler):
            raise AssertionError
        elif not isinstance(kill_boolean, bool):
            raise AssertionError
        if get_num_input_vars(output_queue_handler) != 1:
            kill_boolean = True
            raise RuntimeError('output_queue_handler function must take in at least one arg!')
    while True:
        if kill_boolean:
            LOGGER.warning('Got a death threat from kill_boolean, quitting')
            return
        output_var = outq.get()
        if output_var == 'DIE DIE DIE':
            LOGGER.warning("Finisher queue recieved death threat, quitting - if this didn't happen at the end of the program there's a problem")
            return
        output_queue_handler(output_var)

    raise RuntimeError('We should never get here, somehow we exited our while loop')