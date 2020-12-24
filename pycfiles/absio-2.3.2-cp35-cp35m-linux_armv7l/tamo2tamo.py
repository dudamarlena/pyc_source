# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/TAMO/MDconvert/tamo2tamo.py
# Compiled at: 2019-04-23 02:08:32
import sys, re, os, math, time, string, tempfile, glob
from TAMO import MotifTools
from TAMO.MD import AlignAce, Meme
from TAMO.util import Arith
from TAMO import MotifMetrics
probefile = None
PROBESET = None
letter = 't'
fsafile = None

def main():
    global letter
    fsa_fcn = up_and_no_N
    parse()
    for filename in sys.argv[1:]:
        root = ('.').join(filename.split('.')[0:-1])
        ext = filename.split('.')[(-1)]
        outname = '%s.%s%s' % (root, letter, ext)
        print '%-18s  --> %s' % (filename, outname)
        sys.stdout.flush()
        tamo2tamo(filename, outname)
        try:
            pass
        except:
            print 'Error: Could not convert %s [[ %s ]]' % (
             filename, outname)


def parse():
    global PROBESET
    global fsafile
    global letter
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

    try:
        idx = sys.argv.index('-letter')
        del sys.argv[idx]
        letter = sys.argv[idx]
        del sys.argv[idx]
    except:
        pass

    try:
        idx = sys.argv.index('-f')
        del sys.argv[idx]
        fsafile = sys.argv[idx]
        del sys.argv[idx]
    except:
        pass


def tamo2tamo(file, outname):
    global PROBESET
    motifs = MotifTools.load(file)
    if fsafile:
        fsaname = fsafile
    else:
        fsaname = find_fsa(file)
    print '# FSA ', fsaname
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
        if motif.ROC_auc == None:
            motif.ROC_auc = PROBESET.ROC_AUC(motif, probes, 'v')
        if motif.frac == None:
            motif.frac = PROBESET.frac(motif, probes, 'v', 0.7)
        if motif.numbound == 0:
            matching = PROBESET.matching_ids(motif, [], factor=0.7)
            matchbound = [ x for x in matching if x in probes ]
            motif.numbound = len(probes)
            motif.nummotif = len(matching)
            motif.numboundmotif = len(matchbound)
        if 0 and motif.CRA == None:
            try:
                CRA, Cfrac = PROBESET.cons_ROC_AUC(motif, probes, 'v', tuple='YES')
                motif.CRA = CRA
                motif.Cfrac = Cfrac
            except:
                pass

    MotifTools.save_motifs(motifs, outname)
    return


def find_fsa(name, pathhint='../'):
    exists = os.path.exists
    root = re.sub('\\.\\w*$', '', name)
    smroot = re.sub('_.$', '', root)
    tail = root.split('/')[(-1)]
    parent = ('/').join(name.split('/')[:-2])
    if re.search('\\.fsa$', name):
        if exists(name):
            return name
        if exists(pathhint + name):
            return pathhint + name
    else:
        if exists(root + '.fsa'):
            return root + '.fsa'
        if exists(parent + tail + '.fsa'):
            return parent + tail + '.fsa'
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