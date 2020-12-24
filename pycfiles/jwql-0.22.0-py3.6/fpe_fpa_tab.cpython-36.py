# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/jwql/instrument_monitors/nirspec_monitors/data_trending/plots/fpe_fpa_tab.py
# Compiled at: 2019-08-26 11:08:03
# Size of source mod 2**32: 12038 bytes
"""Prepares plots for Temperature tab

    Module prepares plots for mnemonics below. Combines plots in a grid and
    returns tab object.

    Plot 1 - ASIC 1 Voltages
    IGDP_NRSD_ALG_A1_VDDA
    IGDP_NRSD_ALG_A1GND4VDA
    IGDP_NRSD_ALG_A1GND5VRF
    INRSD_ALG_A1_VDD3P3
    INRSD_ALG_A1_VDD
    INRSD_ALG_A1_REF
    INRSD_A1_DSUB_V
    INRSD_A1_VRESET_V
    INRSD_A1_CELLDRN_V
    INRSD_A1_DRAIN_V
    INRSD_A1_VBIASGATE_V
    INRSD_A1_VBIASPWR_V

    Plot 2 - ASIC 1 Currents
    IGDP_NRSD_ALG_A1_VDD_C
    IGDP_NRSD_ALG_A1VDAP12C
    IGDP_NRSD_ALG_A1VDAN12C
    INRSD_A1_VDDA_I

    Plot 3 - ASIC 2 Voltages
    IGDP_NRSD_ALG_A2_VDDA
    IGDP_NRSD_ALG_A2GND4VDA
    IGDP_NRSD_ALG_A2GND5VRF
    INRSD_ALG_A2_VDD3P3
    INRSD_ALG_A2_VDD
    INRSD_ALG_A2_REF
    INRSD_A2_DSUB_V
    INRSD_A2_VRESET_V
    INRSD_A2_CELLDRN_V
    INRSD_A2_DRAIN_V
    INRSD_A2_VBIASGATE_V
    INRSD_A2_VBIASPWR_V

    Plot 4 - ASIC 2 Currents
    IGDP_NRSD_ALG_A2_VDD_C
    IGDP_NRSD_ALG_A2VDAP12C
    IGDP_NRSD_ALG_A2VDAN12C
    INRSD_A2_VDDA_I

Authors
-------
    - Daniel Kühbacher

Use
---
    The functions within this module are intended to be imported and
    used by ``nirspec_dashboard.py``, e.g.:

    ::
        from .plots.fpa_fpe_tab import fpa_fpe_plots
        tab = fpa_fpe_plots(conn, start, end)

Dependencies
------------
    User must provide database "nirspec_database.db"

"""
import jwql.instrument_monitors.nirspec_monitors.data_trending.utils.sql_interface as sql, jwql.instrument_monitors.nirspec_monitors.data_trending.plots.plot_functions as pf
from bokeh.models import LinearAxis, Range1d
from bokeh.plotting import figure
from bokeh.models.widgets import Panel, Tabs, Div
from bokeh.models import ColumnDataSource, HoverTool
from bokeh.layouts import WidgetBox, gridplot, Column, Row
import pandas as pd, numpy as np
from astropy.time import Time

def asic_1_voltages(conn, start, end):
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
      plot_height=800,
      x_axis_type='datetime',
      output_backend='webgl',
      x_axis_label='Date',
      y_axis_label='Voltage (V)')
    p.grid.visible = True
    p.title.text = 'ASIC 1 Voltages'
    pf.add_basic_layout(p)
    a = pf.add_to_plot(p, 'VDDA', 'IGDP_NRSD_ALG_A1_VDDA', start, end, conn, color='burlywood')
    b = pf.add_to_plot(p, 'A1GND4VDA', 'IGDP_NRSD_ALG_A1GND4VDA', start, end, conn, color='cadetblue')
    c = pf.add_to_plot(p, 'A1GND5VRF', 'IGDP_NRSD_ALG_A1GND5VRF', start, end, conn, color='chartreuse')
    d = pf.add_to_plot(p, 'A1VDD3P3', 'INRSD_ALG_A1_VDD3P3', start, end, conn, color='chocolate')
    e = pf.add_to_plot(p, 'VDD', 'INRSD_ALG_A1_VDD', start, end, conn, color='coral')
    f = pf.add_to_plot(p, 'REF', 'INRSD_ALG_A1_REF', start, end, conn, color='darkorange')
    g = pf.add_to_plot(p, 'DSUB_V', 'INRSD_A1_DSUB_V', start, end, conn, color='crimson')
    h = pf.add_to_plot(p, 'VRESET_V', 'INRSD_A1_VRESET_V', start, end, conn, color='cyan')
    i = pf.add_to_plot(p, 'CELLDRN_V', 'INRSD_A1_CELLDRN_V', start, end, conn, color='darkblue')
    j = pf.add_to_plot(p, 'DRAIN_V', 'INRSD_A1_DRAIN_V', start, end, conn, color='darkgreen')
    k = pf.add_to_plot(p, 'VBIASGATE_V', 'INRSD_A1_VBIASGATE_V', start, end, conn, color='darkmagenta')
    l = pf.add_to_plot(p, 'VBIASPWR_V', 'INRSD_A1_VBIASPWR_V', start, end, conn, color='cornflowerblue')
    pf.add_hover_tool(p, [a, b, c, d, e, f, g, h, i, j, k, l])
    p.legend.location = 'bottom_right'
    p.legend.click_policy = 'hide'
    return p


def asic_2_voltages(conn, start, end):
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
      plot_height=800,
      x_axis_type='datetime',
      output_backend='webgl',
      x_axis_label='Date',
      y_axis_label='Voltage (V)')
    p.grid.visible = True
    p.title.text = 'ASIC 2 Voltages'
    pf.add_basic_layout(p)
    a = pf.add_to_plot(p, 'VDDA', 'IGDP_NRSD_ALG_A2_VDDA', start, end, conn, color='burlywood')
    b = pf.add_to_plot(p, 'A2GND4VDA', 'IGDP_NRSD_ALG_A2GND4VDA', start, end, conn, color='cadetblue')
    c = pf.add_to_plot(p, 'A2GND5VRF', 'IGDP_NRSD_ALG_A2GND5VRF', start, end, conn, color='chartreuse')
    d = pf.add_to_plot(p, 'A2VDD3P3', 'INRSD_ALG_A2_VDD3P3', start, end, conn, color='chocolate')
    e = pf.add_to_plot(p, 'VDD', 'INRSD_ALG_A2_VDD', start, end, conn, color='coral')
    f = pf.add_to_plot(p, 'REF', 'INRSD_ALG_A2_REF', start, end, conn, color='darkorange')
    g = pf.add_to_plot(p, 'DSUB_V', 'INRSD_A2_DSUB_V', start, end, conn, color='crimson')
    h = pf.add_to_plot(p, 'VRESET_V', 'INRSD_A2_VRESET_V', start, end, conn, color='cyan')
    i = pf.add_to_plot(p, 'CELLDRN_V', 'INRSD_A2_CELLDRN_V', start, end, conn, color='darkblue')
    j = pf.add_to_plot(p, 'DRAIN_V', 'INRSD_A2_DRAIN_V', start, end, conn, color='darkgreen')
    k = pf.add_to_plot(p, 'VBIASGATE_V', 'INRSD_A2_VBIASGATE_V', start, end, conn, color='darkmagenta')
    l = pf.add_to_plot(p, 'VBIASPWR_V', 'INRSD_A2_VBIASPWR_V', start, end, conn, color='cornflowerblue')
    pf.add_hover_tool(p, [a, b, c, d, e, f, g, h, i, j, k, l])
    p.legend.location = 'bottom_right'
    p.legend.click_policy = 'hide'
    return p


def asic_1_currents(conn, start, end):
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
      y_axis_label='Current (mA)')
    p.grid.visible = True
    p.title.text = 'ASIC 1 Currents'
    pf.add_basic_layout(p)
    a = pf.add_to_plot(p, 'VDD_C', 'IGDP_NRSD_ALG_A1_VDD_C', start, end, conn, color='burlywood')
    b = pf.add_to_plot(p, 'A1VDAP12C', 'IGDP_NRSD_ALG_A1VDAP12C', start, end, conn, color='cadetblue')
    c = pf.add_to_plot(p, 'A1VDAN12C', 'IGDP_NRSD_ALG_A1VDAN12C', start, end, conn, color='chartreuse')
    d = pf.add_to_plot(p, 'VDDA_I', 'INRSD_A1_VDDA_I', start, end, conn, color='chocolate')
    pf.add_hover_tool(p, [a, b, c, d])
    p.legend.location = 'bottom_right'
    p.legend.click_policy = 'hide'
    p.legend.orientation = 'horizontal'
    return p


def asic_2_currents(conn, start, end):
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
      y_axis_label='Current (mA)')
    p.grid.visible = True
    p.title.text = 'ASIC 2 Currents'
    pf.add_basic_layout(p)
    a = pf.add_to_plot(p, 'VDD_C', 'IGDP_NRSD_ALG_A2_VDD_C', start, end, conn, color='burlywood')
    b = pf.add_to_plot(p, 'A2VDAP12C', 'IGDP_NRSD_ALG_A2VDAP12C', start, end, conn, color='cadetblue')
    c = pf.add_to_plot(p, 'A2VDAN12C', 'IGDP_NRSD_ALG_A2VDAN12C', start, end, conn, color='chartreuse')
    d = pf.add_to_plot(p, 'VDDA_I', 'INRSD_A2_VDDA_I', start, end, conn, color='chocolate')
    pf.add_hover_tool(p, [a, b, c, d])
    p.legend.location = 'bottom_right'
    p.legend.click_policy = 'hide'
    p.legend.orientation = 'horizontal'
    return p


def fpe_fpa_plots(conn, start, end):
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
    descr = Div(text='\n    <style>\n    table, th, td {\n      border: 1px solid black;\n      background-color: #efefef;\n      border-collapse: collapse;\n      padding: 5px\n    }\n    table {\n      border-spacing: 15px;\n    }\n    </style>\n\n    <body>\n    <table style="width:100%">\n      <tr>\n        <th><h6>Plotname</h6></th>\n        <th><h6>Mnemonic</h6></th>\n        <th><h6>Description</h6></th>\n      </tr>\n      <tr>\n        <td>ASIC (1,2) Voltages</td>\n        <td>IGDP_NRSD_ALG_A(1,2)_VDDA<br>\n            IGDP_NRSD_ALG_A(1,2)GND4VDA<br>\n            IGDP_NRSD_ALG_A(1,2)GND5VRF<br>\n            INRSD_ALG_A(1,2)_VDD3P3<br>\n            INRSD_ALG_A(1,2)_VDD<br>\n            INRSD_ALG_A(1,2)_REF<br>\n            INRSD_A(1,2)_DSUB_V<br>\n            INRSD_A(1,2)_VRESET_V<br>\n            INRSD_A(1,2)_CELLDRN_V<br>\n            INRSD_A(1,2)_DRAIN_V<br>\n            INRSD_A(1,2)_VBIASGATE_V<br>\n            INRSD_A(1,2)_VBIASPWR_V<br>\n        </td>\n        <td>\n            ASIC (1,2) VDDA Voltage<br>\n            ASIC (1,2) VDDA/Ground Voltage<br>\n            ASIC (1,2) Ref/Ground Voltage<br>\n            ASIC (1,2) VDD 3.3 Supply Voltage<br>\n            ASIC (1,2) VDD Voltage<br>\n            ASIC (1,2) Reference Voltage<br>\n            ASIC (1,2) Dsub Voltage<br>\n            ASIC (1,2) Reset Voltage<br>\n            ASIC (1,2) Cell Drain Voltage<br>\n            ASIC (1,2) Drain Voltage<br>\n            ASIC (1,2) Bias Gate Voltage<br>\n            ASIC (1,2) Bias Power Voltage<br>\n        </td>\n      </tr>\n\n      <tr>\n        <td>ASIC (1,2) Currents</td>\n        <td>IGDP_NRSD_ALG_A(1,2)_VDD_C<br>\n            IGDP_NRSD_ALG_A(1,2)VDAP12C<br>\n            IGDP_NRSD_ALG_A(1,2)VDAN12C<br>\n            INRSD_A(1,2)_VDDA_I<br>\n        </td>\n        <td>ASIC (1,2) VDD Current<br>\n            ASIC (1,2) VDDA +12V Current<br>\n            ASIC (1,2) VDDA -12V Current<br>\n            ASIC (1,2) VDDA Current<br>\n        </td>\n      </tr>\n      \n    </table>\n    </body>\n    ',
      width=1100)
    plot1 = asic_1_voltages(conn, start, end)
    plot2 = asic_2_voltages(conn, start, end)
    plot3 = asic_1_currents(conn, start, end)
    plot4 = asic_2_currents(conn, start, end)
    currents = Row(plot3, plot4)
    layout = Column(descr, plot1, plot2, currents)
    tab = Panel(child=layout, title='FPE/FPA')
    return tab