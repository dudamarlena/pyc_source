# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/taurus/qt/qtdesigner/extraguiqwtplugin.py
# Compiled at: 2019-08-19 15:09:29
"""
guiqwt widgets plugins for Qt Designer
"""
try:
    from guiqwt.qtdesigner import create_qtdesigner_plugin
    PlotPlugin = create_qtdesigner_plugin('guiqwt', 'guiqwt.plot', 'CurveWidget', icon='curve.png')
    ImagePlotPlugin = create_qtdesigner_plugin('guiqwt', 'guiqwt.plot', 'ImageWidget', icon='image.png')
except ImportError:
    from taurus.core.util.log import debug
    debug('failed to load guiqwt designer plugin')