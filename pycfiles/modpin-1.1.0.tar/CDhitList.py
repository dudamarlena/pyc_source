# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/patricia/patricia/modppi/./src/SBI/external/CDhit/CDhitList.py
# Compiled at: 2018-02-02 06:38:56
from SBI.beans.StorableObject import StorableObject
from SBI.beans.File import File
from .CDhit import CDhit
from .CDhitHomolog import CDhitHomolog

class CDhitList(StorableObject):

    def __init__(self, cdhitfile):
        self._clusters = []
        self._allseqids = {}
        self._file = File(file_name=cdhitfile)
        self._parse_file()

    @property
    def clusters(self):
        return self._clusters

    def get_cluster4sequence(self, sequence):
        if sequence in self._allseqids:
            return self._clusters[self._allseqids[sequence]]
        else:
            return
            return

    def is_in_cluster(self, sequence):
        c = self.get_cluster4sequence(sequence)
        if c is None:
            return 'N'
        else:
            if c.is_master(sequence):
                return 'M'
            else:
                return 'H'

            return

    def add_cluster(self, cluster):
        self._clusters.append(cluster)

    def add_sequence2cluster(self, sequence, clusterid=None):
        if clusterid is None:
            self.clusters[(-1)].add_sequence(sequence)
            self._allseqids[sequence.name] = len(self.clusters) - 1
        else:
            for x in range(len(self._clusters)):
                if self._clusters[x].identifier == clusterid:
                    self._clusters[x].add_sequence(sequence)
                    self._allseqids[sequence.name] = x
                    break

        return

    def dictionary_role_summary(self):
        data = {'master': [], 'homolog': []}
        for c in self.clusters:
            data['master'].append(c.master.name)
            for s in c.sequences:
                data['homolog'].append(s)

        return data

    def _parse_file(self):
        for line in self._file.descriptor:
            if line.startswith('>'):
                c = CDhit(clusterid=line.split()[(-1)].strip())
                self.add_cluster(c)
            else:
                data = line.split()[1:]
                h = CDhitHomolog(name=data[1], length=data[0], homology=data[(-1)])
                self.add_sequence2cluster(sequence=h)

        self._file.close()

    def __repr__(self):
        text = []
        for c in self.clusters:
            text.append(('{0}').format(c))

        return ('\n').join(text)