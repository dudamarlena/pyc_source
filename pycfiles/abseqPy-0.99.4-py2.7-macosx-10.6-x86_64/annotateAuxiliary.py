# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/abseqPy/IgRepAuxiliary/annotateAuxiliary.py
# Compiled at: 2019-04-23 02:08:32
"""
    Short description: Quality Control Analysis of Immunoglobulin Repertoire NGS (Paired-End MiSeq)    
    Author: Monther Alhamdoosh    
    Python Version: 2.7
    Changes log: check git commits. 
"""
from __future__ import division
import os, sys, glob, gc
from multiprocessing import Queue
from collections import Counter
from Bio import SeqIO
from pandas.core.frame import DataFrame
from math import ceil
from abseqPy.IgRepAuxiliary.IgBlastWorker import analyzeSmallFile, IgBlastWorker
from abseqPy.IgRepertoire.igRepUtils import splitFastaFile, safeOpen
from abseqPy.logger import printto, LEVEL

def annotateIGSeqRead(fastaFile, chain, db, noWorkers, seqsPerFile, seqType='dna', outdir='', domainSystem='imgt', stream=None):
    if fastaFile is None:
        return Counter()
    else:
        printto(stream, 'The IGV clones of ' + os.path.basename(fastaFile) + ' are being annotated ...')
        with open(fastaFile) as (f):
            noSeqs = sum(1 for line in f if line.startswith('>'))
        totalFiles = int(ceil(noSeqs / seqsPerFile))
        if totalFiles < noWorkers:
            seqsPerFile = int(noSeqs / noWorkers) if noSeqs >= noWorkers else noSeqs
            totalFiles = int(ceil(noSeqs / seqsPerFile))
        noSplit = noSeqs <= seqsPerFile
        printto(stream, ('\t{0:,} sequences were found to be distributed into {1:,} file(s)').format(noSeqs, totalFiles if not noSplit else 1))
        newFastFile = fastaFile
        if noWorkers == 1 or noSplit:
            cloneAnnot, filteredIDs = analyzeSmallFile(newFastFile, chain, db, seqType, noWorkers, outdir, domainSystem=domainSystem, stream=stream)
        else:
            prefix, ext = os.path.splitext(os.path.basename(fastaFile))
            filesDir = os.path.join(outdir, 'tmp')
            prefix = prefix[prefix.find('_R') + 1:prefix.find('_R') + 3] + '_' if prefix.find('_R') != -1 else ''
            splitFastaFile(fastaFile, totalFiles, seqsPerFile, filesDir, prefix, ext, stream=stream)
            tasks = Queue()
            outcomes = Queue()
            exitQueue = Queue()
            cloneAnnot = DataFrame()
            filteredIDs = []
            workers = []
            try:
                try:
                    for _ in range(noWorkers):
                        w = IgBlastWorker(chain, db, seqType, int(ceil(noWorkers / totalFiles)), domainSystem=domainSystem, stream=stream)
                        w.tasksQueue = tasks
                        w.resultsQueue = outcomes
                        w.exitQueue = exitQueue
                        workers.append(w)
                        w.start()
                        sys.stdout.flush()

                    for i in range(totalFiles):
                        tasks.put(os.path.join(filesDir, prefix + 'part' + str(i + 1) + ext))

                    for _ in range(noWorkers + 10):
                        tasks.put(None)

                    i = 0
                    while i < noWorkers:
                        m = exitQueue.get()
                        if m == 'exit':
                            i += 1

                    printto(stream, 'Results are being collated from all workers ...')
                    sys.stdout.flush()
                    while totalFiles:
                        outcome = outcomes.get()
                        totalFiles -= 1
                        if outcome is None:
                            continue
                        cloneAnnoti, fileteredIDsi = outcome
                        cloneAnnot = cloneAnnot.append(cloneAnnoti)
                        filteredIDs += fileteredIDsi
                        sys.stdout.flush()
                        gc.collect()

                    printto(stream, '\tResults were collated successfully.')
                except Exception:
                    printto(stream, 'Something went wrong during the annotation process!', LEVEL.EXCEPT)
                    raise

            finally:
                for w in workers:
                    w.terminate()

            if noSeqs > seqsPerFile and os.path.exists(filesDir + os.path.sep + prefix + 'part1' + ext):
                map(os.remove, glob.glob(filesDir + os.path.sep + '*' + ext))
        return (
         cloneAnnot, filteredIDs)