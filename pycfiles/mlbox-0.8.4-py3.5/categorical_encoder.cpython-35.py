# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mlbox/encoding/categorical_encoder.py
# Compiled at: 2020-04-13 16:34:29
# Size of source mod 2**32: 20977 bytes
import numpy as np, pandas as pd, warnings, os
from tensorflow.keras.layers import Dense, Reshape, Dropout, Embedding, concatenate, Input
from tensorflow.keras.models import Model

class Categorical_encoder:
    __doc__ = 'Encodes categorical features.\n\n    Several strategies are possible (supervised or not). Works for both\n    classification and regression tasks.\n\n    Parameters\n    ----------\n    strategy : str, default = "label_encoding"\n        The strategy to encode categorical features.\n        Available strategies = {"label_encoding", "dummification",\n        "random_projection", entity_embedding"}\n    verbose : bool, default = False\n        Verbose mode. Useful for entity embedding strategy.\n\n    '

    def __init__(self, strategy='label_encoding', verbose=False):
        """Init method for class Categorical_encoder()."""
        self.strategy = strategy
        self.verbose = verbose
        self._Categorical_encoder__Lcat = []
        self._Categorical_encoder__Lnum = []
        self._Categorical_encoder__Enc = dict()
        self._Categorical_encoder__K = dict()
        self._Categorical_encoder__weights = None
        self._Categorical_encoder__fitOK = False

    def get_params(self, deep=True):
        """Get param that can be defined by the user.

        Get strategy parameters and verbose parameters

        Parameters
        ----------
        strategy : str, default = "label_encoding"
            The strategy to encode categorical features.
            Available strategies = {"label_encoding", "dummification",
            "random_projection", entity_embedding"}
        verbose : bool, default = False
            Verbose mode. Useful for entity embedding strategy.

        Returns
        -------
        dict : dictionary
            Dictionary that contains strategy and verbose parameters.

        """
        dict = {'strategy': self.strategy, 
         'verbose': self.verbose}
        return dict

    def set_params(self, **params):
        """Set param method for Categorical encoder.

        Set strategy parameters and verbose parameters

        Parameters
        ----------
        strategy : str, default = "label_encoding"
            The strategy to encode categorical features.
            Available strategies = {"label_encoding", "dummification",
            "random_projection", entity_embedding"}
        verbose : bool, default = False
            Verbose mode. Useful for entity embedding strategy.

        """
        self._Categorical_encoder__fitOK = False
        for k, v in params.items():
            if k not in self.get_params():
                warnings.warn('Invalid parameter(s) for encoder Categorical_encoder. Parameter(s) IGNORED. Check the list of available parameters with `encoder.get_params().keys()`')
            else:
                setattr(self, k, v)

    def fit(self, df_train, y_train):
        """Fit Categorical Encoder.

        Encode categorical variable of a dataframe
        following strategy parameters.

        Parameters
        ----------
        df_train : pandas.Dataframe of shape = (n_train, n_features).
            The training dataset with numerical and categorical features.
            NA values are allowed.
        y_train : pandas.Series of shape = (n_train, ).
            The target for classification or regression tasks.

        Returns
        -------
        object
            self

        """
        self._Categorical_encoder__Lcat = df_train.dtypes[(df_train.dtypes == 'object')].index
        self._Categorical_encoder__Lnum = df_train.dtypes[(df_train.dtypes != 'object')].index
        if len(self._Categorical_encoder__Lcat) == 0:
            self._Categorical_encoder__fitOK = True
        else:
            if self.strategy == 'label_encoding':
                for col in self._Categorical_encoder__Lcat:
                    d = dict()
                    levels = list(df_train[col].unique())
                    nan = False
                    if np.NaN in levels:
                        nan = True
                        levels.remove(np.NaN)
                    for enc, level in enumerate([np.NaN] * nan + sorted(levels)):
                        d[level] = enc

                    self._Categorical_encoder__Enc[col] = d

                self._Categorical_encoder__fitOK = True
            else:
                if self.strategy == 'dummification':
                    for col in self._Categorical_encoder__Lcat:
                        self._Categorical_encoder__Enc[col] = list(df_train[col].dropna().unique())

                    self._Categorical_encoder__fitOK = True
                else:
                    if self.strategy == 'entity_embedding':
                        A = 10
                        B = 5
                        self._Categorical_encoder__K = {}
                        for col in self._Categorical_encoder__Lcat:
                            exp_ = np.exp(-df_train[col].nunique() * 0.05)
                            self._Categorical_encoder__K[col] = np.int(5 * (1 - exp_) + 1)

                        sum_ = sum([1.0 * np.log(k) for k in self._Categorical_encoder__K.values()])
                        n_layer1 = min(1000, int(A * len(self._Categorical_encoder__K) ** 0.5 * sum_ + 1))
                        n_layer2 = int(n_layer1 / B) + 2
                        dropout1 = 0.1
                        dropout2 = 0.1
                        epochs = 20
                        batch_size = 128
                        embeddings = []
                        inputs = []
                        for col in self._Categorical_encoder__Lcat:
                            d = dict()
                            levels = list(df_train[col].unique())
                            nan = False
                            if np.NaN in levels:
                                nan = True
                                levels.remove(np.NaN)
                            for enc, level in enumerate([np.NaN] * nan + sorted(levels)):
                                d[level] = enc

                            self._Categorical_encoder__Enc[col] = d
                            var = Input(shape=(1, ))
                            inputs.append(var)
                            emb = Embedding(input_dim=len(self._Categorical_encoder__Enc[col]), output_dim=self._Categorical_encoder__K[col], input_length=1)(var)
                            emb = Reshape(target_shape=(self._Categorical_encoder__K[col],))(emb)
                            embeddings.append(emb)

                        if len(self._Categorical_encoder__Lcat) > 1:
                            emb_layer = concatenate(embeddings)
                        else:
                            emb_layer = embeddings[0]
                        lay1 = Dense(n_layer1, kernel_initializer='uniform', activation='relu')(emb_layer)
                        lay1 = Dropout(dropout1)(lay1)
                        lay2 = Dense(n_layer2, kernel_initializer='uniform', activation='relu')(lay1)
                        lay2 = Dropout(dropout2)(lay2)
                        if (y_train.dtype == object) | (y_train.dtype == 'int'):
                            if y_train.nunique() == 2:
                                outputs = Dense(1, kernel_initializer='normal', activation='sigmoid')(lay2)
                                model = Model(inputs=inputs, outputs=outputs)
                                model.compile(loss='binary_crossentropy', optimizer='adam')
                                model.fit([df_train[col].apply(lambda x: self._Categorical_encoder__Enc[col][x]).values for col in self._Categorical_encoder__Lcat], pd.get_dummies(y_train, drop_first=True).astype(int).values, epochs=epochs, batch_size=batch_size, verbose=int(self.verbose))
                            else:
                                outputs = Dense(y_train.nunique(), kernel_initializer='normal', activation='softmax')(lay2)
                                model = Model(inputs=inputs, outputs=outputs)
                                model.compile(loss='binary_crossentropy', optimizer='adam')
                                model.fit([df_train[col].apply(lambda x: self._Categorical_encoder__Enc[col][x]).values for col in self._Categorical_encoder__Lcat], pd.get_dummies(y_train, drop_first=False).astype(int).values, epochs=epochs, batch_size=batch_size, verbose=int(self.verbose))
                        else:
                            outputs = Dense(1, kernel_initializer='normal')(lay2)
                            model = Model(inputs=inputs, outputs=outputs)
                            model.compile(loss='mean_squared_error', optimizer='adam')
                            model.fit([df_train[col].apply(lambda x: self._Categorical_encoder__Enc[col][x]).values for col in self._Categorical_encoder__Lcat], y_train.values, epochs=epochs, batch_size=batch_size, verbose=int(self.verbose))
                        self._Categorical_encoder__weights = model.get_weights()
                        self._Categorical_encoder__fitOK = True
                    else:
                        if self.strategy == 'random_projection':
                            for col in self._Categorical_encoder__Lcat:
                                exp_ = np.exp(-df_train[col].nunique() * 0.05)
                                self._Categorical_encoder__K[col] = np.int(5 * (1 - exp_)) + 1
                                d = dict()
                                levels = list(df_train[col].unique())
                                nan = False
                                if np.NaN in levels:
                                    nan = True
                                    levels.remove(np.NaN)
                                for k in range(self._Categorical_encoder__K[col]):
                                    if k == 0:
                                        levels = sorted(levels)
                                    else:
                                        np.random.seed(k)
                                        np.random.shuffle(levels)
                                    for enc, level in enumerate([np.NaN] * nan + levels):
                                        if k == 0:
                                            d[level] = [
                                             enc]
                                        else:
                                            d[level] = d[level] + [enc]

                                self._Categorical_encoder__Enc[col] = d

                            self._Categorical_encoder__fitOK = True
                        else:
                            raise ValueError('Categorical encoding strategy is not valid')
        return self

    def fit_transform(self, df_train, y_train):
        """Fits Categorical Encoder and transforms the dataset.

        Fit categorical encoder following strategy parameter and transform the
        dataset df_train.

        Parameters
        ----------
        df_train : pandas.Dataframe of shape = (n_train, n_features)
            The training dataset with numerical and categorical features.
            NA values are allowed.
        y_train : pandas.Series of shape = (n_train, ).
            The target for classification or regression tasks.

        Returns
        -------
        pandas.Dataframe of shape = (n_train, n_features)
            Training dataset with numerical and encoded categorical features.

        """
        self.fit(df_train, y_train)
        return self.transform(df_train)

    def transform(self, df):
        """Transform categorical variable of df dataset.

        Transform df DataFrame encoding categorical features with the strategy
        parameter if self.__fitOK is set to True.

        Parameters
        ----------
        df : pandas.Dataframe of shape = (n_train, n_features)
            The training dataset with numerical and categorical features.
            NA values are allowed.

        Returns
        -------
        pandas.Dataframe of shape = (n_train, n_features)
            The dataset with numerical and encoded categorical features.

        """
        if self._Categorical_encoder__fitOK:
            if len(self._Categorical_encoder__Lcat) == 0:
                return df[self._Categorical_encoder__Lnum]
            if self.strategy == 'label_encoding':
                for col in self._Categorical_encoder__Lcat:
                    unknown_levels = list(set(df[col].values) - set(self._Categorical_encoder__Enc[col].keys()))
                    if len(unknown_levels) != 0:
                        new_enc = len(self._Categorical_encoder__Enc[col])
                        for unknown_level in unknown_levels:
                            d = self._Categorical_encoder__Enc[col]
                            d[unknown_level] = new_enc
                            self._Categorical_encoder__Enc[col] = d

                if len(self._Categorical_encoder__Lnum) == 0:
                    return pd.concat([pd.DataFrame(df[col].apply(lambda x: self._Categorical_encoder__Enc[col][x]).values, columns=[col], index=df.index) for col in self._Categorical_encoder__Lcat], axis=1)[df.columns]
                else:
                    return pd.concat([
                     df[self._Categorical_encoder__Lnum]] + [pd.DataFrame(df[col].apply(lambda x: self._Categorical_encoder__Enc[col][x]).values, columns=[col], index=df.index) for col in self._Categorical_encoder__Lcat], axis=1)[df.columns]
            else:
                if self.strategy == 'dummification':
                    sub_var = []
                    missing_var = []
                    for col in self._Categorical_encoder__Lcat:
                        unique_levels = set(df[col].values)
                        sub_levels = unique_levels & set(self._Categorical_encoder__Enc[col])
                        missing_levels = [col + '_' + str(s) for s in list(set(self._Categorical_encoder__Enc[col]) - sub_levels)]
                        sub_levels = [col + '_' + str(s) for s in list(sub_levels)]
                        sub_var = sub_var + sub_levels
                        missing_var = missing_var + missing_levels

                    if len(missing_var) != 0:
                        return pd.SparseDataFrame(pd.concat([
                         pd.get_dummies(df, sparse=True)[(list(self._Categorical_encoder__Lnum) + sub_var)]] + [
                         pd.DataFrame(np.zeros((df.shape[0],
                          len(missing_var))), columns=missing_var, index=df.index)], axis=1)[(list(self._Categorical_encoder__Lnum) + sorted(missing_var + sub_var))])
                    else:
                        return pd.get_dummies(df, sparse=True)[(list(self._Categorical_encoder__Lnum) + sorted(sub_var))]
                else:
                    if self.strategy == 'entity_embedding':

                        def get_embeddings(x, col, i):
                            if int(self._Categorical_encoder__Enc[col][x]) < np.shape(self._Categorical_encoder__weights[i])[0]:
                                return self._Categorical_encoder__weights[i][int(self._Categorical_encoder__Enc[col][x]), :]
                            return np.mean(self._Categorical_encoder__weights[i], axis=0)

                        for col in self._Categorical_encoder__Lcat:
                            unknown_levels = list(set(df[col].values) - set(self._Categorical_encoder__Enc[col].keys()))
                            if len(unknown_levels) != 0:
                                new_enc = len(self._Categorical_encoder__Enc[col])
                                for unknown_level in unknown_levels:
                                    d = self._Categorical_encoder__Enc[col]
                                    d[unknown_level] = new_enc
                                    self._Categorical_encoder__Enc[col] = d

                        if len(self._Categorical_encoder__Lnum) == 0:
                            return pd.concat([pd.DataFrame(df[col].apply(lambda x: get_embeddings(x, col, i)).tolist(), columns=[col + '_emb' + str(k + 1) for k in range(self._Categorical_encoder__K[col])], index=df.index) for i, col in enumerate(self._Categorical_encoder__Lcat)], axis=1)
                        else:
                            return pd.concat([
                             df[self._Categorical_encoder__Lnum]] + [pd.DataFrame(df[col].apply(lambda x: get_embeddings(x, col, i)).tolist(), columns=[col + '_emb' + str(k + 1) for k in range(self._Categorical_encoder__K[col])], index=df.index) for i, col in enumerate(self._Categorical_encoder__Lcat)], axis=1)
                    else:
                        for col in self._Categorical_encoder__Lcat:
                            unknown_levels = list(set(df[col].values) - set(self._Categorical_encoder__Enc[col].keys()))
                            if len(unknown_levels) != 0:
                                new_enc = len(self._Categorical_encoder__Enc[col])
                                for unknown_level in unknown_levels:
                                    d = self._Categorical_encoder__Enc[col]
                                    d[unknown_level] = [new_enc for _ in range(self._Categorical_encoder__K[col])]
                                    self._Categorical_encoder__Enc[col] = d

                        if len(self._Categorical_encoder__Lnum) == 0:
                            return pd.concat([pd.DataFrame(df[col].apply(lambda x: self._Categorical_encoder__Enc[col][x]).tolist(), columns=[col + '_proj' + str(k + 1) for k in range(self._Categorical_encoder__K[col])], index=df.index) for col in self._Categorical_encoder__Lcat], axis=1)
                        else:
                            return pd.concat([
                             df[self._Categorical_encoder__Lnum]] + [pd.DataFrame(df[col].apply(lambda x: self._Categorical_encoder__Enc[col][x]).tolist(), columns=[col + '_proj' + str(k + 1) for k in range(self._Categorical_encoder__K[col])], index=df.index) for col in self._Categorical_encoder__Lcat], axis=1)
        else:
            raise ValueError('Call fit or fit_transform function before')