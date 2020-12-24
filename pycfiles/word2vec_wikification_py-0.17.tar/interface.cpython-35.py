# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/kensuke-mi/Desktop/analysis_work/wiki_node_disambiguation/word2vec_wikification_py/interface.py
# Compiled at: 2017-03-15 17:23:10
# Size of source mod 2**32: 5702 bytes
try:
    from gensim.models import KeyedVectors
    from gensim.models import Word2Vec
except ImportError:
    from gensim.models import Word2Vec

from word2vec_wikification_py.models import WikipediaArticleObject, LatticeObject, SequenceScore
from word2vec_wikification_py.make_lattice import make_lattice_object
from word2vec_wikification_py.load_entity_model import load_entity_model
from word2vec_wikification_py import search_wiki_pages
from typing import List, Any, Union
from functools import partial

def string_normalization_function(input_str: str) -> str:
    return input_str


def add_article_symbol(input_str: str) -> str:
    return '[{}]'.format(input_str)


def predict_japanese_wiki_names_with_wikidump(input_tokens, wikipedia_db_connector, entity_vector_model, is_use_cache=True,
                                              is_sort_object=True,
                                              page_table_name='page',
                                              page_table_redirect='redirect',
                                              search_method='complete') -> List[SequenceScore]:
    """* What you can do
    - You can run "Wikification" over your tokenized text

    * Params
    - input_tokens: list of tokens
    - wikipedia_db_connector: mysql connector into wikipedia-dump database
    - entity_vector_model: wikipedia entity vector of word2vec model
    - is_use_cache: a boolean flag for keeping huge-object on disk
    - is_sort_object: a boolean flag for sorting SequenceScore object
    - page_table_name: the name of "page" table of wikipedia-dump database
    - page_table_redirect: the name of "redirect" table of wikipedia-dump database
    - search_method: a way to find candidates of wikipedia article name.
        - partial: It tries to find wikipedia article name by concatenating tokens
        - complete: It trusts the result of tokenizer.
    """
    if search_method == 'partial':
        search_function = partial(search_wiki_pages.search_function_from_wikipedia_database, wikipedia_db_connector=wikipedia_db_connector, page_table_name=page_table_name, page_table_redirect=page_table_redirect)
        search_result = search_wiki_pages.search_from_dictionary(target_tokens=input_tokens, string_normalization_function=string_normalization_function, partially_param_given_function=search_function)
        seq_wiki_article_name = [WikipediaArticleObject(page_title=token_name, candidate_article_name=[add_article_symbol(string) for string in results]) for token_name, results in search_result.items() if not results == []]
        return compute_wiki_node_probability(seq_wiki_article_name=seq_wiki_article_name, entity_vector_model=entity_vector_model, is_use_cache=is_use_cache, is_sort_object=is_sort_object)
    if search_method == 'complete':
        search_result = [search_wiki_pages.search_function_from_wikipedia_database(token=token, wikipedia_db_connector=wikipedia_db_connector, page_table_name=page_table_name, page_table_redirect=page_table_redirect) for token in input_tokens]
        seq_wiki_article_name = [WikipediaArticleObject(page_title=token, candidate_article_name=[add_article_symbol(string) for string in results]) for token, results in zip(input_tokens, search_result) if not results == []]
        return compute_wiki_node_probability(seq_wiki_article_name=seq_wiki_article_name, entity_vector_model=entity_vector_model, is_use_cache=is_use_cache, is_sort_object=is_sort_object)
    raise Exception('There is no search method named {}'.format(search_method))


def compute_wiki_node_probability(seq_wiki_article_name, entity_vector_model, is_use_cache=True, is_sort_object=True):
    """* What you can do
    - You can get sequence of wikipedia-article-names with its sequence-score

    * Params
    - is_use_cache: a boolean flag for keeping huge-object on disk
    - is_sort_object: a boolean flag for sorting SequenceScore object

    * Caution
    - You must proper wikipedia-article-name on WikipediaArticleObject.candidate_article_name attribute
    """
    lattice_object = make_lattice_object(seq_wiki_article_name=seq_wiki_article_name, entity_vector_model=entity_vector_model, is_use_cache=is_use_cache)
    sequence_score_objects = lattice_object.get_score_routes()
    if is_sort_object:
        sequence_score_objects.sort(key=lambda obj: obj.sequence_score, reverse=True)
    return sequence_score_objects