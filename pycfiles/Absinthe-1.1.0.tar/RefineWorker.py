# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/abseqPy/IgRepAuxiliary/RefineWorker.py
# Compiled at: 2019-06-21 04:18:28
__doc__ = '\n    Short description: Quality Control Analysis of Immunoglobulin Repertoire NGS (Paired-End MiSeq)    \n    Author: Monther Alhamdoosh    \n    Python Version: 2.7\n    Changes log: check git commits. \n'
from multiprocessing import Process
from Bio.SeqRecord import SeqRecord
from collections import defaultdict
from numpy import isnan, nan
from abseqPy.config import FR4_CONSENSUS, FR4_CONSENSUS_DNA
from abseqPy.IgRepertoire.igRepUtils import extractProteinFrag, findBestAlignment, extractCDRsandFRsProtein, calMaxIUPACAlignScores, findBestMatchedPattern
from abseqPy.IgRepAuxiliary.IgBlastWorker import convertCloneRecordToOrderedList
from abseqPy.logger import LEVEL, printto

class RefineWorker(Process):

    def __init__(self, procCounter, chain, actualQstart, fr4cut, trim5End, trim3End, refineFlagNames, stream=None):
        super(RefineWorker, self).__init__()
        self.procCounter = procCounter
        self.chain = chain
        self.actualQstart = actualQstart
        self.fr4cut = fr4cut
        self.trim5End = trim5End
        self.trim3End = trim3End if isinstance(trim3End, int) else _parse3EndSeqs(trim3End)
        self.refineFlagNames = refineFlagNames
        self.tasksQueue = None
        self.exitQueue = None
        self.resultsQueue = None
        self.firstJobTaken = False
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
                if not self.firstJobTaken:
                    printto(self.stream, self.name + ' process commenced a new task ... ')
                    self.firstJobTaken = True
                qsRecs = []
                seqsAll = []
                recordLengths = defaultdict(_defaultdefaultInt)
                flags = {}
                for f in self.refineFlagNames:
                    flags[f] = []

                for record, qsRec in zip(nextTask[0], nextTask[1]):
                    seqs = refineCloneAnnotation(qsRec, record, self.actualQstart, self.chain, self.fr4cut, self.trim5End, self.trim3End, flags, stream=self.stream)
                    if qsRec['v-jframe'] != 'Out-of-frame':
                        stillInFrame = refineInFramePrediction(qsRec, record, self.actualQstart, flags, stream=self.stream)
                        if stillInFrame:
                            _recordFRLength(qsRec, recordLengths)
                    qsRec['queryid'] = record.id
                    qsRecs.append(convertCloneRecordToOrderedList(qsRec, self.chain))
                    seqsAll.append(seqs)

                self.procCounter.increment(len(qsRecs))
                self.resultsQueue.put((qsRecs, seqsAll, flags, recordLengths))
            except Exception as e:
                printto(self.stream, 'An error occurred while processing ' + self.name, LEVEL.EXCEPT)
                self.resultsQueue.put(None)
                continue

        return


def refineCloneAnnotation(qsRec, record, actualQstart, chain, fr4cut, trim5End, trim3End, flags, stream=None):
    seqs = [record.id, qsRec['vgene']]
    if qsRec['chain'] in ('VH', 'VK', 'VL'):
        chain = qsRec['chain']
    else:
        if chain == 'klv':
            if 'K' in qsRec['vgene']:
                chain = 'VK'
            else:
                chain = 'VL'
        else:
            chain = chain[::-1].upper()
        printto(stream, ('Chain had unknown type {}').format(qsRec['chain']), LEVEL.WARN)
    try:
        if qsRec['strand'] == 'reversed':
            record = SeqRecord(record.seq.reverse_complement(), id=record.id, name='', description='')
        record = record[trim5End:]
        if isinstance(trim3End, int):
            record = record[:len(record) - trim3End]
        if actualQstart > -1:
            offset = actualQstart
        else:
            offset = int(qsRec['vqstart'] - qsRec['vstart'])
        if offset < 0:
            offset = 0
        vh = record.seq[offset:]
        if len(vh) % 3 != 0:
            vh = vh[:-1 * (len(vh) % 3)]
        protein = str(vh.translate())
        if qsRec['vqstart'] != qsRec['fr1.start']:
            flags['fr1NotAtBegin'] += [record.id]
        qsRec['fr1.start'] = offset + 1
        if isnan(qsRec['fr4.end']):
            searchRegion = extractProteinFrag(protein, qsRec['fr3.end'] + 1, -1, offset, trimAtStop=False, stream=stream)
            if searchRegion is None:
                raise Exception('ERROR: undefined search region to find FR4 consensus.')
            qsRec['cdr3.start'] = qsRec['fr3.end'] + 1
            fr4start, fr4end, gapped = findBestAlignment(searchRegion, FR4_CONSENSUS[chain], dna=False)
            if not gapped and fr4start != -1 and fr4end != -1 and fr4end > fr4start:
                qsRec['fr4.start'] = (fr4start - 1) * 3 + qsRec['fr3.end'] + 1
                qsRec['cdr3.end'] = qsRec['fr4.start'] - 1
                fr4end = qsRec['fr3.end'] + fr4end * 3
            else:
                searchRegion = str(record.seq)[int(qsRec['fr3.end']):]
                fr4start, fr4end, gapped = findBestAlignment(searchRegion, FR4_CONSENSUS_DNA[chain], dna=True)
                if fr4start != -1 and fr4end != -1 and fr4end > fr4start:
                    qsRec['fr4.start'] = qsRec['fr3.end'] + fr4start
                    qsRec['cdr3.end'] = qsRec['fr4.start'] - 1
                    flags['CDR3dna'] += [record.id]
                    fr4end = qsRec['fr3.end'] + fr4end
                else:
                    qsRec['cdr3.end'] = qsRec['jqend']
                    fr4end = nan
            if not fr4cut:
                if not isinstance(trim3End, int):
                    _, _, _, relativeFR4EndPosition, _ = findBestMatchedPattern(str(record.seq)[int(qsRec['cdr3.end']):], trim3End, extend5end=True)
                    if relativeFR4EndPosition == -1:
                        flags['FR4endless'] += [record.id]
                        qsRec['fr4.end'] = fr4end
                    else:
                        qsRec['fr4.end'] = qsRec['cdr3.end'] + relativeFR4EndPosition
                        if qsRec['fr4.end'] < qsRec['jqend']:
                            flags['FR4cutEarly'] += [record.id]
                            qsRec['fr4.end'] = fr4end
                else:
                    qsRec['fr4.end'] = len(record.seq)
            else:
                if isnan(fr4end):
                    qsRec['FR4PredictedError'] += [record.id]
                qsRec['fr4.end'] = fr4end
        protein, tmp = extractCDRsandFRsProtein(protein, qsRec, offset, stream=stream)
        seqs += tmp
        if seqs[(-1)][:4] != FR4_CONSENSUS[chain][:4]:
            flags['fr4NotAsExpected'] += [record.id]
        if seqs[(-1)] == '':
            flags['noFR4'] += [record.id]
        if '*' in protein:
            flags['endsWithStopCodon'] += [record.id]
            if qsRec['stopcodon'] == 'No':
                flags['updatedStopCodon'] += [record.id]
                qsRec['stopcodon'] = 'Yes'
        gaps = int(abs(qsRec['vqstart'] - qsRec['vstart']) - offset)
        mismatches = qsRec['vstart'] - 1
        if qsRec['vstart'] > qsRec['vqstart'] and gaps > 0:
            mismatches -= gaps
        if gaps > 0:
            qsRec['fr1.gaps'] += gaps
            qsRec['vgaps'] += gaps
        if mismatches > 0:
            qsRec['fr1.mismatches'] += mismatches
            qsRec['vmismatches'] += mismatches
            qsRec['vstart'] -= mismatches
            qsRec['vqstart'] -= mismatches
    except Exception as e:
        if 'partitioning' in str(e):
            flags['partitioning'] += [record.id]

    return seqs


def refineInFramePrediction(qsRec, record, actualQstart, flags, stream=None):
    inframe = True
    if qsRec['v-jframe'] == 'N/A' or not isinstance(qsRec['v-jframe'], str) and isnan(qsRec['v-jframe']):
        flags['updatedInFrameNA'] += [record.id]
        inframe = False
    offset = int(qsRec['vqstart'] - qsRec['vstart']) + 1
    if inframe and (offset < 1 or actualQstart != -1 and (offset - 1 - actualQstart) % 3 != 0):
        inframe = False
        flags['updatedInFrameConc'] += [record.id]
    if inframe and (isnan(qsRec['fr4.start']) or isnan(qsRec['fr4.end']) or isnan(qsRec['cdr3.start']) or qsRec['cdr3.start'] >= qsRec['cdr3.end']):
        inframe = False
        flags['updatedInFrameNo3or4'] += [record.id]
    if inframe and ((qsRec['fr4.end'] - qsRec['fr1.start'] + 1) % 3 != 0 or actualQstart != -1) and (qsRec['fr4.end'] - actualQstart) % 3 != 0:
        inframe = False
        flags['updatedInFrame3x'] += [record.id]
    if inframe and (qsRec['fr1.gaps'] % 3 != 0 or qsRec['fr2.gaps'] % 3 != 0 or qsRec['fr3g.gaps'] % 3 != 0 or qsRec['cdr1.gaps'] % 3 != 0 or qsRec['cdr2.gaps'] % 3 != 0 or not isnan(qsRec['cdr3g.gaps']) and qsRec['cdr3g.gaps'] % 3 != 0):
        inframe = False
        flags['updatedInFrameIndel'] += [record.id]
    if not inframe:
        qsRec['v-jframe'] = 'Out-of-frame'
        flags['updatedInFrame'] += [record.id]
    return inframe


def _parse3EndSeqs(seqs):
    """
    transform list of seqs to expected format by findBestMatchedPattern
    :param seqs: raw string sequences
    :return: zippped(ids, seqs, maxUIPACScores)
    """
    targetids = [ str(i) for i in range(len(seqs)) ]
    maxScores = calMaxIUPACAlignScores(seqs)
    return zip(targetids, seqs, maxScores)


def _recordFRLength(qsRec, germlineConsensusLength):
    vgene = qsRec['vgene'].split('*')[0]
    jgene = qsRec['jgene'].split('*')[0]
    for region in ('fr1', 'fr2', 'fr3', 'fr4'):
        start = region + '.start'
        end = region + '.end'
        length = qsRec[end] - qsRec[start] + 1
        gene = vgene if region != 'fr4' else jgene
        if not isnan(length):
            germlineConsensusLength[gene][region][length] += 1

    return germlineConsensusLength


def _defaultInt():
    """
    to be pickle-able, this function cannot be lambda
    :return: equivalent to defaultdict(int)
    """
    return defaultdict(int)


def _defaultdefaultInt():
    """
    to be pickle-able, this function cannot be lambda
    :return: equivalent to defaultdict(lambda: defaultdict(int)
    """
    return defaultdict(_defaultInt)