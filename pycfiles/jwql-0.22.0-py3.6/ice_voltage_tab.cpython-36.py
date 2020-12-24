# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/jwql/instrument_monitors/miri_monitors/data_trending/plots/ice_voltage_tab.py
# Compiled at: 2019-08-26 11:08:03
# Size of source mod 2**32: 8378 bytes
"""Prepares plots for ICE VOLTAGE tab

    Module prepares plots for mnemonics below, combines plots in a grid and
    returns tab object.

    Plot 1:
    IMIR_HK_ICE_SEC_VOLT1
    IMIR_HK_ICE_SEC_VOLT3

    Plot 2:
    IMIR_HK_ICE_SEC_VOLT2

    Plot 3:
    IMIR_HK_ICE_SEC_VOLT4 : IDLE and HV_ON

    Plot 4:
    IMIR_HK_FW_POS_VOLT
    IMIR_HK_GW14_POS_VOLT
    IMIR_HK_GW23_POS_VOLT
    IMIR_HK_CCC_POS_VOLT

Authors
-------
    - Daniel Kühbacher

Use
---
    The functions within this module are intended to be imported and
    used by ``dashborad.py``, e.g.:

    ::
        from .plots.ice_voltage_tab import ice_plots
        tab = ice_plots(conn, start, end)

Dependencies
------------
    User must provide database "miri_database.db"

"""
import jwql.instrument_monitors.miri_monitors.data_trending.utils.sql_interface as sql, jwql.instrument_monitors.miri_monitors.data_trending.plots.plot_functions as pf
from bokeh.models import LinearAxis, Range1d
from bokeh.plotting import figure
from bokeh.models.widgets import Panel, Tabs, Div
from bokeh.models import ColumnDataSource
from bokeh.layouts import gridplot, Column
import pandas as pd, numpy as np
from astropy.time import Time

def volt4(conn, start, end):
    """Create specific plot and return plot object
    Parameters
    ----------
    conn : DBobject
        Connection object that represents database
    start : time
        Startlimit for x-axis and query (typ. datetime.now()- 4Months)
    end : time
        Endlimit for x-axis and query (typ. datetime.now())
    Return
    ------
    p : Plot object
        Bokeh plot
    """
    p = figure(tools='pan,wheel_zoom,box_zoom,reset,save', toolbar_location='above',
      plot_width=560,
      plot_height=500,
      y_range=[
     4.2, 5],
      x_axis_type='datetime',
      output_backend='webgl',
      x_axis_label='Date',
      y_axis_label='Voltage (V)')
    p.grid.visible = True
    p.title.text = 'ICE_SEC_VOLT4'
    pf.add_basic_layout(p)
    a = pf.add_to_plot(p, 'Volt4 Idle', 'IMIR_HK_ICE_SEC_VOLT4_IDLE', start, end, conn, color='orange')
    b = pf.add_to_plot(p, 'Volt4 Hv on', 'IMIR_HK_ICE_SEC_VOLT4_HV_ON', start, end, conn, color='red')
    pf.add_hover_tool(p, [a, b])
    p.legend.location = 'bottom_right'
    p.legend.click_policy = 'hide'
    return p


def volt1_3(conn, start, end):
    """Create specific plot and return plot object
    Parameters
    ----------
    conn : DBobject
        Connection object that represents database
    start : time
        Startlimit for x-axis and query (typ. datetime.now()- 4Months)
    end : time
        Endlimit for x-axis and query (typ. datetime.now())
    Return
    ------
    p : Plot object
        Bokeh plot
    """
    p = figure(tools='pan,wheel_zoom,box_zoom,reset,save', toolbar_location='above',
      plot_width=560,
      plot_height=500,
      y_range=[
     30, 50],
      x_axis_type='datetime',
      output_backend='webgl',
      x_axis_label='Date',
      y_axis_label='Voltage (V)')
    p.grid.visible = True
    p.title.text = 'ICE_SEC_VOLT1/3'
    pf.add_basic_layout(p)
    a = pf.add_to_plot(p, 'Volt1', 'IMIR_HK_ICE_SEC_VOLT1', start, end, conn, color='red')
    b = pf.add_to_plot(p, 'Volt3', 'IMIR_HK_ICE_SEC_VOLT3', start, end, conn, color='purple')
    pf.add_hover_tool(p, [a, b])
    p.legend.location = 'bottom_right'
    p.legend.click_policy = 'hide'
    return p


def volt2(conn, start, end):
    """Create specific plot and return plot object
    Parameters
    ----------
    conn : DBobject
        Connection object that represents database
    start : time
        Startlimit for x-axis and query (typ. datetime.now()- 4Months)
    end : time
        Endlimit for x-axis and query (typ. datetime.now())
    Return
    ------
    p : Plot object
        Bokeh plot
    """
    p = figure(tools='pan,wheel_zoom,box_zoom,reset,save', toolbar_location='above',
      plot_width=560,
      plot_height=500,
      x_axis_type='datetime',
      output_backend='webgl',
      x_axis_label='Date',
      y_axis_label='Voltage (V)')
    p.grid.visible = True
    p.title.text = 'ICE_SEC_VOLT2'
    pf.add_basic_layout(p)
    a = pf.add_to_plot(p, 'Volt2', 'IMIR_HK_ICE_SEC_VOLT2', start, end, conn, color='red')
    pf.add_hover_tool(p, [a])
    p.legend.location = 'bottom_right'
    p.legend.click_policy = 'hide'
    return p


def pos_volt(conn, start, end):
    """Create specific plot and return plot object
    Parameters
    ----------
    conn : DBobject
        Connection object that represents database
    start : time
        Startlimit for x-axis and query (typ. datetime.now()- 4Months)
    end : time
        Endlimit for x-axis and query (typ. datetime.now())
    Return
    ------
    p : Plot object
        Bokeh plot
    """
    p = figure(tools='pan,wheel_zoom,box_zoom,reset,save', toolbar_location='above',
      plot_width=560,
      plot_height=500,
      y_range=[
     280, 300],
      x_axis_type='datetime',
      output_backend='webgl',
      x_axis_label='Date',
      y_axis_label='Voltage (mV)')
    p.grid.visible = True
    p.title.text = 'Wheel Sensor Supply'
    pf.add_basic_layout(p)
    a = pf.add_to_plot(p, 'FW', 'IMIR_HK_FW_POS_VOLT', start, end, conn, color='red')
    b = pf.add_to_plot(p, 'GW14', 'IMIR_HK_GW14_POS_VOLT', start, end, conn, color='purple')
    c = pf.add_to_plot(p, 'GW23', 'IMIR_HK_GW23_POS_VOLT', start, end, conn, color='orange')
    d = pf.add_to_plot(p, 'CCC', 'IMIR_HK_CCC_POS_VOLT', start, end, conn, color='firebrick')
    pf.add_hover_tool(p, [a, b, c, d])
    p.legend.location = 'bottom_right'
    p.legend.click_policy = 'hide'
    return p


def volt_plots(conn, start, end):
    """Combines plots to a tab
    Parameters
    ----------
    conn : DBobject
        Connection object that represents database
    start : time
        Startlimit for x-axis and query (typ. datetime.now()- 4Months)
    end : time
        Endlimit for x-axis and query (typ. datetime.now())
    Return
    ------
    p : tab object
        used by dashboard.py to set up dashboard
    """
    descr = Div(text='\n    <style>\n    table, th, td {\n      border: 1px solid black;\n      background-color: #efefef;\n      border-collapse: collapse;\n      padding: 5px\n    }\n    table {\n      border-spacing: 15px;\n    }\n    </style>\n\n    <body>\n    <table style="width:100%">\n      <tr>\n        <th><h6>Plotname</h6></th>\n        <th><h6>Mnemonic</h6></th>\n        <th><h6>Description</h6></th>\n      </tr>\n      <tr>\n        <td>ICE_SEC_VOLT1/3</td>\n        <td>IMIR_HK_ICE_SEC_VOLT1 <br>\n            IMIR_HK_ICE_SEC_VOLT3 <br> </td>\n        <td>ICE Secondary Voltage (HV) V1 and V3</td>\n      </tr>\n      <tr>\n        <td>ICE_SEC_VOLT2</td>\n        <td>IMIR_HK_SEC_VOLT2</td>\n        <td>ICE secondary voltage (HV) V2</td>\n      </tr>\n      <tr>\n        <td>ICE_SEC_VOLT4</td>\n        <td>IMIR_HK_SEC_VOLT2</td>\n        <td>ICE secondary voltage (HV) V4 - HV on and IDLE</td>\n      </tr>\n      <tr>\n        <td>Wheel Sensor Supply</td>\n        <td>IMIR_HK_FW_POS_VOLT<br>\n            IMIR_HK_GW14_POS_VOLT<br>\n            IMIR_HK_GW23_POS_VOLT<br>\n            IMIR_HK_CCC_POS_VOLT</td>\n        <td>Wheel Sensor supply voltages </td>\n      </tr>\n    </table>\n    </body>\n    ',
      width=1100)
    plot1 = volt1_3(conn, start, end)
    plot2 = volt2(conn, start, end)
    plot3 = volt4(conn, start, end)
    plot4 = pos_volt(conn, start, end)
    l = gridplot([[plot1, plot2], [plot3, plot4]], merge_tools=False)
    layout = Column(descr, l)
    tab = Panel(child=layout, title='ICE VOLTAGE')
    return tab