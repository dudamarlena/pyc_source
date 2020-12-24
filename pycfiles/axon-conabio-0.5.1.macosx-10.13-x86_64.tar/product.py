# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/site-packages/axon_conabio/products/product.py
# Compiled at: 2018-12-10 18:39:29
from abc import ABCMeta, abstractmethod
import six, logging

@six.add_metaclass(ABCMeta)
class Product(object):
    logger = logging.getLogger(__name__)

    @abstractmethod
    def read_file(self, filepath):
        pass

    def preprocess(self, inputs):
        return inputs

    @abstractmethod
    def process(self, preprocessed_inputs):
        pass

    def _process_file(self, filepath):
        self.logger.info('Reading file %s', filepath)
        input_ = self.read_file(filepath)
        self.logger.info('Preprocessing file')
        preprocessed_input = self.preprocess(input_)
        self.logger.info('Processing file')
        output = self.process(preprocessed_input)
        self.logger.info('Done processing file %s', filepath)
        return output