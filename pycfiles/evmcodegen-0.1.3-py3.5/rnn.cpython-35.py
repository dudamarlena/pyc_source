# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\evmcodegen\generators\rnn.py
# Compiled at: 2018-10-12 12:08:10
# Size of source mod 2**32: 1846 bytes
"""
RNN based code generators
"""
import os, pkg_resources
from textgenrnn import textgenrnn
from .distribution import _BaseCodeGen
from ..distributions import EVM_INSTRUCTION

class RnnCodeGen(_BaseCodeGen):

    def __init__(self, weights_path=None, vocab_path=None, config_path=None):
        super().__init__()
        self.type = _BaseCodeGen.TYPE_OPCODE_WITH_OPERAND
        pkg_root = pkg_resources.resource_filename(__name__, os.path.join('..', 'weights'))
        weights_path = weights_path or os.path.join(pkg_root, 'rnn_ethcontract_weights.hdf5')
        vocab_path = vocab_path or os.path.join(pkg_root, 'rnn_ethcontract_vocab.json')
        config_path = config_path or os.path.join(pkg_root, 'rnn_ethcontract_config.json')
        self.weights_path, self.vocab_path, self.config_path = weights_path, vocab_path, config_path
        self.textgen = textgenrnn(weights_path=self.weights_path, vocab_path=self.vocab_path, config_path=self.config_path)
        self.n = 5
        self.temperature = 0.1

    def _generator(self, length, n, temperature):
        while True:
            for code in self.textgen.generate(n=n, temperature=self.temperature, max_gen_length=length, return_as_list=True):
                yield code

    def generate(self, length=None):
        length = length or EVM_INSTRUCTION.avg
        return bytes.fromhex(next(self._generator(length=length, n=self.n, temperature=self.temperature)).replace(' ', ''))