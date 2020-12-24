# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/getml/models/validation.py
# Compiled at: 2020-03-16 07:21:38
# Size of source mod 2**32: 19753 bytes
import numbers, numpy as np
from getml.helpers.validation import _check_parameter_bounds
from .aggregations import _all_aggregations

def _validate_multirel_model_parameters(aggregation, allow_sets, delta_t, feature_selector, grid_factor, include_categorical, loss_function, max_length, min_num_samples, num_features, num_subfeatures, num_threads, predictor, regularization, round_robin, sampling_factor, seed, share_aggregations, share_conditions, share_selected_features, shrinkage, use_timestamps):
    """Checks both the types and values of the `parameters` belonging to
    :class:`~getml.models.MultirelModel` and raises an exception is
    something is off.

    Examples:

        .. code-block:: python

            population_table, peripheral_table = getml.datasets.make_numerical()

            population_placeholder = population_table.to_placeholder()
            peripheral_placeholder = peripheral_table.to_placeholder()

            population_placeholder.join(peripheral_placeholder,
                                        join_key = "join_key",
                                        time_stamp = "time_stamp"
            )

            m = getml.models.MultirelModel(
                population = population_placeholder,
                peripheral = peripheral_placeholder,
                name = "multirel"
            )

            getml.helpers.validation.validate_MultirelModel_parameters(
                aggregation = m.aggregation,
                allow_sets = m.allow_sets,
                delta_t = m.delta_t,
                feature_selector = m.feature_selector,
                grid_factor = m.grid_factor,
                include_categorical = m.include_categorical,
                loss_function = m.loss_function,
                max_length = m.max_length,
                min_num_samples = m.min_num_samples,
                num_features = 300,
                num_subfeatures = m.num_subfeatures,
                num_threads = 4,
                predictor = m.predictor,
                regularization = m.regularization,
                round_robin = m.round_robin,
                sampling_factor = m.sampling_factor,
                seed = m.seed,
                share_aggregations = m.share_aggregations,
                share_conditions = m.share_conditions,
                share_selected_features = m.share_selected_features,
                shrinkage = 0.7,
                use_timestamps = m.use_timestamps
            )

    Args:
       parameters (dict): Dictionary containing some of all
            parameters supported in
            :class:`~getml.predictors.LinearRegression` and
            :class:`~getml.predictors.LogisticRegression`.

    Raises:
        KeyError: If an unsupported parameter is encountered.
        TypeError: If any parameter is of wrong type.
        ValueError: If any parameter does not match its possible
            choices (string) or is out of the expected bounds
            (numerical).

    Note:

        The parameters of a :class:`~getml.models.MultirelModel` have
        to be considered as a whole to ensure invalid combinations
        will be properly handled too. `predictor`, `feature_selector`,
        and `loss_function` are just supplied for references and to
        get the bigger picture of the model. They won't be validated
        by this function!

        For a more convenient handling you can create a new
        :class:`~getml.models.MultirelModel` instance, change some of
        its instance variables, and call its
        :meth:`~getml.models.MultirelModel.validate` method instead.

    """
    if not type(aggregation) is not list:
        if not len(aggregation) > 0:
            if not all([type(ll) is str for ll in aggregation]):
                raise TypeError("'aggregation' must be a non-empty list of str found in getml.models.aggregations")
        else:
            if type(allow_sets) is not bool:
                raise TypeError("'allow_sets' must be of type bool")
            else:
                if not isinstance(delta_t, numbers.Real):
                    raise TypeError("'delta_t' must be a real number")
                else:
                    if not isinstance(grid_factor, numbers.Real):
                        raise TypeError("'grid_factor' must be a real number")
                    else:
                        if type(include_categorical) is not bool:
                            raise TypeError("'include_categorical' must be of type bool")
                        else:
                            if not isinstance(max_length, numbers.Real):
                                raise TypeError("'max_length' must be a real number")
                            else:
                                if not isinstance(min_num_samples, numbers.Real):
                                    raise TypeError("'min_num_samples' must be a real number")
                                else:
                                    if not isinstance(num_features, numbers.Real):
                                        raise TypeError("'num_features' must be a real number")
                                    else:
                                        if not isinstance(num_subfeatures, numbers.Real):
                                            raise TypeError("'num_subfeatures' must be a real number")
                                        assert isinstance(num_threads, numbers.Real), "'num_threads' must be a real number"
                                    assert isinstance(regularization, numbers.Real), "'regularization' must be a real number"
                                if type(round_robin) is not bool:
                                    raise TypeError("'round_robin' must be of type bool")
                                assert isinstance(sampling_factor, numbers.Real), "'sampling_factor' must be a real number"
                            if seed is not None and not isinstance(seed, numbers.Real):
                                raise TypeError("'seed' must be a real number or None")
                        assert isinstance(share_aggregations, numbers.Real), "'share_aggregations' must be a real number"
                    assert isinstance(share_conditions, numbers.Real), "'share_conditions' must be a real number"
                assert isinstance(share_selected_features, numbers.Real), "'share_selected_features' must be a real number"
            assert isinstance(shrinkage, numbers.Real), "'shrinkage' must be a real number"
        if type(use_timestamps) is not bool:
            raise TypeError("'use_timestamps' must be of type bool")
    else:
        if not all([aa in _all_aggregations for aa in aggregation]):
            raise ValueError("'aggregation' must be a list composed exclusively of strings defined in getml.models.aggregations")
        _check_parameter_bounds(delta_t, 'delta_t', [
         0.0, np.finfo(np.float64).max])
        _check_parameter_bounds(grid_factor, 'grid_factor', [
         np.finfo(np.float64).resolution, np.finfo(np.float64).max])
        _check_parameter_bounds(max_length, 'max_length', [
         0, np.iinfo(np.int32).max])
        _check_parameter_bounds(min_num_samples, 'min_num_samples', [
         1, np.iinfo(np.int32).max])
        _check_parameter_bounds(num_features, 'num_features', [
         1, np.iinfo(np.int32).max])
        _check_parameter_bounds(num_subfeatures, 'num_subfeatures', [
         1, np.iinfo(np.int32).max])
        _check_parameter_bounds(num_threads, 'num_threads', [
         np.iinfo(np.int32).min, np.iinfo(np.int32).max])
        _check_parameter_bounds(regularization, 'regularization', [
         0.0, 1.0])
        _check_parameter_bounds(sampling_factor, 'sampling_factor', [
         0.0, np.finfo(np.float64).max])
        if seed is not None:
            _check_parameter_bounds(seed, 'seed', [
             0.0, np.iinfo(np.uint64).max])
        _check_parameter_bounds(share_aggregations, 'share_aggregations', [
         np.finfo(np.float64).resolution, 1.0])
        _check_parameter_bounds(share_conditions, 'share_conditions', [
         0.0, 1.0])
        _check_parameter_bounds(share_selected_features, 'share_selected_features', [
         0.0, 1.0])
        _check_parameter_bounds(shrinkage, 'shrinkage', [0.0, 1.0])
        if seed is not None:
            multithreaded = False
            if num_threads > 1:
                multithreaded = True
            if predictor is not None and not predictor.type == 'XGBoostClassifier':
                if predictor.type == 'XGBoostRegressor':
                    if predictor.n_jobs > 1:
                        multithreaded = True
                if feature_selector is not None and not feature_selector.type == 'XGBoostClassifier':
                    if feature_selector.type == 'XGBoostRegressor':
                        if feature_selector.n_jobs > 1:
                            multithreaded = True
                if multithreaded:
                    raise ValueError("'seed' can only used in a single-threaded setting. Please ensure both 'num_threads' and the 'n_jobs' parameters of potential getml.predictors.XGBoostClassifier and getml.predictors.XGBoostRegressor in 'predictor' and 'feature_selector' are set to 1.")


def _validate_relboost_model_parameters(allow_null_weights, delta_t, feature_selector, gamma, include_categorical, loss_function, max_depth, min_num_samples, num_features, num_subfeatures, num_threads, predictor, reg_lambda, sampling_factor, seed, share_selected_features, shrinkage, target_num, use_timestamps):
    """Checks both the types and values of the `parameters` belonging to
    :class:`~getml.models.MultirelModel` and raises an exception is
    something is off.

    Examples:

        .. code-block:: python

            population_table, peripheral_table = getml.datasets.make_numerical()

            population_placeholder = population_table.to_placeholder()
            peripheral_placeholder = peripheral_table.to_placeholder()

            population_placeholder.join(peripheral_placeholder,
                                        join_key = "join_key",
                                        time_stamp = "time_stamp"
            )

            r = getml.models.RelboostModel(
                population = population_placeholder,
                peripheral = peripheral_placeholder,
                name = "relboost"
            )

            getml.helpers.validation.validate_RelboostModel_parameters(
                allow_null_weights = r.allow_null_weights,
                delta_t = r.delta_t,
                feature_selector = r.feature_selector,
                gamma = r.gamma,
                include_categorical = r.include_categorical,
                loss_function = r.loss_function,
                max_length = r.max_length,
                min_num_samples = r.min_num_samples,
                num_features = 300,
                num_subfeatures = r.num_subfeatures,
                num_threads = 4,
                predictor = r.predictor,
                reg_lambda = r.reg_lambda,
                sampling_factor = r.sampling_factor,
                seed = r.seed,
                share_selected_features = r.share_selected_features,
                shrinkage = 0.7,
                target_num = r.target_num,
                use_timestamps = r.use_timestamps
            )

    Args:
       parameters (dict): Dictionary containing some of all
            parameters supported in
            :class:`~getml.predictors.LinearRegression` and
            :class:`~getml.predictors.LogisticRegression`.

    Raises:
        KeyError: If an unsupported parameter is encountered.
        TypeError: If any parameter is of wrong type.
        ValueError: If any parameter does not match its possible
            choices (string) or is out of the expected bounds
            (numerical).

    Note:

        The parameters of a :class:`~getml.models.RelboostModel` have
        to be considered as a whole to ensure invalid combinations
        will be properly handled too. `predictor`, `feature_selector`,
        and `loss_function` are just supplied for references and to
        get the bigger picture of the model. They won't be validated
        by this function!

        For a more convenient handling you can create a new
        :class:`~getml.models.RelboostModel` instance, change some of
        its instance variables, and call its
        :meth:`~getml.models.RelboostModel.validate` method instead.

    """
    if type(allow_null_weights) is not bool:
        raise TypeError("'allow_null_weights' must be of type bool")
    else:
        if not isinstance(delta_t, numbers.Real):
            raise TypeError("'delta_t' must be a real number")
        else:
            if not isinstance(gamma, numbers.Real):
                raise TypeError("'gamma' must be a real number")
            else:
                if type(include_categorical) is not bool:
                    raise TypeError("'include_categorical' must be of type bool")
                else:
                    if not isinstance(max_depth, numbers.Real):
                        raise TypeError("'max_depth' must be a real number")
                    else:
                        if not isinstance(min_num_samples, numbers.Real):
                            raise TypeError("'min_num_samples' must be a real number")
                        else:
                            if not isinstance(num_features, numbers.Real):
                                raise TypeError("'num_features' must be a real number")
                            else:
                                if not isinstance(num_subfeatures, numbers.Real):
                                    raise TypeError("'num_subfeatures' must be a real number")
                                if not isinstance(num_threads, numbers.Real):
                                    raise TypeError("'num_threads' must be a real number")
                                assert isinstance(reg_lambda, numbers.Real), "'reg_lambda' must be a real number"
                            assert isinstance(sampling_factor, numbers.Real), "'sampling_factor' must be a real number"
                        if seed is not None and not isinstance(seed, numbers.Real):
                            raise TypeError("'seed' must be a real number or None")
                    assert isinstance(share_selected_features, numbers.Real), "'share_selected_features' must be a real number"
                assert isinstance(shrinkage, numbers.Real), "'shrinkage' must be a real number"
            assert isinstance(target_num, numbers.Real), "'target_num' must be a real number"
        if type(use_timestamps) is not bool:
            raise TypeError("'use_timestamps' must be of type bool")
        _check_parameter_bounds(delta_t, 'delta_t', [
         0.0, np.finfo(np.float64).max])
        _check_parameter_bounds(gamma, 'gamma', [
         0.0, np.finfo(np.float64).max])
        _check_parameter_bounds(max_depth, 'max_depth', [
         0, np.iinfo(np.int32).max])
        _check_parameter_bounds(min_num_samples, 'min_num_samples', [
         1, np.iinfo(np.int32).max])
        _check_parameter_bounds(num_features, 'num_features', [
         1, np.iinfo(np.int32).max])
        _check_parameter_bounds(num_subfeatures, 'num_subfeatures', [
         1, np.iinfo(np.int32).max])
        _check_parameter_bounds(num_threads, 'num_threads', [
         np.iinfo(np.int32).min, np.iinfo(np.int32).max])
        _check_parameter_bounds(reg_lambda, 'reg_lambda', [
         0.0, np.finfo(np.float64).max])
        _check_parameter_bounds(sampling_factor, 'sampling_factor', [
         0.0, np.finfo(np.float64).max])
        if seed is not None:
            _check_parameter_bounds(seed, 'seed', [
             0.0, np.iinfo(np.uint64).max])
        _check_parameter_bounds(share_selected_features, 'share_selected_features', [
         0.0, 1.0])
        _check_parameter_bounds(shrinkage, 'shrinkage', [0.0, 1.0])
        _check_parameter_bounds(target_num, 'target_num', [
         0, np.iinfo(np.int32).max])
        if seed is not None:
            multithreaded = False
            if num_threads > 1:
                multithreaded = True
            if predictor is not None and not predictor.type == 'XGBoostClassifier':
                if predictor.type == 'XGBoostRegressor':
                    if predictor.n_jobs > 1:
                        multithreaded = True
                if feature_selector is not None and not feature_selector.type == 'XGBoostClassifier':
                    if feature_selector.type == 'XGBoostRegressor':
                        if feature_selector.n_jobs > 1:
                            multithreaded = True
                if multithreaded:
                    raise ValueError("'seed' can only used in a single-threaded setting. Please ensure both 'num_threads' and the 'n_jobs' parameters of potential getml.predictors.XGBoostClassifier and getml.predictors.XGBoostRegressor in 'predictor' and 'feature_selector' are set to 1.")