# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/caver/classify.py
# Compiled at: 2018-12-03 22:41:49
# Size of source mod 2**32: 2504 bytes
import torch, numpy as np
from . import model
from .utils import update_config, scaler, zero_padding
from .config import Config
from .data import TextData, Segment

class Caver:
    """Caver"""

    def __init__(self, model_name, model_path, data_path='', **kwargs):
        self.config = update_config((Config()), **kwargs)
        self.load_data(data_path)
        assert hasattr(model, model_name)
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.model = (getattr(model, model_name))(vocab_size=len(self.word2index), 
         label_num=len(self.label2index), **kwargs).to(self.device)
        self.model.load(model_path)
        self.model.eval()
        self.segmentor = Segment(self.config.cut_model)

    def load_data(self, path):
        """
        Load word index and label index from file.

        If there is no JSON file saved in :class:`caver.config.Config.index_path`,
        this will generate new index file.
        """
        data = TextData(path)
        self.word2index = data.word2index
        self.label2index = data.label2index
        self.index2label = dict([(a, b) for b, a in data.label2index.items()])

    def predict(self, text):
        """
        This text will be transformed to lower-case and segmented by
        :class:`caver.config.Config.cut_model`.
        """
        text = self.segmentor.cut(text.strip().lower())
        feature = [self.word2index.get(t) for t in text]
        feature = zero_padding([feature], self.config.sentence_length)
        feature = torch.from_numpy(feature).type(torch.long).to(self.device)
        with torch.no_grad():
            logits = self.model(feature).cpu().numpy()[0]
        return scaler(logits, 0, 1)

    def get_top_label(self, text, top=5):
        """
        :param str text: text
        :param int top: top-n most possible labels
        """
        preds = self.predict(text)
        top_index = np.argsort(preds)[::-1]
        result = []
        result.append([self.index2label[i] for i in top_index[:top]])
        result.append([preds[i] for i in top_index[:top]])
        return result