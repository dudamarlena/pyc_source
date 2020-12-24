# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/drqascripts/retriever/build_tfidf.py
# Compiled at: 2019-08-29 06:03:42
# Size of source mod 2**32: 7028 bytes
"""A script to build the tf-idf document matrices for retrieval."""
import numpy as np, scipy.sparse as sp, argparse, os, math, logging
from multiprocessing import Pool as ProcessPool
from multiprocessing.util import Finalize
from functools import partial
from collections import Counter
from drqa import retriever
from drqa import tokenizers
logger = logging.getLogger('DRQA')

class TfIdfBuilder:

    def __init__(self, args, db, db_opts):
        self.DOC2IDX = None
        self.PROCESS_TOK = None
        self.PROCESS_DB = None
        self.args = args
        tok_class = tokenizers.get_class(args.tokenizer)
        db_class = retriever.get_class(db)
        self.PROCESS_TOK = tok_class()
        self.PROCESS_DB = db_class(**db_opts)

    def init_thread(self):
        Finalize((self.PROCESS_TOK), (self.PROCESS_TOK.shutdown), exitpriority=100)
        Finalize((self.PROCESS_DB), (self.PROCESS_DB.close), exitpriority=100)

    def fetch_text(self, doc_id):
        return self.PROCESS_DB.get_doc_text(doc_id)

    def tokenize(self, text):
        return self.PROCESS_TOK.tokenize(text)

    def count(self, ngram, hash_size, doc_id):
        """Fetch the text of a document and compute hashed ngrams counts."""
        row, col, data = [], [], []
        tokens = self.tokenize(retriever.utils.normalize(self.fetch_text(doc_id)))
        ngrams = tokens.ngrams(n=ngram,
          uncased=True,
          filter_fn=(retriever.utils.filter_ngram))
        counts = Counter([retriever.utils.hash(gram, hash_size) for gram in ngrams])
        row.extend(counts.keys())
        col.extend([self.DOC2IDX[doc_id]] * len(counts))
        data.extend(counts.values())
        return (row, col, data)

    def get_count_matrix(self):
        """Form a sparse word to document count matrix (inverted index).

        M[i, j] = # times word i appears in document j.
        """
        doc_ids = self.PROCESS_DB.get_doc_ids()
        self.DOC2IDX = {doc_id:i for i, doc_id in enumerate(doc_ids)}
        logger.info('Mapping...')
        row, col, data = [], [], []
        step = max(int(len(doc_ids) / 10), 1)
        batches = [doc_ids[i:i + step] for i in range(0, len(doc_ids), step)]
        _count = partial(self.count, self.args.ngram, self.args.hash_size)
        for i, batch in enumerate(batches):
            logger.info('-' * 25 + 'Batch %d/%d' % (i + 1, len(batches)) + '-' * 25)
            for b_row, b_col, b_data in map(_count, batch):
                row.extend(b_row)
                col.extend(b_col)
                data.extend(b_data)

        logger.info('Creating sparse matrix...')
        count_matrix = sp.csr_matrix((
         data, (row, col)),
          shape=(self.args.hash_size, len(doc_ids)))
        count_matrix.sum_duplicates()
        return (count_matrix, (self.DOC2IDX, doc_ids))

    def get_tfidf_matrix(self, cnts):
        """Convert the word count matrix into tfidf one.

        tfidf = log(tf + 1) * log((N - Nt + 0.5) / (Nt + 0.5))
        * tf = term frequency in document
        * N = number of documents
        * Nt = number of occurences of term in all documents
        """
        Ns = self.get_doc_freqs(cnts)
        idfs = np.log((cnts.shape[1] - Ns + 0.5) / (Ns + 0.5))
        idfs[idfs < 0] = 0
        idfs = sp.diags(idfs, 0)
        tfs = cnts.log1p()
        tfidfs = idfs.dot(tfs)
        return tfidfs

    def get_doc_freqs(self, cnts):
        """Return word --> # of docs it appears in."""
        binary = (cnts > 0).astype(int)
        freqs = np.array(binary.sum(1)).squeeze()
        return freqs


if __name__ == '__main__':
    logger.setLevel(logging.INFO)
    fmt = logging.Formatter('%(asctime)s: [ %(message)s ]', '%m/%d/%Y %I:%M:%S %p')
    console = logging.StreamHandler()
    console.setFormatter(fmt)
    logger.addHandler(console)
    parser = argparse.ArgumentParser()
    parser.add_argument('db_path', type=str, default=None, help='Path to sqlite db holding document texts')
    parser.add_argument('out_dir', type=str, default=None, help='Directory for saving output files')
    parser.add_argument('--ngram', type=int, default=2, help='Use up to N-size n-grams (e.g. 2 = unigrams + bigrams)')
    parser.add_argument('--hash-size', type=int, default=(int(math.pow(2, 24))), help='Number of buckets to use for hashing ngrams')
    parser.add_argument('--tokenizer', type=str, default='simple', help="String option specifying tokenizer type to use (e.g. 'corenlp')")
    parser.add_argument('--num-workers', type=int, default=None, help='Number of CPU processes (for tokenizing, etc)')
    args = parser.parse_args()
    logging.info('Counting words...')
    tb = TfIdfBuilder(args, 'sqlite', {'db_path': args.db_path})
    count_matrix, doc_dict = tb.get_count_matrix()
    logger.info('Making tfidf vectors...')
    tfidf = tb.get_tfidf_matrix(count_matrix)
    logger.info('Getting word-doc frequencies...')
    freqs = tb.get_doc_freqs(count_matrix)
    basename = os.path.splitext(os.path.basename(args.db_path))[0]
    basename += '-tfidf-ngram=%d-hash=%d-tokenizer=%s' % (
     args.ngram, args.hash_size, args.tokenizer)
    filename = os.path.join(args.out_dir, basename)
    logger.info('Saving to %s.npz' % filename)
    metadata = {'doc_freqs':freqs, 
     'tokenizer':args.tokenizer, 
     'hash_size':args.hash_size, 
     'ngram':args.ngram, 
     'doc_dict':doc_dict}
    retriever.utils.save_sparse_csr(filename, tfidf, metadata)