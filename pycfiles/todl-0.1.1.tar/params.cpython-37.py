# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/svpino/dev/tensorflow-object-detection-sagemaker/todl/tensorflow-object-detection/research/audioset/yamnet/params.py
# Compiled at: 2020-04-05 19:50:57
# Size of source mod 2**32: 1562 bytes
"""Hyperparameters for YAMNet."""
SAMPLE_RATE = 16000
STFT_WINDOW_SECONDS = 0.025
STFT_HOP_SECONDS = 0.01
MEL_BANDS = 64
MEL_MIN_HZ = 125
MEL_MAX_HZ = 7500
LOG_OFFSET = 0.001
PATCH_WINDOW_SECONDS = 0.96
PATCH_HOP_SECONDS = 0.48
PATCH_FRAMES = int(round(PATCH_WINDOW_SECONDS / STFT_HOP_SECONDS))
PATCH_BANDS = MEL_BANDS
NUM_CLASSES = 521
CONV_PADDING = 'same'
BATCHNORM_CENTER = True
BATCHNORM_SCALE = False
BATCHNORM_EPSILON = 0.0001
CLASSIFIER_ACTIVATION = 'sigmoid'
FEATURES_LAYER_NAME = 'features'
EXAMPLE_PREDICTIONS_LAYER_NAME = 'predictions'