# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/busybees/job_list.py
# Compiled at: 2015-07-22 09:29:41


class JobList(object):

    def __init__(self):
        self.queue = []

    def add(self, idnum, command):
        entry = [
         idnum, command, 'scheduled']
        self.queue.append(entry)

    def list_all(self):
        return self.queue

    def cancel(self, idnum):
        index = self.find_tuple(idnum, self.queue)
        assert self.queue[index][2] == 'scheduled', "Job looks like it wasn't waiting."
        self.queue[index][2] = 'cancelled'

    def curr(self, idnum):
        index = self.find_tuple(idnum, self.queue)
        assert self.queue[index][2] == 'scheduled', "Job looks like it wasn't waiting."
        self.queue[index][2] = 'current'

    def done(self, idnum):
        index = self.find_tuple(idnum, self.queue)
        assert self.queue[index][2] == 'current', "Job looks like it wasn't running."
        self.queue[index][2] = 'completed'

    def find_tuple(self, val1, q):
        for index, i in enumerate(q):
            x, y, z = i
            if x == val1:
                return index