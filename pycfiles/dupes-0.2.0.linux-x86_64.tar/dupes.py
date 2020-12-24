# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python2.7/site-packages/dupes/dupes.py
# Compiled at: 2015-03-11 19:11:02
import os, hashlib
__author__ = 'Devin Kelly'

class Dupes(object):
    """Docstring for Dupes. """

    def __init__(self):
        """
        :desc: Initialize, get list of files
        """
        self.pwd = os.getcwd()
        self.files = [ f for f in os.listdir(self.pwd) if os.path.isfile(os.path.join(self.pwd, f))
                     ]
        self.hashes = {}
        self.duped_hashes = {}
        self.buf_size = int(100000.0)

    def get_hashes(self):
        """
        :desc: Makes a dict of file names to file hashes
        :returns: TODO

        """
        for f in self.files:
            m = hashlib.sha1()
            with open(f, 'r') as (fd):
                while True:
                    contents = fd.read(self.buf_size)
                    if contents == '':
                        break
                    m.update(contents)

                self.hashes[f] = m.hexdigest()

    def dedupe(self):
        """
        :desc: Find all the common values and group them
        """
        all_hashes = self.hashes.values()
        dupes = set([ x for x in all_hashes if all_hashes.count(x) > 1 ])
        for d in dupes:
            self.duped_hashes[d] = []

        for f in self.files:
            h = self.hashes[f]
            if h in dupes:
                self.duped_hashes[h].append(f)

        return self.duped_hashes

    def remove(self):
        """
        :desc: Remove dupes one by one
        """
        if not self.duped_hashes:
            return
        print 'Select files to remove:'
        for ii in self.duped_hashes:
            files = sorted(self.duped_hashes[ii])
            for ll, kk in enumerate(files):
                print ('[{0}] {1}').format(ll + 1, kk)

            reply = int(raw_input()) - 1
            if reply >= 0 and reply < len(files):
                os.remove(files[reply])
            else:
                print ('{0} is not a valid option').format(reply + 1)