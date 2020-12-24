# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/oaraque/git/gsi/gsitk/gsitk/features/features.py
# Compiled at: 2017-02-27 14:18:45
# Size of source mod 2**32: 1076 bytes
"""
Access operations on the feature extractors.
"""
import os, glob
from gsitk.features import utils

class Features:
    __doc__ = '\n    Class that abstracts the features. \n    '

    def transform(self, X):
        """
        Transform the text (should be normalized) to numeric features.
        Must be implemented by the class that inherits.
        """
        pass


def load_features(name, format=None):
    """Reads the features."""
    return utils.read_features(name, format)


def save_features(features, name):
    utils.save_features(features, name)


def view_features(pprint=True):
    """
    Check the available features, the ones that have already been
    extracted and stored.
    """
    features = []
    for feats in glob.glob(utils.features_path + '*'):
        filename = os.path.basename(feats)
        name = os.path.splitext(filename)[0]
        format = utils.detect_saving_format(filename)
        features.append(utils._check_features(name, format))

    if pprint:
        print('\n'.join(features))
    else:
        return features