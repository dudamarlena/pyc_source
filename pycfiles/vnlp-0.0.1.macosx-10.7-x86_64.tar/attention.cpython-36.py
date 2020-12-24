# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/anaconda3/lib/python3.6/site-packages/vnlp/nn/attention.py
# Compiled at: 2018-06-21 18:54:14
# Size of source mod 2**32: 1875 bytes
from torch import nn
from torch.nn import functional as F
from vnlp.nn.functional import mask_invalid_scores

class Pointer(nn.Module):
    __doc__ = '\n    dot product pointer.\n    '

    def forward(self, seq, lens, cond):
        scores = seq.bmm(cond.unsqueeze(2)).squeeze(2)
        return mask_invalid_scores(scores, lens)


class Attention(Pointer):
    __doc__ = '\n    attend over the sequences `seq` using the condition `cond`.\n    '

    @classmethod
    def mix(cls, seq, raw_scores):
        scores = F.softmax(raw_scores, dim=1)
        return scores.unsqueeze(2).expand_as(seq).mul(seq).sum(1)

    def forward(self, seq, lens, cond):
        raw_scores = super().forward(seq, lens, cond)
        return self.mix(seq, raw_scores)


class SelfAttention(nn.Module):
    __doc__ = '\n    scores each element of the sequence with a linear layer and uses the normalized scores to compute a context over the sequence.\n    '

    def __init__(self, dhid, scorer=None):
        super().__init__()
        self.scorer = scorer or nn.Linear(dhid, 1)

    def forward(self, inp, lens):
        batch_size, seq_len, d_feat = inp.size()
        scores = self.scorer(inp.contiguous().view(-1, d_feat)).view(batch_size, seq_len)
        raw_scores = mask_invalid_scores(scores, lens)
        scores = F.softmax(raw_scores, dim=1)
        context = scores.unsqueeze(2).expand_as(inp).mul(inp).sum(1)
        return context


class Coattention(nn.Module):
    __doc__ = '\n    one layer of coattention.\n    '

    def forward(self, q, q_len, d, d_len):
        a = q.bmm(d.transpose(1, 2))
        aq = F.softmax((mask_invalid_scores(a, q_len)), dim=1)
        ad = F.softmax((mask_invalid_scores(a.transpose(1, 2), d_len)), dim=1)
        sd = q.transpose(1, 2).bmm(aq)
        sq = d.transpose(1, 2).bmm(ad)
        cd = sq.bmm(aq)
        return (cd.transpose(1, 2), sq.transpose(1, 2), sd.transpose(1, 2))