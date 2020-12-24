# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sam/Documents/fall17/mathviz/mathviz_hopper/src/helpers.py
# Compiled at: 2017-11-28 23:03:57
import os, sys, socket

def get_cur_path():
    return os.path.dirname(os.path.abspath(__file__))


def insert(st, trie):
    i = 0
    for s in st:
        if s not in trie.keys():
            trie[s] = {}
        if i == 20:
            break
        trie = trie[s]
        i += 1

    if i == 20:
        trie[st[i:]] = {}
        trie = trie[st[i:]]
    trie['full_word'] = 1


def construct_trie(list_of_str):
    trie = {}
    for st in list_of_str:
        insert(st, trie)

    return trie


def find_free_port():
    s = socket.socket()
    s.bind(('', 0))
    return s.getsockname()[1]