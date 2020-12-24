# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./src/tfjs/tfjs_conversion.py
# Compiled at: 2018-12-28 07:17:31
from utility.file_utility import valid_file, valid_directory, show_invalid_message

def process_tfjs_model(path_input, path_output, output_names=None):
    import subprocess
    if not valid_file(path_input):
        show_invalid_message('input model file', path_input)
        return
    else:
        if not valid_directory(path_output):
            show_invalid_message('output directory', path_output)
            return
        MAIN_JS_PATH = './src/tfjs/main.js'
        if output_names is None:
            subprocess.check_call(['node', MAIN_JS_PATH, path_input, path_output])
        else:
            output_names = '--output_layer_names=' + output_names
            subprocess.check_call(['node', MAIN_JS_PATH, output_names, path_input, path_output])
        return


def show_tfjs_model_summary(path_input):
    import subprocess
    if not valid_file(path_input):
        show_invalid_message('input model file', path_input)
        return
    MAIN_JS_PATH = './src/tfjs/main.js'
    subprocess.check_call(['node', MAIN_JS_PATH, '--summary', path_input])