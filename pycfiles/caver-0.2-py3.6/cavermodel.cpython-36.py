# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/caver/model/cavermodel.py
# Compiled at: 2018-12-26 01:10:06
# Size of source mod 2**32: 1380 bytes
import torch, os
from .cnn import CNN
from .lstm import LSTM
MODEL_CLASS = {'CNN':CNN(), 
 'LSTM':LSTM()}

class CaverModelInitiationTypeError(Exception):
    pass


class CaverModel(object):
    __doc__ = '\n    Wrapper for models, make it simpler for inference\n    '

    def __init__(self, path=None, device='cpu'):
        super().__init__()
        self._inside_model = None
        if path:
            self.load(path, device)

    def load(self, path, device):
        """ load model from file """
        loaded_checkpoint = torch.load((os.path.join(path, 'checkpoint_best.pt')), map_location=device)
        self.model_type = loaded_checkpoint['model_type']
        self._inside_model = MODEL_CLASS[self.model_type]
        self._inside_model.load(loaded_checkpoint, path)
        self._inside_model.eval()

    def predict(self, batch_sequence_text, top_k=5):
        res = self._inside_model.predict(batch_sequence_text, top_k=top_k)
        return res

    def predict_prob(self, batch_sequence_text):
        batch_prob = self._inside_model.predict_prob(batch_sequence_text)
        return batch_prob.data.numpy()