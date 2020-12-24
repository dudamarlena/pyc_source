# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/abseqPy/IgRepAuxiliary/RestrictionSitesScanner.py
# Compiled at: 2019-04-23 02:08:32
"""
    Short description: Quality Control Analysis of Immunoglobulin Repertoire NGS (Paired-End MiSeq)    
    Author: Monther Alhamdoosh    
    Python Version: 2.7
    Changes log: check git commits. 
"""
from multiprocessing import Process
from numpy import isnan
from Bio.Seq import Seq
from collections import Counter
import abseqPy.IgRepAuxiliary.restrictionAuxiliary
from abseqPy.logger import printto, LEVEL

class RestrictionSitesScanner(Process):

    def __init__(self, records, cloneAnnot, procCounter, sites, simpleScan=True, stream=None):
        super(RestrictionSitesScanner, self).__init__()
        self.records = records
        self.cloneAnnot = cloneAnnot
        self.procCounter = procCounter
        self.sites = sites
        self.simpleScan = simpleScan
        self.tasksQueue = None
        self.exitQueue = None
        self.resultsQueue = None
        self.stream = stream
        return

    def run(self):
        printto(self.stream, self.name + ' process is now ready to start a new job ...')
        while True:
            nextTask = self.tasksQueue.get()
            if nextTask is None:
                printto(self.stream, self.name + ' process has stopped.')
                self.exitQueue.put('exit')
                break
            try:
                if self.simpleScan:
                    self.runSimple(nextTask)
                else:
                    self.runDetailed(nextTask)
            except Exception as e:
                printto(self.stream, 'An error occurred while processing ' + self.name + (' error: {}').format(str(e)), LEVEL.ERR)
                self.resultsQueue.put(None)
                continue

        return

    def runSimple(self, nextTask):
        """
        Runs Restriction sites simple analysis

        :param nextTask: iterable of sequence ids that should exist in self.records
        :return: None
        """
        stats = abseqPy.IgRepAuxiliary.restrictionAuxiliary.initRSAStats(simple=True)
        stats['total'] = len(nextTask)
        for id_ in nextTask:
            record = self.records[id_]
            qsRec = self.cloneAnnot.loc[id_].to_dict()
            seq = sliceRecord(record, qsRec)
            cut = False
            for site, siteRegex in self.sites.items():
                hits = abseqPy.IgRepAuxiliary.restrictionAuxiliary.findHits(seq, siteRegex)
                if len(hits) == 0:
                    seqRC = str(Seq(seq).reverse_complement())
                    hits = abseqPy.IgRepAuxiliary.restrictionAuxiliary.findHits(seqRC, siteRegex)
                if len(hits) > 0:
                    stats['siteHitsCount'][site] += len(hits)
                    stats['siteHitSeqsCount'][site] += 1
                    stats['siteHitsSeqsIDs'][site].add(id_)
                    cut = True

            stats['seqsCutByAny'] += cut

        self.procCounter.increment(len(nextTask))
        self.resultsQueue.put(stats)

    def runDetailed(self, nextTask):
        stats = abseqPy.IgRepAuxiliary.restrictionAuxiliary.initRSAStats(simple=False)
        stats['total'] = len(nextTask)
        for id_ in nextTask:
            record = self.records[id_]
            qsRec = self.cloneAnnot.loc[id_].to_dict()
            seq = sliceRecord(record, qsRec)
            strand = 'forward'
            cut = False
            for site, siteRegex in self.sites.items():
                hits = abseqPy.IgRepAuxiliary.restrictionAuxiliary.findHits(seq, siteRegex)
                if len(hits) == 0:
                    seqRC = str(Seq(seq).reverse_complement())
                    strand = 'reversed'
                    hits = abseqPy.IgRepAuxiliary.restrictionAuxiliary.findHits(seqRC, siteRegex)
                if len(hits) > 0:
                    stats['siteHitsCount'][site] += len(hits)
                    stats['siteHitSeqsCount'][site] += 1
                    stats['siteHitsSeqsIDs'][site].add(id_)
                    hitsRegion = abseqPy.IgRepAuxiliary.restrictionAuxiliary.findHitsRegion(qsRec, hits)
                    if len(set(hitsRegion).intersection({'fr1', 'cdr1', 'fr2', 'cdr2', 'fr3'})) and len(stats['siteHitSeqsGermline'][site]) < 10000:
                        stats['siteHitSeqsGermline'][site].append((strand, record))
                        stats['siteHitsSeqsIGV'][site].add(qsRec['vgene'].split('*')[0])
                    stats['hitRegion'][site] += Counter(hitsRegion)
                    cut = True

            stats['seqsCutByAny'] += cut

        self.procCounter.increment(len(nextTask))
        self.resultsQueue.put(stats)


def sliceRecord(rec, qsRec):
    """
    given a string of nucleotides denoted by 'rec', return a sliced string with starting index at
    max(0, qsRec['vqstart'] - qsRec['vstart']), and ending at either fr4.end if provided, or the length of the sequence
    itself. That is, return the sequence where the query first aligned with
    the subject sequence by extending the 5' end. For example:

    2  ACGTTA... (subject)
       ||||||...
    53 ACGTTA...(query, 'rec')

    will return the query sequence starting from index 52. (all indices in this example are 1-based).
    So this is what we get:

    1  .ACGTTA... (subject)
       |||||||...
    52 .ACGTTA...(query, 'rec')

    If vqstart - vstart is less than 0, then the sequence will start from index 0

    :param rec: string. Query sequence
    :param qsRec: a row slice from cloneAnnot, requires the fields: vqstart, vstart, and fr4.end
    :return: string. Sliced 'rec' such that the 5' end alignment is extended, and the 3' end is either the length of
    the sequence if fr4.end was nan, or fr4.end if it wasn't
    """
    qstart = int(max(0, qsRec['vqstart'] - qsRec['vstart']))
    if isnan(qsRec['fr4.end']):
        end = len(rec)
    else:
        end = int(qsRec['fr4.end'])
    return rec[qstart:end]