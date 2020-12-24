# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/DeepJetCore/bin/convertToTF.py
# Compiled at: 2018-07-12 08:05:01
import imp
try:
    imp.find_module('setGPU')
    import setGPU
except ImportError:
    found = False

from keras.models import load_model
from argparse import ArgumentParser
from keras import backend as K
from Losses import *
import os
parser = ArgumentParser('')
parser.add_argument('inputModel')
parser.add_argument('outputDir')
args = parser.parse_args()
if os.path.isdir(args.outputDir):
    raise Exception('output directory must not exist yet')
model = load_model(args.inputModel, custom_objects=global_loss_list)
import tensorflow as tf, keras.backend as K
tfsession = K.get_session()
saver = tf.train.Saver()
tfoutpath = args.outputDir + '/tf'
import os
os.system('mkdir -p ' + tfoutpath)
saver.save(tfsession, tfoutpath)