# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/jwql/instrument_monitors/nirspec_monitors/data_trending/plots/temperature_tab.py
# Compiled at: 2019-08-26 11:08:03
# Size of source mod 2**32: 21457 bytes
"""Prepares plots for Temperature tab

    Module prepares plots for mnemonics below. Combines plots in a grid and
    returns tab object.

    Plot 1 - IRSU monitored temps
    SI_GZCTS75A / SI_GZCTS75B
    SI_GZCTS68A / SI_GZCTS68B
    SI_GZCTS81A / SI_GZCTS81B
    SI_GZCTS80A / SI_GZCTS80B
    SI_GZCTS76A / SI_GZCTS76B
    SI_GZCTS79A / SI_GZCTS79B
    SI_GZCTS77A / SI_GZCTS77B
    SI_GZCTS78A / SI_GZCTS78B
    SI_GZCTS69A / SI_GZCTS69B

    Plot 2 - Box Temps
    IGDP_NRSD_ALG_TEMP
    INRSH_HK_TEMP1
    INRSH_HK_TEMP2

    Plot 3 - FPE Power Data
    IGDP_NRSI_C_CAM_TEMP
    IGDP_NRSI_C_COL_TEMP
    IGDP_NRSI_C_COM1_TEMP
    IGDP_NRSI_C_FOR_TEMP
    IGDP_NRSI_C_IFU_TEMP
    IGDP_NRSI_C_BP1_TEMP
    IGDP_NRSI_C_BP2_TEMP
    IGDP_NRSI_C_BP3_TEMP
    IGDP_NRSI_C_BP4_TEMP
    IGDP_NRSI_C_RMA_TEMP
    IGDP_NRSI_C_CAAL1_TEMP
    IGDP_NRSI_C_CAAL2_TEMP
    IGDP_NRSI_C_CAAL3_TEMP
    IGDP_NRSI_C_CAAL4_TEMP
    IGDP_NRSI_C_FWA_TEMP
    IGDP_NRSI_C_GWA_TEMP

    Plot 4 - MCE internal Temp
    INRSM_MCE_PCA_TMP1
    INRSM_MCE_PCA_TMP2
    INRSM_MCE_AIC_TMP_FPGA
    INRSM_MCE_AIC_TMP_ADC
    INRSM_MCE_AIC_TMP_VREG
    INRSM_MCE_MDAC_TMP_FPGA
    INRSM_MCE_MDAC_TMP_OSC
    INRSM_MCE_MDAC_TMP_BRD
    INRSM_MCE_MDAC_TMP_PHA
    INRSM_MCE_MDAC_TMP_PHB

    Plot 5 - MSA Temp
    INRSM_Q1_TMP_A
    INRSM_Q2_TMP_A
    INRSM_Q3_TMP_A
    INRSM_Q4_TMP_A
    INRSM_MECH_MTR_TMP_A
    INRSM_LL_MTR_TMP_A
    INRSM_MSA_TMP_A

    Plot 6 - FPA Temp
    IGDP_NRSD_ALG_FPA_TEMP
    IGDP_NRSD_ALG_A1_TEMP
    IGDP_NRSD_ALG_A2_TEMP

    Plot 7 - Heat Strap Temps (Trim heaters)
    SI_GZCTS74A / SI_GZCTS74B
    SI_GZCTS67A / SI_GZCTS67B

Authors
-------
    - Daniel Kühbacher

Use
---
    The functions within this module are intended to be imported and
    used by ``nirspec_dashboard.py``, e.g.:

    ::
        from .plots.temperature_tab import temperature_plots
        tab = temperature_plots(conn, start, end)

Dependencies
------------
    User must provide database "nirspec_database.db"

"""
import jwql.instrument_monitors.nirspec_monitors.data_trending.utils.sql_interface as sql, jwql.instrument_monitors.nirspec_monitors.data_trending.plots.plot_functions as pf
from bokeh.models import LinearAxis, Range1d
from bokeh.plotting import figure
from bokeh.models.widgets import Panel, Tabs, Div
from bokeh.models import ColumnDataSource, HoverTool
from bokeh.layouts import WidgetBox, gridplot, Column
import pandas as pd, numpy as np
from astropy.time import Time

def irsu_temp(conn, start, end):
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
      plot_height=700,
      x_axis_type='datetime',
      output_backend='webgl',
      x_axis_label='Date',
      y_axis_label='Temperature (K)')
    p.grid.visible = True
    p.title.text = 'IRSU monitored Temperatures'
    pf.add_basic_layout(p)
    a = pf.add_to_plot(p, '75A', 'SI_GZCTS75A', start, end, conn, color='red')
    b = pf.add_to_plot(p, '68A', 'SI_GZCTS68A', start, end, conn, color='green')
    c = pf.add_to_plot(p, '81A', 'SI_GZCTS81A', start, end, conn, color='blue')
    d = pf.add_to_plot(p, '80A', 'SI_GZCTS80A', start, end, conn, color='orange')
    e = pf.add_to_plot(p, '76A', 'SI_GZCTS76A', start, end, conn, color='brown')
    f = pf.add_to_plot(p, '79A', 'SI_GZCTS79A', start, end, conn, color='cyan')
    g = pf.add_to_plot(p, '77A', 'SI_GZCTS77A', start, end, conn, color='darkmagenta')
    h = pf.add_to_plot(p, '78A', 'SI_GZCTS78A ', start, end, conn, color='burlywood')
    i = pf.add_to_plot(p, '69A', 'SI_GZCTS69A ', start, end, conn, color='chocolate')
    pf.add_hover_tool(p, [a, b, c, d, e, f, g, h, i])
    p.legend.location = 'bottom_right'
    p.legend.click_policy = 'hide'
    p.legend.orientation = 'horizontal'
    return p


def fpe_temp(conn, start, end):
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
      plot_height=700,
      x_axis_type='datetime',
      output_backend='webgl',
      x_axis_label='Date',
      y_axis_label='Temperature (K)')
    p.grid.visible = True
    p.title.text = 'FPE Temperatures'
    pf.add_basic_layout(p)
    a = pf.add_to_plot(p, 'CAM', 'IGDP_NRSI_C_CAM_TEMP', start, end, conn, color='red')
    b = pf.add_to_plot(p, 'COL', 'IGDP_NRSI_C_COL_TEMP', start, end, conn, color='green')
    c = pf.add_to_plot(p, 'COM1', 'IGDP_NRSI_C_COM1_TEMP', start, end, conn, color='blue')
    d = pf.add_to_plot(p, 'FOR', 'IGDP_NRSI_C_FOR_TEMP', start, end, conn, color='darkorange')
    e = pf.add_to_plot(p, 'IFU', 'IGDP_NRSI_C_IFU_TEMP', start, end, conn, color='cyan')
    f = pf.add_to_plot(p, 'BP1', 'IGDP_NRSI_C_BP1_TEMP', start, end, conn, color='darkmagenta')
    g = pf.add_to_plot(p, 'BP2', 'IGDP_NRSI_C_BP2_TEMP', start, end, conn, color='burlywood')
    h = pf.add_to_plot(p, 'BP3', 'IGDP_NRSI_C_BP3_TEMP', start, end, conn, color='brown')
    i = pf.add_to_plot(p, 'BP4', 'IGDP_NRSI_C_BP4_TEMP', start, end, conn, color='chocolate')
    j = pf.add_to_plot(p, 'RMA', 'IGDP_NRSI_C_RMA_TEMP', start, end, conn, color='darkgreen')
    pf.add_hover_tool(p, [a, b, c, d, e, f, g, h, i, j])
    p.legend.location = 'bottom_right'
    p.legend.click_policy = 'hide'
    p.legend.orientation = 'horizontal'
    return p


def caal_temp(conn, start, end):
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
      plot_height=700,
      x_axis_type='datetime',
      output_backend='webgl',
      x_axis_label='Date',
      y_axis_label='Temperature (K)')
    p.grid.visible = True
    p.title.text = 'CAA Lamps / FWA, GWA'
    pf.add_basic_layout(p)
    a = pf.add_to_plot(p, 'CAAL1', 'IGDP_NRSI_C_CAAL1_TEMP', start, end, conn, color='darkblue')
    b = pf.add_to_plot(p, 'CAAL2', 'IGDP_NRSI_C_CAAL2_TEMP', start, end, conn, color='magenta')
    c = pf.add_to_plot(p, 'CAAL3', 'IGDP_NRSI_C_CAAL3_TEMP', start, end, conn, color='mediumaquamarine')
    d = pf.add_to_plot(p, 'CAAL4', 'IGDP_NRSI_C_CAAL4_TEMP', start, end, conn, color='goldenrod')
    e = pf.add_to_plot(p, 'FWA', 'IGDP_NRSI_C_FWA_TEMP', start, end, conn, color='darkseagreen')
    f = pf.add_to_plot(p, 'GWA', 'IGDP_NRSI_C_GWA_TEMP', start, end, conn, color='darkkhaki')
    pf.add_hover_tool(p, [a, b, c, d, e, f])
    p.legend.location = 'bottom_right'
    p.legend.click_policy = 'hide'
    p.legend.orientation = 'horizontal'
    return p


def box_temp(conn, start, end):
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
      plot_height=700,
      x_axis_type='datetime',
      output_backend='webgl',
      x_axis_label='Date',
      y_axis_label='Temperature (K)')
    p.grid.visible = True
    p.title.text = 'Box Temperatures'
    pf.add_basic_layout(p)
    a = pf.add_to_plot(p, 'ALG_TEMP', 'IGDP_NRSD_ALG_TEMP', start, end, conn, color='red')
    b = pf.add_to_plot(p, 'HK_TEMP1', 'INRSH_HK_TEMP1', start, end, conn, color='green')
    c = pf.add_to_plot(p, 'HK_TEMP2', 'INRSH_HK_TEMP2', start, end, conn, color='blue')
    pf.add_hover_tool(p, [a, b, c])
    p.legend.location = 'bottom_right'
    p.legend.click_policy = 'hide'
    p.legend.orientation = 'horizontal'
    return p


def mce_internal_temp(conn, start, end):
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
      plot_height=700,
      x_axis_type='datetime',
      output_backend='webgl',
      x_axis_label='Date',
      y_axis_label='Temperature (K)')
    p.grid.visible = True
    p.title.text = 'MCE internal Temperatures'
    pf.add_basic_layout(p)
    a = pf.add_to_plot(p, 'PCA_TMP1', 'INRSM_MCE_PCA_TMP1', start, end, conn, color='green')
    b = pf.add_to_plot(p, 'PCA_TMP2', 'INRSM_MCE_PCA_TMP2', start, end, conn, color='blue')
    c = pf.add_to_plot(p, 'FPGA_AIC', 'INRSM_MCE_AIC_TMP_FPGA', start, end, conn, color='brown')
    d = pf.add_to_plot(p, 'ADC_AIC', 'INRSM_MCE_AIC_TMP_ADC', start, end, conn, color='red')
    e = pf.add_to_plot(p, 'VREG_AIC', 'INRSM_MCE_AIC_TMP_VREG', start, end, conn, color='hotpink')
    f = pf.add_to_plot(p, 'FPGA_MDAC', 'INRSM_MCE_MDAC_TMP_FPGA', start, end, conn, color='cadetblue')
    g = pf.add_to_plot(p, 'OSC_MDAC', 'INRSM_MCE_MDAC_TMP_OSC', start, end, conn, color='navy')
    h = pf.add_to_plot(p, 'BRD_MDAC', 'INRSM_MCE_MDAC_TMP_BRD', start, end, conn, color='darkgreen')
    i = pf.add_to_plot(p, 'PHA_MDAC', 'INRSM_MCE_MDAC_TMP_PHA', start, end, conn, color='magenta')
    j = pf.add_to_plot(p, 'PHB_MDAC', 'INRSM_MCE_MDAC_TMP_PHB', start, end, conn, color='orange')
    pf.add_hover_tool(p, [a, b, c, d, e, f, g, h, i, j])
    p.legend.location = 'bottom_right'
    p.legend.click_policy = 'hide'
    p.legend.orientation = 'horizontal'
    return p


def msa_temp(conn, start, end):
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
      plot_height=700,
      x_axis_type='datetime',
      output_backend='webgl',
      x_axis_label='Date',
      y_axis_label='Temperature (K)')
    p.grid.visible = True
    p.title.text = 'MSA Temperatures'
    pf.add_basic_layout(p)
    a = pf.add_to_plot(p, 'Q1_TEMP', 'INRSM_Q1_TMP_A', start, end, conn, color='green')
    b = pf.add_to_plot(p, 'Q2_TEMP', 'INRSM_Q2_TMP_A', start, end, conn, color='red')
    c = pf.add_to_plot(p, 'Q3_TEMP', 'INRSM_Q3_TMP_A', start, end, conn, color='blue')
    d = pf.add_to_plot(p, 'Q4_TEMP', 'INRSM_Q4_TMP_A', start, end, conn, color='brown')
    e = pf.add_to_plot(p, 'MECH_MTR', 'INRSM_MECH_MTR_TMP_A', start, end, conn, color='orange')
    f = pf.add_to_plot(p, 'LL_MTR', 'INRSM_LL_MTR_TMP_A', start, end, conn, color='darkmagenta')
    g = pf.add_to_plot(p, 'MSA', 'INRSM_MSA_TMP_A', start, end, conn, color='indigo')
    pf.add_hover_tool(p, [a, b, c, d, e, f, g])
    p.legend.location = 'bottom_right'
    p.legend.click_policy = 'hide'
    return p


def fpa_temp(conn, start, end):
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
      plot_height=700,
      x_axis_type='datetime',
      output_backend='webgl',
      x_axis_label='Date',
      y_axis_label='Temperature (K)')
    p.grid.visible = True
    p.title.text = 'FPA Temperatures'
    pf.add_basic_layout(p)
    a = pf.add_to_plot(p, 'ALG_FPA', 'IGDP_NRSD_ALG_FPA_TEMP', start, end, conn, color='green')
    b = pf.add_to_plot(p, 'ALG_A1', 'IGDP_NRSD_ALG_A1_TEMP', start, end, conn, color='red')
    c = pf.add_to_plot(p, 'ALG_A2', 'IGDP_NRSD_ALG_A2_TEMP', start, end, conn, color='blue')
    pf.add_hover_tool(p, [a, b, c])
    p.legend.location = 'bottom_right'
    p.legend.click_policy = 'hide'
    return p


def heat_strap_temp(conn, start, end):
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
      plot_height=700,
      x_axis_type='datetime',
      output_backend='webgl',
      x_axis_label='Date',
      y_axis_label='Temperature (K)')
    p.grid.visible = True
    p.title.text = 'Heat Strap Temperatures (Trim heaters)'
    pf.add_basic_layout(p)
    a = pf.add_to_plot(p, '74A', 'SI_GZCTS74A', start, end, conn, color='green')
    b = pf.add_to_plot(p, '67A', 'SI_GZCTS67A', start, end, conn, color='red')
    pf.add_hover_tool(p, [a, b])
    p.legend.location = 'bottom_right'
    p.legend.click_policy = 'hide'
    return p


def temperature_plots(conn, start, end):
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
    descr = Div(text='\n    <style>\n    table, th, td {\n      border: 1px solid black;\n      background-color: #efefef;\n      border-collapse: collapse;\n      padding: 5px\n    }\n    table {\n      border-spacing: 15px;\n    }\n    </style>\n\n    <body>\n    <table style="width:100%">\n      <tr>\n        <th><h6>Plotname</h6></th>\n        <th><h6>Mnemonic</h6></th>\n        <th><h6>Description</h6></th>\n      </tr>\n      <tr>\n        <td>IRSU monitored Temperatures</td>\n        <td>SI_GZCTS75A<br>\n            SI_GZCTS68A<br>\n            SI_GZCTS81A<br>\n            SI_GZCTS80A<br>\n            SI_GZCTS76A<br>\n            SI_GZCTS79A<br>\n            SI_GZCTS77A<br>\n            SI_GZCTS78A<br>\n            SI_GZCTS69A</td>\n        <td>CAA IRSU Temperature<br>\n            CAM IRSU Temperature<br>\n            COM1 Nominal IRSU Temperature<br>\n            COM1 Redundant IRSU Temperature<br>\n            FWA IRSU Temperature<br>\n            GWA IRSU Temperature<br>\n            Thermal Strap Nominal IRSU Temperature<br>\n            Thermal Strap Redundant IRSU Temperature<br>\n            MSA Nominal IRSU Temperature<br>\n            MSA Redundant IRSU Temperature</td>\n      </tr>\n\n      <tr>\n        <td>FPE Temperatures/td>\n        <td>IGDP_NRSI_C_CAM_TEMP<br>\n            IGDP_NRSI_C_COL_TEMP<br>\n            IGDP_NRSI_C_COM1_TEMP<br>\n            IGDP_NRSI_C_FOR_TEMP<br>\n            IGDP_NRSI_C_IFU_TEMP<br>\n            IGDP_NRSI_C_BP1_TEMP<br>\n            IGDP_NRSI_C_BP2_TEMP<br>\n            IGDP_NRSI_C_BP3_TEMP<br>\n            IGDP_NRSI_C_BP4_TEMP<br>\n            IGDP_NRSI_C_RMA_TEMP</td>\n        <td>OA CAM Temperature<br>\n            OA COL Temperature<br>\n            OA COM1 Temperature<br>\n            OA FOR Temperature<br>\n            OA IFU Temperature<br>\n            OA BP1 Temperature<br>\n            OA BP2 Temperature<br>\n            OA BP3 Temperature<br>\n            OA BP4 Temperature<br>\n            OA RMA Temperature</td>\n      </tr>\n\n      <tr>\n        <td>Box Temperatures</td>\n        <td>IGDP_NRSD_ALG_TEMP<br>\n            INRSH_HK_TEMP1<br>\n            INRSH_HK_TEMP2</td>\n        <td>ICE Internal Temperature 1<br>\n            ICE Internal Temperature 2</td>\n      </tr>\n\n      <tr>\n        <td>MCE internal Temperatures</td>\n        <td>INRSM_MCE_PCA_TMP1<br>\n            INRSM_MCE_PCA_TMP2<br>\n            INRSM_MCE_AIC_TMP_FPGA<br>\n            INRSM_MCE_AIC_TMP_ADC<br>\n            INRSM_MCE_AIC_TMP_VREG<br>\n            INRSM_MCE_MDAC_TMP_FPGA<br>\n            INRSM_MCE_MDAC_TMP_OSC<br>\n            INRSM_MCE_MDAC_TMP_BRD<br>\n            INRSM_MCE_MDAC_TMP_PHA<br>\n            INRSM_MCE_MDAC_TMP_PHB</td>\n        <td>MCE PCA Board Temperature 1<br>\n            MCE PCA Board Temperature 2<br>\n            MCE AIC Board FPGA Temperature<br>\n            MCE AIC Board Analog/Digital Converter Temperature<br>\n            MCE AIC Board Voltage Regulator Temperature<br>\n            MCE MDAC Board FPGA Temperature<br>\n            MCE MDAC Board Oscillator Temperature<br>\n            MCE MDAC Board Temperature<br>\n            MCE MDAC Board Phase A PA10 Temperature<br>\n            MCE MDAC Board Phase B PA10 Temperature</td>\n      </tr>\n\n      <tr>\n        <td>MSA Temperatures</td>\n        <td>INRSM_Q1_TMP_A<br>\n            INRSM_Q2_TMP_A<br>\n            INRSM_Q3_TMP_A<br>\n            INRSM_Q4_TMP_A<br>\n            INRSM_MECH_MTR_TMP_A<br>\n            INRSM_LL_MTR_TMP_A<br>\n            INRSM_MSA_TMP_A</td>\n        <td>MSA Quad 1 Temperature<br>\n            MSA Quad 2 Temperature<br>\n            MSA Quad 3 Temperature<br>\n            MSA Quad 4 Temperature<br>\n            MSA Magnetic Arm Motor Temperature<br>\n            MSA Launch Lock Motor Temperature<br>\n            MSA Frame Temperature</td>\n      </tr>\n\n      <tr>\n        <td>FPA Temperatures</td>\n        <td>IGDP_NRSD_ALG_FPA_TEMP<br>\n            IGDP_NRSD_ALG_A1_TEMP<br>\n            IGDP_NRSD_ALG_A2_TEMP</td>\n        <td>FPE Temperature<br>\n            FPA Temperature<br>\n            ASIC 1 Temperature<br>\n            ASIC 2 Temperature</td>\n      </tr>\n\n      <tr>\n        <td>Heat Strap Temperatures (Trim Heaters)</td>\n        <td>SI_GZCTS74A<br>\n            SI_GZCTS67A</td>\n        <td>FPA TH-Strap A Temperature from IRSU A<br>\n            FPA TH-Strap B Temperature from IRSU A</td>\n      </tr>\n\n      <tr>\n        <td>CAA Lamps / FWA,GWA</td>\n        <td>IGDP_NRSI_C_CAAL1_TEMP<br>\n            IGDP_NRSI_C_CAAL2_TEMP<br>\n            IGDP_NRSI_C_CAAL3_TEMP<br>\n            IGDP_NRSI_C_CAAL4_TEMP<br>\n            IGDP_NRSI_C_FWA_TEMP<br>\n            IGDP_NRSI_C_GWA_TEMP</td>\n        <td>CAA Temperature LINE1<br>\n            CAA Temperature LINE2<br>\n            CAA Temperature LINE3<br>\n            CAA Temperature LINE4<br>\n            FWA Temperature Sensor Value<br>\n            GWA Temperature Sensor Value</td>\n      </tr>\n\n    </table>\n    </body>\n    ',
      width=1100)
    plot1 = irsu_temp(conn, start, end)
    plot2 = fpe_temp(conn, start, end)
    plot3 = box_temp(conn, start, end)
    plot4 = mce_internal_temp(conn, start, end)
    plot5 = msa_temp(conn, start, end)
    plot6 = fpa_temp(conn, start, end)
    plot7 = heat_strap_temp(conn, start, end)
    plot8 = caal_temp(conn, start, end)
    layout = Column(descr, plot1, plot2, plot3, plot4, plot5, plot6, plot7, plot8)
    tab = Panel(child=layout, title='TEMPERATURE')
    return tab