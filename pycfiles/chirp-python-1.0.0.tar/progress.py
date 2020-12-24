# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\chirp\common\progress.py
# Compiled at: 2013-12-11 23:17:46
__doc__ = "\nProvides a system for monitoring the progress of a multiprocess batch\njob through a queue.  As worker processes or threads complete jobs,\nthey place objects into the queue. When they exit, they place None on\nthe queue.  The consumer thread removes objects from the queue,\noptionally updating a progress indicator as it does so.  When it has\nreceived a number of Nones equal to the number of workers, the job is\ncomplete.  One advantage of this method is that the batch can be\nprematurely terminated (typically through a shared variable) and the\nconsumer won't block indefinitely.\n\nCopyright (C) 2012 Daniel Meliza <dmeliza@dylan.uchicago.edu>\nCreated 2012-02-17\n"
from __future__ import absolute_import

class consumer(object):
    """
    Base class for consuming objects from a queue. Methods to
    override:

    __init__   initialization of display/processing for retrieved items
    start      start consuming values from the queue
    process    called for each value pulled off the queue
    finish     called when the batch is done
    """

    def start(self, queue, nworkers, stop_signal, njobs=None, gen=None):
        """
        Consume data from the queue. Workers should indicate when they
        terminate by placing None on the queue; this function will
        exit when it has received None from each of the
        processes.

        @param queue       the queue to poll
        @param nworkers    the number of workers adding values to the queue
        @param stop_signal a variable used to terminate the job (for consumers
                           linked to GUIs, for example)
        @param njobs       the (approximate) number of jobs in the batch
        @param gen         an optional callback generator; if not None,
                           calls send() with each new value
        """
        i = 0
        while nworkers > 0:
            v = queue.get()
            if v is None:
                nworkers -= 1
            else:
                self.process(i, v)
                if gen:
                    gen.send(v)
                i += 1

        self.finish(i)
        return

    def process(self, index, value):
        """ Called when a value is retrieved from the queue """
        pass

    def finish(self, lastindex):
        """ Called when the queue is empty """
        pass


try:
    from progressbar import ProgressBar, Percentage, Bar, Counter

    class progressbar(consumer):
        """ Provides a text-based progress bar """

        def __init__(self, title=''):
            self.title = title

        def start(self, queue, nworkers, stop_signal, njobs=None, gen=None):
            if njobs is not None:
                self.pbar = ProgressBar(widgets=[self.title, Percentage(), Bar()], maxval=njobs)
            else:
                self.pbar = ProgressBar(widgets=[self.title, Counter])
            self.pbar.start()
            consumer.start(self, queue, nworkers, stop_signal, njobs, gen)
            return

        def process(self, index, value):
            self.pbar.update(index)

        def finish(self, index):
            self.pbar.finish()


except ImportError:
    import sys

    class progressbar(consumer):
        """ Provides a text-based progress bar """

        def __init__(self, title=''):
            self.title = title

        def start(self, queue, nworkers, stop_signal, njobs=None, gen=None):
            sys.stderr.write('[ %s completed 0 ]' % self.title)
            consumer.start(self, queue, nworkers, stop_signal, njobs, gen)

        def process(self, index, value):
            if index % 10 == 0:
                sys.stderr.write('\r[ %s completed %d ]' % (self.title, index + 1))

        def finish(self, index):
            sys.stderr.write('\r[ %s completed %d/%d ]\n' % (self.title, index, index))