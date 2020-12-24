# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\xicam\plugins\zipythonconsole.py
# Compiled at: 2018-08-27 17:21:07
from PySide import QtGui
import sys, base
from xicam import plugins

def new_load_qt(api_options):
    from PySide import QtCore, QtGui, QtSvg
    return (
     QtCore, QtGui, QtSvg, 'pyside')


from qtconsole import qt_loaders
qt_loaders.load_qt = new_load_qt
from qtconsole.rich_jupyter_widget import RichJupyterWidget
from qtconsole.inprocess import QtInProcessKernelManager
import qdarkstyle, os

class IPythonPlugin(base.plugin):
    name = 'IPython'

    def __init__(self, *args, **kwargs):
        with open('xicam/gui/style.stylesheet', 'r') as (f):
            style = f.read()
        style = qdarkstyle.load_stylesheet() + style
        kernel_manager = QtInProcessKernelManager()
        kernel_manager.start_kernel()
        kernel = kernel_manager.kernel
        kernel.gui = 'qt4'
        kernel.shell.push(dict(plugins.plugins))
        kernel_client = kernel_manager.client()
        kernel_client.start_channels()

        def stop():
            kernel_client.stop_channels()
            kernel_manager.shutdown_kernel()

        control = RichJupyterWidget()
        control.kernel_manager = kernel_manager
        control.kernel_client = kernel_client
        control.exit_requested.connect(stop)
        control.style_sheet = style
        control.syntax_style = 'monokai'
        control.set_default_style(colors='Linux')
        self.centerwidget = control
        self.rightwidget = None
        self.featureform = None
        self.bottomwidget = None
        self.leftwidget = None
        self.toolbar = None
        super(IPythonPlugin, self).__init__(*args, **kwargs)
        return