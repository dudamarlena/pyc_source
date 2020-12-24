# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hudan/Git/nerlogparser/nerlogparser/model/config.py
# Compiled at: 2019-01-07 01:52:20
# Size of source mod 2**32: 3626 bytes
import os
from nerlogparser.model.general_utils import get_logger
from nerlogparser.model.data_utils import get_trimmed_glove_vectors, load_vocab, get_processing_word

class Config:

    def __init__(self, load=True):
        """Initialize hyperparameters and load vocabs

        Args:
            load_embeddings: (bool) if True, load embeddings into
                np array, else None

        """
        if not os.path.exists(self.dir_output):
            os.makedirs(self.dir_output)
        self.logger = get_logger(self.path_log)
        if load:
            self.load()

    def load(self):
        """Loads vocabulary, processing functions and embeddings

        Supposes that build_data.py has been run successfully and that
        the corresponding files have been created (vocab and trimmed GloVe
        vectors)

        """
        self.vocab_words = load_vocab(self.filename_words)
        self.vocab_tags = load_vocab(self.filename_tags)
        self.vocab_chars = load_vocab(self.filename_chars)
        self.nwords = len(self.vocab_words)
        self.nchars = len(self.vocab_chars)
        self.ntags = len(self.vocab_tags)
        self.processing_word = get_processing_word(self.vocab_words, self.vocab_chars, lowercase=True, chars=self.use_chars)
        self.processing_tag = get_processing_word(self.vocab_tags, lowercase=False, allow_unk=False)
        self.embeddings = get_trimmed_glove_vectors(self.filename_trimmed) if self.use_pretrained else None

    file_path = os.path.dirname(os.path.realpath(__file__))
    dir_output = os.path.join(file_path, '..', 'results/test/')
    dir_model = dir_output + 'model.weights/'
    path_log = dir_output + 'log.txt'
    dim_word = 300
    dim_char = 100
    filename_glove = 'data/glove.6B/glove.6B.{}d.txt'.format(dim_word)
    filename_trimmed = os.path.join(file_path, '..', 'data/glove.6B.{}d.trimmed.npz'.format(dim_word))
    use_pretrained = True
    filename_dev = 'data/conll/conll.dev.txt'
    filename_test = 'data/conll/conll.test.txt'
    filename_train = 'data/conll/conll.train.txt'
    max_iter = None
    filename_words = os.path.join(file_path, '..', 'data/words.txt')
    filename_tags = os.path.join(file_path, '..', 'data/tags.txt')
    filename_chars = os.path.join(file_path, '..', 'data/chars.txt')
    train_embeddings = False
    nepochs = 15
    dropout = 0.5
    batch_size = 20
    lr_method = 'adam'
    lr = 0.001
    lr_decay = 0.9
    clip = -1
    nepoch_no_imprv = 3
    hidden_size_char = 100
    hidden_size_lstm = 300
    use_crf = False
    use_chars = True
    label_file = os.path.join(file_path, '..', 'data/label.txt')