# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/taurus/qt/qtgui/style/nebula.py
# Compiled at: 2019-08-19 15:09:30
"""This module contains a taurus qt style called nebula"""
__all__ = [
 'getStyle', 'getStyleSheet']
__docformat__ = 'restructuredtext'
from taurus.external.qt import Qt
_NEBULA_KEYS = {'border_radius': '4px', 
   'titlebar_background_color': 'qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 rgb(200, 200, 200), stop: 1 rgb(150, 150, 150))', 
   'selected_titlebar_background_color': 'qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 rgb(60, 150, 255), stop: 1 rgb(0, 65, 200))', 
   'single_titlebar_background_color': 'qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 rgb(90, 180, 255), stop: 1 rgb(30, 95, 250))', 
   'titlebar_color': 'white', 
   'selected_titlebar_color': 'white', 
   'content_background_color': 'qlineargradient(x1: 0, y1: 0, x2: 1.0, y2: 1.0, stop: 0 rgb(224, 224, 224), stop: 1 rgb(255, 255, 255))'}
_NEBULA_STYLESHEET = 'QToolBox:tab {{\n    color: {titlebar_color};\n    border-width: 0px;\n    border-style: solid;\n    border-color: rgb(0, 65, 200);\n    border-top-left-radius: 0px;\n    border-top-right-radius: {border_radius};\n    border-bottom-left-radius: {border_radius};\n    border-bottom-right-radius: {border_radius};\n    background-color: {titlebar_background_color};\n}}\n\nQToolBox:tab:selected {{\n    background-color: {selected_titlebar_background_color};\n}}\n\nQToolBox:tab:first {{\n    border-top-left-radius: 0px;\n    border-top-right-radius: 0px;\n}}\n\nQToolBox:tab:last {{\n    border-bottom-left-radius: 0px;\n    border-bottom-right-radius: 0px;\n}}\n\nQToolBox:tab:only-one {{\n    background-color: {single_titlebar_background_color};\n}}\n\nQDockWidget {{\n    color: {titlebar_color};\n    background-color: {content_background_color};\n    titlebar-close-icon: url(:/titlebar_close_black.png);\n    titlebar-normal-icon: url(:/titlebar_undock_black.png);\n}}\n\nQDockWidget::title {{\n    text-align: left;\n    padding-left: {border_radius};\n\n    border-top-left-radius: {border_radius};\n    border-top-right-radius: {border_radius};\n    border-bottom-left-radius: {border_radius};\n    border-bottom-right-radius: {border_radius};\n\n    background-color: {selected_titlebar_background_color};\n}}\n\n QGroupBox {{\n    border: 1px solid;\n    border-color: rgb(0, 65, 200);\n    border-radius: {border_radius};\n    margin-top: 1.5ex;\n    padding-top: 8px;\n    background-color: {content_background_color};\n }}\n\nQGroupBox::title {{\n    subcontrol-origin: margin;\n    subcontrol-position: top left;\n    padding-top: 1px;\n    padding-right: 3px;\n    padding-bottom: 2px;\n    padding-left: 3px;\n    border-width: 0px;\n    border-radius: {border_radius};\n    color:white;\n    background-color: {selected_titlebar_background_color};\n    left: 5px;\n}}\n\n QGroupBox::indicator {{\n    width: 15px;\n    height: 15px;\n}}\n\nQTabWidget {{\n\n}}\n\nQTabWidget::tab-bar {{\n    left: 6px;\n}}\n\nQTabWidget::pane {{\n    border: 1px solid;\n    border-color: rgb(0, 65, 200);\n    border-top-left-radius: {border_radius};\n    border-top-right-radius: {border_radius};\n    border-bottom-left-radius: {border_radius};\n    border-bottom-right-radius: {border_radius};\n    background-color: {content_background_color};\n}}\n\nQTabBar::tab {{\n    color:white;\n    border-bottom-color: rgb(0, 65, 200);\n    background-color: {titlebar_background_color};\n    min-width: 8ex;\n    padding: 2px;\n}}\n\nQTabBar::tab:top {{\n    border-top-left-radius: {border_radius};\n    border-top-right-radius: {border_radius};\n}}\n\nQTabBar::tab:bottom {{\n    border-bottom-left-radius: {border_radius};\n    border-bottom-right-radius: {border_radius};\n}}\n\nQTabBar::tab:selected {{\n    background-color: {selected_titlebar_background_color};\n}}\n\n\n/*\n QMainWindow::separator {{\n    background: yellow;\n    width: 2px;\n    height: 2px;\n }}\n\n QMainWindow::separator:hover {{\n    background: red;\n }}\n\n */\n\n\n'
NEBULA_STYLESHEET = _NEBULA_STYLESHEET.format(**_NEBULA_KEYS)

def getStyle():
    return


def getStyleSheet():
    return NEBULA_STYLESHEET