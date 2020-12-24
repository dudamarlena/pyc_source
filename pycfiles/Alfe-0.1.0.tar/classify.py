# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/alfanous/Support/whoosh/classify.py
# Compiled at: 2015-06-30 06:52:38
__doc__ = 'Classes and functions for classifying and extracting information from\ndocuments.\n'
from collections import defaultdict
from math import log

class ExpansionModel(object):

    def __init__(self, ixreader, fieldname):
        self.N = float(ixreader.doc_count_all())
        self.collection_total = ixreader.field_length(fieldname)
        self.mean_length = self.collection_total / self.N

    def normalizer(self, maxweight, top_total):
        raise NotImplementedError

    def score(self, weight_in_top, weight_in_collection, top_total):
        raise NotImplementedError


class Bo1Model(ExpansionModel):

    def normalizer(self, maxweight, top_total):
        f = maxweight / self.N
        return (maxweight * log((1.0 + f) / f) + log(1.0 + f)) / log(2.0)

    def score(self, weight_in_top, weight_in_collection, top_total):
        f = weight_in_collection / self.N
        return weight_in_top * log((1.0 + f) / f, 2) + log(1.0 + f, 2)


class Bo2Model(ExpansionModel):

    def normalizer(self, maxweight, top_total):
        f = maxweight * self.N / self.collection_total
        return maxweight * log((1.0 + f) / f, 2) + log(1.0 + f, 2)

    def score(self, weight_in_top, weight_in_collection, top_total):
        f = weight_in_top * top_total / self.collection_total
        return weight_in_top * log((1.0 + f) / f, 2) + log(1.0 + f, 2)


class KLModel(ExpansionModel):

    def normalizer(self, maxweight, top_total):
        return maxweight * log(self.collection_total / top_total) / log(2.0) * top_total

    def score(self, weight_in_top, weight_in_collection, top_total):
        wit_over_tt = weight_in_top / top_total
        wic_over_ct = weight_in_collection / self.collection_total
        if wit_over_tt < wic_over_ct:
            return 0
        else:
            return wit_over_tt * log(wit_over_tt / (weight_in_top / self.collection_total), 2)


class Expander(object):
    """Uses an ExpansionModel to expand the set of query terms based on the top
    N result documents.
    """

    def __init__(self, ixreader, fieldname, model=Bo1Model):
        """
        :param reader: A :class:whoosh.reading.IndexReader object.
        :param fieldname: The name of the field in which to search.
        :param model: (classify.ExpansionModel) The model to use for expanding
            the query terms. If you omit this parameter, the expander uses
            scoring.Bo1Model by default.
        """
        self.fieldname = fieldname
        if type(model) is type:
            model = model(ixreader, fieldname)
        self.model = model
        self.collection_freq = dict((word, freq) for word, _, freq in ixreader.iter_field(fieldname))
        self.topN_weight = defaultdict(float)
        self.top_total = 0

    def add(self, vector):
        """Adds forward-index information about one of the "top N" documents.
        
        :param vector: A series of (text, weight) tuples, such as is
            returned by Reader.vector_as("weight", docnum, fieldnum).
        """
        total_weight = 0
        topN_weight = self.topN_weight
        for word, weight in vector:
            total_weight += weight
            topN_weight[word] += weight

        self.top_total += total_weight

    def expanded_terms(self, number, normalize=True):
        """Returns the N most important terms in the vectors added so far.
        
        :param number: The number of terms to return.
        :param normalize: Whether to normalize the weights.
        :*returns*: A list of ("term", weight) tuples.
        """
        model = self.model
        tlist = []
        maxweight = 0
        collection_freq = self.collection_freq
        for word, weight in self.topN_weight.iteritems():
            score = model.score(weight, collection_freq[word], self.top_total)
            if score > maxweight:
                maxweight = score
            tlist.append((score, word))

        if normalize:
            norm = model.normalizer(maxweight, self.top_total)
        else:
            norm = maxweight
        tlist = [ (weight / norm, t) for weight, t in tlist ]
        tlist.sort(reverse=True)
        return [ (t, weight) for weight, t in tlist[:number] ]