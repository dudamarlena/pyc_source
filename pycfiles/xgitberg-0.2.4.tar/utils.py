# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: gitenberg/metadata/utils.py
# Compiled at: 2016-03-08 12:03:43
marc_rels = {'aut': 'author', 'adp': 'adapter', 
   'aft': 'author_of_afterword', 
   'ann': 'annotator', 
   'arr': 'arranger', 
   'art': 'artist', 
   'aui': 'author_of_introduction', 
   'clb': 'collaborator', 
   'cmm': 'commentator', 
   'cmp': 'composer', 
   'cnd': 'conductor', 
   'com': 'compiler', 
   'ctb': 'contributor', 
   'dub': 'dubious_author', 
   'edt': 'editor', 
   'egr': 'engineer', 
   'ill': 'illustrator', 
   'lbt': 'librettist', 
   'oth': 'other_contributor', 
   'pbl': 'publisher_contributor', 
   'pht': 'photographer', 
   'prf': 'performer', 
   'prt': 'printer', 
   'res': 'researcher', 
   'trc': 'transcriber', 
   'trl': 'translator', 
   'unk': 'unknown_contributor'}
inverse_marc_rels = {v:k for k, v in marc_rels.items()}

def plural(key):
    if key.endswith('s'):
        return key + 'es'
    else:
        return key + 's'


def reverse_name(name):
    tokens = name.split(' ')
    if len(tokens) > 1:
        return tokens[(-1)] + ', ' + (' ').join(tokens[0:-1])