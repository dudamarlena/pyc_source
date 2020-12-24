# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nwinter/PycharmProjects/photon_projects/photon_core/photonai/processing/permutation_test.py
# Compiled at: 2019-10-22 09:34:51
# Size of source mod 2**32: 19670 bytes
import numpy as np, dask
from dask.distributed import Client
from pymodm import connect
from pymodm.errors import DoesNotExist, ConnectionError
from pymongo import DESCENDING
from photonai.base import OutputSettings
import photonai.photonlogger.logger as logger
from photonai.processing.inner_folds import Scorer
from photonai.processing.results_structure import MDBPermutationResults, MDBPermutationMetrics, MDBHyperpipe, FoldOperations

class PermutationTest:

    def __init__(self, hyperpipe_constructor, permutation_id: str, n_perms=1000, n_processes=1, random_state=15):
        self.hyperpipe_constructor = hyperpipe_constructor
        self.n_perms = n_perms
        self.permutation_id = permutation_id
        self.mother_permutation_id = PermutationTest.get_mother_permutation_id(permutation_id)
        self.n_processes = n_processes
        self.random_state = random_state
        self.pipe = None
        self.metrics = None

    @staticmethod
    def manage_metrics(metrics, last_element=None, best_config_metric=''):
        metric_dict = dict()
        for metric in metrics:
            metric_dict[metric] = {'name':metric, 
             'greater_is_better':PermutationTest.set_greater_is_better(metric, last_element)}

        if best_config_metric not in metric_dict.keys():
            metric_dict[best_config_metric] = {'name':best_config_metric, 
             'greater_is_better':PermutationTest.set_greater_is_better(best_config_metric)}
        return metric_dict

    @staticmethod
    def get_mother_permutation_id(permutation_id):
        m_perm = permutation_id + '_reference'
        return m_perm

    def fit(self, X, y):
        self.pipe = self.hyperpipe_constructor()
        if not self.pipe.output_settings.mongodb_connect_url:
            raise ValueError('MongoDB connection string must be given for permutation tests')
        else:
            best_config_metric = self.pipe.optimization.best_config_metric
            self.metrics = PermutationTest.manage_metrics(self.pipe.optimization.metrics, self.pipe.elements[(-1)], best_config_metric)
            y_true = y
            connect((self.pipe.output_settings.mongodb_connect_url), alias='photon_core')
            try:
                existing_reference = MDBHyperpipe.objects.raw({'permutation_id':self.mother_permutation_id,  'computation_completed':True}).first()
                if not existing_reference.permutation_test:
                    existing_reference.permutation_test = MDBPermutationResults(n_perms=(self.n_perms))
                    existing_reference.save()
                logger.info('Found hyperpipe computation with true targets, skipping the optimization process with true targets')
            except DoesNotExist:
                logger.info('Calculating Reference Values with true targets.')
                try:
                    self.pipe.permutation_id = self.mother_permutation_id
                    self.pipe.fit(X, y_true)
                    self.pipe.results.computation_completed = True
                    self.pipe.results.permutation_test = MDBPermutationResults(n_perms=(self.n_perms))
                    self.pipe.results.save()
                except Exception as e:
                    try:
                        if self.pipe.results is not None:
                            self.pipe.results.permutation_failed = str(e)
                            self.pipe.results.save()
                    finally:
                        e = None
                        del e

            existing_permutations = list(MDBHyperpipe.objects.raw({'permutation_id':self.permutation_id,  'computation_completed':True}).only('name'))
            existing_permutations = [int(perm_run.name.split('_')[(-1)]) for perm_run in existing_permutations]
            if len(existing_permutations) > 0:
                perms_todo = set(np.arange(self.n_perms)) - set(existing_permutations)
            else:
                perms_todo = np.arange(self.n_perms)
            logger.info(str(len(perms_todo)) + ' permutation runs to do')
            if len(perms_todo) > 0:
                np.random.seed(self.random_state)
                self.permutations = [np.random.permutation(y_true) for _ in range(self.n_perms)]
                job_list = list()
                if self.n_processes > 1:
                    try:
                        my_client = Client(threads_per_worker=1, n_workers=(self.n_processes),
                          processes=False)
                        for perm_run in perms_todo:
                            del_job = dask.delayed(PermutationTest.run_parallelized_permutation)(self.hyperpipe_constructor, X, perm_run, self.permutations[perm_run], self.permutation_id)
                            job_list.append(del_job)

                        (dask.compute)(*job_list)
                    finally:
                        my_client.close()

                else:
                    for perm_run in perms_todo:
                        PermutationTest.run_parallelized_permutation(self.hyperpipe_constructor, X, perm_run, self.permutations[perm_run], self.permutation_id)

        self._calculate_results(self.permutation_id, self.metrics)
        return self

    @staticmethod
    def run_parallelized_permutation(hyperpipe_constructor, X, perm_run, y_perm, permutation_id):
        perm_pipe = hyperpipe_constructor()
        perm_pipe.verbosity = 2
        perm_pipe.name = perm_pipe.name + '_perm_' + str(perm_run)
        perm_pipe.permutation_id = permutation_id
        po = OutputSettings(mongodb_connect_url=(perm_pipe.output_settings.mongodb_connect_url), save_output=False)
        perm_pipe.output_settings = po
        perm_pipe.calculate_metrics_across_folds = False
        try:
            print('Fitting permutation ' + str(perm_run) + ' ...')
            perm_pipe.fit(X, y_perm)
            perm_pipe.results.computation_completed = True
            perm_pipe.results.save()
            print('Finished permutation ' + str(perm_run) + ' ...')
        except Exception as e:
            try:
                if perm_pipe.results is not None:
                    perm_pipe.results.permutation_failed = str(e)
                    perm_pipe.results.save()
                    print('Failed permutation ' + str(perm_run) + ' ...')
            finally:
                e = None
                del e

        return perm_run

    @staticmethod
    def _calculate_results(permutation_id, metrics, save_to_db=True):
        try:
            mother_permutation = MDBHyperpipe.objects.raw({'permutation_id':PermutationTest.get_mother_permutation_id(permutation_id),  'computation_completed':True}).first()
        except DoesNotExist:
            return (None, None)
        else:
            all_permutations = MDBHyperpipe.objects.raw({'permutation_id':permutation_id,  'computation_completed':True})
            number_of_permutations = all_permutations.count()
            if number_of_permutations == 0:
                number_of_permutations = 1
            else:
                n_outer_folds = len(mother_permutation.outer_folds)
                true_performance = dict()
                for _, metric in metrics.items():
                    performance = list()
                    for fold in range(n_outer_folds):
                        performance.append(mother_permutation.outer_folds[fold].best_config.inner_folds[(-1)].validation.metrics[metric['name']])

                    true_performance[metric['name']] = np.mean(performance)

                perm_performances_global = list()
                for index, perm_pipe in enumerate(all_permutations):
                    try:
                        n_outer_folds = len(perm_pipe.outer_folds)
                        perm_performances = dict()
                        for _, metric in metrics.items():
                            performance = list()
                            for fold in range(n_outer_folds):
                                performance.append(perm_pipe.outer_folds[fold].best_config.inner_folds[(-1)].validation.metrics[metric['name']])

                            perm_performances[metric['name']] = np.mean(performance)

                        perm_performances['ind_perm'] = index
                        perm_performances_global.append(perm_performances)
                    except Exception as e:
                        try:
                            logger.error('Dismissed one permutation from calculation:')
                            logger.error(e)
                        finally:
                            e = None
                            del e

                perm_perf_metrics = dict()
                for _, metric in metrics.items():
                    perms = list()
                    for i in range(len(perm_performances_global)):
                        perms.append(perm_performances_global[i][metric['name']])

                    perm_perf_metrics[metric['name']] = perms

                p = PermutationTest.calculate_p(true_performance=true_performance, perm_performances=perm_perf_metrics, metrics=metrics,
                  n_perms=number_of_permutations)
                p_text = dict()
                for _, metric in metrics.items():
                    if p[metric['name']] == 0:
                        p_text[metric['name']] = 'p < {}'.format(str(1 / number_of_permutations))
                    else:
                        p_text[metric['name']] = 'p = {}'.format(p[metric['name']])

                logger.clean_info('\n            Done with permutations...\n    \n            Results Permutation test\n            ===============================================\n            ')
                for _, metric in metrics.items():
                    logger.clean_info('\n                    Metric: {}\n                    True Performance: {}\n                    p Value: {}\n    \n                '.format(metric['name'], true_performance[metric['name']], p_text[metric['name']]))

                if save_to_db:
                    if mother_permutation.permutation_test is None:
                        perm_results = MDBPermutationResults(n_perms=number_of_permutations)
                    else:
                        perm_results = mother_permutation.permutation_test
                    perm_results.n_perms_done = number_of_permutations
                    results_all_metrics = list()
                    for _, metric in metrics.items():
                        perm_metrics = MDBPermutationMetrics(metric_name=(metric['name']), p_value=(p[metric['name']]), metric_value=(true_performance[metric['name']]))
                        perm_metrics.values_permutations = perm_perf_metrics[metric['name']]
                        results_all_metrics.append(perm_metrics)

                    perm_results.metrics = results_all_metrics
                    mother_permutation.permutation_test = perm_results
                    mother_permutation.save()
                if mother_permutation.permutation_test is not None:
                    n_perms = mother_permutation.permutation_test.n_perms
                else:
                    n_perms = 1000
            result = PermutationTest.PermutationResult(true_performance, perm_perf_metrics, p, number_of_permutations, n_perms)
            return result

    class PermutationResult:

        def __init__(self, true_performances: dict={}, perm_performances: dict={}, p_values: dict={}, n_perms_done: int=0, n_perms: int=0):
            self.true_performances = true_performances
            self.perm_performances = perm_performances
            self.p_values = p_values
            self.n_perms_done = n_perms_done
            self.n_perms = n_perms

    @staticmethod
    def find_reference(mongo_db_connect_url, permutation_id, find_wizard_id=False):

        def _find_mummy(permutation_id):
            if not find_wizard_id:
                return MDBHyperpipe.objects.raw({'permutation_id':PermutationTest.get_mother_permutation_id(permutation_id), 
                 'computation_completed':True}).order_by([('computation_start_time', DESCENDING)]).first()
            return MDBHyperpipe.objects.raw({'wizard_object_id': permutation_id}).order_by([('computation_start_time', DESCENDING)]).first()

        try:
            connect(mongo_db_connect_url, alias='photon_core')
            mother_permutation = _find_mummy(permutation_id)
        except DoesNotExist:
            return
        except ConnectionError:
            connect(mongo_db_connect_url, alias='photon_core')
            try:
                mother_permutation = _find_mummy(permutation_id)
            except DoesNotExist:
                return

        return mother_permutation

    @staticmethod
    def get_permutation_status(permutation_id, mongo_db_connect_url='mongodb://trap-umbriel:27017/photon_results', save_to_db=False):
        mother_permutation = PermutationTest.find_reference(mongo_db_connect_url, permutation_id)
        if mother_permutation is not None:
            metric_list = list(set([m.metric_name for m in mother_permutation.metrics_test]))
            metric_dict = PermutationTest.manage_metrics(metric_list, None, mother_permutation.hyperpipe_info.best_config_metric)
            return PermutationTest._calculate_results(permutation_id, metric_dict, save_to_db)
        return

    @staticmethod
    def estimated_duration_per_permutation(permutation_id, mongo_db_connect_url='mongodb://trap-umbriel:27017/photon_results'):
        mother_permutation = PermutationTest.find_reference(mongo_db_connect_url, permutation_id)
        if mother_permutation is not None:
            return mother_permutation.computation_end_time - mother_permutation.computation_start_time
        return

    @staticmethod
    def validate_permutation_test_usability(wizard_id, mongo_db_connect_url='mongodb://trap-umbriel:27017/photon_results'):
        mother_permutation = PermutationTest.find_reference(mongo_db_connect_url, permutation_id=wizard_id, find_wizard_id=True)
        if mother_permutation is not None:
            if mother_permutation.dummy_estimator:
                best_config_metric = mother_permutation.hyperpipe_info.best_config_metric
                dummy_threshold_to_beat = [i.value for i in mother_permutation.dummy_estimator.test if i.metric_name == best_config_metric if i.operation == str(FoldOperations.MEAN)]
                if len(dummy_threshold_to_beat) > 0:
                    dummy_threshold_to_beat = dummy_threshold_to_beat[0]
                    if mother_permutation.hyperpipe_info.maximize_best_config_metric:
                        if mother_permutation.best_config.best_config_score.validation.metrics[best_config_metric] > dummy_threshold_to_beat:
                            return True
                        return False
                    else:
                        if mother_permutation.best_config.best_config_score.validation.metrics[best_config_metric] < dummy_threshold_to_beat:
                            return True
                        return False
        else:
            return

    @staticmethod
    def update_permutation_id(wizard_pipe_id, permutation_id, mongo_db_connect_url='mongodb://trap-umbriel:27017/photon_results'):
        reference_obj = PermutationTest.find_reference(mongo_db_connect_url, wizard_pipe_id, find_wizard_id=True)
        if reference_obj is not None:
            reference_obj.permutation_id = PermutationTest.get_mother_permutation_id(permutation_id)
            reference_obj.save()

    def collect_results(self, result):
        logger.info('Finished Permutation Run' + str(result))

    @staticmethod
    def calculate_p(true_performance, perm_performances, metrics, n_perms):
        p = dict()
        for _, metric in metrics.items():
            if metric['greater_is_better']:
                p[metric['name']] = np.sum(true_performance[metric['name']] < np.asarray(perm_performances[metric['name']])) / (n_perms + 1)
            else:
                p[metric['name']] = np.sum(true_performance[metric['name']] > np.asarray(perm_performances[metric['name']])) / (n_perms + 1)

        return p

    @staticmethod
    def set_greater_is_better(metric, last_element=None):
        """
        Set greater_is_better for metric
        :param string specifying metric
        """
        if metric == 'score':
            if last_element is not None:
                if hasattr(last_element.base_element, '_estimator_type'):
                    greater_is_better = True
            else:
                logger.error('NotImplementedError: No metric was chosen and last pipeline element does not specify whether it is a classifier, regressor, transformer or clusterer.')
                raise NotImplementedError('No metric was chosen and last pipeline element does not specify whether it is a classifier, regressor, transformer or clusterer.')
        else:
            greater_is_better = Scorer.greater_is_better_distinction(metric)
        return greater_is_better