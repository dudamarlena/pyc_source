# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/pschork/workspace/numerai-cli/numerai_compute/examples/python3-multimodel/model.py
# Compiled at: 2020-05-12 03:12:32
# Size of source mod 2**32: 1484 bytes
import pickle, joblib, numerox as nx
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.svm import SVC
from sklearn import decomposition, pipeline, preprocessing

class LinearModel(nx.Model):
    model_id = 'fcd5e7bc-adf1-49a3-920d-4f30ec951be1'

    def __init__(self, verbose=False):
        self.verbose = verbose
        self.model = LinearRegression()

    def fit(self, dfit, tournament):
        self.model.fit(dfit.x, dfit.y[tournament])

    def fit_predict(self, dfit, dpre, tournament):
        yhat = self.model.predict(dpre.x)
        return (
         dpre.ids, yhat)

    def save(self, filename):
        joblib.dump(self, filename)

    @classmethod
    def load(cls, filename):
        return joblib.load(filename)


class YetAnotherLinearModel(LinearModel):
    model_id = None

    def fit_predict(self, dfit, dpre, tournament):
        yhat = self.model.predict(dpre.x)
        return (
         dpre.ids, yhat)


models = [
 LinearModel, YetAnotherLinearModel]