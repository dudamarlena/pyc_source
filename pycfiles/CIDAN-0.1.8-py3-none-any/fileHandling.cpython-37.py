# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/CIDAN/GUI/Data_Interaction/fileHandling.py
# Compiled at: 2020-04-29 15:32:22
# Size of source mod 2**32: 4169 bytes
import CIDAN.GUI.Data_Interaction.DataHandler as DataHandler
from PySide2.QtWidgets import *
from PySide2 import QtCore
import logging
logger1 = logging.getLogger('CIDAN.fileHandling')

def createFileDialog(directory='', forOpen=True, fmt='', isFolder=0):
    directory = '/Users/sschickler/Documents/LSSC-python/input_images'
    options = QFileDialog.Options()
    options |= QFileDialog.DontUseNativeDialog
    options |= QFileDialog.DontUseCustomDirectoryIcons
    dialog = QFileDialog()
    dialog.setOptions(options)
    dialog.setFilter(dialog.filter() | QtCore.QDir.Hidden)
    if isFolder == 1:
        dialog.setFileMode(QFileDialog.DirectoryOnly)
    if isFolder == 2:
        dialog.setFileMode(QFileDialog.AnyFile)
    dialog.setAcceptMode(QFileDialog.AcceptOpen) if forOpen else dialog.setAcceptMode(QFileDialog.AcceptSave)
    if fmt != '':
        if isFolder is False:
            dialog.setDefaultSuffix(fmt)
            dialog.setNameFilters([f"{fmt} (*.{fmt})"])
    if directory != '':
        dialog.setDirectory(str(directory))
    if dialog.exec_() == QDialog.Accepted:
        path = dialog.selectedFiles()[0]
        return path
    return ''


def load_new_dataset(main_widget, file_input, save_dir_input, trials=None):
    print(trials)
    file_path = file_input.current_state()
    save_dir_path = save_dir_input.current_state()
    if not trials:
        try:
            main_widget.data_handler = DataHandler(data_path='', trials=[file_path], save_dir_path=save_dir_path,
              save_dir_already_created=False)
            main_widget.init_w_data()
        except Exception as e:
            try:
                logger1.error(e)
                print('Loading Failed please make sure it is a valid file')
            finally:
                e = None
                del e

    if trials:
        logger1.debug('Trials:' + str(trials))
        if len(trials) == 0:
            print('Please select at least one trial')
        try:
            main_widget.data_handler = DataHandler(data_path=file_path, trials=trials, save_dir_path=save_dir_path,
              save_dir_already_created=False)
            main_widget.init_w_data()
        except Exception as e:
            try:
                logger1.error(e)
                print('Loading Failed please make sure it is a valid folder and all trialsare valid files')
            finally:
                e = None
                del e


def load_prev_session(main_widget, save_dir_input):
    save_dir_path = save_dir_input.current_state()
    try:
        main_widget.data_handler = DataHandler(data_path='', save_dir_path=save_dir_path,
          save_dir_already_created=True)
        main_widget.init_w_data()
    except Exception as e:
        try:
            logger1.error(e)
            print('Loading Failed please try again, if problem persists save directory is corrupted')
        finally:
            e = None
            del e


def export_timetraces(main_widget):
    createFileDialog(forOpen=False, isFolder=2)