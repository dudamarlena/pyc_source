# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/tareen/Desktop/Desktop_Tests/MPathic3/mpathic/src/learn_model.py
# Compiled at: 2018-06-21 15:27:41
# Size of source mod 2**32: 40899 bytes
"""
Doc-string from learn_model_class:
A script which produces linear energy matrix models for a given data set.
"""
from __future__ import division
import numpy as np, scipy as sp, sys, scipy.sparse, pandas as pd
from mpathic.src import utils
from sklearn import linear_model
from mpathic.src import EstimateMutualInfoforMImax
import pymc
from mpathic.src import stepper
import os
from mpathic import SortSeqError
from mpathic.src import io_local as io
from mpathic.src import gauge
from mpathic.src import qc
import pdb
from mpathic import shutthefuckup
from mpathic.src import numerics
from sklearn.preprocessing import StandardScaler
import cvxopt
from cvxopt import solvers, matrix, spdiag, sqrt, div, exp
import warnings
from mpathic.src.profile_mut import ProfileMut
from mpathic.src.utils import handle_errors, check, ControlledError
from mpathic.src import fast

class LearnModel:
    __doc__ = '\n     Constructor for the learn model class. Models can be learnt via the matrix model or\n     the neighbor model. Matrix models assume independent contributions to activity\n     from characters at a particular position whereas neighbor model assume near contributions\n     to activity from all possible adjacent characters.\n\n     Parameters\n     ----------\n\n     df: (pandas data frame)\n         Dataframe containing several columns representing \n\n         bins and sequence column. The integer values in bins \n\n         represent the occurrence of the sequence that bin.\n\n     lm: (str)\n         Learning model. Possible values include {\'ER\',\'LS\',\'IM\', \'PR\'}. \n\n         \'ER\': enrichment ratio inference. \'LS\': least squares \n\n         optimization. \'IM\' : mutual information maximization \n\n         (similar to maximum likelihood inference in the large data limit). \n\n         \'PR\' stands for Poisson Regression.\n\n     modeltype: (string)\n         Type of model to be learned. Valid choices include "MAT" \n\n         and "NBR", which stands for matrix model and neigbhour model, \n\n         respectively. Matrix model assumes mutations at a location are \n\n         independent and neighbour model assumes epistatic effects for \n\n         mutations.\n\n     LS_means_std: (pandas dataframe)\n         For the least-squares method, this contains \n\n         the user supplied mean and standard deviation. \n\n         The order of the columns is [\'bin\', \'mean\', \'std\'].\n\n\n     db: (string)\n         File name for a SQL script; it could be passed \n\n         in to the function MaximizeMI_memsaver\n\n     iteration: (int)\n         Total number of MCMC iterations to do. Passed \n\n         in the sample method from MCMC.py which may be \n\n         part of pymc.\n\n     burnin: (int)\n          Variables will not be tallied until this many \n\n          iterations are complete (thermalization).\n\n     thin: (int)\n         Similar to parameter burnin, but with smaller \n\n         default value.\n\n     runnum: (int)\n         Run number, used to determine the correct sql \n\n         script extension in MaximizeMI_memsaver\n\n     initialize: (string)\n         Variable for initializing the learn model class \n\n         constructor. Valid values include "rand", \n\n         "LS", "PR". rand is MCMC, LS is least squares \n\n          and PR and poisson regression.\n\n     start: (int)\n         Starting position of the sequence.\n\n     end: (int)\n         end position of the sequence.\n\n     foreground: (int)\n         Indicates column number representing foreground \n\n         (E.g. can be passed to Berg_Von_Hippel method).\n\n     background: (int)\n         Indicates column number representing background.\n\n     alpha : (float)\n         Regularization strength; must be a positive float. Regularization \n\n         improves the conditioning of the problem and reduces the variance of \n\n         the estimates. Larger values specify stronger regularization. \n\n         Alpha corresponds to ``C^-1`` in other linear models such as \n\n         LogisticRegression or LinearSVC. (this snippet taken from ridge.py \n\n         written by Mathieu Blondel)\n\n     pseudocounts: (int)\n         A artificial number added to bin counts where counts are \n\n         really low. Needs to be Non-negative.\n\n     verbose: (bool)\n         A value of false for this parameter suppresses the \n\n         output to screen.\n\n     tm: (int)\n         Number bins. DOUBLE CHECK.\n     '

    @handle_errors
    def __init__(self, df, lm='ER', modeltype='MAT', LS_means_std=None, db=None, iteration=30000, burnin=1000, thin=10, runnum=0, initialize='LS', start=0, end=None, foreground=1, background=0, alpha=0.0, pseudocounts=1, drop_library=False, verbose=False, tm=None):
        self.df = df
        self.lm = lm
        self.modeltype = modeltype
        self.LS_means_std = LS_means_std
        self.db = db
        self.iteration = iteration
        self.burnin = burnin
        self.thin = thin
        self.runnum = runnum
        self.initialize = initialize
        self.start = start
        self.end = end
        self.foreground = foreground
        self.background = background
        self.alpha = alpha
        self.pseudocounts = pseudocounts
        self.drop_library = drop_library
        self.verbose = verbose
        self.tm = tm
        self.output_df = None
        self._input_checks()
        seq_cols = qc.get_cols_from_df(df, 'seqs')
        if not len(seq_cols) == 1:
            raise SortSeqError('Dataframe has multiple seq cols: %s' % str(seq_cols))
        else:
            dicttype = qc.colname_to_seqtype_dict[seq_cols[0]]
            seq_dict, inv_dict = utils.choose_dict(dicttype, modeltype=modeltype)
            type_name_dict = {'dna':'seq', 
             'rna':'seq_rna',  'protein':'seq_pro'}
            seq_col_name = type_name_dict[dicttype]
            lin_seq_dict, lin_inv_dict = utils.choose_dict(dicttype, modeltype='MAT')
            par_seq_dict = {v:k for v, k in seq_dict.items() if k != len(seq_dict) - 1}
            df = df[(df.loc[:, 'ct'] != 0)]
            df.reset_index(drop=True, inplace=True)
            if len(set(df[seq_col_name].apply(len))) > 1:
                sys.stderr.write('Lengths of all sequences are not the same!')
            df.loc[:, seq_col_name] = df.loc[:, seq_col_name].str.slice(start, end)
            df = utils.collapse_further(df)
            col_headers = utils.get_column_headers(df)
            df[col_headers] = df[col_headers].astype(int)
            val_cols = ['val_' + inv_dict[i] for i in range(len(seq_dict))]
            df.reset_index(inplace=True, drop=True)
            if not end:
                seqL = len(df[seq_col_name][0]) - start
            else:
                seqL = end - start
        df = df[(df[seq_col_name].apply(len) == seqL)]
        df.reset_index(inplace=True, drop=True)
        if lm == 'ER':
            if modeltype == 'NBR':
                emat = self.Markov(df, dicttype, foreground=foreground, background=background, pseudocounts=pseudocounts)
            else:
                emat = self.Berg_von_Hippel(df,
                  dicttype, foreground=foreground, background=background, pseudocounts=pseudocounts)
        if lm == 'PR':
            emat = self.convex_opt(df, seq_dict, inv_dict, col_headers, tm=tm, dicttype=dicttype,
              modeltype=modeltype)
        if lm == 'LS':
            if LS_means_std:
                means_std_df = io.load_meanstd(LS_means_std)
                labels = list(means_std_df['bin'].apply(self.add_label))
                std = means_std_df['std']
                std.index = labels
                df[labels] = df[labels].div(std)
                means = means_std_df['mean']
                means.index = labels
            else:
                means = None
            df['ct'] = df[col_headers].sum(axis=1)
            df = df[(df.ct != 0)]
            df.reset_index(inplace=True, drop=True)
            if drop_library:
                try:
                    df.drop('ct_0', inplace=True)
                    col_headers = utils.get_column_headers(df)
                    if len(col_headers) < 2:
                        raise SortSeqError('After dropping library there are no longer enough \n                            columns to run the analysis')
                except:
                    raise SortSeqError('drop_library option was passed, but no ct_0\n                        column exists')

            print('init learn model: \n')
            print(par_seq_dict)
            print('dict: ', dicttype)
            raveledmat, batch, sw = utils.genweightandmat(df,
              par_seq_dict, dicttype, means=means, modeltype=modeltype)
            emat = self.Compute_Least_Squares(raveledmat, batch, sw, alpha=alpha)
        if lm == 'IM':
            seq_mat, wtrow = numerics.dataset2mutarray(df.copy(), modeltype)
            if initialize == 'rand':
                if modeltype == 'MAT':
                    emat_0 = utils.RandEmat(len(df[seq_col_name][0]), len(seq_dict))
                else:
                    if modeltype == 'NBR':
                        emat_0 = utils.RandEmat(len(df[seq_col_name][0]) - 1, len(seq_dict))
            else:
                if initialize == 'LS':
                    emat_cols = ['val_' + inv_dict[i] for i in range(len(seq_dict))]
                    emat_0_df = LearnModel((df.copy()), lm='LS', modeltype=modeltype, alpha=alpha, start=0, end=None, verbose=verbose).output_df
                    emat_0 = np.transpose(np.array(emat_0_df[emat_cols]))
                else:
                    if initialize == 'PR':
                        emat_cols = ['val_' + inv_dict[i] for i in range(len(seq_dict))]
                        emat_0_df = LearnModel((df.copy()), lm='PR', modeltype=modeltype, start=0, end=None).output_df
                        emat_0 = np.transpose(np.array(emat_0_df[emat_cols]))
            emat = self.MaximizeMI_memsaver(seq_mat, (df.copy()), emat_0, wtrow, db=db, iteration=iteration, burnin=burnin,
              thin=thin,
              runnum=runnum,
              verbose=verbose)
        if lm == 'IM' or lm == 'memsaver':
            if modeltype == 'NBR':
                try:
                    emat_typical = gauge.fix_neighbor(np.transpose(emat))
                except:
                    sys.stderr.write('Gauge Fixing Failed')
                    emat_typical = np.transpose(emat)

            else:
                if modeltype == 'MAT':
                    try:
                        emat_typical = gauge.fix_matrix(np.transpose(emat))
                    except:
                        sys.stderr.write('Gauge Fixing Failed')
                        emat_typical = np.transpose(emat)

        else:
            if lm == 'ER':
                if modeltype == 'NBR':
                    emat_cols = ['val_' + inv_dict[i] for i in range(len(seq_dict))]
                    emat_typical = emat[emat_cols]
                else:
                    emat_cols = ['val_' + inv_dict[i] for i in range(len(seq_dict))]
                    emat_typical = emat[emat_cols]
                    try:
                        emat_typical = gauge.fix_matrix(np.array(emat_typical))
                    except:
                        sys.stderr.write('Gauge Fixing Failed')
                        emat_typical = emat_typical

            else:
                if lm == 'MK':
                    pass
                else:
                    if lm == 'PR':
                        emat_typical = np.transpose(emat)
                    else:
                        emat_typical = utils.emat_typical_parameterization(emat, len(seq_dict))
        if modeltype == 'NBR':
            try:
                emat_typical = gauge.fix_neighbor(np.transpose(emat_typical))
            except:
                sys.stderr.write('Gauge Fixing Failed')
                emat_typical = np.transpose(emat_typical)

        else:
            if modeltype == 'MAT':
                try:
                    emat_typical = gauge.fix_matrix(np.transpose(emat_typical))
                except:
                    sys.stderr.write('Gauge Fixing Failed')
                    emat_typical = np.transpose(emat_typical)

            else:
                em = pd.DataFrame(emat_typical)
                em.columns = val_cols
                if modeltype == 'NBR':
                    pos = pd.Series((range(start, start - 1 + len(df[seq_col_name][0]))), name='pos')
                else:
                    pos = pd.Series((range(start, start + len(df[seq_col_name][0]))), name='pos')
            output_df = pd.concat([pos, em], axis=1)
            output_df = qc.validate_model(output_df, fix=True)
            self.output_df = output_df

    def _input_checks(self):
        """
        check input parameters for correctness
        """
        if self.df is None:
            raise ControlledError(" The Learn Model class requires pandas dataframe as input dataframe. Entered df was 'None'.")
        else:
            if self.df is not None:
                check(isinstance(self.df, pd.DataFrame), 'type(df) = %s; must be a pandas dataframe ' % type(self.df))
                check(pd.DataFrame.equals(self.df, qc.validate_dataset(self.df)), ' Input dataframe failed quality control,                   please ensure input dataset has the correct format of an mpathic dataframe ')
            else:
                check(isinstance(self.lm, str), 'type(lm) = %s must be a string ' % type(self.lm))
                valid_lm_values = [
                 'ER', 'LS', 'IM', 'PR']
                check(self.lm in valid_lm_values, 'lm = %s; must be in %s' % (self.lm, valid_lm_values))
                check(isinstance(self.modeltype, str), 'type(modeltype) = %s must be a string ' % type(self.modeltype))
                valid_modeltype_values = [
                 'MAT', 'NBR']
                check(self.modeltype in valid_modeltype_values, 'modeltype = %s; must be in %s' % (self.modeltype, valid_modeltype_values))
                LS_means_std_valid_col_order = [
                 'bin', 'mean', 'std']
                if self.LS_means_std is not None:
                    check(pd.DataFrame.equals(self.LS_means_std, qc.validate_meanstd(self.LS_means_std)), ' LS_means_std failed quality control,                   please ensure input dataset has the correct format for LS_means_std: %s' % LS_means_std_valid_col_order)
                if self.db is not None:
                    check(isinstance(self.db, str), 'type(db) = %s must be a string ' % type(self.db))
                check(isinstance(self.iteration, int), 'type(iteration) = %s; must be of type int ' % type(self.iteration))
                check(isinstance(self.burnin, int), 'type(burnin) = %s; must be of type int ' % type(self.burnin))
                check(isinstance(self.thin, int), 'type(thin) = %s; must be of type int ' % type(self.thin))
                check(isinstance(self.runnum, int), 'type(runnum) = %s; must be of type int ' % type(self.runnum))
                check(isinstance(self.initialize, str), 'type(initialize) = %s must be a string ' % type(self.initialize))
                valid_initialize_values = [
                 'rand', 'LS', 'PR']
                check(self.initialize in valid_initialize_values, 'initialize = %s; must be in %s' % (self.initialize, valid_initialize_values))
                check(isinstance(self.start, int), 'type(start) = %s; must be of type int ' % type(self.start))
                check(self.start >= 0, 'start = %d must be a positive integer ' % self.start)
                if self.end is not None:
                    check(isinstance(self.end, int), 'type(end) = %s; must be of type int ' % type(self.end))
            check(isinstance(self.foreground, int), 'type(foreground) = %s; must be of type int ' % type(self.foreground))
            check(isinstance(self.background, int), 'type(background) = %s; must be of type int ' % type(self.background))
            check(isinstance(self.alpha, float), 'type(alpha) = %s; must be of type float ' % type(self.background))
            check(isinstance(self.pseudocounts, int), 'type(pseudocounts) = %s; must be of type int ' % type(self.pseudocounts))
            check(isinstance(self.verbose, bool), 'type(verbose) = %s; must be of type bool ' % type(self.verbose))
            if self.tm is not None:
                check(isinstance(self.tm, int), 'type(tm) = %s; must be of type int ' % type(self.tm))

    def weighted_std(self, values, weights):
        """Takes in a dataframe with seqs and cts and calculates the std"""
        average = np.average(values, weights=weights)
        variance = np.average(((values - average) ** 2), weights=weights)
        return np.sqrt(variance)

    def add_label(self, s):
        return 'ct_' + str(s)

    def MaximizeMI_memsaver(self, seq_mat, df, emat_0, wtrow, db=None, burnin=1000, iteration=30000, thin=10, runnum=0, verbose=False):
        """Performs MCMC MI maximzation in the case where lm = memsaver"""
        n_seqs = seq_mat.shape[0]

        @pymc.stochastic(observed=True, dtype=(pd.DataFrame))
        def pymcdf(value=df):
            return 0

        @pymc.stochastic(dtype=float)
        def emat(p=pymcdf, value=emat_0):
            p['val'] = numerics.eval_modelmatrix_on_mutarray(np.transpose(value), seq_mat, wtrow)
            MI = EstimateMutualInfoforMImax.alt4(p.copy())
            return n_seqs * MI

        if db:
            dbname = db + '_' + str(runnum) + '.sql'
            M = pymc.MCMC([pymcdf, emat], db='sqlite', dbname=dbname)
        else:
            M = pymc.MCMC([pymcdf, emat])
        M.use_step_method(stepper.GaugePreservingStepper, emat)
        if not verbose:
            M.sample = shutthefuckup(M.sample)
        M.sample(iteration, thin=thin)
        emat_mean = np.mean((M.trace('emat')[burnin:]), axis=0)
        return emat_mean

    def robls(self, A, b, rho):
        m, n = A.size

        def F(x=None, z=None):
            if x is None:
                return (
                 0, matrix(0.0, (n, 1)))
            else:
                y = A * x - b
                w = sqrt(rho + y ** 2)
                f = sum(w)
                Df = div(y, w).T * A
                if z is None:
                    return (
                     f, Df)
                H = A.T * spdiag(z[0] * rho * w ** (-3)) * A
                return (f, Df, H)

        return solvers.cp(F)['x']

    def test_iter(self, A, B):
        m, n1 = A.shape
        n2 = B.shape[1]
        Cshape = (m, n1 * n2)
        with warnings.catch_warnings():
            warnings.simplefilter('ignore')
            data = np.empty((m,), dtype=object)
            col = np.empty((m,), dtype=object)
            row = np.empty((m,), dtype=object)
            for i, (a, b) in enumerate(zip(A, B)):
                col1 = a.indices * n2
                col[i] = (col1[:, None] + b.indices).flatten()
                row[i] = np.full((a.nnz * b.nnz,), i)
                data[i] = np.ones(len(col[i]))

        data = np.concatenate(data)
        col = np.concatenate(col)
        row = np.concatenate(row)
        return scipy.sparse.coo_matrix((data, (row, col)), shape=Cshape)

    def convex_opt_agorithm(self, s, N0, Nsm, tm, alpha=1):
        bins = tm.shape[1]
        N0_matrix = np.matrix(N0)
        tm_matrix = np.matrix(tm)
        Nsm_matrix = np.matrix(Nsm)
        tm_matrix_squared = np.matrix(np.multiply(tm, tm))
        i, c = s.shape
        s_hessian_mat = sp.sparse.lil_matrix((i, c * c))
        s_hessian_mat = scipy.sparse.csr_matrix(self.test_iter(s, s))

        def F(x=None, z=None):
            if x is None:
                return (
                 0, matrix(0.0, (c + bins, 1)))
            else:
                gm = np.transpose(np.array(x[c:]))
                y = s * x[:c]
                w = np.add(gm, y * tm_matrix)
                term2 = np.array(N0) * np.array(np.exp(w))
                term1 = np.multiply(np.array(Nsm), np.array(w))
                f = cvxopt.matrix(-np.sum(term1 - term2) + alpha / 2 * np.sum(cvxopt.mul(x, x)))
                Df = np.zeros((1, c + bins))
                Nm = np.sum(Nsm, axis=0)
                Df_gm = Nm - sum(term2)
                Df_theta = np.transpose((Nsm - term2) * np.transpose(tm)) * s
                Df[0, :c] = Df_theta
                Df[0, c:] = Df_gm
                Df = Df - np.transpose(alpha * x)
                Df_cvx = cvxopt.matrix(-Df)
                if z is None:
                    return (
                     f, Df_cvx)
                H = np.zeros((c + bins, c + bins))
                Inner_term = N0 * tm_matrix_squared
                Inner_term2 = np.sum((np.array(Inner_term) * np.array(np.exp(w))), axis=1)
                H_thetas_temp = Inner_term2 * s_hessian_mat
                H[:c, :c] = H_thetas_temp.reshape((c, c), order='F')
                Inner_term = np.array(N0) * np.array(np.matrix(np.exp(w)))
                Inner_term2 = np.array(tm) * Inner_term
                H_gm_theta_temp = np.transpose(np.matrix(Inner_term2)) * s
                H[c:c + bins, :c] = H_gm_theta_temp
                Temp_term = np.sum(Inner_term, axis=0)
                ident = np.identity(bins)
                H_gms = np.array(Temp_term) * ident
                H[c:c + bins, c:c + bins] = H_gms
                for q in range(c + bins):
                    for k in range(q):
                        H[(k, q)] = H[(q, k)]

                penalty_term = alpha * np.identity(c + bins)
                H = cvxopt.matrix(z[0] * (H + penalty_term))
                return (
                 f, Df_cvx, H)

        return solvers.cp(F)['x']

    def reverse_parameterization(self, output, cols_for_keep, wtrow, seq_dict, bins=1, modeltype='MAT'):
        output = output[:-bins]
        df_out = np.zeros(len(wtrow))
        print(df_out.shape)
        df_out.flat[cols_for_keep] = output
        print(len(seq_dict))
        df_out2 = df_out.reshape((
         len(seq_dict), len(df_out) / len(seq_dict)),
          order='F')
        return df_out2

    def find_second_NBR_matrix_entry(self, s):
        """this is a function for use with numpy apply along axis.
            It will take in a sequence matrix and return the second nonzero entry"""
        print(np.nonzero(s)[0])
        return np.nonzero(s)[0][1]

    def convex_opt(self, df, seq_dict, inv_dict, columns, tm=None, modeltype='MAT', dicttype='dna'):
        rowsforwtcalc = 1000
        seq_mat, wtrow = numerics.dataset2mutarray((df.copy()), modeltype, rowsforwtcalc=rowsforwtcalc)
        no_reps = np.sum((np.matrix(df['ct_0']) * seq_mat), axis=0)
        cols_for_keep = [x for x in range(seq_mat.shape[1]) if x in np.nonzero(no_reps)[1]]
        if modeltype == 'NBR':
            mut_df = ProfileMut(df.loc[:rowsforwtcalc, :]).mut_df
            wtseq = ''.join(list(mut_df['wt']))
            single_seq_dict, single_inv_dict = utils.choose_dict(dicttype, modeltype='MAT')
            seqs = []
            for i, let in enumerate(wtseq[1:-1]):
                for m in range(1, 4):
                    let_for_mutation = single_seq_dict[let]
                    let_for_mutation = single_inv_dict[np.mod(let_for_mutation + m, 4)]
                    mut_seq = list(wtseq)
                    mut_seq[i + 1] = let_for_mutation
                    seqs.append(''.join(mut_seq))

            seqs_df = pd.DataFrame()
            seqs_df['seq'] = seqs
            seq_mat_mutants, wtrow2 = numerics.dataset2mutarray_withwtseq(seqs_df, modeltype, wtseq)
            bad_cols = np.apply_along_axis(self.find_second_NBR_matrix_entry, 1, seq_mat_mutants.todense())
            cols_for_keep = [cols_for_keep[x] for x in range(len(cols_for_keep)) if cols_for_keep[x] not in bad_cols]
        else:
            seq_mat = seq_mat.tocsc()
            seq_mat2 = seq_mat[:, cols_for_keep]
            columns = [x for x in columns if 'ct_0' != x]
            N0 = np.matrix(df['ct_0']).T
            Nsm = np.matrix(df[columns])
            if tm:
                tm = np.array(tm)
            else:
                tm = np.matrix([x for x in range(1, len(columns) + 1)])
        print(tm)
        output = self.convex_opt_agorithm(seq_mat2, N0, Nsm, tm)
        output_parameterized = self.reverse_parameterization(output, cols_for_keep, wtrow, seq_dict, bins=(tm.shape[1]),
          modeltype=modeltype)
        print(output_parameterized)
        print(output_parameterized.shape)
        return output_parameterized

    def Berg_von_Hippel(self, df, dicttype, foreground=1, background=0, pseudocounts=1):
        """Learn models using berg von hippel model. The foreground sequences are
             usually bin_1 and background in bin_0, this can be changed via flags."""
        seq_dict, inv_dict = utils.choose_dict(dicttype)
        columns_to_check = {
         'ct_' + str(foreground), 'ct_' + str(background)}
        if not columns_to_check.issubset(set(df.columns)):
            raise SortSeqError('Foreground or Background column does not exist!')
        foreground_counts = utils.profile_counts(df, dicttype, bin_k=foreground)
        background_counts = utils.profile_counts(df, dicttype, bin_k=background)
        binheaders = utils.get_column_headers(foreground_counts)
        foreground_counts[binheaders] = foreground_counts[binheaders] + pseudocounts
        background_counts[binheaders] = background_counts[binheaders] + pseudocounts
        ct_headers = utils.get_column_headers(foreground_counts)
        if foreground_counts[ct_headers].isin([0]).values.any():
            raise SortSeqError('There are some bases without any representation in                the foreground data, you should use pseudocounts to avoid failure                 of the learning method')
        if background_counts[ct_headers].isin([0]).values.any():
            raise SortSeqError('There are some bases without any representation in                the background data, you should use pseudocounts to avoid failure                 of the learning method')
        foreground_freqs = foreground_counts.copy()
        background_freqs = background_counts.copy()
        foreground_freqs[binheaders] = foreground_freqs[binheaders].div(foreground_freqs[binheaders].sum(axis=1),
          axis=0)
        background_freqs[binheaders] = background_freqs[binheaders].div(background_freqs[binheaders].sum(axis=1),
          axis=0)
        output_df = -np.log(foreground_freqs / background_freqs)
        rename_dict = {'ct_' + str(inv_dict[i]):'val_' + str(inv_dict[i]) for i in range(len(seq_dict))}
        output_df = output_df.rename(columns=rename_dict)
        return output_df

    def compute_etas_for_markov(self, freqs_neighbor, freqs, seq_dict, inv_dict):
        total_pairs = len(freqs.index)
        seq_dict_length = len(seq_dict)
        eta = np.zeros((total_pairs - 1, seq_dict_length ** 2))
        for q in range(seq_dict_length):
            for m in range(seq_dict_length):
                eta[(0, q * seq_dict_length + m)] = freqs_neighbor.loc[(0,
                 'ct_' + inv_dict[q] + inv_dict[m])] * np.sqrt(freqs.loc[(0,
                 'ct_' + inv_dict[q])] / freqs.loc[(1,
                 'ct_' + inv_dict[m])])

        for i in range(1, total_pairs - 2):
            for q in range(seq_dict_length):
                for m in range(seq_dict_length):
                    eta[(i, q * seq_dict_length + m)] = freqs_neighbor.loc[(i,
                     'ct_' + inv_dict[q] + inv_dict[m])] / np.sqrt(freqs.loc[(i,
                     'ct_' + inv_dict[q])] * freqs.loc[(i + 1,
                     'ct_' + inv_dict[m])])

        for q in range(seq_dict_length):
            for m in range(seq_dict_length):
                eta[(total_pairs - 2, q * seq_dict_length + m)] = freqs_neighbor.loc[(total_pairs - 2,
                 'ct_' + inv_dict[q] + inv_dict[m])] * np.sqrt(freqs.loc[(total_pairs - 1,
                 'ct_' + inv_dict[m])] / freqs.loc[(
                 total_pairs - 2,
                 'ct_' + inv_dict[q])])

        eta = np.log(eta)
        return eta

    def Markov(self, df, dicttype, foreground=1, background=0, pseudocounts=1):
        """Learn models using berg von hippel model. The foreground sequences are
             usually bin_1 and background in bin_0, this can be changed via flags."""
        seq_dict, inv_dict = utils.choose_dict(dicttype)
        seq_dict_length = len(seq_dict)
        columns_to_check = {
         'ct_' + str(foreground), 'ct_' + str(background)}
        if not columns_to_check.issubset(set(df.columns)):
            raise SortSeqError('Foreground or Background column does not exist!')
        foreground_counts = utils.profile_counts(df, dicttype, bin_k=foreground)
        background_counts = utils.profile_counts(df, dicttype, bin_k=background)
        binheaders = utils.get_column_headers(foreground_counts)
        foreground_counts_neighbor = utils.profile_counts_neighbor(df, dicttype, bin_k=foreground)
        background_counts_neighbor = utils.profile_counts_neighbor(df, dicttype, bin_k=background)
        binheaders_neighbor = utils.get_column_headers(foreground_counts_neighbor)
        foreground_counts_neighbor[binheaders_neighbor] = foreground_counts_neighbor[binheaders_neighbor] + pseudocounts
        background_counts_neighbor[binheaders_neighbor] = background_counts_neighbor[binheaders_neighbor] + pseudocounts
        foreground_counts[binheaders] = foreground_counts[binheaders] + pseudocounts * seq_dict_length
        background_counts[binheaders] = background_counts[binheaders] + pseudocounts * seq_dict_length
        ct_headers = utils.get_column_headers(foreground_counts_neighbor)
        if foreground_counts_neighbor[ct_headers].isin([0]).values.any():
            raise SortSeqError('There are some bases without any representation in                the foreground data, you should use pseudocounts to avoid failure                 of the learning method')
        if background_counts_neighbor[ct_headers].isin([0]).values.any():
            raise SortSeqError('There are some bases without any representation in                the background data, you should use pseudocounts to avoid failure                 of the learning method')
        foreground_freqs_neighbor = foreground_counts_neighbor.copy()
        background_freqs_neighbor = background_counts_neighbor.copy()
        foreground_freqs_neighbor[binheaders_neighbor] = foreground_freqs_neighbor[binheaders_neighbor].div(foreground_freqs_neighbor[binheaders_neighbor].sum(axis=1),
          axis=0)
        background_freqs_neighbor[binheaders_neighbor] = background_freqs_neighbor[binheaders_neighbor].div(background_freqs_neighbor[binheaders_neighbor].sum(axis=1),
          axis=0)
        print(foreground_freqs_neighbor)
        foreground_freqs = foreground_counts.copy()
        background_freqs = background_counts.copy()
        foreground_freqs[binheaders] = foreground_freqs[binheaders].div(foreground_freqs[binheaders].sum(axis=1),
          axis=0)
        background_freqs[binheaders] = background_freqs[binheaders].div(background_freqs[binheaders].sum(axis=1),
          axis=0)
        eta_fg = self.compute_etas_for_markov(self, foreground_freqs_neighbor, foreground_freqs, seq_dict, inv_dict)
        eta_bg = self.compute_etas_for_markov(self, background_freqs_neighbor, background_freqs, seq_dict, inv_dict)
        model = eta_fg - eta_bg
        model_df = pd.DataFrame(model)
        model_df.columns = ['val_' + inv_dict[q] + inv_dict[m] for q in range(seq_dict_length) for m in range(seq_dict_length)]
        model_df['pos'] = foreground_counts_neighbor['pos']
        return model_df

    def Compute_Least_Squares(self, raveledmat, batch, sw, alpha=0):
        """Ridge regression is the only sklearn regressor that supports sample
            weights, which will make this much faster"""
        clf = linear_model.Ridge(alpha=alpha)
        clf.fit(raveledmat, batch, sample_weight=sw)
        emat = clf.coef_
        return emat