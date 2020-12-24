# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nwinter/PycharmProjects/photon_projects/photon_core/photonai/processing/inner_folds.py
# Compiled at: 2019-09-11 10:06:07
# Size of source mod 2**32: 24040 bytes
import time, traceback, warnings, queue, numpy as np, json
from sklearn.pipeline import Pipeline
from multiprocessing import Process, Queue
from photonai.base.photon_elements import Stack, Branch, Switch
from photonai.base.helper import PhotonPrintHelper
from photonai.processing.results_structure import MDBHelper, MDBInnerFold, MDBScoreInformation, MDBFoldMetric, FoldOperations, MDBConfig
from photonai.photonlogger import Logger
from photonai.processing.metrics import Scorer
import warnings
warnings.filterwarnings('ignore', category=DeprecationWarning)
warnings.filterwarnings('ignore', category=FutureWarning)

class InnerFoldManager(object):
    __doc__ = '\n        Trains and tests a sklearn pipeline for a specific hyperparameter combination with cross-validation,\n        calculates metrics for each fold and averages metrics over all folds\n    '

    def __init__(self, pipe_ctor, specific_config: dict, optimization_infos, cross_validation_infos, outer_fold_id, optimization_constraints: list=None, raise_error: bool=False, save_predictions: bool=False, save_feature_importances: bool=False, training: bool=False, cache_folder=None, cache_updater=None, parallel_cv: bool=False, nr_of_parrallel_processes: int=4):
        """
        Creates a new InnerFoldManager object
        :param pipe: The sklearn pipeline instance that shall be trained and tested
        :type pipe: Pipeline
        :param specific_config: The hyperparameter configuration to test
        :type specific_config: dict
        :param raise_error: if true, raises exception when training and testing the pipeline fails
        :type raise_error: bool
        """
        self.params = specific_config
        self.pipe = pipe_ctor
        self.optimization_infos = optimization_infos
        self.optimization_constraints = optimization_constraints
        self.outer_fold_id = outer_fold_id
        self.cross_validation_infos = cross_validation_infos
        self.save_predictions = save_predictions
        self.save_feature_importances = save_feature_importances
        self.cache_folder = cache_folder
        self.cache_updater = cache_updater
        self.raise_error = raise_error
        self.training = training
        self.parallel_cv = parallel_cv
        self.nr_of_parallel_processes = nr_of_parrallel_processes

    def fit(self, X, y, **kwargs):
        """
        Iterates over cross-validation folds and trains the pipeline, then uses it for predictions.
        Calculates metrics per fold and averages them over fold.
        :param X: Training and test data
        :param y: Training and test targets
        :returns: configuration class for result tree that monitors training and test performance
        """
        config_item = MDBConfig()
        config_item.config_dict = self.params
        config_item.inner_folds = []
        config_item.metrics_test = []
        config_item.metrics_train = []
        original_save_predictions = self.save_predictions
        save_predictions = bool(self.save_predictions)
        save_feature_importances = self.save_feature_importances
        if self.cross_validation_infos.calculate_metrics_across_folds:
            save_predictions = True
        if self.parallel_cv:
            nr_of_processes = min(self.nr_of_parallel_processes)
            folds_to_do = Queue()
            folds_done = Queue()
        try:
            for idx, (inner_fold_id, inner_fold) in enumerate(self.cross_validation_infos.inner_folds[self.outer_fold_id].items()):
                train, test = inner_fold.train_indices, inner_fold.test_indices
                kwargs_cv_train = {}
                kwargs_cv_test = {}
                if len(kwargs) > 0:
                    for name, sublist in kwargs.items():
                        if isinstance(sublist, (list, np.ndarray)):
                            kwargs_cv_train[name] = sublist[train]
                            kwargs_cv_test[name] = sublist[test]

                new_pipe = self.pipe()
                if self.cache_folder is not None:
                    if self.cache_updater is not None:
                        self.cache_updater(new_pipe, self.cache_folder, inner_fold_id)
                if not config_item.human_readable_config:
                    config_item.human_readable_config = PhotonPrintHelper.config_to_human_readable_dict(new_pipe, self.params)
                job_data = InnerFoldManager.InnerCVJob(pipe=new_pipe, config=(dict(self.params)),
                  metrics=(list(self.optimization_infos.metrics)),
                  callbacks=(self.optimization_constraints),
                  train_data=(InnerFoldManager.JobData(X[train], y[train], train, dict(kwargs_cv_train))),
                  test_data=(InnerFoldManager.JobData(X[test], y[test], test, dict(kwargs_cv_test))),
                  save_feature_importances=save_feature_importances,
                  save_predictions=save_predictions)
                if not self.parallel_cv:
                    Logger().debug(config_item.human_readable_config)
                    Logger().debug('calculating...')
                    curr_test_fold, curr_train_fold = InnerFoldManager.fit_and_score(job_data)
                    durations = job_data.pipe.time_monitor
                    self.update_config_item_with_inner_fold(config_item=config_item, fold_cnt=(idx + 1),
                      curr_train_fold=curr_train_fold,
                      curr_test_fold=curr_test_fold,
                      time_monitor=durations)
                    if isinstance(self.optimization_constraints, list):
                        break_cv = 0
                        for cf in self.optimization_constraints:
                            if not cf.shall_continue(config_item):
                                Logger().debug('Skip further cross validation of config because of performance constraints')
                                break_cv += 1
                                break

                        if break_cv > 0:
                            break
                    elif self.optimization_constraints is not None:
                        self.optimization_constraints.shall_continue(config_item) or Logger().debug('Skip further cross validation of config because of performance constraints')
                        break
                else:
                    folds_to_do.put(job_data)

            if self.parallel_cv:
                process_list = list()
                for w in range(nr_of_processes):
                    p = Process(target=(InnerFoldManager.parallel_inner_cv), args=(folds_to_do, folds_done))
                    process_list.append(p)
                    p.start()

                for p in process_list:
                    p.join()

                while not folds_done.empty():
                    curr_test_fold, curr_train_fold = folds_done.get()
                    self.update_config_item_with_inner_fold(config_item, 0, curr_test_fold, curr_train_fold, {})

            InnerFoldManager.process_fit_results(config_item, self.cross_validation_infos.calculate_metrics_across_folds, self.cross_validation_infos.calculate_metrics_per_fold, original_save_predictions, self.optimization_infos.metrics)
        except Exception as e:
            if self.raise_error:
                raise e
            Logger().error(e)
            Logger().error(traceback.format_exc())
            traceback.print_exc()
            if not isinstance(e, Warning):
                config_item.config_failed = True
            config_item.config_error = str(e)
            warnings.warn('One test iteration of pipeline failed with error')

        Logger().debug('...done with')
        Logger().info(json.dumps((config_item.human_readable_config), indent=4, sort_keys=True))
        return config_item

    class JobData:

        def __init__(self, X, y, indices, cv_kwargs):
            self.X = X
            self.y = y
            self.indices = indices
            self.cv_kwargs = cv_kwargs

    class InnerCVJob:

        def __init__(self, pipe, config, metrics, callbacks, train_data, test_data, save_predictions, save_feature_importances):
            self.pipe = pipe
            self.config = config
            self.metrics = metrics
            self.callbacks = callbacks
            self.train_data = train_data
            self.test_data = test_data
            self.save_predictions = save_predictions
            self.save_feature_importances = save_feature_importances

    @staticmethod
    def parallel_inner_cv(folds_to_do, folds_done):
        while True:
            try:
                task = folds_to_do.get_nowait()
            except queue.Empty:
                break
            else:
                fold_output = InnerFoldManager.fit_and_score(task)
                folds_done.put(fold_output)

        return True

    @staticmethod
    def update_config_item_with_inner_fold(config_item, fold_cnt, curr_train_fold, curr_test_fold, time_monitor):
        inner_fold = MDBInnerFold()
        inner_fold.fold_nr = fold_cnt
        inner_fold.training = curr_train_fold
        inner_fold.validation = curr_test_fold
        inner_fold.number_samples_validation = len(curr_test_fold.indices)
        inner_fold.number_samples_training = len(curr_train_fold.indices)
        inner_fold.time_monitor = time_monitor
        config_item.inner_folds.append(inner_fold)

    @staticmethod
    def process_fit_results(config_item, calculate_metrics_across_folds, calculate_metrics_per_fold, original_save_predictions, metrics):
        overall_y_pred_test = []
        overall_y_true_test = []
        overall_y_pred_train = []
        overall_y_true_train = []
        for fold in config_item.inner_folds:
            curr_test_fold = fold.validation
            curr_train_fold = fold.training
            if calculate_metrics_across_folds:
                if isinstance(curr_test_fold.y_pred, np.ndarray):
                    if len(curr_test_fold.y_pred.shape) > 1:
                        axis = 1
                    else:
                        axis = 0
                else:
                    axis = 0
                    overall_y_true_test = np.concatenate((overall_y_true_test, curr_test_fold.y_true), axis=axis)
                    overall_y_pred_test = np.concatenate((overall_y_pred_test, curr_test_fold.y_pred), axis=axis)
                    overall_y_true_train = np.concatenate((overall_y_true_train, curr_train_fold.y_true), axis=axis)
                    overall_y_pred_train = np.concatenate((overall_y_pred_train, curr_train_fold.y_pred), axis=axis)
                metrics_to_calculate = list(metrics)
                if 'score' in metrics_to_calculate:
                    metrics_to_calculate.remove('score')
                metrics_train = InnerFoldManager.calculate_metrics(overall_y_true_train, overall_y_pred_train, metrics_to_calculate)
                metrics_test = InnerFoldManager.calculate_metrics(overall_y_true_test, overall_y_pred_test, metrics_to_calculate)

                def metric_to_db_class(metric_list):
                    db_metrics = []
                    for metric_name, metric_value in metric_list.items():
                        new_metric = MDBFoldMetric(operation=(FoldOperations.RAW), metric_name=metric_name, value=metric_value)
                        db_metrics.append(new_metric)

                    return db_metrics

                db_metrics_train = metric_to_db_class(metrics_train)
                db_metrics_test = metric_to_db_class(metrics_test)
                if calculate_metrics_per_fold:
                    db_metrics_fold_train, db_metrics_fold_test = MDBHelper.aggregate_metrics_for_inner_folds(config_item.inner_folds, metrics)
                    config_item.metrics_train = db_metrics_train + db_metrics_fold_train
                    config_item.metrics_test = db_metrics_test + db_metrics_fold_test
                else:
                    config_item.metrics_train = db_metrics_train
                    config_item.metrics_test = db_metrics_test
                if not original_save_predictions:
                    for inner_fold in config_item.inner_folds:
                        inner_fold.training.y_true = []
                        inner_fold.training.y_pred = []
                        inner_fold.training.indices = []
                        inner_fold.validation.y_true = []
                        inner_fold.validation.y_pred = []
                        inner_fold.validation.indices = []

                else:
                    if calculate_metrics_per_fold:
                        config_item.metrics_train, config_item.metrics_test = MDBHelper.aggregate_metrics_for_inner_folds(config_item.inner_folds, metrics)

    @staticmethod
    def fit_and_score(job: InnerCVJob):
        pipe = job.pipe
        (pipe.set_params)(**job.config)
        fit_start_time = time.time()
        (pipe.fit)((job.train_data.X), (job.train_data.y), **(job.train_data).cv_kwargs)
        curr_test_fold = (InnerFoldManager.score)(pipe, job.test_data.X, job.test_data.y, job.metrics, indices=job.test_data.indices, save_predictions=job.save_predictions, 
         save_feature_importances=job.save_feature_importances, **job.test_data.cv_kwargs)
        curr_train_fold = (InnerFoldManager.score)(pipe, job.train_data.X, job.train_data.y, job.metrics, indices=job.train_data.indices, 
         save_predictions=job.save_predictions, 
         save_feature_importances=job.save_feature_importances, 
         training=True, **job.train_data.cv_kwargs)
        return (
         curr_test_fold, curr_train_fold)

    @staticmethod
    def score(estimator, X, y_true, metrics, indices=[], save_predictions=False, save_feature_importances=False, calculate_metrics: bool=True, training: bool=False, **kwargs):
        """
        Uses the pipeline to predict the given data, compare it to the truth values and calculate metrics

        :param estimator: the pipeline or pipeline element for prediction
        :param X: the data for prediction
        :param y_true: the truth values for the data
        :param metrics: the metrics to be calculated
        :param indices: the indices of the given data and targets that are logged into the result tree
        :param save_predictions: if True, the predicted value array is stored in to the result tree
        :param save_feature_importances: if True, the feature importances of the estimator, if any, are stored to the result tree
        :param training: if True, all training_only pipeline elements are executed, if False they are skipped
        :param calculate_metrics: if True, calculates metrics for given data
        :return: ScoreInformation object
        """
        scoring_time_start = time.time()
        output_metrics = {}
        non_default_score_metrics = list(metrics)
        checklist = [
         'score']
        matches = set(checklist).intersection(set(non_default_score_metrics))
        if len(matches) > 0:
            default_score = estimator.score(X, y_true)
            output_metrics['score'] = default_score
            non_default_score_metrics.remove('score')
        if not training:
            y_pred = (estimator.predict)(X, **kwargs)
        else:
            X, y_true_new, kwargs_new = (estimator.transform)(X, y_true, **kwargs)
        if y_true_new is not None:
            y_true = y_true_new
        if kwargs_new is not None:
            if len(kwargs_new) > 0:
                kwargs = kwargs_new
            y_pred = (estimator.predict)(X, training=True, **kwargs)
        else:
            f_importances = []
            if save_feature_importances:
                f_importances = InnerFoldManager.extract_feature_importances(estimator)
            if calculate_metrics:
                score_metrics = InnerFoldManager.calculate_metrics(y_true, y_pred, non_default_score_metrics)
                if output_metrics:
                    output_metrics = {**output_metrics, **score_metrics}
                else:
                    output_metrics = score_metrics
            else:
                output_metrics = {}
            final_scoring_time = time.time() - scoring_time_start
            if save_predictions:
                probabilities = []
                if hasattr(estimator._final_estimator.base_element, 'predict_proba'):
                    probabilities = (estimator.predict_proba)(X, training=training, **kwargs)
                    try:
                        if probabilities is not None:
                            if not len(probabilities) == 0:
                                probabilities = probabilities.tolist()
                    except:
                        warnings.warn('No probabilities available.')

                if not isinstance(y_pred, list):
                    y_pred = np.asarray(y_pred).tolist()
                if not isinstance(y_true, list):
                    y_true = np.asarray(y_true).tolist()
                score_result_object = MDBScoreInformation(metrics=output_metrics, score_duration=final_scoring_time,
                  y_pred=y_pred,
                  y_true=y_true,
                  indices=(np.asarray(indices).tolist()),
                  probabilities=probabilities)
                if save_feature_importances:
                    score_result_object.feature_importances = f_importances
            else:
                if save_feature_importances:
                    score_result_object = MDBScoreInformation(metrics=output_metrics, score_duration=final_scoring_time,
                      feature_importances=f_importances)
                else:
                    score_result_object = MDBScoreInformation(metrics=output_metrics, score_duration=final_scoring_time)
        return score_result_object

    @staticmethod
    def extract_feature_importances(estimator):
        final_estimator = estimator._final_estimator
        if isinstance(final_estimator, Switch):
            base_element = final_estimator.base_element.base_element
        else:
            if isinstance(final_estimator, (Branch, Stack)):
                return
            base_element = final_estimator.base_element
        if hasattr(base_element, 'coef_'):
            f_importances = base_element.coef_
            if f_importances is not None:
                f_importances = f_importances.tolist()
        else:
            if hasattr(base_element, 'feature_importances_'):
                f_importances = base_element.feature_importances_
                if f_importances is not None:
                    f_importances = f_importances.tolist()
            else:
                f_importances = None
        return f_importances

    @staticmethod
    def calculate_metrics(y_true, y_pred, metrics):
        """
        Applies all metrics to the given predicted and true values.
        The metrics are encoded via a string literal which is mapped to the according calculation function
        :param y_true: the truth values
        :type y_true: list
        :param y_pred: the predicted values
        :param metrics: list
        :return: dict of metrics
        """
        output_metrics = {}
        if metrics:
            for metric in metrics:
                scorer = Scorer.create(metric)
                if scorer is not None:
                    scorer_value = scorer(y_true, y_pred)
                    Logger().debug(str(scorer_value))
                    output_metrics[metric] = scorer_value
                else:
                    output_metrics[metric] = np.nan

        return output_metrics