# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pylinkirc/selectdriver.py
# Compiled at: 2020-04-11 03:31:40
# Size of source mod 2**32: 1526 bytes
__doc__ = '\nSocket handling driver using the selectors module. epoll, kqueue, and devpoll\nare used internally when available.\n'
import selectors, threading
from pylinkirc import world
from pylinkirc.log import log
SELECT_TIMEOUT = 0.5
selector = selectors.DefaultSelector()

def _process_conns():
    """Main loop which processes connected sockets."""
    while not world.shutting_down.is_set():
        for socketkey, mask in selector.select(timeout=SELECT_TIMEOUT):
            irc = socketkey.data
            try:
                if mask & selectors.EVENT_READ:
                    if not irc._aborted.is_set():
                        irc._run_irc()
            except:
                log.exception('Error in select driver loop:')
                continue


def register(irc):
    """
    Registers a network to the global selectors instance.
    """
    log.debug('selectdriver: registering %s for network %s', irc._socket, irc.name)
    selector.register((irc._socket), (selectors.EVENT_READ), data=irc)


def unregister(irc):
    """
    Removes a network from the global selectors instance.
    """
    if irc._socket.fileno() != -1:
        log.debug('selectdriver: de-registering %s for network %s', irc._socket, irc.name)
        selector.unregister(irc._socket)
    else:
        log.debug('selectdriver: skipping de-registering %s for network %s', irc._socket, irc.name)


def start():
    """
    Starts a thread to process connections.
    """
    t = threading.Thread(target=_process_conns, name='Selector driver loop')
    t.start()