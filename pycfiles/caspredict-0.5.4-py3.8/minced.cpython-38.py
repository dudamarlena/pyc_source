# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/caspredict/minced.py
# Compiled at: 2020-03-23 04:26:01
# Size of source mod 2**32: 3672 bytes
import os, subprocess, logging, sys, re

class CRISPR(object):
    count = 0

    def __init__(self, sequence):
        self.sequence = sequence.rstrip()
        CRISPR.count += 1
        self.crispr = '{}_{}'.format(self.sequence, CRISPR.count)
        self.repeats = []
        self.spacers = []

    def setPos(self, start, end):
        self.start = start.rstrip()
        self.end = end.rstrip()

    def addRepeat(self, repeat):
        self.repeats.append(repeat.rstrip())

    def addSpacer(self, spacer):
        self.spacers.append(spacer.rstrip())

    def getConsensus(self):
        self.cons = max((set(self.repeats)), key=(self.repeats.count))


class Minced(object):

    def __init__(self, obj):
        self.master = obj
        for key, val in vars(obj).items():
            setattr(self, key, val)

    def run_minced(self):
        if not self.redo:
            logging.info('Predicting CRISPR arrays with minced')
            subprocess.run(['minced',
             self.fasta,
             self.out + 'minced.out'],
              stdout=(subprocess.DEVNULL),
              stderr=(subprocess.DEVNULL))
            self.parse_minced()
            self.write_crisprs()
            self.write_spacers()

    def parse_minced(self):
        file = open(self.out + 'minced.out', 'r')
        crisprs = []
        for ll in file:
            if ll.startswith('Sequence'):
                sequence_current = re.sub("' \\(.*", '', re.sub("Sequence '", '', ll))
            else:
                if ll.startswith('CRISPR'):
                    crisp_tmp = CRISPR(sequence_current)
                    pos = re.sub('.*Range: ', '', ll)
                    start = re.sub(' - .*', '', pos)
                    end = re.sub('.* - ', '', pos)
                    crisp_tmp.setPos(start, end)
                if ll[:1].isdigit():
                    lll = ll.split()
                    if len(lll) == 7:
                        crisp_tmp.addRepeat(lll[1])
                        crisp_tmp.addSpacer(lll[2])
                    if len(lll) == 2:
                        crisp_tmp.addRepeat(lll[1])
            if ll.startswith('Repeats'):
                crisp_tmp.getConsensus()
                crisprs.append(crisp_tmp)
            file.close()
            self.crisprs = crisprs

    def write_crisprs(self):
        f = open(self.out + 'crisprs_all.tab', 'w')
        f.write('Contig\tCRISPR\tStart\tEnd\tConsensus_repeat\tN_repeats\n')
        for crisp in self.crisprs:
            f.write('{}\t{}\t{}\t{}\t{}\t{}\n'.format(crisp.sequence, crisp.crispr, crisp.start, crisp.end, crisp.cons, len(crisp.repeats)))
        else:
            f.close()

    def write_spacers(self):
        if len(self.crisprs) > 0:
            os.mkdir(self.out + 'spacers')
            for crisp in self.crisprs:
                f = open(self.out + 'spacers/{}.fa'.format(crisp.crispr), 'w')
                n = 0
                for sq in crisp.spacers:
                    n += 1
                    f.write('>{}:{}\n'.format(crisp.crispr, n))
                    f.write('{}\n'.format(sq))
                else:
                    f.close()