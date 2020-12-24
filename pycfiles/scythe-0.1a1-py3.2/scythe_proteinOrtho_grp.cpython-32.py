# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/scythe/convert/scythe_proteinOrtho_grp.py
# Compiled at: 2014-06-13 04:01:08


class ProteinOrthoParser(object):

    def readInfo(self, po):
        po = open(po, 'r')
        res = ''
        for l in po:
            if l.startswith('#'):
                res += l
                continue

        po.close()
        return res

    def readGroups(self, po, speciesNames=None):
        """Iterate over proteinOrtho output and return numbered list with orthogroups."""
        po = open(po, 'r')
        cnt = 0
        l = po.readline()
        if not speciesNames:
            sn = l.strip().split('\t')[3:]
        else:
            if len(speciesNames) == len(l.strip().split('\t')[3:]):
                sn = speciesNames
            else:
                raise ScytheError('Number of speciesNames must equal the number of species in the file.')
        for l in po:
            if l.startswith('#'):
                continue
                tmp_list = l.strip().split('\t')[3:]
                tmp_list = [l.split(',') for l in tmp_list]
                tmp_list = [val for tmp in tmp_list for val in tmp]
                yield (cnt, tmp_list, sn)
                cnt += 1

        po.close()

    def groupDct(self, po, speciesNames=None):
        res = {}
        for gr, ids, spec in self.readGroups(po, speciesNames):
            res[gr] = ids

        return res

    def findOrthologs(self, po, geneID):
        res = []
        for a in self.readGroups(po):
            if geneID in a[1]:
                res.append(a)
                continue

        return res