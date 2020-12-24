# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\stacklesslib\test\teststdlibunittests.py
# Compiled at: 2017-12-11 20:12:50
"""
This unit test script should not implement any unit tests of its own.
Its goal is to wrap the running of standard library unit tests again the
monkey-patched environment that stacklesslib provides.

TODO:
- pump() blocks for at least a second.  why?  where?
"""
from __future__ import absolute_import
from __future__ import print_function
import stacklesslib.monkeypatch
stacklesslib.monkeypatch.patch_all()
import asyncore, traceback, sys, logging, stackless, stacklesslib.main, stacklesslib.app
from time import time as elapsed_time
stacklesslib.main.elapsed_time = elapsed_time

def run_unittests():
    from test import test_threading
    from test import test_socket
    from test import test_urllib
    from test import test_urllib2
    from test import test_xmlrpc
    print('** run_unittests.test_threading')
    import sys
    sys.modules['ctypes'] = None
    test_threading.test_main()
    del sys.modules['ctypes']
    print('** run_unittests.test_socket')
    test_socket.test_main()
    print('** run_unittests.test_urllib')
    test_urllib.test_main()
    print('** run_unittests.test_urllib2')
    test_urllib2.test_main()
    print('** run_unittests.test_xmlrpc')
    test_xmlrpc.test_main()
    print('** run_unittests - done')
    return


def new_tasklet(f, *args, **kwargs):
    try:
        f(*args, **kwargs)
    except Exception:
        traceback.print_exc()


if __name__ == '__main__':
    logging.basicConfig(level=logging.ERROR)
    stacklesslib.app.install_stackless()
    run_unittests_tasklet = stackless.tasklet(new_tasklet)(run_unittests)
    while run_unittests_tasklet.alive:
        tick_time = elapsed_time()
        try:
            stacklesslib.main.mainloop.loop()
        except Exception as e:
            import asyncore
            if isinstance(e, ReferenceError):
                print('run:EXCEPTION', str(e), asyncore.socket_map)
            else:
                print('run:EXCEPTION', asyncore.socket_map)
                traceback.print_exc()
            sys.exc_clear()

        if False and elapsed_time() - tick_time > 0.1:
            print('Pump took too long: %0.5f' % (elapsed_time() - tick_time))