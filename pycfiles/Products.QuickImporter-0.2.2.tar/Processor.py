# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/Products/QueueCatalog/Processor.py
# Compiled at: 2008-05-13 06:38:33
__doc__ = '\n$Id: Processor.py 86692 2008-05-13 10:38:28Z andreasjung $\n'
import thread, Zope
from time import sleep
import sys
from zLOG import LOG, ERROR, PANIC, INFO

class Processor:
    """Simple thread that processes queued catalog events
    """
    __module__ = __name__

    def __init__(self, queue_catalog_paths, interval=60):
        self._queue_catalog_paths = queue_catalog_paths
        self._interval = interval
        thread.start_new_thread(self.live, ())

    def live(self):
        LOG('QueuedCatalog', INFO, 'Set up to process queue entries')
        while 1:
            sleep(self._interval)
            for queue_catalog_path in self._queue_catalog_paths:
                try:
                    application = Zope.app()
                except:
                    LOG('QueuedCatalog', PANIC, "Couldn't connect to database", error=sys.exc_info())
                    break
                else:
                    try:
                        queue_catalog = application.unrestrictedTraverse(queue_catalog_path)
                        queue_catalog.process()
                    except:
                        LOG('QueuedCatalog', ERROR, 'Queue processing failed', error=sys.exc_info())
                    else:
                        LOG('QueuedCatalog', INFO, 'Processed queue')

                    application._p_jar.close()


__doc__ = Processor.__doc__ + __doc__