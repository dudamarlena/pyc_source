# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/jwql/instrument_monitors/nirspec_monitors/data_trending/dashboard.py
# Compiled at: 2019-08-26 11:08:03
# Size of source mod 2**32: 3202 bytes
"""Combines plots to tabs and prepares dashboard

The module imports all prepares plot functions from .plots and combines
prebuilt tabs to a dashboard. Furthermore it defines the timerange for
the visualisation. Default time_range should be set to about 4 Month (120days)

Authors
-------
    - Daniel Kühbacher

Use
---
    The functions within this module are intended to be imported and
    used by ``data_container.py``, e.g.:

    ::
        import jwql.instrument_monitors.miri_monitors.data_trending.dashboard as dash
        dashboard, variables = dash.data_trending_dashboard(start_time, end_time)

Dependencies
------------
    User must provide "nirspec_database.db" in folder jwql/database

"""
import os, jwql.instrument_monitors.nirspec_monitors.data_trending.utils.sql_interface as sql
from jwql.utils.utils import get_config, filename_parser
from bokeh.embed import components
from bokeh.models.widgets import Tabs
from bokeh.resources import Resources
from bokeh.io.state import curstate
from astropy.time import Time
import datetime
from datetime import date
from .plots.power_tab import power_plots
from .plots.voltage_tab import volt_plots
from .plots.temperature_tab import temperature_plots
from .plots.msa_mce_tab import msa_mce_plots
from .plots.fpe_fpa_tab import fpe_fpa_plots
from .plots.caa_tab import caa_plots
from .plots.wheel_tab import wheel_pos
now = datetime.datetime.now()
default_start = datetime.date(2017, 8, 15).isoformat()
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

def data_trending_dashboard(start=default_start, end=now):
    """Bulilds dashboard
    Parameters
    ----------
    start : time
        configures start time for query and visualisation
    end : time
        configures end time for query and visualisation
    Return
    ------
    plot_data : list
        A list containing the JavaScript and HTML content for the dashboard
    variables : dict
        no use
    """
    DATABASE_LOCATION = os.path.join(get_config()['jwql_dir'], 'database')
    DATABASE_FILE = os.path.join(DATABASE_LOCATION, 'nirspec_database.db')
    conn = sql.create_connection(DATABASE_FILE)
    variables = dict(init=1)
    variables = dict(init=1)
    tab1 = power_plots(conn, start, end)
    tab2 = volt_plots(conn, start, end)
    tab3 = temperature_plots(conn, start, end)
    tab4 = msa_mce_plots(conn, start, end)
    tab5 = fpe_fpa_plots(conn, start, end)
    tab6 = caa_plots(conn, start, end)
    tab7 = wheel_pos(conn, start, end)
    tabs = Tabs(tabs=[tab1, tab2, tab3, tab4, tab5, tab6, tab7])
    script, div = components(tabs)
    plot_data = [div, script]
    sql.close_connection(conn)
    return (
     plot_data, variables)