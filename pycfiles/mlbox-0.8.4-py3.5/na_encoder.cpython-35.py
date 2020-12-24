# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mlbox/encoding/na_encoder.py
# Compiled at: 2020-04-13 16:34:29
# Size of source mod 2**32: 8252 bytes
import pandas as pd, warnings
from sklearn.impute import SimpleImputer

class NA_encoder:
    __doc__ = 'Encodes missing values for both numerical and categorical features.\n\n    Several strategies are possible in each case.\n\n    Parameters\n    ----------\n    numerical_strategy : str or float or int. default = "mean"\n        The strategy to encode NA for numerical features.\n        Available strategies = "mean", "median",\n        "most_frequent" or a float/int value\n\n    categorical_strategy : str, default = \'<NULL>\'\n        The strategy to encode NA for categorical features.\n        Available strategies = a string or "most_frequent"\n\n    '

    def __init__(self, numerical_strategy='mean', categorical_strategy='<NULL>'):
        """Init a NA_encoder.

        User can choose numerical strategy and categorical strategy.

        Parameters
        ----------
        numerical_strategy : str or float or int. default = "mean"
            The strategy to encode NA for numerical features.

        categorical_strategy : str, default = '<NULL>'
            The strategy to encode NA for categorical features.

        """
        self.numerical_strategy = numerical_strategy
        self.categorical_strategy = categorical_strategy
        self._NA_encoder__Lcat = []
        self._NA_encoder__Lnum = []
        self._NA_encoder__imp = None
        self._NA_encoder__mode = dict()
        self._NA_encoder__fitOK = False

    def get_params(self, deep=True):
        """Get parameters of a NA_encoder object."""
        return {'numerical_strategy': self.numerical_strategy, 
         'categorical_strategy': self.categorical_strategy}

    def set_params(self, **params):
        """Set parameters for a NA_encoder object.

        Set numerical strategy and categorical strategy.

        Parameters
        ----------
        numerical_strategy : str or float or int. default = "mean"
            The strategy to encode NA for numerical features.

        categorical_strategy : str, default = '<NULL>'
            The strategy to encode NA for categorical features.

        """
        self._NA_encoder__fitOK = False
        for k, v in params.items():
            if k not in self.get_params():
                warnings.warn('Invalid parameter(s) for encoder NA_encoder. Parameter(s) IGNORED. Check the list of available parameters with `encoder.get_params().keys()`')
            else:
                setattr(self, k, v)

    def fit(self, df_train, y_train=None):
        """Fits NA Encoder.

        Parameters
        ----------
        df_train : pandas dataframe of shape = (n_train, n_features)
            The train dataset with numerical and categorical features.

        y_train : pandas series of shape = (n_train, ), default = None
            The target for classification or regression tasks.

        Returns
        -------
        object
            self

        """
        self._NA_encoder__Lcat = df_train.dtypes[(df_train.dtypes == 'object')].index
        self._NA_encoder__Lnum = df_train.dtypes[(df_train.dtypes != 'object')].index
        if self.numerical_strategy in ('mean', 'median', 'most_frequent'):
            self._NA_encoder__imp = SimpleImputer(strategy=self.numerical_strategy)
            if len(self._NA_encoder__Lnum) != 0:
                self._NA_encoder__imp.fit(df_train[self._NA_encoder__Lnum])
        else:
            if (type(self.numerical_strategy) == int) | (type(self.numerical_strategy) == float):
                pass
            else:
                raise ValueError('Numerical strategy for NA encoding is not valid')
            if type(self.categorical_strategy) == str:
                if self.categorical_strategy == 'most_frequent':
                    na_count = df_train[self._NA_encoder__Lcat].isnull().sum()
                    for col in na_count[(na_count > 0)].index:
                        try:
                            self._NA_encoder__mode[col] = df_train[col].mode()[0]
                        except:
                            self._NA_encoder__mode[col] = '<NULL>'

            else:
                raise ValueError('Categorical strategy for NA encoding is not valid')
        self._NA_encoder__fitOK = True
        return self

    def fit_transform(self, df_train, y_train=None):
        """Fits NA Encoder and transforms the dataset.

        Parameters
        ----------
        df_train : pandas.Dataframe of shape = (n_train, n_features)
            The train dataset with numerical and categorical features.

        y_train : pandas.Series of shape = (n_train, ), default = None
            The target for classification or regression tasks.

        Returns
        -------
        pandas.Dataframe of shape = (n_train, n_features)
            The train dataset with no missing values.

        """
        self.fit(df_train, y_train)
        return self.transform(df_train)

    def transform--- This code section failed: ---

 L. 182         0  LOAD_FAST                'self'
                3  LOAD_ATTR                _NA_encoder__fitOK
                6  POP_JUMP_IF_FALSE   640  'to 640'

 L. 184         9  LOAD_GLOBAL              len
               12  LOAD_FAST                'self'
               15  LOAD_ATTR                _NA_encoder__Lnum
               18  CALL_FUNCTION_1       1  '1 positional, 0 named'
               21  LOAD_CONST               0
               24  COMPARE_OP               ==
               27  POP_JUMP_IF_FALSE    94  'to 94'

 L. 186        30  LOAD_FAST                'self'
               33  LOAD_ATTR                categorical_strategy
               36  LOAD_STR                 'most_frequent'
               39  COMPARE_OP               !=
               42  POP_JUMP_IF_FALSE    68  'to 68'

 L. 187        45  LOAD_FAST                'df'
               48  LOAD_FAST                'self'
               51  LOAD_ATTR                _NA_encoder__Lcat
               54  BINARY_SUBSCR    
               55  LOAD_ATTR                fillna
               58  LOAD_FAST                'self'
               61  LOAD_ATTR                categorical_strategy
               64  CALL_FUNCTION_1       1  '1 positional, 0 named'
               67  RETURN_END_IF    
             68_0  COME_FROM            42  '42'

 L. 190        68  LOAD_FAST                'df'
               71  LOAD_FAST                'self'
               74  LOAD_ATTR                _NA_encoder__Lcat
               77  BINARY_SUBSCR    
               78  LOAD_ATTR                fillna
               81  LOAD_FAST                'self'
               84  LOAD_ATTR                _NA_encoder__mode
               87  CALL_FUNCTION_1       1  '1 positional, 0 named'
               90  RETURN_VALUE     
               91  JUMP_ABSOLUTE       652  'to 652'
               94  ELSE                     '637'

 L. 194        94  LOAD_FAST                'self'
               97  LOAD_ATTR                numerical_strategy

 L. 196       100  LOAD_CONST               ('mean', 'median', 'most_frequent')
              103  COMPARE_OP               in
              106  POP_JUMP_IF_FALSE   395  'to 395'

 L. 198       109  LOAD_GLOBAL              len
              112  LOAD_FAST                'self'
              115  LOAD_ATTR                _NA_encoder__Lcat
              118  CALL_FUNCTION_1       1  '1 positional, 0 named'
              121  LOAD_CONST               0
              124  COMPARE_OP               !=
              127  POP_JUMP_IF_FALSE   342  'to 342'

 L. 200       130  LOAD_FAST                'self'
              133  LOAD_ATTR                categorical_strategy
              136  LOAD_STR                 'most_frequent'
              139  COMPARE_OP               !=
              142  POP_JUMP_IF_FALSE   242  'to 242'

 L. 202       145  LOAD_GLOBAL              pd
              148  LOAD_ATTR                concat

 L. 203       151  LOAD_GLOBAL              pd
              154  LOAD_ATTR                DataFrame
              157  LOAD_FAST                'self'
              160  LOAD_ATTR                _NA_encoder__imp
              163  LOAD_ATTR                transform
              166  LOAD_FAST                'df'
              169  LOAD_FAST                'self'
              172  LOAD_ATTR                _NA_encoder__Lnum
              175  BINARY_SUBSCR    
              176  CALL_FUNCTION_1       1  '1 positional, 0 named'
              179  LOAD_STR                 'columns'

 L. 204       182  LOAD_FAST                'self'
              185  LOAD_ATTR                _NA_encoder__Lnum
              188  LOAD_STR                 'index'

 L. 205       191  LOAD_FAST                'df'
              194  LOAD_ATTR                index
              197  CALL_FUNCTION_513   513  '1 positional, 2 named'

 L. 206       200  LOAD_FAST                'df'
              203  LOAD_FAST                'self'
              206  LOAD_ATTR                _NA_encoder__Lcat
              209  BINARY_SUBSCR    
              210  LOAD_ATTR                fillna
              213  LOAD_FAST                'self'
              216  LOAD_ATTR                categorical_strategy
              219  CALL_FUNCTION_1       1  '1 positional, 0 named'
              222  BUILD_TUPLE_2         2 
              225  LOAD_STR                 'axis'

 L. 208       228  LOAD_CONST               1
              231  CALL_FUNCTION_257   257  '1 positional, 1 named'
              234  LOAD_FAST                'df'
              237  LOAD_ATTR                columns
              240  BINARY_SUBSCR    
              241  RETURN_END_IF    
            242_0  COME_FROM           142  '142'

 L. 212       242  LOAD_GLOBAL              pd
              245  LOAD_ATTR                concat

 L. 213       248  LOAD_GLOBAL              pd
              251  LOAD_ATTR                DataFrame
              254  LOAD_FAST                'self'
              257  LOAD_ATTR                _NA_encoder__imp
              260  LOAD_ATTR                transform
              263  LOAD_FAST                'df'
              266  LOAD_FAST                'self'
              269  LOAD_ATTR                _NA_encoder__Lnum
              272  BINARY_SUBSCR    
              273  CALL_FUNCTION_1       1  '1 positional, 0 named'
              276  LOAD_STR                 'columns'

 L. 214       279  LOAD_FAST                'self'
              282  LOAD_ATTR                _NA_encoder__Lnum
              285  LOAD_STR                 'index'

 L. 215       288  LOAD_FAST                'df'
              291  LOAD_ATTR                index
              294  CALL_FUNCTION_513   513  '1 positional, 2 named'

 L. 216       297  LOAD_FAST                'df'
              300  LOAD_FAST                'self'
              303  LOAD_ATTR                _NA_encoder__Lcat
              306  BINARY_SUBSCR    
              307  LOAD_ATTR                fillna
              310  LOAD_FAST                'self'
              313  LOAD_ATTR                _NA_encoder__mode
              316  CALL_FUNCTION_1       1  '1 positional, 0 named'
              319  BUILD_TUPLE_2         2 
              322  LOAD_STR                 'axis'

 L. 218       325  LOAD_CONST               1
              328  CALL_FUNCTION_257   257  '1 positional, 1 named'
              331  LOAD_FAST                'df'
              334  LOAD_ATTR                columns
              337  BINARY_SUBSCR    
              338  RETURN_VALUE     
              339  JUMP_ABSOLUTE       637  'to 637'
              342  ELSE                     '392'

 L. 222       342  LOAD_GLOBAL              pd
              345  LOAD_ATTR                DataFrame

 L. 223       348  LOAD_FAST                'self'
              351  LOAD_ATTR                _NA_encoder__imp
              354  LOAD_ATTR                transform
              357  LOAD_FAST                'df'
              360  LOAD_FAST                'self'
              363  LOAD_ATTR                _NA_encoder__Lnum
              366  BINARY_SUBSCR    
              367  CALL_FUNCTION_1       1  '1 positional, 0 named'
              370  LOAD_STR                 'columns'

 L. 224       373  LOAD_FAST                'self'
              376  LOAD_ATTR                _NA_encoder__Lnum
              379  LOAD_STR                 'index'

 L. 225       382  LOAD_FAST                'df'
              385  LOAD_ATTR                index
              388  CALL_FUNCTION_513   513  '1 positional, 2 named'
              391  RETURN_VALUE     
              392  JUMP_ABSOLUTE       652  'to 652'
              395  ELSE                     '637'

 L. 228       395  LOAD_GLOBAL              type
              398  LOAD_FAST                'self'
              401  LOAD_ATTR                numerical_strategy
              404  CALL_FUNCTION_1       1  '1 positional, 0 named'
              407  LOAD_GLOBAL              int
              410  COMPARE_OP               ==
              413  LOAD_GLOBAL              type
              416  LOAD_FAST                'self'
              419  LOAD_ATTR                numerical_strategy
              422  CALL_FUNCTION_1       1  '1 positional, 0 named'
              425  LOAD_GLOBAL              float
              428  COMPARE_OP               ==
              431  BINARY_OR        
              432  POP_JUMP_IF_FALSE   652  'to 652'

 L. 230       435  LOAD_GLOBAL              len
              438  LOAD_FAST                'self'
              441  LOAD_ATTR                _NA_encoder__Lcat
              444  CALL_FUNCTION_1       1  '1 positional, 0 named'
              447  LOAD_CONST               0
              450  COMPARE_OP               !=
              453  POP_JUMP_IF_FALSE   614  'to 614'

 L. 232       456  LOAD_FAST                'self'
              459  LOAD_ATTR                categorical_strategy
              462  LOAD_STR                 'most_frequent'
              465  COMPARE_OP               !=
              468  POP_JUMP_IF_FALSE   541  'to 541'

 L. 234       471  LOAD_GLOBAL              pd
              474  LOAD_ATTR                concat

 L. 235       477  LOAD_FAST                'df'
              480  LOAD_FAST                'self'
              483  LOAD_ATTR                _NA_encoder__Lnum
              486  BINARY_SUBSCR    
              487  LOAD_ATTR                fillna
              490  LOAD_FAST                'self'
              493  LOAD_ATTR                numerical_strategy
              496  CALL_FUNCTION_1       1  '1 positional, 0 named'

 L. 236       499  LOAD_FAST                'df'
              502  LOAD_FAST                'self'
              505  LOAD_ATTR                _NA_encoder__Lcat
              508  BINARY_SUBSCR    
              509  LOAD_ATTR                fillna
              512  LOAD_FAST                'self'
              515  LOAD_ATTR                categorical_strategy
              518  CALL_FUNCTION_1       1  '1 positional, 0 named'
              521  BUILD_TUPLE_2         2 
              524  LOAD_STR                 'axis'

 L. 238       527  LOAD_CONST               1
              530  CALL_FUNCTION_257   257  '1 positional, 1 named'
              533  LOAD_FAST                'df'
              536  LOAD_ATTR                columns
              539  BINARY_SUBSCR    
              540  RETURN_END_IF    
            541_0  COME_FROM           468  '468'

 L. 242       541  LOAD_GLOBAL              pd
              544  LOAD_ATTR                concat

 L. 243       547  LOAD_FAST                'df'
              550  LOAD_FAST                'self'
              553  LOAD_ATTR                _NA_encoder__Lnum
              556  BINARY_SUBSCR    
              557  LOAD_ATTR                fillna
              560  LOAD_FAST                'self'
              563  LOAD_ATTR                numerical_strategy
              566  CALL_FUNCTION_1       1  '1 positional, 0 named'

 L. 244       569  LOAD_FAST                'df'
              572  LOAD_FAST                'self'
              575  LOAD_ATTR                _NA_encoder__Lcat
              578  BINARY_SUBSCR    
              579  LOAD_ATTR                fillna
              582  LOAD_FAST                'self'
              585  LOAD_ATTR                _NA_encoder__mode
              588  CALL_FUNCTION_1       1  '1 positional, 0 named'
              591  BUILD_TUPLE_2         2 
              594  LOAD_STR                 'axis'

 L. 246       597  LOAD_CONST               1
              600  CALL_FUNCTION_257   257  '1 positional, 1 named'
              603  LOAD_FAST                'df'
              606  LOAD_ATTR                columns
              609  BINARY_SUBSCR    
              610  RETURN_VALUE     
              611  JUMP_ABSOLUTE       652  'to 652'
              614  ELSE                     '637'

 L. 249       614  LOAD_FAST                'df'
              617  LOAD_FAST                'self'
              620  LOAD_ATTR                _NA_encoder__Lnum
              623  BINARY_SUBSCR    
              624  LOAD_ATTR                fillna
              627  LOAD_FAST                'self'
              630  LOAD_ATTR                numerical_strategy
              633  CALL_FUNCTION_1       1  '1 positional, 0 named'
              636  RETURN_END_IF    
            637_0  COME_FROM           432  '432'
              637  JUMP_FORWARD        652  'to 652'
              640  ELSE                     '652'

 L. 253       640  LOAD_GLOBAL              ValueError
              643  LOAD_STR                 'Call fit or fit_transform function before'
              646  CALL_FUNCTION_1       1  '1 positional, 0 named'
              649  RAISE_VARARGS_1       1  'exception'
            652_0  COME_FROM           637  '637'

Parse error at or near `JUMP_FORWARD' instruction at offset 637