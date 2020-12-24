# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ss/tensorspace-converter/tensorspacejs/install.py
# Compiled at: 2019-03-17 04:06:27
# Size of source mod 2**32: 794 bytes
"""
@author syt123450 / https://github.com/syt123450
"""
import os, subprocess
tfjs_workspace = os.path.abspath(os.path.join(__file__, os.pardir, 'tfjs'))
pb2json_workspace = os.path.abspath(os.path.join(__file__, os.pardir, 'tf', 'pb2json'))

def install():
    print('Initializing TensorSpace Converter...')
    install_tfjs()
    install_pb2json()
    print('TensorSpace Converter Initialization Completed!')


def install_tfjs():
    path_now = os.getcwd()
    os.chdir(tfjs_workspace)
    subprocess.check_call([
     'npm',
     'install'])
    os.chdir(path_now)


def install_pb2json():
    path_now = os.getcwd()
    os.chdir(pb2json_workspace)
    subprocess.check_call([
     'npm',
     'install'])
    os.chdir(path_now)