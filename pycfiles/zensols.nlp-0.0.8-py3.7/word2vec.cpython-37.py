# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/zensols/nlp/word2vec.py
# Compiled at: 2020-04-17 19:37:40
# Size of source mod 2**32: 3508 bytes
"""Convenience Gensim glue code for word embeddings/vectors.

"""
__author__ = 'Paul Landes'
import logging
from time import time
from pathlib import Path
from abc import abstractmethod
import numpy as np
from zensols.actioncli import persisted, ConfigFactory
from gensim.models import KeyedVectors, Word2Vec
logger = logging.getLogger(__name__)

class Word2VecModelFactory(ConfigFactory):
    __doc__ = 'Creates instances of ``Word2VecModel``.\n\n    An entry for the Google pretrained vectors look something like:\n\n    [gensim_google_word_vector]\n    class_name = GensimWord2VecModel\n    path = /path/to/GoogleNews-vectors-negative300.bin\n    model_type = keyed\n    size = 300\n\n    '
    INSTANCE_CLASSES = {}

    def __init__(self, config):
        super(Word2VecModelFactory, self).__init__(config, '{name}_word_vector')


class Word2VecModel(object):
    __doc__ = 'Abstract class for word vector/embedding models.\n\n    '

    def __init__(self, size):
        self.zero_arr = np.zeros((1, int(size)))
        self.vectors_length = size

    @abstractmethod
    def _words_to_vectors(self, words):
        pass

    def __getitem__(self, i):
        if i == '<unk>':
            return self.zero_arr
        return self.model[i]

    def __contains__(self, key):
        return key in self.model


class GensimWord2VecModel(Word2VecModel):
    __doc__ = "Load keyed or non-keyed Gensim models.\n\n    Don't instantiate these directly.\n\n    :see Word2VecModelFactory:\n\n    "

    def __init__(self, name, size, model_type, path):
        super(GensimWord2VecModel, self).__init__(size)
        self.name = name
        self.model_type = model_type
        self.path = Path(path).expanduser()

    @property
    @persisted('_models', cache_global=True)
    def models(self):
        return {}

    @property
    def model(self):
        """The word2vec model.

        """
        name = self.name
        models = self.models
        logger.debug(f"getting model {name}")
        if name in models:
            model = models[name]
        else:
            if self.model_type == 'keyed':
                model = self.get_keyed_model()
            else:
                model = self.get_trained_model()
            models[name] = model
        return model

    def get_trained_model(self, name='train_file', force=False):
        """Load a model trained with gensim.

        """
        path = self.path
        if path.exists():
            logger.info('loading trained file: {}'.format(path))
            t0 = time()
            model = Word2Vec.load(str(path.absolute()))
            logger.info('loading model from {} in {:2f}s'.format(path, time() - t0))
        else:
            model = self._train()
            logger.info('saving trained vectors to: {}'.format(path))
            model.save(str(path.absolute()))
        return model

    def get_keyed_model(self, name='keyed_file', force=False):
        """Load a model from a pretrained word2vec model.

        """
        path = self.path
        logger.info('loading keyed file: {}'.format(path))
        fname = str(path.absolute())
        t0 = time()
        model = KeyedVectors.load_word2vec_format(fname, binary=True)
        logger.info('load took {:.2f}s'.format(time() - t0))
        return model

    def _words_to_vectors(self, words):
        wv = self.model.wv
        return map(lambda t: wv[t], filter(lambda t: t in wv, words))


Word2VecModelFactory.register(GensimWord2VecModel)