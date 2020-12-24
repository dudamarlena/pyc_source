# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\bmccs\Desktop\streamml2\streamml2\streamline\transformation\flow\TransformationStream.py
# Compiled at: 2019-01-20 14:43:15
# Size of source mod 2**32: 12792 bytes
from __future__ import division
import pandas as pd, numpy as np
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')
import transformers.ScaleTransformer as ScaleTransformer
import transformers.BernoulliRBMTransformer as BernoulliRBMTransformer
import transformers.BinarizeTransformer as BinarizeTransformer
import transformers.KMeansTransformer as KMeansTransformer
import transformers.TSNETransformer as TSNETransformer
import transformers.NormalizeTransformer as NormalizeTransformer
import transformers.PCATransformer as PCATransformer
import transformers.BoxcoxTransformer as BoxcoxTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import HashingVectorizer

class TransformationStream:
    _vectorizer = None

    def __init__(self, df=None, corpus=False, method='tfidf', min_df=0.01, max_df=0.99, n_features=10000, verbose=True):
        self._corpus_options = [
         'tfidf', 'count', 'hash']
        if corpus == False:
            assert isinstance(df, pd.DataFrame), 'data must be a pandas DataFrame'
            self._X = df
        else:
            if not isinstance(df, list):
                raise AssertionError('data must be a list of strings when corpus is true')
            elif not method in self._corpus_options:
                raise AssertionError('method must be in corpus_options: ' + ' '.join(self._corpus_options))
            elif verbose:
                print('Constructing ' + method)
            elif method == 'tfidf':
                self._vectorizer = TfidfVectorizer(min_df=min_df, max_df=max_df).fit(df)
                self._vocabulary = self._vectorizer.vocabulary_
                tmp = self._vectorizer.fit_transform(df)
                self._X = pd.DataFrame((tmp.todense()), columns=(self._vocabulary))
            else:
                if method == 'count':
                    self._vectorizer = CountVectorizer(min_df=min_df, max_df=max_df).fit(df)
                    self._vocabulary = self._vectorizer.vocabulary_
                    tmp = self._vectorizer.fit_transform(df)
                    self._X = pd.DataFrame((tmp.todense()), columns=(self._vocabulary))
                else:
                    if method == 'hash':
                        tmp = HashingVectorizer(n_features=n_features).fit_transform(df)
                        self._X = pd.DataFrame(tmp.todense())
                    else:
                        print('Error: method specified not in list of vectorizers\n')
                        sys.exit()

    def flow(self, preproc_args=[], params=None, verbose=False):
        if not isinstance(self._X, pd.DataFrame):
            raise AssertionError('data must be a pandas DataFrame.')
        else:
            self._verbose = verbose
            if 'pca' in preproc_args:
                if 'pca__percent_variance' in params.keys():
                    assert isinstance(params['pca__percent_variance'], float), 'percent variance must be float.'
                    self._percent_variance = params['pca__percent_variance']
                else:
                    self._percent_variance = 0.9
                if 'pca__n_components' in params.keys():
                    assert isinstance(params['pca__n_components'], int), 'number of components must be int.'
                    self._pca_n_components = params['pca__n_components']
                else:
                    self._pca_n_components = len(self._X.columns.tolist())
            if 'tsne' in preproc_args:
                if 'tsne__n_components' in params.keys():
                    assert isinstance(params['tsne__n_components'], int), 'n_components must be integer.'
                    self._tsne_n_components = params['tsne__n_components']
                else:
                    self._tsne_n_components = 3
            if 'kmeans' in preproc_args:
                if 'kmeans__n_clusters' in params.keys():
                    assert isinstance(params['kmeans__n_clusters'], int), 'clusters must be integer.'
                    self._n_clusters = params['kmeans__n_clusters']
                else:
                    self._n_clusters = 2
            if 'binarize' in preproc_args:
                if 'binarize__threshold' in params.keys():
                    assert isinstance(params['binarize__threshold'], float), 'threshold must be float.'
                    self._threshold = params['binarize__threshold']
                else:
                    self._threshold = 0.0
            if 'brbm' in preproc_args:
                if 'brbm__n_components' in params.keys():
                    assert isinstance(params['brbm__n_components'], int), 'n_components must be integer.'
                    self._n_components = params['brbm__n_components']
                else:
                    if 'brbm__learning_rate' in params.keys():
                        assert isinstance(params['brbm__learning_rate'], float), 'learning_rate must be a float'
                        self._learning_rate = params['brbm__learning_rate']
        stringbuilder = ''
        for thing in preproc_args:
            stringbuilder += thing
            stringbuilder += '--> '

        if self._verbose:
            print('**************************************************')
            print('Transformation Streamline: ' + stringbuilder[:-4])
            print('**************************************************')

        def runScale(X, verbose=False):
            if verbose:
                print('Executing Scaling')
            return ScaleTransformer().transform(X)

        def runNormalize(X, verbose=False):
            if verbose:
                print('Executing Normalize')
            return NormalizeTransformer().transform(X)

        def runBinarize(X, verbose=False):
            if verbose:
                print('Executing Binarization')
            return BinarizeTransformer(self._threshold).transform(X)

        def runBoxcox(X, verbose=False):
            if verbose:
                print('Executing Boxcox')
            bct = BoxcoxTransformer()
            X_boxcoxed = bct.transform(X)
            self._lambdas = bct._lambdas
            return X_boxcoxed

        def runPCA(X, verbose=False):
            if verbose:
                print('Executing PCA')
            return PCATransformer(self._percent_variance, self._pca_n_components, self._verbose).transform(X)

        def runKmeans(X, verbose=False):
            if verbose:
                print('Executing Kmeans with ' + str(self._n_clusters) + ' clusters\n')
            return KMeansTransformer(self._n_clusters).transform(X)

        def runBRBM(X, verbose=False):
            if verbose:
                print('Executing Bernoulli Restricted Boltzman Machine\n')
            return BernoulliRBMTransformer().transform(X)

        def runTSNE(X, verbose=False):
            if verbose:
                print('Executing TNSE with ' + str(self._tsne_n_components) + ' components\n')
            return TSNETransformer(self._tsne_n_components).transform(X)

        def runItemset(X, verbose=False):
            if verbose:
                print('Itemset mining unimplemented\n')
            return X

        options = {'scale':runScale, 
         'normalize':runNormalize, 
         'binarize':runBinarize, 
         'itemset':runItemset, 
         'boxcox':runBoxcox, 
         'pca':runPCA, 
         'kmeans':runKmeans, 
         'brbm':runBRBM, 
         'tsne':runTSNE}
        self._df_transformed = self._X
        for key in preproc_args:
            self._df_transformed = options[key]((self._df_transformed), verbose=(self._verbose))

        return self._df_transformed