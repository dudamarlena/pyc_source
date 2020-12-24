# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/busybees/queen.py
# Compiled at: 2015-07-22 09:29:41
import locked_queue, logging, time, threading
logging.basicConfig(filename='/tmp/queen.log', level=logging.DEBUG, format='%(asctime)s (%(threadName)-2s) %(message)s')

class Queen(object):

    def __init__(self, name, lock, sched, default_worker):
        self.lock = lock
        self.sched = sched
        self.name = name
        self.default_worker = default_worker

    def main(self):
        f = int(1)
        logging.debug('Starting the queen...')
        local_lock = locked_queue.LockedQueue()
        self.lock.acquire()
        logging.debug('Acquired the lock for the first time.')
        workers = []
        die = False
        while True:
            q = self.lock.enum()
            for i in q:
                if i == 'die':
                    die = True
                else:
                    instruction = i[0]
                    if i[1] == 'default':
                        worker_var = self.default_worker
                    else:
                        worker_var = i[1]
                    cw = worker_var(local_lock, instruction)
                    c = threading.Thread(name='%s:worker%d' % (self.name, f), target=cw.run)
                    f += 1
                    c.start()
                    time.sleep(0.1)
                    workers.append(c)

            if die == True:
                logging.debug('Death command received.')
                break
            else:
                self.lock.clear()
                self.lock.cond.notify()
                logging.debug('Apiary notified. Releasing...')
                self.lock.cond.wait()
                logging.debug('Reacquired the lock.')

        logging.debug('Waiting for remaining workers...')
        for i in workers:
            i.join()

        logging.debug('No more workers in line.')
        logging.debug('Sending results back to the hive...')
        self.lock.clear()
        self.lock.append(local_lock.enum())
        self.lock.release()
        logging.debug('Queen died (gracefully, one hopes).')