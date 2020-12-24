# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/TAMO/MDconvert/MDconvert/ace2tamo.py
# Compiled at: 2019-04-23 02:08:32
import sys, re, os, math, time, string, tempfile
from TAMO import AlignAce
from TAMO.MD import Meme
from TAMO.util import Arith
from TAMO import MotifTools
from TAMO import MotifMetrics
probefile = None
PROBESET = None

def main():
    fsa_fcn = up_and_no_N
    parse()
    for filename in sys.argv[1:]:
        tamoname = re.sub('\\.(\\w*)$', '.t\\1', filename)
        print '%-18s  --> %s' % (filename, tamoname)
        sys.stdout.flush()
        try:
            ace2tamo(filename, tamoname)
        except:
            print 'Did not convert %s' % filename


def parse():
    global PROBESET
    global probefile
    try:
        idx = sys.argv.index('-genome')
        del sys.argv[idx]
        probefile = sys.argv[idx]
        del sys.argv[idx]
        PROBESET = MotifMetrics.ProbeSet(probefile)
        PROBESET.factor = 0.65
    except:
        pass


def ace2tamo(filename, tamoname):
    global PROBESET
    if re.search('\\.ace$', filename):
        mdobject = AlignAce.AlignAce(filename)
    else:
        if re.search('\\.meme$', filename):
            mdobject = Meme.Meme(filename)
        fsaname = find_fsa(mdobject.fastafile)
        fsaD = MotifMetrics.fasta2seqs(fsaname, 'want_dict')
        probes = fsaD.keys()
        if not probefile:
            PROBESET = MotifMetrics.ProbeSet('HUMAN_250')
        for key, seq in fsaD.items():
            PROBESET.probes[key] = seq

        for motif in mdobject.motifs:
            if motif.pvalue == 1:
                motif.pvalue = PROBESET.p_value(motif, probes, 'v')
            if motif.church == 1:
                motif.church = PROBESET.church(motif, probes, 'v')
            if motif.E_site == None:
                motif.E_site = PROBESET.E_sitef(motif, probes, 3, 'v')
            if motif.E_seq == None:
                motif.E_seq = PROBESET.E_seq(motif, probes, 'v')
            if motif.ROC_auc == None:
                motif.ROC_auc = PROBESET.ROC_AUC(motif, probes, 'v')
            if motif.MNCP == None:
                motif.MNCP = PROBESET.MNCP(motif, probes, 'v')
            if re.search('\\.meme$', filename):
                motif.MAP = -math.log(motif.evalue) / math.log(10)
            sys.stdout.flush()

        i = 0
        for motif in mdobject.motifs:
            motif.seednum = i
            i = i + 1
            kmers = motif.bogus_kmers(100)
            motif.maxscore = -100
            scores = [ motif.scan(kmer)[2][0] for kmer in kmers ]
            print Arith.avestd(scores)

    if re.search('\\.meme$', filename):
        mdobject.motifs.sort(lambda x, y: cmp(x.pvalue, y.pvalue))
    else:
        mdobject.motifs.sort(lambda x, y: cmp(x.church, y.church))
    MotifTools.save_motifs(mdobject.motifs, tamoname)
    return


def find_fsa(name, pathhint='../'):
    exists = os.path.exists
    root = re.sub('\\.\\w*$', '', name)
    smroot = re.sub('_.$', '', root)
    if re.search('\\.fsa$', name):
        if exists(name):
            return name
        if exists(pathhint + name):
            return pathhint + name
    else:
        if exists(root + '.fsa'):
            return root + '.fsa'
        if exists(pathhint + root + '.fsa'):
            return pathhint + root + '.fsa'
        if exists(smroot + '.fsa'):
            return smroot + '.fsa'
        if exists(pathhint + smroot + '.fsa'):
            return pathhint + smroot + '.fsa'
    print '## ! Could not find fsa file for %s' % name
    return


def up_and_no_N(name):
    root = re.sub('_N.ace', '', name)
    ans = '../%s.fsa' % root
    return ans


if __name__ == '__main__':
    main()