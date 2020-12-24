# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nwinter/PycharmProjects/photon_projects/photon_core/photonai/base/photon_pipeline.py
# Compiled at: 2019-11-07 12:26:02
# Size of source mod 2**32: 22585 bytes
import datetime, os, numpy as np
from sklearn.utils.metaestimators import _BaseComposition
from photonai.base.cache_manager import CacheManager
from photonai.helper.helper import PhotonDataHelper
import photonai.photonlogger.logger as logger

class PhotonPipeline(_BaseComposition):

    def __init__(self, elements, random_state=False):
        self.elements = elements
        self.random_state = random_state
        self.current_config = None
        self.caching = False
        self._fold_id = None
        self._cache_folder = None
        self.time_monitor = {'fit':[],  'transform_computed':[],  'transform_cached':[],  'predict':[]}
        self.cache_man = None
        self._single_subject_caching = False
        self._fix_fold_id = False
        self._do_not_delete_cache_folder = False
        self._parallel_use = False
        self._meta_information = None
        self.skip_loading = False

    def set_lock(self, lock):
        self.cache_man.lock = lock

    @property
    def single_subject_caching(self):
        return self._single_subject_caching

    @single_subject_caching.setter
    def single_subject_caching(self, value: bool):
        if value:
            self._fix_fold_id = True
            self._do_not_delete_cache_folder = True
        else:
            self._fix_fold_id = False
            self._do_not_delete_cache_folder = False
        self._single_subject_caching = value

    @property
    def fold_id(self):
        return self._fold_id

    @fold_id.setter
    def fold_id(self, value):
        if value is None:
            self._fold_id = ''
            self.caching = False
            self.cache_man = None
        else:
            if self._fix_fold_id:
                self._fold_id = 'fixed_fold_id'
            else:
                self._fold_id = str(value)
            self.caching = True
            self.cache_man = CacheManager(self._fold_id, self.cache_folder, self._parallel_use, self._single_subject_caching)

    @property
    def cache_folder(self):
        return self._cache_folder

    @cache_folder.setter
    def cache_folder(self, value):
        if not self._do_not_delete_cache_folder:
            self._cache_folder = value
        else:
            if isinstance(value, str):
                if not value.endswith('DND'):
                    self._cache_folder = value + 'DND'
                else:
                    self._cache_folder = value
            elif isinstance(self._cache_folder, str):
                self.caching = True
                if not os.path.isdir(self._cache_folder):
                    os.makedirs(self._cache_folder)
                self.cache_man = CacheManager(self._fold_id, self.cache_folder, self._parallel_use, self._single_subject_caching)
            else:
                self.caching = False

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
        return self._get_params('elements', deep=deep)

    def set_params(self, **kwargs):
        """Set the parameters of this estimator.
        Valid parameter keys can be listed with ``get_params()``.
        Returns
        -------
        self
        """
        if self.current_config is not None:
            if len(self.current_config) > 0:
                if kwargs is not None:
                    if len(kwargs) == 0:
                        raise ValueError('Pipeline cannot set parameters to elements with an emtpy dictionary. Old values persist')
        self.current_config = kwargs
        (self._set_params)(*('elements', ), **kwargs)
        return self

    def _validate_elements(self):
        names, estimators = zip(*self.elements)
        self._validate_names(names)
        transformers = estimators[:-1]
        estimator = estimators[(-1)]
        for t in transformers:
            if t is None:
                continue
            if hasattr(t, 'fit') or hasattr(t, 'transform'):
                raise TypeError("All intermediate elements should be transformers and implement fit and transform. '%s' (type %s) doesn't" % (
                 t, type(t)))

        if estimator is not None:
            if not hasattr(estimator, 'fit'):
                raise TypeError("Last step of Pipeline should implement fit. '%s' (type %s) doesn't" % (
                 estimator, type(estimator)))

    def fit(self, X, y=None, **kwargs):
        self._validate_elements()
        X, y, kwargs = self._caching_fit_transform(X, y, kwargs, fit=True)
        if self._final_estimator is not None:
            logger.debug('PhotonPipeline: Fitting ' + self._final_estimator.name)
            fit_start_time = datetime.datetime.now()
            if self.random_state:
                self._final_estimator.random_state = self.random_state
            (self._final_estimator.fit)(X, y, **kwargs)
            n = PhotonDataHelper.find_n(X)
            fit_duration = (datetime.datetime.now() - fit_start_time).total_seconds()
            self.time_monitor['fit'].append((self.elements[(-1)][0], fit_duration, n))
        return self

    def check_for_numpy_array(self, list_object):
        if isinstance(list_object, list):
            return np.asarray(list_object)
        return list_object

    def transform(self, X, y=None, **kwargs):
        """
        Calls transform on every step that offers a transform function
        including the last step if it has the transformer flag,
        and excluding the last step if it has the estimator flag but no transformer flag.

        Returns transformed X, y and kwargs
        """
        if self.single_subject_caching:
            initial_X = np.array(X)
        else:
            initial_X = None
        X, y, kwargs = self._caching_fit_transform(X, y, kwargs)
        if self._final_estimator is not None:
            if self._estimator_type is None:
                if self.caching:
                    X, y, kwargs = self.load_or_save_cached_data((self._final_estimator.name), X, y, kwargs, (self._final_estimator),
                      initial_X=initial_X)
                else:
                    logger.debug('PhotonPipeline: Transforming data with ' + self._final_estimator.name)
                    X, y, kwargs = (self._final_estimator.transform)(X, y, **kwargs)
        return (
         X, y, kwargs)

    def load_or_save_cached_data(self, name, X, y, kwargs, transformer, fit=False, needed_for_further_computation=False, initial_X=None):
        if (self.single_subject_caching or self).skip_loading and not needed_for_further_computation:
            if self.cache_man.check_cache(name):
                return (X, y, kwargs)
                cached_result = None
            else:
                start_time_for_loading = datetime.datetime.now()
                cached_result = self.cache_man.load_cached_data(name)
            if cached_result is None:
                X, y, kwargs = (self._do_timed_fit_transform)(name, transformer, fit, X, y, **kwargs)
                start_time_saving = datetime.datetime.now()
                self.cache_man.save_data_to_cache(name, (X, y, kwargs))
                saving_duration = (datetime.datetime.now() - start_time_saving).total_seconds()
                self.time_monitor['transform_cached'].append((name, saving_duration, 1))
            else:
                X, y, kwargs = cached_result[0], cached_result[1], cached_result[2]
                loading_duration = (datetime.datetime.now() - start_time_for_loading).total_seconds()
                n = PhotonDataHelper.find_n(X)
                self.time_monitor['transform_cached'].append((name, loading_duration, n))
            return (
             X, y, kwargs)
            processed_X, processed_y, processed_kwargs = list(), list(), dict()
            X_uncached, y_uncached, kwargs_uncached, initial_X_uncached = (list(), list(), dict(), list())
            list_of_idx_cached, list_of_idx_non_cached = list(), list()
            nr = PhotonDataHelper.find_n(X)
            for start, stop in PhotonDataHelper.chunker(nr, 1):
                X_key, _, _ = PhotonDataHelper.split_data(initial_X, None, {}, start, stop)
                X_batched, y_batched, kwargs_dict_batched = PhotonDataHelper.split_data(X, y, kwargs, start, stop)
                self.cache_man.update_single_subject_state_info(X_key)
                if self.cache_man.check_cache(name):
                    list_of_idx_cached.append(start)
                else:
                    list_of_idx_non_cached.append(start)
                    X_uncached = PhotonDataHelper.stack_data_vertically(X_uncached, X_batched)
                    y_uncached = PhotonDataHelper.stack_data_vertically(y_uncached, y_batched)
                    initial_X_uncached = PhotonDataHelper.stack_data_vertically(initial_X_uncached, X_key)
                    kwargs_uncached = PhotonDataHelper.join_dictionaries(kwargs_uncached, kwargs_dict_batched)

            if len(list_of_idx_non_cached) > 0:
                new_group_X, new_group_y, new_group_kwargs = (self._do_timed_fit_transform)(name, transformer, fit, 
                 X_uncached, 
                 y_uncached, **kwargs_uncached)
                nr = PhotonDataHelper.find_n(new_group_X)
                for start in range(nr):
                    X_batched, y_batched, kwargs_dict_batched = PhotonDataHelper.split_data(new_group_X, new_group_y, new_group_kwargs, start, start)
                    X_key, _, _ = PhotonDataHelper.split_data(initial_X_uncached, None, {}, start, start)
                    self.cache_man.update_single_subject_state_info(X_key)
                    start_time_saving = datetime.datetime.now()
                    self.cache_man.save_data_to_cache(name, (X_batched, y_batched, kwargs_dict_batched))
                    saving_duration = (datetime.datetime.now() - start_time_saving).total_seconds()
                    self.time_monitor['transform_cached'].append((name, saving_duration, 1))

                if not self.skip_loading or needed_for_further_computation:
                    processed_X, processed_y, processed_kwargs = new_group_X, new_group_y, new_group_kwargs
            if len(list_of_idx_cached) > 0:
                if not self.skip_loading or needed_for_further_computation:
                    for cache_idx in list_of_idx_cached:
                        self.cache_man.update_single_subject_state_info([initial_X[cache_idx]])
                        start_time_for_loading = datetime.datetime.now()
                        transformed_X, transformed_y, transformed_kwargs = self.cache_man.load_cached_data(name)
                        loading_duration = (datetime.datetime.now() - start_time_for_loading).total_seconds()
                        self.time_monitor['transform_cached'].append((name, loading_duration, PhotonDataHelper.find_n(X)))
                        processed_X, processed_y, processed_kwargs = PhotonDataHelper.join_data(processed_X, transformed_X, processed_y, transformed_y, processed_kwargs, transformed_kwargs)

            logger.debug(name + ' loaded ' + str(len(list_of_idx_cached)) + ' items from cache and computed ' + str(len(list_of_idx_non_cached)))
            if not self.skip_loading or needed_for_further_computation:
                processed_X, processed_y, processed_kwargs = PhotonDataHelper.resort_splitted_data(processed_X, processed_y, processed_kwargs, PhotonDataHelper.stack_data_vertically(list_of_idx_cached, list_of_idx_non_cached))
        return (
         processed_X, processed_y, processed_kwargs)

    def _do_timed_fit_transform(self, name, transformer, fit, X, y, **kwargs):
        n = PhotonDataHelper.find_n(X)
        if self.random_state:
            transformer.random_state = self.random_state
        if fit:
            logger.debug('PhotonPipeline: Fitting ' + transformer.name)
            fit_start_time = datetime.datetime.now()
            (transformer.fit)(X, y, **kwargs)
            fit_duration = (datetime.datetime.now() - fit_start_time).total_seconds()
            self.time_monitor['fit'].append((name, fit_duration, n))
        logger.debug('PhotonPipeline: Transforming data with ' + transformer.name)
        transform_start_time = datetime.datetime.now()
        X, y, kwargs = (transformer.transform)(X, y, **kwargs)
        transform_duration = (datetime.datetime.now() - transform_start_time).total_seconds()
        self.time_monitor['transform_computed'].append((name, transform_duration, n))
        return (X, y, kwargs)

    def _caching_fit_transform(self, X, y, kwargs, fit=False):
        if self.single_subject_caching:
            initial_X = np.array(X)
        else:
            initial_X = None
        if self.caching:
            self.cache_man.hash = self._fold_id
            self.cache_man.cache_folder = self.cache_folder
            if not self.single_subject_caching:
                self.cache_man.prepare([name for name, e in self.elements], self.current_config, X)
            else:
                self.cache_man.prepare([name for name, e in self.elements], (self.current_config), single_subject_caching=True)
            last_cached_item = None
        num_steps = len(self.elements) - 1
        for num, (name, transformer) in enumerate(self.elements[:-1]):
            if self.caching and not self.current_config is None:
                if not hasattr(transformer, 'skip_caching') or transformer.skip_caching:
                    X, y, kwargs = (self._do_timed_fit_transform)(name, transformer, fit, X, y, **kwargs)
            elif self.cache_man.check_cache(name):
                last_cached_item = name
                if num + 1 == num_steps:
                    X, y, kwargs = self.skip_loading or self.load_or_save_cached_data(last_cached_item, X, y, kwargs, transformer, fit, initial_X=initial_X)
            else:
                if last_cached_item is not None:
                    X, y, kwargs = self.load_or_save_cached_data(last_cached_item, X, y, kwargs, transformer, fit, needed_for_further_computation=True,
                      initial_X=initial_X)
                X, y, kwargs = self.load_or_save_cached_data(name, X, y, kwargs, transformer, fit, initial_X=initial_X)
            X = self.check_for_numpy_array(X)
            y = self.check_for_numpy_array(y)

        return (X, y, kwargs)

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
                logger.debug('PhotonPipeline: Predicting with ' + self._final_estimator.name + ' ...')
                predict_start_time = datetime.datetime.now()
                y_pred = (self._final_estimator.predict)(X, **kwargs)
                predict_duration = (datetime.datetime.now() - predict_start_time).total_seconds()
                n = PhotonDataHelper.find_n(X)
                self.time_monitor['predict'].append((self.elements[(-1)][0], predict_duration, n))
                return y_pred
            return X
        else:
            return

    def predict_proba(self, X, training: bool=False, **kwargs):
        if not training:
            X, _, kwargs = (self.transform)(X, y=None, **kwargs)
        elif self._final_estimator is not None:
            if self._final_estimator.is_estimator:
                if hasattr(self._final_estimator, 'predict_proba'):
                    if hasattr(self._final_estimator, 'needs_covariates'):
                        if self._final_estimator.needs_covariates:
                            return (self._final_estimator.predict_proba)(X, **kwargs)
                        return self._final_estimator.predict_proba(X)
                    else:
                        return self._final_estimator.predict_proba(X)
        raise NotImplementedError('The final estimator does not have a predict_proba method')

    def inverse_transform(self, X, y=None, **kwargs):
        for name, transform in self.elements[::-1]:
            try:
                X, y, kwargs = (transform.inverse_transform)(X, y, **kwargs)
            except Exception as e:
                try:
                    if isinstance(e, NotImplementedError):
                        return (
                         X, y, kwargs)
                finally:
                    e = None
                    del e

        return (
         X, y, kwargs)

    def fit_transform(self, X, y=None, **kwargs):
        raise NotImplementedError('fit_transform not yet implemented in PHOTON Pipeline')

    def fit_predict(self, X, y=None, **kwargs):
        raise NotImplementedError('fit_predict not yet implemented in PHOTON Pipeline')

    def copy_me(self):
        pipeline_steps = []
        for item_name, item in self.elements:
            cpy = item.copy_me()
            if isinstance(cpy, list):
                for new_step in cpy:
                    pipeline_steps.append((new_step.name, new_step))

            else:
                pipeline_steps.append((cpy.name, cpy))

        new_pipe = PhotonPipeline(pipeline_steps)
        new_pipe.random_state = self.random_state
        return new_pipe

    @property
    def named_steps(self):
        return dict(self.elements)

    @property
    def _final_estimator(self):
        return self.elements[(-1)][1]

    @property
    def _estimator_type(self):
        return getattr(self._final_estimator, '_estimator_type')

    def clear_cache(self):
        if self.cache_man is not None:
            self.cache_man.clear_cache()

    def _add_preprocessing(self, preprocessing):
        if preprocessing:
            self.elements.insert(0, (preprocessing.name, preprocessing))

    @property
    def feature_importances_(self):
        return self.elements[(-1)][1].feature_importances_