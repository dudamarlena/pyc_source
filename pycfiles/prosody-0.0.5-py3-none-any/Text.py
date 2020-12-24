# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/ryan/DH/prosodic/lib/Text.py
# Compiled at: 2019-06-07 00:03:27
import sys, re, os, codecs, time
from Stanza import Stanza
from Line import Line
from Word import Word
from WordToken import WordToken
from entity import entity, being
from tools import *
from operator import itemgetter
from ipa import sampa2ipa
from functools import reduce
DASHES = [
 '--', '–', '—']
REPLACE_DASHES = True

class Text(entity):

    def __init__(self, filename=None, lang=None, meter=None, printout=None, limWord=False, linebreak=None, use_dict=True, fix_phons_novowel=True, stress_ambiguity=True):
        import prosodic
        self.featpaths = {}
        self.__parses = {}
        self.__bestparses = {}
        self.__boundParses = {}
        self.__parsed_ents = {}
        self.phrasebreak_punct = str(',;:.?!()[]{}<>')
        self.phrasebreak = prosodic.config['linebreak'].strip()
        self.limWord = limWord
        self.isFromFile = False
        self.feats = {}
        self.children = []
        self.isUnicode = True
        self.use_dict = use_dict
        self.fix_phons_novowel = fix_phons_novowel
        self.stress_ambiguity = stress_ambiguity
        self.dir_prosodic = prosodic.dir_prosodic
        self.dir_results = prosodic.dir_results
        self.dir_mtree = prosodic.dir_mtree
        self.config = prosodic.config
        self.meter = self.config['meters'][meter] if meter and meter in self.config['meters'] else None
        self._sentences = []
        if self.phrasebreak == 'line':
            pass
        else:
            if self.phrasebreak.startswith('line'):
                self.phrasebreak_punct = str(self.phrasebreak.replace('line', ''))
                self.phrasebreak = 'both'
            else:
                self.phrasebreak_punct = str(self.phrasebreak)
            if not filename:
                self.name = '[undefined]'
                self.isFromFile = False
                self.lang = (lang or self.set_lang)(filename) if 1 else lang
                self.dict = prosodic.dict[self.lang]
            elif os.path.exists(filename) and filename != '.':
                self.filename = filename
                self.name = filename.split('/').pop().strip()
                print ('>> loading text:', self.name)
                file = codecs.open(filename, encoding='utf-8', errors='replace')
                self.isFromFile = True
                self.lang = (lang or self.set_lang)(filename) if 1 else lang
                self.dict = prosodic.dict[self.lang]
                self.init_text(file)
            else:
                lines = filename.split('\n')
                self.name = noPunc(lines[0].lower())[:25].strip().replace(' ', '-')
                self.filename = lines[0].replace(' ', '_')[:100] + '.txt'
                self.isFromFile = False
                self.lang = (lang or self.set_lang)(filename) if 1 else lang
                self.dict = prosodic.dict[self.lang]
                self.init_text(lines)
            self.children = [ stanza for stanza in self.children if not stanza.empty() ]
            for stanza in self.children:
                stanza.children = [ line for line in stanza.children if not line.empty() ]

        return

    def sentences(self):
        return self._sentences

    def set_lang(self, filename):
        if not filename:
            return 'en'
        filename = os.path.basename(filename)
        import prosodic
        if self.isFromFile and len(filename) > 2 and filename[2] == '.' and filename[0:2] in prosodic.dict:
            lang = filename[0:2]
        elif prosodic.lang:
            lang = prosodic.lang
        else:
            lang = choose(prosodic.languages, "in what language is '" + self.name + "' written?")
            if not lang:
                lang = prosodic.languages[0]
                print '!! language choice not recognized. defaulting to: ' + lang
            else:
                lang = lang.pop()
        if lang not in prosodic.dict:
            lang0 = lang
            lang = prosodic.languages[0]
            print '!! language ' + lang0 + ' not recognized. defaulting to: ' + lang
        return lang

    def stats_lines(self, meter=None, all_parses=False, viols=True, save=True):
        meter = self.get_meter(meter)
        constraint_names = [ c.name_weight for c in meter.constraints ]
        header = ['line', 'parse', 'meter', 'num_sylls', 'num_parses', 'num_viols', 'score_viols'] + constraint_names

        def _writegen():
            for line in self.lines():
                dx = {'text': self.name, 'line': str(line), 'header': header}
                bp = line.bestParse(meter)
                ap = line.allParses(meter)
                dx['parse'] = bp.posString(viols=viols) if bp else ''
                dx['meter'] = bp.str_meter() if bp else ''
                dx['num_parses'] = len(ap)
                dx['num_viols'] = bp.totalCount if bp else ''
                dx['score_viols'] = bp.score() if bp else ''
                dx['num_sylls'] = bp.num_sylls if bp else ''
                for c in meter.constraints:
                    dx[c.name_weight] = bp.constraintScores[c] if bp and c in bp.constraintScores else ''

                yield dx

        name = self.name.replace('.txt', '')
        ofn = os.path.join(self.dir_results, 'stats', 'texts', name, name + '.lines.' + ('meter=' + meter.id if meter else 'unknown') + '.csv')
        if not os.path.exists(os.path.split(ofn)[0]):
            os.makedirs(os.path.split(ofn)[0])
        for dx in writegengen(ofn, _writegen, save=save):
            yield dx

        if save:
            print ('>> saved:', ofn)

    def stats_lines_ot_header(self, meter=None):
        meter = self.get_meter(meter)
        constraint_names = [ str(c) for c in meter.constraints ]
        header = ['line', 'parse', 'meter', 'num_viols', 'score_viols'] + constraint_names + ['num_line', 'num_stanza']
        return header

    def stats_lines_ot(self, meter=None, all_parses=False, viols=True, save=True):
        meter = self.get_meter(meter)
        header = self.stats_lines_ot_header(meter)

        def _writegen():
            for line in self.lines():
                ap = line.allParses(meter)
                if all_parses:
                    ap += line.boundParses(meter)
                for pi, parse in enumerate(ap):
                    dx = {'line': (pi or str)(line) if 1 else ''}
                    dx['text'] = self.name
                    dx['header'] = header
                    dx['parse'] = parse.posString(viols=viols)
                    dx['score_viols'] = parse.score()
                    dx['num_line'] = line.num
                    dx['num_stanza'] = line.parent.num
                    dx['num_viols'] = parse.totalCount
                    dx['meter'] = parse.str_meter()
                    for c in meter.constraints:
                        dx[str(c)] = parse.constraintCounts[c] if parse and c in parse.constraintScores and parse.constraintScores[c] else ''

                    yield dx

        name = self.name.replace('.txt', '')
        ofn = os.path.join(self.dir_results, 'stats', 'texts', name, name + '.lines_ot.' + ('meter=' + meter.id if meter else 'unknown') + '.csv')
        if not os.path.exists(os.path.split(ofn)[0]):
            os.makedirs(os.path.split(ofn)[0])
        for dx in writegengen(ofn, _writegen, save=save):
            if not save:
                del dx['header']
            yield dx

        if save:
            print ('>> saved:', ofn)

    def stats_positions(self, meter=None, all_parses=False):
        """Produce statistics from the parser"""
        parses = self.allParses(meter=meter) if all_parses else [ [parse] for parse in self.bestParses(meter=meter) ]
        dx = {}
        for parselist in parses:
            for parse in parselist:
                if not parse:
                    continue
                slot_i = 0
                for pos in parse.positions:
                    for slot in pos.slots:
                        slot_i += 1
                        feat_dicts = [
                         slot.feats, pos.constraintScores, pos.feats]
                        for feat_dict in feat_dicts:
                            for k, v in list(feat_dict.items()):
                                dk = (
                                 slot_i, str(k))
                                if dk not in dx:
                                    dx[dk] = []
                                dx[dk] += [v]

        def _writegen():
            for (slot_i, k), l in sorted(dx.items()):
                l2 = []
                for x in l:
                    if type(x) == bool:
                        x = 1 if x else 0
                    elif type(x) == type(None):
                        x = 0
                    elif type(x) in [str, str]:
                        continue
                    else:
                        x = float(x)
                    if x > 1:
                        x = 1
                    l2 += [x]

                if not l2:
                    continue
                avg = sum(l2) / float(len(l2))
                count = sum(l2)
                chances = len(l2)
                odx = {'slot_num': slot_i, 'statistic': k, 'average': avg, 'count': count, 'chances': chances, 'text': self.name}
                odx['header'] = [
                 'slot_num', 'statistic', 'count', 'chances', 'average']
                yield odx

            return

        name = self.name.replace('.txt', '')
        ofn = os.path.join(self.dir_results, 'stats', 'texts', name, name + '.positions.csv')
        if not os.path.exists(os.path.split(ofn)[0]):
            os.makedirs(os.path.split(ofn)[0])
        for dx in writegengen(ofn, _writegen):
            yield dx

        print (
         '>> saved:', ofn)

    def stats(self, meter=None, all_parses=False, funcs=['stats_lines', 'stats_lines_ot', 'stats_positions']):
        for funcname in funcs:
            func = getattr(self, funcname)
            for dx in func(meter=meter, all_parses=all_parses):
                yield dx

    def init_text(self, lines_or_file):
        stanza = self.newchild()
        stanza.num = stanza_num = 1
        line = stanza.newchild()
        line.num = line_num = 1
        numwords = 0
        recentpunct = True
        import prosodic
        tokenizer = prosodic.config['tokenizer'].replace('\\\\', '\\')
        for ln in lines_or_file:
            if REPLACE_DASHES:
                for dash in DASHES:
                    ln = ln.replace(dash, ' ' + dash + ' ')

            ln = ln.strip()
            if self.limWord and numwords > self.limWord:
                break
            toks = re.findall(tokenizer, ln.strip(), flags=re.UNICODE) if self.isUnicode else re.findall(tokenizer, ln.strip())
            toks = [ tok.strip() for tok in toks if tok.strip() ]
            numtoks = len(toks)
            if not ln or numtoks < 1:
                if not stanza.empty():
                    stanza.finish()
                continue
            for toknum, tok in enumerate(toks):
                punct0, tok, punct = gleanPunc2(tok)
                if stanza.finished:
                    stanza = self.newchild()
                    stanza.num = stanza_num = stanza_num + 1
                if line.finished:
                    line = stanza.newchild()
                    line.num = line_num = line_num + 1
                if punct0:
                    wordtok = WordToken([], token=punct0, is_punct=True, line=line)
                    line.newchild(wordtok)
                if tok:
                    newwords = self.dict.get(tok, stress_ambiguity=self.stress_ambiguity)
                    wordtok = WordToken(newwords, token=tok, is_punct=False, line=line)
                    line.newchild(wordtok)
                    numwords += 1
                    self.om(str(numwords).zfill(6) + '\t' + str(newwords[0].output_minform()))
                if punct:
                    wordtok = WordToken([], token=punct, is_punct=True, line=line)
                    line.newchild(wordtok)
                if punct and len(line.children) and self.phrasebreak != 'line':
                    if self.phrasebreak_punct.find(punct) > -1:
                        line.finish()

            if self.phrasebreak == 'both' or self.phrasebreak == 'line':
                line.finish()

        if self.config.get('parse_using_metrical_tree', False) and self.lang == 'en':
            import time
            then = time.time()
            print '>> parsing text using MetricalTree (because "parse_using_metrical_tree" setting activated in config.py)...'
            try:
                self.parse_mtree()
            except ImportError as e:
                print (
                 '!! text not parsed because python module missing:', str(e).split()[(-1)])
                print ('!! to install, run: pip install', str(e).split()[(-1)])
                print "!! if you don't have pip installed, run this script: <https://bootstrap.pypa.io/get-pip.py>"
                print ()
            except LookupError as e:
                emsg = str(e)
                if 'Resource' in emsg and 'punkt' in emsg and 'not found' in emsg:
                    print '!! text not parsed because NLTK missing needed data: punkt'
                    print '!! to install, run: python -c "import nltk; nltk.download(\'punkt\')"'
                    print ()
                elif 'stanford-parser.jar' in emsg:
                    import prosodic
                    print '!! text not parsed because Stanford NLP Parser not installed'
                    print '!! to install, run: python prosodic.py install stanford_parser'
                    print "!! if that doesn't work:"
                    print '!! \t1) download: http://nlp.stanford.edu/software/stanford-parser-full-2015-04-20.zip'
                    print '!! \t2) unzip it'
                    print ('!! \t3) move the unzipped directory to:', self.dir_mtree + '/Stanford Library/stanford-parser-full-2015-04-20/')
                    print ()
                else:
                    print '!! text not parsed for unknown reason!'
                    print '!! error message received:'
                    print emsg
                    print ()
            except AssertionError:
                print "This is a bug in PROSODIC that is Ryan Heuser's fault. [Bug ID: Assertion_MTree]"
                print 'Please kindly report it to: https://github.com/quadrismegistus/prosodic/issues'
                print ()
            except Exception as e:
                emsg = str(e)
                print '!! text not parsed for unknown reason!'
                print '!! error message received:'
                print emsg
                print ()

            now = time.time()
            print ('>> done:', round(now - then, 2), 'seconds')

    def parse_mtree(self):
        if self.lang != 'en':
            raise Exception('MetricalTree parsing only works currently for English text.')
        import metricaltree as mtree
        mtree.set_paths(self.dir_mtree)
        wordtoks = self.wordtokens()
        toks = [ wtok.token for wtok in wordtoks ]
        pauses = mtree.pause_splitter_tokens(toks)
        sents = []
        for pause in pauses:
            sents.extend(mtree.split_sentences_from_tokens(pause))

        parser = mtree.return_parser(self.dir_mtree)
        trees = list(parser.lex_parse_sents(sents, verbose=False))
        stats = parser.get_stats(trees, arto=True, format_pandas=False)
        assert len(stats) == len(wordtoks)
        sents = []
        sent = []
        sent_id = None
        for wTok, wStat in zip(wordtoks, stats):
            if sent_id != wStat['sidx']:
                sent_id = wStat['sidx']
                if sent:
                    sents += [sent]
                sent = []
            sent += [wTok]
            if not hasattr(wTok, 'feats'):
                wTok.feats = {}
            for k, v in list(wStat.items()):
                if k in mtree.INFO_DO_NOT_STORE:
                    continue
                wTok.feats[k] = v

        if sent:
            sents += [sent]
        assert len(sents) == len(trees)
        from Sentence import Sentence
        for sent, tree in zip(sents, trees):
            sentobj = Sentence(sent, tree)
            self._sentences += [sentobj]

        import numpy as np
        for line in self.lines():
            wtoks = line.children
            stresses = [ wtok.feats['norm_mean'] for wtok in wtoks if not np.isnan(wtok.feats['norm_mean']) ]
            max_stress = float(max(stresses))
            min_stress = float(min(stresses))
            for wtok in wtoks:
                wtok.feats['norm_mean_line'] = (wtok.feats['norm_mean'] - min_stress) / (max_stress - min_stress) if max_stress else np.nan

            stresses = [ wtok.feats['mean'] for wtok in wtoks if not np.isnan(wtok.feats['mean']) ]
            min_stress = float(min(stresses))
            diff = 1.0 - min_stress
            for wtok in wtoks:
                wtok.feats['mean_line'] = wtok.feats['mean'] + diff

        return

    def grid(self, nspace=10):
        return ('\n\n').join(sent.grid(nspace=nspace) for sent in self.sentences())

    def clear_parses(self):
        self.__parses = {}
        self.__bestparses = {}
        self.__boundParses = {}
        self.__parsed_ents = {}

    def iparse(self, meter=None, num_processes=1, arbiter='Line', line_lim=None):
        """Parse this text metrically, yielding it line by line."""
        from Meter import Meter, genDefault, parse_ent, parse_ent_mp
        import multiprocessing as mp
        meter = self.get_meter(meter)
        self.__parses[meter.id] = []
        self.__bestparses[meter.id] = []
        self.__boundParses[meter.id] = []
        self.__parsed_ents[meter.id] = []
        lines = self.lines()
        lines = lines[:line_lim]
        numlines = len(lines)
        init = self
        ents = self.ents(arbiter)
        smax = self.config.get('line_maxsylls', 100)
        smin = self.config.get('line_minsylls', 0)
        ents = [ e for e in ents if e.num_syll >= smin and e.num_syll <= smax ]
        self.scansion_prepare(meter=meter, conscious=True)
        numents = len(ents)
        toprint = being.config['print_to_screen']
        objects = [ (ent, meter, init, False) for ent in ents ]
        if num_processes > 1:
            print '!! MULTIPROCESSING PARSING IS NOT WORKING YET !!'
            pool = mp.Pool(num_processes)
            jobs = [ pool.apply_async(parse_ent_mp, (x,)) for x in objects ]
            for j in jobs:
                print j.get()
                yield j.get()

        else:
            now = time.time()
            clock_snum = 0
            for ei, objectx in enumerate(objects):
                clock_snum += objectx[0].num_syll
                if ei and not ei % 100:
                    nownow = time.time()
                    if being.config['print_to_screen']:
                        print (
                         '>> parsing line #', ei, 'of', numents, 'lines', '[', round(float(clock_snum / (nownow - now)), 2), 'syllables/second', ']')
                    now = nownow
                    clock_snum = 0
                yield parse_ent_mp(objectx)

        if being.config['print_to_screen']:
            print (
             '>> parsing complete in:', time.time() - now, 'seconds')

    def parse(self, meter=None, arbiter='Line', line_lim=None):
        list(self.iparse(meter=meter, arbiter=arbiter, line_lim=line_lim))

    def parse1(self, meter=None, arbiter='Line'):
        """@DEPRECATED
                Parse this text metrically."""
        from Meter import Meter, genDefault, parse_ent
        meter = self.get_meter(meter)
        if self.isFromFile:
            print ('>> parsing', self.name, 'with meter:', meter.id)
        self.meter = meter
        self.__parses[meter.id] = []
        self.__bestparses[meter.id] = []
        self.__boundParses[meter.id] = []
        self.__parsed_ents[meter.id] = []
        init = self
        ents = self.ents(arbiter)
        smax = self.config.get('line_maxsylls', 100)
        smin = self.config.get('line_minsylls', 0)
        ents = [ e for e in ents if e.num_syll >= smin and e.num_syll <= smax ]
        self.scansion_prepare(meter=meter, conscious=True)
        numents = len(ents)
        now = time.time()
        clock_snum = 0
        for ei, ent in enumerate(ents):
            clock_snum += ent.num_syll
            if ei and not ei % 100:
                nownow = time.time()
                print ('>> parsing line #', ei, 'of', numents, 'lines', '[', round(float(clock_snum / (nownow - now)), 2), 'syllables/second', ']')
                now = nownow
                clock_snum = 0
            ent.parse(meter, init=init)
            self.__parses[meter.id].append(ent.allParses(meter))
            self.__bestparses[meter.id].append(ent.bestParse(meter))
            self.__boundParses[meter.id].append(ent.boundParses(meter))
            self.__parsed_ents[meter.id].append(ent)
            ent.scansion(meter=meter, conscious=True)

        if being.config['print_to_screen']:
            print ()

    def iparse2line(self, i, meter=None):
        meter = self.get_meter(meter)
        return self.__parsed_ents[meter.id][i]

    def isParsed(self):
        return bool(hasattr(self, '_Text__bestparses') and self.__bestparses)

    @property
    def numSyllables(self):
        if self.isParsed:
            num_syll = 0
            for bp in self.bestParses():
                for pos in bp.positions:
                    num_syll += len(pos.slots)

        else:
            num_syll = len(self.syllables())
        return num_syll

    def scansion(self, meter=None, conscious=False):
        """Print out the parses and their violations in scansion format."""
        meter = self.get_meter(meter)
        self.scansion_prepare(meter=meter, conscious=conscious)
        for line in self.lines():
            try:
                line.scansion(meter=meter, conscious=conscious)
            except AttributeError:
                print '!!! Line skipped [Unknown word]:'
                print line
                print line.words()
                print ()

    def allParsesByLine(self, meter=None):
        parses = self.allParses(meter=meter)
        for parse_product in product(*parses):
            yield parse_product

    def allParses(self, meter=None, include_bounded=False, one_per_meter=True):
        """Return a list of lists of parses."""
        meter = self.get_meter(meter)
        try:
            parses = self.__parses[meter.id]
            if one_per_meter:
                toreturn = []
                for _parses in parses:
                    sofar = set()
                    _parses2 = []
                    for _p in _parses:
                        _pm = _p.str_meter()
                        if _pm not in sofar:
                            sofar |= {_pm}
                            if _p.isBounded and _p.boundedBy.str_meter() == _pm:
                                pass
                            else:
                                _parses2 += [_p]

                    toreturn += [_parses2]

                parses = toreturn
            if include_bounded:
                boundedParses = self.boundParses(meter)
                return [ bp + boundp for bp, boundp in zip(toreturn, boundedParses) ]
            return parses
        except (KeyError, IndexError) as e:
            return []

    def get_meter(self, meter=None):
        if not meter:
            if self.meter:
                meter = self.meter
            else:
                if hasattr(self, '_Text__bestparses') and self.__bestparses:
                    return self.get_meter(sorted(self.__bestparses.keys())[0])
                import Meter
                meter = Meter.genDefault()
        elif type(meter) in [str, str]:
            meter = self.config['meters'][meter]
        if meter.id not in self.config['meters']:
            self.config['meters'][meter.id] = meter
        return meter

    def report(self, meter=None, include_bounded=False, reverse=True):
        meter = self.get_meter(meter)
        return entity.report(self, meter=meter, include_bounded=include_bounded, reverse=reverse)

    def bestParses(self, meter=None):
        """Return a list of the best parse per line."""
        meter = self.get_meter(meter)
        try:
            return self.__bestparses[meter.id]
        except (KeyError, IndexError) as e:
            return []

    def boundParses(self, meter=None, include_stressbounds=False):
        """Return a list of the best parse per line."""
        meter = self.get_meter(meter)
        try:
            toreturn = []
            for _parses in self.__boundParses[meter.id]:
                sofar = set()
                _parses2 = []
                for _p in _parses:
                    _pm = _p.str_meter()
                    if _pm not in sofar:
                        if _p.isBounded and _p.boundedBy.str_meter() == _pm:
                            pass
                        else:
                            sofar |= {_pm}
                            _parses2 += [_p]

                toreturn += [_parses2]

            return toreturn
        except (KeyError, IndexError) as e:
            return [[]]

    def viol_words(self):
        bp = self.bestParses()
        if not bp:
            return ''
        constraintd = {}
        for parse in bp:
            for mpos in parse.positions:
                viold = False
                words = set([ slot.word.token for slot in mpos.slots ])
                for ck, cv in list(mpos.constraintScores.items()):
                    if not cv:
                        continue
                    ckk = ck.name.replace('.', '_')
                    if ckk not in constraintd:
                        constraintd[ckk] = set()
                    constraintd[ckk] |= words

        for k in constraintd:
            constraintd[k] = list(constraintd[k])

        return constraintd

    def parsed_words(self):
        bp = self.bestParses()
        if not bp:
            return []
        else:
            wordNow = None
            words = []
            for parse in bp:
                for mpos in parse.positions:
                    for mslot in mpos.slots:
                        word = mslot.i_word
                        if wordNow is word:
                            continue
                        words += [word]
                        wordNow = word

            return words

    def parse_strs(self, text=True, viols=True, text_poly=False):
        for parses in self.allParsesByLine():
            yield self.parse_str(text=text, viols=viols, text_poly=text_poly, parses=parses)

    def parse_str(self, text=True, viols=True, text_poly=False, parses=False):
        if not parses:
            bp = self.bestParses() if 1 else parses
            return bp or ''
        all_strs = []
        letters = [
         'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R']
        for parse in bp:
            parse_strs = []
            for mpos in parse.positions:
                viold = False
                for ck, cv in list(mpos.constraintScores.items()):
                    if cv:
                        viold = True
                        break

                if text_poly:
                    word_pos = [ slot.wordpos[0] for slot in mpos.slots ]
                    mpos_letters = [ letters[(pos - 1)] for pos in word_pos ]
                    if not mpos.isStrong:
                        mpos_letters = [ letter.lower() for letter in mpos_letters ]
                    mpos_str = ('.').join(mpos_letters)
                elif not text:
                    mpos_str = mpos.mstr
                else:
                    mpos_str = mpos.token
                if viols and viold:
                    mpos_str += '*'
                parse_strs += [mpos_str]

            all_strs += [('|').join(parse_strs)]

        return ('||').join(all_strs)

    @property
    def numBeats(self):
        parse_str = self.parse_str(text=False, viols=False)
        s_feet = [ x for x in parse_str.split('|') if x.startswith('s') ]
        return len(s_feet)

    @property
    def constraintd(self):
        return self.constraintViolations(self, normalize=True)

    def constraintViolations--- This code section failed: ---

 L. 790         0  LOAD_FAST             0  'self'
                3  LOAD_ATTR             0  'bestParses'
                6  CALL_FUNCTION_0       0  None
                9  STORE_FAST            3  'bp'

 L. 791        12  BUILD_MAP_0           0  None
               15  STORE_FAST            4  'viold'

 L. 792        18  LOAD_FAST             3  'bp'
               21  POP_JUMP_IF_TRUE     28  'to 28'
               24  BUILD_MAP_0           0  None
               27  RETURN_END_IF    
             28_0  COME_FROM            21  '21'

 L. 793        28  BUILD_LIST_0          0 
               31  STORE_FAST            5  'mstrs'

 L. 794        34  SETUP_LOOP          155  'to 192'
               37  LOAD_FAST             3  'bp'
               40  GET_ITER         
               41  FOR_ITER            147  'to 191'
               44  STORE_FAST            6  'parse'

 L. 795        47  SETUP_LOOP          138  'to 188'
               50  LOAD_FAST             6  'parse'
               53  LOAD_ATTR             1  'positions'
               56  GET_ITER         
               57  FOR_ITER            127  'to 187'
               60  STORE_FAST            7  'mpos'

 L. 796        63  SETUP_LOOP          118  'to 184'
               66  LOAD_GLOBAL           2  'list'
               69  LOAD_FAST             7  'mpos'
               72  LOAD_ATTR             3  'constraintScores'
               75  LOAD_ATTR             4  'items'
               78  CALL_FUNCTION_0       0  None
               81  CALL_FUNCTION_1       1  None
               84  GET_ITER         
               85  FOR_ITER             95  'to 183'
               88  UNPACK_SEQUENCE_2     2 
               91  STORE_FAST            8  'ck'
               94  STORE_FAST            9  'cv'

 L. 797        97  LOAD_FAST             8  'ck'
              100  LOAD_ATTR             5  'name'
              103  STORE_FAST            8  'ck'

 L. 798       106  LOAD_FAST             8  'ck'
              109  LOAD_FAST             4  'viold'
              112  COMPARE_OP            7  not-in
              115  POP_JUMP_IF_FALSE   131  'to 131'
              118  BUILD_LIST_0          0 
              121  LOAD_FAST             4  'viold'
              124  LOAD_FAST             8  'ck'
              127  STORE_SUBSCR     
              128  JUMP_FORWARD          0  'to 131'
            131_0  COME_FROM           128  '128'

 L. 799       131  LOAD_FAST             9  'cv'
              134  POP_JUMP_IF_FALSE   155  'to 155'
              137  LOAD_FAST             2  'use_weights'
              140  POP_JUMP_IF_TRUE    149  'to 149'
              143  LOAD_FAST             9  'cv'
              146  JUMP_ABSOLUTE       158  'to 158'
              149  LOAD_CONST               1
              152  JUMP_FORWARD          3  'to 158'
              155  LOAD_CONST               0
            158_0  COME_FROM           152  '152'
              158  STORE_FAST           10  'val'

 L. 800       161  LOAD_FAST             4  'viold'
              164  LOAD_FAST             8  'ck'
              167  DUP_TOPX_2            2  None
              170  BINARY_SUBSCR    
              171  LOAD_FAST            10  'val'
              174  BUILD_LIST_1          1 
              177  INPLACE_ADD      
              178  ROT_THREE        
              179  STORE_SUBSCR     
              180  JUMP_BACK            85  'to 85'
              183  POP_BLOCK        
            184_0  COME_FROM            63  '63'
              184  JUMP_BACK            57  'to 57'
              187  POP_BLOCK        
            188_0  COME_FROM            47  '47'
              188  JUMP_BACK            41  'to 41'
              191  POP_BLOCK        
            192_0  COME_FROM            34  '34'

 L. 802       192  SETUP_LOOP           74  'to 269'
              195  LOAD_FAST             4  'viold'
              198  GET_ITER         
              199  FOR_ITER             66  'to 268'
              202  STORE_FAST            8  'ck'

 L. 803       205  LOAD_FAST             4  'viold'
              208  LOAD_FAST             8  'ck'
              211  BINARY_SUBSCR    
              212  STORE_FAST           11  'lv'

 L. 804       215  LOAD_FAST             1  'normalize'
              218  POP_JUMP_IF_FALSE   249  'to 249'
              221  LOAD_GLOBAL           6  'sum'
              224  LOAD_FAST            11  'lv'
              227  CALL_FUNCTION_1       1  None
              230  LOAD_GLOBAL           7  'float'
              233  LOAD_GLOBAL           8  'len'
              236  LOAD_FAST            11  'lv'
              239  CALL_FUNCTION_1       1  None
              242  CALL_FUNCTION_1       1  None
              245  BINARY_DIVIDE    
              246  JUMP_FORWARD          9  'to 258'
              249  LOAD_GLOBAL           6  'sum'
              252  LOAD_FAST            11  'lv'
              255  CALL_FUNCTION_1       1  None
            258_0  COME_FROM           246  '246'
              258  LOAD_FAST             4  'viold'
              261  LOAD_FAST             8  'ck'
              264  STORE_SUBSCR     
              265  JUMP_BACK           199  'to 199'
              268  POP_BLOCK        
            269_0  COME_FROM           192  '192'

 L. 806       269  LOAD_FAST             4  'viold'
              272  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `STORE_FAST' instruction at offset 158

    @property
    def ambiguity(self):
        ap = self.allParses()
        line_numparses = []
        line_parselen = 0
        if not ap:
            return 0
        for parselist in ap:
            numparses = len(parselist)
            line_numparses += [numparses]

        import operator
        ambigx = reduce(operator.mul, line_numparses, 1)
        return ambigx

    def get_parses(self, meter):
        return self.__parses[meter.id]

    def givebirth(self):
        """Return an empty Stanza."""
        stanza = Stanza()
        return stanza

    def validlines(self):
        """Return all lines within which Prosodic understood all words."""
        return [ ln for ln in self.lines() if not ln.isBroken() and not ln.ignoreMe ]

    def __repr__(self):
        return '<Text.' + str(self.name) + '> (' + str(len(self.words())) + ' words)'