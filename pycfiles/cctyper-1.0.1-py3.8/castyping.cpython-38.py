# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/cctyper/castyping.py
# Compiled at: 2020-04-19 11:01:09
# Size of source mod 2**32: 10219 bytes
import re, logging, sys, numpy as np, pandas as pd, multiprocessing as mp
from itertools import chain
from scipy import ndimage

class Typer(object):

    def __init__(self, obj):
        self.master = obj
        for key, val in vars(obj).items():
            setattr(self, key, val)

    def type_operon(self, operon):
        """
        Subtype of a single operon
        """
        logging.debug('Typing operon ' + operon)
        tmp = self.hmm_df_all[(self.hmm_df_all['operon'] == operon)].sort_values('Pos')
        tmpX = tmp.sort_values('score', ascending=False)
        tmpX['Hmm'] = [re.sub('_.*', '', x) for x in tmpX['Hmm']]
        tmpX.drop_duplicates('Hmm', inplace=True)
        start = list(tmp['start'])
        end = list(tmp['end'])
        if operon in self.circ_operons:
            gene_end = np.argmax(np.diff(list(tmp['Pos'])))
            start_operon = start[(gene_end + 1)]
            end_operon = end[gene_end]
        else:
            start_operon = min(start + end)
            end_operon = max(start + end)
        type_scores = tmpX.iloc[:, 14:].sum(axis=0)
        best_score = np.amax(type_scores)
        best_type = type_scores.index.values[np.argmax(type_scores.values)]
        if len(tmpX) >= 3:
            if best_score <= 5:
                if any([x in self.signature for x in list(tmpX['Hmm'])]):
                    if sum(type_scores == best_score) > 1:
                        prediction = 'Ambiguous'
                        best_type = list(type_scores.index.values[(type_scores.values == np.amax(type_scores.values))])
                    else:
                        prediction = best_type
                else:
                    prediction = 'False'
            else:
                if len(tmpX) >= 6:
                    zzz = tmpX.iloc[:, 14:].transpose()
                    zzz = zzz[zzz.apply((lambda r: any(r >= 3)), axis=1)]
                    zzz = zzz.loc[:, zzz.apply((lambda r: sum(r > 0) == 1), axis=0)]
                    zzz[zzz < 0] = 0
                    zzz['sum'] = zzz.sum(axis=1)
                    zzz = zzz[(zzz['sum'] >= 6)]
                    if len(zzz) > 1:
                        prediction = 'Hybrid({})'.format(','.join(zzz.index))
                    else:
                        prediction = best_type
                else:
                    if sum(type_scores == best_score) > 1:
                        prediction = 'Ambiguous'
                        best_type = list(type_scores.index.values[(type_scores.values == np.amax(type_scores.values))])
                    else:
                        prediction = best_type
        else:
            if len(tmpX) == 2:
                first_signature = list(tmpX['Hmm'])[0] in self.signature
                second_signature = list(tmpX['Hmm'])[1] in self.signature
                accept = first_signature or second_signature
            else:
                if len(tmpX) == 1:
                    accept = list(tmpX['Hmm'])[0] in self.signature
                if accept:
                    if sum(type_scores == best_score) > 1:
                        prediction = 'Ambiguous'
                        best_type = list(type_scores.index.values[(type_scores.values == np.amax(type_scores.values))])
                    else:
                        prediction = best_type
                else:
                    prediction = 'False'
        outdict = {'Contig':list(tmp['Acc'])[0], 
         'Operon':operon, 
         'Start':start_operon, 
         'End':end_operon, 
         'Prediction':prediction, 
         'Best_type':best_type, 
         'Best_score':best_score, 
         'Genes':list(tmp['Hmm']), 
         'Positions':list(tmp['Pos']), 
         'E-values':['{:0.2e}'.format(x) for x in list(tmp['Eval'])], 
         'CoverageSeq':[round(x, 3) for x in list(tmp['Cov_seq'])], 
         'CoverageHMM':[round(x, 3) for x in list(tmp['Cov_hmm'])]}
        return outdict

    def cluster_adj(self, data):
        """
        Cluster adjacent genes into operons

        Params:
        data: A pandas data.frame with an Acc (accession number) column and a Pos (gene posistion) column
        dist: Int. Max allowed distance between genes in an operon

        Returns:
        List. Operon IDs with the same length and order as the input data.frame
        """
        dist = self.dist
        positions = list(data['Pos'])
        if self.circular:
            pos_range = max(self.genes[(self.genes['Contig'] == list(data['Acc'])[0])]['Pos']) * [0]
        else:
            pos_range = max(positions) * [0]
        for x in positions:
            pos_range[x - 1] = 1
        else:
            pad = list(np.zeros(dist, dtype=int))
            pos_range_pad = pad + pos_range + pad
            pos_range_dilated = ndimage.morphology.binary_closing(pos_range_pad, structure=(list(np.ones(dist + 1))))
            clust_pad, nclust = ndimage.label(pos_range_dilated)
            clust = clust_pad[dist:len(clust_pad) - dist]
            is_circ = False
            if self.circular:
                if any(clust[len(clust) - dist - 1:] > 0):
                    if any(clust[:dist + 1] > 0):
                        last_num = clust[len(clust) - dist - 1:][(clust[len(clust) - dist - 1:] > 0)][0]
                        first_num = clust[:dist + 1][(clust[:dist + 1] > 0)][0]
                        if last_num != first_num:
                            clust[clust == last_num] = first_num
                            is_circ = True
            return [
             [list(data['Acc'])[0] + '@' + str(clust[(x - 1)]) for x in positions], is_circ]

    def typing(self):
        """
        Subtyping of putative Cas operons
        """
        if self.any_cas:
            logging.info('Subtyping putative operons')
            specifics = []
            for key, value in self.cutoffs.items():
                which_sub = [i for i in list(self.hmm_df['Hmm']) if key.lower() in i.lower()]
                if len(which_sub) > 0:
                    specifics.extend(which_sub)
                    self.hmm_df = self.hmm_df[((self.hmm_df['Eval'] < float(value[0])) & (self.hmm_df['Cov_seq'] >= float(value[1])) & (self.hmm_df['Cov_hmm'] >= float(value[2])) | [x not in which_sub for x in self.hmm_df['Hmm']])]
            else:
                self.hmm_df = self.hmm_df[((self.hmm_df['Cov_seq'] >= self.ocs) & (self.hmm_df['Cov_hmm'] >= self.och) & (self.hmm_df['Eval'] < self.oev) | [x in specifics for x in self.hmm_df['Hmm']])]
                if self.circular:
                    if self.redo:
                        self.genes = pd.read_csv((self.out + 'genes.tab'), sep='\t')
                self.hmm_df = self.hmm_df.sort_values('Acc')
                operons = self.hmm_df.groupby('Acc').apply(self.cluster_adj)
                self.hmm_df.loc[:, 'operon'] = list(chain.from_iterable([x[0] for x in list(operons)]))
                self.circ_operons = []
                any_circ = [x[1] for x in list(operons)]
                if any(any_circ):
                    self.circ_operons = [sorted(i)[0] for i, v in zip([x[0] for x in list(operons)], any_circ) if v]
                scores = pd.read_csv((self.scoring), sep=',')
                scores.fillna(0, inplace=True)
                self.signature = [re.sub('_.*', '', x) for x in list(specifics)]
                self.hmm_df_all = pd.merge((self.hmm_df), scores, on='Hmm')
                operons_unq = set(self.hmm_df_all['operon'])
                dictlst = [self.type_operon(operonID) for operonID in operons_unq]
                self.preddf = pd.DataFrame(dictlst)
                self.check_type()
                self.write_type()

    def check_type(self):
        if self.any_cas:
            if len(self.preddf) == 0:
                logging.info('No operons found.')
            else:
                self.any_operon = True

    def write_type(self):
        if self.any_operon:
            operons_good = self.preddf[(~self.preddf['Prediction'].isin(['False', 'Ambiguous']))]
            operons_put = self.preddf[self.preddf['Prediction'].isin(['False', 'Ambiguous'])]
            if len(operons_good) > 0:
                operons_good.to_csv((self.out + 'cas_operons.tab'), sep='\t', index=False)
            if len(operons_put) > 0:
                operons_put.to_csv((self.out + 'cas_operons_putative.tab'), sep='\t', index=False)