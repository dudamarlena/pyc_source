# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/kensuke-mi/Desktop/analysis_work/wiki_node_disambiguation/wiki_node_disambiguation/search_wiki_pages.py
# Compiled at: 2016-12-02 10:24:37
# Size of source mod 2**32: 4290 bytes
from typing import List, Any, Dict
from pymysql import Connection, cursors
from typing import Tuple

def __generate_window_size(target_token: List[str]) -> List[int]:
    return [i for i in range(1, len(target_token) + 1)]


def __generate_index_range(list_index: List[int], window_size: int) -> List[List[int]]:
    """generate set of list, which describes range-index of candidate tokens
    """
    search_index = []
    for start_i in range(0, len(list_index)):
        end_i = start_i + window_size
        if end_i <= len(list_index):
            search_index.append(list(range(start_i, end_i)))

    return search_index


def search_function_from_wikipedia_database(token: str, wikipedia_db_connector: Connection, page_table_name: str='page',
                                            page_table_redirect: str='redirect') -> List[str]:
    """*
    部分文字検索をするときに使う
    """

    def decode_string(string):
        try:
            unicode_string = string.decode('utf-8')
            return unicode_string
        except:
            return

    cursor = wikipedia_db_connector.cursor()
    page_query = 'SELECT page_id, page_title, page_is_redirect FROM {} WHERE (page_title = %s OR page_title LIKE %s) AND page_namespace = 0'.format(page_table_name)
    cursor.execute(page_query, (token, '{}\\_(%)'.format(token)))
    fetched_records = list(cursor.fetchall())
    page_names = [page_id_title[1] for page_id_title in fetched_records if page_id_title[2] == 0]
    redirect_names = [page_id_title[0] for page_id_title in fetched_records if page_id_title[2] == 1]
    cursor.close()
    if not redirect_names == []:
        cursor = wikipedia_db_connector.cursor()
        select_query = 'SELECT rd_title FROM {} WHERE rd_from IN %s'.format(page_table_redirect)
        cursor.execute(select_query, (redirect_names,))
        article_page_names = [page_id_title[0] for page_id_title in cursor.fetchall()]
        cursor.close()
    else:
        article_page_names = []
    article_name_string = list(set([decode_string(article_name) for article_name in page_names + article_page_names if decode_string(article_name) is not None]))
    return article_name_string


def search_from_dictionary(target_tokens: List[str], string_normalization_function, partially_param_given_function) -> Dict[(str, Any)]:
    """*
    """
    list_window_size = __generate_window_size(target_tokens)
    found_index = []
    found_token_tuple_object = {}
    all_index = [i for i in range(0, len(target_tokens))]
    for w_size in list_window_size[::-1]:
        list_index = list(range(0, len(target_tokens)))
        candidate_index_list = __generate_index_range(list_index, window_size=w_size)
        for candidate_indices in candidate_index_list:
            if len(set(candidate_indices).intersection(set(found_index))) >= 1:
                pass
            else:
                start_index = candidate_indices[0]
                end_index = candidate_indices[(-1)] + 1
                search_token = ''.join(target_tokens[start_index:end_index])
                normalized_search_token = string_normalization_function(search_token)
                search_result = partially_param_given_function(normalized_search_token)
                if len(search_result) > 0:
                    found_token_tuple_object.update({normalized_search_token: search_result})
                    if all_index[(-1)] in candidate_indices:
                        found_index += candidate_indices
                    else:
                        if len(candidate_indices) == 1:
                            found_index += candidate_indices
                        else:
                            found_index += candidate_indices

        if set(found_index) == set(all_index):
            break

    return found_token_tuple_object


def complete_search():
    pass