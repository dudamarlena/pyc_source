# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/TAMO/MDconvert/MDconvert/kellis2tamo.py
# Compiled at: 2019-04-23 02:08:32
import sys, re, os, math, time, string, tempfile, glob
from TAMO import MotifTools
from TAMO.MD import AlignAce, Meme
from TAMO.util import Arith
from TAMO import MotifMetrics
probefile = None
PROBESET = None

def main():
    fsa_fcn = up_and_no_N
    parse()
    FID = open(sys.argv[1])
    tokss = [ x.strip().split(',') for x in FID.readlines() ]
    FID.close()
    D = {}
    for expt, motif, score, source in tokss:
        print expt, motif
        if expt == 'Category':
            continue
        if motif == 'x':
            continue
        motif = MotifTools.Motif_from_text(motif)
        motif.kellis = float(score)
        motif.source = source
        try:
            D[expt].append(motif)
        except:
            D[expt] = [motif]

    for expt, motifs in D.items():
        root = expt
        ext = 'cons'
        if root[0:3] == 'Rnd':
            num = re.sub('.*_', '', root)
            if len(num) == 1:
                root = re.sub('_', '_00', root)
            else:
                root = re.sub('_', '_0', root)
            root = re.sub('Rnd', 'random_', root)
        outname = '%s.t%s' % (root, ext)
        print '%-18s  --> %s' % (root, outname)
        sys.stdout.flush()
        motifs2tamo(motifs, outname)
        try:
            pass
        except:
            print 'Error: Could not convert %s [[ %s ]]' % (
             filename, outname)


def parse():
    global PROBESET
    global probefile
    try:
        idx = sys.argv.index('-genome')
        del sys.argv[idx]
        probefile = sys.argv[idx]
        del sys.argv[idx]
        PROBESET = MotifMetrics.ProbeSet(probefile)
        PROBESET.factor = 0.7
    except:
        pass


def motifs2tamo(motifs, outname):
    global PROBESET
    fsaname = find_fsa(outname)
    fsaD = MotifMetrics.fasta2seqs(fsaname, 'want_dict')
    probes = fsaD.keys()
    if not probefile:
        PROBESET = MotifMetrics.ProbeSet('YEAST')
    print '# %d motifs' % len(motifs)
    for motif in motifs:
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

    MotifTools.save_motifs(motifs, outname)
    return


def find_fsa(name, pathhint='../'):
    exists = os.path.exists
    root = re.sub('\\.\\w*$', '', name)
    smroot = re.sub('_.$', '', root)
    print root
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