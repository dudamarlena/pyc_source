# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/epitome/test/models_test.py
# Compiled at: 2020-01-22 09:52:53
# Size of source mod 2**32: 1187 bytes
from epitome.test import EpitomeTestCase
from epitome.constants import Dataset
import numpy as np
from epitome.models import VLP

class ModelsTest(EpitomeTestCase):

    def test_model_functions(self):
        train_iters = 50
        validation_size = 10
        model = self.makeSmallModel()
        model.train(train_iters)
        results = model.test(validation_size)
        if not results['preds_mean'].numpy()[(0, 0)] < 0.1:
            raise AssertionError
        else:
            if not results['preds_mean'].shape[0] == validation_size:
                raise AssertionError
            else:
                results = model.test(validation_size, mode=(Dataset.TEST))
                assert results['preds_mean'].numpy()[(0, 0)] < 0.1
                dnase_vector = np.ones(model.data[Dataset.TRAIN].shape[1])
                results = model.eval_vector(model.data[Dataset.TRAIN], dnase_vector, np.arange(0, 20))
                assert results[0].shape[0] == 20
            tmp_path = self.tmpFile()
            model.save(tmp_path)
            loaded_model = VLP(data_path=(model.data_path), checkpoint=tmp_path)
            results = loaded_model.test(validation_size)
            assert results['preds_mean'].numpy()[(0, 0)] < 0.1