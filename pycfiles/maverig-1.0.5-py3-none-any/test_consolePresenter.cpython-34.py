# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\Sascha\Documents\PycharmProjects\maverig\maverig\tests\test_consolePresenter.py
# Compiled at: 2014-11-03 15:02:55
# Size of source mod 2**32: 2485 bytes
import gettext, locale, sys
from unittest import TestCase
from PySide import QtCore, QtGui
from maverig.models.model import Model
from maverig.presenter.presenterManager import PresenterManager
from maverig.data import dataHandler
from maverig.views.consolePanelView import ConsolePanelView
from maverig.views.menuBarView import MenuBarView
try:
    app = QtGui.QApplication(sys.argv)
except RuntimeError:
    app = QtCore.QCoreApplication.instance()

class TestStatusBarPresenter(TestCase):

    def __init__consolePresenter(self):
        model = Model()
        presenter_manager = PresenterManager(model)
        console_view = ConsolePanelView()
        current_locale, encoding = locale.getdefaultlocale()
        locale_path = dataHandler.get_lang_path()
        language = gettext.translation(current_locale, locale_path, [current_locale])
        language.install()
        presenter_manager.console_panel_presenter.view = console_view
        console_view.associated_presenter = presenter_manager.console_panel_presenter
        console_view.init_ui()
        return presenter_manager.console_panel_presenter

    def test_on_output(self):
        console_panel_presenter = self._TestStatusBarPresenter__init__consolePresenter()
        test_message = 'Testing'
        console_panel_presenter.on_output(test_message)
        assert console_panel_presenter.view.txt_edit_console.document().isEmpty() == False