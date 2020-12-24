# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/datascienceutils/sklearnUtils.py
# Compiled at: 2017-11-27 07:43:32
# Size of source mod 2**32: 7310 bytes
import copy, fnmatch, numpy as np, os, pandas as pd, json
from collections import defaultdict
from sklearn.externals import joblib
from sklearn.preprocessing import LabelEncoder, MultiLabelBinarizer, LabelBinarizer
from . import settings
from . import utils

def feature_scale_or_normalize(dataframe, col_names, norm_type='StandardScaler'):
    """
    Basically converts floating point or integer valued columns to fit into the range of 0 to 1
    """
    from sklearn.preprocessing import StandardScaler, MinMaxScaler
    if norm_type == 'StandardScaler':
        return StandardScaler().fit_transform(dataframe[col_names])
    else:
        if norm_type == 'MinMaxScaler':
            return MinMaxScaler().fit_transform(dataframe[col_names])
        return


def feature_select(dataframe, target=None, selector='variance', **kwargs):
    from sklearn.feature_selection import VarianceThreshold, SelectKBest
    if selector == 'variance':
        selector = VarianceThreshold()
        return selector.fit_transform(dataframe)
    if selector == 'SelectKBest':
        assert target
        return SelectKBest(chi2, k=2).fit_transform(dataframe, target)
    raise "Don't know this feature selector"


def feature_standardize(dataframe, col_names):
    """
    In essence makes sure the column values obey-or-very close to the standard-z- distribution
    But how?? and why is it not confounding all yours to think before using this, but
    generally this helps logistic regression models from being domminated by high variance variables.
    From here: http://www.analyticsvidhya.com/blog/2016/07/practical-guide-data-preprocessing-python-scikit-learn/
    """
    from sklearn.preprocessing import scale
    return scale(dataframe[col_names])


def encode_labels(dataframe, column):
    if dataframe[column].nunique() == 2:
        enc = LabelBinarizer()
        encoded_labels = enc.fit_transform(dataframe[column].tolist())
    else:
        le = LabelEncoder()
        encoded_labels = le.fit_transform(dataframe[column])
    return encoded_labels


def dump_model(model, filename, model_params):
    """
    @params:
        @model: actual scikits-learn (or supported by sklearn.joblib) model file
        @model_params: parameters used to build the model
        @filename: Filename to store the model as.

    @output:
        Dumps the model and the parameters as separate files
    """
    import uuid
    from sklearn.externals import joblib
    if not model:
        raise AssertionError('Model required')
    else:
        if not filename:
            raise AssertionError('Filename Required')
        else:
            if not model_params:
                raise AssertionError('model parameters (dict required)')
            elif not model_params['model_type']:
                raise AssertionError('model_type required in model_params')
            assert model_params['output_type'], 'output_type required in model_params'
        assert model_params['input_metadata'], 'input_metadata required in model_params'
    if not model_params['output_metadata']:
        model_params['output_metadata'] = None
    model_params.update({'filename':filename,  'id':str(uuid.uuid4())})
    with open(utils.get_full_path((settings.MODELS_BASE_PATH), filename, model_params,
      extn='.json', params_file=True), 'w') as (params_file):
        json.dump(model_params, params_file)
    joblib.dump(model, utils.get_full_path((settings.MODELS_BASE_PATH), filename, model_params,
      extn='.pkl'),
      compress=('lzma', 3))


def load_model(filename=None, model_type=None):
    """
    @params:
        @filename: Filename..
        @model_type: Pass, if you can't find filename. we use regex on the settings.models_base_path to find matching
                filenames and pick latest file for the model

    @return:
        @model: joblib.load(filename). basically the model
        @params: The parameters the model  was stored with  if it was
    """
    foldername = settings.MODELS_BASE_PATH
    if not filename:
        if not model_type:
            raise AssertionError('model_type or filename mandatory')
        else:
            relevant_models = list(filter(lambda x: fnmatch.fnmatch(x, '*' + model_type + '*.pkl'), os.listdir(foldername)))
            assert relevant_models, 'no relevant models found'
        relevant_models.sort(key=(lambda x: os.stat(os.path.join(foldername, x)).st_mtime), reverse=True)
        model = joblib.load(os.path.join(foldername, relevant_models[0]))
        names = relevant_models[0].split('_')
        names[-1] = names[(-1)].split('.')[0]
    else:
        model = joblib.load(os.path.join(foldername, filename + '.pkl'))
        names = filename.split('_')
    names.append('params')
    with open(os.path.join(foldername, '_'.join(names)) + '.json', 'r') as (fd):
        params = json.load(fd)
    return (
     model, params)


def load_latest_model(foldername, model_type='knn'):
    """
    Parses through the files in the model folder and returns the latest model
    @model_type: can be overloaded to match any string. though the function surrounds a * after value
    """
    if not foldername:
        raise AssertionError('Please pass in a foldername')
    else:
        relevant_models = list(filter(lambda x: fnmatch.fnmatch(x, '*' + model_type + '*.pkl'), os.listdir(foldername)))
        assert relevant_models, 'no relevant models found'
    relevant_models.sort(key=(lambda x: os.stat(os.path.join(foldername, x)).st_mtime), reverse=True)
    latest_model = relevant_models[0]
    return joblib.load(os.path.join(foldername, latest_model))


class MultiColumnLabelEncoder:

    def __init__(self, columns=None):
        self.encoders = defaultdict(LabelEncoder)
        if columns:
            self.columns = columns
            for each in self.columns:
                self.encoders[each] = LabelEncoder()

    def fit(self, X, y=None):
        return self

    def reverse_transform_all(self, X):
        output = copy.deepcopy(X)
        if self.columns is not None:
            for col in self.columns:
                output[col] = self.encoders[col].inverse_transform(output[col])

        else:
            for colname, col in output.iteritems():
                output[colname] = self.encoders[col].inverse_transform(col)

        return output

    def transform(self, X):
        """
        Transforms columns of X specified in self.columns using
        LabelEncoder(). If no columns specified, transforms all
        columns in X.
        """
        output = copy.deepcopy(X)
        if self.columns is not None:
            for col in self.columns:
                output[col] = self.encoders[col].fit_transform(output[col])

        else:
            for colname, col in output.iteritems():
                output[colname] = self.encoders[col].fit_transform(col)

        return output

    def reverse_transform(self, X, y=None):
        return self.fit(X, y).inverse_transform(X)

    def fit_transform(self, X, y=None):
        return self.fit(X, y).transform(X)


def cross_val_predict_score(model, actuals, predictions):
    from sklearn.cross_validation import cross_val_predict
    return cross_val_predict(model, actuals, predictions)


def accuracy_calc(actuals, predictions):
    from sklearn.metrics import accuracy_score
    return accuracy_score(actuals, predictions)