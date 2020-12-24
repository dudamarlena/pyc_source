# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/embeddings/embedding_configs.py
# Compiled at: 2019-04-04 14:27:52
# Size of source mod 2**32: 307 bytes


class EmbeddingConfigs(object):
    __doc__ = '\n        Configuration information\n    '
    is_word2vec_format = True
    do_normalize_emb = True
    model_paths_list = []
    model_names_list = []
    model_dims_list = []
    char_model_path = None
    char_model_dims = -1
    output_format = '.txt;.npz;.gz'