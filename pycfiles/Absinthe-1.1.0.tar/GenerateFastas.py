# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/TAMO/seq/seq/GenerateFastas.py
# Compiled at: 2019-04-23 02:08:32
import sys, re, os, math, getopt
from TAMO import MotifTools
from TAMO import HT
from TAMO import MotifMetrics
GLOBALS = {}
BADPROBES = []

def usage(txt=''):
    if txt:
        print 'Error: %s' % txt
    print 'Usage: %s -D dataset.csv [ -g|--genome genomefile (YEAST)] ' % re.sub('^.*/', '', sys.argv[0])
    print '         [--expt   experiment_name]'
    print '         [--top    n]'
    print '         [--pvalue pvalue 0.001]'
    print '         [--ratioabove ratio]'
    print '         [--nofilter]'
    print '         [--badprobes file]'
    sys.exit(1)


def main():
    global BADPROBES
    global GLOBALS
    print '#' + (' ').join([ x.replace(' ', '\\ ') for x in sys.argv ])
    parse_opts()
    ARGS = getarg('args')
    GLOBALS['GENOME'] = MotifMetrics.ProbeSet(getarg('genome'))
    print '# Loaded %s' % getarg('genome')
    badprobes = []
    for f in BADPROBES:
        b = [ x.strip() for x in open(f).readlines() ]
        badprobes.extend(b)

    d = getarg('DATA')
    p = getarg('GENOME')
    S = SimilarFilter(50)
    experiments = getarg('expts')
    top = getarg('top')
    THRESH = getarg('pvalue')
    NO_FILTER = getarg('nofilter')
    ratioabove = getarg('ratioabove')
    if not experiments:
        experiments = d.experiments
    for expt in experiments:
        e = expt
        if top:
            _tups = d.scores(e)
            _tups.sort(lambda x, y: cmp(x[0], y[0]))
            unfiltered = [ x[1] for x in _tups[0:top] ]
        else:
            if ratioabove:
                unfiltered = d.ratioabove(e, ratioabove)
            else:
                unfiltered = d.bound(e, THRESH)
            badfiltered = [ x for x in unfiltered if x not in badprobes ]
            if len(unfiltered) - len(badfiltered) > 2:
                unfiltered = badfiltered
            bound_ids = p.filter(unfiltered)
            filtered_ids = bound_ids
            print '### Removed ', len(bound_ids) - len(S.filter(bound_ids)), 'from ', expt
            if not NO_FILTER:
                filtered_ids = p.filter(S.filter(bound_ids))
            if NO_FILTER:
                print '#%-15s   %3d    ' % (expt, len(bound_ids))
            else:
                print '#%-15s   Before %3d    After %3d ' % (expt, len(bound_ids), len(filtered_ids))
            if len(unfiltered) - len(bound_ids) > 2:
                diff = [ x for x in unfiltered if x not in bound_ids ]
                print '%-15s  %3d probes (out of %3d) without predicted sequences ' % (
                 expt, len(diff), len(unfiltered))
                for _p in diff:
                    print '# Absent in (%s) %s' % (expt, _p)

            final_ids, final_scores = [], []
            _tups = d.scores(e)
            _tups.sort(lambda x, y: cmp(x[0], y[0]))
            for score, id in _tups:
                if id in filtered_ids:
                    final_ids.append(id)
                    final_scores.append('%8.4e' % score)

        if final_scores:
            print '#%% %-15s %s' % (expt, final_scores[(-1)])
        else:
            print '#%% %-15s None' % expt
        s = p.fsa_string_from_ids(final_ids, final_scores)
        if len(s) == 0:
            continue
        f = expt + '.fsa'
        f = re.sub(' ', '_', f)
        FID = open(f, 'w')
        FID.write(s)
        FID.close()
        sys.stdout.flush()


class SimilarFilter:
    """
    Class to use data about similarity between sequences (e.g. predicted PCR
    products on microarrays) to reduce a list of probes to a quasi-unique set.
    Not used in the release version of TAMO.
    """

    def __init__(self, pcnt=70):
        self.prefix = '/HOME/intergenic/pcr/SimilarProbes.'
        self.pcnt = pcnt
        self.similar = {}
        self.lengths = {}
        self.loadsimilarfile()

    def filter(self, probelist_orig):
        """
        Port of removeduplicates.pl
        Behavior is only almost identical.  The inconsistencies occur in the
        unusual case that A~B, and B~C but A !~ C.  In the perl code B and C
        would be preserved, but in this code, only C is, due to differences 
        in sorting order different list order on input. At 70% id, here
        are some sample differences:

        GAL4 Cu2.fsa:55            | GAL4 Cu2.fsa:54
        MCM1 YPD.fsa:110           | MCM1 YPD.fsa:109
        RDS1 H2O2.fsa:64           | RDS1 H2O2.fsa:63
        RLM1 YPD.fsa:65            | RLM1 YPD.fsa:64
        ZAP1 Zn.fsa:43             | ZAP1 Zn.fsa:42
        """
        probelist = probelist_orig[:]
        probedict = {}
        for probe in probelist:
            probedict[probe] = 1

        plen = self.lengths
        probelist.sort()
        for probe in probelist:
            if not probedict.has_key(probe):
                continue
            if not self.similar.has_key(probe):
                continue
            m = self.similar[probe]['matches']
            maxkey = probe
            maxlen = plen[probe]
            for key in m.keys():
                if key == probe:
                    continue
                if probedict.has_key(key):
                    if m[key] >= maxlen:
                        maxkey = key
                        maxlen = m[key]

            if maxkey != probe:
                del probedict[probe]

        ans = probedict.keys()
        ans.sort()
        return ans

    def loadsimilarfile(self):
        ans = {}
        FNAME = '%s%d' % (self.prefix, self.pcnt)
        if not os.path.exists(FNAME):
            self.similar = ans
            return
        FID = open(FNAME)
        lines = FID.readlines()
        FID.close()
        for line in lines:
            toks = line.split()
            D = {}
            D['len'] = toks[2]
            D['longest'] = toks[3]
            D['shortest'] = toks[4]
            m = {}
            otherprobes = toks[5].split(',')
            otherlengths = toks[6].split(',')
            for i in range(len(otherprobes)):
                m[otherprobes[i]] = int(otherlengths[i])

            D['matches'] = m
            self.lengths[toks[0]] = int(toks[2])
            ans[toks[0]] = D

        self.similar = ans


def parse_opts():
    GLOBALS['genome'] = 'YEAST'
    GLOBALS['expts'] = []
    GLOBALS['pvalue'] = 0.001
    short_opts = 'D:g:e:'
    long_opts = ['genome=', 'expt=', 'top=', 'pvalue=', 'nofilter', 'badprobes=',
     'ratioabove=']
    try:
        opts, args = getopt.getopt(sys.argv[1:], short_opts, long_opts)
    except getopt.GetoptError:
        print getopt.GetoptError.__dict__
        usage()

    if not opts:
        usage()
    GLOBALS['args'] = args
    for opt, value in opts:
        if opt == '-D':
            GLOBALS['DATA'] = HT.Dataset(value)
        if opt in ('-g', '--genome'):
            GLOBALS['genome'] = value
        if opt in ('-e', '--expt'):
            GLOBALS['expts'].append(value)
        if opt == '--top':
            GLOBALS['top'] = int(value)
        if opt in ('-p', '--pvalue'):
            GLOBALS['pvalue'] = float(value)
        if opt == '--nofilter':
            GLOBALS['nofilter'] = 1
        if opt == '--badprobes':
            BADPROBES.append(value)
        if opt == '--ratioabove':
            GLOBALS['ratioabove'] = float(value)

    if not getarg('DATA'):
        usage('Must specify a CSV file')


def getarg(varname):
    if GLOBALS.has_key(varname):
        return GLOBALS[varname]
    else:
        return
        return


if __name__ == '__main__':
    main()