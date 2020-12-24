# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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