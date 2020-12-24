# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ryan/DH/prosodic/lib/Corpus.py
# Compiled at: 2019-06-07 00:03:27
import glob, os
from entity import entity, being
from tools import *
from Text import Text

class Corpus(entity):

    def __init__(self, corpusRoot, lang=None, printout=None, corpusFiles='*.txt', phrasebreak=',;:.?!()[]{}<>', limWord=None):
        import prosodic
        if not lang:
            self.lang = prosodic.config['lang'] if 1 else lang
            self.dict = prosodic.dict[self.lang]
            self.parent = False
            self.children = []
            self.feats = {}
            self.featpaths = {}
            self.finished = False
            self.config = prosodic.config
            self.meter = None
            if printout == None:
                printout = being.printout
            self.corpusRoot = corpusRoot
            self.corpusFiles = corpusFiles
            self.name = os.path.split(os.path.abspath(self.corpusRoot))[(-1)]
            self.foldername = self.name
            self.dir_results = prosodic.dir_results
            lang = lang or being.lang
        self.lang = lang
        for filename in glob.glob(os.path.join(corpusRoot, corpusFiles)):
            newtext = Text(filename, printout=printout)
            self.newchild(newtext)

        return

    def parse(self, meter=None, arbiter='Line'):
        if not meter and self.meter:
            meter = self.meter
        for text in self.children:
            text.parse(meter=meter, arbiter=arbiter)
            if not meter:
                self.meter = meter = text.meter

    def report(self, meter=None, include_bounded=False):
        for text in self.children:
            print ()
            print ('>> text:', text.name)
            text.report(meter=meter, include_bounded=include_bounded)

    def scansion(self, meter=None):
        for text in self.children:
            print (
             '>> text:', text.name)
            text.scansion(meter=meter)
            print ()

    def get_meter(self, meter=None):
        if not meter:
            child = self.children[0] if self.children else None
            if self.meter:
                meter = self.meter
            else:
                if child and hasattr(child, '_Text__bestparses') and child.__bestparses:
                    return self.get_meter(sorted(child.__bestparses.keys())[0])
                import Meter
                meter = Meter.genDefault()
        elif type(meter) in [str, str]:
            meter = self.config['meters'][meter]
        return meter

    def stats(self, meter=None, all_parses=False, funcs=['stats_lines', 'stats_lines_ot', 'stats_positions']):
        for funcname in funcs:
            func = getattr(self, funcname)
            for dx in func(meter=meter, all_parses=all_parses):
                yield dx

    def stats_lines(self, meter=None, all_parses=False):
        meter = self.get_meter(meter)

        def _writegen():
            for text in self.children:
                for dx in text.stats_lines(meter=meter):
                    dx['header'] = [
                     'text'] + dx['header']
                    yield dx

        ofn = os.path.join(self.dir_results, 'stats', 'corpora', self.name, self.name + '.lines.' + ('meter=' + meter.id if meter else 'unknown') + '.csv')
        if not os.path.exists(os.path.split(ofn)[0]):
            os.makedirs(os.path.split(ofn)[0])
        for dx in writegengen(ofn, _writegen):
            yield dx

        print (
         '>> saved:', ofn)

    def isParsed(self):
        return False not in [ child.isParsed() for child in self.children ]

    def stats_lines_ot(self, meter=None, all_parses=False):
        meter = self.get_meter(meter)

        def _writegen():
            for text in self.children:
                for dx in text.stats_lines_ot(meter=meter):
                    dx['header'] = [
                     'text'] + dx['header']
                    yield dx

        ofn = os.path.join(self.dir_results, 'stats', 'corpora', self.name, self.name + '.lines_ot.' + ('meter=' + meter.id if meter else 'unknown') + '.csv')
        if not os.path.exists(os.path.split(ofn)[0]):
            os.makedirs(os.path.split(ofn)[0])
        for dx in writegengen(ofn, _writegen):
            yield dx

        print (
         '>> saved:', ofn)

    def grid(self, nspace=10):
        grid = []
        for text in self.children:
            textgrid = text.grid(nspace=nspace)
            if textgrid:
                grid += ['## TEXT: ' + text.name + '\n\n' + textgrid]

        return ('\n\n\n').join(grid)

    def stats_positions(self, meter=None, all_parses=False):

        def _writegen():
            for text in self.children:
                for dx in text.stats_positions(meter=meter, all_parses=all_parses):
                    dx['header'] = [
                     'text'] + dx['header']
                    yield dx

        ofn = os.path.join(self.dir_results, 'stats', 'corpora', self.name, self.name + '.positions.csv')
        if not os.path.exists(os.path.split(ofn)[0]):
            os.makedirs(os.path.split(ofn)[0])
        for dx in writegengen(ofn, _writegen):
            yield dx

        print (
         '>> saved:', ofn)

    def sentences(self):
        return [ sent for text in self.children for sent in text.sentences() ]