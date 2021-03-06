# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\ggui\ggui.py
# Compiled at: 2019-07-01 22:48:28
# Size of source mod 2**32: 8017 bytes
"""
.. module:: ggui
    :synopsis: Defines the gGui class and startup behavior
.. moduleauthor:: Duy Nguyen <dnguyen@nrao.edu>
"""
import argparse, pathlib, yaml
from glue.core import DataCollection
from glue.app.qt.application import GlueApplication
from glue.config import menubar_plugin
from PyQt5 import QtWidgets
from ggui import qtTabLayouts
from ggui.targetManager import target_manager

class ggui_glue_application(GlueApplication):
    __doc__ = 'Primary gGui Application Class\n    Integrates gGui framework (target manager, custom tab generation, etc.) into Glue\n    '

    def __init__(self, data_collection=DataCollection(), target_dict=None):
        """Initializes gGui
        If provided a dictionary of targets, in outlined gGui YAML structure, it will load those targets into the target manager

        :param data_collection: Glue data collection containing Glue data to plot
        :param target_dict: Dict of targets and paths to associated gPhoton data products to load initially
        """
        super().__init__(data_collection)
        default_tab = self.current_tab

        def init_overview_tab(self):
            self.overview_widget = qtTabLayouts.ggui_overview_tab(session=(self.session))
            self.tab_widget.addTab(self.overview_widget, 'gGui Overview Tab: No Data Loaded')
            self.tab_widget.setCurrentWidget(self.overview_widget)

        init_overview_tab(self)
        self.target_manager = target_manager(self, self.primary_target_changed)
        self.addToolBar(self.target_manager)
        if target_dict:
            print(str(len(target_dict.keys())) + ' targets received. Loading ' + str(list(target_dict.keys())[0]) + ' as default.')
            self.load_targets(target_dict)
        self.close_tab(self.get_tab_index(default_tab), False)

    def primary_target_changed(self, _):
        """Updates tab data of new primary target
        Indended as signal callback for the target manager to notify gGui of primary target changes
        """
        self.overview_widget.load_data(self.session, self.target_manager.getPrimaryName(), self.target_manager.getPrimaryData())
        self.tab_widget.setTabText(self.get_tab_index(self.overview_widget), 'Overview of ' + str(self.target_manager.getPrimaryName()))

    def load_targets(self, target_dict: dict):
        """
        Imports gGui-compliant data (see yaml standard) into target manager

        :param target_dict: Dict of targets and paths to associated gPhoton data products
        """
        self.target_manager.loadTargetDict(target_dict)

    def create_overview_widget(self, target_name: str, target_data: dict):
        """
        Creates an overview tab of gPhoton lightcurve, coadd, and cube data.
        Automatically constructs the tab, adds it to gGui and sets focus to it.

        :param target_name: The name of the target
        :param target_data: The corresponding gPhoton data of the target
        """
        self.overview_widget = qtTabLayouts.ggui_overview_tab(session=(self.session), target_name=target_name, target_data=target_data)
        self.tab_widget.addTab(self.overview_widget, 'Overview of ' + str(target_name))
        self.tab_widget.setCurrentWidget(self.overview_widget)


def main(user_arguments: list=None):
    """Entry point/helper function to start ggui

    :param user_arguments: list of arguments, should simulate command line args. Use ['-h'] or ['--help'] for help documentation
    """
    parser = argparse.ArgumentParser(description='gPhoton Graphical User Interface. An analysis package for GALEX gPhoton data products')
    parser.add_argument('--target_list', help='Specify a path to a YAML style list of astronomical targets and associated gPhoton data products')
    parser.add_argument('--yaml_select', action='store_true', help='Spawns a file select dialog to choose a YAML style list of astronomical targets and associated gPhoton data products')
    if user_arguments:
        args = parser.parse_args(user_arguments)
    else:
        args = parser.parse_args()
    target_data_products = {}

    def validate_targlist_format(target_list: dict, list_source: str) -> dict:
        empty_targets = []
        for target_name, target_data in target_list.items():
            valid_files = 0
            for data_type, band_data in target_data.items():
                for band, filepathString in band_data.items():
                    if not pathlib.Path(filepathString).is_file():
                        if filepathString:
                            print(filepathString + ' does not exist on disk. Ignoring...')
                    else:
                        valid_files += 1

            if not valid_files:
                empty_targets.append(target_name)

        for bad_target in empty_targets:
            print(str(bad_target) + ' does not have any valid data. Ignoring target...')
            del target_list[bad_target]

        return target_list

    if args.target_list:
        print('File received: ' + str(args.target_list))
        target_list_path = pathlib.Path(args.target_list)
        target_data_products.update(validate_targlist_format(yaml.load((open(str(target_list_path), 'r')), Loader=(yaml.BaseLoader)), str(target_list_path)))
    if args.yaml_select:

        def prompt_user_for_file(dialogCaption: str, dialogNameFilter: str) -> list:
            """
            Modular QtWidget File-Selection Dialog to prompt user for file import.
            Returns array of filenames selected

            :param dialogCaption: Caption to display along top of file dialog window
            :param dialogNameFilter: Filters file dialog to certain extension
            """
            x = QtWidgets.QApplication([])
            dialog = QtWidgets.QFileDialog(caption=dialogCaption)
            dialog.setFileMode(QtWidgets.QFileDialog.ExistingFiles)
            dialog.setNameFilter(dialogNameFilter)
            dialog.exec_()
            filenames = dialog.selectedFiles()
            return filenames

        for ggui_yaml_file in prompt_user_for_file('Select GGUI YAML Target List', 'gGUI YAML (*.yaml; *.yml)'):
            target_data_products.update(validate_targlist_format(yaml.load((open(ggui_yaml_file, 'r')), Loader=(yaml.BaseLoader)), ggui_yaml_file))

    if not target_data_products:
        print('No yaml received. Starting empty gGui session...')
    ggui_app = ggui_glue_application(target_dict=target_data_products)
    ggui_app.start()


if __name__ == '__main__':
    main()