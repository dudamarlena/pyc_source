# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/AA/Python/Projects/montepylib/examples/example1.py
# Compiled at: 2014-08-05 23:13:47
import os
from pandas import Series, DataFrame
import pandas as pd
from montepylib.io import excel_table_pos
from montepylib.manip import unpivot_int_cols, cross_merge
from montepylib.sim import Simulator
import montepylib.extend, numpy as np

def read_data(data_path='data'):
    num_trees = pd.read_csv(os.path.join(data_path, 'numTrees.csv'), comment='#', skipinitialspace=True)
    ann_mean_fruit_per_tree = pd.read_csv(os.path.join(data_path, 'meanFruitPerTree.csv'), comment='#', skipinitialspace=True)
    sd_fruit_per_tree = pd.read_csv(os.path.join(data_path, 'sdFruitPerTree.csv'), comment='#', skipinitialspace=True)
    sd_fruit_per_tree = sd_fruit_per_tree['sd'][0]
    fruit_per_tree = unpivot_int_cols(ann_mean_fruit_per_tree, 'year', 'mean')
    fruit_per_tree['sd'] = sd_fruit_per_tree * fruit_per_tree['mean']
    ann_fixed_costs = pd.read_csv(os.path.join(data_path, 'fixedCosts.csv'), comment='#', skipinitialspace=True)
    fixed_cost = unpivot_int_cols(ann_fixed_costs, 'year', 'value')
    ann_var_costs_per_fruit = pd.read_csv(os.path.join(data_path, 'varCostsPerFruit.csv'), comment='#', skipinitialspace=True)
    cost_per_fruit = unpivot_int_cols(ann_var_costs_per_fruit, 'year', 'cost per fruit')
    ann_mean_revenue_per_fruit = pd.read_csv(os.path.join(data_path, 'meanRevenuePerFruit.csv'), comment='#', skipinitialspace=True)
    sd_revenue_per_fruit = pd.read_csv(os.path.join(data_path, 'sdRevenuePerFruit.csv'), comment='#', skipinitialspace=True)
    sd_revenue_per_fruit = sd_revenue_per_fruit['sd'][0]
    revenue_per_fruit = unpivot_int_cols(ann_mean_revenue_per_fruit, 'year', 'mean')
    revenue_per_fruit['sd'] = sd_revenue_per_fruit * revenue_per_fruit['mean']
    return {'num_trees': num_trees, 'fruit_per_tree': fruit_per_tree, 
       'fixed_cost': fixed_cost, 
       'cost_per_fruit': cost_per_fruit, 
       'revenue_per_fruit': revenue_per_fruit}


def simulate_vars(data, simulator, N):
    """
    Simulate and calculate quantities at farm x fruit x variety (x iteration x year) level.
    Returns a dictionary of simulated quantities.
    Eg.:
    >>> data = read_data()
    >>> simulator = Simulator()
    >>> simulate_vars(data, simulator, N=3)
    """
    sim_fruit_per_tree = simulator.sim_from_params(N, data['fruit_per_tree'], 'fruit per tree')
    sim_fixed_cost = simulator.sim_from_params(N, data['fixed_cost'], 'fixed cost')
    sim_revenue_per_fruit = simulator.sim_from_params(N, data['revenue_per_fruit'], 'revenue per fruit')
    sim_fruit = simulator.merge(data['num_trees'], sim_fruit_per_tree, how='outer')
    sim_fruit['volume'] = sim_fruit['fruit per tree'] * sim_fruit['num trees']
    sim_var_cost = simulator.merge(sim_fruit, data['cost_per_fruit'])
    sim_var_cost['var cost'] = sim_var_cost['volume'] * sim_var_cost['cost per fruit']
    sim_revenue = simulator.merge(sim_revenue_per_fruit, sim_fruit)
    sim_revenue['revenue'] = sim_revenue['volume'] * sim_revenue['revenue per fruit']
    return {'sim_var_cost': sim_var_cost, 'sim_revenue': sim_revenue, 
       'sim_fixed_cost': sim_fixed_cost}


def aggregate_cashflows(sims, simulator, discount_rate=None, base_year=None):
    """
    Aggregate up to the iteration x year level.
    Eg.:
    >>> data = read_data()
    >>> simulator = Simulator()
    >>> sims = simulate_vars(data, simulator, N=3)
    >>> aggregate_cashflows(sims, simulator)
    TBC
    """
    cashflows = simulator.merge(sims['sim_var_cost'], sims['sim_revenue'], how='outer')
    agg_cashflows = cashflows.groupby(['farm', 'year', 'iteration']).sum().reset_index()
    agg_cashflows = simulator.merge(agg_cashflows, sims['sim_fixed_cost'], how='outer').fillna(0)
    agg_cashflows['profit'] = agg_cashflows['revenue'] - agg_cashflows['fixed cost'] - agg_cashflows['var cost']
    agg_cashflows.drop(['fruit per tree', 'cost per fruit', 'revenue per fruit', 'num trees'], axis=1)
    total_per_iteration = agg_cashflows.groupby(['iteration', 'year']).sum()
    if discount_rate and base_year:
        total_per_iteration = total_per_iteration.reset_index()
        total_per_iteration['discount factor'] = 1 / discount_rate ** (total_per_iteration['year'].apply(int) - base_year)
        total_per_iteration['discounted profit'] = total_per_iteration['discount factor'] * total_per_iteration['profit']
        total_per_iteration = total_per_iteration.set_index(['iteration', 'year'])
    return total_per_iteration


def simulate(data, N, discount_rate=None, base_year=None):
    """
    Package up the simulation and the aggregation, and calculate NPV.
    Given the data from read_data(), run the whole simulation and return total_per_iteration.
    >>> data = read_data()
    >>> total_per_iteration = simulate(data, N=1000)
    """
    simulator = Simulator()
    sims = simulate_vars(data, simulator, N)
    return aggregate_cashflows(sims, simulator, discount_rate, base_year)


def calc_NPVs(total_per_iteration):
    """
    Returns a DataFrame containing one simulated NPV per iteration.
    Expects as argument the output of simulate()
    Plot a histogram of NPV with eg.: 
    >>> calc_NPVs(total_per_iteration).hist(xrot=90)
    """
    return total_per_iteration.reset_index().groupby(['iteration'])[['discounted profit']].sum().rename(columns={'discounted profit': 'NPV'})


def sim_output(total_per_iteration, N):
    """
    Example of some stats you can apply to the output of aggregate_cashflows()
    """
    print total_per_iteration.xs('2017', level='year').describe(percentile_width=80).T
    print (total_per_iteration.xs('2014', level='year')['profit'] <= 0).sum() / (N + 0.0)
    total_per_iteration.xs('2014', level='year')[['profit']].hist(xrot=90)