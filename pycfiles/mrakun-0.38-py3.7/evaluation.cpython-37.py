# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mrakun/evaluation.py
# Compiled at: 2019-11-06 08:13:40
# Size of source mod 2**32: 3640 bytes
import editdistance
from nltk.stem.porter import *
import numpy as np
from nltk.stem.porter import *

def compare_with_gold_fuzzy(detected_keywords, gold_standard_keywords, fuzzy_threshold=3, keyword_separator=';'):
    """
    Fuzzy comparison of keyword matches. Given a fuzzy edit distance threshold, how many  keywords out of the top 10 are OK?
    input: detected_keywords (list of string).
    input: gold_standard_keywords (list of strings).
    input: fuzzy_threshold (int) -> max acceptable edit distance.    
    """
    precision_correct = 0
    precision_overall = 0
    recall_correct = 0
    recall_overall = 0
    for enx, keyword_set in enumerate(detected_keywords):
        gold_standard_set = gold_standard_keywords[enx]
        count = 0
        method_keywords = keyword_set.split(keyword_separator)
        if type(gold_standard_set) is float:
            continue
        gold_standard_set = set(gold_standard_set.split(keyword_separator))
        top_n = len(gold_standard_set)
        if top_n >= len(method_keywords):
            top_n = len(method_keywords)
        parsed_rec = set()
        for el in method_keywords:
            if el not in parsed_rec:
                parsed_rec.add(el)
                if el in gold_standard_set:
                    recall_correct += 1

        recall_overall += top_n
        parsed_prec = set()
        for el in method_keywords:
            if el not in parsed_prec:
                parsed_prec.add(el)
                if el in gold_standard_set:
                    precision_correct += 1

        precision_overall += len(method_keywords)

    precision = float(precision_correct) / precision_overall
    recall = float(recall_correct) / recall_overall
    if precision + recall > 0:
        F1 = 2 * (precision * recall) / (precision + recall)
    else:
        F1 = 0
    return (precision, recall, F1)


def compare_gold_exact(detected_keywords, gold_standard_keywords):
    stemmer = PorterStemmer()
    tp_fp_all = []
    tp_fn_all = []
    tp = []
    for enx, keyword_set in enumerate(detected_keywords):
        gold_standard_set = gold_standard_keywords[enx]
        method_keywords = list(set(keyword_set))[:10]
        gold_standard_set = list(set(gold_standard_set))
        stem_preds = []
        stem_true = []
        for kw in method_keywords:
            kw = ' '.join([stemmer.stem(word) for word in kw.split()])
            stem_preds.append(kw)

        for kw in gold_standard_set:
            kw = ' '.join([stemmer.stem(word) for word in kw.split()])
            stem_true.append(kw)

        correct = 0
        for el in stem_preds:
            if el.lower() in stem_true:
                correct += 1

        tp_fn = float(len(gold_standard_set))
        tp_fp = float(len(method_keywords))
        tp_fn_all.append(tp_fn)
        tp_fp_all.append(tp_fp)
        tp.append(correct)

    precision = sum(tp) / sum(tp_fp_all)
    recall = sum(tp) / sum(tp_fn_all)
    try:
        F1 = 2 * (precision * recall) / (precision + recall)
    except:
        F1 = 0

    return (
     precision, recall, F1)