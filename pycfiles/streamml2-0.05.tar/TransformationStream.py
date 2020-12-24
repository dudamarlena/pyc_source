# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bmc/Desktop/streamml/streamline/transformation/flow/TransformationStream.py
# Compiled at: 2018-06-22 09:39:20
from __future__ import division
import pandas as pd, numpy as np
from sklearn import preprocessing
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from scipy import stats
from sklearn.neural_network import BernoulliRBM
import matplotlib.pyplot as plt

class TransformationStream:
    """
    Constructor:
    1. Default
        Paramters: df : pd.DataFrame, dataframe must be accepted to use this class
    """

    def __init__(self, df=None):
        assert isinstance(df, pd.DataFrame), 'data must be a pandas DataFrame'
        self._df = df

    def flow(self, preproc_args=[], params=None, verbose=False):
        assert isinstance(self._df, pd.DataFrame), 'data must be a pandas DataFrame.'
        self._verbose = verbose
        if 'pca' in preproc_args:
            if 'pca__percent_variance' in params.keys():
                assert isinstance(params['pca__percent_variance'], float), 'percent variance must be float.'
                self._percent_variance = params['pca__percent_variance']
                print 'custom: pca__percent_variance=' + str(self._percent_variance)
            else:
                self._percent_variance = 0.9
                print 'default: pca__percent_variance=' + str(self._percent_variance)
        if 'kmeans' in preproc_args:
            if 'kmeans__n_clusters' in params.keys():
                assert isinstance(params['kmeans__n_clusters'], int), 'clusters must be integer.'
                self._n_clusters = params['kmeans__n_clusters']
                print 'custom: kmeans__n_clusters=' + str(self._n_clusters)
            else:
                self._n_clusters = 2
                print 'default: kmeans__n_clusters=' + str(self._n_clusters)
        if 'binarize' in preproc_args:
            if 'binarize__threshold' in params.keys():
                assert isinstance(params['binarize__threshold'], float), 'threshold must be float.'
                self._threshold = params['binarize__threshold']
                print 'default: binarize__threshold=' + str(self._threshold)
            else:
                self._threshold = 0.0
                print 'default: binarize__threshold=' + str(self._threshold)
        if 'brbm' in preproc_args:
            if 'brbm__n_components' in params.keys():
                assert isinstance(params['brbm__n_components'], int), 'n_components must be integer.'
                self._n_components = params['brbm__n_components']
            elif 'brbm__learning_rate' in params.keys():
                assert isinstance(params['brbm__learning_rate'], float), 'learning_rate must be a float'
                self._learning_rate = params['brbm__learning_rate']
        stringbuilder = ''
        for thing in preproc_args:
            stringbuilder += thing
            stringbuilder += '--> '

        if verbose:
            print '**************************************************'
            print 'Transformation Streamline: ' + stringbuilder[:-4]
            print '**************************************************'

        def runScale(X, verbose=False):
            if verbose:
                print 'Executing Scaling'
            X_scaled = preprocessing.scale(X)
            return pd.DataFrame(X_scaled)

        def runNormalize(X, verbose=False):
            if verbose:
                print 'Executing Normalize'
            X_normalized = preprocessing.normalize(X, norm='l2')
            return pd.DataFrame(X_normalized)

        def runBinarize(X, verbose=False):
            if verbose:
                print 'Executing Binarization'
            X_binarized = preprocessing.Binarizer(threshold=self._threshold).fit(X).transform(X)
            return pd.DataFrame(X_binarized)

        def runBoxcox(X, verbose=False):
            if verbose:
                print 'Executing Boxcox'
            X_boxcoxed = X
            lambdas = []
            for col in X:
                X_boxcoxed[col], l = stats.boxcox(X_boxcoxed[col])
                lambdas.append(l)

            self._lambdas = lambdas
            if verbose:
                print 'Optimized BoxCox-Lambdas For Each Column: '
                print self._lambdas
            return X_boxcoxed

        def runPCA(X, verbose=False):
            if verbose:
                print 'Executing PCA'
            pca = PCA()
            pca_output = pca.fit(X)
            components_nums = [ i for i in range(len(pca_output.components_)) ]
            self._percentVarianceExplained = pca_output.explained_variance_ / sum(pca_output.explained_variance_)
            tot = 0.0
            idx = 0
            for i in range(len(self._percentVarianceExplained)):
                tot += self._percentVarianceExplained[i]
                if tot >= self._percent_variance:
                    idx = i + 1
                    break

            if verbose:
                print 'Percent of Variance Explained By Components:\n'
                print str(self._percentVarianceExplained), '\n'
                print str(self._percent_variance * 100), '% variance is explained in the first ', str(idx), ' components\n'
                pca_df = pd.DataFrame({'explained_variance': pca_output.explained_variance_}, index=components_nums)
                pca_df.plot(title='Components vs. Variance')
                plt.show()
            pca_output = pca.fit_transform(X)
            pca_df = pd.DataFrame(pca_output, columns=[ 'PC_' + str(i) for i in components_nums ])
            return pca_df.iloc[:, :idx]

        def runKmeans(X, verbose=False):
            if verbose:
                print 'Executing Kmeans with ' + str(self._n_clusters) + ' clusters\n'
            kmeans = KMeans(n_clusters=self._n_clusters).fit(X)
            X['cluster'] = pd.DataFrame(kmeans.labels_, columns=['cluster'], dtype='category')
            return X

        def runBRBM(X, verbose=False):
            if verbose:
                print 'Executing Bernoulli Restricted Boltzman Machine\n'
            brbm = BernoulliRBM(n_components=256, learning_rate=0.1, batch_size=10, n_iter=10, verbose=0, random_state=None)
            Xnew = pd.DataFrame(brbm.fit_transform(X))
            return Xnew

        def runItemset(X, verbose=False):
            if verbose:
                print 'Itemset mining unimplemented\n'
            return X

        options = {'scale': runScale, 'normalize': runNormalize, 
           'binarize': runBinarize, 
           'itemset': runItemset, 
           'boxcox': runBoxcox, 
           'pca': runPCA, 
           'kmeans': runKmeans, 
           'brbm': runBRBM}
        self._df_transformed = self._df
        for key in preproc_args:
            self._df_transformed = options[key](self._df_transformed, verbose=self._verbose)

        return self._df_transformed