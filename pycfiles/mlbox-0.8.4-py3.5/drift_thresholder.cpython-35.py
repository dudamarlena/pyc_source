# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mlbox/preprocessing/drift_thresholder.py
# Compiled at: 2020-04-13 16:34:29
# Size of source mod 2**32: 5964 bytes
import os, time
from sklearn.pipeline import Pipeline
from .drift import DriftThreshold
from ..encoding.na_encoder import NA_encoder
from ..encoding.categorical_encoder import Categorical_encoder

class Drift_thresholder:
    __doc__ = 'Automatically drops ids and drifting variables between train and test datasets.\n\n    Drops on train and test datasets. The list of drift coefficients is available and\n    saved as "drifts.txt". To get familiar with drift:\n    https://github.com/AxeldeRomblay/MLBox/blob/master/docs/webinars/features.pdf\n\n    Parameters\n    ----------\n    threshold : float, defaut = 0.6\n        Drift threshold under which features are kept. Must be between 0. and 1.\n        The lower the more you keep non-drifting/stable variables: a feature with\n        a drift measure of 0. is very stable and a one with 1. is highly unstable.\n\n    inplace : bool, default = False\n        If True, train and test datasets are transformed. Returns self.\n        Otherwise, train and test datasets are not transformed. Returns a new dictionnary with\n        cleaned datasets.\n\n    verbose : bool, default = True\n        Verbose mode\n\n    to_path : str, default = "save"\n        Name of the folder where the list of drift coefficients is saved.\n    '

    def __init__(self, threshold=0.6, inplace=False, verbose=True, to_path='save'):
        self.threshold = threshold
        self.inplace = inplace
        self.verbose = verbose
        self.to_path = to_path
        self._Drift_thresholder__Ddrifts = {}
        self._Drift_thresholder__fitOK = False

    def fit_transform(self, df):
        """Fits and transforms train and test datasets

        Automatically drops ids and drifting variables between train and test datasets.
        The list of drift coefficients is available and saved as "drifts.txt"

        Parameters
        ----------
        df : dict, defaut = None
            Dictionnary containing :

            - 'train' : pandas dataframe for train dataset
            - 'test' : pandas dataframe for test dataset
            - 'target' : pandas serie for the target on train set

        Returns
        -------
        dict
            Dictionnary containing :

            - 'train' : transformed pandas dataframe for train dataset
            - 'test' : transformed pandas dataframe for test dataset
            - 'target' : pandas serie for the target on train set
        """
        if df['test'].shape[0] == 0:
            if self.verbose:
                print('')
                print('You have no test dataset...')
            return df
        start_time = time.time()
        ds = DriftThreshold(self.threshold)
        na = NA_encoder(numerical_strategy=0)
        ca = Categorical_encoder()
        pp = Pipeline([('na', na), ('ca', ca)])
        pp.fit(df['train'], None)
        if self.verbose:
            print('')
            print('computing drifts ...')
        ds.fit(pp.transform(df['train']), pp.transform(df['test']))
        if self.verbose:
            print('CPU time: %s seconds' % (time.time() - start_time))
            print('')
        self._Drift_thresholder__fitOK = True
        self._Drift_thresholder__Ddrifts = ds.drifts()
        drifts_top = sorted(ds.drifts().items(), key=lambda x: x[1], reverse=True)[:10]
        if self.verbose:
            print('> Top 10 drifts')
            print('')
            for d in range(len(drifts_top)):
                print(drifts_top[d])

        if self.verbose:
            print('')
            print('> Deleted variables : ' + str(ds.get_support(complement=True)))
        if self.to_path is not None:
            try:
                os.mkdir(self.to_path)
            except OSError:
                pass

            file = open(self.to_path + '/drifts.txt', 'w')
            file.write('\n')
            file.write('*******************************************  Drifts coefficients *******************************************\n')
            file.write('\n')
            for var, d in sorted(ds.drifts().items(), key=lambda x: x[1], reverse=True):
                file.write(str(var) + ' = ' + str(d) + '\n')

            file.close()
            if self.verbose:
                print('> Drift coefficients dumped into directory : ' + self.to_path)
            if self.inplace:
                df['train'] = ds.transform(df['train'])
                df['test'] = ds.transform(df['test'])
        else:
            return {'train': ds.transform(df['train']), 
             'test': ds.transform(df['test']), 
             'target': df['target']}

    def drifts(self):
        """Returns the univariate drifts for all variables.

        Returns
        -------
        dict
            Dictionnary containing the drifts for each feature
        """
        if self._Drift_thresholder__fitOK:
            return self._Drift_thresholder__Ddrifts
        raise ValueError('Call the fit_transform function before !')