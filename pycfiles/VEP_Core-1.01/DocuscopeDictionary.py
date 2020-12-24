# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\LocalUsers\ealexand\VEP_Core\Ity\Taggers\DocuscopeTagger\DocuscopeDictionary.py
# Compiled at: 2013-12-05 14:02:30
__author__ = 'kohlmann'
import re, string
from collections import OrderedDict
from os.path import isdir

def getLatFileList(dictionaryDirectory):
    """
    Read in the Lats - return them as a dictionary so we can look them up
    easily and get their info.
    Because we lose the order, we keep the lat index as part of what
    goes into the dictionary
    the triple is ID,Cluster,Dimension
    """
    lats = OrderedDict()
    clusts = OrderedDict()
    dims = OrderedDict()
    count = 0
    clust = ''
    dim = ''
    with openAny(dictionaryDirectory, ['_tones.txt', 'tones.txt']) as (f):
        for r in f:
            l = r.split()
            if len(l) > 1:
                if l[0] == 'CLUSTER:':
                    clust = l[1]
                    clusts[l[1]] = []
                elif l[0] == 'DIMENSION:':
                    dim = l[1]
                    dims[l[1]] = []
                    if clust != '':
                        clusts[clust].append(dim)
                elif l[0] == 'LAT:' or l[0] == 'CLASS:':
                    lats[l[1]] = (
                     count, clust, dim, l[1:])
                    if dim != '':
                        dims[dim].append(l[1])
                    count = count + 1

    return (
     lats, dims, clusts)


class DocuscopeDictionary:

    def __init__(self, dictname='default', debug=False):
        self.directory = findDict(dictname)
        self.debug = debug
        self.ruleCount = 0
        self.rules = dict()
        self.shortRules = dict()
        self.words = dict()
        self.lats, self.dims, self.clusts = getLatFileList(self.directory)
        with openAny(self.directory, ['_wordclasses.txt', 'wordclasses.txt']) as (f):
            curClass = 'NONE'
            for r in f:
                l = r.split()
                if len(l) == 1:
                    wl = l[0].lower()
                    if wl not in self.words:
                        self.words[wl] = [
                         wl]
                    self.words[wl].append(curClass)
                elif len(l) == 2:
                    curClass = '!' + l[1].upper()

        for lat in self.lats:
            for latfs in self.lats[lat][3]:
                for suffix in ['', '_p']:
                    try:
                        with open(makePath(self.directory, latfs + suffix + '.txt')) as (f):
                            for r in f:
                                li = re.findall("[!?\\w'-]+|[" + string.punctuation + ']', r)
                                l = map(lambda x: x.upper() if x[0] == '!' else x.lower(), li)
                                ll = len(l)
                                if ll > 0:
                                    self.ruleCount += 1
                                    for w in l:
                                        if w not in self.words:
                                            self.words[w] = [
                                             w]

                                    if len(l) > 1:
                                        if l[0] not in self.rules:
                                            self.rules[l[0]] = dict()
                                        if l[1] not in self.rules[l[0]]:
                                            self.rules[l[0]][l[1]] = []
                                        self.rules[l[0]][l[1]].append((lat, tuple(l)))
                                    else:
                                        self.shortRules[l[0]] = lat

                    except IOError:
                        pass

    def getRule(self, word):
        """get the rule associated with a word - returns nothing if there aren't any"""
        try:
            return self.rules[word]
        except KeyError:
            return []

    def getWord(self, word):
        if word in self.words:
            return self.words[word]
        else:
            return
            return

    def syns(self, word):
        try:
            return self.words[word]
        except KeyError:
            return [
             word]


dictionarySearchPath = [
 '..', '../Docuscope', '.']

def findDict(dictname='default'):
    if isdir(dictname):
        return dictname
    for d in dictionarySearchPath:
        if isdir(makePath(d, dictname)):
            return makePath(d, dictname)

    raise IOError(999, "Can't find Dictionary " + dictname)


def makePath(dir, file):
    if dir[(-1)] == '/' or dir[(-1)] == '\\':
        return dir + file
    else:
        return dir + '/' + file


def openAny(dir, fnames):
    """try a bunch of file names until you find one that exists"""
    for f in fnames:
        try:
            return open(makePath(dir, f), 'r')
        except IOError:
            pass

    raise IOError


def getDict(dictn='default', force=False):
    """get the DocuscopeDictionary - if it hasn't been read, read it in"""
    global theDocuscopeDictionary
    if force or 'theDocuscopeDictionary' not in globals():
        theDocuscopeDictionary = DocuscopeDictionary(dictn)
    return theDocuscopeDictionary