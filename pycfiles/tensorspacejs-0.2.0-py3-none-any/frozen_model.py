# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ss/tensorspace-converter/tensorspacejs/tf/frozen_model.py
# Compiled at: 2019-03-19 06:25:32
"""
@author syt123450 / https://github.com/syt123450
"""
import subprocess, os, shutil
from tf.pb2json.pb2json_conversion import convert
input_format_config = '--input_format=tf_frozen_model'

def preprocess_frozen_model(input_path, output_path, output_node_names):
    print 'Preprocessing tensorflow frozen model...'
    os.makedirs(output_path + '/tmp', exist_ok=True)
    print 'Converting frozen model to web friendly format...'
    subprocess.check_call([
     'tensorflowjs_converter',
     input_format_config,
     '--output_node_names=' + output_node_names,
     '--saved_model_tags=serve',
     input_path,
     output_path + '/tmp'])
    path_now = os.getcwd()
    os.chdir(output_path)
    absolute_output_path = os.getcwd()
    absolute_output_path_temp = absolute_output_path + '/tmp/'
    os.chdir(path_now)
    print 'Converting pb to json...'
    convert(absolute_output_path_temp, absolute_output_path)
    print 'Removing temp pb model...'
    shutil.rmtree(absolute_output_path_temp)