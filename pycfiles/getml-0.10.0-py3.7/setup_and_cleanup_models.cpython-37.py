# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/getml/helpers/setup_and_cleanup_models.py
# Compiled at: 2020-03-16 07:21:38
# Size of source mod 2**32: 4338 bytes
from getml import data, datasets, engine, predictors, models
from getml.models import MultirelModel, RelboostModel, loss_functions

def get_mulbert():
    """Returns a custom MultirelModel used for unit testing.
    """
    population_table, peripheral_table = datasets.make_numerical(random_state=118)
    population_placeholder = population_table.to_placeholder()
    peripheral_placeholder = peripheral_table.to_placeholder()
    population_placeholder.join(peripheral_placeholder, 'join_key', 'time_stamp')
    predictor = predictors.LinearRegression()
    feature_selector = predictors.XGBoostRegressor(booster='gblinear',
      n_estimators=60,
      n_jobs=1,
      max_depth=7,
      reg_lambda=500)
    model = models.MultirelModel(name='Mulbert',
      population=population_placeholder,
      peripheral=[
     peripheral_placeholder],
      loss_function=(loss_functions.SquareLoss()),
      aggregation=[
     models.aggregations.Avg,
     models.aggregations.Count,
     models.aggregations.CountDistinct,
     models.aggregations.CountMinusCountDistinct,
     models.aggregations.Max,
     models.aggregations.Median,
     models.aggregations.Min,
     models.aggregations.Sum,
     models.aggregations.Var],
      feature_selector=feature_selector,
      num_features=20,
      num_subfeatures=10,
      share_aggregations=0.2,
      predictor=predictor,
      allow_sets=True,
      min_num_samples=80,
      num_threads=1,
      shrinkage=0.2,
      seed=2231)
    return (
     model, population_table, peripheral_table)


def get_relbert():
    """Returns a custom RelboostModel used for unit testing.
    """
    population_table, peripheral_table = datasets.make_numerical(random_state=118)
    population_placeholder = data.Placeholder(name='numerical_population',
      numerical=[
     'column_01'],
      join_keys=[
     'join_key'],
      time_stamps=[
     'time_stamp'],
      targets=[
     'targets'])
    peripheral_placeholder = data.Placeholder(name='numerical_peripheral',
      numerical=[
     'column_01'],
      join_keys=[
     'join_key'],
      time_stamps=[
     'time_stamp'])
    population_placeholder.join(peripheral_placeholder, 'join_key', 'time_stamp')
    predictor = predictors.LinearRegression()
    feature_selector = predictors.XGBoostRegressor(booster='gblinear',
      n_estimators=60,
      n_jobs=1,
      max_depth=7,
      reg_lambda=500)
    model = models.RelboostModel(name='Relbert',
      population=population_placeholder,
      peripheral=[
     peripheral_placeholder],
      loss_function=(loss_functions.SquareLoss()),
      feature_selector=feature_selector,
      num_features=20,
      num_subfeatures=10,
      predictor=predictor,
      min_num_samples=80,
      num_threads=1,
      shrinkage=0.2,
      seed=2231)
    return (
     model, population_table, peripheral_table)


def setup_models():
    """Uploads a bunch of models which can be accessed and used by unit
    tests.
    """
    engine.set_project('model-unit-tests')
    model_multirel, population_table_multirel, peripheral_table_multirel = get_mulbert()
    model_relboost, population_table_relboost, peripheral_table_relboost = get_relbert()
    model_multirel.send().fit(population_table=population_table_multirel,
      peripheral_tables=[
     peripheral_table_multirel])
    model_relboost.send().fit(population_table=population_table_relboost,
      peripheral_tables=[
     peripheral_table_relboost])


def cleanup_models():
    """Removes all testing folders and models from the engine.
    """
    engine.delete_project('model-unit-tests')