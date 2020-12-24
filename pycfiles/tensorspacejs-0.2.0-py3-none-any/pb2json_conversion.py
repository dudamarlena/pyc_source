# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ss/tensorspace-converter/tensorspacejs/tf/pb2json/pb2json_conversion.py
# Compiled at: 2019-03-17 01:22:32
"""
@author syt123450 / https://github.com/syt123450
"""
import os
TS_NODE_BIN_PATH = os.path.abspath(os.path.join(__file__, os.pardir, 'node_modules', '.bin', 'ts-node'))
CONVERTER_SCRIPT_PATH = os.path.abspath(os.path.join(__file__, os.pardir, 'tools', 'pb2json_converter.ts'))

def convert(path_input, path_output):
    print 'pb to json'
    import subprocess
    subprocess.check_call(['node', TS_NODE_BIN_PATH, CONVERTER_SCRIPT_PATH, path_input, path_output])