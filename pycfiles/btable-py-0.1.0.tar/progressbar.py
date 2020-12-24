# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/bta/tools/progressbar.py
# Compiled at: 2014-07-11 17:28:38
import sys, time, datetime, struct, fcntl

def string_progress_bar(total, desc='Progress', step=100, obj='rec'):
    t0 = time.time()
    tprevstep = t0 - 0.01
    i = 0
    iprevstep = 0
    iprevcall = -1
    progress = None
    while True:
        new_i = yield progress
        progress = None
        i = new_i if new_i is not None else i + 1
        if iprevcall / step != i / step or i >= total:
            t = time.time()
            avg = i / (t - t0)
            inst = (i - iprevstep) / (t - tprevstep)
            eta = datetime.timedelta(seconds=int((total - i) / inst))
            elapsed = datetime.timedelta(seconds=int(t - t0))
            tprevstep = t
            iprevstep = i
            progress = '%s: %i / %i  --  avg=%.2f %s/s inst=%.2f %s/s  --  ETA=%s elapsed=%s' % (desc, i, total, avg, obj, inst, obj, eta, elapsed)
        iprevcall = i

    return


def stderr_progress_bar(*args, **kargs):
    spb = string_progress_bar(*args, **kargs)
    nval = None
    while True:
        r = spb.send(nval)
        if r is not None:
            sys.stderr.write('\x1b[A\x1b[K%s\n' % r)
        nval = yield

    return


def null_progress_bar(total, desc='Progress', step=100, obj='rec'):
    while True:
        yield


class MultiProgressBar(object):

    def __init__(self, mothership, *args, **kargs):
        self.mothership = mothership
        self.spb = string_progress_bar(*args, **kargs)

    def next(self):
        p = next(self.spb)
        if p is not None:
            self.mothership.update(self, p)
        return

    def send(self, val):
        p = self.spb.send(val)
        if p is not None:
            self.mothership.update(self, p)
        return

    def __del__(self):
        self.mothership.delete(self)


class StderrMultiProgressBarMothership(object):
    TIOCGWINSZ = 21523

    def __init__(self, manager):
        self.progress = manager.dict()
        self.lock = manager.Lock()

    def __call__(self, *args, **kargs):
        child = MultiProgressBar(self, *args, **kargs)
        self.progress[id(child)] = '--'
        return child

    def update(self, child, progress):
        if progress is not None:
            self.progress[id(child)] = progress
        self.refresh_screen()
        return

    def delete(self, child):
        del self.progress[id(child)]
        self.refresh_screen()

    def refresh_screen(self):
        with self.lock:
            rows, _cols = struct.unpack('HH', fcntl.ioctl(sys.stderr, self.TIOCGWINSZ, 'xxxx'))
            sys.stderr.write('\x1b[s\x1b[r')
            for row, p in enumerate(self.progress.values() + ['==================']):
                sys.stderr.write('\x1b[%i;1H\x1b[K%s' % (row + 1, p))

            sys.stderr.write('\x1b[%i;%ir\x1b[u' % (len(self.progress) + 2, rows))

    def __del__(self):
        sys.stderr.write('\x1b[r')