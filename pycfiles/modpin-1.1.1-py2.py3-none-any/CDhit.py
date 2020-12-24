# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/patri/MODPIN/modpin/./src/SBI/external/CDhit/CDhit.py
# Compiled at: 2020-04-28 10:16:58


class CDhit(object):

    def __init__(self, clusterid):
        self._id = clusterid
        self._master = None
        self._sequences = {}
        return

    @property
    def identifier(self):
        return self._id

    @property
    def master(self):
        return self._master

    @property
    def sequences(self):
        return self._sequences

    def is_master(self, seq):
        return self._master.name == seq

    def is_sequence(self, seq):
        return seq in self._sequences

    def add_sequence(self, cdhithomolog):
        if cdhithomolog.is_master:
            self._master = cdhithomolog
        else:
            self._sequences[cdhithomolog.name] = cdhithomolog

    def __repr__(self):
        text = []
        text.append(('Cluster {0.identifier}:').format(self))
        text.append(('\tMaster Sequence: {0.master}').format(self))
        for s in self.sequences:
            text.append(('\t\t{0}').format(self.sequences[s]))

        return ('\n').join(text)