# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/cctyper/hmmer.py
# Compiled at: 2020-04-19 11:01:08
# Size of source mod 2**32: 4469 bytes
import os, subprocess, sys, logging, re, glob, tqdm, multiprocess as mp, pandas as pd

class HMMER(object):

    def __init__(self, obj):
        self.master = obj
        for key, val in vars(obj).items():
            setattr(self, key, val)

    def main_hmm(self):
        if self.redo:
            self.read_hmm()
        else:
            self.run_hmm()
            self.load_hmm()
            self.write_hmm()
        self.check_hmm()
        self.parse_hmm()

    def hmmsearch(self, hmm):
        hmm_name = re.sub('\\.hmm', '', hmm)
        logging.debug('Running HMMER against ' + hmm_name)
        with open(self.out + 'hmmer.log', 'a') as (hmmer_log):
            subprocess.run(['hmmsearch',
             '--domtblout', os.path.join(self.out + 'hmmer', hmm_name + '.tab'),
             os.path.join(self.pdir, hmm),
             self.prot_path],
              stdout=(subprocess.DEVNULL),
              stderr=hmmer_log)

    def run_hmm(self):
        logging.info('Running HMMER against Cas profiles')
        os.mkdir(self.out + 'hmmer')
        pool = mp.Pool(self.threads)
        if self.lvl == 'DEBUG' or self.simplelog:
            list(pool.imap(self.hmmsearch, os.listdir(self.pdir)))
        else:
            list(tqdm.tqdm((pool.imap(self.hmmsearch, os.listdir(self.pdir))), total=(len(os.listdir(self.pdir)))))
        pool.close()

    def load_hmm(self):
        logging.debug('Loading HMMER output')
        hmm_files = glob.glob(os.path.join(self.out + 'hmmer', '*.tab'))
        with open(self.out + 'hmmer.tab', 'w') as (hmmer_tab):
            subprocess.run((['grep', '-v', '^#'] + hmm_files), stdout=hmmer_tab)
            subprocess.run(['sed', '-i', 's/:/ /', self.out + 'hmmer.tab'])
        hmm_df = pd.read_csv((self.out + 'hmmer.tab'), sep='\\s+', header=None, usecols=(0,
                                                                                         1,
                                                                                         3,
                                                                                         6,
                                                                                         7,
                                                                                         8,
                                                                                         16,
                                                                                         17,
                                                                                         18,
                                                                                         19,
                                                                                         20,
                                                                                         21,
                                                                                         22,
                                                                                         24,
                                                                                         26,
                                                                                         28),
          names=('Hmm', 'ORF', 'tlen', 'qlen', 'Eval', 'score', 'hmm_from', 'hmm_to',
                 'ali_from', 'ali_to', 'env_from', 'env_to', 'pprop', 'start', 'end',
                 'strand'))
        hmm_df['Hmm'] = [re.sub('\\.tab', '', re.sub(os.path.join(self.out, 'hmmer', ''), '', x)) for x in hmm_df['Hmm']]
        hmm_df['Acc'] = [re.sub('_[0-9]*$', '', x) for x in hmm_df['ORF']]
        hmm_df['Pos'] = [int(re.sub('.*_', '', x)) for x in hmm_df['ORF']]

        def covs(df_sub):
            df_sub['Cov_seq'] = len(set([x for sublst in [list(range(i, j)) for i, j in zip(df_sub['ali_from'], df_sub['ali_to'] + 1)] for x in sublst])) / df_sub['tlen']
            df_sub['Cov_hmm'] = len(set([x for sublst in [list(range(i, j)) for i, j in zip(df_sub['hmm_from'], df_sub['hmm_to'] + 1)] for x in sublst])) / df_sub['qlen']
            df_sub = df_sub[['Hmm', 'ORF', 'tlen', 'qlen', 'Eval', 'score',
             'start', 'end', 'Acc', 'Pos', 'Cov_seq', 'Cov_hmm', 'strand']]
            return df_sub

        hmm_df = hmm_df.groupby(['Hmm', 'ORF']).apply(covs)
        self.hmm_df = hmm_df.drop_duplicates()

    def write_hmm(self):
        self.hmm_df.to_csv((self.out + 'hmmer.tab'), sep='\t', index=False)

    def read_hmm(self):
        self.hmm_df = pd.read_csv((self.out + 'hmmer.tab'), sep='\t')

    def check_hmm(self):
        if len(self.hmm_df) == 0:
            logging.info('No Cas proteins found.')
        else:
            self.any_cas = True

    def parse_hmm(self):
        if self.any_cas:
            logging.info('Parsing HMMER output')
            self.hmm_df.sort_values('score', ascending=False, inplace=True)
            self.hmm_df.drop_duplicates('ORF', inplace=True)