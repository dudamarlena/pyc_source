# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ss/tensorspace-converter/src/tfjs_conversion.py
# Compiled at: 2018-12-17 01:36:10
# Size of source mod 2**32: 598 bytes
from file_utility import remove_file, valid_file, valid_directory, show_invalid_message

def process_tfjs_model(path_input, path_output, output_names):
    import subprocess
    if not valid_file(path_input):
        show_invalid_message('input model file', path_input)
        return
    if not valid_directory(path_output):
        show_invalid_message('output directory', path_output)
        return
    MAIN_JS_PATH = './src/tfjs/main.js'
    output_names = '--output_layer_names=' + output_names
    subprocess.check_call(['node', MAIN_JS_PATH, output_names, path_input, path_output])