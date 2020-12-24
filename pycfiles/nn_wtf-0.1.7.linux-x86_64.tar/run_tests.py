# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/nn_wtf/tests/run_tests.py
# Compiled at: 2016-12-17 04:58:38
from nn_wtf.tests.neural_network_graph_test import NeuralNetworkGraphTest
from nn_wtf.tests.images_labels_data_set_test import ImagesLabelsDataSetTest
from nn_wtf.tests.input_data_test import InputDataTest
from nn_wtf.tests.predictor_test import PredictorTest
from nn_wtf.tests.neural_network_optimizer_test import NeuralNetworkOptimizerTest
from nn_wtf.tests.trainer_test import TrainerTest
from nn_wtf.tests.save_and_restore_test import SaveAndRestoreTest
import unittest
__author__ = 'Lene Preuss <lene.preuss@gmx.net>'
unittest.main()