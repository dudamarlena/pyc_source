# uncompyle6 version 3.6.7
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/cifitlib/state.py
# Compiled at: 2011-01-27 14:39:21
__doc__ = "\nstate.py\nGoal: retain optional state between cifit runs\nI envision something like RRD, but not as limiting and not as annoying\ndependency wise.\n\n\n\nKeep a {} of time:value\nvalue can be whatever you want that's pickleable.\n\n\nYou define a 'name' of something you want to store, and it starts a new Data\nobject for that name.\n\nand handles storage/retrieval.\n\nState():\n\tname:\n\t\tshould be a simple name of the data you want to store. automatically\n\t\tthis gets turned into a filename, and by default stored in\n\t\t~/.cifit/<name>.state\n\t\tif you include a path, it will use that path instead.\n\n"
import os, time, shutil
try:
    import cPickle as pickle
except ImportError:
    import pickle

class State(object):
    """I store and manage the info"""

    def __init__(self, name='cifit', opts={}):
        """initialize
                name is generally required, may be a path+filename (without extension)
                opts is dict of options
                currently only type 'value' is implemented, which means ANY value can
                be stored, and nothing is computed for you.
                TODO: I hope to someday add
                extra functionality that would let it act a lote more like RRD
                databases, and compute MEAN,AVERAGE,etc. for type 'number'.

                """
        opts.setdefault('count', 9)
        opts.setdefault('type', 'value')
        path = os.path.join(os.path.expanduser('~'), '.cifit')
        opts.setdefault('path', path)
        self.opts = opts
        self.data = []
        if os.path.sep in name:
            (self.opts['path'], self.name) = os.path.split(name)
        else:
            self.name = name
        self.filename = '%s.state' % self.name
        self.filename = os.path.join(self.opts['path'], self.filename)
        if os.path.exists(self.filename):
            self.load()

    def add(self, arg1, arg2=None):
        """Add a value to the DB
                add(value)
                or
                add(timestamp,value)
                either work.

                timestamp is a unix secs from epoch
                and value is any pickleable object.
                """
        if not arg2:
            key = time.time()
            value = arg1
        else:
            key = time.gmtime(arg1)
            value = arg2
        if len(self.data) > self.opts['count']:
            self.data = self.data[1:]
        self.data.append((time.time(), value))

    def save(self):
        if not os.path.exists(self.opts['path']):
            os.makedirs(self.opts['path'], 448)
        fd = open(self.filename + '.tmp', 'wb')
        pickle.dump({'opts': self.opts, 'name': self.name, 'data': self.data}, fd, -1)
        fd.close()
        shutil.move(self.filename + '.tmp', self.filename)
        return True

    def load(self):
        fd = open(self.filename, 'r')
        data = pickle.load(fd)
        self.name = data['name']
        self.data = data['data']
        self.opts = data['opts']
        fd.close()

    def update(self, timeIndex, value):
        """update a timeIndex"""
        index = 0
        for (t, v) in self.data:
            if timeIndex == t:
                self.data[index] = (
                 t, value)
            index += 1

    def get(self, index=None):
        """Get value, or values from DB
                index can be a unix timestamp(secs from epoch)
                or 'first' (get the earliest known value in DB)
                or 'last' (get the latest known value in DB)
                or an integer index into the DB (must be less than count)
                """
        if str(index) in ('last', 'LAST', 'Last'):
            return self.data[(len(self.data) - 1)]
        elif str(index) in ('first', 'FIRST', 'First'):
            return self.data[0]
        elif '.' not in str(index) and index != None:
            index = int(index)
            print 'index:%s count:%s' % (index, self.opts['count'])
            if index <= self.opts['count']:
                try:
                    return self.data[index]
                except IndexError:
                    return (None, None)

        if not index:
            return self.data
        for (t, v) in self.data:
            if index:
                if t == index:
                    return (t, v)

        return