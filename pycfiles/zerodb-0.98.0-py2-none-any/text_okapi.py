# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /zerodb/catalog/indexes/text_okapi.py
# Compiled at: 2016-03-05 15:57:06
import itertools
from BTrees.Length import Length
from zope.index.text.okapiindex import OkapiIndex as _OkapiIndex
from zerodb import trees
from zerodb.storage import prefetch_trees, parallel_traversal
from zerodb.catalog.indexes.pwid import PersistentWid

class OkapiIndex(_OkapiIndex):

    def clear(self):
        self._wordinfo = trees.family32.IO.BTree()
        self._docweight = self.family.IF.BTree()
        self._docwords = self.family.IO.BTree()
        self.wordCount = Length()
        self.documentCount = Length()

    def _mass_add_wordinfo(self, wid2weight, docid):
        dicttype = type({})
        get_doc2score = self._wordinfo.get
        new_word_count = 0
        wids = wid2weight.keys()
        parallel_traversal(self._wordinfo, wids)
        parallel_traversal(map(get_doc2score, wids), [docid] * len(wids))
        for wid, weight in wid2weight.items():
            doc2score = get_doc2score(wid)
            if doc2score is None:
                doc2score = {}
                new_word_count += 1
            elif isinstance(doc2score, dicttype) and len(doc2score) == self.DICT_CUTOFF:
                doc2score = self.family.IF.BTree(doc2score)
            doc2score[docid] = weight
            self._wordinfo[wid] = doc2score

        try:
            self.wordCount.change(new_word_count)
        except AttributeError:
            self.wordCount = Length(len(self._wordinfo))

        return

    def index_doc(self, docid, text):
        if docid in self._docwords:
            return self._reindex_doc(docid, text)
        wids = self._lexicon.sourceToWordIds(text)
        wid2weight, docweight = self._get_frequencies(wids)
        self._mass_add_wordinfo(wid2weight, docid)
        self._docweight[docid] = docweight
        self._docwords[docid] = PersistentWid.encode_wid(wids)
        try:
            self.documentCount.change(1)
        except AttributeError:
            self.documentCount = Length(len(self._docweight))

        count = len(wids)
        self._change_doc_len(count)
        return count

    def _reindex_doc(self, docid, text):
        self._change_doc_len(-self._docweight[docid])
        old_wids = self.get_words(docid)
        old_wid2w, old_docw = self._get_frequencies(old_wids)
        new_wids = self._lexicon.sourceToWordIds(text)
        new_wid2w, new_docw = self._get_frequencies(new_wids)
        old_widset = self.family.IF.TreeSet(old_wid2w.keys())
        new_widset = self.family.IF.TreeSet(new_wid2w.keys())
        IF = self.family.IF
        in_both_widset = IF.intersection(old_widset, new_widset)
        only_old_widset = IF.difference(old_widset, in_both_widset)
        only_new_widset = IF.difference(new_widset, in_both_widset)
        del old_widset
        del new_widset
        for wid in only_old_widset.keys():
            self._del_wordinfo(wid, docid)

        for wid in only_new_widset.keys():
            self._add_wordinfo(wid, new_wid2w[wid], docid)

        for wid in in_both_widset.keys():
            newscore = new_wid2w[wid]
            if old_wid2w[wid] != newscore:
                self._add_wordinfo(wid, newscore, docid)

        self._docweight[docid] = new_docw
        self._docwords[docid] = PersistentWid.encode_wid(new_wids)
        return len(new_wids)

    def get_words(self, docid):
        """Return a list of the wordids for a given docid."""
        return self._docwords[docid].decode_wid()

    def _search_wids(self, wids):
        if len(wids) > 1:
            parallel_traversal(self._wordinfo, wids)
        prefetch_trees([ self._wordinfo[wid] for wid in wids ])
        docids = list(set(itertools.chain(*[ self._wordinfo[wid].keys() for wid in wids ])))
        if len(docids) > 1:
            parallel_traversal(self._docweight, docids)
        return super(OkapiIndex, self)._search_wids(wids)