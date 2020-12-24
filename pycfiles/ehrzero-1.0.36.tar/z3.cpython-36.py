# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ishanu/.local/lib/python3.6/site-packages/ehrzero/z3.py
# Compiled at: 2019-04-25 03:56:18
# Size of source mod 2**32: 9704 bytes
""" z3 Classification """
__author__ = 'Ishanu Chattopadhyay'
__copyright__ = 'Copyright 2018, zed@uchicago '
__credits__ = ['Dmytro Onishchenko', 'Yi Huang']
__license__ = 'GPL'
__version__ = '0.314'
__maintainer__ = 'Rob Knight'
__email__ = 'ishanu@uchicago.edu'
__status__ = 'beta'
import pandas as pd, numpy as np, os.path, subprocess, os, glob, tempfile
from sklearn.metrics import confusion_matrix, accuracy_score, f1_score, roc_auc_score
from sklearn import metrics
DEBUG_ = True
result_dir = tempfile.TemporaryDirectory()
result_path = result_dir.name

def negative_confidence(true, pred):
    tn, fp, fn, tp = confusion_matrix(true, pred).ravel()
    if tn + fn > 0:
        return tn / (tn + fn)
    else:
        return 0


def positive_confidence(true, pred):
    tn, fp, fn, tp = confusion_matrix(true, pred).ravel()
    if tp + fp > 0:
        return tp / (tp + fp)
    else:
        return 0


class Z3Classifier(object):
    __doc__ = '\n    Class implementing z3 time-series classification\n    The input streams are assumed to be short\n    but many, and have non-trivial temporal patterns.\n    We first learn PFSA models for each category, using\n    all exemplars in the category simultaneously,\n    using multistream GenESeSS. Then, we use the\n    PFSA likelihood computation to ascertain which\n    category each test stream belongs to.\n\n    Author:\n        zed.uchicago.edu 2018\n\n    Inputs:\n        neighbor_fips(string)- Filename specifying neighboring counties.\n        data_path(string)- Path to MPOS, MNEG, FPOS, FNEG files.\n        genesess_path(string)- Path to GenESeSS binary\n        llk_path (string)- Path to LLK binary\n        data_len (int)- Number of time steps considered\n        jump (int)- Number of jumps considered to compute county clusters\n        model_eps (double)- GenESeSS eps\n        test_train_split (double)- Fraction of data used for testing\n        tag (string)- Name of dataset\n    Returns:\n        NA\n    '

    def __init__(self, genesess_path=os.path.dirname(os.path.realpath(__file__)) + '/bin/genESeSS', llk_path=os.path.dirname(os.path.realpath(__file__)) + '/bin/llk', trainposfile='trainpos.dat', testposfile='testpos.dat', trainnegfile='trainneg.dat', testnegfile='testneg.dat', use_own_pfsa=False, posmod='POS.pfsa', negmod='NEG.pfsa', model_eps=0.2):
        try:
            os.makedirs(result_path)
        except OSError:
            if not os.path.isdir(result_path):
                raise

        if not os.path.exists(genesess_path):
            raise AssertionError('GenESeSS binary cannot be found.')
        else:
            assert os.path.exists(llk_path), 'Pfsa likelihood estimator binary not found'
            self.GENESESS = genesess_path
            self.LLK = llk_path
            self.result_path = result_path
            self.use_own_pfsa = use_own_pfsa
            if not use_own_pfsa:
                self.neg_model = os.path.join(result_path, negmod)
                self.pos_model = os.path.join(result_path, posmod)
            else:
                self.neg_model = negmod
            self.pos_model = posmod
        self.model_eps = model_eps

    def produce_file(self, df, path, target='target'):
        path = os.path.join(self.result_path, path)
        with open(path, 'w') as (f):
            if 'record' in df.columns:
                for row in df.record:
                    f.write(row + '\n')

            else:
                for row in df.values:
                    f.write(' '.join([str(i) for i in row]) + '\n')

        return path

    def fit(self, df, peps=0.25, neps=0.2, verbose=True):
        """
        generate PFSA models for positive and negative training sets
        """
        pos = df[(df['target'] == 1)]
        neg = df[(df['target'] == 0)]
        train_pos = self.produce_file(pos.drop('target', 1), 'trainpos.dat')
        train_neg = self.produce_file(neg.drop('target', 1), 'trainneg.dat')
        sstr = self.GENESESS + ' -f ' + train_neg + ' -D row -T symbolic -o ' + self.neg_model + ' -F -t off -v 0 -e ' + str(neps)
        res = subprocess.check_output(sstr, shell=True)
        if verbose:
            print(res)
        sstr = self.GENESESS + ' -f ' + train_pos + ' -t off' + ' -F -v 0 -D row -T symbolic -o ' + self.pos_model + ' -e ' + str(peps)
        res = subprocess.check_output(sstr, shell=True)
        if verbose:
            print(res)

    def inspect_model(self):
        """
            Read in some properties of generated models
        """
        self.posstates = sum(1 for line in open(self.posmod)) - 9
        self.negstates = sum(1 for line in open(self.negmod)) - 9

    def ll_to_prob(self, l1, l2):
        """
            Convert two loglikelihoods
            into one-sum probabilities of a sequence to belong
            to either models
        """
        e1 = np.exp(-l1)
        e2 = np.exp(-l2)
        return [e1 / (e1 + e2), e2 / (e1 + e2)]

    def predictions(self, test):
        """
            Get raw loglikelihoods for each of the PFSAs
        """
        llpos = self.LLK + ' -s ' + test + ' -f ' + self.pos_model
        llneg = self.LLK + ' -s ' + test + ' -f ' + self.neg_model
        POS = np.array(subprocess.check_output(llpos, shell=True).split()).astype(float)
        NEG = np.array(subprocess.check_output(llneg, shell=True).split()).astype(float)
        return [POS, NEG]

    def predictions_ll(self, test):
        llpos = self.LLK + ' -s ' + test + ' -f ' + self.pos_model
        POS = np.array(subprocess.check_output(llpos, shell=True).split()).astype(float)
        llneg = self.LLK + ' -s ' + test + ' -f ' + self.neg_model
        NEG = np.array(subprocess.check_output(llneg, shell=True).split()).astype(float)
        return POS - NEG

    def predict_ll(self, X_test):
        test = self.produce_file(X_test, 'testfile.dat')
        return self.predictions_ll(test)

    def predict_proba(self, X_test):
        test = self.produce_file(X_test, 'testfile.dat')
        return [(self.ll_to_prob)(*i) for i in self.predictions(test)]

    def predict_loglike(self, X_test):
        test = self.produce_file(X_test, 'testfile.dat')
        return self.predictions(test)

    def predict(self, X_test):
        test = self.produce_file(X_test, 'testfile.dat')
        return [int(i[0] < i[1]) for i in self.predictions(test)]

    def evaluate(self, Xt, yt, fips):
        preds = self.predict(Xt)
        pr_preds = self.predict_proba(Xt)
        while len(pr_preds) != yt.shape[0]:
            pr_preds = self.predict_proba(Xt)

        while len(preds) != yt.shape[0]:
            preds = self.predict(Xt)

        print(Xt.shape)
        print(yt.shape)
        try:
            ACC = accuracy_score(yt, preds)
            F1 = f1_score(yt, preds)
        except:
            print(fips)
            print(len(preds))

        AUC = roc_auc_score(yt, [i[1] for i in pr_preds])
        TN, FP, FN, TP = confusion_matrix(yt, preds).ravel()
        posconf = positive_confidence(yt, preds)
        negconf = negative_confidence(yt, preds)
        dataframe = pd.DataFrame.from_dict({'fips':fips,  'AUC':AUC, 
         'F1':F1, 
         'TP':TP, 
         'FP':FP,  'TN':TN,  'FN':FN, 
         'ACC':ACC,  'POS_confid':posconf, 
         'NEG_confid':negconf},
          orient='index').transpose()
        dataframe.fillna(0, inplace=True)
        return dataframe


def read_unequalf(filepath, len_=150, sep=' '):
    """
        Fast readin of csv with unequal rows
    """
    u_f = pd.DataFrame()
    if os.path.exists(filepath):
        u_f = pd.read_csv(filepath, sep=sep, header=None,
          usecols=(range(len_)),
          engine='python',
          index_col=None)
    return u_f


def read_neighbor(sep=' '):
    """
            Read neighbor fips
        """
    n_f = pd.DataFrame()
    with open(NEIGH_FILE, 'r') as (f):
        for line in f:
            n_f = pd.concat([n_f,
             pd.DataFrame([tuple(line.strip().split(sep))])],
              ignore_index=True)

    n_f.index = n_f[0]
    del n_f[0]
    n_f.index.name = 'fips'
    return n_f


def getNeighbors(fips, jump=3):
    """
        gets neighbors which might be more than
        one jump away
    """
    neighbors = read_neighbor()
    a_x = list(set(np.array(neighbors.loc[fips].dropna()).astype(str)))
    while jump > 1:
        b_x = []
        for i in a_x:
            b_x = np.append(b_x, np.array(neighbors.loc[i].dropna()).astype(str))

        a_x = list(set(b_x))
        jump -= 1

    return a_x


def getFilenames(fips, jump, gender='M', cat='POS'):
    """
       get filenames in specified format
    """
    fp = getNeighbors(fips, jump)
    return [gender + cat + i for i in fp]