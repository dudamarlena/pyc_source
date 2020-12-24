# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\ggui\targetManager.py
# Compiled at: 2019-12-22 01:36:00
# Size of source mod 2**32: 21207 bytes
"""
.. module:: qtTabLayouts
    :synopsis: Defines the gGui Target Manager to manage multiple targets
.. moduleauthor:: Duy Nguyen <dnguyen@nrao.edu>
"""
from collections import OrderedDict
from configparser import ConfigParser
import itertools
from typing import Callable
from copy import copy
import pathlib, yaml
from PyQt5 import QtWidgets, QtGui, QtCore
from glue.app.qt.application import GlueApplication
from glue.core.link_helpers import LinkSame
from glue.core.data_factories import load_data
from pkg_resources import resource_filename

class TargetManager(QtWidgets.QToolBar):
    __doc__ = '\n    Class that handles the loading of gPhoton data and management of multiple\n    gGui targets\n    '

    def __init__(self, glue_parent, target_change_callback=None):
        """Initializes gGui Target Manager
        If provided a dictionary of targets, in outlined gGui YAML structure, it will load those targets into the target manager

        :param glue_parent: The Glue instance that instantiated this object. Target Manager cannot be run outside a Glue context
        :param target_change_callback: Callback function to notify upon primary target change
        """
        super().__init__()
        self._glue_parent = glue_parent
        self._target_catalog = OrderedDict()
        self._primary_data = {}
        self._target_change_callbacks = []
        self._target_notes = None
        self._note_display_widget = target_note_display(self)
        config = ConfigParser()
        config.read(resource_filename('ggui', 'ggui.conf'))
        self.addWidget(QtWidgets.QLabel('gGui Target Manager: '))
        self.addAction(QtGui.QIcon(resource_filename('ggui.icons', 'ArrowBack_transparent.png')), 'Previous Target', self.previous_target)
        QtWidgets.QShortcut(QtGui.QKeySequence(config.get('Target Manager Shortcuts', 'previous_target', fallback='PgUp')), self).activated.connect(self.previous_target)
        self.QComboBox = QtWidgets.QComboBox(self)
        self.QComboBox.currentIndexChanged.connect(self.setPrimaryTarget)
        self.addWidget(self.QComboBox)
        self.addAction(QtGui.QIcon(resource_filename('ggui.icons', 'ArrowForward_transparent.png')), 'Next Target', self.next_target)
        QtWidgets.QShortcut(QtGui.QKeySequence(config.get('Target Manager Shortcuts', 'next_target', fallback='PgDown')), self).activated.connect(self.next_target)
        self.addAction(QtGui.QIcon(resource_filename('ggui.icons', 'Information.svg')), 'Target Information', self.show_targ_info)
        self.addAction(QtGui.QIcon(resource_filename('ggui.icons', 'Notepad.png')), 'Target Notes', self._note_display_widget.show)
        if target_change_callback:
            self.register_target_change_callback(target_change_callback)

    def close(self):
        """Handles graceful exit housekeeping"""
        self._note_display_widget.close()

    def register_target_change_callback(self, callback):
        """Registers a callback function to call when primary target changes

        :param callback: Callback function
        """
        self._target_change_callbacks.append(callback)

    def loadTargetDict(self, target_catalog: str, target_files: dict):
        """Loads a single dictionary of targets and associated data product paths into internal cache

        :param target_files: gGui compliant yaml dictionary of targets and paths to associated gPhoton data products
        :param target_catalog: Name/identifier of this dictionary of targets. Can be used to return data
        """
        target_catalog = str(pathlib.Path(target_catalog).resolve())
        if target_catalog in self._target_catalog:
            raise ValueError('Duplicate gGui catalog. Catalog already imported into gGui: ' + target_catalog)
        self._target_catalog[target_catalog] = OrderedDict(target_files)
        for item in target_files.keys():
            self.QComboBox.addItem(item, {'target_catalog': target_catalog})

    def setPrimaryTarget(self, targIndex: int):
        """Changes primary target to target specified
        Unloads existing primary target's data (internal cache and parent Glue session),
        loads the new primary target's data, links their corresponding attributes together,
        and notifies all stakeholders of the new changed primary target

        :param targIndex: Index of desired new primary target
        """
        targName = self.QComboBox.currentText()
        targ_catalog = self.QComboBox.currentData()['target_catalog']
        if targName not in self.getTargetNames():
            raise KeyError('Target Manager does not recognize requested target: ' + str(targName))
        if self._primary_data:

            def unload_primary_data():
                for band_data_set in list(self._primary_data.values()):
                    for band_data in band_data_set.values():
                        if isinstance(band_data, list):
                            for data in band_data:
                                self._glue_parent.data_collection.remove(data)

                        else:
                            self._glue_parent.data_collection.remove(band_data)

            unload_primary_data()
        self._note_display_widget.save_notes()
        self._primary_data.clear()
        self._target_notes = None
        target_files = copy(self.getTargetFiles(targ_catalog, targName))
        self._target_notes = target_files.pop('_notes', None)
        for data_product_type in target_files:
            self._primary_data[data_product_type] = {}
            config = ConfigParser()
            config.read(resource_filename('ggui', 'ggui.conf'))
            x_att = config.get('Mandatory Fields', (data_product_type + '_x'), fallback='')
            y_att = config.get('Mandatory Fields', (data_product_type + '_y'), fallback='')
            for band, band_file in target_files[data_product_type].items():
                if band_file:
                    if not pathlib.PurePath(band_file).is_absolute():
                        if '\\' in band_file:
                            band_file = str(pathlib.PurePath(targ_catalog).parent.joinpath(pathlib.PureWindowsPath(band_file)))
                        else:
                            if '/' in band_file:
                                band_file = str(pathlib.PurePath(targ_catalog).parent.joinpath(pathlib.PurePosixPath(band_file)))
                            else:
                                band_file = str(pathlib.PurePath(targ_catalog).parent.joinpath(pathlib.PurePath(band_file)))
                    self._primary_data[data_product_type][band] = load_data(band_file)
                    try:
                        if x_att:
                            self._primary_data[data_product_type][band].id[x_att]
                        if y_att:
                            self._primary_data[data_product_type][band].id[y_att]
                    except KeyError as e:
                        try:
                            parsed_error = e.args[0].split(':')
                            if parsed_error[0] == 'ComponentID not found or not unique':
                                print("WARNING: '" + parsed_error[1].strip() + "' field specified in ggui.conf missing from " + targName + ' ' + data_product_type + ' ' + band + ': ' + band_file)
                                x_att = ''
                                y_att = ''
                            else:
                                raise
                        finally:
                            e = None
                            del e

                    except AttributeError:
                        if isinstance(self._primary_data[data_product_type][band], list):
                            print('WARNING: ' + str(len(self._primary_data[data_product_type][band])) + ' datasets imported from ' + targName + ' ' + data_product_type + ' band ' + band + '. gGui shall import this data, but will be unable to perform automatic actions on it (i.e. gluing, displaying overview, etc.)')
                        else:
                            raise

                    self._glue_parent.data_collection.append(self._primary_data[data_product_type][band])

            try:
                if len(self._primary_data[data_product_type].keys()) > 1:
                    attributes_to_glue = {'lightcurve':[
                      't_mean', 'flux_bgsub'], 
                     'coadd':[
                      'Right Ascension', 'Declination'], 
                     'cube':[
                      'Right Ascension', 'Declination', 'World 0']}
                    for glue_attribute in list(filter(lambda x: x is not '', [x_att, y_att] + config.get('Additional Fields To Glue', data_product_type, fallback='').split(','))):
                        from itertools import permutations
                        for linking_pair in set((frozenset(t) for t in permutations(self._primary_data[data_product_type].values(), 2))):
                            accessor = tuple(linking_pair)
                            self._glue_parent.data_collection.add_link(LinkSame(accessor[0].id[glue_attribute], accessor[1].id[glue_attribute]))

            except TypeError as e:
                try:
                    print('Unable to glue ' + str(targName) + ' ' + str(data_product_type) + ': ' + str(e))
                finally:
                    e = None
                    del e

        for callback in self._target_change_callbacks:
            callback(self.getPrimaryName())

    def setPrimaryNotes(self, new_notes: str):
        """"
        Updates internal cache of target's notes to given string

        :param new_notes: New notes for the primary target
        """
        self._target_notes = new_notes
        self.getTargetFiles(self.getPrimaryTargetCatalog(), self.getPrimaryName())['_notes'] = new_notes

    def getTargetNames(self) -> list:
        """Returns the names of all registered targets, in their registered order

        :returns: list of all cached targets' names
        """
        return list(itertools.chain.from_iterable(self._target_catalog.values()))

    def getTargetFiles(self, target_catalog: str, target_name: str) -> dict:
        """Returns the files and metadata of a specified target (Unloaded data, as per lazy evaluation principle)
        
        :param target_catalog: gGui catalog file this target originated from
        :param target_name: Name of the target whose files to lookup
        :returns: Unloaded metadata and filepaths of the corresponding target's data
        """
        try:
            return self._target_catalog[target_catalog][target_name]
        except KeyError:
            raise KeyError("'" + str(target_name) + "' not found in cache")

    def getTargetNotes(self, target_catalog: str, target_name: str) -> str:
        """Returns the notes specified target, or blank string if no notes registered
        
        :param target_catalog: gGui catalog this target originated from
        :param target_name: Name of the target whose notes to lookup
        :returns: Notes of the specified target, or blank string if no notes
        """
        try:
            return self.getTargetFiles(target_catalog, target_name)['_notes']
        except KeyError:
            return ''

    def getPrimaryData(self) -> dict:
        """Returns currently loaded primary target's data

        :returns: dictionary of the current primary target's data
        """
        return self._primary_data

    def getPrimaryName(self) -> dict:
        """Returns the current primary target's name

        :returns: current primary target's name as string
        """
        return self.QComboBox.currentText()

    def getPrimaryTargetCatalog(self) -> str:
        """Returns the current primary target's parent gGui Target Catalog path
        If no target is selected, returns a blank string

        :returns: primary target's gGui Target Catalog path as string
        """
        try:
            return self.QComboBox.currentData()['target_catalog']
        except TypeError:
            return ''

    def getPrimaryNotes(self) -> str:
        """Returns any notes associated with the current target. Returns empty string if no notes found.

        :returns: notes registered with the current target
        """
        return self._target_notes

    def next_target(self):
        """Advances to next primary target"""
        current_target_index = self.QComboBox.currentIndex()
        next_target_index = current_target_index + 1
        if next_target_index > self.QComboBox.count() - 1:
            next_target_index = 0
        self.QComboBox.setCurrentText(self.QComboBox.itemText(next_target_index))

    def previous_target(self):
        """Advances to previous primary target"""
        current_target_index = self.QComboBox.currentIndex()
        next_target_index = current_target_index - 1
        if next_target_index < 0:
            next_target_index = self.QComboBox.count() - 1
        self.QComboBox.setCurrentText(self.QComboBox.itemText(next_target_index))

    def show_targ_info(self):
        """Displays name and target catalog for the primary target"""
        QtWidgets.QMessageBox(QtWidgets.QMessageBox.Information, 'About Target', 'Target name: ' + str(self.getPrimaryName()) + '\ngGui Target Catalog: ' + str(self.getPrimaryTargetCatalog()), QtWidgets.QMessageBox.Ok).exec()

    def flushSourceFile(self, source_filename: str):
        """Force saves (flushes) the given source file
        Intended to be used for saving notes

        :param source_filename: Filename of source file to be flushed
        """
        with open(source_filename, 'w') as (source_file):
            source_file.write(yaml.dump(dict(self._target_catalog[source_filename])))


class target_note_display(QtWidgets.QGroupBox):
    __doc__ = 'Subwidget to display notes of current target'

    def __init__(self, parent):
        super().__init__()
        self.setWindowTitle('gGui Notepad')
        self._target_manager = parent
        self._target_manager.register_target_change_callback(self.primary_target_changed)
        self._text_field = QtWidgets.QTextEdit()
        self._text_field.document().modificationChanged.connect(self.modificationChanged)
        self._save_button = QtWidgets.QPushButton('Save Notes')
        self.setTitle('Notes: Unmodified')
        self._save_button.setEnabled(False)
        self._save_button.clicked.connect(lambda : self.save_notes(True))
        self._discard_button = QtWidgets.QPushButton('Discard Changes')
        self._discard_button.clicked.connect(self.discard_note_changes)
        self._discard_button.setEnabled(False)
        self._layout = QtWidgets.QGridLayout()
        self.setLayout(self._layout)
        self._layout.addWidget(self._text_field, 0, 0, 1, 2)
        self._layout.addWidget(self._save_button, 1, 0)
        self._layout.addWidget(self._discard_button, 1, 1)

    def closeEvent(self, _):
        """When close is detected, prompts user to save notes if text has been modified"""
        self.save_notes()

    def primary_target_changed(self, new_target: str):
        """
        When primary target has changed, retrieves notes for the new target

        :param new_target: Name of the new primary target
        """
        self._text_field.setText(self._target_manager.getPrimaryNotes())
        self._text_field.document().setModified(False)

    def save_notes(self, force_save: bool=False):
        """
        Checks if notes need to be saved. If so, saves the notes and flushes to disk

        :param force_save: If True, skips text modification checks and forces a save to disk
        """
        if not force_save:
            unsaved_text = self._text_field.document().isModified()
            if unsaved_text:
                if QtWidgets.QMessageBox.Cancel == QtWidgets.QMessageBox.question(self, 'Close Confirmation', 'Do you want to save changes to your notes?', QtWidgets.QMessageBox.Save | QtWidgets.QMessageBox.Cancel):
                    return
            else:
                return
        self._target_manager.setPrimaryNotes(self._text_field.toPlainText())
        try:
            self._target_manager.flushSourceFile(self._target_manager.getPrimaryTargetCatalog())
            self._text_field.document().setModified(False)
        except IOError:
            print('Error saving notes! Your notes have NOT been saved!')

    def discard_note_changes(self):
        """Discards any changes to notes and reverts to last saved notes"""
        if QtWidgets.QMessageBox.Cancel == QtWidgets.QMessageBox.question(self, 'Discard Confirmation', 'Are you sure you want to permanently discard changes to your notes?', QtWidgets.QMessageBox.Discard | QtWidgets.QMessageBox.Cancel):
            return
        self._text_field.setText(self._target_manager.getPrimaryNotes())
        self._text_field.document().setModified(False)
        self.setTitle('Notes: Changes Discarded')
        self.setStyleSheet('QGroupBox:title {color: rgb(0, 0, 175);}')

    def modificationChanged(self, changed: bool):
        self._save_button.setEnabled(changed)
        self._discard_button.setEnabled(changed)
        if changed:
            self.setTitle('Notes: Modified')
            self.setStyleSheet('QGroupBox:title {color: rgb(255, 0, 0);}')
        else:
            self.setTitle('Notes: Saved')
            self.setStyleSheet('QGroupBox:title {color: rgb(0, 150, 0);}')