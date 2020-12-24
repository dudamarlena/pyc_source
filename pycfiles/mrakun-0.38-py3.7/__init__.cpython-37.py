# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mrakun/__init__.py
# Compiled at: 2020-03-17 08:02:39
# Size of source mod 2**32: 16526 bytes
"""
RaKUn is an algorithm for graph-absed keyword extraction.
"""
import itertools, time, nltk, string
import nltk.corpus as stpw
from nltk import word_tokenize
from nltk.stem.porter import *
import operator
from collections import defaultdict, Counter
import networkx as nx, numpy as np, glob, editdistance, os, re, pandas
import nltk.corpus as wn
from tqdm import tqdm
import logging
logging.basicConfig(format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')
logging.getLogger().setLevel(logging.INFO)
try:
    from py3plex.visualization.multilayer import *
except Exception as es:
    try:
        print('Please install py3plex library (pip install py3plex) for visualization capabilities!')
    finally:
        es = None
        del es

class RakunDetector:

    def __init__(self, hyperparameters, verbose=True):
        self.distance_method = hyperparameters['distance_method']
        self.hyperparameters = hyperparameters
        if 'max_occurrence' not in self.hyperparameters:
            self.hyperparameters['max_occurrence'] = 3
        if 'max_similar' not in self.hyperparameters:
            self.hyperparameters['max_similar'] = 3
        if 'stopwords' not in self.hyperparameters:
            self.hyperparameters['stopwords'] = None
        self.verbose = verbose
        self.keyword_graph = None
        self.inverse_lemmatizer_mapping = {}
        if self.distance_method == 'fasttext':
            from gensim.models import fasttext
            self.pretrained_embedding_path = hyperparameters['pretrained_embedding_path']
            self.model = fasttext.load_facebook_vectors(self.pretrained_embedding_path)
        if self.verbose:
            logging.info('Initiated a keyword detector instance.')
        self.default_visualization_parameters = {'top_n':10,  'max_node_size':8,  'min_node_size':2,  'label_font_size':10,  'text_color':'red',  'num_layout_iterations':50,  'edge_width':0.08,  'alpha_channel':0.5}

    def visualize_network(self, visualization_parameters=None, display=True):
        if not visualization_parameters:
            visualization_parameters = self.default_visualization_parameters
        if self.verbose:
            logging.info(nx.info(self.keyword_graph))
        centrality = np.array([self.centrality[node] for node in self.keyword_graph.nodes()])
        top_10 = list(centrality.argsort()[-visualization_parameters['top_n']:][::-1])
        node_list = set((x for enx, x in enumerate(self.keyword_graph.nodes()) if enx in top_10))
        rgba = ['red' if enx in set(top_10) else 'black' for enx, x in enumerate(list(centrality))]
        labels = [x for x in self.keyword_graph.nodes() if x in node_list]
        node_sizes = [visualization_parameters['max_node_size'] if x in node_list else visualization_parameters['min_node_size'] for x in self.keyword_graph.nodes()]
        hairball_plot((self.keyword_graph), labels=labels,
          label_font_size=(visualization_parameters['label_font_size']),
          color_list=rgba,
          text_color=(visualization_parameters['text_color']),
          node_sizes=node_sizes,
          layout_parameters={'iterations': visualization_parameters['num_layout_iterations']},
          scale_by_size=True,
          edge_width=(visualization_parameters['edge_width']),
          alpha_channel=(visualization_parameters['alpha_channel']),
          layout_algorithm='force',
          legend=False)
        if display:
            plt.show()

    def corpus_graph(self, language_file, limit_range=3000000, verbose=False, lemmatizer=None, stopwords=None, min_char=4, stemmer=None, input_type='file'):
        G = nx.DiGraph()
        ctx = 0
        reps = False
        dictionary_with_counts_of_pairs = {}
        self.whole_document = []

        def process_line(line):
            nonlocal ctx
            nonlocal reps
            stop = list(string.punctuation)
            line = line.strip()
            line = [i for i in word_tokenize(line.lower()) if i not in stop]
            self.whole_document += line
            if stopwords is not None:
                line = [w for w in line if w not in stopwords]
            if stemmer is not None:
                line = [stemmer.stem(w) for w in line]
            if lemmatizer is not None:
                new_line = []
                for x in line:
                    lemma = lemmatizer.lemmatize(x)
                    if lemma not in self.inverse_lemmatizer_mapping:
                        self.inverse_lemmatizer_mapping[lemma] = set()
                    self.inverse_lemmatizer_mapping[lemma].add(x)
                    new_line.append(lemma)

                line = new_line
            line = [x for x in line if len(x) > min_char]
            if len(line) > 1:
                ctx += 1
                if ctx % 15000 == 0:
                    logging.info('Processed {} sentences.'.format(ctx))
                if ctx % limit_range == 0:
                    return True
                for enx, el in enumerate(line):
                    if enx > 0:
                        edge_directed = (
                         line[(enx - 1)], el)
                        if edge_directed[0] != edge_directed[1]:
                            G.add_edge(edge_directed[0], edge_directed[1])
                        else:
                            edge_directed = None
                    elif enx < len(line) - 1:
                        edge_directed = (
                         el, line[(enx + 1)])
                        if edge_directed[0] != edge_directed[1]:
                            G.add_edge(edge_directed[0], edge_directed[1])
                        else:
                            edge_directed = None
                    if edge_directed:
                        if edge_directed in dictionary_with_counts_of_pairs:
                            dictionary_with_counts_of_pairs[edge_directed] += 1
                            reps = True
                        else:
                            dictionary_with_counts_of_pairs[edge_directed] = 1

            return False

        if input_type == 'file':
            with open(language_file) as (lf):
                for line in lf:
                    breakBool = process_line(line)
                    if breakBool:
                        break

        else:
            if input_type == 'text':
                lines = language_file.split('\n')
                for line in lines:
                    breakBool = process_line(line)
                    if breakBool:
                        break

        for edge in G.edges(data=True):
            try:
                edge[2]['weight'] = dictionary_with_counts_of_pairs[(edge[0], edge[1])]
            except Exception as es:
                try:
                    raise es
                finally:
                    es = None
                    del es

        if verbose:
            print(nx.info(G))
        return (G, reps)

    def generate_hypervertices(self, G):
        """
        This node generates hypervertices.
        """
        for k, v in self.to_merge.items():
            for pair in v:
                n0 = pair[0]
                n1 = pair[1]
                pair_0_cent = self.centrality[n0]
                pair_1_cent = self.centrality[n1]
                if pair_0_cent >= pair_1_cent:
                    to_rewire_in = G.in_edges(n1, data=True)
                    to_rewire_out = G.out_edges(n1, data=True)
                    for neigh in to_rewire_in:
                        e1 = (
                         neigh[1], n0)
                        (G.add_edge)(*e1, **{'weight': neigh[2]['weight']})

                    for neigh in to_rewire_out:
                        e1 = (
                         n0, neigh[0])
                        (G.add_edge)(*e1, **{'weight': neigh[2]['weight']})

                    if n1 in G:
                        G.remove_node(n1)
                    else:
                        to_rewire_in = G.in_edges(n0, data=True)
                        to_rewire_out = G.out_edges(n0, data=True)
                        for neigh in to_rewire_in:
                            e1 = (
                             neigh[1], n1)
                            (G.add_edge)(*e1, **{'weight': neigh[2]['weight']})

                        for neigh in to_rewire_out:
                            e1 = (
                             n1, neigh[0])
                            (G.add_edge)(*e1, **{'weight': neigh[2]['weight']})

                        if n0 in G:
                            G.remove_node(n0)

    def hypervertex_prunning(self, graph, distance_threshold, pair_diff_max=2, distance_method='editdistance'):
        self.to_merge = defaultdict(list)
        for pair in itertools.combinations(graph.nodes(), 2):
            abs_diff = np.abs(len(pair[0]) - len(pair[1]))
            if abs_diff < pair_diff_max:
                if distance_method == 'editdistance':
                    ed = self.calculate_edit_distance(pair[0], pair[1])
                else:
                    if distance_method == 'fasttext':
                        ed = self.calculate_embedding_distance(pair[0], pair[1])
                if abs(ed) < distance_threshold:
                    self.to_merge[(abs_diff, ed)].append(pair)

        self.generate_hypervertices(graph)

    def find_keywords(self, document, input_type='file', validate=False):
        if validate == True:
            distance_method = 'editdistance'
        else:
            distance_method = self.distance_method
        limit_num_keywords = self.hyperparameters['num_keywords']
        if 'lemmatizer' in self.hyperparameters:
            lemmatizer = self.hyperparameters['lemmatizer']
        else:
            lemmatizer = None
        double_weight_threshold = self.hyperparameters['bigram_count_threshold']
        stopwords = self.hyperparameters['stopwords']
        num_tokens = self.hyperparameters['num_tokens']
        distance_threshold = self.hyperparameters['distance_threshold']
        pair_diff_length = self.hyperparameters['pair_diff_length']
        all_terms = set()
        klens = {}
        weighted_graph, reps = self.corpus_graph(document, lemmatizer=lemmatizer, stopwords=stopwords, input_type=input_type)
        nn = len(list(weighted_graph.nodes()))
        if distance_threshold > 0:
            self.centrality = nx.load_centrality(weighted_graph)
            self.hypervertex_prunning(weighted_graph, distance_threshold, pair_diff_max=pair_diff_length, distance_method=distance_method)
        nn2 = len(list(weighted_graph.nodes()))
        self.initial_tokens = nn
        self.pruned_tokens = nn2
        if self.verbose:
            logging.info('Number of nodes reduced from {} to {}'.format(nn, nn2))
        pgx = nx.load_centrality(weighted_graph)
        self.keyword_graph = weighted_graph
        self.centrality = pgx
        keywords_with_scores = sorted((pgx.items()), key=(operator.itemgetter(1)), reverse=True)
        kw_map = dict(keywords_with_scores)
        if not reps or 2 in num_tokens or 3 in num_tokens:
            higher_order_1 = []
            higher_order_2 = []
            frequent_pairs = []
            for edge in weighted_graph.edges(data=True):
                if edge[0] != edge[1] and 'weight' in edge[2] and edge[2]['weight'] > double_weight_threshold:
                    frequent_pairs.append(edge[0:2])

            for pair in frequent_pairs:
                w1 = pair[0]
                w2 = pair[1]
                if w1 in kw_map and w2 in kw_map:
                    score = np.mean([kw_map[w1], kw_map[w2]])
                    if w1 + ' ' + w2 not in all_terms:
                        higher_order_1.append((w1 + ' ' + w2, score))
                        all_terms.add(w1 + ' ' + w2)

            three_gram_candidates = []
            for pair in frequent_pairs:
                for edge in weighted_graph.in_edges(pair[0]):
                    if edge[0] in kw_map:
                        trip_score = [
                         kw_map[edge[0]], kw_map[pair[0]], kw_map[pair[1]]]
                        term = edge[0] + ' ' + pair[0] + ' ' + pair[1]
                        score = np.mean(trip_score)
                        if term not in all_terms:
                            higher_order_2.append((term, score))
                            all_terms.add(term)

                for edge in weighted_graph.out_edges(pair[1]):
                    if edge[1] in kw_map:
                        trip_score = [
                         kw_map[edge[1]], kw_map[pair[0]], kw_map[pair[1]]]
                        term = pair[0] + ' ' + pair[1] + ' ' + edge[1]
                        score = np.mean(trip_score)
                        if term not in all_terms:
                            higher_order_2.append((term, score))
                            all_terms.add(term)

        else:
            higher_order_1 = []
            higher_order_2 = []
        total_keywords = []
        if 1 in num_tokens:
            total_keywords += keywords_with_scores
        if 2 in num_tokens:
            total_keywords += higher_order_1
        if 3 in num_tokens:
            total_keywords += higher_order_2
        total_kws = sorted((set(total_keywords)), key=(operator.itemgetter(1)), reverse=True)
        tokensets = []
        for keyword in total_kws:
            ltx = keyword[0].split(' ')
            if len(ltx) > 1:
                tokensets += ltx

        penalty = set([x[0] for x in Counter(tokensets).most_common(self.hyperparameters['max_occurrence'])])
        tmp = []
        pnx = 0
        for keyword in total_kws:
            parts = set(keyword[0].split(' '))
            if len(penalty.intersection(parts)) > 0:
                pnx += 1
                if pnx < self.hyperparameters['max_similar']:
                    tmp.append(keyword)
            else:
                tmp.append(keyword)

        total_kws = tmp
        total_kws = total_kws[0:limit_num_keywords]
        return total_kws

    def calculate_edit_distance(self, key1, key2):
        return editdistance.eval(key1, key2)

    def calculate_embedding_distance(self, key1, key2):
        return self.model.wv.similarity(key1, key2)


if __name__ == '__main__':
    from nltk.corpus import stopwords
    hyperparameters = {'distance_threshold':4, 
     'distance_method':'editdistance', 
     'num_keywords':20, 
     'pair_diff_length':3, 
     'stopwords':stopwords.words('english'), 
     'bigram_count_threshold':2, 
     'max_occurrence':5, 
     'max_similar':3, 
     'num_tokens':[
      1, 2]}
    keyword_detector = RakunDetector(hyperparameters)
    example_data = '../datasets/wiki20/docsutf8/7183.txt'
    keywords = keyword_detector.find_keywords(example_data)
    print(keywords)