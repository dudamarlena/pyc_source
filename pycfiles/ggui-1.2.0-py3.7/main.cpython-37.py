# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\ggui\main.py
# Compiled at: 2019-12-29 04:15:56
# Size of source mod 2**32: 10783 bytes
"""
.. module:: ggui
    :synopsis: Defines the gGui class and startup behavior
.. moduleauthor:: Duy Nguyen <dnguyen@nrao.edu>
"""
import argparse, pathlib, tempfile, urllib
from urllib.parse import urlparse
import webbrowser, yaml
from zipfile import ZipFile
from glue.core import DataCollection
from glue.app.qt.application import GlueApplication
from glue.config import menubar_plugin
from glue.utils import nonpartial
from PyQt5 import QtWidgets, QtCore
from ggui import qtTabLayouts
from ggui.targetManager import TargetManager
from ggui.make_param import validate_target_catalog_file
from .version import __version__
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

class gGuiGlueApplication(GlueApplication):
    __doc__ = 'Primary gGui Application Class\n    Integrates gGui framework (target manager, custom tab generation, etc.) into Glue\n    '

    def __init__(self, data_collection=DataCollection(), imported_target_catalogs=None):
        """Initializes gGui
        If provided a dictionary of targets, in outlined gGui YAML structure,
        it will load those targets into the target manager

        :param data_collection: Glue data collection containing Glue data to plot
        :param imported_target_catalogs: Dict of targets and paths to associated gPhoton data products to load initially
        """
        super().__init__(data_collection)
        self.setWindowTitle('gGui: gPhoton Graphical User Interface')
        self.menuBar().actions()[0].menu().addSeparator()
        self.menuBar().actions()[0].menu().addAction('Load gGui Target Catalog', self.load_ggui_yaml)
        self.menuBar().actions()[6].setText('&Glue Help')
        menu_about_ggui = self.menuBar().addMenu('&gGui Help')
        ggui_rtd = QtWidgets.QAction('gGui &Online Documentation', menu_about_ggui)
        ggui_rtd.triggered.connect(nonpartial(webbrowser.open, 'https://ggui.readthedocs.io/'))
        menu_about_ggui.addAction(ggui_rtd)
        menu_about_ggui.addAction('About gGui', self.show_about_ggui)
        menu_about_ggui.addAction('Load gGui Sample Data', self.ggui_tutorial)
        default_tab = self.current_tab

        def init_overview_tab(self):
            self.overview_widget = qtTabLayouts.ggui_overview_tab(session=(self.session))
            self.tab_widget.addTab(self.overview_widget, 'gGui Overview Tab: No Data Loaded')
            self.tab_widget.setCurrentWidget(self.overview_widget)

        init_overview_tab(self)
        self.target_manager = TargetManager(self, self.primary_target_changed)
        self.addToolBarBreak()
        self.addToolBar(self.target_manager)
        if imported_target_catalogs:
            self.load_targets(imported_target_catalogs)
        self.close_tab(self.get_tab_index(default_tab), False)

    def closeEvent(self, event):
        """Handles subwindows when gGui is closed"""
        self.target_manager.close()

    def primary_target_changed(self, _):
        """Updates tab data of new primary target
        Indended as signal callback for the target manager to notify gGui of primary target changes
        """
        self.overview_widget.load_data(self.session, self.target_manager.getPrimaryName(), self.target_manager.getPrimaryData())
        self.tab_widget.setTabText(self.get_tab_index(self.overview_widget), 'Overview of ' + str(self.target_manager.getPrimaryName()))

    def load_targets(self, imported_target_catalogs: dict):
        """
        Imports gGui-compliant data (see yaml standard) into target manager

        :param imported_target_catalogs: Dict of gGui yamls and filenames imported from main
        """
        for filename in imported_target_catalogs:
            self.target_manager.loadTargetDict(filename, imported_target_catalogs[filename])

    def load_ggui_yaml(self):
        """Prompts user with File Dialog for gGui YAML Target List
        Validates the YAML file and loads it into the Target Manager
        """
        for ggui_yaml_file in gGuiGlueApplication.prompt_user_for_file('Select GGUI YAML Target List', 'gGUI YAML (*.yaml; *.yml)'):
            self.target_manager.loadTargetDict(ggui_yaml_file, validate_targlist_format(yaml.load((open(ggui_yaml_file, 'r')), Loader=(yaml.BaseLoader)), ggui_yaml_file))

    def show_about_ggui(self):
        """Displays about gGui Message Box"""
        QtWidgets.QMessageBox.about(self, 'About gGui', 'gPhoton Graphical User Interface (gGui)\nDeveloped by Duy Nguyen, Scott Fleming\nVersion: ' + __version__ + '\n\ngGui is provided under the AURA Software License. Please see the included license for details.')

    def ggui_tutorial(self):
        """Loads gGui sample data"""
        sample_data_url = 'https://github.com/gphoton-tools/ggui/raw/master/docs/ggui_tutorial_data2019-11-11.zip'
        sample_filename = pathlib.Path(urlparse(sample_data_url).path).name
        sample_data_local_path = pathlib.Path(tempfile.gettempdir()) / sample_filename
        if not sample_data_local_path.is_file():
            print('Downloading sample data to: ' + str(sample_data_local_path) + ' from: ' + str(sample_data_url))
            urllib.request.urlretrieve(sample_data_url, str(sample_data_local_path))
            print('Download Successful: ' + str(sample_data_local_path.is_file()))
        with ZipFile(sample_data_local_path, 'r') as (sample_data_zip):
            sample_data_zip.extractall(tempfile.gettempdir())
            resolved_path = (pathlib.Path(tempfile.gettempdir()) / 'tutorial.yaml').resolve()
            self.load_targets({resolved_path: validate_target_catalog_file(str(resolved_path))})

    @staticmethod
    def prompt_user_for_file(dialog_caption: str, dialog_name_filter: str) -> list:
        """
        Modular QtWidget File-Selection Dialog to prompt user for file import.
        Returns array of filenames selected

        :param dialog_caption: Caption to display along top of file dialog window
        :param dialog_name_filter: Filters file dialog to certain extension
        """
        dialog = QtWidgets.QFileDialog(caption=dialog_caption)
        dialog.setFileMode(QtWidgets.QFileDialog.ExistingFiles)
        dialog.setNameFilter(dialog_name_filter)
        dialog.exec_()
        filenames = dialog.selectedFiles()
        return filenames


def main(user_arguments: list=None):
    """Entry point/helper function to start ggui

    :param user_arguments: list of arguments, should simulate command line args. Use ['-h'] or ['--help'] for help documentation
    """
    parser = argparse.ArgumentParser(description='gPhoton Graphical User Interface. An analysis package for GALEX gPhoton data products')
    parser.add_argument('--target_list',
      nargs='+',
      help='Specify a path to a YAML style list of astronomical targets and associated gPhoton data products')
    parser.add_argument('--yaml_select',
      action='store_true',
      help='Spawns a file select dialog to choose a YAML style list of astronomical targets and associated gPhoton data products')
    if user_arguments:
        args = parser.parse_args(user_arguments)
    else:
        args = parser.parse_args()
    target_data_products = {}
    if args.target_list:
        for ggui_yaml_file in args.target_list:
            resolved_path = pathlib.Path(ggui_yaml_file).resolve()
            target_data_products[resolved_path] = validate_target_catalog_file(str(resolved_path))

    if args.yaml_select:
        x = QtWidgets.QApplication([])
        for ggui_yaml_file in gGuiGlueApplication.prompt_user_for_file('Select GGUI YAML Target List', 'gGUI YAML (*.yaml; *.yml)'):
            resolved_path = pathlib.Path(ggui_yaml_file).resolve()
            target_data_products[resolved_path] = validate_target_catalog_file(str(resolved_path))

    if not target_data_products:
        print('No yaml received. Starting empty gGui session...')
    ggui_app = gGuiGlueApplication(imported_target_catalogs=target_data_products)
    ggui_app.start()


if __name__ == '__main__':
    main()