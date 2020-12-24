# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/CIDAN/GUI/Data_Interaction/loadDataset.py
# Compiled at: 2020-04-29 16:42:31
# Size of source mod 2**32: 2947 bytes
import CIDAN.GUI.Data_Interaction.DataHandler as DataHandler
from CIDAN.GUI.Inputs.FileInput import createFileDialog
import logging
logger1 = logging.getLogger('CIDAN.fileHandling')

def load_new_dataset(main_widget, file_input, save_dir_input, trials=None):
    print(trials)
    file_path = file_input.current_state()
    save_dir_path = save_dir_input.current_state()
    if not trials:
        try:
            main_widget.data_handler = DataHandler(data_path=file_path, trials=[''], save_dir_path=save_dir_path,
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