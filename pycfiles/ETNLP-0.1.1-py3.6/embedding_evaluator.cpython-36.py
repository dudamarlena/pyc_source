# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/api/embedding_evaluator.py
# Compiled at: 2019-04-16 16:58:06
# Size of source mod 2**32: 16905 bytes
import logging, gensim, argparse
from gensim.models.keyedvectors import WordEmbeddingsKeyedVectors, Word2VecKeyedVectors
from gensim import utils, matutils
from six import string_types
from numpy import dot, float32 as REAL, array, ndarray, argmax
from utils import embedding_io, emb_utils
from embeddings.embedding_configs import EmbeddingConfigs
logger = logging.getLogger(__name__)

class new_Word2VecKeyedVectors(Word2VecKeyedVectors):

    def __init__(self, vector_size):
        super(Word2VecKeyedVectors, self).__init__(vector_size=vector_size)

    def most_similar(self, positive=None, negative=None, topn=10, restrict_vocab=None, indexer=None):
        """
        Find the top-N most similar words. Positive words contribute positively towards the
        similarity, negative words negatively.

        This method computes cosine similarity between a simple mean of the projection
        weight vectors of the given words and the vectors for each word in the model.
        The method corresponds to the `word-analogy` and `distance` scripts in the original
        word2vec implementation.

        If topn is False, most_similar returns the vector of similarity scores.

        `restrict_vocab` is an optional integer which limits the range of vectors which
        are searched for most-similar values. For example, restrict_vocab=10000 would
        only check the first 10000 word vectors in the vocabulary order. (This may be
        meaningful if you've sorted the vocabulary by descending frequency.)

        Example::

          >>> trained_model.most_similar(positive=['woman', 'king'], negative=['man'])
          [('queen', 0.50882536), ...]

        """
        if positive is None:
            positive = []
        else:
            if negative is None:
                negative = []
            self.init_sims()
            if isinstance(positive, string_types):
                if not negative:
                    positive = [
                     positive]
            positive = [(word, 1.0) if isinstance(word, string_types + (ndarray,)) else word for word in positive]
            negative = [(word, -1.0) if isinstance(word, string_types + (ndarray,)) else word for word in negative]
            all_words, mean = set(), []
            for word, weight in positive + negative:
                if isinstance(word, ndarray):
                    mean.append(weight * word)
                else:
                    mean.append(weight * self.word_vec(word, use_norm=True))
                    if word in self.vocab:
                        all_words.add(self.vocab[word].index)

            raise mean or ValueError('cannot compute similarity with no input')
        mean = matutils.unitvec(array(mean).mean(axis=0)).astype(REAL)
        if indexer is not None:
            return indexer.most_similar(mean, topn)
        else:
            limited = self.syn0norm if restrict_vocab is None else self.syn0norm[:restrict_vocab]
            dists = dot(limited, mean)
            if not topn:
                return dists
            best = matutils.argsort(dists, topn=(topn + len(all_words)), reverse=True)
            result = [(self.index2word[sim], float(dists[sim])) for sim in best if sim not in all_words]
            return result[:topn]

    def new_accuracy(self, questions, restrict_vocab=30000, most_similar=most_similar, case_insensitive=True):
        """
        Compute accuracy of the model. `questions` is a filename where lines are
        4-tuples of words, split into sections by ": SECTION NAME" lines.
        See questions-words.txt in
        https://storage.googleapis.com/google-code-archive-source/v2/code.google.com/word2vec/source-archive.zip
        for an example.

        The accuracy is reported (=printed to log and returned as a list) for each
        section separately, plus there's one aggregate summary at the end.

        Use `restrict_vocab` to ignore all questions containing a word not in the first `restrict_vocab`
        words (default 30,000). This may be meaningful if you've sorted the vocabulary by descending frequency.
        In case `case_insensitive` is True, the first `restrict_vocab` words are taken first, and then
        case normalization is performed.

        Use `case_insensitive` to convert all words in questions and vocab to their uppercase form before
        evaluating the accuracy (default True). Useful in case of case-mismatch between training tokens
        and question words. In case of multiple case variants of a single word, the vector for the first
        occurrence (also the most frequent if vocabulary is sorted) is taken.

        This method corresponds to the `compute-accuracy` script of the original C word2vec.

        """
        print('INFO: Using new accuracy')
        ok_vocab = [(w, self.vocab[w]) for w in self.index2word[:restrict_vocab]]
        ok_vocab = {w.upper():v for w, v in reversed(ok_vocab)} if case_insensitive else dict(ok_vocab)
        oov_counter, idx_cnt, is_vn_counter = (0, 0, 0)
        sections, section = [], None
        for line_no, line in enumerate(utils.smart_open(questions)):
            line = utils.to_unicode(line)
            if line.startswith(': '):
                if section:
                    sections.append(section)
                    self.log_accuracy(section)
                section = {'section':line.lstrip(': ').strip(), 
                 'correct':[],  'incorrect':[]}
            else:
                idx_cnt += 1
                if not section:
                    raise ValueError('missing section header before line #%i in %s' % (line_no, questions))
                try:
                    if case_insensitive:
                        a, b, c, expected = [word.upper() for word in line.split(' | ')]
                    else:
                        a, b, c, expected = [word for word in line.split(' | ')]
                except ValueError:
                    logger.info('SVX: ERROR skipping invalid line #%i in %s', line_no, questions)
                    print('Line : ', line)
                    print('a, b, c, expected: %s, %s, %s, %s' % (a, b, c, expected))
                    input('>>> Wait ...')
                    continue

                if ' ' in a or ' ' in b or ' ' in c or ' ' in expected:
                    is_vn_counter += 1
                else:
                    if a not in ok_vocab or b not in ok_vocab or c not in ok_vocab or expected not in ok_vocab:
                        logger.debug('SVX: skipping line #%i with OOV words: %s', line_no, line.strip())
                        oov_counter += 1
                        continue
                original_vocab = self.vocab
                self.vocab = ok_vocab
                ignore = {a, b, c}
                predicted = None
                sims = most_similar(self, positive=[b, c], negative=[a], topn=False, restrict_vocab=restrict_vocab)
                self.vocab = original_vocab
                for index in matutils.argsort(sims, reverse=True):
                    predicted = self.index2word[index].upper() if case_insensitive else self.index2word[index]
                    if predicted in ok_vocab:
                        if predicted not in ignore:
                            if predicted != expected:
                                logger.debug('%s: expected %s, predicted %s', line.strip(), expected, predicted)
                        break

                if predicted == expected:
                    section['correct'].append((a, b, c, expected))
                else:
                    section['incorrect'].append((a, b, c, expected))

        if section:
            sections.append(section)
            self.log_accuracy(section)
        total = {'OOV/Total/VNCompound_Words':[
          oov_counter, idx_cnt, is_vn_counter], 
         'section':'total', 
         'correct':sum((s['correct'] for s in sections), []), 
         'incorrect':sum((s['incorrect'] for s in sections), [])}
        self.log_accuracy(total)
        sections.append(total)
        return sections


def convert_conll_format_to_normal(connl_file, out_file):
    """
    read file conll format
    return format : One sentence per line
    sentences_arr: [EU rejects German call .., ...]
    tags_arr: [B-ORG O B-MIST O ..., ...]
    """
    f = open(connl_file)
    sentences = []
    sentence = ''
    for line in f:
        if len(line) == 0 or line.startswith('-DOCSTART') or line[0] == '\n':
            sentences.append(sentence.rstrip())
            sentence = ''
            continue
        else:
            splits = line.split('\t')
            sentence += splits[1].rstrip() + ' '

    if len(sentence) > 0:
        sentences.append(sentence)
        del sentence
    if out_file is None:
        out_file = connl_file + '.std.txt'
    writer = open(out_file, 'w')
    for sen in sentences:
        writer.write(sen + '\n')
        writer.flush()

    writer.close()
    return sentences


def verify_word_analogies(file):
    """
    Verify the word analogy file.
    :param file:
    :return:
    """
    f_reader = open(file, 'r')
    valid_cnt, invalid_cnt = (0, 0)
    for line in f_reader:
        if not len(line) == 0:
            if line.startswith('-DOCSTART') or line[0] == '\n':
                continue
            else:
                splits = line.split('\t')
                if len(splits) != 4:
                    invalid_cnt += 1
                else:
                    valid_cnt += 1

    print('Valid analogy: %s, invalid analogy: %s' % (valid_cnt, invalid_cnt))


def check_oov_of_word_analogies(w2v_format_emb_file, analogy_file, is_vn=True, case_sensitive=True):
    emb_model = gensim.models.KeyedVectors.load_word2vec_format(w2v_format_emb_file, binary=False,
      unicode_errors='ignore')
    f_reader = open(analogy_file, 'r')
    vocab_arr = []
    for line in f_reader:
        if not case_sensitive:
            line = line.lower()
        if line.startswith(': '):
            continue
        else:
            for word in line.split(' | '):
                vocab_arr.append(word)

    print('Before unique set: len = ', len(vocab_arr))
    unique_vocab_arr = set(vocab_arr)
    print('After unique set: len = ', len(unique_vocab_arr))
    valid_word_cnt = 0
    for word in unique_vocab_arr:
        if word in emb_model:
            valid_word_cnt += 1

    print('With Is_VN = %s, case_sensitive = %s, Valid word = %s/%s' % (is_vn,
     case_sensitive,
     valid_word_cnt,
     len(unique_vocab_arr)))


def evaluator_api(input_files, analoglist, output, embed_config=None):
    """

    :param input_files:
    :param analoglist:
    :param output:
    :param embed_config:
    :return:
    """
    if embed_config is None:
        embed_config = EmbeddingConfigs()
    local_embedding_names, local_word_embeddings = embedding_io.load_word_embeddings(input_files, embed_config)
    local_output_str = emb_utils.eval_word_analogy_4_all_embeddings(analoglist, local_embedding_names,
      local_word_embeddings,
      output_file=output)
    print('OUTPUT: ', local_output_str)


if __name__ == '__main__':
    desc = 'Evaluates a word embedding model'
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('-input', required=True,
      default='../data/embedding_dicts/ELMO_23.vec',
      help='Input multiple word embeddings, each model separated by a `;`.')
    parser.add_argument('-analoglist', nargs='?',
      default='../data/embedding_analogies/vi/solveable_analogies_vi.txt',
      help='Input analogy file to run the word analogy evaluation.')
    parser.add_argument('-r', nargs='?',
      default=False,
      help='Vocabulary restriction')
    parser.add_argument('-checkoov', nargs='?',
      default=False,
      help='Check OOV percentage')
    parser.add_argument('-lang', nargs='?',
      default='VI',
      help="Specify language, by default, it's Vietnamese.")
    parser.add_argument('-lowercase', nargs='?',
      default=True,
      help='Lowercase all word analogies? (depends on how the emb was trained).')
    parser.add_argument('-output', nargs='?',
      default='../data/embedding_analogies/vi/results_out.txt',
      help='Output file of word analogy task')
    parser.add_argument('-remove_redundancy', nargs='?',
      default=True,
      help='Remove redundancy in predicted words')
    print('Params: ', parser)
    args = parser.parse_args()
    embedding_config = EmbeddingConfigs()
    paths_of_models = args.input
    testset = args.analoglist
    is_vietnamese = args.lang
    output_file = args.output
    restriction = None
    if args.r:
        restriction = 30000
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=(logging.INFO))
    if args.checkoov:
        print('Checking OOV ...')
        check_oov_of_word_analogies(paths_of_models, testset, is_vn=is_vietnamese)
    if not args.checkoov:
        print('Evaluating embeddings on the word analogy task ...')
        if is_vietnamese:
            print(" ... for ETNLP's evaluation approach.")
            embedding_names, word_embeddings = embedding_io.load_word_embeddings(paths_of_models, embedding_config)
            output_str = emb_utils.eval_word_analogy_4_all_embeddings(testset, embedding_names, word_embeddings, output_file=(args.output_file))
            print('####################')
            print(output_str)
            print('####################')
        else:
            print(" ... for Mirkolov et al.'s evaluation approach.")
            word_analogy_obj = new_Word2VecKeyedVectors(1024)
            model = word_analogy_obj.load_word2vec_format(paths_of_models,
              binary=False,
              unicode_errors='ignore')
            model.accuracy = word_analogy_obj.new_accuracy
            acc = model.accuracy(testset, restrict_vocab=restriction, case_insensitive=False)
            print('Acc = ', acc)
    print('DONE')