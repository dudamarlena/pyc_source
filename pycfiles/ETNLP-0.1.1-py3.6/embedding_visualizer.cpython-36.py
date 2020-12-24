# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/api/embedding_visualizer.py
# Compiled at: 2019-03-30 11:14:02
# Size of source mod 2**32: 8206 bytes
import sys, os, gensim, tensorflow as tf, numpy as np
from tensorflow.contrib.tensorboard.plugins import projector
import logging
from tensorboard import default
from tensorboard import program

class TensorBoardTool:

    def __init__(self, dir_path):
        self.dir_path = dir_path

    def run(self, emb_name, port):
        logging.basicConfig(level=(logging.INFO))
        logging.propagate = False
        tb = program.TensorBoard(default.get_plugins(), default.get_assets_zip_provider())
        tb.configure(argv=[None, '--logdir', self.dir_path, '--port', str(port)])
        url = tb.launch()
        sys.stdout.write('TensorBoard of %s at %s \n' % (emb_name, url))


def convert_multiple_emb_models_2_tf(emb_name_arr, w2v_model_arr, output_path, port):
    """

    :param emb_name_arr:
    :param w2v_model_arr:
    :param output_path:
    :param port:
    :return:
    """
    idx = 0
    sess = tf.InteractiveSession()
    for w2v_model in w2v_model_arr:
        emb_name = emb_name_arr[idx]
        meta_file = '%s.tsv' % emb_name
        placeholder = np.zeros((len(w2v_model.wv.index2word), w2v_model.vector_size))
        with open(os.path.join(output_path, meta_file), 'wb') as (file_metadata):
            for i, word in enumerate(w2v_model.wv.index2word):
                placeholder[i] = w2v_model[word]
                if word == '':
                    print('Empty Line, should replaced by any thing else, or will cause a bug of tensorboard')
                    file_metadata.write('{0}'.format('<Empty Line>').encode('utf-8') + b'\n')
                else:
                    file_metadata.write('{0}'.format(word).encode('utf-8') + b'\n')

        word_embedding_var = tf.Variable(placeholder, trainable=False, name=emb_name)
        tf.global_variables_initializer().run()
        sess.run(word_embedding_var)
        config = projector.ProjectorConfig()
        embed = config.embeddings.add()
        embed.tensor_name = emb_name
        embed.metadata_path = meta_file
        idx += 1

    saver = tf.train.Saver()
    writer = tf.summary.FileWriter(output_path, sess.graph)
    projector.visualize_embeddings(writer, config)
    all_emb_name = '_'.join(emb_name for emb_name in emb_name_arr)
    saver.save(sess, os.path.join(output_path, '%s.ckpt' % all_emb_name))
    tb_tool = TensorBoardTool(output_path)
    tb_tool.run(all_emb_name, port)


def convert_one_emb_model_2_tf(emb_name, model, output_path, port):
    """

    :param model: Word2Vec model
    :param output_path:
    :return:
    """
    meta_file = '%s.tsv' % emb_name
    placeholder = np.zeros((len(model.wv.index2word), model.vector_size))
    with open(os.path.join(output_path, meta_file), 'wb') as (file_metadata):
        for i, word in enumerate(model.wv.index2word):
            placeholder[i] = model[word]
            if word == '':
                print('Empty Line, should replaced by any thing else, or will cause a bug of tensorboard')
                file_metadata.write('{0}'.format('<Empty Line>').encode('utf-8') + b'\n')
            else:
                file_metadata.write('{0}'.format(word).encode('utf-8') + b'\n')

    sess = tf.InteractiveSession()
    word_embedding_var = tf.Variable(placeholder, trainable=False, name=emb_name)
    sess.run(word_embedding_var)
    saver = tf.train.Saver()
    writer = tf.summary.FileWriter(output_path, sess.graph)
    config = projector.ProjectorConfig()
    embed = config.embeddings.add()
    embed.tensor_name = emb_name
    embed.metadata_path = meta_file
    projector.visualize_embeddings(writer, config)
    saver.save(sess, os.path.join(output_path, '%s.ckpt' % emb_name))
    tb_tool = TensorBoardTool(output_path)
    tb_tool.run(emb_name, port)


def visualize_multiple_embeddings_individually(paths_of_emb_models):
    output_root_dir = '../data/embedding_tf_data/'
    starting_port = 6006
    embedding_names = []
    print('Loaded all word embeddings, going to visualize ...')
    if paths_of_emb_models:
        if paths_of_emb_models.__contains__(';'):
            files = paths_of_emb_models.split(';')
            for emb_file in files:
                embedding_name = os.path.basename(os.path.normpath(emb_file))
                tf_data_folder = output_root_dir + embedding_name
                if not os.path.exists(tf_data_folder):
                    os.makedirs(tf_data_folder)
                is_binary = False
                if emb_file.endswith('.bin'):
                    is_binary = True
                emb_model = gensim.models.KeyedVectors.load_word2vec_format(emb_file, binary=is_binary)
                convert_one_emb_model_2_tf(embedding_name, emb_model, tf_data_folder, starting_port)
                embedding_names.append(embedding_name)
                starting_port += 1

    while 1:
        print('Type exit to quite the visualizer: ')
        user_input = input()
        if user_input == 'exit':
            break


def visualize_multiple_embeddings_all_in_one(paths_of_emb_models):
    output_root_dir = '../data/embedding_tf_data/'
    starting_port = 6006
    embedding_names = []
    print('Loaded all word embeddings, going to visualize ...')
    embedding_name_arr = []
    w2v_embedding_model_arr = []
    if paths_of_emb_models:
        if paths_of_emb_models.__contains__(';'):
            files = paths_of_emb_models.split(';')
            for emb_file in files:
                embedding_name = os.path.basename(os.path.normpath(emb_file))
                embedding_name_arr.append(embedding_name)
                is_binary = False
                if emb_file.endswith('.bin'):
                    is_binary = True
                emb_model = gensim.models.KeyedVectors.load_word2vec_format(emb_file, binary=is_binary)
                w2v_embedding_model_arr.append(emb_model)
                embedding_names.append(embedding_name)

    all_emb_name = '_'.join(emb_name for emb_name in embedding_name_arr)
    tf_data_folder = output_root_dir + all_emb_name
    if not os.path.exists(tf_data_folder):
        os.makedirs(tf_data_folder)
    convert_multiple_emb_models_2_tf(embedding_name_arr, w2v_embedding_model_arr, tf_data_folder, starting_port)
    while 1:
        print('Type exit to quite the visualizer: ')
        user_input = input()
        if user_input == 'exit':
            break


def visualize_multiple_embeddings(paths_of_emb_models):
    """
    API to other part to call, don't modify this function.
    :param paths_of_emb_models:
    :return:
    """
    visualize_multiple_embeddings_all_in_one(paths_of_emb_models)


if __name__ == '__main__':
    try:
        model_path = sys.argv[1]
        output_path = sys.argv[2]
    except Exception as e:
        print('Please provide model path and output path %s ' % e)

    model = gensim.models.KeyedVectors.load_word2vec_format(model_path, binary=True)
    convert_one_emb_model_2_tf(model, output_path)