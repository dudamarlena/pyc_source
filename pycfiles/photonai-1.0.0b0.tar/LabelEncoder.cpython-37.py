# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nwinter/PycharmProjects/photon_projects/photon_core/photonai/modelwrapper/LabelEncoder.py
# Compiled at: 2019-02-21 07:32:17
# Size of source mod 2**32: 505 bytes
from sklearn.base import BaseEstimator, TransformerMixin
import sklearn.preprocessing as SKLabelEncoder

class LabelEncoder(BaseEstimator, TransformerMixin):

    def __init__(self):
        self.label_encoder_object = SKLabelEncoder()
        self.needs_y = True

    def fit(self, X, y=None, **kwargs):
        self.label_encoder_object.fit(y)
        return self

    def transform(self, X, y=None, **kwargs):
        yt = self.label_encoder_object.transform(y)
        return (X, yt)