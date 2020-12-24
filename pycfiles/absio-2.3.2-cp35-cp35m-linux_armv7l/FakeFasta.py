# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/TAMO/seq/seq/FakeFasta.py
# Compiled at: 2019-04-23 02:08:32
__doc__ = '\nFakeFasta.py -- Utilities for generating and analyzing "fake" Fasta-formatted sequences.\n\nCopyright (2005) Whitehead Institute for Biomedical Research (except as noted below)\nAll Rights Reserved\n\nAuthor: David Benjamin Gordon\n'
import sys, re, os, math, time, string, tempfile, shelve, random
from TAMO import MotifMetrics
from TAMO.seq import GenerateFastas
alphabet = [
 'A', 'C', 'T', 'G']

def count_matches(motif, seqlist):
    threshold = motif.maxscore * 0.8
    count = 0
    for seq in seqlist:
        matches, endpoints, scores = motif._scan(seq, threshold)
        for match, endpoint, score in zip(matches, endpoints, scores):
            print 'Prob debug:  %3d' % count, match, endpoint, score

        if len(matches) > 0:
            count = count + 1

    return count


def seed_random_seqD(motif, probability, numseq=50, genome='YEAST', emitprob=0.1):
    seqD = {}
    pre_seqD = random_seqs(numseq, genome, 'want dict')
    ids = [ x[0] for x in pre_seqD.items() ]
    seqs = [ x[1] for x in pre_seqD.items() ]
    nseqs = seed(seqs, motif, probability, emitprob)
    for id, seq in zip(ids, nseqs):
        seqD[id] = seq

    return seqD


PROBESETS = {}
BADPROBES = []
ALL_IDS = []
BADPROBEFILES = []

def random_seqs(numseq=50, genome='YEAST', want_dict=None):
    global ALL_IDS
    global BADPROBEFILES
    global BADPROBES
    global PROBESETS
    if PROBESETS.has_key(genome):
        probeset = PROBESETS[genome]
    else:
        probeset = MotifMetrics.ProbeSet(genome)
        PROBESETS[genome] = probeset
    if not BADPROBES:
        _d = {}
        for file in BADPROBEFILES:
            F = open(file)
            for id in [ x.strip() for x in F.readlines() ]:
                _d[id] = 1

            F.close()

        BADPROBES = _d.keys()
        simfilter = GenerateFastas.SimilarFilter(50)
        all_ids = [ x for x in probeset.probes.keys() if x not in BADPROBES ]
        ALL_IDS = simfilter.filter(all_ids)
    ids = ALL_IDS
    randomids = []
    count = 0
    numids = len(ids)
    while 1:
        randomid = ids[int(random.random() * numids)]
        if randomid not in randomids:
            randomids.append(randomid)
            count = count + 1
        if count >= numseq:
            break

    if not want_dict:
        seqs = []
        for randomid in randomids:
            seqs.append(probeset.probes[randomid])

    else:
        seqs = {}
        for randomid in randomids:
            seqs[randomid] = probeset.probes[randomid]

    return seqs


def main():
    seqlist = Fake_seqs(10, 40)
    seed(seqlist, '_<_____>_', 0.5)
    for seq in seqlist:
        print seq


def Fake_seq(length):
    seq = ''
    s = []
    for letter in alphabet:
        repeats = int(0.25 * length)
        for repeat in range(repeats):
            s.append(letter)

    random.shuffle(s)
    random.shuffle(s)
    seq = ('').join(s)
    return seq


def Fake_seqs(number, length):
    seqs = []
    for i in range(number):
        seqs.append(Fake_seq(length))

    return seqs


def seed(seqlist, motif, probability=1, emitprob=0.1):
    last = int(probability * len(seqlist))
    seedids = range(len(seqlist))
    seedids = seedids[0:last]
    newlist = []
    zip(seqlist, range(len(seqlist)))
    count = 0
    for seq, i in zip(seqlist, range(len(seqlist))):
        if i in seedids:
            if type(motif) == type(''):
                substring = motif
            else:
                substring = motif.emit(emitprob)
            count = count + 1
            pos = int(random.random() * (len(seq) - len(motif)))
            s = seq[0:pos]
            s = s + substring
            s = s + seq[pos + len(motif):]
            newlist.append(s)
        else:
            newlist.append(seqlist[i])

    return newlist


if __name__ == '__main__':
    main()