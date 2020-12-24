# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/utils/embedding_io.py
# Compiled at: 2019-04-04 14:27:52
# Size of source mod 2**32: 7069 bytes
from typing import Iterable, List, Set
from itertools import groupby
import numpy as np, re, utils.vectors as v
from utils.word import Word
import logging, os
from embeddings.embedding_configs import EmbeddingConfigs

def save_model_to_file(embedding_model: List[Word], model_file_out: str):
    """
    Save loaded model back to file (to remove duplicated items).
    :param embedding_model:
    :param model_file_out:
    :return:
    """
    fwriter = open(model_file_out, 'w')
    meta_data = '%s %s\n' % (len(embedding_model), len(embedding_model[0].vector))
    fwriter.write(meta_data)
    fwriter.flush()
    for w_Word in embedding_model:
        line = w_Word.text + ' ' + ' '.join(str(scalar) for scalar in w_Word.vector.tolist())
        fwriter.write(line + '\n')
        fwriter.flush()

    fwriter.close()


def load_word_embeddings(file_paths: str, emb_config: EmbeddingConfigs) -> List[List[Word]]:
    """
    Sonvx: load multiple embeddings: e.g., <emb_file1>;<emb_file2>
    :param file_paths:
    :param emb_config:
    :return:
    """
    embedding_models = []
    embedding_names = []
    if file_paths:
        if file_paths.__contains__(';'):
            files = file_paths.split(';')
            for emb_file in files:
                word_embedding = load_word_embedding(emb_file.replace('"', ''), emb_config)
                embedding_name = os.path.basename(os.path.normpath(emb_file))
                embedding_models.append(word_embedding)
                embedding_names.append(embedding_name)

    else:
        return [
         load_word_embedding(file_paths), emb_config]
    return (embedding_names, embedding_models)


def load_word_embedding(file_path: str, emb_config: EmbeddingConfigs) -> List[Word]:
    """
    Load and cleanup the data.
    :param file_path:
    :param emb_config:
    :return:
    """
    print(f"Loading {file_path}...")
    words = load_words_raw(file_path, emb_config)
    print(f"Loaded {len(words)} words.")
    word1 = words[1]
    print('Vec Len(word1) = ', len(word1.vector))
    logging.debug('Embedding words: ', words[:10])
    print('Emb_vocab_size = ', len(words))
    return words


def load_words_raw(file_path: str, emb_config: EmbeddingConfigs) -> List[Word]:
    """
    Load the file as-is, without doing any validation or cleanup.
    :param file_path:
    :param emb_config:
    :return:
    """

    def parse_line(line, frequency):
        tokens = line.split(' ')
        word = tokens[0]
        if emb_config.do_normalize_emb:
            vector = v.normalize(np.array([float(x) for x in tokens[1:]]))
        else:
            vector = np.array([float(x) for x in tokens[1:]])
        return Word(word, vector, frequency)

    unique_dict = {}
    words = []
    frequency = 1
    duplicated_entry = 0
    idx_counter, vocab_size, emb_dim = (0, 0, 0)
    with open(file_path) as (f):
        for line in f:
            line = line.rstrip()
            if idx_counter == 0:
                if emb_config.is_word2vec_format:
                    try:
                        meta_info = line.split(' ')
                        vocab_size = int(meta_info[0])
                        emb_dim = int(meta_info[1])
                        idx_counter += 1
                        continue
                    except Exception as e:
                        print('meta_info = ' % meta_info)
                        logging.error('Input embedding has format issue: Error = %s' % e)

            w = parse_line(line, frequency)
            if w.text not in unique_dict:
                unique_dict[w.text] = frequency
                words.append(w)
                frequency += 1
            else:
                duplicated_entry += 1
            if idx_counter == 10:
                if len(w.vector) != emb_dim:
                    message = 'Metadata and the real vector size do not match: meta:real = %s:%s' % (
                     emb_dim, len(w.vector))
                    logging.error(message)
                    raise ValueError(message)
            idx_counter += 1

    if duplicated_entry > 0:
        logging.debug('Loading the same word again: %s' % duplicated_entry)
    if frequency - 1 != vocab_size:
        msg = 'Loaded %s/%s unique vocab.' % (frequency - 1, vocab_size)
        logging.info(msg)
    return words


def iter_len(iter: Iterable[complex]) -> int:
    return sum(1 for _ in iter)


def most_common_dimension(words: List[Word]) -> int:
    """
    There is a line in the input file which is missing a word
    (search -0.0739, -0.135, 0.0584).
    """
    lengths = sorted([len(word.vector) for word in words])
    dimensions = [(k, iter_len(v)) for k, v in groupby(lengths)]
    print('Dimensions:')
    for dim, num_vectors in dimensions:
        print(f"{num_vectors} {dim}-dimensional vectors")

    most_common = sorted(dimensions, key=(lambda t: t[1]), reverse=True)[0]
    return most_common[0]


ignore_char_regex = re.compile('[\\W_]')
is_valid_word = re.compile('^[^\\W_].*[^\\W_]$')

def remove_duplicates(words: List[Word]) -> List[Word]:
    seen_words = set()
    unique_words = []
    for w in words:
        canonical = ignore_char_regex.sub('', w.text)
        if canonical not in seen_words:
            seen_words.add(canonical)
            unique_words.append(w)

    return unique_words


def remove_stop_words(words: List[Word]) -> List[Word]:
    return [w for w in words if len(w.text) > 1 if is_valid_word.match(w.text)]


if not [w.text for w in remove_stop_words([
 Word('a', [], 1),
 Word('ab', [], 1),
 Word('-ab', [], 1),
 Word('ab_', [], 1),
 Word('a.', [], 1),
 Word('.a', [], 1),
 Word('ab', [], 1)])] == [
 'ab', 'ab']:
    raise AssertionError
elif not [w.text for w in remove_duplicates([
 Word('a.b', [], 1),
 Word('-a-b', [], 1),
 Word('ab_+', [], 1),
 Word('.abc...', [], 1)])] == [
 'a.b', '.abc...']:
    raise AssertionError