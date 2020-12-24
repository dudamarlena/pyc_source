# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nwinter/PycharmProjects/photon_projects/photon_core/photonai/base/PhotonPipeline.py
# Compiled at: 2019-09-26 08:58:51
# Size of source mod 2**32: 5169 bytes
from sklearn.utils.metaestimators import _BaseComposition

class PhotonPipeline(_BaseComposition):

    def __init__(self, steps):
        self.steps = steps

    def get_params(self, deep=True):
        """Get parameters for this estimator.
        Parameters
        ----------
        deep : boolean, optional
            If True, will return the parameters for this estimator and
            contained subobjects that are estimators.
        Returns
        -------
        params : mapping of string to any
            Parameter names mapped to their values.
        """
        return self._get_params('steps', deep=deep)

    def set_params(self, **kwargs):
        """Set the parameters of this estimator.
        Valid parameter keys can be listed with ``get_params()``.
        Returns
        -------
        self
        """
        (self._set_params)(*('steps', ), **kwargs)
        return self

    def _validate_steps(self):
        names, estimators = zip(*self.steps)
        self._validate_names(names)
        transformers = estimators[:-1]
        estimator = estimators[(-1)]
        for t in transformers:
            if t is None:
                continue
            if hasattr(t, 'fit') or hasattr(t, 'transform'):
                raise TypeError("All intermediate steps should be transformers and implement fit and transform. '%s' (type %s) doesn't" % (
                 t, type(t)))

        if estimator is not None:
            if not hasattr(estimator, 'fit'):
                raise TypeError("Last step of Pipeline should implement fit. '%s' (type %s) doesn't" % (
                 estimator, type(estimator)))

    def fit(self, X, y=None, **kwargs):
        self._validate_steps()
        for name, transformer in self.steps[:-1]:
            (transformer.fit)(X, y, **kwargs)
            X, y, kwargs = (transformer.transform)(X, y, **kwargs)

        if self._final_estimator is not None:
            (self._final_estimator.fit)(X, y, **kwargs)
        return self

    def transform(self, X, y=None, **kwargs):
        """
        Calls transform on every step that offers a transform function
        including the last step if it has the transformer flag,
        and excluding the last step if it has the estimator flag but no transformer flag.

        Returns transformed X, y and kwargs
        """
        for name, transformer in self.steps[:-1]:
            X, y, kwargs = (transformer.transform)(X, y, **kwargs)

        if self._final_estimator is not None:
            if self._final_estimator.is_transformer:
                if not self._final_estimator.is_estimator:
                    X, y, kwargs = (self._final_estimator.transform)(X, y, **kwargs)
        return (
         X, y, kwargs)

    def predict(self, X, training=False, **kwargs):
        """
        Transforms the data for every step that offers a transform function
        and then calls the estimator with predict on transformed data.
        It returns the predictions made.

        In case the last step is no estimator, it returns the transformed data.
        """
        if not training:
            X, _, kwargs = (self.transform)(X, y=None, **kwargs)
        elif self._final_estimator is not None:
            if self._final_estimator.is_estimator:
                y_pred = (self._final_estimator.predict)(X, **kwargs)
                return y_pred
            return X
        else:
            return

    def predict_proba(self, X, training: bool=False, **kwargs):
        if not training:
            X, _, kwargs = (self.transform)(X, y=None, **kwargs)
        if self._final_estimator is not None:
            if self._final_estimator.is_estimator:
                if hasattr(self._final_estimator, 'predict_proba'):
                    return (self._final_estimator.predict_proba)(X, **kwargs)
        raise NotImplementedError('The final estimator does not have a predict_proba method')

    def inverse_transform(self, X, y=None, **kwargs):
        for name, transform in self.steps[::-1]:
            if hasattr(transform, 'inverse_transform'):
                X, y, kwargs = (transform.inverse_transform)(X, y, **kwargs)

        return (
         X, y, kwargs)

    def fit_transform(self, X, y=None, **kwargs):
        raise NotImplementedError('fit_transform not yet implemented in PHOTON Pipeline')

    def fit_predict(self, X, y=None, **kwargs):
        raise NotImplementedError('fit_predict not yet implemented in PHOTON Pipeline')

    @property
    def _estimator_type(self):
        return self.steps[(-1)][1]._estimator_type

    @property
    def named_steps(self):
        return dict(self.steps)

    @property
    def _final_estimator(self):
        return self.steps[(-1)][1]