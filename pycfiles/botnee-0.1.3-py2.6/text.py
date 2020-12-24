# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/botnee/process/text.py
# Compiled at: 2012-08-16 08:02:11
"""Main text processing engine."""
import re, codecs, numpy as np
from time import time
import datetime
from bidict import bidict
import logging, itertools, hashlib, csv, nltk, shelve
from collections import defaultdict
import botnee_config
from botnee.process.meta_dict import MetaDict
from botnee.process.data_dict import DataDict
from botnee.process.time_dict import TimeDict
from botnee.doc_store import DocStore
from botnee.standard_document import StandardDocument
from botnee import debug, errors
from botnee.taxonomy.metamap_wrapper import MetamapWrapper
from botnee.counter import OrderedCounter
process_text_logger = logging.getLogger(__name__)
if type(botnee_config.STEMMER) in [str, unicode]:
    if botnee_config.STEMMER.lower() not in ('porter', 'lancaster', 'snowball', 'snowball2'):
        raise TypeError('Stemmer %s not supported' % botnee_config.STEMMER)
    stemmer = eval('nltk.stem.%sStemmer()' % botnee_config.STEMMER.title())
else:
    stemmer = None
if botnee_config.METAMAP:
    metamap = MetamapWrapper()
regular_expressions = {'emails': re.compile('^[A-Z0-9a-z._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,4}$'), 
   'urls': re.compile('[fh][t]?tp[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'), 
   'dois': re.compile('[(][A-Za-z0-9-:;,.\\s]*(doi:)[A-Za-z0-9-:;,.\\s]*[)]'), 
   'refs': re.compile('[A-Z]{3,} [0-9]{4}; [0-9]+: [a-z]+[0-9]+'), 
   'acronyms': re.compile('([A-Za-z0-9-\\s]+)([(][A-Z]+[A-Za-z\\s]+?[)])'), 
   'tokenise': re.compile('[0-9a-zA-Z]+[0-9a-zA-Z]*[-]*[0-9a-zA-Z]*[0-9a-zA-Z]+'), 
   'in_paren': re.compile('\\([^)\\s]*\\)')}

def constant_factory(value):
    """A constant value generator for defaultdict"""
    return itertools.repeat(value).next


def get_caster(ngram):
    """Used to cast values depending whether they are tokens or ngrams"""
    if ngram == 1:
        return unicode
    else:
        return tuple


class DictWrapperMongo(object):

    def __init__(self, table):
        self._tab = table

    def __setitem__(self, key, value):
        doc = {'_id': key, 'value': value}
        self._tab.insert(doc)

    def __getitem__(self, key):
        cursor = self._tab.find({'_id': key})
        if cursor.count() == 1:
            return cursor[0]['value']
        raise KeyError(key)


class DictWrapperShelve(object):

    def __init__(self, shelf):
        self._shelf = shelf

    def __del__(self):
        self._shelf.close()


class Dictionaries(list):

    def __init__(self, doc_store=None, verbose=False):
        for ngram in botnee_config.NGRAMS.keys():
            if doc_store:
                table = doc_store._database[('dictionary_%d' % ngram)]
                self.append(DictWrapperMongo(table))
            else:
                filename = '%s_%d.dat' % (botnee_config.DICTIONARY_FILE, ngram)
                shelf = shelve.open(filename, flag='c', protocol=None, writeback=False)
                self.append(DictWrapperShelve(shelf))

        return


def get_stopword_dictionary(ngram):
    """Loads the stopword dictionary from disk."""
    try:
        swinfo = botnee_config.STOPWORD_FILES[ngram]
    except KeyError:
        errors.ProcessWarning('Stopword file not defined for %d' % ngram)
        return {}

    if not swinfo:
        return {}
    fname = swinfo['filename']
    with codecs.open(fname, encoding='utf-8') as (f):
        if swinfo['type'] == 'text':
            swdict = dict((hash(x.strip()), i) for (i, x) in enumerate(f.readlines()))
        elif swinfo['type'] == 'csv':
            csv_reader = csv.reader(f)
            column = swinfo['extra']
            swdict = dict((eval(r[column]), i) for (i, r) in enumerate(csv_reader))
    return swdict


stopword_dictionary = {}
for key in botnee_config.STOPWORD_FILES.keys():
    stopword_dictionary[key] = get_stopword_dictionary(int(key))

def process_docs(docs, meta_dict, data_dict, time_dict, doc_store, reindex=False, verbose=False):
    """
    Helper function to processes the documents (tokenising etc), 
    and creates token hash lists and dictionaries
    
    Will accept documents that are already in the corpus, in which case the old 
    docs are overwritten. 
    
    Docs can be provided as a list or as a generator
    
    If reindex=True the dictionary is recalculated when adding new docs in.

    New meta data is written into the meta_dict dictionary structure.
    """
    if type(docs) is list and len(docs) > 0:
        if type(docs[0]) is not StandardDocument:
            msg = 'expected list of StandardDict got ' + str(type(docs[0]))
            raise TypeError(msg)
    if type(meta_dict) is not MetaDict:
        raise TypeError('expected MetaDict got ' + str(type(meta_dict)))
    if type(data_dict) is not DataDict:
        raise TypeError('expected DataDict got ' + str(type(data_dict)))
    if type(time_dict) is not TimeDict:
        raise TypeError('expected TimeDict got ' + str(type(time_dict)))
    if type(doc_store) is not DocStore:
        raise TypeError('expected DocStore got ' + str(type(doc_store)))
    with debug.Timer('reindex=%s' % str(reindex), time_dict, verbose, process_text_logger):
        meta_dict.update({'inserts': [], 'updates': [], 'deletes': [], 'pseudos': [], 'failures': []})
        docs_to_insert = []
        meta_dict['guids'] = doc_store.get_guid_indices()
        if meta_dict['last_index'] == -1 and len(meta_dict['guids']) > 0:
            meta_dict['last_index'] = max(meta_dict['guids'].values())

        def put_guid(guid, meta_dict):
            """Helper function to control index creation for guids"""
            meta_dict['last_index'] += 1
            index = meta_dict['last_index']
            meta_dict['guids'][guid] = index
            if guid not in meta_dict['guids']:
                meta_dict['inserts'].append(guid)
            else:
                index = meta_dict['guids'][guid]
                meta_dict['updates'].append(guid)
            return index

        count = 0
        for doc in docs:
            old_len = len(meta_dict['tokens_map_1'])
            count += 1
            if meta_dict.has_key('STOP_AT') and meta_dict['STOP_AT'] > 0:
                if count > meta_dict['STOP_AT']:
                    break
            try:
                count_string = '%d/%d' % (count, meta_dict['n_docs_in_queue'])
            except KeyError:
                count_string = '%d' % count

            if type(doc) is not StandardDocument:
                raise TypeError('Expected StandardDocument got ' + str(type(doc)))
            if doc.check_for_failures() is not None:
                meta_dict['failures'].append(doc['guid'])
                continue
            guid = doc['guid']
            doc['index'] = put_guid(guid, meta_dict)
            process_doc(doc, count_string, verbose)
            del doc['sentences']
            try:
                doc_store.update(doc, verbose)
            except Exception, e:
                raise e

        if meta_dict.has_key('n_docs_in_queue'):
            del meta_dict['n_docs_in_queue']
        meta_dict['n_docs'] = doc_store.get_num_docs(verbose)
        if reindex and meta_dict['n_docs'] > 0:
            debug.print_verbose('REINDEXING...', verbose, process_text_logger)
            for ngram in botnee_config.NGRAMS.keys():
                ngstr = '_%d' % ngram
                tokens_lists = doc_store.get_ngram_lists_by_guid(meta_dict['guids'], ngram)
                create_token_map(tokens_lists, doc_store, meta_dict, data_dict, time_dict, ngram, verbose)

            if meta_dict['n_docs'] > 1:
                for (ngram, value) in botnee_config.NGRAMS.items():
                    (good_ids, bad_ids) = filter_extremes(meta_dict, data_dict, time_dict, value['min_frequency'], value['max_proportion'], value['max_dict_size'], ngram, verbose)

            if len(meta_dict['inserts']) < meta_dict['n_docs']:
                meta_dict['updates'] = meta_dict['guids'].keys()
    return


def update_dictionaries(dictionaries, doc, verbose=False):
    """
    Updates the dictionaries (tokens, ngrams etc)
    """
    with debug.Timer(None, None, verbose, process_text_logger):
        for (i, ngram) in enumerate(botnee_config.NGRAMS.keys()):
            ngstr = '_%d' % ngram
            for sentence in doc[('tokens' + ngstr)]:
                for token in sentence:
                    if botnee_config.DEBUG:
                        if ngram == 1:
                            if type(token) is not unicode:
                                raise TypeError('Incorrect token type')
                        elif len(token) != ngram:
                            raise errors.ProcessError('Incorrect NGRAM length')
                    dictionaries[i][hash(token)] = token

    return


def process_raw_text(title, abstract, body, meta_dict, data_dict, pseudo_meta_dict, verbose=False):
    """
    Process raw text as if it were a document - for raw text retrieval.
    """
    with debug.Timer('Processing raw text', None, verbose, process_text_logger):
        doc = create_pseudo_doc(title, abstract, body)
        process_doc(doc, '1/1', verbose)
        if len(doc['tokens_1']) == 0:
            debug.print_verbose('Failed - no tokens in body', verbose, process_text_logger)
            return
        pseudo_meta_dict.update({'guids': bidict({doc['guid']: 0}), 
           'inserts': [], 'updates': [], 'deletes': [], 'pseudos': [
                     doc['guid']], 
           'last_index': 0, 
           'n_docs': 1})
        for ngram in botnee_config.NGRAMS.keys():
            ngstr = '_%d' % ngram
            pseudo_meta_dict.update({'tokens_map' + ngstr: meta_dict[('tokens_map' + ngstr)], 
               'tokens_map_inv' + ngstr: meta_dict[('tokens_map_inv' + ngstr)]})
            for suffix in botnee_config.SUFFIXES:
                pseudo_meta_dict['tokens' + suffix + ngstr] = {doc['guid']: doc[('tokens' + suffix + ngstr)]}

    return


def process_raw_tokens(tokens_dict, meta_dict, data_dict, pseudo_meta_dict, verbose=False):
    """
    Process lists of tokens (ngrams included) as if it were a document
    """
    with debug.Timer('Processing tokens lists', None, verbose, process_text_logger):
        doc = create_pseudo_doc(None, None, None)
        pseudo_meta_dict.update({'guids': bidict({doc['guid']: 0}), 
           'inserts': [], 'updates': [], 'deletes': [], 'pseudos': [
                     doc['guid']], 
           'last_index': 0, 
           'n_docs': 1})
        for ngram in botnee_config.NGRAMS.keys():
            ngstr = '_%d' % ngram
            pseudo_meta_dict.update({'tokens_map' + ngstr: meta_dict[('tokens_map' + ngstr)], 
               'tokens_map_inv' + ngstr: meta_dict[('tokens_map_inv' + ngstr)]})
            for suffix in botnee_config.SUFFIXES:
                full_name = 'tokens' + suffix + ngstr
                if full_name not in tokens_dict:
                    pseudo_meta_dict[full_name] = {doc['guid']: []}
                    continue
                msg = full_name + ' (%s tokens)' % len(tokens_dict[full_name])
                debug.print_verbose(msg, verbose, process_text_logger)
                pseudo_meta_dict[full_name] = {doc['guid']: tokens_dict[full_name]}

    return


def create_pseudo_doc(title, abstract, body):
    guid = hashlib.md5(str(time())).hexdigest()
    doc = StandardDocument({'title': title, 
       'guid': guid, 
       'publication': '', 
       'url': '', 
       'publication-date': datetime.date.today(), 
       'abstract': abstract, 
       'body': body, 
       'content-type': 'text/plain'})
    return doc


def process_doc(doc, count_string, verbose=False):
    """
    Calls all of the text proessing functions and stores original body 
    along with processed body to be stored. Also stores computation time
    """
    with debug.Timer(doc['guid'], None, verbose, process_text_logger):
        (tokens, data) = process_text(doc['body'])
        doc['tags'] = []
        doc['tokens_1'] = tokens
        doc['tokens_abstract_1'] = []
        doc['tokens_title_1'] = []
        if 'abstract' in doc and len(doc['abstract']) > 0:
            (tokens_abstract, abs_data) = process_text(doc['abstract'])
            if len(doc['tokens_1']) == 0:
                doc['tokens_1'] = tokens_abstract
            doc['tokens_abstract_1'] = tokens_abstract
        (tokens_title, _) = process_text(doc['title'])
        if len(doc['tokens_1']) == 0 and len(doc['tokens_abstract_1']) == 0:
            doc['tokens_1'] = tokens_title
        doc['tokens_title_1'] = tokens_title
        if botnee_config.METAMAP:
            if 'abstract' in doc and len(doc['abstract']) > 0:
                sentences = abs_data['sentences']
            else:
                sentences = data['sentences']
            if sum(map(lambda x: len(x), sentences)) > 5000:
                for sentence in sentences:
                    doc['tags'] += metamap.query_by_text(sentence, False)

            else:
                text = ('').join([ s + '\n' for s in sentences ])
                doc['tags'] = metamap.query_by_text(text, False)
            msg = '%d tags found' % len(doc['tags'])
            debug.print_verbose(msg, verbose, process_text_logger)
        for ngram in botnee_config.NGRAMS.keys():
            ngstr = '_%d' % ngram
            for suffix in botnee_config.SUFFIXES:
                if ngram == 1:
                    tokens = doc[('tokens' + suffix + ngstr)]
                else:
                    tokens = get_ngrams(doc[('tokens%s_1' % suffix)], ngram)
                    doc['tokens' + suffix + ngstr] = tokens
                doc['tokens' + suffix + ngstr + '_len'] = len(tokens)

        if 'body' in doc:
            del doc['body']
        if 'abstract' in doc:
            del doc['abstract']
        doc.update(data)
    return


def process_text(text):
    """
    Full processing function: runs sanitise_text(), 
    tokenise() and remove_stopwords().
    """
    (text, data) = sanitise_text(text)
    data['sentences'] = nltk.sent_tokenize(text)
    sentences = [ remove_stopwords(tokenise(s), 1) for s in data['sentences'] ]
    if stemmer:
        stemmed = []
        for sentence in sentences:
            stemmed.append([ stemmer.stem(token) for token in sentence ])

        sentences = stemmed
    return (
     sentences, data)


def sanitise_text(text):
    """Sanitise text (remove emails, urls, dois)."""
    data = {}
    text = text.replace('\n', ' ')
    (text, data['emails']) = extract_emails(text)
    (text, data['urls']) = extract_urls(text)
    (text, data['dois']) = extract_dois(text)
    (text, data['refs']) = extract_refs(text)
    (text, data['acronyms']) = extract_acronyms(text)
    return (
     text, data)


def extract_emails(text):
    """
    Extracts emails using a regex, returns remaining text and list of emails
    """
    emails = regular_expressions['emails'].findall(text.lower())
    text = ('').join(regular_expressions['emails'].split(text))
    return (text, emails)


def extract_urls(text):
    """Extracts urls using a regex, returns remaining text and list of urls"""
    urls = regular_expressions['urls'].findall(text.lower())
    text = ('').join(regular_expressions['urls'].split(text))
    return (text, urls)


def extract_refs(text):
    """Extract refs of the form "BMJ 2010; 341: c4229" and store them"""
    refs = regular_expressions['refs'].findall(text)
    text = ('').join(regular_expressions['refs'].split(text))
    return (text, refs)


def extract_dois(text):
    """Extracts DOIs using a regex, returns remaining text and list of DOIs"""
    dois = regular_expressions['dois'].findall(text)
    text = ('').join(regular_expressions['dois'].split(text))
    return (text, dois)


def extract_acronyms(text):
    """
    Extracts acronyms using Schwartz Hearst algorithm.
    Currently only looks for:    An Acronym Like This (AALT)
    Would also like to look for: AALT (An Acronym Like This)
    """
    result = regular_expressions['acronyms'].findall(text)
    result = filter(lambda x: len(x[0]) > len(x[1]), result)
    result = filter(lambda x: regular_expressions['in_paren'].findall(x[1]), result)
    result = [ (find_best_long_form(r[1], r[0]), r[1]) for r in result ]
    result = filter(lambda x: x[0] is not None, result)
    acronyms = filter(lambda x: len(x[0].split(' ')) <= min(len(x[1]) + 5, len(x[1]) * 2), result)
    for a in acronyms:
        text = ('').join(re.split(a[0], text))

    return (text, acronyms)


def find_best_long_form(short_form, long_form):
    """
    Method findBestLongForm takes as input a short-form and a long-
    form candidate (a list of words) and returns the best long-form
    that matches the short-form, or null if no match is found.
    """
    short_index = len(short_form) - 1
    long_index = len(long_form) - 1
    for c_short in short_form[::-1]:
        curr_char = c_short.lower()
        short_index -= 1
        if not curr_char.isalnum():
            continue
        while long_index >= 0 and (long_form[long_index].lower() != curr_char or short_index == 0 and long_index > 0 and long_form[(long_index - 1)].isalnum()):
            long_index -= 1

        if long_index < 0:
            return
        long_index -= 1

    long_index = long_form.find(' ', long_index) + 1
    return long_form[long_index:-1]


def extract_sentence_boundaries(text):
    boundaries = []
    return boundaries


def tokenise(text):
    """
    Tokeniser. Uses a simple regex that allows hypens and apostrophes.
    Also makes sure tokens are between 3 and 20 characters long
    """
    tokens = regular_expressions['tokenise'].findall(text.lower())
    tokens = filter(lambda x: len(x) > 1, tokens)
    tokens = filter(lambda x: len(x) < 21, tokens)
    return tokens


def remove_stopwords(tokens, ngram):
    """
    Removes stopwords using the loaded stopword file. 
    Returns remaining tokens.
    """
    swlist = stopword_dictionary[ngram]
    tokens_trimmed = [ x for x in tokens if hash(x) not in swlist ]
    return tokens_trimmed


def get_ngrams(sentences, ng, verbose=False):
    """ 
    Gets ngrams from tokens
    """
    ng_lists = []
    for tokens_list in sentences:
        if type(tokens_list) is not list:
            debug.debug_here()
        if len(tokens_list) < ng:
            continue
        if len(tokens_list) == ng:
            ng_lists.append([tuple(tokens_list)])
            continue
        ng_list = []
        for i in xrange(0, ng):
            ng_list.append(tokens_list[i:-ng + i])

        ng_lists.append(zip(*ng_list))
        ng_lists[-1] = remove_stopwords(ng_lists[(-1)], ng)

    if botnee_config.DEBUG and ng > 1:
        for ngl in ng_lists:
            for ngram in ngl:
                if len(ngram) != ng:
                    debug.debug_here()

    return ng_lists


def create_token_map(tokens_lists_by_guid, doc_store, meta_dict, data_dict, time_dict, ngram=1, verbose=False):
    """
    Creates hash map which is the mapping of tokens to indices.
    Also creates the reverse mapping for indices to tokens
    
    Updates the fields (token_map, token_map_inv) in meta_dict
    """
    with debug.Timer('(%d)' % ngram, time_dict, verbose, process_text_logger):
        ngstr = '_%d' % ngram
        caster = get_caster(ngram)
        tokens_map = defaultdict(constant_factory(-1))
        tokens_map_inv = defaultdict(caster)
        meta_dict['bad_ids' + ngstr] = defaultdict(constant_factory(-1))
        meta_dict['bad_ids_inv' + ngstr] = defaultdict(caster)
        term_freq_dict = OrderedCounter()
        last_idx = 0
        expand = False
        for (i, (guid, doc_idx, tokens_list)) in enumerate(tokens_lists_by_guid):
            doc_dict = defaultdict(int)
            debug.print_dot(i, verbose)
            for sentence in tokens_list:
                for token in sentence:
                    doc_dict[unicode(caster(token))] += 1
                    if doc_dict[unicode(caster(token))] == 1:
                        term_idx = tokens_map[caster(token)]
                        if term_idx == -1:
                            tokens_map[caster(token)] = last_idx
                            tokens_map_inv[last_idx] = caster(token)
                            term_idx = last_idx
                            last_idx += 1
                        term_freq_dict[term_idx] += 1

            doc_store.update_fields(guid, {'term_freq' + ngstr: doc_dict})

        data_dict['term_freq' + ngstr] = np.array(term_freq_dict.values(), dtype=np.uint16)
        meta_dict['tokens_map' + ngstr] = tokens_map
        meta_dict['tokens_map_inv' + ngstr] = tokens_map_inv
        if len(term_freq_dict) != len(tokens_map):
            msg = 'term_freq & tokens_map not the same length (%d, %d)' % (
             len(term_freq_dict), len(tokens_map))
            debug.debug_here()
            raise errors.ProcessError(msg, process_text_logger)
        if len(tokens_map) != len(tokens_map_inv):
            msg = 'tokens_map & tokens_map_inv not the same length (%d, %d)' % (
             len(tokens_map), len(tokens_map_inv))
            debug.debug_here()
            raise errors.ProcessError(msg, process_text_logger)
        n_tokens = len(meta_dict[('tokens_map' + ngstr)])
        debug.print_verbose('%d unique dictionary items' % n_tokens, verbose, process_text_logger)


def tokens_to_hash(sentences):
    """
    Takes a list of tokens and returns a list of hash values
    """
    th_list = []
    for tokens in sentences:
        for token in tokens:
            if type(token) in [str, unicode, tuple]:
                th_list.append(hash(token))
            elif type(token) is list:
                th_list.append(hash(tuple(token)))
            else:
                raise TypeError('Unexpected type %s' % str(type(token)))

    return th_list


def filter_extremes(meta_dict, data_dict, time_dict, no_below=2, no_above=0.9, max_dict_size=100000, ngram=1, verbose=False):
    """
    Filter out tokens that appear in

    1. less than `no_below` documents (absolute number) or
    2. more than `no_above` documents (fraction of total corpus size, *not*
       absolute number).
    3. after (1) and (2), keep only the first `keep_n` most frequent tokens (or
       keep all if `None`).

    After the pruning, shrink resulting gaps in word ids.

    **Note**: Due to the gap shrinking, the same word may have a different
    word id before and after the call to this function!
    """
    n_docs = meta_dict['n_docs']
    no_above_abs = int(no_above * n_docs)
    fstr = '#below %d, #above %d' % (no_below, no_above_abs)
    ngstr = '_%d' % ngram
    caster = get_caster(ngram)
    with debug.Timer(fstr, time_dict, verbose, process_text_logger):
        term_freq = data_dict[('term_freq' + ngstr)].copy()
        tokens_map = meta_dict[('tokens_map' + ngstr)]
        tokens_map_inv = meta_dict[('tokens_map_inv' + ngstr)]
        good_ids = np.argwhere((term_freq <= no_above_abs) & (term_freq >= no_below)).ravel()
        if len(good_ids) > max_dict_size:
            tfi = np.argsort(term_freq[good_ids]).ravel()[::-1]
            good_ids = good_ids[tfi[0:max_dict_size]]
        bad_ids = set(tokens_map.values()).difference(good_ids)
        new_tokens_map = dict()
        new_tokens_map_inv = dict()
        meta_dict['bad_ids' + ngstr] = dict()
        meta_dict['bad_ids_inv' + ngstr] = dict()
        data_dict['term_freq' + ngstr] = np.zeros(len(good_ids), dtype=np.uint16)
        data_dict['term_freq_bad' + ngstr] = np.zeros(len(bad_ids), dtype=np.uint16)
        try:
            for (new, old) in enumerate(good_ids):
                new_tokens_map[tokens_map_inv[old]] = new
                new_tokens_map_inv[new] = tokens_map_inv[old]
                data_dict[('term_freq' + ngstr)][new] = term_freq[old]

            for (new, old) in enumerate(bad_ids):
                meta_dict[('bad_ids' + ngstr)][tokens_map_inv[old]] = new
                meta_dict[('bad_ids_inv' + ngstr)][new] = tokens_map_inv[old]
                data_dict[('term_freq_bad' + ngstr)][new] = term_freq[old]

        except Exception, e:
            raise e

        meta_dict['tokens_map' + ngstr] = new_tokens_map
        meta_dict['tokens_map_inv' + ngstr] = new_tokens_map_inv
        try:
            debug.print_verbose('Kept %d tokens (%.2f%%)' % (
             len(good_ids),
             float(len(good_ids)) / len(tokens_map) * 100), verbose)
        except Exception, e:
            pass

        if len(good_ids) == 0:
            debug.debug_here()
    return (
     good_ids, bad_ids)