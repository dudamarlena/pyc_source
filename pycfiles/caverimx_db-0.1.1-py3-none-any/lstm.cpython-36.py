# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/caver/model/lstm.py
# Compiled at: 2018-12-26 01:04:56
# Size of source mod 2**32: 6324 bytes
import torch, torch.nn as nn, torch.nn.functional as F
from .base import BaseModule

class InvalidInputException(Exception):
    pass


class LSTM(BaseModule):
    """LSTM"""

    def __init__(self, hidden_dim=100, embedding_dim=100, vocab_size=1000, label_num=100, device='cpu', layer_num=2, dropout=0.3, batch_first=True, bidirectional=True):
        super().__init__()
        self._layer_num = layer_num
        self._bidirectional = bidirectional
        self._device = device
        self._hidden_dim = hidden_dim
        self._vocab_size = vocab_size
        self._embedding_dim = embedding_dim
        self._label_num = label_num
        self._dropout = dropout
        self._batch_first = batch_first
        self.embedding = nn.Embedding(self._vocab_size, self._embedding_dim)
        self.dropout = nn.Dropout(self._dropout)
        self.lstm = nn.LSTM((self._embedding_dim), (self._hidden_dim),
          (self._layer_num),
          batch_first=(self._batch_first),
          bidirectional=(self._bidirectional),
          dropout=(self._dropout))
        self.predictor = nn.Linear(self._hidden_dim * 2 if self._bidirectional else self._hidden_dim * 1, self._label_num)

    def init_hidden(self, batch_size):
        return (
         torch.zeros(self.layer_num * (2 if self.bidirectional else 1), batch_size, self.hidden_dim).to(self.device),
         torch.zeros(self.layer_num * (2 if self.bidirectional else 1), batch_size, self.hidden_dim).to(self.device))

    def attention(self, rnn_out, state):
        state = state.unsqueeze(0)
        merged_state = torch.cat([s for s in state], 1)
        merged_state = merged_state.unsqueeze(2)
        weights = torch.bmm(rnn_out, merged_state)
        weights = F.softmax(weights.squeeze(2)).unsqueeze(2)
        return torch.bmm(torch.transpose(rnn_out, 1, 2), weights).squeeze(2)

    def forward(self, sequence):
        embedded = self.embedding(sequence)
        embedded = self.dropout(embedded)
        self.lstm.flatten_parameters()
        output, (hidden, cell) = self.lstm(embedded)
        output_feature = torch.cat((hidden[-2, :, :], hidden[-1, :, :]), dim=1)
        output_feature = self.dropout(output_feature)
        preds = self.predictor(output_feature)
        return preds

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

    def _get_model_output(self, batch_sequence_text, vocab_dict, device='cpu'):
        """
        do prediction for for tokenized text in batch way

        LSTM in normal way

        vocab_dict: {"word": 1, "<pad>": 0}
        """
        batch_tokenized = [seq.split() for seq in batch_sequence_text]
        for sent in batch_tokenized:
            if len(sent) == 0:
                raise InvalidInputException('Invalid Input')

        batch_longest = max(map(len, batch_tokenized))
        batch_padding_threshold = batch_longest
        for sample in batch_tokenized:
            if len(sample) < batch_padding_threshold:
                sample += ['<pad>'] * (batch_padding_threshold - len(sample))

        batch_indexed = [[vocab_dict[sample_token] for sample_token in sample] for sample in batch_tokenized]
        indexed = torch.LongTensor(batch_indexed).to(device)
        batch_preds = self.forward(indexed)
        return batch_preds