# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/caver/model/cnn.py
# Compiled at: 2018-12-26 01:07:52
# Size of source mod 2**32: 5384 bytes
import torch, torch.nn as nn, torch.nn.functional as F
from .base import BaseModule

class InvalidInputException(Exception):
    pass


class CNN(BaseModule):
    __doc__ = '\n    :param filter_num: number of filter\n    :type filter_num: int\n    :param filter_size: size of filter\n    :type filter_size: list\n\n    This is the implementation of CNN from `cnn_paper`_:\n    Kim, Yoon. "Convolutional neural networks for sentence classification." arXiv preprint arXiv:1408.5882 (2014).\n\n    .. _cnn_paper: https://arxiv.org/pdf/1408.5882.pdf\n\n    text -> embedding -> conv -> relu -> BatchNorm -> max_pool -> mlp -> sigmoid\n    '

    def __init__(self, vocab_size=1000, embedding_dim=100, filter_num=100, filter_sizes=[2, 3, 4], label_num=100, dropout=0.3):
        super().__init__()
        self._vocab_size = vocab_size
        self._embedding_dim = embedding_dim
        self._filter_sizes = filter_sizes
        self._dropout = dropout
        self._filter_num = filter_num
        self._label_num = label_num
        self._hidden_dim = len(self._filter_sizes) * self._filter_num
        self.embedding = nn.Embedding(self._vocab_size, self._embedding_dim)
        self.convs = nn.ModuleList([nn.Conv2d(in_channels=1, out_channels=(self._filter_num), kernel_size=(filter_size, self._embedding_dim)) for filter_size in self._filter_sizes])
        self.dropout = nn.Dropout(self._dropout)
        self.bn = nn.BatchNorm1d(self._hidden_dim)
        self.predictor = nn.Linear(self._hidden_dim, self._label_num)

    def forward(self, sequence):
        embedded = self.embedding(sequence)
        embedded = embedded.unsqueeze(1)
        conved = [F.relu(conv(embedded)).squeeze(3) for conv in self.convs]
        pooled = [F.max_pool1d(conv, conv.shape[2]).squeeze(2) for conv in conved]
        cat = self.dropout(torch.cat(pooled, dim=1))
        return self.predictor(cat)

    def predict(self, batch_sequence_text, device='cpu', top_k=5):
        batch_preds = self._get_model_output(batch_sequence_text=batch_sequence_text, vocab_dict=(self.vocab),
          device=device)
        batch_top_k_value, batch_top_k_index = torch.topk((torch.sigmoid(batch_preds)), k=top_k, dim=1)
        labels = self.predict_label(batch_top_k_index)
        return labels

    def predict_prob(self, batch_sequence_text, device='cpu'):
        batch_preds = self._get_model_output(batch_sequence_text=batch_sequence_text, vocab_dict=(self.vocab),
          device=device)
        batch_prob = torch.softmax(batch_preds, dim=1)
        return batch_prob

    def _get_model_output(self, *args, **kwargs):
        """
        do prediction for tokenized text in batch way
        CNN is special in processing <pad>
        vocab_dict: {"word": 1, "<pad>": 0}
        """
        batch_sequence_text = kwargs['batch_sequence_text']
        vocab_dict = kwargs['vocab_dict']
        device = kwargs['device']
        batch_tokenized = [seq.split() for seq in batch_sequence_text]
        for sent in batch_tokenized:
            if len(sent) == 0:
                raise InvalidInputException('Invalid Input')

        batch_longest = max(map(len, batch_tokenized))
        batch_padding_threshold = max(max(self._filter_sizes), batch_longest)
        for sample in batch_tokenized:
            if len(sample) < batch_padding_threshold:
                sample += ['<pad>'] * (batch_padding_threshold - len(sample))

        batch_indexed = [[vocab_dict[sample_token] for sample_token in sample] for sample in batch_tokenized]
        indexed = torch.LongTensor(batch_indexed).to(device)
        batch_preds = self.forward(indexed)
        return batch_preds