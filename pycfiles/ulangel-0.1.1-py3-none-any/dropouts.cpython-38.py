# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./ulangel/rnn/dropouts.py
# Compiled at: 2020-03-05 08:23:54
# Size of source mod 2**32: 3241 bytes
import warnings
import torch.nn as nn
import torch.nn.functional as F

def dropout_mask(x, sz, p):
    """create a mask to zero out p persent of the activation, by keeping the
    same module of the tensor."""
    return (x.new)(*sz).bernoulli_(1 - p).div_(1 - p)


class ActivationDropout(nn.Module):
    __doc__ = 'zeroing out p percent of the layer activation, returning a layer of\n    actication with p persent of zeros.\n    '

    def __init__(self, p=0.5):
        super().__init__()
        self.p = p

    def forward(self, x):
        if not self.training or self.p == 0.0:
            return x
        size = (
         x.size(0), 1, x.size(2))
        m = dropout_mask(x.data, size, self.p)
        return x * m


class EmbeddingDropout(nn.Module):
    __doc__ = "Applies dropout on the embedding layer by zeroing out some elements of\n    the embedding vector. It's the activation dropout of the embedding layers.\n    Returning an embedding object.\n    "

    def __init__(self, emb, embed_p):
        super().__init__()
        self.emb = emb
        self.embed_p = embed_p
        self.pad_idx = self.emb.padding_idx
        if self.pad_idx is None:
            self.pad_idx = -1

    def forward(self, words, scale=None):
        if self.training and self.embed_p != 0:
            size = (
             self.emb.weight.size(0), 1)
            mask = dropout_mask(self.emb.weight.data, size, self.embed_p)
            masked_embed = self.emb.weight * mask
        else:
            masked_embed = self.emb.weight
        if scale:
            masked_embed.mul_(scale)
        return F.embedding(words, masked_embed, self.pad_idx, self.emb.max_norm, self.emb.norm_type, self.emb.scale_grad_by_freq, self.emb.sparse)


class ConnectionWeightDropout(nn.Module):
    __doc__ = 'zeroing out p percent of the connection weights between defined layers\n    (hh in the default setting), returning a matrix of connection weights with\n    p persent of zeros.\n    '

    def __init__(self, module, weight_p=[
 0.0], layer_names=['weight_hh_l0']):
        super().__init__()
        self.module = module
        self.weight_p = weight_p
        self.layer_names = layer_names
        for layer in self.layer_names:
            w = getattr(self.module, layer)
            self.module.register_parameter(f"{layer}_raw", nn.Parameter(w.data))
            self.module._parameters[layer] = F.dropout(w,
              p=(self.weight_p), training=False)

    def _setweights(self):
        for layer in self.layer_names:
            raw_w = getattr(self.module, f"{layer}_raw")
            self.module._parameters[layer] = F.dropout(raw_w,
              p=(self.weight_p), training=(self.training))

    def forward--- This code section failed: ---

 L.  93         0  LOAD_FAST                'self'
                2  LOAD_METHOD              _setweights
                4  CALL_METHOD_0         0  ''
                6  POP_TOP          

 L.  94         8  LOAD_GLOBAL              warnings
               10  LOAD_METHOD              catch_warnings
               12  CALL_METHOD_0         0  ''
               14  SETUP_WITH           52  'to 52'
               16  POP_TOP          

 L.  96        18  LOAD_GLOBAL              warnings
               20  LOAD_METHOD              simplefilter
               22  LOAD_STR                 'ignore'
               24  CALL_METHOD_1         1  ''
               26  POP_TOP          

 L.  97        28  LOAD_FAST                'self'
               30  LOAD_ATTR                module
               32  LOAD_ATTR                forward
               34  LOAD_FAST                'args'
               36  CALL_FUNCTION_EX      0  'positional arguments only'
               38  POP_BLOCK        
               40  ROT_TWO          
               42  BEGIN_FINALLY    
               44  WITH_CLEANUP_START
               46  WITH_CLEANUP_FINISH
               48  POP_FINALLY           0  ''
               50  RETURN_VALUE     
             52_0  COME_FROM_WITH       14  '14'
               52  WITH_CLEANUP_START
               54  WITH_CLEANUP_FINISH
               56  END_FINALLY      

Parse error at or near `ROT_TWO' instruction at offset 40