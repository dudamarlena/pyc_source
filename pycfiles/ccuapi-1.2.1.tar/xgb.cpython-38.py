# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/cctyper/xgb.py
# Compiled at: 2020-04-24 10:14:01
# Size of source mod 2**32: 3933 bytes
import logging, os, pandas as pd, numpy as np, itertools as it, xgboost as xgb

class XGB(object):

    def __init__(self, obj):
        self.master = obj
        for key, val in vars(obj).items():
            setattr(self, key, val)

        base_for = 'ACGT'
        base_rev = 'TGCA'
        self.comp_tab = str.maketrans(base_for, base_rev)

    def load_xgb_model--- This code section failed: ---

 L.  22         0  LOAD_GLOBAL              logging
                2  LOAD_METHOD              debug
                4  LOAD_STR                 'Loading xgboost model'
                6  CALL_METHOD_1         1  ''
                8  POP_TOP          

 L.  24        10  LOAD_GLOBAL              xgb
               12  LOAD_METHOD              Booster
               14  LOAD_STR                 'nthread'
               16  LOAD_FAST                'self'
               18  LOAD_ATTR                threads
               20  BUILD_MAP_1           1 
               22  CALL_METHOD_1         1  ''
               24  STORE_FAST               'bst'

 L.  25        26  LOAD_FAST                'bst'
               28  LOAD_METHOD              load_model
               30  LOAD_FAST                'self'
               32  LOAD_ATTR                xgb
               34  CALL_METHOD_1         1  ''
               36  POP_TOP          

 L.  26        38  LOAD_FAST                'bst'
               40  LOAD_FAST                'self'
               42  STORE_ATTR               bst

 L.  29        44  LOAD_GLOBAL              open
               46  LOAD_FAST                'self'
               48  LOAD_ATTR                typedict
               50  LOAD_STR                 'r'
               52  CALL_FUNCTION_2       2  ''
               54  SETUP_WITH           92  'to 92'
               56  STORE_FAST               'f'

 L.  30        58  LOAD_GENEXPR             '<code_object <genexpr>>'
               60  LOAD_STR                 'XGB.load_xgb_model.<locals>.<genexpr>'
               62  MAKE_FUNCTION_0          ''
               64  LOAD_FAST                'f'
               66  GET_ITER         
               68  CALL_FUNCTION_1       1  ''
               70  STORE_FAST               'rs'

 L.  31        72  LOAD_DICTCOMP            '<code_object <dictcomp>>'
               74  LOAD_STR                 'XGB.load_xgb_model.<locals>.<dictcomp>'
               76  MAKE_FUNCTION_0          ''
               78  LOAD_FAST                'rs'
               80  GET_ITER         
               82  CALL_FUNCTION_1       1  ''
               84  LOAD_FAST                'self'
               86  STORE_ATTR               label_dict
               88  POP_BLOCK        
               90  BEGIN_FINALLY    
             92_0  COME_FROM_WITH       54  '54'
               92  WITH_CLEANUP_START
               94  WITH_CLEANUP_FINISH
               96  END_FINALLY      

Parse error at or near `BEGIN_FINALLY' instruction at offset 90

    def generate_canonical_kmer(self):
        logging.debug'Generating canonical {}mers'.formatself.kmer
        letters = [
         'A', 'C', 'G', 'T']
        all_kmer = [''.joink for k in it.product(letters, repeat=(self.kmer))]
        all_kmer_rev = [x.translateself.comp_tab[::-1] for x in all_kmer]
        can_kmer = list(it.compress(all_kmer_rev, [not kf < kr for kf, kr in zipall_kmerall_kmer_rev]))
        can_kmer.sort()
        self.can_kmer = can_kmer

    def count_kmer(self, seq):
        kmer_d = {}
        for i in range(len(seq) - self.kmer + 1):
            kmer_for = seq[i:i + self.kmer]
            kmer_rev = kmer_for.translateself.comp_tab[::-1]
            if kmer_for < kmer_rev:
                kmer = kmer_for
            else:
                kmer = kmer_rev
            if kmer in kmer_d:
                kmer_d[kmer] += 1
            else:
                kmer_d[kmer] = 1

        return kmer_d

    def xgb_run(self):
        if not self.redo:
            self.repeats = [x.cons for x in self.crisprs]
            df = pd.read_csv((self.out + 'crisprs_all.tab'), sep='\t')
            if len(df) > 0:
                self.any_crispr = True
            else:
                logging.info'No CRISPRs found.'
                os.remove(self.out + 'crisprs_all.tab')
            if self.any_crispr:
                self.predict_repeats()
                df['Prediction'] = self.z_type
                df['Subtype'] = self.z_type
                df['Subtype_probability'] = self.z_max
                df.loc[(df.Subtype_probability < self.pred_prob, 'Prediction')] = 'Unknown'
                df['Subtype_probability'] = df['Subtype_probability'].round3
                df.to_csv((self.out + 'crisprs_all.tab'), sep='\t', index=False)

    def predict_repeats(self):
        logging.info'Predicting subtype of CRISPR repeats'
        self.load_xgb_model()
        self.generate_canonical_kmer()
        self.repeats = [x.upper() for x in self.repeats]
        z_df = pd.DataFrame([dict(zipself.can_kmernp.zeroslen(self.can_kmer))] + [self.count_kmerx for x in self.repeats]).fillna0
        z_df = z_df.reindex((sorted(z_df.columns)), axis=1)
        self.z_pred = self.bst.predict((xgb.DMatrixz_df), ntree_limit=(int(self.bst.attr'best_iteration')))
        self.z_best = [x.argmax() for x in self.z_pred][1:len(self.z_pred)]
        self.z_max = [x.max() for x in self.z_pred][1:len(self.z_pred)]
        self.z_type = [self.label_dict[str(x)] for x in self.z_best]

    def print_xgb(self):
        for i in range(len(self.repeats)):
            print('{}\t{}\t{}'.format(self.repeats[i], self.z_type[i], self.z_max[i]))