# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/cctyper/xgb.py
# Compiled at: 2020-04-24 10:14:01
# Size of source mod 2**32: 3933 bytes
import logging, os, pandas as pd, numpy as np, itertools as it, xgboost as xgb

class XGB(object):

    def __init__(self, obj):
        self.master = obj
        for key, val in vars(obj).items():
            setattr(self, key, val)
        else:
            base_for = 'ACGT'
            base_rev = 'TGCA'
            self.comp_tab = str.maketrans(base_for, base_rev)

    def load_xgb_model(self):
        logging.debug('Loading xgboost model')
        bst = xgb.Booster({'nthread': self.threads})
        bst.load_model(self.xgb)
        self.bst = bst
        with open(self.typedict, 'r') as (f):
            rs = (ll.rstrip().split(':') for ll in f)
            self.label_dict = {r[0]:r[1] for r in rs}

    def generate_canonical_kmer(self):
        logging.debug('Generating canonical {}mers'.format(self.kmer))
        letters = [
         'A', 'C', 'G', 'T']
        all_kmer = [''.join(k) for k in it.product(letters, repeat=(self.kmer))]
        all_kmer_rev = [x.translate(self.comp_tab)[::-1] for x in all_kmer]
        can_kmer = list(it.compress(all_kmer_rev, [not kf < kr for kf, kr in zip(all_kmer, all_kmer_rev)]))
        can_kmer.sort()
        self.can_kmer = can_kmer

    def count_kmer(self, seq):
        kmer_d = {}
        for i in range(len(seq) - self.kmer + 1):
            kmer_for = seq[i:i + self.kmer]
            kmer_rev = kmer_for.translate(self.comp_tab)[::-1]
            if kmer_for < kmer_rev:
                kmer = kmer_for
            else:
                kmer = kmer_rev
            if kmer in kmer_d:
                kmer_d[kmer] += 1
            else:
                kmer_d[kmer] = 1
        else:
            return kmer_d

    def xgb_run(self):
        if not self.redo:
            self.repeats = [x.cons for x in self.crisprs]
            df = pd.read_csv((self.out + 'crisprs_all.tab'), sep='\t')
            if len(df) > 0:
                self.any_crispr = True
            else:
                logging.info('No CRISPRs found.')
                os.remove(self.out + 'crisprs_all.tab')
            if self.any_crispr:
                self.predict_repeats()
                df['Prediction'] = self.z_type
                df['Subtype'] = self.z_type
                df['Subtype_probability'] = self.z_max
                df.loc[(df.Subtype_probability < self.pred_prob, 'Prediction')] = 'Unknown'
                df['Subtype_probability'] = df['Subtype_probability'].round(3)
                df.to_csv((self.out + 'crisprs_all.tab'), sep='\t', index=False)

    def predict_repeats(self):
        logging.info('Predicting subtype of CRISPR repeats')
        self.load_xgb_model()
        self.generate_canonical_kmer()
        self.repeats = [x.upper() for x in self.repeats]
        z_df = pd.DataFrame([dict(zip(self.can_kmer, np.zeros(len(self.can_kmer))))] + [self.count_kmer(x) for x in self.repeats]).fillna(0)
        z_df = z_df.reindex((sorted(z_df.columns)), axis=1)
        self.z_pred = self.bst.predict((xgb.DMatrix(z_df)), ntree_limit=(int(self.bst.attr('best_iteration'))))
        self.z_best = [x.argmax() for x in self.z_pred][1:len(self.z_pred)]
        self.z_max = [x.max() for x in self.z_pred][1:len(self.z_pred)]
        self.z_type = [self.label_dict[str(x)] for x in self.z_best]

    def print_xgb(self):
        for i in range(len(self.repeats)):
            print('{}\t{}\t{}'.format(self.repeats[i], self.z_type[i], self.z_max[i]))