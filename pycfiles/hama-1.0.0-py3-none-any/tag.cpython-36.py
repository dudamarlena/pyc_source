# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/seongminnpark/hama-py/src/hama/tag.py
# Compiled at: 2020-03-20 00:34:39
# Size of source mod 2**32: 3442 bytes
import pandas as pd
from hama.listutil import insert, cartesian_product
data = pd.read_csv('pos22.csv')

def tag(text):
    """Produces POS tags for each morpheme in a text.

    Args:
        text (str): Text to separate into morphemes and tag.

    Returns:
        list: list containing tuples in the form of:
        (morpheme, tag).
    """
    tags = []
    words = text.split()
    for word in words:
        word_tags = tag_word(word)
        tags.extend(word_tags)

    return tags


def tag_word(word):
    """Produces POS tags for each morpheme in a single word.

    Args:
        word (str): Word to separate into morphemes and tag.

    Returns:
        list: List containing tuples in the form of:
        (morpheme, tag).
    """
    candidate_ms = candidate_morpheme_seqs(word)
    best_ms = [word]
    best_ts = ['u']
    best_score = 0
    for cms in candidate_ms:
        ct = candidate_tags(cms)
        tag_seqs = cartesian_product(*ct)
        for ts in tag_seqs:
            s = score_tag_seq(ts)
            if s > best_score:
                best_ms = cms
                best_ts = ts
                best_score = s

    return zip(best_ms, best_ts)


def candidate_morpheme_seqs(word):
    """Produces every possible partition of word 
    into candidate morphemes.

    Args:
        word (string): String to partition into morphemes.

    Returns:
        list: Returns a 2-D array of strings.
        For example, 메롱is partitioned into [[메롱], [메,롱]].
    """
    partitions = []
    if len(word) <= 0:
        return [[]]
    else:
        if len(word) <= 1:
            return [
             [
              word]]
        head = word[0]
        tail_partitions = candidate_morpheme_seqs(word[1:])
        for partition in tail_partitions:
            partitions.append(insert(partition[1:], 0, head + partition[0]))
            partitions.append(insert(partition, 0, head))

        return partitions


def score_tag_seq(ts):
    """Produces a likeliness score for an ordered tag sequence.

    Args:
        ts (list): Tag sequence to score.

    Returns:
        float: Tag sequence likeliness score.
    """
    return 1.0


def candidate_tags(ms):
    """Produces a list of possible tags for each morpheme 
    in a word partition.

    Args:
        ms (list): Morphemem sequence. 
        List of strings, each representing a morpheme.
        Example input value: ['아버지', '가'],

    Returns:
        list: Returns a 2-D list of tags. 
        Length of input and output arrays is the same.
        Example return value: [[nnc], [nc, jc]]
    """
    tags = []
    for m in ms:
        m_tags = query_dict(m)
        if len(m_tags) > 0:
            tags.append(m_tags)
        else:
            tags.append(['u'])

    assert len(ms) == len(tags)
    return tags


def query_dict(morpheme):
    """Queries embedded dictionary for morpheme.

    Args:
        morpheme (str): Morpheme to search for.

    Returns:
        list: List containing all found tags in the 
        embedded dictionary.
        empty if not found.
    """
    tags = []
    entries = data.loc[data.term.isin([morpheme])]
    if len(entries) > 0:
        for row in entries.itertuples():
            tags.append(row.tag)

    return tags