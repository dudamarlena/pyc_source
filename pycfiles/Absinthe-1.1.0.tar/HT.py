# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/TAMO/HT.py
# Compiled at: 2019-04-23 02:08:32
__doc__ = "\nHT.py --  Fast Interface to Tabular High-Throughput data (e.g. microarray)\n\nCORE OBJECTS: \nclass Dataset\nclass metaDataset\n\nExample:\n\nSay you have a comma-separated file summarizing p-values for a large number of\nhigh-throughput experiments in the form:\n\nrefseq_id, HNF4a_HepG2,  HNF4a_Hepcyt, HNF1a_HepG2, HNF1a_Hepcyt, ....\nNM_000345,  0.0001,      0.01,         0.343,       0.23,   \nNM_000347,  0.01,        0.443,        0.13,        0.5,\nNM_000456,  0.21,        0.04,         1.0,         0.004,\n.\n.\n.\n\nSuch files could represent enrichment ratios or p-values from expression data, ChIP-chip data, or\nother high-throughput data.\n\nInstantiate a Dataset object:\n\n>>> DATA = MT.Dataset('human_chip_data.csv')\n\nThe first time a file is loaded, a cached '.dataset' file is generated for faster access later.  You\nmust therefore have write permission in the directory of the original .csv file if it is being\ninstantiated into a Dataset object for the first time.\n\nNow you can ask questions:\n\n>>> print DATA.bound('HNF4_HepG2',threshold=0.001)   #Produces ['NM_00345']\n>>> print DATA.bound('HNF4_HepG2',0.01)              #Produces ['NM_00345', 'NM_00347']\n\nIf the input file contains Expression data, the Dataset object can be queried for\noverexpressed or underexpressed genes in terms of the ratios represented in the dataset:\n\n\n>>> genes = DATA.ratioabove('yeast_heat',2.0)  #With correct dataset, produces upregulated gene list\n>>> genes = DATA.ratiobelow('yeast_heat',0.2)  #With correct dataset, produces downregulated gene list\n\nIn conjunction with the ProbeSet object (in the MotifMetrics module), these genes may be\ndirectly associated with sequences.\n\nA 'metaDataset' provides a way to consider a collection of '.CSV' files as a single dataset.\n\nOther member functions include:\n    boundq(experiment,id,threshold)   # True or false:  Bound (or ratiobelow) for this id/experiment condition?\n    boundby(id,threshold)             # List of experiments in which 'id' is bound (or ratiobelow).\n    value(experiment,id)              # Query values\n    values(experiment, idlist)        # Query many values\n    scores(experiment)                # Query all values, as (value, id) tuples\n    boundre(regexp,threshold)         # logical 'and' on all experiments matching threshold (bound or ratiobelow)\n\nIn the metaDataset object, there are the member functions:\n    highest_n(experiment,N,threshold) # Return of list of N id's  with values above threshold\n    lowest_n(experiment,N,threshold)  # Return of list of N id's  with values below threshold\n    scores(experiment)                # Same as for Dataset object\n    values(experiment,idlist)         # Same as for Dataset object\n    \n\nCopyright (2005) Whitehead Institute for Biomedical Research\nAll Rights Reserved\nAuthor: David Benjamin Gordon\n\n"
import sys, re, os, math, time, string, tempfile, shelve
from Numeric import *
from glob import glob
from TAMO.seq import Fasta

class Dataset:
    """Represent a dataset of p-values of binding regions -- See TAMO.HT module documentation"""

    def __init__(self, csvfile):
        self.csvfile = csvfile
        if self.csvfile.find('.dataset') >= 0:
            self.picklefile = csvfile
        else:
            self.picklefile = csvfile + '.dataset'
        self.byprobe = {}
        self.data = None
        self.experiments = []
        self.probes = []
        self.probe2idx = {}
        self.exp2idx = {}
        if os.path.exists(self.picklefile):
            self.readpickle()
        else:
            self.readprobecsv()
            self.savepickle()
        return

    def savepickle(self):
        FID = open(self.picklefile, 'w')
        pickle.dump(self.__dict__, FID)
        FID.close()

    def readpickle(self):
        sys.stdout.flush()
        FID = open(self.picklefile, 'r')
        _newdict = pickle.load(FID)
        FID.close()
        self.__dict__ = _newdict

    def readprobecsv(self):
        lines = loadcsv(self.csvfile)
        experiments = lines[0]
        del lines[0]
        if len(lines[0]) < 2:
            del lines[0]
        self.experiments = experiments[1:]
        for i in range(len(self.experiments)):
            self.exp2idx[self.experiments[i]] = i

        self.data = zeros([len(lines), len(self.experiments)], Float)
        for i in range(len(lines)):
            probe = lines[i][0]
            try:
                self.data[i] = map(float, lines[i][1:])
            except:
                print 'Problem Converting Line:'
                print lines[i]
                for item in lines[i][1:]:
                    print '->', item,
                    print float(item)

                sys.exit(1)

            self.probes.append(probe)
            self.probe2idx[probe] = i

    def boundq(self, experiment, probe, threshold=0.001):
        ans = 0
        try:
            expidx = self.exp2idx[experiment]
        except:
            print 'Error: Experiment %s not found (%s %f)' % (
             experiment, probe, threshold)
            return

        try:
            probeidx = self.probe2idx[probe]
        except:
            print 'Error: Probe %s not found (%s %f)' % (
             probe, experiment, threshold)
            return

        value = self.data[(probeidx, expidx)]
        return value <= threshold

    def probe_boundby(self, probe, threshold=0.001):
        ans = []
        expts = self.exp2idx.keys()
        expts.sort()
        for expt in expts:
            if self.boundq(expt, probe, threshold):
                ans.append(expt)

        return ans

    def value(self, experiment, probe):
        return self.pvalue(experiment, probe)

    def values(self, experiment, probeids):
        ans = []
        if not self.exp2idx.has_key(experiment):
            print 'Error: Experiment %s not found (%s)' % (experiment, probe)
            return
        expidx = self.exp2idx[experiment]
        for probe in probeids:
            idx = self.probe2idx[probe]
            ans.append(self.data[(idx, expidx)])

        return ans

    def pvalue(self, experiment, probe):
        ans = 0
        if not self.exp2idx.has_key(experiment):
            print 'Error: Experiment %s not found (%s)' % (experiment, probe)
            return
        if not self.probe2idx.has_key(probe):
            print 'Error: Probe %s not found (%s)' % (probe, experiment)
            return
        value = self.data[(self.probe2idx[probe], self.exp2idx[experiment])]
        return value

    def scores(self, experiment):
        if not self.exp2idx.has_key(experiment):
            print 'Error: Experiment %s not found (%s)' % (experiment, probe)
            return
        ansT = []
        expidx = self.exp2idx[experiment]
        for probe in self.probe2idx.keys():
            idx = self.probe2idx[probe]
            ansT.append((self.data[(idx, expidx)], probe))

        return ansT

    def overexpressed(self, expt, threshold=2.0):
        return self.ratioabove(expt, threshold)

    def ratioabove(self, expt, threshold=2.0):
        if not self.exp2idx.has_key(expt):
            return []
        pvalues = self.data[:, self.exp2idx[expt]]
        thresholded = greater_equal(pvalues, threshold)
        indexes = nonzero(thresholded)
        ans = [ self.probes[i] for i in indexes ]
        return ans

    def underexpressed(self, expt, threshold=0.001):
        return self.bound(expt, threshold)

    def bound(self, expt, threshold=0.001):
        if not self.exp2idx.has_key(expt):
            return []
        pvalues = self.data[:, self.exp2idx[expt]]
        thresholded = less_equal(pvalues, threshold)
        indexes = nonzero(thresholded)
        ans = [ self.probes[i] for i in indexes ]
        return ans

    def boundre(self, regexps, threshold=0.001):
        interestings = []
        if type(regexps) == type(''):
            regexps = [
             regexps]
        for regexp in regexps:
            if regexp[0] == '~':
                _not = 1
                regexp = regexp[1:]
            else:
                _not = 0
            for expt in self.experiments:
                if re.search(regexp, expt):
                    interestings.append((expt, _not))

        if not interestings:
            print '# No matches found for expression: %s' % regexp
            return []
        truth = ones(len(self.probes))
        for expt, _not in interestings:
            pvalues = self.data[:, self.exp2idx[expt]]
            if not _not:
                thresholded = less_equal(pvalues, threshold)
            else:
                thresholded = greater_equal(pvalues, threshold)
            truth = logical_and(truth, thresholded)

        indexes = nonzero(truth)
        ans = []
        for index in indexes:
            ans.append(self.probes[index])

        return ans

    def matching_exp(self, regexp):
        return [ e for e in self.experiments if re.search(regexp, e) ]


class metaDataset:
    """Represent a dataset of p-values of binding regions -- See TAMO.HT module documentation"""

    def __init__(self, filelist=[]):
        self.datasets = []
        for file in filelist:
            print '# Adding dataset to metaDataset: %s' % file
            _t = Dataset(file)
            self.datasets.append(_t)

    def matching_exp(self, regexp):
        matching_exps = []
        for dataset in self.datasets:
            exps = [ e for e in dataset.experiments if re.search(regexp, e) and e not in matching_exps ]
            matching_exps.extend(exps)

        return matching_exps

    def highest_n(self, experiment_id, N, threshold=None):
        probelist = []
        for dataset in self.datasets:
            if re.sub('^~', '', experiment_id) in dataset.experiments:
                score_idT = dataset.scores(experiment_id)
                score_idT.sort()
                score_idT.reverse()
                score_idT = score_idT[0:N]
                if threshold != None:
                    _A = []
                    for score, id in score_idT:
                        if score >= threshold:
                            _A.append((score, id))
                        else:
                            break

            probelist = [ x[1] for x in _A ]

        return probelist

    def lowest_n(self, experiment_id, N, threshold=None):
        probelist = []
        for dataset in self.datasets:
            if re.sub('^~', '', experiment_id) in dataset.experiments:
                score_idT = dataset.scores(experiment_id)
                score_idT.sort()
                score_idT = score_idT[0:N]
                if threshold != None:
                    _A = []
                    for score, id in score_idT:
                        if score <= threshold:
                            _A.append((score, id))
                        else:
                            break

            probelist = [ x[1] for x in _A ]

        return probelist

    def scores(self, expt):
        D = None
        experiment = re.sub('_', ' ', expt)
        for dataset in self.datasets:
            if experiment in dataset.experiments:
                D = dataset
                break

        if not D:
            print '#Error: could not find %s among experiments' % experiment
            return
        else:
            return D.scores(experiment)

    def values(self, expt, probeids):
        D = None
        experiment = re.sub('_', ' ', expt)
        for dataset in self.datasets:
            if experiment in dataset.experiments:
                D = dataset
                break

        if not D:
            print '#Error: could not find %s among experiments' % experiment
            return
        else:
            return D.values(experiment, probeids)

    def underexpressed(self, expt, threshold=0.001):
        return self.bound(expt, threshold)

    def bound(self, expt, pvalue=0.001):
        for dataset in self.datasets:
            if expt in dataset.experiments:
                return dataset.bound(expt, pvalue)

        return []

    def overexpressed(self, expt, threshold=2.0):
        return self.ratioabove(expt, threshold)

    def ratioabove(self, expt, threshold=2.0):
        for dataset in self.datasets:
            if expt in dataset.experiments:
                return dataset.ratioabove(expt, threshold)

        return []

    def boundprobes(self, experiment_id, pvalue=0.001):
        probelist = []
        for dataset in self.datasets:
            if re.sub('^~', '', experiment_id) in dataset.experiments:
                regexp = re.sub('[\\(\\)\\-]', '.', experiment_id)
                probelist = dataset.bound(regexp, pvalue)
                break

        return probelist


def l_andnot(l1, l2):
    ans = []
    for item in l1:
        if item not in l2:
            ans.append(item)

    return ans


def l_and(l1, l2):
    ans = []
    for item in l1:
        if item in l2:
            ans.append(item)

    return ans


def l_or(l1, l2):
    ans = l1[:]
    for item in l2:
        if item not in l1:
            ans.append(item)

    return ans


def l_union(l1, l2):
    return l_or(l1, l2)


def l_intersection(l1, l2):
    return l_and(l1, l2)


def l_xor(l1, l2):
    return l_or(l_andnot(l1, l2), l_andnot(l2, l1))


class Experiment:

    def __init__(self, name=None):
        self.partners = []
        if not name:
            return
        self.name = name
        toks = name.split('_')
        self.factor = toks[0]
        self.cond = ('_').join(toks[1:])


def loadcsv(filename):
    FID = open(filename, 'r')
    lists = []
    while 1:
        line = FID.readline()
        if not line:
            break
        toks = line.replace('NaN', '0.9999').split(',')
        for i in range(1, len(toks)):
            if toks[i].strip().isdigit():
                toks[i] = float(toks[i])
            else:
                toks[i] = toks[i].strip()

        lists.append(toks)

    return lists


def vcsv2dict(filename):
    csvlines = loadcsv(filename)
    keys = csvlines[0]
    D = {}
    for key in keys:
        D[key] = []

    nexpts = len(keys)
    for toks in csvlines[1:]:
        for i in range(nexpts):
            if toks[i]:
                D[keys[i]].append(toks[i])

    return D