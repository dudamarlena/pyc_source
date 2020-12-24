# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/embeddings/embedding_utils.py
# Compiled at: 2019-04-16 16:56:54
# Size of source mod 2**32: 4261 bytes
import os
from utils import file_utils
from embeddings.embedding_models import Embedding_Model, Embedding_Models

def reload_char2vec_model(model_path, model_dim):
    char_model = Embedding_Model('char2vec', model_dim)
    char_model.load_model(model_path)
    return char_model


def reload_embedding_models(model_paths_list, model_names_list, model_dims_list, char_model):
    """
    Reload collection of embedding models to serve feature extraction task.
    :param model_paths_list:
    :param model_names_list:
    :param model_dims_list:
    :param char_model:
    :return:
    """
    print('model_paths_list = ', model_paths_list)
    print('model_formats_list = ', model_names_list)
    if not len(model_names_list) == len(model_paths_list):
        raise AssertionError('Not equal length')
    elif not len(model_names_list) == len(model_dims_list):
        raise AssertionError('Not equal length')
    all_emb_models = Embedding_Models([])
    for model_idx in range(len(model_paths_list)):
        model_path = model_paths_list[model_idx]
        model_name = model_names_list[model_idx]
        model_dim = model_dims_list[model_idx]
        if model_path is not None:
            emb_model = Embedding_Model(model_name, model_dim)
            emb_model.load_model(model_path)
            all_emb_models.add_model(emb_model, char_model)

    return all_emb_models


def save_embedding_models_tofolder(dir_path, final_embeddings, reverse_dictionary, vocabulary_size):
    """
    Save all trained word-embedding model of the custom word2vec.
    :param final_embeddings:
    :param reverse_dictionary:
    :param vocabulary_size:
    :return:
    """
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

    def save_to_word2vec_model(vocabs_list):
        filewriter = open((os.path.join(dir_path, 'word2vec.txt')), 'w', encoding='utf-8')
        filewriter.write('%s %s\n' % (len(vocabs_list), len(final_embeddings[0])))
        for word in vocabs_list:
            word_idx = vocabs_list.index(word)
            emb_vector = final_embeddings[word_idx]
            line = ' '.join(['%s' % x for x in emb_vector])
            filewriter.write(word + ' ' + line + '\n')

        filewriter.close()

    file_utils.save_obj(final_embeddings, os.path.join(dir_path, 'final_embeddings'))
    vocab_list = [reverse_dictionary[i] for i in range(vocabulary_size)]
    save_to_word2vec_model(vocab_list)
    file_utils.save_obj(vocab_list, os.path.join(dir_path, 'words_dictionary'))


def save_embedding_models(FLAGS, final_embeddings, reverse_dictionary, vocabulary_size):
    """
    Keep for old implementation.
    :param FLAGS:
    :param final_embeddings:
    :param reverse_dictionary:
    :param vocabulary_size:
    :return:
    """
    save_embedding_models_tofolder(FLAGS.trained_models, final_embeddings, reverse_dictionary, vocabulary_size)


def reload_embeddings(trained_models_dir):
    """
    Reload trained word-embedding model of the custom word2vec.
    :param trained_models_dir:
    :return:
    """
    final_embeddings = file_utils.load_obj(os.path.join(trained_models_dir, 'final_embeddings'))
    reverse_dictionary = None
    labels = file_utils.load_obj(os.path.join(trained_models_dir, 'words_dictionary'))
    return (final_embeddings, reverse_dictionary, labels)


def create_single_utf8_file(input_dir, output_file):
    import glob
    files = glob.glob(input_dir)
    for file in files:
        with open(output_file, 'a') as (myfile):
            with open(file, 'r') as (fp):
                for line in fp:
                    line = line.strip().lower()
                    line = line.decode('utf-8', 'ignore').encode('utf-8')
                    myfile.write(line)

    print('done')