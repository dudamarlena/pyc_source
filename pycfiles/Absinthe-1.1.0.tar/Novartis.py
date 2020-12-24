# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/TAMO/DataSources/Novartis.py
# Compiled at: 2019-04-23 02:08:32
__doc__ = '\nNovartis.py\n\nLoads Novartis mapping Data and Dataset as a HT.Dataset object\n\nid2feature(id)\nid2other(id,other), where "other" can be \n\nCopyright (2005) Whitehead Institute for Biomedical Research (except as noted below)\nAll Rights Reserved\n\nAuthor: David Benjamin Gordon\n\n'
from gzip import GzipFile
from TAMO.HT import Dataset
import TAMO.paths
ANNOFILE = TAMO.paths.Novartisdir + 'gnf1h-anntable.txt.gz'
DATAFILE = TAMO.paths.Novartisdir + 'U133A+GNF1B_101402.AD.txt'
ANNO = {}
REVANNO = {}
ref = {'feature': 2, 'name': 1, 
   'location': 4, 
   'desc': 10, 
   'func': 11, 
   'refseq': 5, 
   'locuslink': 5, 
   'uniprot': 7, 
   'unigene': 6, 
   'ensenbl': 8, 
   'family': 12}

def load_anno():
    if ANNO:
        return
    TAMO.paths.CHECK(ANNOFILE, 'Novartis')
    F = GzipFile(ANNOFILE)
    lines = F.readlines()
    F.close()
    for line in lines:
        toks = line.strip().split('\t')
        if len(toks) < 15:
            continue
        D = {}
        for id, pos in ref.items():
            id = id.lower()
            if pos != 0:
                REVANNO[toks[pos]] = toks[0]
            D[id] = toks[pos]
            ANNO[toks[0]] = D


def id2feature(id):
    load_anno()
    if REVANNO.has_key(id):
        return REVANNO[id]
    else:
        return ''


def id2other(id, other):
    other = other.lower()
    feature = id2feature(id)
    if not feature:
        return ''
    if not ANNO[feature].has_key(other):
        return ''
    return ANNO[feature][other]


def humandata():
    TAMO.paths.CHECK(DATAFILE, 'Novartis')
    G = Dataset(DATAFILE)


def id2unigene(id):
    return id2other(id, 'unigene')


def id2locuslink(id):
    return id2other(id, 'locuslink')


def id2ll(id):
    return id2locuslink(id)


def id2uniprot(id):
    return id2other(id, 'uniprot')