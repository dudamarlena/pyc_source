# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/kensuke-mi/Desktop/analysis_work/wiki_node_disambiguation/word2vec_wikification_py/models.py
# Compiled at: 2017-02-14 02:48:20
# Size of source mod 2**32: 13587 bytes
from typing import List, Tuple, Any, Union, Dict
from numpy.core import ndarray
from scipy.sparse import csr_matrix
from itertools import product
import pickle, json, csv, os, shutil, copy, itertools

class PersistentDict(dict):
    __doc__ = " Persistent dictionary with an API compatible with shelve and anydbm.\n    The dict is kept in memory, so the dictionary operations run as fast as\n    a regular dictionary.\n    Write to disk is delayed until close or sync (similar to gdbm's fast mode).\n    Input file format is automatically discovered.\n    Output file format is selectable between pickle, json, and csv.\n    All three serialization formats are backed by fast C implementations.\n    "

    def __init__(self, filename, flag='c', mode=None, format='pickle', *args, **kwds):
        self.flag = flag
        self.mode = mode
        self.format = format
        self.filename = filename
        if flag != 'n' and os.access(filename, os.R_OK):
            fileobj = open(filename, 'rb' if format == 'pickle' else 'r')
            with fileobj:
                self.load(fileobj)
        dict.__init__(self, *args, **kwds)

    def sync(self):
        """Write dict to disk"""
        if self.flag == 'r':
            return
        filename = self.filename
        tempname = filename + '.tmp'
        fileobj = open(tempname, 'wb' if self.format == 'pickle' else 'w')
        try:
            try:
                self.dump(fileobj)
            except Exception:
                os.remove(tempname)
                raise

        finally:
            fileobj.close()

        shutil.move(tempname, self.filename)
        if self.mode is not None:
            os.chmod(self.filename, self.mode)

    def close(self):
        self.sync()

    def __enter__(self):
        return self

    def __exit__(self, *exc_info):
        self.close()

    def dump(self, fileobj):
        if self.format == 'csv':
            csv.writer(fileobj).writerows(self.items())
        else:
            if self.format == 'json':
                json.dump(self, fileobj, separators=(',', ':'))
            else:
                if self.format == 'pickle':
                    pickle.dump(dict(self), fileobj, 2)
                else:
                    raise NotImplementedError('Unknown format: ' + repr(self.format))

    def load(self, fileobj):
        for loader in (pickle.load, json.load, csv.reader):
            fileobj.seek(0)
            try:
                return self.update(loader(fileobj))
            except Exception:
                pass


class WikipediaArticleObject(object):
    __doc__ = 'Wikipediaの記事情報を記述するためのクラス\n    '
    __slots__ = ['page_title', 'candidate_article_name', 'article_name']

    def __init__(self, page_title: str, candidate_article_name: List[str], article_name: str=None):
        self.page_title = page_title
        self.candidate_article_name = candidate_article_name
        self.article_name = article_name

    def __str__(self) -> str:
        return self.page_title

    def __dict__(self) -> Dict[(str, Any)]:
        return {'page_title': self.page_title, 
         'candidate_article_name': self.candidate_article_name, 
         'article_name': self.article_name}

    @classmethod
    def from_dict(cls, dict_object: Dict[(str, Any)]):
        if 'article_name' in dict_object:
            article_name = dict_object['article_name']
        else:
            article_name = None
        return WikipediaArticleObject(page_title=dict_object['page_title'], candidate_article_name=dict_object['candidate_article_name'], article_name=article_name)


class SequenceScore(object):
    __doc__ = '計算された記事系列のスコアを保持するオブジェクト\n\n    '

    def __init__(self, seq_words: List[WikipediaArticleObject], seq_transition_score: List[Tuple[(str, str, float)]], sequence_score: float):
        self.seq_words = seq_words
        self.seq_transition_score = seq_transition_score
        self.sequence_score = sequence_score

    def __dict__(self):
        return {'seq_words': [wikipedia_obj.__dict__() for wikipedia_obj in self.seq_words], 
         'seq_transition_score': self.seq_transition_score, 
         'sequence_score': self.sequence_score}

    def __str__(self):
        return 'SequenceScore object with score={}'.format(self.sequence_score)

    def _SequenceScore__generate_label_sequence(self, seq_score_tuple: List[Tuple[(str, str, float)]]) -> List[str]:
        """* What you can do
        - You generate list of label
        """
        seq_label = []
        for index in range(0, len(seq_score_tuple)):
            if index == 0:
                seq_label.append(seq_score_tuple[index][0])
            else:
                if index + 1 == len(seq_score_tuple):
                    seq_label.append(seq_score_tuple[index][0])
                    seq_label.append(seq_score_tuple[index][1])
                else:
                    seq_label.append(seq_score_tuple[index][0])

        return seq_label

    def get_tokens(self) -> List[str]:
        return self._SequenceScore__generate_label_sequence(seq_score_tuple=self.seq_transition_score)

    @classmethod
    def from_dict(cls, dict_object: Dict[(str, Any)]):
        seq_words = [WikipediaArticleObject.from_dict(wikipedia_dict_obj) for wikipedia_dict_obj in dict_object['seq_words']]
        return SequenceScore(seq_words=seq_words, seq_transition_score=dict_object['seq_transition_score'], sequence_score=dict_object['sequence_score'])


class EdgeObject(object):
    __slots__ = [
     'index_at_t', 'index_at_t_plus']

    def __init__(self, index_at_t: int, index_at_t_plus: int):
        self.index_at_t = index_at_t
        self.index_at_t_plus = index_at_t_plus

    def to_tuple(self):
        return (
         self.index_at_t, self.index_at_t_plus)


class IndexDictionaryObject(object):
    __doc__ = 'Class object for keeping a relation of state_name and index.\n    state2index attribute must have 2 key names.\n    - row2index\n    - column2index\n\n    index2state attribute must have 2 key names.\n    - index2row\n    - index2column\n\n    '
    __slots__ = ['state2index', 'index2state']

    def __init__(self, state2index: Union[(Dict[(str, Dict)], PersistentDict)], index2state: Union[(Dict[(str, Dict)], PersistentDict)]):
        self.state2index = state2index
        self.index2state = index2state


class LatticeObject(object):

    def __init__(self, transition_matrix: Union[(csr_matrix, ndarray)], index_dictionary_obj: IndexDictionaryObject, seq_edge_groups: List[List[EdgeObject]], seq_wiki_article_name: List[WikipediaArticleObject]=None):
        """*
        """
        self.transition_matrix = transition_matrix
        self.index_dictionary_obj = index_dictionary_obj
        self.seq_edge_groups = seq_edge_groups
        self.index_tuple_route = self._LatticeObject__generate_edge_routes()
        self.seq_wiki_article_name = seq_wiki_article_name
        if seq_wiki_article_name is not None:
            function_key = lambda tuple_wikilabel_wikiobj: tuple_wikilabel_wikiobj[0]
            seq_tuple_wikilabel_wikiobj = [(wiki_article_name, wiki_obj_index, wiki_article_obj) for wiki_obj_index, wiki_article_obj in enumerate(self.seq_wiki_article_name) for wiki_article_name in wiki_article_obj.candidate_article_name]
            self.label2WikiArticleObj = {}
            for wiki_label_name, g_obj in itertools.groupby(sorted(seq_tuple_wikilabel_wikiobj, key=function_key), key=function_key):
                self.label2WikiArticleObj[wiki_label_name] = [(tuple_wikilabel_wiki_obj[1], tuple_wikilabel_wiki_obj[2]) for tuple_wikilabel_wiki_obj in g_obj]

        else:
            self.label2WikiArticleObj = None

    def _LatticeObject__generate_edge_routes--- This code section failed: ---

 L. 234         0  LOAD_GLOBAL              Tuple
                3  LOAD_GLOBAL              Tuple
                6  LOAD_GLOBAL              int
                9  LOAD_GLOBAL              int
               12  BUILD_TUPLE_2         2 
               15  BINARY_SUBSCR    
               16  BINARY_SUBSCR    
               17  LOAD_GLOBAL              bool
               20  LOAD_CONST               ('index_tuple_route', 'return')
               23  LOAD_CLOSURE             'self'
               26  BUILD_TUPLE_1         1 
               29  LOAD_CODE                <code_object judge_proper_route>
               32  LOAD_STR                 'LatticeObject.__generate_edge_routes.<locals>.judge_proper_route'
               35  MAKE_CLOSURE_A_3_0        '0 positional, 0 keyword only, 3 annotated'
               41  STORE_FAST               'judge_proper_route'

 L. 248        44  LOAD_LISTCOMP            '<code_object <listcomp>>'
               47  LOAD_STR                 'LatticeObject.__generate_edge_routes.<locals>.<listcomp>'
               50  MAKE_FUNCTION_0          '0 positional, 0 keyword only, 0 annotated'

 L. 249        53  LOAD_DEREF               'self'
               56  LOAD_ATTR                seq_edge_groups
               59  GET_ITER         
               60  CALL_FUNCTION_1       1  '1 positional, 0 named'
               63  STORE_FAST               'index_tuple_of_edge'

 L. 250        66  LOAD_GLOBAL              product
               69  LOAD_FAST                'index_tuple_of_edge'
               72  CALL_FUNCTION_VAR_0     0  '0 positional, 0 named'
               75  STORE_FAST               'index_tuple_of_route_candidates'

 L. 252        78  LOAD_GLOBAL              list
               81  LOAD_GLOBAL              filter
               84  LOAD_FAST                'judge_proper_route'
               87  LOAD_FAST                'index_tuple_of_route_candidates'
               90  CALL_FUNCTION_2       2  '2 positional, 0 named'
               93  CALL_FUNCTION_1       1  '1 positional, 0 named'
               96  STORE_FAST               'index_tuple_of_route'

 L. 253        99  LOAD_FAST                'index_tuple_of_route'
              102  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    def _LatticeObject__get_score(self, row: int, column: int) -> float:
        return self.transition_matrix[(row, column)]

    def _LatticeObject__compute_route_score(self, index_tuple_route: Tuple[Tuple[(int, int)]]) -> float:
        """* What you can do
        - You get score of a route
        """
        seq_score = [self._LatticeObject__get_score(index_tuple[0], index_tuple[1]) for index_tuple in index_tuple_route]
        return sum(seq_score)

    def _LatticeObject__generate_state_name_sequence(self, index_tuple_route: Tuple[Tuple[(int, int)]]) -> List[Tuple[(str, str, float)]]:
        """* What you can do
        - You get sequence of label & score tuple (label_t, label_t_plus_1, score)
        """
        seq_state_name_score = [(self.index_dictionary_obj.index2state['index2row'][index_tuple[0]][1], self.index_dictionary_obj.index2state['index2column'][index_tuple[1]][1], self._LatticeObject__get_score(index_tuple[0], index_tuple[1])) for index_tuple in index_tuple_route]
        return seq_state_name_score

    def _LatticeObject__generate_label_sequence(self, seq_score_tuple: List[Tuple[(str, str, float)]]) -> List[str]:
        """* What you can do
        - You generate list of label
        """
        seq_label = []
        for index in range(0, len(seq_score_tuple)):
            if index == 0:
                seq_label.append(seq_score_tuple[index][0])
            else:
                if index + 1 == len(seq_score_tuple):
                    seq_label.append(seq_score_tuple[index][0])
                    seq_label.append(seq_score_tuple[index][1])
                else:
                    seq_label.append(seq_score_tuple[index][0])

        return seq_label

    def _LatticeObject__generate_wiki_article_object_sequence(self, seq_label_name: List[str]) -> List[WikipediaArticleObject]:
        """* What you can do
        - You generate list of WikipediaArticleObject. They are already disambiguated.
        """
        seq_wiki_article_obj = [
         None] * len(seq_label_name)
        for l_index, label in enumerate(seq_label_name):
            seq_tuple_index_wikiobj = copy.deepcopy(self.label2WikiArticleObj[label])
            wiki_article_obj_in_index = [tuple_index_wikiobj for tuple_index_wikiobj in seq_tuple_index_wikiobj if tuple_index_wikiobj[0] == l_index][0][1]
            wiki_article_obj_in_index.article_name = label
            seq_wiki_article_obj[l_index] = wiki_article_obj_in_index

        return list(filter(lambda element: True if element is not None else False, seq_wiki_article_obj))

    def get_score_routes(self) -> List[SequenceScore]:
        """* What you can do
        - You generate list of SequenceScore.
            - Each SequenceScore has information of one-route and its score.
        """
        sequence_score_objects = [
         None] * len(self.index_tuple_route)
        for l_index, route in enumerate(self.index_tuple_route):
            route_score = self._LatticeObject__compute_route_score(route)
            seq_score_tuple = self._LatticeObject__generate_state_name_sequence(route)
            seq_label_name = self._LatticeObject__generate_label_sequence(seq_score_tuple=seq_score_tuple)
            if self.seq_wiki_article_name is not None:
                label_object = self._LatticeObject__generate_wiki_article_object_sequence(seq_label_name)
            else:
                label_object = seq_label_name
            sequence_score_objects[l_index] = SequenceScore(seq_words=label_object, seq_transition_score=seq_score_tuple, sequence_score=route_score)

        seq_result_score_object = list(filter(lambda element_obj: True if element_obj is not None else False, sequence_score_objects))
        return seq_result_score_object