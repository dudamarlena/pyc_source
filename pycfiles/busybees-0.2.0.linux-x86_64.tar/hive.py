# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/busybees/hive.py
# Compiled at: 2015-07-22 09:29:41
import threading, logging, operator, locked_queue, queen_dir, queen, worker, random, job_list
logging.basicConfig(filename='/tmp/hive.log', level=logging.DEBUG, format='%(asctime)s (%(threadName)-2s) %(message)s')

class Hive(object):

    def __init__(self):
        self.queens = queen_dir.QueenDir()

    def create_queen(self, name, default_worker=worker.Worker):
        logging.debug("Creating a queen with name '%s'..." % name)
        lock = locked_queue.LockedQueue()
        sched = job_list.JobList()
        cq = queen.Queen(name, lock, sched, default_worker)
        c = threading.Thread(name='%s:queen' % name, target=cq.main)
        self.queens.add_queen(name, c, lock, sched)

    def kill_queen(self, name):
        if self.queens.get_queen(name).isAlive():
            if self.queens.get_stat(name) != 'ded':
                logging.debug('Waiting for the lock in order to kill %s...' % name)
                self.queens.get_lock(name).acquire()
                logging.debug('Sending death command to %s...' % name)
                self.queens.get_lock(name).append('die')
                self.queens.set_stat(name, 'ded')
                self.queens.get_lock(name).cond.notify()
                self.queens.get_lock(name).release()
            else:
                logging.debug("Kill command for queen '%s' failed: already marked for death." % name)
        else:
            logging.debug('ERROR: I tried to kill a queen (%s) who was unstarted!' % name)

    def start_queen(self, name):
        if not self.queens.get_queen(name).isAlive():
            logging.debug("Starting the queen with name '%s'..." % name)
            self.queens.get_queen(name).start()
        else:
            logging.debug('ERROR: I tried to start a queen (%s) who was already alive!' % name)

    def instruct_queen(self, name, instructions, worker_type='default'):
        self.queens.get_lock(name).acquire()
        if type(instructions) == list:
            for i in instructions:
                self.queens.get_lock(name).append((i, worker_type))

        else:
            self.queens.get_lock(name).append((instructions, worker_type))
        self.queens.get_lock(name).cond.notify()
        self.queens.get_lock(name).release()

    def die(self):
        logging.debug('Trying to die...')
        for queen in self.queens.enum_queens():
            self.kill_queen(queen)

        for queen in self.queens.enum_queens():
            self.queens.get_queen(queen).join()
            if not self.queens.get_queen(queen).isAlive():
                logging.debug('Joined: %s' % queen)
            elif not not self.queens.get_queen(queen).isAlive():
                raise AssertionError("Joined the queen '%s', but the thread is still alive." % queen)

        results = {}
        for queen in self.queens.enum_queens():
            results[queen] = self.get_result(queen)

        logging.debug('RIP everyone')
        return results

    def get_result(self, name):
        self.queens.set_result(name, self.queens.get_lock(name).access())
        return self.queens.get_result(name)

    def get_queens(self):
        return self.queens.enum_queens()