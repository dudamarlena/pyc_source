# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/access/fca/fca3.py
# Compiled at: 2020-02-24 17:09:30
# Size of source mod 2**32: 5533 bytes
import pandas as pd, numpy as np
from .fca1 import weighted_catchment
from ..weights.weights import step_fn

def three_stage_fca(demand_df, supply_df, cost_df, max_cost, demand_index='geoid', demand_name='demand', supply_index='geoid', supply_name='supply', cost_origin='origin', cost_dest='dest', cost_name='cost', weight_fn=None, normalize=False):
    r"""Calculation of the floating catchment accessibility
    ratio, from DataFrames with precomputed distances.
    This is accomplished through a single call of the :meth:`access.access.weighted_catchment` method,
    to retrieve the patients using each provider.
    The ratio of providers per patient is then calculated at each care destination,
    and that ratio is weighted and summed at each corresponding demand site.
    The only difference weight respect to the 2SFCA method is that,
    in addition to a distance-dependent weight (`weight_fn`),
    a preference weight *G* is calculated.  That calculation
    uses the value :math:`\beta`.
    See the original paper by Wan, Zou, and Sternberg. :cite:`2012_wan_3SFCA`

    Parameters
    ----------

    demand_df     : `pandas.DataFrame <https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html>`_
                    The origins dataframe, containing a location index and a total demand.
    demand_origin : str
                    is the name of the column of `demand` that holds the origin ID.
    demand_value  : str
                    is the name of the column of `demand` that holds the aggregate demand at a location.
    supply_df     : `pandas.DataFrame <https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html>`_
                    The origins dataframe, containing a location index and level of supply
    supply_df     : `pandas.DataFrame <https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html>`_
                    The origins dataframe, containing a location index and level of supply
    cost_df       : `pandas.DataFrame <https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html>`_
                    This dataframe contains a link between neighboring demand locations, and a cost between them.
    cost_origin   : str
                    The column name of the locations of users or consumers.
    cost_dest     : str
                    The column name of the supply or resource locations.
    cost_name     : str
                    The column name of the travel cost between origins and destinations
    weight_fn  : function
                 This fucntion will weight the value of resources/facilities,
                 as a function of the raw cost.
    max_cost   : float
                 This is the maximum cost to consider in the weighted sum;
                 note that it applies *along with* the weight function.
    preference_weight_beta : float
                             Parameter scaling with the gaussian weights,
                             used to generate preference weights.

    Returns
    -------
    access     : pandas.Series
                 A -- potentially-weighted -- three-stage access ratio.
    """
    cost_df['W3'] = cost_df[cost_name].apply(weight_fn)
    W3sum_frame = cost_df[['origin', 'W3']].groupby('origin').sum().rename(columns={'W3': 'W3sum'}).reset_index()
    cost_df = pd.merge(cost_df, W3sum_frame)
    cost_df['G'] = cost_df.W3 / cost_df.W3sum
    total_demand_series = weighted_catchment(demand_df, cost_df, max_cost, cost_source=cost_origin,
      cost_dest=cost_dest,
      cost_cost=cost_name,
      loc_index=demand_index,
      loc_value=demand_name,
      weight_fn=weight_fn,
      three_stage_weight=True)
    temp = supply_df.join(total_demand_series, how='right', rsuffix='r')
    temp[supply_name].fillna(0, inplace=True)
    temp['Rl'] = temp[supply_name] / temp[demand_name]
    supply_to_total_demand_frame = pd.DataFrame(data={'Rl': temp['Rl']})
    supply_to_total_demand_frame.index.name = 'geoid'
    three_stage_fca_series = weighted_catchment(supply_to_total_demand_frame, (cost_df.sort_index()), max_cost, cost_source=cost_dest,
      cost_dest=cost_origin,
      cost_cost=cost_name,
      loc_index='geoid',
      loc_value='Rl',
      weight_fn=weight_fn,
      three_stage_weight=True)
    cost_df.drop(columns=['G', 'W3', 'W3sum'], inplace=True)
    return three_stage_fca_series