# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/spatial_access/Models.py
# Compiled at: 2019-06-09 10:59:34
# Size of source mod 2**32: 29108 bytes
import pandas as pd
from spatial_access.BaseModel import ModelData
from spatial_access.SpatialAccessExceptions import UnrecognizedDecayFunctionException
from spatial_access.SpatialAccessExceptions import IncompleteCategoryDictException
from spatial_access.SpatialAccessExceptions import UnexpectedNormalizeTypeException
from spatial_access.SpatialAccessExceptions import UnexpectedNormalizeColumnsException
from spatial_access.SpatialAccessExceptions import UnexpectedEmptyColumnException
import math

def linear_decay_function(time, upper):
    """
    Linear decay function for distance
    """
    if time > upper:
        return 0
    else:
        return (upper - time) / upper


def root_decay_function(time, upper):
    """
    Square root decay function for distance.
    """
    if time > upper:
        return 0
    else:
        return 1 / math.sqrt(upper) * -time ** 0.5 + 1


def logit_decay_function(time, upper):
    """
    Logit distance decay function.
    """
    if time > upper:
        return 0
    else:
        return 1 - 1 / (math.exp(upper / 180 - 0.008 * time) + 1)


class Coverage(ModelData):
    __doc__ = '\n    Build Coverage which captures\n    the level of spending for low income residents in\n    urban environments.\n    '

    def __init__(self, network_type, sources_filename=None, source_column_names=None, destinations_filename=None, dest_column_names=None, transit_matrix_filename=None, categories=None, debug=False):
        """
        Args:
            network_type: string, one of {'walk', 'bike', 'drive', 'otp'}.
            sources_filename: string, csv filename.
            destinations_filename: string, csv filename.
            source_column_names: dictionary, map column names to expected values.
            dest_column_names: dictionary, map column names to expected values.
            debug: boolean, enable to see more detailed logging output.
            transit_matrix_filename: string, optional
        """
        super().__init__(network_type, sources_filename=sources_filename,
          source_column_names=source_column_names,
          destinations_filename=destinations_filename,
          dest_column_names=dest_column_names,
          debug=debug)
        self.load_transit_matrix(transit_matrix_filename)
        self.set_focus_categories(categories=categories)
        self._is_source = False
        self._result_column_names = {'service_pop', 'percap_spending'}

    def calculate(self, upper_threshold):
        """
        Args:
            upper_threshold: numeric, time in seconds.
        Calculate the per-capita values and served population for each destination record.

        Returns: DataFrame
        """
        self.calculate_sources_in_range(upper_threshold)
        results = {}
        for category in self.focus_categories:
            for dest_id in self.get_ids_for_category(category):
                population_in_range = self.get_population_in_range(dest_id)
                if population_in_range > 0:
                    percapita_spending = self.get_capacity(dest_id) / population_in_range
                else:
                    percapita_spending = 0
                results[dest_id] = [
                 population_in_range, percapita_spending, category]

        self.model_results = pd.DataFrame.from_dict(results, orient='index', columns=[
         'service_pop',
         'percap_spending',
         'category'])
        for column in self.model_results.columns:
            if 'service_pop' in column:
                self._aggregation_args[column] = 'sum'
            else:
                if 'percap_spending' in column:
                    self._aggregation_args[column] = 'mean'

        return self.model_results


class DestSum(ModelData):
    __doc__ = '\n    Build DestSum which captures the capacity\n    and capacity per capita of providers in a\n    community area.\n    '

    def __init__(self, network_type, sources_filename=None, source_column_names=None, destinations_filename=None, dest_column_names=None, categories=None, configs=None, debug=False):
        """
        Args:
            network_type: string, one of {'walk', 'bike', 'drive', 'otp'}.
            sources_filename: string, csv filename.
            destinations_filename: string, csv filename.
            source_column_names: dictionary, map column names to expected values.
            dest_column_names: dictionary, map column names to expected values.
            configs: defaults to None, else pass in an instance of Configs to override
                default values for p2p.
            debug: boolean, enable to see more detailed logging output.
        """
        super().__init__(network_type, sources_filename=sources_filename, source_column_names=source_column_names, destinations_filename=destinations_filename,
          dest_column_names=dest_column_names,
          configs=configs,
          debug=debug)
        self.reload_sources(sources_filename)
        self.reload_dests(destinations_filename)
        self.set_focus_categories(categories=categories)
        self._is_aggregatable = False
        self._is_source = False

    def calculate(self, shapefile='data/chicago_boundaries/chicago_boundaries.shp', spatial_index='community', projection='epsg:4326'):
        """
        Calculate the target/capacity per capita of providers in spatial areas.
        Args:
            shapefile: filename of shapefile
            spatial_index: index of geospatial area in shapefile
            projection: defaults to 'epsg:4326'

        Returns: data frame.
        """
        dests_copy = self.dests.copy(deep=True)
        capacity_col = dests_copy.columns.get_loc('capacity') + 1
        category_col = dests_copy.columns.get_loc('category') + 1
        for row in dests_copy.itertuples():
            dests_copy.loc[(row[0], row[category_col])] = row[capacity_col]
            dests_copy.loc[(row[0], 'all_categories')] = row[capacity_col]

        dest_aggregation_args = {key:'sum' for key in set(dests_copy['category'])}
        dest_aggregation_args['all_categories'] = 'sum'
        dests_copy.fillna(value=0, inplace=True)
        self._rejoin_results_with_coordinates(dests_copy, is_source=False)
        self._rejoin_results_with_coordinates((self.sources), is_source=True)
        aggregated_dests = self._build_aggregate(data_frame=dests_copy, shapefile=shapefile,
          spatial_index=spatial_index,
          projection=projection,
          aggregation_args=dest_aggregation_args)
        aggregated_sources = self._build_aggregate(data_frame=(self.sources), shapefile=shapefile,
          spatial_index=spatial_index,
          projection=projection,
          aggregation_args={'population': 'sum'})
        for column in aggregated_dests.columns:
            aggregated_dests[column + '_per_capita'] = aggregated_dests[column] / aggregated_sources['population']

        self.aggregated_results = aggregated_dests
        return self.aggregated_results


class TSFCA(ModelData):
    __doc__ = '\n    Build the TSFCA which quantifies\n    the per-resident spending for given categories.\n    '

    def __init__(self, network_type, sources_filename=None, source_column_names=None, destinations_filename=None, dest_column_names=None, transit_matrix_filename=None, categories=None, configs=None, debug=False):
        """
        Args:
            network_type: string, one of {'walk', 'bike', 'drive', 'otp'}.
            sources_filename: string, csv filename.
            destinations_filename: string, csv filename.
            source_column_names: dictionary, map column names to expected values.
            dest_column_names: dictionary, map column names to expected values.
            configs: defaults to None, else pass in an instance of Configs to override
                default values for p2p.
            debug: boolean, enable to see more detailed logging output.
            transit_matrix_filename: string, optional.
        """
        super().__init__(network_type=network_type, sources_filename=sources_filename,
          destinations_filename=destinations_filename,
          source_column_names=source_column_names,
          dest_column_names=dest_column_names,
          configs=configs,
          debug=debug)
        self.load_transit_matrix(transit_matrix_filename)
        self.set_focus_categories(categories=categories)
        self._result_column_names = {'percap_spend', 'total_spend'}

    def calculate(self, upper_threshold):
        """
        Args:
            upper_threshold: numeric, time in seconds.

        Returns: DataFrame
        """
        self.calculate_sources_in_range(upper_threshold)
        self.calculate_dests_in_range(upper_threshold)
        results = {}
        num_categories = len(self.focus_categories)
        for source_id in self.get_all_source_ids():
            results[source_id] = [
             0] * num_categories

        column_name_to_index = {}
        column_names = []
        for index, category in enumerate(self.focus_categories):
            column_names.append('percap_spend_' + category)
            column_name_to_index[category] = index

        dests_capacity = {}
        for category in self.focus_categories:
            for dest_id in self.get_ids_for_category(category):
                population_in_range = self.get_population_in_range(dest_id)
                if population_in_range > 0:
                    contribution_to_spending = self.get_capacity(dest_id) / population_in_range
                    dests_capacity[dest_id] = contribution_to_spending
                else:
                    dests_capacity[dest_id] = 0

        for source_id in self.get_all_source_ids():
            for dest_id in self.get_dests_in_range_of_source(source_id):
                category = self.get_category(dest_id)
                if category in self.focus_categories:
                    results[source_id][column_name_to_index[category]] += dests_capacity[dest_id]

        self.model_results = pd.DataFrame.from_dict(results, orient='index', columns=column_names)
        self.model_results['percap_spend_all_categories'] = self.model_results.sum(axis=1)
        for column in self.model_results.columns:
            if 'percap_spend' in column:
                self._aggregation_args[column] = 'mean'
            elif 'total_spend' in column:
                self._aggregation_args[column] = 'sum'

        return self.model_results


class AccessTime(ModelData):
    __doc__ = '\n    Measures the closest destination for each source per category.\n    '

    def __init__(self, network_type, sources_filename=None, source_column_names=None, destinations_filename=None, dest_column_names=None, transit_matrix_filename=None, categories=None, configs=None, debug=False):
        """
        Args:
            network_type: string, one of {'walk', 'bike', 'drive', 'otp'}.
            sources_filename: string, csv filename.
            destinations_filename: string, csv filename.
            source_column_names: dictionary, map column names to expected values.
            dest_column_names: dictionary, map column names to expected values.
            configs: defaults to None, else pass in an instance of Configs to override
                default values for p2p.
            debug: boolean, enable to see more detailed logging output.
            transit_matrix_filename: string, optional.
        """
        super().__init__(network_type=network_type, sources_filename=sources_filename,
          destinations_filename=destinations_filename,
          source_column_names=source_column_names,
          dest_column_names=dest_column_names,
          configs=configs,
          debug=debug)
        self.load_transit_matrix(transit_matrix_filename)
        self.set_focus_categories(categories=categories)
        self._requires_user_aggregation_type = True
        self._map_categories_to_sp_matrix()

    def calculate(self):
        """
        Returns: DataFrame
        """
        results = {}
        focus_categories_list = list(self.focus_categories)
        column_names = ['time_to_nearest_' + category for category in focus_categories_list]
        for source_id in self.get_all_source_ids():
            results[source_id] = []
            for category in focus_categories_list:
                time_to_nearest_neighbor = self.time_to_nearest_dest(source_id, category)
                results[source_id].append(time_to_nearest_neighbor)

        self.model_results = pd.DataFrame.from_dict(results, orient='index', columns=column_names)
        self.model_results['time_to_nearest_all_categories'] = self.model_results.min(axis=1)
        return self.model_results


class AccessCount(ModelData):
    __doc__ = '\n    Measures the number of destinations in range\n    for each source per category.\n    '

    def __init__(self, network_type, sources_filename=None, source_column_names=None, destinations_filename=None, dest_column_names=None, transit_matrix_filename=None, categories=None, configs=None, debug=False):
        """
        Args:
            network_type: string, one of {'walk', 'bike', 'drive', 'otp'}.
            sources_filename: string, csv filename.
            destinations_filename: string, csv filename.
            source_column_names: dictionary, map column names to expected values.
            dest_column_names: dictionary, map column names to expected values.
            configs: defaults to None, else pass in an instance of Configs to override
                default values for p2p.
            debug: boolean, enable to see more detailed logging output.
            transit_matrix_filename: string, optional.
        """
        super().__init__(network_type=network_type, sources_filename=sources_filename,
          destinations_filename=destinations_filename,
          source_column_names=source_column_names,
          dest_column_names=dest_column_names,
          configs=configs,
          debug=debug)
        self.load_transit_matrix(transit_matrix_filename)
        self.set_focus_categories(categories=categories)
        self._map_categories_to_sp_matrix()
        self._result_column_names = 'count_in_range'

    def calculate(self, upper_threshold):
        """
        Args:
            upper_threshold: numeric, time in seconds.

        Returns: DataFrame
        """
        results = {}
        focus_categories_list = list(self.focus_categories)
        column_names = ['count_in_range_' + category for category in focus_categories_list]
        self.calculate_dests_in_range(upper_threshold)
        for source_id in self.get_all_source_ids():
            results[source_id] = []
            for category in focus_categories_list:
                count_in_range = self.count_dests_in_range_by_categories(source_id=source_id, category=category,
                  upper_threshold=upper_threshold)
                results[source_id].append(count_in_range)

        self.model_results = pd.DataFrame.from_dict(results, orient='index', columns=column_names)
        self.model_results['count_in_range_all_categories'] = self.model_results.sum(axis=1)
        for column in self.model_results.columns:
            self._aggregation_args[column] = 'mean'

        return self.model_results


class AccessSum(ModelData):
    __doc__ = '\n    Measures the capacity of providers in range\n    for each source per category.\n    '

    def __init__(self, network_type, sources_filename=None, source_column_names=None, destinations_filename=None, dest_column_names=None, transit_matrix_filename=None, categories=None, configs=None, debug=False):
        """
        Args:
            network_type: string, one of {'walk', 'bike', 'drive', 'otp'}.
            sources_filename: string, csv filename.
            destinations_filename: string, csv filename.
            source_column_names: dictionary, map column names to expected values.
            dest_column_names: dictionary, map column names to expected values.
            configs: defaults to None, else pass in an instance of Configs to override
                default values for p2p.
            debug: boolean, enable to see more detailed logging output.
            transit_matrix_filename: string, optional.
        """
        super().__init__(network_type=network_type, sources_filename=sources_filename,
          destinations_filename=destinations_filename,
          source_column_names=source_column_names,
          dest_column_names=dest_column_names,
          configs=configs,
          debug=debug)
        self.load_transit_matrix(transit_matrix_filename)
        self.set_focus_categories(categories=categories)
        self._map_categories_to_sp_matrix()
        self._result_column_names = 'sum_in_range'

    def calculate(self, upper_threshold):
        """
        Args:
            upper_threshold: numeric, time in seconds.

        Returns: DataFrame
        """
        results = {}
        focus_categories_list = list(self.focus_categories)
        column_names = ['sum_in_range_' + category for category in focus_categories_list]
        self.calculate_dests_in_range(upper_threshold)
        for source_id in self.get_all_source_ids():
            results[source_id] = []
            for category in focus_categories_list:
                sum_in_range = self.count_sum_in_range_by_categories(source_id, category)
                results[source_id].append(sum_in_range)

        self.model_results = pd.DataFrame.from_dict(results, orient='index', columns=column_names)
        self.model_results['sum_in_range_all_categories'] = self.model_results.sum(axis=1)
        for column in self.model_results.columns:
            self._aggregation_args[column] = 'mean'

        return self.model_results


class AccessModel(ModelData):
    __doc__ = '\n    Build the Access model which captures the accessibility of \n    nonprofit services in urban environments.\n    '

    def __init__(self, network_type, sources_filename=None, source_column_names=None, destinations_filename=None, dest_column_names=None, transit_matrix_filename=None, decay_function='linear', configs=None, debug=False):
        """
        Args:
            network_type: string, one of {'walk', 'bike', 'drive', 'otp'}.
            sources_filename: string, csv filename.
            destinations_filename: string, csv filename.
            source_column_names: dictionary, map column names to expected values.
            dest_column_names: dictionary, map column names to expected values.
            configs: defaults to None, else pass in an instance of Configs to override
                default values for p2p.
            debug: boolean, enable to see more detailed logging output.
            decay_function: lambda or string
            transit_matrix_filename: string, optional
        """
        self.decay_function = None
        self.set_decay_function(decay_function)
        super().__init__(network_type=network_type, sources_filename=sources_filename,
          destinations_filename=destinations_filename,
          source_column_names=source_column_names,
          dest_column_names=dest_column_names,
          configs=configs,
          debug=debug)
        self.load_transit_matrix(transit_matrix_filename)
        self._result_column_names = 'score'

    def set_decay_function(self, decay_function):
        """
        Args:
            decay_function: 'linear', 'root', 'logit', or a lambda of
            the form f(x, y) -> z. Range should be the nonnegative
            integer space.

        Raises:
            UnrecognizedDecayFunctionException: Illegal decay function.
        """
        if isinstance(decay_function, str):
            if decay_function == 'linear':
                self.decay_function = linear_decay_function
            else:
                if decay_function == 'root':
                    self.decay_function = root_decay_function
                else:
                    if decay_function == 'logit':
                        self.decay_function = logit_decay_function
                    else:
                        raise UnrecognizedDecayFunctionException(decay_function)
        else:
            if isinstance(decay_function, type(lambda : x)):
                try:
                    x = decay_function(1, 2)
                    if not isinstance(x, int):
                        if not isinstance(x, float):
                            raise AssertionError
                except (TypeError, AssertionError):
                    raise UnrecognizedDecayFunctionException('lambda sbould have form:f(x, y) -> z')

                self.decay_function = decay_function
            else:
                message = "Decay function should be either a string: ['linear', 'root', 'logit'], or a lamda"
                raise UnrecognizedDecayFunctionException(message)

    @staticmethod
    def _test_category_weight_dict(category_weight_dict):
        """
        Ensure category_weight_dict has the expected form.
        Args:
            category_weight_dict: dictionary of {category : [numeric weights]}
        Raises:
            IncompleteCategoryDictException: category_weight_dict does
                not have the expected format.
        """
        if not isinstance(category_weight_dict, dict):
            raise IncompleteCategoryDictException('category_weight_dict should be a dictionary or None')
        for value in category_weight_dict.values():
            if not isinstance(value, list):
                raise IncompleteCategoryDictException('category_weight_dict values should be arrays')

    def _log_category_weight_dict(self, category_weight_dict):
        """
        Log the category_weight_dict in a useful format.
        Args:
            category_weight_dict: dictionary of arrays.
        """
        presented_weight_dict = {key:'No decay' for key in self.all_categories}
        presented_weight_dict = {**presented_weight_dict, **category_weight_dict}
        self.logger.info('Using weights: {}'.format(presented_weight_dict))

    def calculate(self, upper_threshold, category_weight_dict=None, normalize=False, normalize_type='minmax'):
        """
        Args:
            category_weight_dict: category_weight_dict: dictionary of {category : [numeric weights]} or None
            upper_threshold: time in seconds.
            normalize: boolean. If true, results will be normalized
                from 0 to 100.
            normalize_type: 'z_score', 'minmax'
        Returns: DataFrame.
        Raises:
            UnexpectedNormalizeColumnsException
        """
        if category_weight_dict is None:
            category_weight_dict = {}
        else:
            self._test_category_weight_dict(category_weight_dict)
        max_category_occurances = {category:len(weights) for category, weights in category_weight_dict.items()}
        category_weight_dict = {category:sorted(weights, reverse=True) for category, weights in category_weight_dict.items()}
        self._log_category_weight_dict(category_weight_dict)
        num_columns = len(self.all_categories) + 1
        results = {source_id:[0] * num_columns for source_id in self.get_all_source_ids()}
        category_to_index_map = {}
        column_names = [
         'all_categories_score']
        index = 1
        for category in self.all_categories:
            column_names.append(category + '_score')
            category_to_index_map[category] = index
            index += 1

        for source_id in self.get_all_source_ids():
            category_encounters = {category:0 for category in self.all_categories}
            for dest_id, time in self.get_values_by_source(source_id, sort=True):
                decayed_time = self.decay_function(time, upper_threshold)
                category = self.get_category(dest_id)
                category_occurances = category_encounters[category]
                if category not in category_weight_dict:
                    results[source_id][0] += decayed_time
                    results[source_id][category_to_index_map[category]] += decayed_time
                elif category_occurances < max_category_occurances[category]:
                    decayed_category_weight = category_weight_dict[category][category_occurances]
                    category_encounters[category] += 1
                    score_contribution = decayed_time * decayed_category_weight
                    results[source_id][0] += score_contribution
                    results[source_id][category_to_index_map[category]] += score_contribution
                else:
                    continue

        self.model_results = pd.DataFrame.from_dict(results, orient='index', columns=column_names)
        if isinstance(normalize, list):
            for column in normalize:
                column_key = column + '_score'
                self._normalize(column_key, normalize_type)

        else:
            if normalize is True:
                for column in self.model_results.columns:
                    self._normalize(column, normalize_type)

            else:
                if normalize is False:
                    pass
                else:
                    raise UnexpectedNormalizeColumnsException('Argument ({}) is not of expected type: boolean, list'.format(normalize))
        for column in self.model_results.columns:
            self._aggregation_args[column] = 'mean'

        return self.model_results

    def _normalize(self, column, normalize_type):
        """
        Normalize results.
        Args:
            column: which column to normalize.
            normalize_type: 'z-score', 'minmax'

        Raises:
            UnexpectedEmptyColumnException
            UnexpectedNormalizeTypeException
        """
        if normalize_type == 'z_score':
            try:
                self.model_results[column] = (self.model_results[column] - self.model_results[column].mean()) / self.model_results[column].std()
            except ZeroDivisionError:
                raise UnexpectedEmptyColumnException(column)

        else:
            if normalize_type == 'minmax':
                try:
                    normalize_factor = self.model_results[column].max() - self.model_results[column].min()
                except ZeroDivisionError:
                    raise RuntimeError('column max == column min ({})'.format(self.model_results[column].max()))

                self.model_results[column] = (self.model_results[column] - self.model_results[column].min()) / normalize_factor
            else:
                raise UnexpectedNormalizeTypeException(normalize_type)