# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/jwql/instrument_monitors/nirspec_monitors/data_trending/plots/voltage_tab.py
# Compiled at: 2019-08-26 11:08:03
# Size of source mod 2**32: 7757 bytes
"""Prepares plots for Ref. Voltage/Currents tab

    Module prepares plots for mnemonics below. Combines plots in a grid and
    returns tab object.

    Plot 1 - Ref Voltages
    INRSH_FWA_MOTOR_VREF
    INRSH_GWA_MOTOR_VREF
    INRSH_OA_VREF

    Plot 2 - ADCMGAIN (Voltages)
    INRSH_FWA_ADCMGAIN
    INRSH_GWA_ADCMGAIN
    INRSH_RMA_ADCMGAIN

    Plot 3 - OFFSET (Voltages)
    INRSH_GWA_ADCMOFFSET
    INRSH_FWA_ADCMOFFSET
    INRSH_OA_VREFOFF
    INRSH_RMA_ADCMOFFSET

Authors
-------
    - Daniel Kühbacher

Use
---
    The functions within this module are intended to be imported and
    used by ``nirspec_dashboard.py``, e.g.:

    ::
        from .plots.voltage_tab import voltage_plots
        tab = voltage_plots(conn, start, end)

Dependencies
------------
    User must provide database "nirpsec_database.db"

"""
import jwql.instrument_monitors.nirspec_monitors.data_trending.utils.sql_interface as sql, jwql.instrument_monitors.nirspec_monitors.data_trending.plots.plot_functions as pf
from bokeh.models import LinearAxis, Range1d
from bokeh.plotting import figure
from bokeh.models.widgets import Panel, Tabs, Div
from bokeh.models import ColumnDataSource, HoverTool
from bokeh.layouts import WidgetBox, gridplot, Column
import pandas as pd, numpy as np
from astropy.time import Time

def ref_volt(conn, start, end):
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
      plot_width=1120,
      plot_height=500,
      x_axis_type='datetime',
      output_backend='webgl',
      x_axis_label='Date',
      y_axis_label='Voltage (V)')
    p.grid.visible = True
    p.title.text = 'Ref Voltages'
    pf.add_basic_layout(p)
    a = pf.add_to_plot(p, 'FWA_MOTOR_VREF', 'INRSH_FWA_MOTOR_VREF', start, end, conn, color='green')
    b = pf.add_to_plot(p, 'GWA_MOTOR_VREF', 'INRSH_GWA_MOTOR_VREF', start, end, conn, color='blue')
    c = pf.add_to_plot(p, 'OA_VREF', 'INRSH_OA_VREF', start, end, conn, color='red')
    pf.add_hover_tool(p, [a, b, c])
    p.legend.location = 'bottom_right'
    p.legend.click_policy = 'hide'
    p.legend.orientation = 'horizontal'
    return p


def gain_volt(conn, start, end):
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
      plot_width=1120,
      plot_height=500,
      x_axis_type='datetime',
      output_backend='webgl',
      x_axis_label='Date',
      y_axis_label='Voltage (V)')
    p.grid.visible = True
    p.title.text = 'ADCMAIN'
    pf.add_basic_layout(p)
    a = pf.add_to_plot(p, 'FWA_ADCMGAIN', 'INRSH_FWA_ADCMGAIN', start, end, conn, color='green')
    b = pf.add_to_plot(p, 'GWA_ADCMGAIN', 'INRSH_GWA_ADCMGAIN', start, end, conn, color='blue')
    c = pf.add_to_plot(p, 'RMA_ADCMGAIN', 'INRSH_RMA_ADCMGAIN', start, end, conn, color='red')
    p.legend.location = 'bottom_right'
    p.legend.click_policy = 'hide'
    p.legend.orientation = 'horizontal'
    return p


def offset_volt(conn, start, end):
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
      plot_width=1120,
      plot_height=500,
      x_axis_type='datetime',
      output_backend='webgl',
      x_axis_label='Date',
      y_axis_label='Voltage (V)')
    p.grid.visible = True
    p.title.text = 'OFFSET'
    pf.add_basic_layout(p)
    a = pf.add_to_plot(p, 'GWA_ADCMOFFSET', 'INRSH_GWA_ADCMOFFSET', start, end, conn, color='blue')
    b = pf.add_to_plot(p, 'FWA_ADCMOFFSET', 'INRSH_FWA_ADCMOFFSET', start, end, conn, color='green')
    c = pf.add_to_plot(p, 'OA_VREFOFF', 'INRSH_OA_VREFOFF', start, end, conn, color='orange')
    d = pf.add_to_plot(p, 'RMA_ADCMOFFSET', 'INRSH_RMA_ADCMOFFSET', start, end, conn, color='red')
    pf.add_hover_tool(p, [a, b, c, d])
    p.legend.location = 'bottom_right'
    p.legend.click_policy = 'hide'
    p.legend.orientation = 'horizontal'
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
    descr = Div(text='\n    <style>\n    table, th, td {\n      border: 1px solid black;\n      background-color: #efefef;\n      border-collapse: collapse;\n      padding: 5px\n    }\n    table {\n      border-spacing: 15px;\n    }\n    </style>\n\n    <body>\n    <table style="width:100%">\n      <tr>\n        <th><h6>Plotname</h6></th>\n        <th><h6>Mnemonic</h6></th>\n        <th><h6>Description</h6></th>\n      </tr>\n      <tr>\n        <td>Ref Voltages</td>\n        <td>INRSH_FWA_MOTOR_VREF<br>\n            INRSH_GWA_MOTOR_VREF<br>\n            INRSH_OA_VREF</td>\n        <td>FWA Motor Reference Voltage for Calibration<br>\n            GWA Motor Reference Voltage for Calibration<br>\n            OA/RMA Reference Voltage for TM Calibration<br>\n        </td>\n      </tr>\n\n      <tr>\n        <td>ADCMGAIN</td>\n        <td>INRSH_FWA_ADCMGAIN<br>\n            INRSH_GWA_ADCMGAIN<br>\n            INRSH_RMA_ADCMGAIN</td>\n        <td>FWA ADC Motor Chain Gain for Calibration<br>\n            GWA ADC Motor Chain Gain for Calibration<br>\n            RMA ADC Motor Chain Gain for Calibration<br>\n        </td>\n      </tr>\n\n      <tr>\n        <td>OFFSET</td>\n        <td>INRSH_FWA_ADCMOFFSET<br>\n            INRSH_GWA_ADCMOFFSET<br>\n            INRSH_OA_VREFOFF<br>\n            INRSH_RMA_ADCMOFFSET</td>\n        <td>FWA ADC Motor Chain Offset for Calibration<br>\n            GWA ADC Motor Chain Offset for Calibration<br>\n            CAA Reference Voltage Offset for TM Calibration<br>\n            RMA ADC Motor Chain Offset for Calibration<br>\n        </td>\n      </tr>\n    </table>\n    </body>\n    ',
      width=1100)
    plot1 = ref_volt(conn, start, end)
    plot2 = gain_volt(conn, start, end)
    plot3 = offset_volt(conn, start, end)
    layout = Column(descr, plot1, plot2, plot3)
    tab = Panel(child=layout, title='REF VOLTAGES')
    return tab