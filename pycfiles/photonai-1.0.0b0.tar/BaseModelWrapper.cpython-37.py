# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nwinter/PycharmProjects/photon_projects/photon_core/photonai/base/BaseModelWrapper.py
# Compiled at: 2019-09-26 08:58:51
# Size of source mod 2**32: 2803 bytes


class BaseModelWrapper:
    __doc__ = '\n    The PHOTON interface for implementing custom pipeline elements.\n\n    PHOTON works on top of the scikit-learn object API,\n    [see documentation](http://scikit-learn.org/stable/developers/contributing.html#apis-of-scikit-learn-objects)\n\n    Your class should overwrite the following definitions:\n\n    - `fit(data)`: learn or adjust to the data\n\n    If it is an estimator, which means it has the ability to learn,\n\n    - it should implement `predict(data)`: using the learned model to generate prediction\n    - should inherit *sklearn.base.BaseEstimator* ([see here](http://scikit-learn.org/stable/modules/generated/sklearn.base.BaseEstimator.html))\n    - inherits *get_params* and *set_params*\n\n    If it is an transformer, which means it preprocesses or prepares the data\n\n    - it should implement `transform(data)`: applying the logic to the data to transform it\n    - should inherit from *sklearn.base.TransformerMixin* ([see here](http://scikit-learn.org/stable/modules/generated/sklearn.base.TransformerMixin.html))\n    - inherits *fit_transform* as a concatenation of both fit and transform\n    - should inherit *sklearn.base.BaseEstimator* ([see here](http://scikit-learn.org/stable/modules/generated/sklearn.base.BaseEstimator.html))\n    - inherits *get_params* and *set_params*\n\n    `Prepare for hyperparameter optimization`\n\n    PHOTON expects you to `define all parameters` that you want to optimize in the hyperparameter search in the\n    `constructor stub`, and to be addressable with the `same name as class variable`.\n    In this way you can define any parameter and it is automatically prepared for the hyperparameter search process.\n\n    See the [scikit-learn object API documentation](http://scikit-learn.org/stable/developers/contributing.html#apis-of-scikit-learn-objects) for more in depth information about the interface.\n    '

    def __init__(self):
        pass

    def fit(self, data, targets=None):
        """
        Adjust the underlying model or method to the data.

        Returns
        -------
        IMPORTANT: must return self!
        """
        pass

    def predict(self, data):
        """
        Use the learned model to make predictions.
        """
        pass

    def transform(self, data):
        """
        Apply the method's logic to the data.
        """
        pass

    def get_params(self, deep=True):
        """
        Get the models parameters.
        Automatically implemented when inheriting from sklearn.base.BaseEstimator
        """
        pass

    def set_params(self, *kwargs):
        """
        Takes the given dictionary, with the keys being the variable name, and sets the object's parameters to the given values.
        Automatically implemented when inheriting from sklearn.base.BaseEstimator
        """
        pass