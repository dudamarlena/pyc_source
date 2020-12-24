# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/jovyan/search-tools/search_tools/matching.py
# Compiled at: 2019-10-08 18:59:06
# Size of source mod 2**32: 5312 bytes
import numpy as np
import pyspark.sql.functions as F
import pyspark.sql.types as T
from pyspark.ml.feature import IDF, Tokenizer, CountVectorizer

def isin(element, test_elements, assume_unique=False, invert=False):
    """
    Impliments the numpy function isin() for legacy versions of
    the library
    """
    element = np.asarray(element)
    return np.in1d(element, test_elements, assume_unique=assume_unique, invert=invert).reshape(element.shape)


udf_template = '\ndef bm25(query, tf, idf):\n    \n    mean_dl = {}\n    k = {}\n    b = {}\n    \n    idf_values, tf_indices, tf_values, query_indices = idf.values, tf.indices, tf.values, query.indices\n    freq_nidx = tf_indices[-1]+1\n    freq_indices = np.concatenate((tf_indices, np.array([freq_nidx])))\n    term_frequencies = np.concatenate((tf_values, np.array([0.0])))\n    \n    #get idf vector\n    idf_ = idf_values\n    \n    #get term frequencies\n    intersect = np.intersect1d(query_indices, freq_indices)\n    idx = np.where(isin(query_indices, intersect), query_indices, freq_nidx)\n    freq_idx = np.searchsorted(freq_indices, idx)\n    tf_ = term_frequencies[freq_idx].reshape(-1)\n    \n    #get doc length\n    dl_ = tf_values.sum()\n    \n    #get scores used to compute bm25\n    ntf_ = tf_ / dl_\n    ntf_score = ntf_.sum()\n    tf_score = tf_.sum()\n    tfidf_score = np.dot(ntf_, idf_)\n    \n    #get bm25\n    n_term = k * (1 - b + b * dl_/mean_dl)\n    bm25 = np.dot(idf_, (tf_ * (k + 1)) / ((tf_) + n_term))\n    \n    #return all scores\n    return T.Row(\'tf\', \'ntf\', \'tfidf\', \'bm25\')(float(tf_score), float(ntf_score), float(tfidf_score), float(bm25))\n    \nschema = T.StructType([\n    T.StructField("tf", T.FloatType(), False),\n    T.StructField("ntf", T.FloatType(), False),\n    T.StructField("tfidf", T.FloatType(), False),\n    T.StructField("bm25", T.FloatType(), False)])\n    \nself.udf = F.udf(bm25, returnType=schema)\n'

class BM25Model(object):
    __doc__ = '\n    Computes BM25 score.\n    '

    def __init__(self, k=1.2, b=0.75):
        self.k = k
        self.b = b
        self.tok = Tokenizer(inputCol='__input', outputCol='__tokens')
        self.vec = CountVectorizer(inputCol='__tokens', outputCol='__counts')
        self.idf = IDF(inputCol='__counts', outputCol='__idf')
        self.train_col = None
        self.udf = None
        self.is_fit = False

    def fit(self, df, train_col):
        """
        Does fitting on input df.
            df: a pyspark dataframe.
            train_col (string): The name of the column containing training documents.
            
        Returns: self, a 
        """
        self.train_col = train_col
        df_ = self.tok.transform(df.withColumnRenamed(train_col, '__input'))
        mean_dl = df_.select(F.mean(F.size(F.col('__tokens')))).collect()[0][0]
        self.vec = self.vec.fit(df_)
        df_ = self.vec.transform(df_)
        self.idf = self.idf.fit(df_)
        exec(udf_template.format(mean_dl, self.k, self.b))
        self.is_fit = True
        return self

    def transform(self, df, score_col, bm25_output_name='bm25', tf_output_name=None, ntf_output_name=None, tfidf_output_name=None):
        """
        Computes BM25 score, 
            along with normalized term frequency (ntf) and tfidf.
            These three additional scores come "for free" with bm25
            but are only returned optionally.
        """
        if not self.is_fit:
            raise Exception('You must fit the BM25 model with a call to .fit() first.')
        columns = df.columns
        df_ = self.tok.transform(df.withColumnRenamed(score_col, '__input'))
        df_ = self.vec.transform(df_)
        df_ = self.idf.transform(df_)
        df_ = df_.withColumnRenamed('__counts', '__query_counts').withColumnRenamed('__input', score_col).select(columns + [score_col, '__query_counts', '__idf'])
        df_ = self.tok.transform(df_.withColumnRenamed(self.train_col, '__input'))
        df_ = self.vec.transform(df_)
        df_ = df_.withColumnRenamed('__counts', '__item_counts')
        df_ = df_.withColumn('bm25', self.udf(F.col('__query_counts'), F.col('__item_counts'), F.col('__idf')))
        df_ = df_.withColumnRenamed('__input', self.train_col)
        computed_values = df_.withColumn('more', F.explode(F.array(F.col('bm25')))).select(columns + ['bm25.*'])
        final_selection = columns
        if bm25_output_name is not None:
            computed_values = computed_values.withColumnRenamed('bm25', bm25_output_name)
            final_selection.append(bm25_output_name)
        if tf_output_name is not None:
            computed_values = computed_values.withColumnRenamed('tf', tf_output_name)
            final_selection.append(tf_output_name)
        if ntf_output_name is not None:
            computed_values = computed_values.withColumnRenamed('ntf', ntf_output_name)
            final_selection.append(ntf_output_name)
        if tfidf_output_name is not None:
            computed_values = computed_values.withColumnRenamed('tfidf', tfidf_output_name)
            final_selection.append(tfidf_output_name)
        return computed_values.select(final_selection)