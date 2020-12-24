# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/cjld/new_jittor/jittor/python/jittor/test/test_load_pth.py
# Compiled at: 2020-03-20 04:44:53
# Size of source mod 2**32: 1730 bytes
import jittor as jt
from jittor import nn
from jittor.models import resnet
import numpy as np, sys, os, random, math, unittest
from .test_reorder_tuner import simple_parser
from .test_log import find_log_with_re
model_test = os.environ.get('model_test', '') == '1'
skip_model_test = not model_test
try:
    jt.dirty_fix_pytorch_runtime_error()
    import torch, torchvision as tv
except:
    skip_model_test = True

@unittest.skipIf(skip_model_test, 'Skip model test')
class TestLoadPth(unittest.TestCase):

    def test_load_pth(self):
        img = np.random.random((1, 3, 224, 224)).astype('float32')
        jt_img = jt.array(img)
        torch_img = torch.Tensor(img)
        torch_model = tv.models.resnet18(True)
        jt_model = resnet.Resnet18()
        jt_model.load_parameters(torch_model.state_dict())
        jt_out = jt_model(jt_img)
        torch_out = torch_model(torch_img)
        print(np.max(np.abs(jt_out.fetch_sync() - torch_out.detach().numpy())))
        assert np.max(np.abs(jt_out.fetch_sync() - torch_out.detach().numpy())) < 0.0001


if __name__ == '__main__':
    unittest.main()