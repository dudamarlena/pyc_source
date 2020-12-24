# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/tareen/Desktop/Desktop_Tests/MPathic3/mpathic/src/Models.py
# Compiled at: 2018-06-22 14:34:54
# Size of source mod 2**32: 11081 bytes
"""Class container for Model Handling in the sortseq package. We currently
    only support linear and nearest neighbor models for use within the package.
    In the future, support for additional model types will be added"""
from __future__ import division
import importlib, sys, numpy as np
from mpathic.src import utils
import scipy as sp, pandas as pd, pdb
from mpathic.src import qc
from mpathic.src import io_local as io
from mpathic.src import fast
import time
from mpathic import SortSeqError
from mpathic.src import numerics

class ExpModel:
    pass


class LinearModel(ExpModel):
    __doc__ = ' This model generates energies of binding \n        through a linear energy matrix model'

    def __init__(self, model_df):
        """
        Constructor takes model parameters in the form of a model dataframe
        """
        model_df = qc.validate_model((model_df.copy()), fix=True)
        seqtype, modeltype = qc.get_model_type(model_df)
        if not modeltype == 'MAT':
            raise SortSeqError('Invalid modeltype: %s' % modeltype)
        seq_dict, inv_dict = utils.choose_dict(seqtype, modeltype=modeltype)
        self.seqtype = seqtype
        self.seq_dict = seq_dict
        self.inv_dict = inv_dict
        self.df = model_df
        self.length = model_df.shape[0]
        headers = qc.get_cols_from_df(model_df, 'vals')
        self.matrix = np.transpose(np.array(model_df[headers]))

    def genexp(self, seqs):
        return self.evaluate(seqs)

    def evaluate(self, seqs):
        if isinstance(seqs, pd.DataFrame):
            seq_col = qc.get_cols_from_df(seqs, 'seqs')[0]
            seqs_to_use = list(seqs[seq_col])
        else:
            if not (isinstance(seqs, list) or isinstance(seqs, pd.Series)):
                raise SortSeqError('Sequences must be input as a list, pd.Series, or pd.DataFrame')
            else:
                seqs_to_use = list(seqs)
            if len(seqs_to_use[0]) != self.length:
                raise SortSeqError('Energy Matrix Length does not equal Sequence Length')
            t0 = time.time()
            if not isinstance(self.seqtype, bytes):
                self.seqtype = str(self.seqtype).encode('utf-8')
            if not isinstance(seqs_to_use[0], bytes):
                for i in range(len(seqs_to_use)):
                    seqs_to_use[i] = str(seqs_to_use[i]).encode('utf-8')

        seqarray = fast.seqs2array_for_matmodel(seqs_to_use, self.seqtype)
        t1 = time.time()
        vals = self.evaluate_on_seqarray(seqarray)
        t2 = time.time()
        return vals

    def evaluate_on_seqarray(self, seqarray):
        matrix_vec = np.matrix(np.array(self.matrix.T).ravel()).T
        return np.array(np.matrix(seqarray) * matrix_vec).ravel()

    def evaluate_on_mutarray(self, mutarray, wtrow):
        return numerics.eval_modelmatrix_on_mutarray(modelmatrix=(self.matrix.T),
          mutarray=mutarray,
          wtrow=wtrow)


class NeighborModel(ExpModel):
    __doc__ = ' This model generates energies of binding \n        through a nearest neighbor matrix model'

    def __init__(self, model_df):
        """
        Constructor takes model parameters in the form of a model dataframe
        """
        model_df = qc.validate_model((model_df.copy()), fix=True)
        seqtype, modeltype = qc.get_model_type(model_df)
        if not modeltype == 'NBR':
            raise SortSeqError('Invalid modeltype: %s' % modeltype)
        seq_dict, inv_dict = utils.choose_dict(seqtype, modeltype=modeltype)
        self.seqtype = seqtype
        self.seq_dict = seq_dict
        self.inv_dict = inv_dict
        self.df = model_df
        self.length = model_df.shape[0] + 1
        headers = qc.get_cols_from_df(model_df, 'vals')
        self.matrix = np.transpose(np.array(model_df[headers]))

    def genexp(self, seqs):
        return self.evaluate(seqs)

    def evaluate(self, seqs):
        if isinstance(seqs, pd.DataFrame):
            seq_col = qc.get_cols_from_df(seqs, 'seqs')[0]
            seqs_to_use = list(seqs[seq_col])
        else:
            if not (isinstance(seqs, list) or isinstance(seqs, pd.Series)):
                raise SortSeqError('Sequences must be input as a list, pd.Series, or pd.DataFrame')
            else:
                seqs_to_use = list(seqs)
        if len(seqs_to_use[0]) != self.length:
            raise SortSeqError('Energy Matrix Length does not equal Sequence Length')
        t0 = time.time()
        seqarray = fast.seqs2array_for_nbrmodel(seqs_to_use, self.seqtype)
        t1 = time.time()
        vals = self.evaluate_on_seqarray(seqarray)
        t2 = time.time()
        return vals

    def evaluate_on_seqarray(self, seqarray):
        matrix_vec = np.matrix(np.array(self.matrix.T).ravel()).T
        return np.array(np.matrix(seqarray) * matrix_vec).ravel()

    def evaluate_on_mutarray(self, mutarray, wtrow):
        return numerics.eval_modelmatrix_on_mutarray(modelmatrix=(self.matrix.T),
          mutarray=mutarray,
          wtrow=wtrow)


class RaveledModel(ExpModel):
    __doc__ = 'This model type generates an energy matrix model, \n        but accepts flattened matrices (for sklearn based fitting). It will not\n        generate models from files or dataframes.'

    def __init__(self, param):
        self.matrix = param

    def genexp(self, sparse_seqs_mat, sample_weight=None):
        if sp.sparse.issparse(sparse_seqs_mat):
            n_seqs = sparse_seqs_mat.shape[0]
            energies = np.zeros(n_seqs)
            energiestemp = sparse_seqs_mat.multiply(self.matrix).sum(axis=1)
            for i in range(0, n_seqs):
                energies[i] = energiestemp[i]

        else:
            raise SortSeqError('Enter sparse sequence matrix.')
        if sample_weight:
            t_exp = np.zeros(np.sum(sample_weights))
            counter = 0
            for i, sw in enumerate(sample_weight):
                t_exp[counter:counter + sample_weight[i]] = -energies[i]
                counter = counter + sample_weight[i]

            return t_exp
        else:
            return energies


class NoiseModel:

    def gennoisyexp(self, logexp):
        """If no particular noise function is declared, then just assume no
            noise"""
        return logexp

    def genlist(self, df):
        nlist = []
        T_counts = np.sum(df['ct'])
        nexp = np.zeros(T_counts)
        counter = 0
        seqcol = [c for c in df.columns if qc.is_col_type(c, 'seqs')][0]
        for i, seq in enumerate(df[seqcol]):
            exp = df['val'][i]
            counts = df['ct'][i]
            explist = [exp for z in range(counts)]
            noisyexp = self.gennoisyexp(explist)
            nlist.append(noisyexp)
            nexp[counter:counter + counts] = noisyexp
            counter = counter + counts

        return (
         nexp, nlist)


class LogNormalNoise(NoiseModel):
    __doc__ = 'Noise model that adds autoflourescence and then draws the noisy \n        measurement from a log normal distribution with this mean'

    def __init__(self, npar):
        self.auto = float(npar[0])
        self.scale = float(npar[1])
        if self.auto <= 0 or self.scale <= 0:
            raise SortSeqError('Noise model parameters must be great than zero')

    def gennoisyexp(self, logexp):
        exp = np.exp(logexp) + self.auto
        nexp = np.random.lognormal(np.log(exp), self.scale)
        return np.log(nexp)


class NormalNoise(NoiseModel):
    __doc__ = 'Add Gaussian Noise'

    def __init__(self, npar):
        try:
            self.scale = float(npar[0])
        except ValueError:
            raise SortSeqError('your input parameter must be a float')

        if self.scale <= 0:
            raise SortSeqError('your input scale for normal noise must be greater                than zero')

    def gennoisyexp(self, logexp):
        s = np.abs(logexp).mean() * self.scale + 1e-06
        nexp = logexp + np.random.normal(scale=s,
          size=(len(logexp)))
        return nexp


class PoissonNoise(NoiseModel):
    __doc__ = 'Add Noise for mpra experiment Expression Measurements'

    def gennoisyexp(self, df, T_LibCounts, T_mRNACounts, mult=1):
        exp = np.exp(-df['val'] * mult)
        libcounts = df['ct']
        weights = exp * libcounts
        meanexp = T_mRNACounts * weights / np.sum(weights)
        meanlibcounts = libcounts / np.sum(libcounts) * T_LibCounts
        noisyexp = np.random.poisson(lam=meanexp)
        noisylibcounts = np.random.poisson(lam=meanlibcounts)
        return (noisylibcounts, noisyexp)