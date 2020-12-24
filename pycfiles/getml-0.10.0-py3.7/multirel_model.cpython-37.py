# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/getml/models/multirel_model.py
# Compiled at: 2020-03-16 07:21:38
# Size of source mod 2**32: 104655 bytes
import datetime, json, numbers, time, socket, numpy as np, pandas as pd
from getml import data, engine, predictors
from getml.data import Placeholder, _decode_placeholder, _decode_joined_tables
import getml.communication as comm
from getml.predictors import _Predictor
from .modutils import _make_random_name, _print_time_taken
from .loss_functions import _decode_loss_function, _LossFunction, SquareLoss
from .list_models import list_models
from .validation import _validate_multirel_model_parameters
from .aggregations import Avg, Count, Max, Min, Sum

class MultirelModel(object):
    __doc__ = 'Feature engineering based on Multi-Relational Decision Tree Learning.\n\n    :class:`~getml.models.MultirelModel` automates feature engineering\n    for relational data and time series. It is based on an efficient\n    variation of the Multi-Relational Decision Tree Learning (MRDTL)\n    algorithm and uses the getML Multirel algorithm.\n\n    For more information on the underlying feature engineering algorithm, check\n    out the :ref:`User guide <feature_engineering_algorithms_multirel>`.  For\n    details about the :class:`~getml.models.MultirelModel` container in\n    general, see the documentation of the :mod:`~getml.models` module.\n\n    Examples:\n        A :class:`~getml.models.MultirelModel` can be created in two\n        different ways. The first one is to directly use the \n        constructor:\n\n        .. code-block:: python\n\n            population_table, peripheral_table = getml.datasets.make_numerical()\n\n            population_placeholder = population_table.to_placeholder()\n            peripheral_placeholder = peripheral_table.to_placeholder()\n\n            population_placeholder.join(peripheral_placeholder,\n                                        join_key="join_key",\n                                        time_stamp="time_stamp"\n            )\n\n            model = getml.models.MultirelModel(\n                population=population_placeholder,\n                peripheral=peripheral_placeholder,\n                name="multirel",\n                aggregation=[\n                    getml.models.aggregations.Count,\n                    getml.models.aggregations.Sum\n                ],\n                predictor=getml.predictors.LinearRegression()\n            )\n\n        This creates a handler in the Python\n        API. To construct the actual model in the getML engine, the\n        information in the handler has to be sent to the engine:\n\n        .. code-block:: python\n\n            model.send()\n\n        You can also call the\n        :func:`~getml.models.MultirelModel` constructor with the\n        `send` argument set to True.\n\n        The second way of obtaining a\n        :class:`~getml.models.MultirelModel` handler to a model is to\n        use :func:`~getml.models.load_model`:\n\n        .. code-block:: python\n\n            model_loaded = getml.models.load_model("model-name")\n\n    Args:\n        population (:class:`~getml.data.Placeholder`):\n\n            Abstract representation of the main table.\n\n        peripheral (Union[:class:`~getml.data.Placeholder`, List[:class:`~getml.data.Placeholder`]]): \n\n            Abstract representations of the additional tables used to\n            augment the information provided in `population`. These\n            have to be the same objects that got\n            :meth:`~getml.data.Placeholder.join` on the\n            `population` :class:`~getml.data.Placeholder` and\n            their order strictly determines the order of the\n            peripheral :class:`~getml.data.DataFrame` provided in\n            the \'peripheral_tables\' argument of\n            :meth:`~getml.models.MultirelModel.fit`,\n            :meth:`~getml.models.MultirelModel.predict`,\n            :meth:`~getml.models.MultirelModel.score`, and\n            :meth:`~getml.models.MultirelModel.transform`.\n\n        name (str, optional):\n\n            Unique name of the container created in the getML\n            engine. If an empty string is provided, a random value\n            based on the current time stamp will be used.\n\n        feature_selector (:class:`~getml.predictors`, optional):\n\n            Predictor used to selected the best features among all\n            automatically generated ones.\n\n        predictor (:class:`~getml.predictors`, optional):\n\n            Predictor used to make predictions on new, unseen data.\n\n        units (dict, optional):\n\n            DEPRECATED: only required when a\n            :py:class:`pandas.DataFrame` is provided in the\n            :meth:`~getml.models.MultirelModel.fit`,\n            :meth:`~getml.models.MultirelModel.predict`,\n            :meth:`~getml.models.MultirelModel.score`, and\n            :meth:`~getml.models.MultirelModel.transform` method. If\n            you already uploaded your data to the getML engine, this\n            argument will not have any effect and can be omitted.\n\n        session_name (string, optional):\n\n            Determines whether which :mod:`~getml.hyperopt` run the\n            model was created in or - in case of an empty string - if\n            it\'s a stand-alone one.\n\n        aggregation (List[:class:`~getml.models.aggregations`], optional):\n\n            Mathematical operations used by the automated feature\n            engineering algorithm to create new features. \n\n            Possible options:\n\n                * :const:`~getml.models.aggregations.Avg`\n                * :const:`~getml.models.aggregations.Count`\n                * :const:`~getml.models.aggregations.CountDistinct`\n                * :const:`~getml.models.aggregations.CountMinusCountDistinct`\n                * :const:`~getml.models.aggregations.Max`\n                * :const:`~getml.models.aggregations.Median`\n                * :const:`~getml.models.aggregations.Min`\n                * :const:`~getml.models.aggregations.Stddev`\n                * :const:`~getml.models.aggregations.Sum`\n                * :const:`~getml.models.aggregations.Var`\n\n        allow_sets (bool, optional):\n\n            Multirel can summarize different categories into sets for\n            producing conditions. When expressed as SQL statements these \n            sets might look like this:\n\n            .. code-block:: sql\n\n                t2.category IN ( \'value_1\', \'value_2\', ... )\n\n            This can be very powerful, but it can also produce\n            features that are hard to read and might be prone to\n            overfitting when the `sampling_factor` is too low.\n\n        delta_t (float, optional):\n\n            Frequency with which lag variables will be explored in a\n            time series setting. When set to 0.0, there will be no lag\n            variables.\n\n            Please note that getML does not handle UNIX time stamps,\n            but encodes time as multiples and fractions of\n            days since the 01.01.1970 (1970-01-01T00:00:00). For\n            example :math:`7.334722222222222 = 7 + 6/24 + 2/(24*60)`\n            would be interpreted 1970-01-08T06:02:00.\n\n            For more information see\n            :ref:`data_model_time_series`. Range: [0, :math:`\\infty`]\n\n        grid_factor (float, optional):\n\n            Multirel will try a grid of critical values for your\n            numerical features. A higher `grid_factor` will lead to a\n            larger number of critical values being considered. This\n            can increase the training time, but also lead to more\n            accurate features. Range: (0, :math:`\\infty`]\n\n        include_categorical (bool, optional):\n\n            Whether you want to pass categorical columns from the\n            population table to the `feature_selector` and\n            `predictor`. Passing columns directly allows you to include\n            handcrafted feature as well as raw data. Note, however,\n            that this does not guarantee their presence in the\n            resulting features because it is the task of the\n            `feature_selector` to pick only the best performing\n            ones.\n\n        loss_function (:class:`~getml.models.loss_functions`, optional):\n\n            Objective function used by the feature engineering algorithm\n            to optimize your features. For regression problems use\n            :class:`~getml.models.loss_functions.SquareLoss` and for\n            classification problems use\n            :class:`~getml.models.loss_functions.CrossEntropyLoss`.\n\n        max_length (int, optional):\n\n            The maximum length a subcondition might have. Multirel\n            will create conditions in the form\n\n            .. code-block:: sql\n\n                (condition 1.1 AND condition 1.2 AND condition 1.3 )\n                OR ( condition 2.1 AND condition 2.2 AND condition 2.3 )\n                ...\n\n            Using this parameter you can set the maximum number of\n            conditions allowed in the brackets. Range: [0,\n            :math:`\\infty`]\n\n        min_num_samples (int, optional):\n\n            Determines the minimum number of samples a subcondition\n            should apply to in order for it to be considered. Higher\n            values lead to less complex statements and less danger of\n            overfitting. Range: [1, :math:`\\infty`]\n\n        num_features (int, optional):\n\n            Number of features generated by the feature engineering \n            algorithm. For the total number of features\n            available `share_selected_features` has to be taken into\n            account as well. Range: [1, :math:`\\infty`]\n\n        num_subfeatures (int, optional):\n\n            The number of subfeatures you would like to extract in a\n            subensemble (for snowflake data model only). See\n            :ref:`data_model_snowflake_schema` for more\n            information. Range: [1, :math:`\\infty`]\n\n        num_threads (int, optional):\n\n            Number of threads used by the feature engineering algorithm. If set to\n            zero or a negative value, the number of threads will be\n            determined automatically by the getML engine. Range:\n            [-:math:`\\infty`, :math:`\\infty`]\n\n        regularization (float, optional):\n\n            Most important regularization parameter for the quality of\n            the features produced by Multirel. Higher values will lead\n            to less complex features and less danger of overfitting. A\n            `regularization` of 1.0 is very strong and allows no\n            conditions. Range: [0, 1]\n\n        round_robin (bool, optional):\n\n            If True, the Multirel picks a different `aggregation`\n            every time a new feature is generated.\n\n        sampling_factor (float, optional):\n\n            Multirel uses a bootstrapping procedure (sampling with\n            replacement) to train each of the features. The sampling\n            factor is proportional to the share of the samples\n            randomly drawn from the population table every time\n            Multirel generates a new feature. A lower sampling factor\n            (but still greater than 0.0), will lead to less danger of\n            overfitting, less complex statements and faster\n            training. When set to 1.0, roughly 2,000 samples are drawn\n            from the population table. If the population table\n            contains less than 2,000 samples, it will use standard\n            bagging. When set to 0.0, there will be no sampling at\n            all. Range: [0, :math:`\\infty`]\n\n        seed (Union[int,None], optional):\n\n            Seed used for the random number generator that underlies\n            the sampling procedure to make the calculation\n            reproducible. Due to nature of the underlying algorithm\n            this is only the case if the fit is done without\n            multithreading. To reflect this, a `seed` of None does\n            represent an unreproducible and is only allowed to be set\n            to an actual integer if both `num_threads` and ``n_jobs``\n            instance variables of the `predictor` and\n            `feature_selector` - if they are instances of either\n            :class:`~getml.predictors.XGBoostRegressor` or\n            :class:`~getml.predictors.XGBoostClassifier` - are set to\n            1. Internally, a `seed` of None will be mapped to\n            5543. Range: [0, :math:`\\infty`]\n\n        send (bool, optional):\n\n            If True, the Model will be automatically sent to the getML\n            engine without you having to explicitly call\n            :meth:`~getml.models.MultirelModel.send`.\n\n        share_aggregations (float, optional):\n\n            Every time a new feature is generated, the `aggregation`\n            will be taken from a random subsample of possible\n            aggregations and values to be aggregated. This parameter\n            determines the size of that subsample. Only relevant when\n            `round_robin` is False. Range: (0, 1]\n\n        share_conditions (float, optional):\n\n            Every time a new column is tested for applying conditions,\n            it might be skipped at random. This parameter determines\n            the probability that a column will *not* be\n            skipped. Range: [0, 1]\n\n        share_selected_features (float, optional):\n\n            Percentage of features selected by the\n            `feature_selector`. Any feature with a importance of zero\n            will be removed. Therefore, the number of features\n            actually selected can be smaller than `num_features` *\n            `share_selected_features`.  When set to 0.0, no feature\n            selection will be conducted and all generated ones will\n            provided in :meth:`~getml.models.MultirelModel.transform`\n            and used in\n            :meth:`~getml.models.MultirelModel.predict`. Range: [0, 1]\n\n        shrinkage (float, optional):\n\n            Since Multirel works using a gradient-boosting-like\n            algorithm, `shrinkage` (or learning rate) scales down the\n            weights and thus the impact of each new tree. This gives\n            more room for future ones to improve the overall\n            performance of the model in this greedy algorithm. Higher\n            values will lead to more danger of overfitting. Range: [0,\n            1]\n\n        silent (bool, optional):\n\n            Controls the logging during training.\n\n        use_timestamps (bool, optional):\n\n            Whether you want to ignore all elements in the peripheral\n            tables where the time stamp is greater than the one in the\n            corresponding elements of the population table. In other\n            words, this determines whether you want add the condition\n\n            .. code-block:: sql\n\n                t2.time_stamp <= t1.time_stamp\n\n            at the very end of each feature. It is strongly recommend\n            to enable this behavior.\n\n        Raises:\n            TypeError:\n                If any of the input arguments is of wrong type.\n            KeyError: \n                If an unsupported instance variable is encountered\n                (via :meth:`~getml.models.MultirelModel.validate`).\n            TypeError: \n                If any instance variable is of wrong type (via\n                :meth:`~getml.models.MultirelModel.validate`).\n            ValueError:\n                If any instance variable does not match its possible\n                choices (string) or is out of the expected bounds\n                (numerical) (via\n                :meth:`~getml.models.MultirelModel.validate`).\n\n    '

    def __init__(self, population, peripheral, name='', feature_selector=None, predictor=None, units=dict(), session_name='', aggregation=[
 Avg, Count, Max, Min, Sum], allow_sets=True, delta_t=0.0, grid_factor=1.0, include_categorical=False, loss_function=SquareLoss(), max_length=4, min_num_samples=1, num_features=100, num_subfeatures=100, num_threads=0, regularization=0.0, round_robin=False, sampling_factor=1.0, seed=None, send=False, share_aggregations=0.25, share_conditions=1.0, share_selected_features=0.0, shrinkage=0.0, silent=False, use_timestamps=True):
        if isinstance(peripheral, Placeholder):
            peripheral = [
             peripheral]
        if name == '':
            name = self._make_name()
        self.type = 'MultirelModel'
        self.aggregation = aggregation
        self.allow_sets = allow_sets
        self.delta_t = delta_t
        self.feature_selector = feature_selector
        self.grid_factor = grid_factor
        self.include_categorical = include_categorical
        self.loss_function = loss_function
        self.max_length = max_length
        self.min_num_samples = min_num_samples
        self.name = name
        self.num_features = num_features
        self.num_subfeatures = num_subfeatures
        self.num_threads = num_threads
        self.peripheral = peripheral
        self.population = population
        self.predictor = predictor
        self.regularization = regularization
        self.round_robin = round_robin
        self.sampling_factor = sampling_factor
        self.seed = seed
        self.session_name = session_name
        self.share_aggregations = share_aggregations
        self.share_conditions = share_conditions
        self.share_selected_features = share_selected_features
        self.shrinkage = shrinkage
        self.silent = silent
        self.units = units
        self.use_timestamps = use_timestamps
        self.validate()
        if send:
            self.send()

    def __eq__(self, other):
        """Compares the current instance of the
        :class:`~getml.models.MultirelModel` with another one.

        Args:
            other: Another :class:`~getml.models.MultirelModel` to
                compare the current instance against.

        Returns:
            bool: Whether the current instance and `other` share the
                same content.

        Raises:
            TypeError: If `other` is not of class
                :class:`~getml.models.MultirelModel`
        """
        if not isinstance(other, MultirelModel):
            raise TypeError('A MultirelModel can only be compared to another MultirelModel')
        if len(set(self.__dict__.keys())) != len(set(other.__dict__.keys())):
            return False
        for kkey in self.__dict__:
            if kkey not in other.__dict__:
                return False
            if isinstance(self.__dict__[kkey], numbers.Real):
                if not np.isclose(self.__dict__[kkey], other.__dict__[kkey]):
                    return False
                elif self.__dict__[kkey] != other.__dict__[kkey]:
                    return False

        return True

    def __repr__(self):
        return str(self)

    def __str__(self):
        result = ''
        indent1 = '  '
        indent2 = indent1 + indent1
        result += 'MultirelModel:'
        for kkey, vvalue in self.__dict__.items():
            if kkey == 'loss_function':
                result += '\n' + indent1 + kkey + ': ' + vvalue.type
            elif kkey == 'peripheral':
                if vvalue is not None:
                    result += '\n' + indent1 + 'peripheral (list):'
                    for pplaceholder in vvalue:
                        result += '\n' + indent2 + str(pplaceholder).replace('\n', '\n' + indent2)

                else:
                    result += '\n' + indent1 + 'peripheral: None'
            elif kkey == 'population':
                if vvalue is not None:
                    result += '\n' + indent1 + 'population (Placeholder):' + str(vvalue).lstrip('Placeholder:').replace('\n', '\n' + indent1)
                else:
                    result += '\n' + indent1 + 'population: None'
            elif kkey == 'predictor' or kkey == 'feature_selector':
                if vvalue is not None:
                    result += '\n' + indent1 + kkey + ': ' + str(vvalue).replace('\n', '\n' + indent1)
                else:
                    result += '\n' + indent1 + kkey + ': None'
            else:
                result += '\n' + indent1 + kkey + ': ' + str(vvalue)

        return result

    def _close(self, sock):
        """
        Raises:
            TypeError: If `sock` is not of type 
                :py:class:`socket.socket`
        """
        if type(sock) is not socket.socket:
            raise TypeError("'sock' must be a socket.")
        cmd = dict()
        cmd['type_'] = self.type + '.close'
        cmd['name_'] = self.name
        comm.send_string(sock, json.dumps(cmd))
        msg = comm.recv_string(sock)
        if msg != 'Success!':
            comm.engine_exception_handler(msg)

    def _convert_peripheral_tables(self, peripheral_tables, sock):
        """Converts a list of :class:`getml.data.DataFrame` and
        :class:`pandas.DataFrame` to a :class:`getml.data.DataFrame`
        only list.

        All occurrences of :class:`pandas.DataFrame` will be converted
        to :class:`getml.data.DataFrame`. In order to achieve this a
        new DataFrame will be constructed using the schema information
        of the `peripheral` tables stored in the current instance. The
        mapping which peripheral schema will be used for which element
        in `peripheral_tables` is determined by order. Therefore, the
        order of the peripheral tables supplied in `peripheral` upon
        construction :class:`~getml.models.MultirelModel` and supplied
        in `peripheral_tables` *must* be identically.

        Note that when converting a :class:`pandas.DataFrame` into a
        :class:`getml.data.DataFrame` the latter will be created on
        the engine first and all the data of the former will be
        uploaded into it afterwards. Thus, depending on the size of
        you tables, this step might take a while.

        Args:
            peripheral_tables (list): List of
                :class:`getml.data.DataFrame` or
                :class:`pandas.DataFrame`. Both classes can be
                arbitrarily mixed.
            sock (:py:class:`socket.socket`): Established
                communication to the getML engine used to upload
                create new data frames and upload data when converting
                a :class:`pandas.DataFrame` into a
                :class:`getml.data.DataFrame`.

        Raises:
            TypeError: If `peripheral_tables` is not a list of
                :class:`pandas.DataFrame` and
                :class:`getml.data.DataFrame` or `sock` is not of
                type :py:class:`socket.socket`.

        Returns:
            List: Version of `peripheral_tables` containing only
                :class:`getml.data.DataFrame` elements.

        """
        if isinstance(peripheral_tables, pd.DataFrame) or isinstance(peripheral_tables, data.DataFrame):
            peripheral_tables = [
             peripheral_tables]
        if not ((type(peripheral_tables) is not list or len(peripheral_tables)) > 0 and all([isinstance(ll, data.DataFrame) or isinstance(ll, pd.DataFrame) for ll in peripheral_tables])):
            raise TypeError("'peripheral_tables' must be a getml.data.DataFrame or pandas.DataFrame or a list of those.")
        if type(sock) is not socket.socket:
            raise TypeError("'sock' must be a socket.")
        peripheral_data_frames = []
        for ii, pperipheral_table in enumerate(peripheral_tables):
            if type(pperipheral_table) is data.DataFrame:
                peripheral_data_frames.append(pperipheral_table)
            elif type(pperipheral_table) is pd.DataFrame:
                categorical_peripheral = [per.categorical for per in self.peripheral]
                numerical_peripheral = [per.numerical for per in self.peripheral]
                join_keys_peripheral = [per.join_keys for per in self.peripheral]
                names_peripheral = [per.name for per in self.peripheral]
                time_stamps_peripheral = [per.time_stamps for per in self.peripheral]
                peripheral_data_frames.append(data.DataFrame(name=(_make_random_name()),
                  roles={'join_key':join_keys_peripheral[ii], 
                 'time_stamp':time_stamps_peripheral[ii], 
                 'categorical':categorical_peripheral[ii], 
                 'numerical':numerical_peripheral[ii], 
                 'target':[]}))
                peripheral_data_frames[ii]._send_pandas_df(data_frame=pperipheral_table,
                  sock=sock)
            else:
                raise TypeError('Unknown type of peripheral table' + str(ii) + '\n                    : [' + str(type(pperipheral_table)) + ' \n                    ]. Only getml.data.DataFrame and pandas.DataFrame \n                    are allowed!')

        for df in peripheral_data_frames:
            colnames = df.numerical_names
            colnames += df.categorical_names
            for cname in colnames:
                if cname in self.units:
                    unit = self.units[cname]
                    df._set_unit(cname, unit, sock)

        return peripheral_data_frames

    def _convert_population_table(self, population_table, targets, sock):
        """Ensures an input of either class :class:`getml.data.DataFrame` or
        :class:`pandas.DataFrame` will be a valid
        :class:`getml.data.DataFrame`.

        If `population_table` is a :class:`pandas.DataFrame` it will
        be converted to :class:`getml.data.DataFrame`. In order to
        achieve this a new DataFrame will be constructed using the
        schema information of the `population` tables stored in the
        current instance and the `targets` supplied as input argument.

        Note that when converting a :class:`pandas.DataFrame` into a
        :class:`getml.data.DataFrame` the latter will be created on
        the engine first and all the data of the former will be
        uploaded into it afterwards. Thus, depending on the size of
        you tables, this step might take a while.

        Args:
            population_table (:class:`getml.data.DataFrame` or
                :class:`pandas.DataFrame`): Table which' class should
                be ensured.
            targets (List[str]): List with the names of all columns
                considered the target variable. Depending on the
                context this function is called, e.g. within
                :method:`~getml.models.MultirelModel.fit` or
                :method:`~getml.models.MultirelModel.predict`, it will
                just correspond to the `targets` instance variable of
                the current instance's `population` or requires some
                more processing and checking.
            sock (:py:class:`socket.socket`): Established
                communication to the getML engine used to create new
                data frame and upload data when converting a
                :class:`pandas.DataFrame` into a
                :class:`getml.data.DataFrame`.

        Raises:
            TypeError: If any of the input arguments is not of the
                requested type.

        Returns:
            List: Version of `peripheral_tables` containing only
                :class:`getml.data.DataFrame` elements.

        """
        if not isinstance(population_table, data.DataFrame):
            if not isinstance(population_table, pd.DataFrame):
                raise TypeError("'population_table' must be a getml.data.DataFrame or pandas.data.DataFrame")
        elif not type(targets) is not list:
            if not len(targets) == 0:
                if not all([type(ll) is str for ll in targets]):
                    raise TypeError("'targets' must be an empty list or a list of str.")
            if type(sock) is not socket.socket:
                raise TypeError("'sock' must be a socket.")
            if type(population_table) == data.DataFrame:
                population_data_frame = population_table
        elif type(population_table) == pd.DataFrame:
            population_data_frame = data.DataFrame(name=(_make_random_name()),
              roles={'join_key':self.population.join_keys, 
             'time_stamp':self.population.time_stamps, 
             'categorical':self.population.categorical, 
             'numerical':self.population.numerical, 
             'target':targets})
            population_data_frame._send_pandas_df(data_frame=population_table,
              sock=sock)
        else:
            raise TypeError('Unknown type of population table: [\n                ' + str(type(population_table)) + '\n                ]. Only getml.data.DataFrame and \n                pandas.DataFrame are allowed!')
        colnames = population_data_frame.numerical_names
        colnames += population_data_frame.categorical_names
        for cname in colnames:
            if cname in self.units:
                unit = self.units[cname]
                population_data_frame._set_unit(cname, unit, sock)

        return population_data_frame

    def _make_name(self):
        return datetime.datetime.now().isoformat().split('.')[0].replace(':', '-') + '-multirel'

    def _save(self):
        """
        Saves the model as a JSON file.
        """
        cmd = dict()
        cmd['type_'] = self.type + '.save'
        cmd['name_'] = self.name
        comm.send(cmd)

    def _score(self, yhat, y):
        """
        Returns the score for a set of predictions.
        
        Args:
            yhat (numpy.ndarray): Predictions.
            y (numpy.ndarray): Targets.

        Raises:
            TypeError: If any of the input arguments is of wrong type.
        """
        if type(yhat) is not np.ndarray:
            raise TypeError("'yhat' must be a numpy.ndarray.")
        if type(y) is not np.ndarray:
            raise TypeError("'y' must be a numpy.ndarray.")
        cmd = dict()
        cmd['type_'] = self.type + '.score'
        cmd['name_'] = self.name
        s = comm.send_and_receive_socket(cmd)
        msg = comm.recv_string(s)
        if msg != 'Found!':
            s.close()
            comm.engine_exception_handler(msg)
        comm.send_matrix(s, yhat)
        comm.send_matrix(s, y)
        msg = comm.recv_string(s)
        if msg != 'Success!':
            s.close()
            comm.engine_exception_handler(msg)
        scores = comm.recv_string(s)
        s.close()
        return json.loads(scores)

    def _transform(self, peripheral_data_frames, population_data_frame, sock, score=False, predict=False, df_name='', table_name=''):
        """Returns the features learned by the model or writes them into a data base.

        Args:  
            population_table (:class:`getml.data.DataFrame`):
                Population table. Targets will be ignored.
            peripheral_tables (List[:class:`getml.data.DataFrame`]):
                Peripheral tables.
                The peripheral tables have to be passed in the exact same order as their
                corresponding placeholders!
            sock (:py:class:`socket.socket`): TCP socket used to
                communicate with the getML engine.
            score (bool, optional): Whether the engine should calculate the
                scores of the model based on the input data.
            predict (bool, optional): Whether the engine should transform the
                input data into features.
            df_name (str, optional):
                If not an empty string, the resulting features will be
                written into a newly created DataFrame, instead of returning
                them. 
            table_name (str, optional): If not an empty string, the resulting
                features will be written into the data base, instead
                of returning them. See :ref:`unified_import_interface` for further
                information.

        Raises:
            TypeError: If any of the input arguments is of wrong type.

        """
        if isinstance(peripheral_data_frames, data.DataFrame):
            peripheral_data_frames = [
             peripheral_data_frames]
        elif not type(peripheral_data_frames) is not list:
            if not (len(peripheral_data_frames) > 0 and all([isinstance(ll, data.DataFrame) for ll in peripheral_data_frames])):
                raise TypeError("'peripheral_data_frames' must be a getml.data.DataFrame or a list of those.")
            if not isinstance(population_data_frame, data.DataFrame):
                raise TypeError("'population_data_frame' must be a getml.data.DataFrame")
            if type(sock) is not socket.socket:
                raise TypeError("'sock' must be a socket.")
            if type(score) is not bool:
                raise TypeError("'score' must be of type bool")
            if type(predict) is not bool:
                raise TypeError("'predict' must be of type bool")
            if type(table_name) is not str:
                raise TypeError("'table_name' must be of type str")
            cmd = dict()
            cmd['type_'] = self.type + '.transform'
            cmd['name_'] = self.name
            cmd['score_'] = score
            cmd['predict_'] = predict
            cmd['peripheral_names_'] = [df.name for df in peripheral_data_frames]
            cmd['population_name_'] = population_data_frame.name
            cmd['df_name_'] = df_name
            cmd['table_name_'] = table_name
            comm.send_string(sock, json.dumps(cmd))
            msg = comm.recv_string(sock)
            if msg == 'Success!':
                if table_name == '' and df_name == '':
                    y_hat = comm.recv_matrix(sock)
            else:
                y_hat = None
        else:
            comm.engine_exception_handler(msg)
        return y_hat

    def copy(self, new_name=''):
        """Creates a copy of the model in the engine and returns its 
        handler.
        
        Since there can not be two models in the engine holding the
        same name, a `new_name` has to be assigned to the new
        one (which must not be present in the engine yet).

        Examples:

            A possible use case is to pick a particularly well-performing
            model, create a new one based on it, do a slight adjustment of
            its attributes, and fit it.

            .. code-block:: python

                model = getml.models.load_model("multirel")

                model_new = model.copy("model-new")
                model_new.regularization = 0.8

                model_new.send()

                model_new.fit(population_table, peripheral_table)

        Args:
            new_name (str, optional): Name of the new model. In case
                of an empty string, a new name will be generated 
                automatically.

        Raises:
            NameError: If there is already a model present in the
                engine carrying the name `new_name`.
            TypeError: If `new_name` is not of type str.
            KeyError: If an unsupported instance variable is
                encountered (via
                :meth:`~getml.models.MultirelModel.validate`).
            TypeError: If any instance variable is of wrong type (via
                :meth:`~getml.models.MultirelModel.validate`).
            ValueError: If any instance variable does not match its
                possible choices (string) or is out of the expected
                bounds (numerical) (via
                :meth:`~getml.models.MultirelModel.validate`).

        Returns:
            :class:`getml.models.MultirelModel`:
                The handler of the copied model.

        """
        if type(new_name) is not str:
            raise TypeError("'new_name' must be of type str")
        self.validate()
        if new_name == '':
            new_name = self._make_name()
        model_names_dict = list_models()
        model_names = model_names_dict['multirel_models'] + model_names_dict['relboost_models']
        if new_name in model_names:
            raise NameError("A model called '" + new_name + "' is already present in the engine.")
        cmd = dict()
        cmd['type_'] = self.type + '.copy'
        cmd['name_'] = new_name
        cmd['other_'] = self.name
        comm.send(cmd)
        new_model = MultirelModel(name=new_name,
          population=Placeholder(name='placebert'),
          peripheral=Placeholder(name='placebert')).refresh()
        return new_model

    def delete(self):
        """
        Deletes the underlying model from the engine.

        Raises:
            KeyError: If an unsupported instance variable is
                encountered (via
                :meth:`~getml.models.MultirelModel.validate`).
            TypeError: If any instance variable is of wrong type (via
                :meth:`~getml.models.MultirelModel.validate`).
            ValueError: If any instance variable does not match its
                possible choices (string) or is out of the expected
                bounds (numerical) (via
                :meth:`~getml.models.MultirelModel.validate`).

        Note:
            Caution: You can not undo this action!
        """
        self.validate()
        cmd = dict()
        cmd['type_'] = self.type + '.delete'
        cmd['name_'] = self.name
        cmd['mem_only_'] = False
        comm.send(cmd)

    def deploy(self, deploy):
        """Allows a fitted model to be addressable via an HTTP(S) request.
        See :ref:`deployment` for details.
        
        Args:
            deploy (bool): If :code:`True`, the deployment of the model
                will be triggered.

        Raises:
            TypeError: If `deploy` is not of type bool.
            KeyError: If an unsupported instance variable is
                encountered (via
                :meth:`~getml.models.MultirelModel.validate`).
            TypeError: If any instance variable is of wrong type (via
                :meth:`~getml.models.MultirelModel.validate`).
            ValueError: If any instance variable does not match its
                possible choices (string) or is out of the expected
                bounds (numerical) (via
                :meth:`~getml.models.MultirelModel.validate`).

        """
        if type(deploy) is not bool:
            raise TypeError("'deploy' must be of type bool")
        self.validate()
        cmd = dict()
        cmd['type_'] = self.type + '.deploy'
        cmd['name_'] = self.name
        cmd['deploy_'] = deploy
        comm.send(cmd)
        self._save()

    def fit(self, population_table, peripheral_tables):
        """Trains the feature engineering algorithm and all predictors on the 
        provided data.

        Both the ``feature_selector`` and ``predictor`` will be
        trained alongside the Multirel feature engineering algorithm if
        present.

        Examples:

            .. code-block:: python

                model.fit(
                    population_table = population_table, 
                    peripheral_tables = peripheral_table)

        Args:
            population_table (Union[:class:`pandas.DataFrame`, :class:`getml.data.DataFrame`]):
                Main table containing the target variable(s) and
                corresponding to the ``population``
                :class:`~getml.data.Placeholder` instance
                variable.
            peripheral_tables (Union[:class:`pandas.DataFrame`, :class:`getml.data.DataFrame`, List[:class:`pandas.DataFrame`],List[:class:`getml.data.DataFrame`]]):
                Additional tables corresponding to the ``peripheral``
                :class:`~getml.data.Placeholder` instance
                variable. They have to be provided in the exact same
                order as their corresponding placeholders! A single
                DataFrame will be wrapped into a list internally.

        Raises:
            IOError: If the model corresponding to the instance
                variable ``name`` could not be found on the engine or
                the model could not be fitted.
            KeyError: If an unsupported instance variable is
                encountered (via
                :meth:`~getml.models.MultirelModel.validate`).
            TypeError: If any instance variable is of wrong type (via
                :meth:`~getml.models.MultirelModel.validate`).
            ValueError: If any instance variable does not match its
                possible choices (string) or is out of the expected
                bounds (numerical) (via
                :meth:`~getml.models.MultirelModel.validate`).

        Note:

            This method will only work if there is a corresponding
            model in the getML engine. If you used the
            :class:`~getml.models.MultirelModel` constructor of the
            model in the Python API, be sure to use the
            :meth:`~getml.models.MultirelModel.send` method afterwards
            create its counterpart in the engine.

            All parameters customizing this process have been already
            supplied to the constructor and are assigned as instance
            variables. Any changes applied to them will only be
            respected if the :meth:`~getml.models.MultirelModel.send`
            method will be called on the modified version of the model
            first.

            If a `population_table` or `peripheral_tables` will be
            provided as :class:`pandas.DataFrame`, they will be
            converted to temporary :class:`getml.data.DataFrame`,
            uploaded to the engine, and discarded after the function
            call. Since `peripheral_tables` can very well be the same
            for the :meth:`~getml.models.MultirelModel.predict`,
            :meth:`~getml.models.MultirelModel.score`, and
            :meth:`~getml.models.MultirelModel.transform` methods,
            this way of interacting with the engine can be highly
            inefficient and is discouraged.
        """
        if isinstance(peripheral_tables, pd.DataFrame) or isinstance(peripheral_tables, data.DataFrame):
            peripheral_tables = [
             peripheral_tables]
        elif not isinstance(population_table, data.DataFrame):
            if not isinstance(population_table, pd.DataFrame):
                raise TypeError("'population_table' must be a getml.data.DataFrame or pandas.data.DataFrame")
        elif not type(peripheral_tables) is not list:
            if not (len(peripheral_tables) > 0 and all([isinstance(ll, data.DataFrame) or isinstance(ll, pd.DataFrame) for ll in peripheral_tables])):
                raise TypeError("'peripheral_tables' must be a getml.data.DataFrame or pandas.DataFrame or a list of those")
            self.send()
            cmd = dict()
            cmd['type_'] = self.type + '.fit'
            cmd['name_'] = self.name
            sock = comm.send_and_receive_socket(cmd)
            msg = comm.recv_string(sock)
            if msg != 'Found!':
                sock.close()
                comm.engine_exception_handler(msg)
            peripheral_data_frames = self._convert_peripheral_tables(peripheral_tables, sock)
            targets = self.population.targets
            population_data_frame = self._convert_population_table(population_table, targets, sock)
            cmd = dict()
            cmd['type_'] = self.type + '.fit'
            cmd['name_'] = self.name
            cmd['peripheral_names_'] = [df.name for df in peripheral_data_frames]
            cmd['population_name_'] = population_data_frame.name
            comm.send_string(sock, json.dumps(cmd))
            begin = time.time()
            print('Loaded data. Features are now being trained...')
            msg = comm.recv_string(sock)
            end = time.time()
            if 'Trained' in msg:
                print(msg)
                _print_time_taken(begin, end, 'Time taken: ')
                self._close(sock)
        elif 'has already been fitted' in msg:
            print(msg)
            print('')
        else:
            comm.engine_exception_handler(msg)
        sock.close()
        self._save()
        return self.refresh()

    def predict(self, population_table, peripheral_tables, table_name=''):
        """Forecasts on new, unseen data using the trained ``predictor``.

        Returns the predictions generated by the model based on
        `population_table` and `peripheral_tables` or writes them into
        a data base named `table_name`.

        Examples:

            .. code-block:: python

                model.predict(
                    population_table = population_table,
                    peripheral_tables = peripheral_table)

        Args:  
            population_table (Union[:class:`pandas.DataFrame`, :class:`getml.data.DataFrame`]):
                Main table corresponding to the ``population``
                :class:`~getml.data.Placeholder` instance
                variable. Its target variable(s) will be ignored.
            peripheral_tables (Union[:class:`pandas.DataFrame`, :class:`getml.data.DataFrame`, List[:class:`pandas.DataFrame`],List[:class:`getml.data.DataFrame`]]):
                Additional tables corresponding to the ``peripheral``
                :class:`~getml.data.Placeholder` instance
                variable. They have to be provided in the exact same
                order as their corresponding placeholders! A single
                DataFrame will be wrapped into a list internally.
            table_name (str, optional): 

                If not an empty string, the resulting predictions will
                be written into the :mod:`~getml.database` of the same
                name. See :ref:`unified_import_interface` for
                further information.

        Raises:
            IOError: If the model corresponding to the instance
                variable ``name`` could not be found on the engine or
                the model could not be fitted.
            TypeError: If any input argument is not of proper type.
            ValueError: If no valid ``predictor`` was set/is None.
            KeyError: If an unsupported instance variable is
                encountered (via
                :meth:`~getml.models.MultirelModel.validate`).
            TypeError: If any instance variable is of wrong type (via
                :meth:`~getml.models.MultirelModel.validate`).
            ValueError: If any instance variable does not match its
                possible choices (string) or is out of the expected
                bounds (numerical) (via
                :meth:`~getml.models.MultirelModel.validate`).

        Return:
            :class:`numpy.ndarray`:
                Resulting predictions provided in an array of the
                (number of rows in `population_table`, number of
                targets in `population_table`).

        Note:

            Only fitted models
            (:meth:`~getml.models.MultirelModel.fit`) can be used for
            prediction. In addition, a valid ``predictor`` must be
            trained as well.

            If a `population_table` or `peripheral_tables` will be
            provided as :class:`pandas.DataFrame`, they will be
            converted to temporary :class:`getml.data.DataFrame`,
            uploaded to the engine, and discarded after the function
            call. Since `peripheral_tables` can very well be the same
            for the :meth:`~getml.models.MultirelModel.predict`,
            :meth:`~getml.models.MultirelModel.score`, and
            :meth:`~getml.models.MultirelModel.transform` methods,
            this way of interacting with the engine can be highly
            inefficient and is discouraged.

        """
        if not isinstance(peripheral_tables, pd.DataFrame):
            if isinstance(peripheral_tables, data.DataFrame):
                peripheral_tables = [
                 peripheral_tables]
            if not isinstance(population_table, data.DataFrame):
                if not isinstance(population_table, pd.DataFrame):
                    raise TypeError("'population_table' must be a getml.data.DataFrame or pandas.data.DataFrame")
            if not ((type(peripheral_tables) is not list or len(peripheral_tables)) > 0 and all([isinstance(ll, data.DataFrame) or isinstance(ll, pd.DataFrame) for ll in peripheral_tables])):
                raise TypeError("'peripheral_tables' must be a getml.data.DataFrame or pandas.DataFrame or a list of those")
            if type(table_name) is not str:
                raise TypeError("'table_name' must be of type str")
        else:
            if not isinstance(self.predictor, _Predictor):
                raise ValueError("No 'predictor' set to perform the prediction.")
            self.validate()
            cmd = dict()
            cmd['type_'] = self.type + '.transform'
            cmd['name_'] = self.name
            cmd['http_request_'] = False
            sock = comm.send_and_receive_socket(cmd)
            msg = comm.recv_string(sock)
            if msg != 'Found!':
                sock.close()
                comm.engine_exception_handler(msg)
            peripheral_data_frames = self._convert_peripheral_tables(peripheral_tables, sock)
            if type(population_table) is data.DataFrame:
                targets = []
            else:
                targets = [elem for elem in self.population.targets if elem in population_table.columns]
        population_data_frame = self._convert_population_table(population_table, targets, sock)
        y_hat = self._transform(peripheral_data_frames,
          population_data_frame,
          sock,
          predict=True,
          table_name=table_name)
        self._close(sock)
        sock.close()
        return y_hat

    def refresh(self):
        """Reloads the model from the engine.

        Discards all local changes applied to the model after the last
        invocation of its :meth:`~getml.models.MultirelModel.send`
        method by loading the model corresponding to the ``name``
        attribute from the engine and replacing the attributes of the
        current instance with the results.

        Raises:
            IOError:
                If the engine did not send a proper model.

        Returns:
            :class:`~getml.models.MultirelModel`:
                Current instance
        """
        cmd = dict()
        cmd['type_'] = self.type + '.refresh'
        cmd['name_'] = self.name
        s = comm.send_and_receive_socket(cmd)
        msg = comm.recv_string(s)
        s.close()
        if msg[0] != '{':
            comm.engine_exception_handler(msg)
        json_obj = json.loads(msg)
        for kkey in json_obj['hyperparameters_']:
            if kkey not in ('feature_selector_', 'loss_function_', 'peripheral_', 'peripheral_schema_',
                            'placeholder_', 'population_schema_', 'predictor_'):
                self.__dict__[kkey[:len(kkey) - 1]] = json_obj['hyperparameters_'][kkey]

        if 'predictor_' in json_obj['hyperparameters_']:
            self.predictor = predictors._decode_predictor(json_obj['hyperparameters_']['predictor_'])
        if 'feature_selector_' in json_obj['hyperparameters_']:
            self.feature_selector = predictors._decode_predictor(json_obj['hyperparameters_']['feature_selector_'])
        multithreaded = False
        if self.num_threads > 1:
            multithreaded = True
        if self.predictor is not None and not isinstance(self.predictor, predictors.XGBoostClassifier):
            if isinstance(self.predictor, predictors.XGBoostRegressor):
                if self.predictor.n_jobs > 1:
                    multithreaded = True
            if self.feature_selector is not None and not isinstance(self.feature_selector, predictors.XGBoostClassifier):
                if isinstance(self.feature_selector, predictors.XGBoostRegressor):
                    if self.feature_selector.n_jobs > 1:
                        multithreaded = True
            if multithreaded:
                self.seed = None
        self.loss_function = _decode_loss_function(json_obj['hyperparameters_']['loss_function_'])
        population = _decode_placeholder(json_obj['population_schema_'])
        joined_tables = _decode_joined_tables(json_obj['placeholder_']['joined_tables_'])
        population.set_relations(join_keys_used=(json_obj['placeholder_']['join_keys_used_']),
          other_join_keys_used=(json_obj['placeholder_']['other_join_keys_used_']),
          time_stamps_used=(json_obj['placeholder_']['time_stamps_used_']),
          other_time_stamps_used=(json_obj['placeholder_']['other_time_stamps_used_']),
          upper_time_stamps_used=(json_obj['placeholder_']['upper_time_stamps_used_']),
          joined_tables=joined_tables)
        self.population = population
        peripheral_placeholders = list()
        for pp in range(0, len(json_obj['peripheral_'])):
            pperipheral = Placeholder(name=(json_obj['peripheral_'][pp]),
              categorical=(json_obj['peripheral_schema_'][pp]['categoricals_']),
              numerical=(json_obj['peripheral_schema_'][pp]['numericals_']),
              join_keys=(json_obj['peripheral_schema_'][pp]['join_keys_']),
              time_stamps=(json_obj['peripheral_schema_'][pp]['time_stamps_']),
              targets=(json_obj['peripheral_schema_'][pp]['targets_']))
            peripheral_placeholders.append(pperipheral)

        self.peripheral = peripheral_placeholders
        return self

    def score(self, population_table, peripheral_tables):
        """Calculates the performance of the ``predictor``.

        Returns different scores calculated on `population_table` and
        `peripheral_tables`.

        Examples:

            .. code-block:: python

                model.score(
                    population_table = population_table,
                    peripheral_tables = peripheral_table)

        Args:  
            population_table (Union[:class:`pandas.DataFrame`, :class:`getml.data.DataFrame`]):
                Main table corresponding to the ``population``
                :class:`~getml.data.Placeholder` instance
                variable. Its target variable(s) will be ignored.
            peripheral_tables (Union[:class:`pandas.DataFrame`, :class:`getml.data.DataFrame`, List[:class:`pandas.DataFrame`],List[:class:`getml.data.DataFrame`]]):
                Additional tables corresponding to the ``peripheral``
                :class:`~getml.data.Placeholder` instance
                variable. They have to be provided in the exact same
                order as their corresponding placeholders! A single
                DataFrame will be wrapped into a list internally.

        Raises:
            IOError: If the model corresponding to the instance
                variable ``name`` could not be found on the engine or
                the model could not be fitted.
            TypeError: If any input argument is not of proper type.
            ValueError: If no valid ``predictor`` was set/is None.
            KeyError: If an unsupported instance variable is
                encountered (via
                :meth:`~getml.models.MultirelModel.validate`).
            TypeError: If any instance variable is of wrong type (via
                :meth:`~getml.models.MultirelModel.validate`).
            ValueError: If any instance variable does not match its
                possible choices (string) or is out of the expected
                bounds (numerical) (via
                :meth:`~getml.models.MultirelModel.validate`).

        Return:
            dict:

                Mapping of the name of the score (str) to the
                corresponding value (float).
        
                For regression problems the following scores are
                returned:

                * :const:`~getml.models.scores.rmse`
                * :const:`~getml.models.scores.mae`
                * :const:`~getml.models.scores.rsquared`

                For classification problems, on the other hand, the
                following scores are returned: Possible values for a
                classification problem are:

                * :const:`~getml.models.scores.accuracy`
                * :const:`~getml.models.scores.auc`
                * :const:`~getml.models.scores.cross_entropy`

        Note:

            Only fitted models
            (:meth:`~getml.models.MultirelModel.fit`) can be
            scored. In addition, a valid ``predictor`` must be trained
            as well.

            If a `population_table` or `peripheral_tables` will be
            provided as :class:`pandas.DataFrame`, they will be
            converted to temporary :class:`getml.data.DataFrame`,
            uploaded to the engine, and discarded after the function
            call. Since `peripheral_tables` can very well be the same
            for the :meth:`~getml.models.MultirelModel.predict`,
            :meth:`~getml.models.MultirelModel.score`, and
            :meth:`~getml.models.MultirelModel.transform` methods,
            this way of interacting with the engine can be highly
            inefficient and is discouraged.

        """
        if not isinstance(peripheral_tables, pd.DataFrame):
            if isinstance(peripheral_tables, data.DataFrame):
                peripheral_tables = [
                 peripheral_tables]
            if not isinstance(population_table, data.DataFrame):
                if not isinstance(population_table, pd.DataFrame):
                    raise TypeError("'population_table' must be a getml.data.DataFrame or pandas.data.DataFrame")
            if not type(peripheral_tables) is not list:
                if not (len(peripheral_tables) > 0 and all([isinstance(ll, data.DataFrame) or isinstance(ll, pd.DataFrame) for ll in peripheral_tables])):
                    raise TypeError("'peripheral_tables' must be a getml.data.DataFrame or pandas.DataFrame or a list of those")
        else:
            if not isinstance(self.predictor, _Predictor):
                raise ValueError("No 'predictor' set to perform the prediction.")
            self.validate()
            cmd = dict()
            cmd['type_'] = self.type + '.transform'
            cmd['name_'] = self.name
            cmd['http_request_'] = False
            sock = comm.send_and_receive_socket(cmd)
            msg = comm.recv_string(sock)
            if msg != 'Found!':
                sock.close()
                comm.engine_exception_handler(msg)
            peripheral_data_frames = self._convert_peripheral_tables(peripheral_tables, sock)
            if type(population_table) is data.DataFrame:
                targets = []
            else:
                targets = [elem for elem in self.population.targets if elem in population_table.columns]
        population_data_frame = self._convert_population_table(population_table, targets, sock)
        yhat = self._transform(peripheral_data_frames,
          population_data_frame,
          sock,
          predict=True,
          score=True)
        y = pd.DataFrame()
        for colname in population_data_frame.target_names:
            y[colname] = population_data_frame[colname].to_numpy(sock).ravel()

        y = y.values
        self._close(sock)
        sock.close()
        scores = self._score(yhat, y)
        self._save()
        scores_formatted = dict()
        for sscore in scores:
            if sscore[(len(sscore) - 1)] != '_':
                raise ValueError('All scores are expected to have a trailing underscore.')
            scores_formatted[sscore[:len(sscore) - 1]] = scores[sscore]

        return scores_formatted

    def send(self):
        """Creates a model in the getML engine.

        Serializes the handler with all information provided either
        via the :meth:`~getml.models.MultirelModel.__init__` method,
        by :func:`~getml.models.load_model`, or by manually altering
        the instance variables. These will be sent to the engine,
        which constructs a new model based on them.

        Raises:
            TypeError: If the `population` instance variables is not
                of type :class:`~getml.data.Placeholder` and
                `peripheral` is not a list of these.
            KeyError: If an unsupported instance variable is
                encountered (via
                :meth:`~getml.models.MultirelModel.validate`).
            TypeError: If any instance variable is of wrong type (via
                :meth:`~getml.models.MultirelModel.validate`).
            ValueError: If any instance variable does not match its
                possible choices (string) or is out of the expected
                bounds (numerical) (via
                :meth:`~getml.models.MultirelModel.validate`).

        Returns:
            :class:`~getml.models.MultirelModel`:
                Current instance

        Note:

            If there is already a model with the same ``name``
            attribute is present in the getML engine, it will be
            replaced. Therefore, when calling the
            :meth:`~getml.models.MultirelModel.send` method *after*
            :meth:`~getml.models.MultirelModel.fit` all fit results
            (and calculated scores) will be discarded too and the
            model has to be refitted.

            Imagine you run the following command

            .. code-block:: python

                model.fit(
                    population_table = population_table, 
                    peripheral_tables = peripheral_table)

                model.send()

            Is it possible to undo the changes resulting from calling
            :meth:`~getml.models.MultirelModel.send`?

            The discarding of the old model just happens in memory
            since the :meth:`~getml.models.MultirelModel.send` does
            not trigger the :meth:`~getml.models.MultirelModel._save`
            method and thus does not write the new model to
            disk. These in-memory changes can be undone by using
            :func:`~getml.engine.set_project` to switch to a different
            project and right back to the current one. Since the
            loading of a project is accomplished by reading all
            corresponding objects written to disk, we have restored
            the fitted model.

        """
        if type(self.population) is not Placeholder:
            raise TypeError("'population' must be a valid data.Placeholder!")
        if not (type(self.peripheral) is not list or len(self.peripheral) == 0):
            if not all([type(ll) is Placeholder for ll in self.peripheral]):
                raise TypeError("'peripheral' must be an empty list or a list of getml.data.Placeholder")
        self.validate()
        cmd = dict()
        hyperparameterDict = dict()
        for kkey in self.__dict__:
            if kkey == 'population':
                population = self.__dict__[kkey]
                population_schema = Placeholder(name=(population.name),
                  categorical=(population.categorical),
                  numerical=(population.numerical),
                  join_keys=(population.join_keys),
                  time_stamps=(population.time_stamps),
                  targets=(population.targets))
                population_placeholder = Placeholder(name=(population.name))
                population_placeholder.set_relations(join_keys_used=(population.join_keys_used),
                  other_join_keys_used=(population.other_join_keys_used),
                  time_stamps_used=(population.time_stamps_used),
                  other_time_stamps_used=(population.other_time_stamps_used),
                  upper_time_stamps_used=(population.upper_time_stamps_used),
                  joined_tables=(population.joined_tables))
                cmd['placeholder_'] = population_placeholder
                cmd['population_schema_'] = population_schema
            elif kkey == 'peripheral':
                peripheral = self.__dict__[kkey]
                peripheral_schema = []
                peripheral_placeholder = []
                for pperipheral in peripheral:
                    peripheral_schema.append(Placeholder(name=(pperipheral.name),
                      categorical=(pperipheral.categorical),
                      numerical=(pperipheral.numerical),
                      join_keys=(pperipheral.join_keys),
                      time_stamps=(pperipheral.time_stamps),
                      targets=(pperipheral.targets)))
                    peripheral_placeholder.append(pperipheral.name)

                cmd['peripheral_'] = peripheral_placeholder
                cmd['peripheral_schema_'] = peripheral_schema
            elif kkey in ('name', 'type'):
                cmd[kkey + '_'] = self.__dict__[kkey]
            elif kkey == 'seed':
                if self.seed is None:
                    hyperparameterDict[kkey + '_'] = 5543
                else:
                    hyperparameterDict[kkey + '_'] = self.seed
            else:
                hyperparameterDict[kkey + '_'] = self.__dict__[kkey]

        cmd['hyperparameters_'] = hyperparameterDict
        comm.send(cmd)
        return self

    def to_sql(self):
        """Returns SQL statements visualizing the trained features.

        In order to get insight into the complex features, 
        they are expressed as SQL statements.

        Examples:

            .. code-block:: python

                print(model.to_sql())

        Raises:
            IOError: If the model corresponding to the instance
                variable ``name`` could not be found on the engine or
                the model could not be fitted.
            KeyError: If an unsupported instance variable is
                encountered (via
                :meth:`~getml.models.MultirelModel.validate`).
            TypeError: If any instance variable is of wrong type (via
                :meth:`~getml.models.MultirelModel.validate`).
            ValueError: If any instance variable does not match its
                possible choices (string) or is out of the expected
                bounds (numerical) (via
                :meth:`~getml.models.MultirelModel.validate`).

        Returns:
            str:
                String containing the formatted SQL command.

        Note:

            Only fitted models
            (:meth:`~getml.models.MultirelModel.fit`) do hold trained
            features which can be returned as SQL statements.

            In order to display the returned string properly, it has
            to be pretty printed first using the :py:func:`print`
            function.

            The dialect is based on SQLite3 but not guaranteed to be
            fully compliant with its standard.

        """
        self.validate()
        cmd = dict()
        cmd['type_'] = self.type + '.to_sql'
        cmd['name_'] = self.name
        s = comm.send_and_receive_socket(cmd)
        msg = comm.recv_string(s)
        if msg != 'Found!':
            s.close()
            comm.engine_exception_handler(msg)
        sql = comm.recv_string(s)
        s.close()
        return sql

    def transform(self, population_table, peripheral_tables, df_name='', table_name=''):
        """Translates new data into the trained features.

        Transforms the data provided in `population_table` and
        `peripheral_tables` into features, which can be used to drive
        machine learning models. In addition to returning them as
        numerical array, this method is also able to write the results
        in a data base called `table_name`.

        Examples:

            .. code-block:: python

                model.transform(
                    population_table = population_table,
                    peripheral_tables = peripheral_table)

        Args:  
            population_table (Union[:class:`pandas.DataFrame`, :class:`getml.data.DataFrame`]):
                Main table corresponding to the ``population``
                :class:`~getml.data.Placeholder` instance
                variable. Its target variable(s) will be ignored.
            peripheral_tables (Union[:class:`pandas.DataFrame`, :class:`getml.data.DataFrame`, List[:class:`pandas.DataFrame`],List[:class:`getml.data.DataFrame`]]):
                Additional tables corresponding to the ``peripheral``
                :class:`~getml.data.Placeholder` instance
                variable. They have to be provided in the exact same
                order as their corresponding placeholders! A single
                DataFrame will be wrapped into a list internally.
            df_name (str, optional): 
                If not an empty string, the resulting features will be
                written into a newly created DataFrame. 
            table_name (str, optional): 
                If not an empty string, the resulting features will be
                written into the :mod:`~getml.database` of the same
                name. See :ref:`unified_import_interface` for further information.

        Raises:
            IOError: If the model corresponding to the instance
                variable ``name`` could not be found on the engine or
                the model could not be fitted.
            TypeError: If any input argument is not of proper type.
            KeyError: If an unsupported instance variable is
                encountered (via
                :meth:`~getml.models.MultirelModel.validate`).
            TypeError: If any instance variable is of wrong type (via
                :meth:`~getml.models.MultirelModel.validate`).
            ValueError: If any instance variable does not match its
                possible choices (string) or is out of the expected
                bounds (numerical) (via
                :meth:`~getml.models.MultirelModel.validate`).

        Return:
            :class:`numpy.ndarray`:
                Resulting features provided in an array of the
                (number of rows in `population_table`, number of
                selected features).
            or :class:`getml.data.DataFrame`:
                A DataFrame containing the resulting features.
        Note:

            Only fitted models
            (:meth:`~getml.models.MultirelModel.fit`) can transform
            data into features.

            If a `population_table` or `peripheral_tables` will be
            provided as :class:`pandas.DataFrame`, they will be
            converted to temporary :class:`getml.data.DataFrame`,
            uploaded to the engine, and discarded after the function
            call. Since `peripheral_tables` can very well be the same
            for the :meth:`~getml.models.MultirelModel.predict`,
            :meth:`~getml.models.MultirelModel.score`, and
            :meth:`~getml.models.MultirelModel.transform` methods,
            this way of interacting with the engine can be highly
            inefficient and is discouraged.

        """
        if isinstance(peripheral_tables, pd.DataFrame) or isinstance(peripheral_tables, data.DataFrame):
            peripheral_tables = [
             peripheral_tables]
        else:
            if not isinstance(population_table, data.DataFrame):
                if not isinstance(population_table, pd.DataFrame):
                    raise TypeError("'population_table' must be a getml.data.DataFrame or pandas.data.DataFrame")
            if not type(peripheral_tables) is not list:
                if not (len(peripheral_tables) > 0 and all([isinstance(ll, data.DataFrame) or isinstance(ll, pd.DataFrame) for ll in peripheral_tables])):
                    raise TypeError("'peripheral_tables' must be a getml.data.DataFrame or pandas.DataFrame or a list of those")
                if type(table_name) is not str:
                    raise TypeError("'table_name' must be of type str")
                self.validate()
                cmd = dict()
                cmd['type_'] = self.type + '.transform'
                cmd['name_'] = self.name
                cmd['http_request_'] = False
                sock = comm.send_and_receive_socket(cmd)
                msg = comm.recv_string(sock)
                if msg != 'Found!':
                    sock.close()
                    comm.engine_exception_handler(msg)
                peripheral_data_frames = self._convert_peripheral_tables(peripheral_tables, sock)
                if type(population_table) == data.DataFrame:
                    targets = []
            else:
                targets = [elem for elem in self.population.targets if elem in population_table.columns]
        population_data_frame = self._convert_population_table(population_table, targets, sock)
        y_hat = self._transform(peripheral_data_frames,
          population_data_frame,
          sock,
          df_name=df_name,
          table_name=table_name)
        self._close(sock)
        sock.close()
        if df_name != '':
            y_hat = data.DataFrame(name=df_name).refresh()
        return y_hat

    def validate(self):
        """Checks both the types and the values of all instance 
        variables and raises an exception if something is off.

        Examples:

            .. code-block:: python

                population_table, peripheral_table = getml.datasets.make_numerical()

                population_placeholder = population_table.to_placeholder()
                peripheral_placeholder = peripheral_table.to_placeholder()

                population_placeholder.join(peripheral_placeholder,
                                            join_key = "join_key",
                                            time_stamp = "time_stamp"
                )

                model = getml.models.MultirelModel(
                    population = population_placeholder,
                    peripheral = peripheral_placeholder,
                    name = "multirel"
                )
                model.num_features = 300
                model.shrinkage = 1.7

                model.validate()

        Raises:
            KeyError: If an unsupported instance variable is
                encountered.
            TypeError: If any instance variable is of wrong type.
            ValueError: If any instance variable does not match its
                possible choices (string) or is out of the expected
                bounds (numerical).

        Note: 

            This method is triggered at end of the __init__
            constructor and every time a function communicating with
            the getML engine - except
            :meth:`~getml.models.MultirelModel.refresh` - is called.

            To directly access the validity of single or multiple
            parameters instead of the whole class, you can used
            :func:`getml.helpers.validation.validate_MultirelModel_parameters`.

        """
        if type(self.name) is not str:
            raise TypeError("'name' must be of type str")
        else:
            if not isinstance(self.population, Placeholder):
                raise TypeError("'population' must be a getml.data.Placeholder or None.")
            else:
                if not type(self.peripheral) is not list:
                    if not (len(self.peripheral) > 0 and all([isinstance(ll, Placeholder) for ll in self.peripheral])):
                        raise TypeError("'peripheral' must be either a getml.data.Placeholder or a list of those")
                    if not self.feature_selector is None:
                        if not isinstance(self.feature_selector, _Predictor):
                            raise TypeError("'feature_selector' must implement getml.predictors._Predictor or None.")
                elif not (self.predictor is None or isinstance(self.predictor, _Predictor)):
                    raise TypeError("'predictor' must implement getml.predictors._Predictor or None.")
                if type(self.units) is not dict:
                    raise TypeError("'units' must be of type dict")
                if type(self.session_name) is not str:
                    raise TypeError("'session_name' must be of type str")
                assert isinstance(self.loss_function, _LossFunction), "'loss_function' must implement getml.models.loss_functions._LossFunction or None."
            if type(self.silent) is not bool:
                raise TypeError("'silent' must be of type bool")
            supported = {
             'aggregation', 'allow_sets', 'delta_t',
             'feature_selector', 'grid_factor',
             'include_categorical', 'loss_function',
             'max_length', 'min_num_samples', 'name',
             'num_features', 'num_subfeatures', 'num_threads',
             'peripheral', 'population', 'predictor',
             'regularization', 'round_robin',
             'sampling_factor', 'seed', 'session_name',
             'share_aggregations', 'share_conditions',
             'share_selected_features', 'shrinkage', 'silent',
             'type', 'units', 'use_timestamps'}
            for kkey in self.__dict__:
                if kkey not in supported:
                    raise KeyError('Instance variable [' + kkey + '] is not supported in MultirelModel')

            if self.type != 'MultirelModel':
                raise ValueError("'type' must be 'MultirelModel'")
            assert self.name, "'name' must not be empty"
        _validate_multirel_model_parameters(aggregation=(self.aggregation),
          allow_sets=(self.allow_sets),
          delta_t=(self.delta_t),
          feature_selector=(self.feature_selector),
          grid_factor=(self.grid_factor),
          include_categorical=(self.include_categorical),
          loss_function=(self.loss_function),
          max_length=(self.max_length),
          min_num_samples=(self.min_num_samples),
          num_features=(self.num_features),
          num_subfeatures=(self.num_subfeatures),
          num_threads=(self.num_threads),
          predictor=(self.predictor),
          regularization=(self.regularization),
          round_robin=(self.round_robin),
          sampling_factor=(self.sampling_factor),
          seed=(self.seed),
          share_aggregations=(self.share_aggregations),
          share_conditions=(self.share_conditions),
          share_selected_features=(self.share_selected_features),
          shrinkage=(self.shrinkage),
          use_timestamps=(self.use_timestamps))
        if self.predictor is not None:
            self.predictor.validate()
        if self.feature_selector is not None:
            self.feature_selector.validate()